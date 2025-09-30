# Technology Stack

Complete technology stack powering OPSIIE.

## 🐍 Core Language
**Python 3.8+**

## 🤖 AI & ML

### Language Models
- **Ollama** - Local LLM (Llama3 8B)
- **OpenAI** - GPT-3.5-turbo (Nyx agent)
- **Google Gemini** - 1.5 Flash (G1 agent)
- **ElevenLabs** - Conversational AI (Kronos)

### Vision & Voice
- **OpenCV** - Face recognition
- **SpeechRecognition** - Voice input (Google)
- **ElevenLabs API** - Text-to-speech
- **PyAudio** - Audio I/O

### ML Libraries
- **PyTorch** - Deep learning framework
- **Transformers** - Hugging Face models
- **Sentence Transformers** - Embeddings
- **CUDA** - GPU acceleration (optional)

### Generation
- **Hugging Face** - Image generation
- **Replicate** - Video & music generation
- **AudioCraft** - Music models (MusicGen)

## 💾 Data & Storage

### Databases
- **PostgreSQL** - Conversation storage
- **ChromaDB** - Vector database
- **psycopg2** - PostgreSQL adapter

### Data Processing
- **pandas** - Data analysis
- **numpy** - Numerical computing

## 📄 Document Processing

- **PyPDF2** - PDF reading
- **pdfplumber** - Advanced PDF extraction
- **python-docx** - Word documents
- **openpyxl** - Excel files
- **csv** - CSV parsing

## 🌐 Web & APIs

### HTTP
- **requests** - API calls
- **urllib** - URL handling
- **websockets** - Real-time communication

### Web3
- **web3.py** - Ethereum interaction
- **eth-account** - Key management
- **Base, Ethereum, Polygon** - Networks

### Financial
- **yfinance** - Yahoo Finance API
- **Real-time market data**

## 🧬 Bioinformatics

- **Biopython** - Sequence analysis
- **Bio.Blast** - Homology search
- **NCBI Entrez** - Database access
- **UniProt, Pfam** - Protein databases

## 📧 Communication

- **smtplib** - Email sending
- **imaplib** - Email receiving
- **email** - Message formatting
- **Gmail SMTP/IMAP**

## 🎨 Media

### Audio
- **pygame** - Audio playback
- **pydub** - Audio processing
- **soundfile** - File I/O

### Image
- **Pillow (PIL)** - Image processing
- **matplotlib** - Visualization

## 🎨 UI/UX

- **terminal_colors.py** - Custom theming
- **ASCII art** - Splash screens
- **Markdown rendering** - Formatted output
- **Pastel/Vibrant** - Color themes

## 🔧 Utilities

- **python-dotenv** - Environment variables
- **os, sys** - System operations
- **pathlib** - Path handling
- **json, pickle** - Serialization
- **datetime** - Time operations
- **re** - Regular expressions
- **hashlib** - Hashing

## 📦 Package Management

**requirements.txt**:
```
openai
google-generativeai
elevenlabs
psycopg2-binary
chromadb
sentence-transformers
opencv-python
SpeechRecognition
pyaudio
pygame
pydub
torch
transformers
biopython
web3
eth-account
yfinance
requests
pandas
openpyxl
PyPDF2
pdfplumber
python-docx
python-dotenv
replicate
pillow
```

## 🏗️ Architecture Patterns

**MVC-like**:
- Models: Data classes, API interfaces
- Views: Terminal output, formatting
- Controllers: Command parsers, handlers

**Service Layer**:
- Memory service (PostgreSQL + ChromaDB)
- Agent service (Nyx, G1, Kronos)
- Generation service (Images, videos, music)
- Web3 service (Blockchain operations)

**Repository Pattern**:
- Database interactions abstracted
- Consistent interface for data access

## 🚀 Performance

**Optimizations**:
- Async operations (where possible)
- Connection pooling (database)
- Caching (model outputs)
- Batch processing (embeddings)

**Scalability**:
- Stateless agent calls
- Modular architecture
- Configurable limits
- Resource-aware processing

## 🔄 Integration Flow

```
User Input
    ↓
Terminal/Voice
    ↓
Command Parser
    ↓
Service Layer
    ↓
APIs/Models/Database
    ↓
Response Processing
    ↓
Memory Storage
    ↓
Output Formatting
    ↓
Terminal/Voice Output
```

## 📊 Data Pipeline

**Memory Pipeline**:
```
Conversation → PostgreSQL
Conversation → Embeddings → ChromaDB
Query → Vector Search → Relevant Context
```

**Generation Pipeline**:
```
Prompt → Model API → Generation → Storage → Display
```

**Agent Pipeline**:
```
Query → Agent API → Response → Evaluation → Selection → Display
```

## 🔐 Security Stack

- **OpenCV** - Facial authentication
- **dotenv** - Secret management
- **HTTPS** - All API calls
- **Web3** - Checksum addresses
- **psycopg2** - Parameterized queries

## 🌍 External Services

**Required**:
- ElevenLabs API
- Google AI API (Gemini)
- OpenAI API

**Optional (R-Grade)**:
- Hugging Face Inference
- Replicate API
- Yahoo Finance
- NCBI (Entrez, BLAST)
- Blockchain RPC nodes

## 🖥️ System Requirements

**Minimum**:
- Python 3.8+
- 8GB RAM
- PostgreSQL
- Camera + Microphone
- Internet connection

**Recommended**:
- Python 3.10+
- 16GB RAM
- CUDA-capable GPU
- SSD storage
- High-speed internet

---

**Technology powering intelligence.** 🚀