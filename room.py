import chromadb
import pandas as pd
from datetime import datetime
import re
from colorama import Fore
import os
import torch
from transformers import AutoTokenizer, AutoModel
import numpy as np

#local imports
from agentic_network import ask_model, get_agent_description
from utils import get_system_prompt, get_agent_display_names
from kun import known_user_names

ROOMS_DIR = r"E:\Agents\OPSIIE_Generated_Rooms"
os.makedirs(ROOMS_DIR, exist_ok=True)

# Get the display names at module level
AGENT_DISPLAY_NAMES = get_agent_display_names()

def clean_room_name(prompt):
    """Clean prompt to create valid filename/collection name."""
    name = re.sub(r'[^a-zA-Z0-9_]', '_', prompt.lower())
    return name[:50]  # Limit length

class Room:
    def __init__(self, agents, system_prompt, get_opsie_response_func):
        self.agents = ['opsie'] + [a.strip().lower() for a in agents]
        self.original_prompt = system_prompt
        
        # Get user name (fallback to "User" if not found)
        user_name = "User"  # Default fallback
        for name, data in known_user_names.items():
            if data.get('is_current_user'):
                user_name = data.get('call_name', name)
                break
        
        # Build comprehensive room context
        agent_descriptions = []
        
        # Add OPSIE's description
        agent_descriptions.append(f"OPSIE: {get_system_prompt()}")
        
        # Add other agents' descriptions
        for agent in agents:
            desc = get_agent_description(agent)
            if desc:
                agent_descriptions.append(f"{AGENT_DISPLAY_NAMES[agent]}: {desc}")
        
        # Create newline separator
        nl = '\n'
        double_nl = '\n\n'
        
        # Combine into full system prompt
        self.system_prompt = (
            f"You are summoned by {user_name} in a temporal room alongside " +
            f"{', '.join(AGENT_DISPLAY_NAMES[a] for a in agents)}. " +
            f"The user wants to discuss: {system_prompt}" + double_nl +
            "For context here are some background info for the task force created for this subject:" + double_nl +
            double_nl.join(agent_descriptions) + double_nl +
            "Try to work together in a collaborative fashion to address user needs, evaluate each other, " +
            "and give feedback about each others assumptions, propositions, or statements, always having " +
            f"as compass the initial topic: {system_prompt}."
        )
        
        self.room_name = f"room_{clean_room_name(system_prompt)}"
        self.client = chromadb.Client()
        self.collection = self.client.create_collection(self.room_name)
        self.conversation_history = []
        self.tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
        self.model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
        self.get_opsie_response = get_opsie_response_func
        
    def get_embedding(self, text):
        """Get embeddings for response comparison."""
        inputs = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).numpy()

    def response_similarity(self, resp1, resp2):
        """Calculate cosine similarity between responses."""
        emb1 = self.get_embedding(resp1)
        emb2 = self.get_embedding(resp2)
        return np.dot(emb1[0], emb2[0]) / (np.linalg.norm(emb1[0]) * np.linalg.norm(emb2[0]))

    def _select_best_response(self, responses):
        """Select best response based on multiple criteria."""
        if len(responses) == 1:
            return responses[0]

        # Score each response
        scores = []
        for i, resp in enumerate(responses):
            score = 0
            response_text = resp['response']
            agent = resp['agent']
            
            # Length score (prefer medium-length responses)
            words = len(response_text.split())
            if 50 <= words <= 200:
                score += 1
            
            # Similarity score (prefer unique responses)
            similarity_sum = 0
            for j, other_resp in enumerate(responses):
                if i != j:
                    similarity = self.response_similarity(response_text, other_resp['response'])
                    similarity_sum += similarity
            avg_similarity = similarity_sum / (len(responses) - 1)
            score += (1 - avg_similarity) * 2  # Double weight for uniqueness
            
            # Add interaction scoring
            if len(self.conversation_history) > 0:
                last_speaker = self.conversation_history[-1]['agent']
                # Encourage different agents to speak (variety)
                if agent != last_speaker:
                    score += 0.5
                
                # Check if this agent was directly referenced
                if last_speaker in response_text.lower():
                    score += 0.3
                    
                # Check if response references previous context
                for entry in self.conversation_history[-3:]:
                    if any(phrase in response_text.lower() for phrase in entry['response'].lower().split('.')):
                        score += 0.2

            # Specific keywords/phrases score
            relevant_keywords = ['analysis', 'recommendation', 'solution', 'approach', 'strategy']
            for keyword in relevant_keywords:
                if keyword.lower() in response_text.lower():
                    score += 0.2
            
            scores.append((score, resp))
        
        # Return response with highest score
        return max(scores, key=lambda x: x[0])[1]

    def add_conversation(self, user_prompt, agent_name, response):
        """Add conversation to both ChromaDB and history."""
        timestamp = datetime.now().isoformat()
        
        # Add to ChromaDB
        self.collection.add(
            documents=[response],
            metadatas=[{
                "timestamp": timestamp,
                "agent": agent_name,
                "prompt": user_prompt
            }],
            ids=[f"{timestamp}_{agent_name}"]
        )
        
        # Add to history
        self.conversation_history.append({
            "timestamp": timestamp,
            "prompt": user_prompt,
            "agent": agent_name,
            "response": response
        })

    def get_addressed_agent(self, prompt):
        """Determine if a specific agent is being addressed."""
        prompt_lower = prompt.lower()
        for agent in self.agents:
            if prompt_lower.startswith(f"{agent} ") or prompt_lower.startswith(f"{agent},"):
                return agent
        return None

    def get_conversation_context(self):
        """Get formatted conversation history for context."""
        context_entries = []
        for entry in self.conversation_history[-20:]:
            agent_display_name = AGENT_DISPLAY_NAMES[entry['agent']]
            context_entries.append(f"{agent_display_name}: {entry['response']}")
        return "\n".join(context_entries)

    def get_best_response(self, prompt):
        """Get responses from agents based on context."""
        addressed_agent = self.get_addressed_agent(prompt)
        conv_context = self.get_conversation_context()
        
        # Build more detailed agent-aware context
        agent_context = (
            f"You are participating in a multi-agent conversation.\n\n"
            f"YOUR ROLE: {AGENT_DISPLAY_NAMES[addressed_agent if addressed_agent else self.agents[0]]}\n"
            f"OTHER PARTICIPANTS:\n" +
            "\n".join([f"- {AGENT_DISPLAY_NAMES[a]}" for a in self.agents if a != (addressed_agent or self.agents[0])]) +
            f"\n\nCONVERSATION HISTORY:\n{conv_context}\n\n"
            f"CURRENT TOPIC: {self.original_prompt}\n\n"
            f"USER QUERY: {prompt}"
        )

        if addressed_agent:
            # Direct query to specific agent
            if addressed_agent == 'opsie':
                response = self.get_opsie_response(agent_context, self.system_prompt)
                self.add_conversation(prompt, addressed_agent, response)
                return {'agent': 'opsie', 'response': response}
            else:
                response = ask_model(addressed_agent, agent_context, suppress_output=True)
                self.add_conversation(prompt, addressed_agent, response)
                return {'agent': addressed_agent, 'response': response}
        else:
            # Get responses from all agents and select best one
            responses = []
            for agent in self.agents:
                try:
                    if agent == 'opsie':
                        response = self.get_opsie_response(agent_context, self.system_prompt)
                    else:
                        response = ask_model(agent, agent_context, suppress_output=True)
                    
                    responses.append({
                        'agent': agent,
                        'response': response
                    })
                except Exception as e:
                    print(Fore.RED + f"Error getting response from {agent}: {str(e)}")
                    continue
            
            if not responses:
                return {'agent': 'system', 'response': "Error: No agents were able to respond"}
            
            best_response = self._select_best_response(responses)
            self.add_conversation(prompt, best_response['agent'], best_response['response'])
            return best_response

    def save_to_csv(self):
        """Save room conversation to CSV."""
        df = pd.DataFrame(self.conversation_history)
        filename = os.path.join(ROOMS_DIR, f"{self.room_name}.csv")
        df.to_csv(filename, index=False)
        return filename

    def close(self):
        """Close the room and optionally save history."""
        save = input(Fore.YELLOW + "Would you like to save this room's conversation? (Y/N): ").lower()
        
        if save == 'y':
            filename = self.save_to_csv()
            print(Fore.GREEN + f"Conversation saved to {filename}")
        
        # Clean up ChromaDB collection
        self.client.delete_collection(self.room_name)

    def handle_agent_interruption(self, current_agent, response_text):
        """Check if another agent should interrupt based on expertise."""
        for agent in self.agents:
            if agent == current_agent:
                continue
            
            # Get agent's expertise keywords
            expertise = self.get_agent_expertise(agent)
            
            # Check if response touches on another agent's expertise
            if any(keyword in response_text.lower() for keyword in expertise):
                followup = ask_model(agent, 
                    f"The current response mentions your area of expertise. "
                    f"Original response: {response_text}\n\n"
                    "If you have something important to add, provide a brief interjection. "
                    "Otherwise, return empty.", suppress_output=True)
                
                if followup.strip():
                    return {'agent': agent, 'response': followup}
        
        return None

    def get_agent_color(self, agent_name):
        """Get the appropriate color for each agent."""
        colors = {
            'opsie': Fore.LIGHTGREEN_EX,
            'g1': Fore.LIGHTRED_EX,
            'nyx': Fore.LIGHTBLUE_EX,
            'kronos': Fore.LIGHTYELLOW_EX 
        }
        return colors.get(agent_name, Fore.WHITE)

    def get_agent_expertise(self, agent):
        """Get expertise keywords for each agent."""
        expertise = {
            'opsie': ['ai', 'machine learning', 'neural networks', 'deep learning'],
            'g1': ['quantum', 'technology', 'systems', 'technical'],
            'nyx': ['blockchain', 'biotech', 'neurotech', 'dna'],
            'kronos': ['audit', 'financial', 'greek', 'corporate', 'legal', 'compliance']  # Add Kronos expertise
        }
        return expertise.get(agent, [])