# Configuration Guide

Comprehensive guide for configuring OPSIIE 0.3.79 XP to match your preferences and requirements.

## 🔧 Configuration Files

### Primary Configuration Files
1. **`.env`** - Environment variables and API keys
2. **`kun.py`** - User profiles and Soul Signatures
3. **`terminal_colors.py`** - Theme configuration (Pastel/Vibrant)

## 🌍 Environment Variables (.env)

### Database Configuration
```env
DB_NAME=mnemonic_computer        # PostgreSQL database name
DB_USER=your_username            # Database username
DB_PASSWORD=your_password        # Database password
DB_HOST=localhost                # Database host
DB_PORT=5432                     # Database port
```

### AI Model APIs
```env
# OpenAI (for Nyx agent)
OPENAI_API_KEY=sk-...
ORG_ID=org-...
NYX_ASSISTANT_ID=asst_...

# Google AI (for G1 Black agent)
GOOGLE_API_KEY=AIza...
G1_VOICE_LIVE=your_g1_agent_id

# Kronos (Greek Internal Auditor)
KRONOS_LIVE=your_kronos_agent_id

# ElevenLabs (Voice synthesis)
ELEVENLABS_API_KEY=...
VOICE_ID=...                     # OPSIIE's voice
NYX_VOICE_ID=...                 # Nyx's voice
G1_VOICE_ID=...                  # G1's voice
```

### Web3 & Blockchain
```env
AGENT_PRIVATE_KEY=0x...          # OPSIIE's Ethereum private key
BASE_RPC_URL=https://...         # Base network RPC
ETHEREUM_RPC_URL=https://...     # Ethereum mainnet RPC
POLYGON_RPC_URL=https://...      # Polygon network RPC
```

### Email Configuration
```env
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password  # Gmail app-specific password
```

### Scientific APIs
```env
NCBI_EMAIL=your_email@example.com  # For DNA analysis features
```

## 👤 User Profile Configuration (kun.py)

### Access Levels

**R-Grade (Master Access)**
- Full system access
- All experimental features
- Web3 operations (`/0x` commands)
- Advanced AI agents (`/ask`, `/room`)
- Financial intelligence (`/markets`)
- DNA analysis (`/dna`)

**A-Grade (Standard Access)**
- Basic conversation
- File operations (`/read`, `/open`, `/close`)
- Voice features (`/voice`, `/voice1`, `/voice2`)
- Limited AI generation (`/imagine`, `/video`, `/music`)
- Email (`/mail`)

### User Profile Structure
```python
users = {
    'YourName': {
        # Basic Information
        'full_name': 'Your Full Name',
        'call_name': 'Your Preferred Name',
        'arpa_id': 'R001',  # R for Master, A for Standard
        
        # Blockchain
        'public0x': '0x...',  # Your Ethereum wallet address
        
        # Database Connection
        'db_params': {
            'dbname': 'mnemonic_computer',
            'user': 'your_db_username',
            'password': 'your_db_password',
            'host': 'localhost',
            'port': '5432'
        },
        
        # Authentication
        'picture': r'C:\path\to\your\photo.jpg',
        
        # Communication
        'mail': 'your_email@example.com',
        
        # Soul Signature (Personalization)
        'soul_sig': [
            "Prefers direct communication",
            "Values efficiency and precision",
            "Enjoys technical discussions",
            # Add your preferences here
        ],
    }
}
```

### Soul Signature Guidelines

The Soul Signature is the highest-priority personalization system. Include:

**Communication Preferences**
```python
"Prefers direct communication without pleasantries"
"Values detailed technical explanations"
"Likes sarcastic humor and wit"
"Avoids template-like responses"
```

**Interests & Expertise**
```python
"Deep interest in blockchain technology"
"Background in molecular biology"
"Enjoys philosophical discussions"
"Works in quantum computing field"
```

**Interface Preferences**
```python
"Prefers dark mode interfaces"
"Likes minimalist design"
"Values visual data representations"
```

**Interaction Patterns**
```python
"Remembers past conversations and builds on them"
"Appreciates when OPSIIE shows initiative"
"Enjoys creative and artistic pursuits"
```

**Personal Instructions**
```python
"Do not use my middle name"
"My favorite color is Lilac"
"Call me by my nickname in casual conversations"
"I'm working on a project about AI ethics"
```

## 🎨 Theme Configuration

### Available Themes
1. **Pastel** - Soft, muted colors for gentle visual experience
2. **Vibrant** - High-contrast, bold colors for enhanced visibility

### Theme Selection

**At Startup**
- Choose theme during splash screen
- Default is Pastel

**During Conversation**
```bash
/theme                    # Opens theme selector
# Or voice command: "theme"
```

### Custom Theme Colors (terminal_colors.py)

```python
PASTEL = {
    'lilac': (200, 162, 200),
    'pink': (255, 182, 193),
    'green': (152, 251, 152),
    # ... other colors
}

VIBRANT = {
    'lilac': (138, 43, 226),
    'pink': (255, 20, 147),
    'green': (0, 255, 0),
    # ... other colors
}
```

## 🔊 Voice Configuration

### Voice Modes
```bash
/voice          # Full voice mode (both speak and listen)
/voice1         # OPSIIE speaks, you type
/voice2         # You speak, OPSIIE types
/voiceoff       # Disable voice mode
```

### ElevenLabs Voice IDs
Configure in `.env`:
```env
VOICE_ID=your_opsiie_voice_id         # OPSIIE's primary voice
NYX_VOICE_ID=your_nyx_voice_id        # Nyx agent's voice
G1_VOICE_ID=your_g1_voice_id          # G1 Black agent's voice
```

### Speech Recognition Settings
- Language: English (default)
- Timeout: 20 seconds of inactivity
- Custom word recognition for commands

## 🧬 DNA Analysis Configuration

### NCBI Email
Required for DNA analysis features:
```env
NCBI_EMAIL=your_email@example.com
```

### Database Access
- UniProt: Protein sequences
- Pfam: Protein families
- PROSITE: Protein patterns
- Rfam: RNA families
- miRBase: microRNA sequences
- GtRNAdb: tRNA sequences

## 💰 Web3 Configuration

### Supported Chains
```python
CHAIN_INFO = {
    'Base': {
        'chain_id': 8453,
        'rpc_url': os.getenv('BASE_RPC_URL'),
        'symbol': 'ETH',
        'explorer_url': 'https://basescan.org'
    },
    'Ethereum': {
        'chain_id': 1,
        'rpc_url': os.getenv('ETHEREUM_RPC_URL'),
        'symbol': 'ETH',
        'explorer_url': 'https://etherscan.io'
    },
    'Polygon': {
        'chain_id': 137,
        'rpc_url': os.getenv('POLYGON_RPC_URL'),
        'symbol': 'MATIC',
        'explorer_url': 'https://polygonscan.com'
    }
}
```

### Supported Tokens
```python
TOKENS = {
    'Degen': {
        'Base': '0x4ed4e862860bed51a9570b96d89af5e1b0efefed'
    },
    'USDC': {
        'Base': '0x7F5c764cBc14f9669B88837ca1490cCa17c31607',
        'Ethereum': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606EB48',
        'Polygon': '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174'
    }
}
```

### Gas Strategy
```bash
/0x gas low        # 80% of current gas price
/0x gas medium     # 100% of current gas price (default)
/0x gas high       # 150% of current gas price
```

## 📧 Email Configuration

### Gmail Setup
1. Enable 2-Factor Authentication
2. Generate App-Specific Password
3. Add to `.env`:
```env
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
```

### Known Contacts
Contacts are automatically mapped from kun.py user profiles:
```python
# Any user with 'mail' field becomes a known contact
'mail': 'contact@example.com'
```

## 📁 File Processing Limits

### Web Content Limit
```bash
/weblimit 2000    # Set to 2000 characters (500-5000 range)
```

Default: 1000 characters

### Supported File Types
- PDF (.pdf)
- CSV (.csv)
- DOCX (.docx)
- TXT (.txt)
- XLSX (.xlsx)

## 🎵 AI Generation Settings

### Image Generation (Hugging Face)
Default model: `black-forest-labs/FLUX.1-dev`

Change model:
```bash
/imagine model black-forest-labs/FLUX.1-dev
/imagine model hakurei/waifu-diffusion
```

### Video Generation
Default model: `damo-vilab/text-to-video-ms-1.7b` (ModelScope)

Available models:
- modelscope
- zeroscope
- videogen
- tuneavideo

Change model:
```bash
/video model zeroscope
```

### Music Generation
Model: `facebook/musicgen-small`
- Output: WAV format
- Saved to: `outputs/music/`

## 🔄 Configuration Updates

### Runtime Changes
Many settings can be changed during operation:
- Theme: `/theme`
- Web limit: `/weblimit <number>`
- Gas strategy: `/0x gas <level>`
- Image model: `/imagine model <name>`
- Video model: `/video model <name>`

### Persistent Changes
Edit configuration files and restart OPSIIE:
- `.env` for API keys and credentials
- `kun.py` for user profiles
- `web3_handler.py` for blockchain settings

## 🔐 Security Best Practices

1. **Never commit `.env` or `kun.py` to version control**
2. **Use environment variables for all secrets**
3. **Rotate API keys regularly**
4. **Use app-specific passwords for email**
5. **Keep private keys secure and backed up**
6. **Limit R-Grade access to trusted users only**

## 📋 Configuration Checklist

- [ ] .env file created with all required keys
- [ ] PostgreSQL database created and configured
- [ ] Ollama installed with llama3 model
- [ ] kun.py configured with your profile
- [ ] User photo added for facial recognition
- [ ] ElevenLabs voices configured
- [ ] Web3 wallets configured (if using /0x features)
- [ ] Email credentials configured (if using /mail)
- [ ] NCBI email configured (if using /dna)
- [ ] Theme selected
- [ ] Output directories verified

## 🚀 Next Steps

After configuration:
1. Follow [First Run Guide](first-run.md)
2. Test basic commands
3. Customize Soul Signature
4. Explore [Basic Commands](../user-guides/basic-commands.md)