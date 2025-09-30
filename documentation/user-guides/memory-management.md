# Memory Management

Master OPSIIE's memory system for optimal interaction.

## 🧠 Memory System

**PostgreSQL**: Stores all conversations
**ChromaDB**: Enables semantic search
**Soul Signature**: Highest priority context

## 📝 Core Commands

### /memorize - Store
```bash
/memorize <information>
```

**Examples:**
```bash
/memorize Project Alpha deadline is March 15, 2025
/memorize I prefer Python with type hints
/memorize Meeting with Sarah discussed budget concerns
/memorize Quantum entanglement relates to our AI discussion
```

### /recall - Retrieve
```bash
/recall <keyword>
```

**Examples:**
```bash
/recall project alpha
/recall python preferences
/recall meeting with sarah
/recall quantum
```

### /forget - Exclude
```bash
/forget
```

Removes last prompt-response pair from memory.

## 🎯 Soul Signature

### View
```bash
/soulsig
```

### Add
```bash
/soulsig <message>
```

**Examples:**
```bash
/soulsig I prefer direct communication
/soulsig My favorite color is Lilac
/soulsig Working on blockchain research
/soulsig Don't use formal titles
```

### Wipe
```bash
/soulsig wipe
```
⚠️ Permanent deletion! Use carefully.

### Restore
```bash
/soulsig heal
```
Only works if recently wiped.

## 💡 Best Practices

### Effective Memorization

**DO:**
```bash
✅ /memorize Project X uses TensorFlow 2.x and PyTorch
✅ /memorize Meeting on 2025-01-20 with John about budget
✅ /memorize I prefer code examples in Python with comments
```

**DON'T:**
```bash
❌ /memorize something
❌ /memorize tomorrow
❌ /memorize (content already in current conversation)
```

### Effective Recall

**DO:**
```bash
✅ /recall quantum entanglement discussion
✅ /recall last month project meeting
✅ /recall python code preferences
```

**DON'T:**
```bash
❌ /recall stuff
❌ /recall a
❌ /recall
```

### Soul Signature Strategy

**Include:**
- Communication style
- Technical preferences
- Areas of expertise
- Personal instructions
- Context about you

**Example:**
```python
'soul_sig': [
    "Prefers technical, direct communication",
    "Background in quantum physics and ML",
    "Working on AI ethics research at MIT",
    "Enjoys sarcastic humor",
    "Prefers Python code with type hints",
    "Do not use formal titles",
    "Favorite color is Lilac",
    "Based in Athens, Greece",
    "Interested in blockchain in science"
]
```

## 🔍 How Memory Enhances AI

### Context Building
```
You: Explain neural networks
OPSIIE: [References your quantum computing discussion from last week]
        Based on our quantum neural networks conversation...
```

### Preference Application
```
You: Show me gradient descent
OPSIIE: [Provides Python code with type hints]
        [Remembers your Soul Signature preference]
```

### Long-term Learning
```
You: What's the project timeline?
OPSIIE: [Recalls /memorize from 2 weeks ago]
        You mentioned March 15 deadline with 3-phase approach...
```

## 📊 Memory Hierarchy

1. **Soul Signature** (Highest priority)
2. **Recent /memorize entries**
3. **Conversation history**
4. **Recalled context**
5. **General knowledge**

## 🔧 Maintenance

### Check Status
```bash
/status
```

Shows:
- Total conversations
- Database size
- Memory system status

### Clean Up
```bash
# Remove unwanted last interaction
/forget

# Clear file context
/close

# Wipe Soul Signature (if needed)
/soulsig wipe
```

## 🎯 Use Cases

### Research Assistant
```bash
/memorize Paper X shows quantum advantage in algorithm Y
/memorize Hypothesis: Z relates to previous finding
/recall quantum advantage
```

### Project Tracking
```bash
/memorize Phase 1 completed 2025-01-20
/memorize Team decided microservices architecture
/recall project decisions
```

### Personal Knowledge Base
```bash
/memorize Backpropagation uses chain rule
/memorize Gradient descent minimizes loss function
/recall backpropagation
```

## 🚨 Troubleshooting

**No results from /recall:**
- Try broader keywords
- Check spelling
- Verify conversation wasn't /forgotten

**Slow /recall:**
- Large database needs optimization
- Check database performance

**Soul Signature not applied:**
- Verify kun.py syntax
- Restart OPSIIE
- Check soul_sig list format

## 🔐 Privacy

**Stored:**
- All conversations (unless /forgotten)
- Soul Signature
- Timestamps

**NOT Stored:**
- Conversations after /forget
- Temporary file context
- Live voice (unless explicitly requested)

**Control:**
- `/forget` for last interaction
- Direct database access for bulk deletion
- `/soulsig wipe` for preferences

---

**Master memory for intelligent conversations.** 🧠