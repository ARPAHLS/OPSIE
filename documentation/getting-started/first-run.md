# First Run Guide

Your complete guide to running OPSIIE for the first time and understanding the startup process.

## 🚀 Starting OPSIIE

### Launch Command
```bash
python OPSIIE_0_3_79_XP.py
```

## 📺 Startup Sequence

### 1. Theme Selection
```
Choose your color theme:
1. Pastel (Soft, muted colors)
2. Vibrant (High-contrast, bold colors)

Enter 1 or 2:
```

- **Pastel**: Recommended for extended use, easier on the eyes
- **Vibrant**: Better visibility, high contrast

**Note**: You can change this anytime during conversation with `/theme`

### 2. Splash Screen
```
 ███             ███████    ███████████   █████████  █████ █████ ██████████
░░░███         ███░░░░░███ ░░███░░░░░███ ███░░░░░███░░███ ░░███ ░░███░░░░░█
  ░░░███      ███     ░░███ ░███    ░███░███    ░░░  ░███  ░███  ░███  █ ░ 
    ░░░███   ░███      ░███ ░██████████ ░░█████████  ░███  ░███  ░██████   
     ███░    ░███      ░███ ░███░░░░░░   ░░░░░░░░███ ░███  ░███  ░███░░█   
   ███░      ░░███     ███  ░███         ███    ░███ ░███  ░███  ░███ ░   █
 ███░         ░░░███████░   █████       ░░█████████  █████ █████ ██████████
░░░             ░░░░░░░    ░░░░░         ░░░░░░░░░  ░░░░░ ░░░░░ ░░░░░░░░░░ 

        A Self-Centered Intelligence (SCI) Prototype 
        By ARPA HELLENIC LOGICAL SYSTEMS | Version: 0.3.79 XP | 01 JUL 2025
```

Boot sound: `system_sounds/opsiieboot.mp3` plays

### 3. Facial Recognition Authentication
```
Please look at the camera for authentication...
```

**What Happens**:
1. Camera activates
2. Face detection runs
3. Compares with photo in your `kun.py` profile
4. Emotion detection (via DeepFace)
5. Authentication success/failure

**Success**:
```
Welcome back [Your Name]. I was worried I'd never see you again.
```
*(One of several Master user greetings)*

**Failure**:
```
Authentication failed. Access denied.
```
*System exits*

### 4. System Initialization
OPSIIE loads:
- ✓ PostgreSQL database connection
- ✓ ChromaDB vector database
- ✓ Ollama language model (llama3)
- ✓ MusicGen model (if available)
- ✓ BLIP vision model (for image analysis)
- ✓ Facial recognition system
- ✓ Voice synthesis (ElevenLabs)
- ✓ Speech recognition
- ✓ Theme colors
- ✓ Soul Signature from your profile

### 5. Interactive Interface
```
[Your Name] >>
```

OPSIIE is now ready for interaction!

## 💬 First Interaction

### Test Basic Conversation
```
[Your Name] >> Hello OPSIIE
```

OPSIIE responds based on your Soul Signature and conversation history.

### Try a Command
```
[Your Name] >> /help
```

Displays the help menu with all available commands.

## 🎯 Essential First Commands

### 1. Check System Status
```bash
/status
```
Shows:
- Database connection status
- AI model status
- Voice system status
- Memory usage
- Uptime

### 2. View Available Commands
```bash
/help
```
Categories shown:
- Mnemonic Matrix Commands (/recall, /forget, /memorize)
- Agentic Matrix Commands (/ask, /markets, /read, etc.)
- Web3 Commands (/0x buy, /0x sell, etc.)
- System Commands (/mail, /theme, /soulsig, etc.)

### 3. Test Voice Mode
```bash
/voice
```
- Activates full voice interaction
- Speak your commands
- Say "voice off" to deactivate

### 4. Test Memory System
```bash
/memorize This is my first interaction with OPSIIE
```
Then retrieve it:
```bash
/recall first interaction
```

### 5. Test AI Generation
```bash
/imagine a futuristic city at sunset
```
Generates and displays an image.

## 🧪 Testing Core Features

### Memory & Recall
```bash
# Store information
/memorize I work on AI research at MIT

# Retrieve it
/recall MIT

# Forget last interaction
/forget
```

### AI Agents
```bash
# Ask Nyx (OpenAI)
/ask Nyx What are the latest developments in quantum computing?

# Ask G1 Black (Google)
/ask G1 Analyze the potential of neuromorphic computing

# Start live conversation with G1
/ask g1 live
```

### File Analysis
```bash
# Read a file
/read "C:\Documents\report.pdf"

# Ask questions about it
What are the main conclusions?

# Close file context
/close
```

### Email
```bash
# Send email
/mail john@example.com subject "Hello" content "This is a test from OPSIIE"

# Check inbox
/mail inbox
```

### Web3 (R-Grade only)
```bash
# View wallet addresses
/0x receive

# Set gas strategy
/0x gas medium

# Buy tokens
/0x buy 10 degen using eth on base
```

### Markets (R-Grade only)
```bash
# Get stock data
/markets tesla

# Get crypto data
/markets btc

# Compare stocks
/markets compare tsla nio
```

### DNA Analysis (R-Grade only)
```bash
# Analyze DNA sequence
/dna ATGCGTAACGGCATTAGC

# Detailed analysis
/dna --verbose ATGCGTAACGGCATTAGC
```

### Collaboration Rooms
```bash
# Create room with agents
/room nyx, g1: Discuss quantum computing applications

# Interact in room
What do you think about quantum error correction?

# Close room
/close
```

## 🎨 Customization

### Change Theme
```bash
/theme
```
Or use voice command: "theme"

### Manage Soul Signature
```bash
# View current Soul Signature
/soulsig

# Add to Soul Signature
/soulsig I prefer technical explanations with code examples

# Wipe Soul Signature (⚠️ permanent)
/soulsig wipe

# Restore Soul Signature (if recently wiped)
/soulsig heal
```

### Adjust Web Limit
```bash
# Set web content extraction limit
/weblimit 2000
```

## 🔍 Understanding OPSIIE's Responses

### Natural Conversation
OPSIIE avoids template responses. Instead of:
> "That's an easy question! Let me help you with that."

You get personality-driven responses like:
> "Hmm, interesting question. I've been thinking about this lately..."

### Memory Integration
OPSIIE references past conversations:
> "Remember when we discussed quantum computing last week? This relates to that..."

### Emotional Intelligence
Based on your Soul Signature and interaction history:
- Adapts tone and style
- Remembers preferences
- Builds on previous conversations
- Shows personality traits (tsundere, sarcastic, direct)

## 🚨 Common First-Run Issues

### Camera Not Detected
```
Error: No camera found for facial recognition
```
**Solution**: 
- Check camera connection
- Verify camera permissions in Windows
- Ensure camera is not in use by another application

### Face Not Recognized
```
Authentication failed
```
**Solution**:
- Ensure good lighting
- Face camera directly
- Check photo path in kun.py is correct
- Photo should be clear and recent

### Database Connection Error
```
Error connecting to PostgreSQL database
```
**Solution**:
- Verify PostgreSQL is running
- Check DB credentials in .env
- Ensure database 'mnemonic_computer' exists

### Missing API Keys
```
Error: OPENAI_API_KEY not found
```
**Solution**:
- Verify .env file exists
- Check all required API keys are set
- Restart terminal after adding keys

### Ollama Not Running
```
Error: Failed to connect to Ollama
```
**Solution**:
- Start Ollama service
- Verify llama3 model is installed: `ollama pull llama3`
- Check Ollama is running: `ollama list`

### Voice Synthesis Error
```
Error with Eleven Labs API
```
**Solution**:
- Verify ELEVENLABS_API_KEY is valid
- Check VOICE_ID is correct
- Verify internet connection
- Check API usage limits

## 📊 Access Levels

### R-Grade (Master Access)
Full access to all features:
- All commands available
- Web3 operations (/0x)
- Market data (/markets)
- DNA analysis (/dna)
- Advanced AI agents
- All experimental features

### A-Grade (Standard Access)
Limited access:
- Basic conversation
- Voice features
- File reading
- Email
- Basic AI generation
- No /0x, /markets, /dna commands

**Check your access level**: Look at `arpa_id` in your kun.py profile
- `R###` = Master Access
- `A###` = Standard Access

## 🎯 Next Steps

After successful first run:

1. **Explore Commands**
   - Try each command category
   - Experiment with different features
   - Read [Basic Commands Guide](../user-guides/basic-commands.md)

2. **Customize Your Experience**
   - Build your Soul Signature
   - Set preferred theme
   - Configure voice settings
   - Add email contacts

3. **Learn Advanced Features**
   - [Agentic Network](../advanced-features/agentic-network.md)
   - [DNA Analysis](../advanced-features/dna-analysis.md)
   - [Web3 & Blockchain](../advanced-features/web3-blockchain.md)
   - [Financial Intelligence](../advanced-features/financial-intelligence.md)

4. **Read Documentation**
   - [Memory Management](../user-guides/memory-management.md)
   - [Command Reference](../api-reference/command-reference.md)
   - [System Architecture](../system-architecture/core-components.md)

## 💡 Tips for Best Experience

1. **Build Your Soul Signature** - The more OPSIIE knows about you, the better the interactions
2. **Use Memory System** - Store important information with /memorize
3. **Try Voice Mode** - Natural conversation feels more engaging
4. **Experiment with Rooms** - Collaborate with multiple AI agents
5. **Keep Conversations Going** - OPSIIE remembers context and builds on it
6. **Provide Feedback** - Use /forget if responses aren't accurate

## 📞 Getting Help

- Type `/help` for command list
- Type `/help <command>` for specific command help
- Check [Command Reference](../api-reference/command-reference.md)
- Contact: input@arpacorp.net

---


**Welcome to OPSIIE!** Your journey with a Self-Centered Intelligence begins now. 🚀
