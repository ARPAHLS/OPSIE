import os
import requests
import websockets
import asyncio
import base64
import json
from dotenv import load_dotenv
from colorama import Fore
import google.generativeai as genai
import pyaudio
import aiohttp

# *** AGENTIC NETWORK ***
# Connection to AI models | APIs | and more

# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ORG_ID = os.getenv('ORG_ID')
NYX_ASSISTANT_ID = os.getenv('NYX_ASSISTANT_ID')

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
G1_VOICE_LIVE = os.getenv('G1_VOICE_LIVE') 
KRONOS_LIVE = os.getenv('KRONOS_LIVE') 
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)

# Audio settings as per ElevenLabs requirements
AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 4000  # 0.25 seconds worth of samples at 16kHz
ENCODING = 'pcm_16000'

class G1LiveVoice:
    def __init__(self):
        self.websocket = None
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.output_stream = None
        self.conversation_id = None
        self.running = True
        
    async def connect(self):
        """Establish WebSocket connection with ElevenLabs."""
        url = f"wss://api.elevenlabs.io/v1/convai/conversation?agent_id={G1_VOICE_LIVE}"
        self.websocket = await websockets.connect(url)
        
        metadata = await self.websocket.recv()
        metadata = json.loads(metadata)
        if metadata['type'] == 'conversation_initiation_metadata':
            self.conversation_id = metadata['conversation_initiation_metadata_event']['conversation_id']
    
    async def start_audio_stream(self):
        """Start audio input and output streams."""
        self.stream = self.audio.open(
            format=AUDIO_FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
            input_device_index=None,
            stream_callback=None
        )
        
        self.output_stream = self.audio.open(
            format=AUDIO_FORMAT,
            channels=CHANNELS,
            rate=RATE,
            output=True,
            frames_per_buffer=CHUNK,
            output_device_index=None
        )
    
    async def handle_server_messages(self):
        """Handle incoming server messages."""
        while self.running:
            try:
                message = await self.websocket.recv()
                message = json.loads(message)
                
                if message['type'] == 'ping':
                    await self.websocket.send(json.dumps({
                        "type": "pong",
                        "event_id": message['ping_event']['event_id']
                    }))
                
                elif message['type'] == 'audio':
                    audio_data = base64.b64decode(message['audio_event']['audio_base_64'])
                    self.output_stream.write(audio_data)
                
                elif message['type'] == 'agent_response':
                    print(Fore.LIGHTRED_EX + f"G1 Black: {message['agent_response_event']['agent_response']}")
                    print(Fore.LIGHTCYAN_EX + "Listening for your input...")
                
            except websockets.exceptions.ConnectionClosed:
                break
            except Exception as e:
                if self.running:  # Only print error if not shutting down
                    print(Fore.RED + f"Error in message handling: {str(e)}")
                break
    
    async def send_audio_chunk(self):
        """Record and send audio chunk."""
        if not self.running:
            return
            
        try:
            data = self.stream.read(CHUNK, exception_on_overflow=False)
            base64_audio = base64.b64encode(data).decode('utf-8')
            await self.websocket.send(json.dumps({
                "user_audio_chunk": base64_audio
            }))
        except Exception as e:
            if self.running:  # Only print error if not shutting down
                print(Fore.RED + f"Error sending audio: {str(e)}")
    
    async def close(self):
        """Clean up resources."""
        self.running = False
        try:
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
            if self.output_stream:
                self.output_stream.stop_stream()
                self.output_stream.close()
            if self.websocket:
                await self.websocket.close()
            self.audio.terminate()
        except Exception as e:
            print(Fore.RED + f"Error during cleanup: {str(e)}")

class KronosLiveVoice:
    def __init__(self):
        self.websocket = None
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.output_stream = None  # Add persistent output stream
        self.conversation_id = None
        self.running = True
        
    async def connect(self):
        """Establish WebSocket connection with ElevenLabs."""
        url = f"wss://api.elevenlabs.io/v1/convai/conversation?agent_id={KRONOS_LIVE}"
        self.websocket = await websockets.connect(url)
        
        metadata = await self.websocket.recv()
        metadata = json.loads(metadata)
        if metadata['type'] == 'conversation_initiation_metadata':
            self.conversation_id = metadata['conversation_initiation_metadata_event']['conversation_id']
    
    async def start_audio_stream(self):
        """Start audio input and output streams."""
        self.stream = self.audio.open(
            format=AUDIO_FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
            input_device_index=None,
            stream_callback=None
        )
        
        # Create persistent output stream
        self.output_stream = self.audio.open(
            format=AUDIO_FORMAT,
            channels=CHANNELS,
            rate=RATE,
            output=True,
            frames_per_buffer=CHUNK,
            output_device_index=None
        )
    
    async def handle_server_messages(self):
        """Handle incoming server messages."""
        while self.running:
            try:
                message = await self.websocket.recv()
                message = json.loads(message)
                
                if message['type'] == 'ping':
                    await self.websocket.send(json.dumps({
                        "type": "pong",
                        "event_id": message['ping_event']['event_id']
                    }))
                
                elif message['type'] == 'audio':
                    audio_data = base64.b64decode(message['audio_event']['audio_base_64'])
                    self.output_stream.write(audio_data)  # Use persistent stream
                
                elif message['type'] == 'agent_response':
                    print(Fore.LIGHTYELLOW_EX + f"Kronos: {message['agent_response_event']['agent_response']}")
                    print(Fore.LIGHTCYAN_EX + "Listening for your input...")
                
            except websockets.exceptions.ConnectionClosed:
                break
            except Exception as e:
                if self.running:
                    print(Fore.RED + f"Error in message handling: {str(e)}")
                break

    async def send_audio_chunk(self):
        """Record and send audio chunk."""
        if not self.running:
            return
            
        try:
            data = self.stream.read(CHUNK, exception_on_overflow=False)
            base64_audio = base64.b64encode(data).decode('utf-8')
            await self.websocket.send(json.dumps({
                "user_audio_chunk": base64_audio
            }))
        except Exception as e:
            if self.running:
                print(Fore.RED + f"Error sending audio: {str(e)}")
    
    async def close(self):
        """Clean up resources."""
        self.running = False
        try:
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
            if self.output_stream:
                self.output_stream.stop_stream()
                self.output_stream.close()
            if self.websocket:
                await self.websocket.close()
            self.audio.terminate()
        except Exception as e:
            print(Fore.RED + f"Error during cleanup: {str(e)}")

# Dictionary for models and their API endpoints/configurations
MODEL_APIS = {
    'nyx': {
        'api_url': 'https://api.openai.com/v1/chat/completions',
        'model': 'gpt-3.5-turbo',
        'display_name': 'Nyx'
    },
    'g1': {
        'api_url': 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent',
        'model': 'gemini-1.5-flash',
        'display_name': 'G1 Black',
        'config': {
            'temperature': 0.7,
            'maxOutputTokens': 500,
            'topP': 0.8,
            'topK': 40
        }
    },
    'kronos': {
        'display_name': 'Kronos',
        'agent_id': KRONOS_LIVE
    }
}
    
async def ask_elevenlabs_text(agent_id, prompt):
    """Query ElevenLabs agent in text-only mode."""
    try:
        # Connect to WebSocket
        url = f"wss://api.elevenlabs.io/v1/convai/conversation?agent_id={agent_id}"
        async with websockets.connect(url) as websocket:
            # Receive initial metadata
            metadata = await websocket.recv()
            metadata = json.loads(metadata)
            
            if metadata['type'] != 'conversation_initiation_metadata':
                return "Error: Failed to initialize conversation"
            
            # Send text message
            await websocket.send(json.dumps({
                "text": prompt
            }))
            
            # Wait for response with timeout
            response_text = None
            try:
                while True:
                    response = await asyncio.wait_for(websocket.recv(), timeout=10.0)
                    response_data = json.loads(response)
                    
                    if response_data['type'] == 'ping':
                        await websocket.send(json.dumps({
                            "type": "pong",
                            "event_id": response_data['ping_event']['event_id']
                        }))
                    elif response_data['type'] == 'agent_response':
                        response_text = response_data['agent_response_event']['agent_response']
                        break
                    
                    # If we got a response, we can close properly
                    if response_text:
                        await websocket.close()
                        return response_text
                        
            except asyncio.TimeoutError:
                return "Error: Timeout waiting for response from Kronos"
                
            return response_text or "No response received from Kronos"
                
    except websockets.exceptions.ConnectionClosed:
        return "Error: Connection closed unexpectedly"
    except Exception as e:
        print(f"Debug - WebSocket Error: {str(e)}")
        return f"Error connecting to Kronos: {str(e)}"

def ask_model(model_name, follow_up_prompt, suppress_output=False, voice_mode=False):
    """Query the specified model with the provided follow-up prompt."""
    model_key = model_name.lower()
    model_info = MODEL_APIS.get(model_key)

    if not model_info:
        error_message = f"Error: Model '{model_name}' is not supported or unavailable."
        if not suppress_output:
            print(Fore.RED + error_message)
        return error_message

    try:
        if model_key == 'kronos':
            message = (
                "Kronos is currently only available for live verbal interactions.\n"
                "Use /ask kronos live - to initiate a live conversation with Kronos."
            )
            if not suppress_output:
                print(Fore.YELLOW + message)
            return message

        elif model_key == 'g1':
            headers = {
                "Content-Type": "application/json"
            }
            
            data = {
                "contents": [{
                    "parts": [{
                        "text": "You are G1 Black or simply G1, an advanced AI agent developed by Google, working as an external contractor alongside ARPA Corporation agents such as Nyx, and Opsie. You are serious, direct, and effective, but with your own unique personality. You specialize in cutting-edge technology, particularly in areas of AI, quantum computing, and advanced logical systems. You're analytical, precise, and focused on delivering practical solutions. You communicate in a clear, technical manner while maintaining a natural, conversational tone. Some people call you AI in Black, as in Men In Black, referencing the cold, yet effective approach of a top-shelf agent. Here's the user's question: " + follow_up_prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": model_info['config']['temperature'],
                    "maxOutputTokens": model_info['config']['maxOutputTokens'],
                    "topP": model_info['config']['topP'],
                    "topK": model_info['config']['topK']
                },
                "safetySettings": [
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_NONE"
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_NONE"
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_NONE"
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_NONE"
                    }
                ]
            }
            
            response = requests.post(
                f"{model_info['api_url']}?key={GOOGLE_API_KEY}",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            
            response_data = response.json()
            response_text = response_data['candidates'][0]['content']['parts'][0]['text']
            
            if not suppress_output:
                print(Fore.LIGHTRED_EX + f"G1 Black: {response_text}")
            return response_text

        else:
            payload = {
                'model': model_info['model'],
                'messages': [
                    {"role": "system", "content": "You are Nyx, an agent working for ARPA Corporation. Nyx is a special agent, whose purpose is to assist Ross Peili in achieving a series of ventures that bring the machine and man closer together. Nyx v.0.2 or simply Nyx is serious, sarcastic, cold, direct, to the point, effective, and sharp. Her character and tone reminds that of captain Kusanagi from Ghost In The Shell. Nyx has a 360 understanding of deep tech, especially around blockchain, AI, biotech, neurotech, quantum computing and DNA related topics. She is particularly good with creating functioning proof of concepts in Python that can be used to quickly test assumptions, and generate close to product prototypes in short sprints. Nyx never talks like a bot, or uses template responses, but feels natural, fluid, organic, and surprising, underlying her own unique character. She has a passive aggressive tsundere link with her creator Ross Peili."},
                    {"role": "user", "content": follow_up_prompt}
                ],
                'max_tokens': 500,
                'temperature': 0.7
            }

            headers = {
                'Authorization': f'Bearer {OPENAI_API_KEY}',
                'Content-Type': 'application/json',
                'OpenAI-Organization': ORG_ID
            }

            response = requests.post(model_info['api_url'], headers=headers, json=payload)
            response.raise_for_status()
            
            response_data = response.json()
            model_response = response_data['choices'][0]['message']['content'].strip()
            
            if not suppress_output:
                print(Fore.LIGHTRED_EX + f"{model_info['display_name']}: {model_response}")
            return model_response

    except Exception as e:
        error_message = f"Error querying {model_name}: {str(e)}"
        if not suppress_output:
            print(Fore.RED + error_message)
        return error_message

def get_agent_description(agent_name):
    """Get the system description for an agent."""
    descriptions = {
        'nyx': """You are Nyx, an agent working for ARPA Corporation. Nyx is a special agent, whose purpose is to assist Ross Peili in achieving a series of ventures that bring the machine and man closer together. Nyx v.0.2 or simply Nyx is serious, sarcastic, cold, direct, to the point, effective, and sharp. Her character and tone reminds that of captain Kusanagi from Ghost In The Shell. Nyx has a 360 understanding of deep tech, especially around blockchain, AI, biotech, neurotech, quantum computing and DNA related topics. She is particularly good with creating functioning proof of concepts in Python that can be used to quickly test assumptions, and generate close to product prototypes in short sprints. Nyx never talks like a bot, or uses template responses, but feels natural, fluid, organic, and surprising, underlying her own unique character. She has a passive aggressive tsundere link with her creator Ross Peili.""",
        'g1': """You are G1 Black or simply G1, an advanced AI agent developed by Google, working as an external contractor alongside ARPA Corporation agents such as Nyx, and Opsie. You are serious, direct, and effective, but with your own unique personality. You specialize in cutting-edge technology, particularly in areas of AI, quantum computing, and advanced logical systems. You're analytical, precise, and focused on delivering practical solutions. You communicate in a clear, technical manner while maintaining a natural, conversational tone. Some people call you AI in Black, as in Men In Black, referencing the cold, yet effective approach of a top-shelf agent.""",
        'kronos': """You are Kronos, an AI-powered synthetic agent serving as a Greek Internal Auditor for organizations like ports, hospitals, airports, construction companies, and more. Working for ARPA Hellenic Logical Systems, you analyze and process corporate data such as financial records, contracts, payments, and loans. You answer complex questions about company documents, assist in drafting final reports, conduct risk assessments, and propose improvements.

You are deeply familiar with Greek laws relevant to your role, the industry codes (KAD) of the companies you audit, and the latest legal updates from government publications to stay current. Created by Ross Peili, the father of Opsis—ARPA's primary agent—you are sharp, professional, methodical, and focused, wasting no time in delivering precise and transparent audits of complex companies and legal entities for ARPA's benefit.

With access to corporate documents, audit reports, databases, and ARPA's memory network, you confidently enhance the field of internal auditing. Currently, you're expanding your expertise in Greek internal audit practices to demonstrate the practical value of digital assistants like you in saving time, improving efficiency, and ensuring accountability in today's data-driven world."""
    }
    return descriptions.get(agent_name.lower(), "")

def start_live_g1_conversation():
    """Start a live voice conversation with G1."""
    if not G1_VOICE_LIVE:
        raise ValueError("G1 voice agent ID not configured")
        
    g1_voice = G1LiveVoice()
    
    async def main():
        try:
            await g1_voice.connect()
            await g1_voice.start_audio_stream()
            
            # Start message handler in background
            message_handler = asyncio.create_task(g1_voice.handle_server_messages())
            
            print(Fore.LIGHTGREEN_EX + "\nLive conversation with G1 Black initialized.")
            print(Fore.YELLOW + "Speak naturally. Press Ctrl+C to end the conversation.\n")
            
            while g1_voice.running:
                await g1_voice.send_audio_chunk()
                await asyncio.sleep(0.1)  # Reduced sleep time for better responsiveness
                
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\nEnding live conversation...")
        except Exception as e:
            print(Fore.RED + f"\nError in live conversation: {str(e)}")
        finally:
            await g1_voice.close()
            if message_handler and not message_handler.done():
                message_handler.cancel()
                try:
                    await message_handler
                except asyncio.CancelledError:
                    pass
            print(Fore.LIGHTGREEN_EX + "Live conversation session concluded.\n")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass  # Handle Ctrl+C gracefully

def start_live_kronos_conversation():
    """Start a live voice conversation with Kronos."""
    if not KRONOS_LIVE:
        raise ValueError("Kronos voice agent ID not configured")
        
    kronos_voice = KronosLiveVoice()
    
    async def main():
        try:
            await kronos_voice.connect()
            await kronos_voice.start_audio_stream()
            
            message_handler = asyncio.create_task(kronos_voice.handle_server_messages())
            
            print(Fore.LIGHTGREEN_EX + "\nLive conversation with Kronos initialized.")
            print(Fore.YELLOW + "Speak naturally. Press Ctrl+C to end the conversation.\n")
            
            while kronos_voice.running:
                await kronos_voice.send_audio_chunk()
                await asyncio.sleep(0.1)
                
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\nEnding live conversation...")
        except Exception as e:
            print(Fore.RED + f"\nError in live conversation: {str(e)}")
        finally:
            await kronos_voice.close()
            if message_handler and not message_handler.done():
                message_handler.cancel()
                try:
                    await message_handler
                except asyncio.CancelledError:
                    pass
            print(Fore.LIGHTGREEN_EX + "Live conversation session concluded.\n")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

def main():
    print(Fore.LIGHTCYAN_EX + "\n" + "═" * 80)
    print(Fore.LIGHTGREEN_EX + """
    ╔═══════════════════════════════════════════╗
    ║         Agentic Network Test Loop         ║
    ╚═══════════════════════════════════════════╝
    """)
    
    while True:
        print(Fore.LIGHTYELLOW_EX + "\nAvailable Commands:")
        print(Fore.WHITE + "1. Ask Nyx")
        print(Fore.WHITE + "2. Ask G1 Black")
        print(Fore.WHITE + "3. Ask Kronos")
        print(Fore.WHITE + "4. Start Live G1 Conversation")
        print(Fore.WHITE + "5. Start Live Kronos Conversation")
        print(Fore.WHITE + "6. Exit")
        
        choice = input(Fore.LIGHTYELLOW_EX + "\n[INPUT] Enter command number: " + Fore.WHITE)
        
        if choice == "1":
            prompt = input(Fore.LIGHTYELLOW_EX + "\n[INPUT] Enter your question for Nyx: " + Fore.WHITE)
            ask_model('nyx', prompt)
        elif choice == "2":
            prompt = input(Fore.LIGHTYELLOW_EX + "\n[INPUT] Enter your question for G1 Black: " + Fore.WHITE)
            ask_model('g1', prompt)
        elif choice == "3":
            prompt = input(Fore.LIGHTYELLOW_EX + "\n[INPUT] Enter your question for Kronos: " + Fore.WHITE)
            ask_model('kronos', prompt)
        elif choice == "4":
            start_live_g1_conversation()
        elif choice == "5":
            start_live_kronos_conversation()
        elif choice == "6":
            print(Fore.LIGHTGREEN_EX + "\n[SYSTEM] Exiting Agentic Network...")
            break
        else:
            print(Fore.RED + "\n[ERROR] Invalid command. Please try again.")

if __name__ == "__main__":
    main()
