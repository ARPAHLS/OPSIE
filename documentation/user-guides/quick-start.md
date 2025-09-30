# Quick Start Guide

Get started with OPSIIE in minutes.

## 🚀 Prerequisites

✅ Python 3.8+
✅ PostgreSQL installed
✅ Ollama with llama3
✅ Camera and microphone
✅ Configured .env and kun.py

## ⚡ 5-Minute Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Database
```sql
CREATE DATABASE mnemonic_computer;
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    prompt TEXT NOT NULL,
    response TEXT NOT NULL
);
```

### 3. Configure .env
```env
DB_NAME=mnemonic_computer
DB_USER=your_user
DB_PASSWORD=your_password
OPENAI_API_KEY=...
GOOGLE_API_KEY=...
ELEVENLABS_API_KEY=...
```

### 4. Configure kun.py
```python
'YourName': {
    'arpa_id': 'R001',
    'picture': r'C:\path\to\photo.jpg',
    'mail': 'your@email.com',
    ...
}
```

### 5. Run OPSIIE
```bash
python OPSIIE_0_3_79_XP.py
```

## 📝 Essential Commands

**Memory:**
```bash
/memorize Important information
/recall keyword
/forget
```

**AI Generation:**
```bash
/imagine futuristic city
/video sunset
/music jazz piano
```

**Voice:**
```bash
/voice
[speak commands]
"voice off"
```

**Files:**
```bash
/read "C:\file.pdf"
What are the conclusions?
/close
```

**R-Grade Only:**
```bash
/ask Nyx Python blockchain code
/markets tesla
/dna ATGCGTAACGGC
/0x buy 10 degen using eth on base
```

## 🎯 Next Steps

1. [First Run Guide](../getting-started/first-run.md)
2. [Basic Commands](basic-commands.md)
3. [Memory Management](memory-management.md)

---

**Start your journey with OPSIIE!** 🚀