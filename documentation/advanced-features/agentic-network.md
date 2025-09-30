# Agentic Network & Rooms

Multi-agent collaboration system with Nyx, G1 Black, and Kronos agents.

## 🤖 Agents

**OPSIIE**: Main coordinator, all features
**Nyx (OpenAI)**: Blockchain, AI, Python prototyping
**G1 Black (Gemini)**: Quantum, technical analysis, live voice
**Kronos**: Greek auditing, compliance, live voice

## 📝 Commands

### /ask Agent
```bash
/ask Nyx <prompt>
/ask G1 <prompt>
/ask Kronos <prompt>
```

### Live Voice
```bash
/ask g1 live      # Real-time voice with G1
/ask kronos live  # Real-time voice with Kronos
```

### Rooms
```bash
/room <agents>: <theme>
/room nyx, g1: Quantum computing
/close  # Close and save room
```

## 🔧 Setup

Requires R-Grade access and API keys in .env:
- OPENAI_API_KEY
- GOOGLE_API_KEY  
- G1_VOICE_LIVE
- KRONOS_LIVE

---

**Collaborative intelligence.**
