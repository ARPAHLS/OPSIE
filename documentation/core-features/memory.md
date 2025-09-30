# Memory System - Mnemonic Matrix

OPSIIE's memory system, called the Mnemonic Matrix, provides long-term conversation storage and intelligent context retrieval using PostgreSQL and ChromaDB.

## 🧠 Overview

The Mnemonic Matrix enables OPSIIE to:
- **Remember Past Conversations**: Store all interactions in PostgreSQL
- **Retrieve Relevant Context**: Use vector search to find related memories
- **Build Ongoing Relationships**: Reference previous discussions
- **Maintain User Preferences**: Store and recall your Soul Signature
- **Learn from Interactions**: Improve responses based on history

## 🔧 Architecture

### Database Structure

**PostgreSQL (mnemonic_computer)**
```sql
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    prompt TEXT NOT NULL,
    response TEXT NOT NULL
);
```

**ChromaDB (Vector Database)**
- Stores conversation embeddings
- Enables semantic search
- Finds contextually similar memories

### How It Works

1. **Storage**: Every conversation is stored in PostgreSQL
2. **Vectorization**: Text is converted to embeddings
3. **Indexing**: Embeddings stored in ChromaDB
4. **Retrieval**: Semantic search finds relevant memories
5. **Context**: Retrieved memories enhance AI responses

## 📝 Memory Commands

### /memorize - Store Information
Store important information for future reference.

**Syntax:**
```bash
/memorize <message>
```

**Examples:**
```bash
# Store personal information
/memorize My favorite programming language is Python

# Store project details
/memorize The project deadline is next Friday at 5 PM

# Store preferences
/memorize I prefer technical explanations with code examples

# Store reminders
/memorize Don't forget to review the pull request

# Store research notes
/memorize Quantum entanglement relates to our AI architecture discussion
```

**What Happens:**
1. Message stored in PostgreSQL
2. Embedding created and stored in ChromaDB
3. Available for future /recall queries
4. OPSIIE can reference it in conversations

### /recall - Retrieve Information
Pull relevant context from past conversations.

**Syntax:**
```bash
/recall <keyword>
```

**Examples:**
```bash
# Recall by topic
/recall project x

# Recall by date context
/recall last week discussion

# Recall by person
/recall meeting with John

# Recall by technology
/recall quantum computing

# Recall by preference
/recall my preferences
```

**What Happens:**
1. Semantic search in ChromaDB
2. Finds contextually similar memories
3. Retrieves top relevant conversations
4. Displays results with timestamps
5. OPSIIE uses context in next response

**Example Output:**
```
Retrieved Memories:

[2025-01-15 14:23] 
Prompt: Tell me about project x
Response: Project X is the quantum computing initiative we discussed...

[2025-01-10 09:45]
Prompt: /memorize Project X deadline is March 15
Response: I've stored that information...

Found 2 relevant memories for 'project x'
```

### /forget - Exclude Last Interaction
Prevent the last conversation from being stored.

**Syntax:**
```bash
/forget
```

**Use Cases:**
```bash
# After inaccurate response
OPSIIE >> [incorrect information]
You >> /forget

# After hallucination
OPSIIE >> [hallucinated content]
You >> /forget

# After testing
You >> test command
OPSIIE >> [response]
You >> /forget

# After private information
You >> [sensitive data]
OPSIIE >> [response]
You >> /forget
```

**What Happens:**
1. Last prompt-response pair removed from memory
2. NOT stored in PostgreSQL
3. NOT stored in ChromaDB
4. Fresh start for next interaction

**Important**: 
- Only affects the most recent interaction
- Cannot undo after next prompt
- Use immediately after unwanted response

## 🎯 Soul Signature System

The Soul Signature is your personalized system prompt with highest priority in OPSIIE's context hierarchy.

### View Soul Signature
```bash
/soulsig
```

Displays your current Soul Signature from kun.py.

### Add to Soul Signature
```bash
/soulsig <message>
```

**Examples:**
```bash
# Communication style
/soulsig I prefer direct communication without pleasantries

# Preferences
/soulsig My favorite color is Lilac

# Instructions
/soulsig Do not reply using my middle name

# Context
/soulsig I'm currently working on a blockchain project

# Roles
/soulsig You are my physics lecturer
```

**What Happens:**
1. Message appended to your soul_sig in kun.py
2. Automatically included in all future conversations
3. OPSIIE prioritizes this information
4. Persists across sessions

### Wipe Soul Signature
```bash
/soulsig wipe
```

**⚠️ WARNING**: This permanently deletes your Soul Signature from kun.py

**Before Wiping:**
1. Soul Signature copied to temporary storage
2. Can be restored with `/soulsig heal` if done immediately

### Restore Soul Signature
```bash
/soulsig heal
```

Restores Soul Signature from temporary storage (only if recently wiped).

## 💡 Best Practices

### Effective Memorization

**DO:**
```bash
# Be specific
/memorize Project Alpha uses TensorFlow 2.x and PyTorch

# Include context
/memorize Meeting with Sarah on 2025-01-20 discussed budget concerns

# Store preferences clearly
/memorize I prefer code examples in Python with type hints

# Save important dates
/memorize Annual review scheduled for March 15, 2025
```

**DON'T:**
```bash
# Too vague
/memorize something important

# No context
/memorize tomorrow

# Redundant
/memorize (if already in conversation)
```

### Effective Recall

**DO:**
```bash
# Use specific keywords
/recall quantum entanglement discussion

# Reference timeframes
/recall last month's project discussion

# Use topics
/recall machine learning architecture

# Reference people
/recall conversation with Alice
```

**DON'T:**
```bash
# Too generic
/recall stuff

# Single letters
/recall a

# Empty
/recall
```

### Soul Signature Management

**Include:**
- Communication style preferences
- Areas of expertise and interest
- Personal preferences
- Contextual information
- Specific instructions

**Example Soul Signature:**
```python
'soul_sig': [
    "Prefers direct, technical communication",
    "Background in quantum physics and ML",
    "Working on AI ethics research",
    "Enjoys sarcastic humor",
    "Prefers Python code examples",
    "Do not use formal titles",
    "My favorite color is Lilac",
    "Currently based in Athens, Greece",
    "Interested in blockchain applications in science"
]
```

## 🔍 How Memory Enhances Conversations

### Context Building
```
You: Tell me about neural networks
OPSIIE: Based on our previous discussions about quantum computing, 
        I'll connect this to our conversation last week about 
        quantum neural networks...
```

### Preference Recall
```
You: Explain gradient descent
OPSIIE: [Provides technical explanation with Python code, 
         remembering your Soul Signature preference for 
         code examples]
```

### Long-term Learning
```
You: What did we discuss about the project timeline?
OPSIIE: *recalls /memorize from 2 weeks ago*
        You mentioned the deadline is March 15, and we 
        discussed the three-phase approach...
```

## 📊 Memory Statistics

### View Memory Usage
```bash
/status
```

Shows:
- Total conversations stored
- Database size
- Vector database status
- Memory usage

## 🔐 Privacy & Security

### What's Stored
- All conversation prompts and responses
- Timestamps for each interaction
- Vector embeddings for semantic search
- Soul Signature preferences

### What's NOT Stored
- Conversations after `/forget`
- Temporary file context (after `/close`)
- Live voice conversations (unless explicitly requested)

### Data Isolation
- Each user has separate database connection (configured in kun.py)
- Users can only access their own memories
- R-Grade and A-Grade users are segregated

### Data Control
```bash
# Remove last interaction
/forget

# Wipe personal preferences
/soulsig wipe

# Database is local - you have full control
```

## 🧬 Technical Details

### Vector Embeddings
- Model: `sentence-transformers/all-MiniLM-L6-v2`
- Dimension: 384
- Similarity: Cosine similarity
- Threshold: Configurable

### Storage Optimization
- Conversation deduplication
- Automatic pruning (configurable)
- Efficient indexing
- Compressed embeddings

### Retrieval Algorithm
1. Query vectorization
2. Semantic search in ChromaDB
3. Top-k results selection (default k=5)
4. Relevance ranking
5. Context injection into prompt

## ⚠️ Limitations

### Current Limitations
- No conversation editing after storage
- `/forget` only works for last interaction
- Soul Signature changes require editing kun.py directly (except `/soulsig` append)
- No memory export feature (direct database access required)
- No automatic memory summarization

### Workarounds
```bash
# To update stored information
/memorize [Updated information] (overwrites in practice via relevance)

# To clear specific memories
# Requires direct database access
DELETE FROM conversations WHERE prompt LIKE '%specific topic%';
```

## 🚀 Advanced Usage

### Memory-Driven Workflows

**Research Assistant**
```bash
# Store research findings
/memorize Paper X shows quantum advantage in specific algorithms

# Recall during writing
/recall quantum advantage

# Build knowledge base over time
```

**Project Management**
```bash
# Store milestones
/memorize Phase 1 completed on 2025-01-20

# Track decisions
/memorize Team decided to use microservices architecture

# Recall history
/recall project decisions
```

**Personal Knowledge Base**
```bash
# Store learning
/memorize Neural network backpropagation uses chain rule

# Recall concepts
/recall backpropagation

# Build on previous knowledge
Explains based on what you've already learned
```

## 📚 Related Features

- **File Context** (`/read`, `/open`, `/close`): Temporary file-based memory
- **Room History** (`/room`): Conversation history in multi-agent rooms
- **Command History**: Terminal-level history (not in memory system)

## 🔧 Troubleshooting

### Memory Not Recalled
```
Problem: /recall returns no results
Solutions:
- Check keyword spelling
- Try broader keywords
- Verify conversation was not /forgotten
- Check database connection (/status)
```

### Slow Recall
```
Problem: /recall takes long time
Solutions:
- Large database needs optimization
- Check database performance
- Consider pruning old conversations
```

### Soul Signature Not Applied
```
Problem: OPSIIE ignores Soul Signature
Solutions:
- Verify kun.py has correct soul_sig
- Restart OPSIIE to reload
- Check for syntax errors in soul_sig list
```

## 📞 Support

For memory system issues:
- Check database connection with `/status`
- Verify PostgreSQL is running
- Review kun.py configuration
- Contact: input@arpacorp.net

---


**The Mnemonic Matrix is the foundation of OPSIIE's long-term intelligence and personalization.** 🧠
