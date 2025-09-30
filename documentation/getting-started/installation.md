# Installation Guide

Complete guide for installing and setting up OPSIIE 0.3.79 XP on your system.

## 📋 Prerequisites

### System Requirements
- **Operating System**: Windows 10/11 (primary platform)
- **Python**: 3.8 or higher
- **Database**: PostgreSQL (latest version recommended)
- **Hardware**: 
  - Camera (for facial recognition authentication)
  - Microphone (for voice interaction)
  - GPU with CUDA support (recommended for AI generation)

### Required Accounts & API Keys
- **ElevenLabs** - Voice synthesis (ELEVENLABS_API_KEY, VOICE_ID)
- **Google AI** - G1 Black agent (GOOGLE_API_KEY, G1_VOICE_LIVE)
- **OpenAI** - Nyx agent (OPENAI_API_KEY, ORG_ID, NYX_ASSISTANT_ID)
- **Email** - Gmail account for email features (SENDER_EMAIL, SENDER_PASSWORD)
- **Web3** - Ethereum private key for blockchain features (AGENT_PRIVATE_KEY)
- **NCBI** - For DNA analysis (NCBI_EMAIL)

## 📦 Installation Steps

### 1. Clone the Repository
```bash
git clone <repository-url>
cd OPSIIE_0_3_79_XP_Pastel_BU
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

The requirements.txt includes:
- **AI/ML**: torch, transformers, diffusers, accelerate, ollama
- **Audio**: librosa, torchaudio, pyaudio, speech-recognition, pyttsx3
- **Vision**: opencv-python, face-recognition, deepface, Pillow
- **Web3**: web3, requests
- **Data**: pandas, numpy, scipy, yfinance, statsmodels
- **Database**: psycopg[binary], chromadb
- **Documents**: PyPDF2, pdfplumber, python-docx
- **Web**: beautifulsoup4, lxml, aiohttp, websockets
- **Bioinformatics**: biopython, matplotlib, prettytable, viennarna
- **Email**: imaplib2
- **Utilities**: python-dotenv, colorama, tqdm, pygame

### 3. Set Up PostgreSQL Database
```sql
-- Create the main database
CREATE DATABASE mnemonic_computer;

-- Connect to the database and create the conversations table
\c mnemonic_computer

CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    prompt TEXT NOT NULL,
    response TEXT NOT NULL
);
```

### 4. Install Ollama
OPSIIE uses Ollama for local AI processing with the Llama3 model.

1. Download and install Ollama from https://ollama.ai
2. Pull the Llama3 model:
```bash
ollama pull llama3
```

### 5. Configure Environment Variables
Create a `.env` file in the project root with the following:

```env
# Database Configuration
DB_NAME=mnemonic_computer
DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432

# AI Model APIs
OPENAI_API_KEY=your_openai_key
ORG_ID=your_openai_org_id
GOOGLE_API_KEY=your_google_api_key
ELEVENLABS_API_KEY=your_elevenlabs_key

# Agent IDs
NYX_ASSISTANT_ID=your_nyx_assistant_id
G1_VOICE_LIVE=your_g1_voice_agent_id
KRONOS_LIVE=your_kronos_agent_id

# Voice Configuration
VOICE_ID=your_elevenlabs_voice_id
NYX_VOICE_ID=your_nyx_voice_id
G1_VOICE_ID=your_g1_voice_id

# Web3 Configuration
AGENT_PRIVATE_KEY=your_ethereum_private_key
BASE_RPC_URL=your_base_rpc_url
ETHEREUM_RPC_URL=your_ethereum_rpc_url
POLYGON_RPC_URL=your_polygon_rpc_url

# Email Configuration
SENDER_EMAIL=your_gmail_address
SENDER_PASSWORD=your_gmail_app_password

# Scientific APIs
NCBI_EMAIL=your_email_for_ncbi
```

### 6. Configure User Profile
Copy `kun.example.py` to `kun.py` and configure your user profile:

```python
users = {
    'YourName': {
        'full_name': 'Your Full Name',
        'call_name': 'Your Preferred Name',
        'arpa_id': 'R001',  # R-Grade for Master access, A### for Standard
        'public0x': 'your_ethereum_wallet_address',
        'db_params': {
            'dbname': 'mnemonic_computer',
            'user': 'your_postgres_username',
            'password': 'your_postgres_password',
            'host': 'localhost',
            'port': '5432'
        },
        'picture': r'C:\path\to\your\photo.jpg',
        'mail': 'your_email@example.com',
        'soul_sig': [
            "Your personalized preferences here",
            "Communication style preferences",
            # Add more lines as needed
        ],
    }
}
```

**Important**: 
- `arpa_id` starting with 'R' (e.g., R001) grants Master (R-Grade) access to all features
- `arpa_id` starting with 'A' (e.g., A001) grants Standard (A-Grade) access with limited features
- The `picture` field should point to a photo for facial recognition
- The `soul_sig` (Soul Signature) is a personalized system prompt that defines how OPSIIE interacts with you

### 7. Create Output Directories
The system will create these automatically on first run, but you can create them manually:
```bash
mkdir -p outputs/images
mkdir -p outputs/music
mkdir -p outputs/videos
mkdir -p outputs/rooms
```

## 🧪 Verify Installation

### Test Database Connection
```bash
psql -h localhost -U your_username -d mnemonic_computer -c "SELECT 1;"
```

### Test Ollama
```bash
ollama run llama3 "Hello, world!"
```

### Test Python Environment
```bash
python -c "import torch, transformers, chromadb, psycopg; print('All packages imported successfully')"
```

## ⚠️ Common Issues

### Database Connection Errors
- Verify PostgreSQL is running
- Check DB_USER and DB_PASSWORD in .env
- Ensure the database 'mnemonic_computer' exists
- Verify pg_hba.conf allows local connections

### Missing Python Packages
- Ensure you're using Python 3.8+
- Some packages may require system dependencies (e.g., portaudio for pyaudio)
- On Windows, some packages may need Visual C++ Build Tools

### Face Recognition Issues
- Ensure your camera is connected and accessible
- Check camera permissions in Windows settings
- Verify your photo in kun.py is clear and properly lit

### CUDA/GPU Issues
- Verify CUDA is installed if using GPU acceleration
- Check torch.cuda.is_available() returns True
- Some models will fall back to CPU if GPU unavailable

### API Key Issues
- Verify all API keys are valid and not expired
- Check API usage limits haven't been exceeded
- Ensure API keys have proper permissions

## 🚀 Next Steps

After successful installation:
1. Read the [Configuration Guide](configuration.md)
2. Follow the [First Run Guide](first-run.md)
3. Explore [Quick Start Guide](../user-guides/quick-start.md)

## 📞 Support

If you encounter issues:
- Check the error logs
- Verify all prerequisites are met
- Review the troubleshooting section in README.md
- Contact: opsiebyarpa@gmail.com