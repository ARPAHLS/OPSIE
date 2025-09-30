# Error Codes & Troubleshooting

Common OPSIIE errors and solutions.

## 🚨 Authentication
**Face Recognition Failed**: Check lighting, camera, photo in kun.py
**Camera Not Detected**: Verify connection, permissions, not in use

## 🔌 Database
**Connection Failed**: Start PostgreSQL, check .env credentials
**Table Not Found**: Create conversations table (see installation.md)

## 🎤 Voice
**Microphone Not Found**: Check connection, Windows default, permissions
**ElevenLabs API Error**: Verify ELEVENLABS_API_KEY in .env
**Recognition Failed**: Speak clearly, reduce noise, check internet

## 🤖 AI Models
**Ollama Not Running**: Start Ollama, `ollama pull llama3`
**Model Loading (503)**: Wait 2-5 min, retry, or change model
**GPU Not Available**: Install CUDA, or use CPU (slower)

## 📧 Email
**SMTP Auth Failed**: Use Gmail app password (not regular password), enable 2FA
**Cannot Send**: Check internet, Gmail SMTP, recipient addresses
**IMAP Failed**: Enable IMAP in Gmail, verify credentials

## 📁 Files
**File Not Found**: Use absolute paths, check exists, quote spaces
**Unsupported Format**: Use PDF, CSV, DOCX, TXT, XLSX only
**Extraction Failed**: Check file not corrupted, encoding, password

## 🔗 Web3
**Insufficient Balance**: Check `/0x receive`, add funds
**Transaction Failed**: Increase gas `/0x gas high`, check approvals
**RPC Error**: Verify RPC URLs in .env, check internet

## 🤖 Agents
**Agent Not Responding**: Check API keys, internet, rate limits
**Live Mode Failed**: Verify agent IDs in .env, check ElevenLabs
**Room Creation Failed**: Use correct names (nyx, g1, kronos)

## 📊 Markets
**Symbol Not Found**: Check ticker spelling on Yahoo Finance
**Data Timeout**: Retry, check internet, simplify query

## 🧬 DNA
**Invalid Sequence**: DNA=ATGC, RNA=AUGC, Protein=valid AA, no spaces
**NCBI Error**: Set NCBI_EMAIL in .env, check internet

## 🔐 Access Control
**Restricted Command**: R-Grade required, check ARPA ID in kun.py

## 📞 Support
Email: opsiebyarpa@gmail.com

---

**Quick troubleshooting reference.** 🔧
