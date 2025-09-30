# Voice Interaction System

OPSIIE's voice system provides comprehensive voice input/output capabilities using ElevenLabs for synthesis and Google Speech Recognition for input.

## 🎤 Overview

Voice capabilities include:
- **Full Voice Mode**: Both speak and listen
- **Voice Output Only**: OPSIIE speaks, you type
- **Voice Input Only**: You speak, OPSIIE types
- **Multi-Agent Voices**: Different voices for Nyx, G1, and OPSIIE
- **Voice Commands**: Natural language command detection
- **Live Voice Conversations**: Real-time voice chat with AI agents

## 🔧 Voice Modes

### /voice - Full Voice Mode
**Both speak and listen**

```bash
/voice
```

**Features:**
- OPSIIE speaks responses using ElevenLabs
- You speak commands/queries
- Natural conversation flow
- 20-second inactivity timeout
- Automatic voice command detection

**How to Use:**
1. Type `/voice` or say "voice"
2. Wait for activation confirmation
3. Speak naturally
4. OPSIIE responds with voice
5. Continue conversation
6. Say "voice off" or "exit voice mode" to deactivate

**Example Session:**
```
You: /voice
OPSIIE: "Verbal communication protocol established."

You: [speak] "What's the weather like?"
OPSIIE: [speaks response]

You: [speak] "voice off"
OPSIIE: "Verbal communication protocol bridge collapsed successfully."
```

### /voice1 - OPSIIE Speaks, You Type
**Output-only voice mode**

```bash
/voice1
```

**Use Cases:**
- Want to hear responses
- Prefer typing for accuracy
- Noisy environment
- Hands-free response consumption

**Example:**
```
You: /voice1
OPSIIE: [speaks] "Voice output mode activated."

You: [type] Tell me about quantum computing
OPSIIE: [speaks response]

You: /voiceoff
```

### /voice2 - You Speak, OPSIIE Types
**Input-only voice mode**

```bash
/voice2
```

**Use Cases:**
- Hands-free input
- Faster than typing
- Accessibility
- Quiet environment for reading

**Example:**
```
You: /voice2
OPSIIE: Voice input mode activated.

You: [speak] "Explain neural networks"
OPSIIE: [types response]

You: /voiceoff
```

### /voiceoff - Disable Voice Mode
**Deactivate all voice features**

```bash
/voiceoff
```

Or voice command:
```
"voice off"
"exit voice mode"
```

## 🗣️ Voice Commands

### Natural Language Detection
Voice mode automatically detects command intent from natural speech:

**Memory Commands:**
```
"recall my last project"           → /recall last project
"memorize this is important"       → /memorize this is important
```

**System Commands:**
```
"status"                           → /status
"help"                             → /help
"theme"                            → /theme (opens theme selector)
```

**AI Generation:**
```
"imagine a futuristic city"        → /imagine a futuristic city
"generate music jazz piano"        → /music jazz piano
"create video of sunset"           → /video sunset
```

**File Operations:**
```
"read the file report.pdf"         → /read "report.pdf"
"open the document"                → /open
"close file context"               → /close
```

### Voice Command Examples
```bash
# Works in voice mode:
You: [speak] "recall our discussion about AI"
OPSIIE: [executes /recall] [speaks results]

You: [speak] "memorize project deadline is Friday"
OPSIIE: [executes /memorize] [confirms]

You: [speak] "show me system status"
OPSIIE: [executes /status] [displays status]

You: [speak] "imagine a cyberpunk cityscape"
OPSIIE: [executes /imagine] [generates image] [confirms]
```

## 🎭 Multi-Agent Voices

### Agent Voice Configuration
Each AI agent has a unique voice configured via ElevenLabs:

```env
# .env configuration
VOICE_ID=your_opsiie_voice_id        # OPSIIE's voice
NYX_VOICE_ID=your_nyx_voice_id       # Nyx's voice
G1_VOICE_ID=your_g1_voice_id         # G1 Black's voice
```

### Agent Voice Usage

**OPSIIE Voice:**
```bash
# Default for all OPSIIE responses
You: Tell me about AI
OPSIIE: [responds in OPSIIE voice]
```

**Nyx Voice:**
```bash
/ask Nyx What are the latest quantum computing developments?
# Nyx responds in Nyx's voice (if voice mode active)
```

**G1 Black Voice:**
```bash
/ask G1 Analyze this technical problem
# G1 responds in G1's voice (if voice mode active)
```

## 📞 Live Voice Conversations

### G1 Live Voice
**Real-time voice conversation with G1 Black**

```bash
/ask g1 live
```

**Features:**
- Direct WebSocket connection to ElevenLabs
- Real-time audio streaming
- Continuous conversation
- Press Ctrl+C to end

**How It Works:**
1. Establishes WebSocket connection
2. Starts audio input/output streams
3. You speak, G1 responds immediately
4. Continues until manually stopped

**Example Session:**
```
You: /ask g1 live

[System]: Live conversation with G1 Black initialized.
[System]: Speak naturally. Press Ctrl+C to end the conversation.

You: [speak] What's happening with Bitcoin?
G1 Black: [responds in real-time]

You: [speak] And what about Ethereum?
G1 Black: [responds immediately]

[Press Ctrl+C]
[System]: Ending live conversation...
[System]: Live conversation session concluded.
```

### Kronos Live Voice
**Live conversation with Kronos (Greek Internal Auditor)**

```bash
/ask kronos live
```

Similar to G1 live mode, specialized for Greek internal auditing.

## 🔊 Voice Synthesis (ElevenLabs)

### Configuration
```env
ELEVENLABS_API_KEY=your_api_key
VOICE_ID=your_voice_id
```

### How It Works
1. Text response generated by OPSIIE
2. Sent to ElevenLabs API
3. Audio synthesized with specified voice
4. Streamed and played back
5. Temporary file cleaned up

### Voice Parameters
- **Optimize Streaming**: Latency=3 (fastest)
- **Format**: MP3
- **Playback**: pygame.mixer
- **Cleanup**: Automatic temp file deletion

### API Verification
OPSIIE verifies ElevenLabs API on startup:
```
Checking Eleven Labs API access... ✓
```

## 🎧 Speech Recognition (Google)

### How It Works
1. Microphone captures audio
2. Google Speech API transcribes
3. Text processed as command/query
4. OPSIIE responds

### Recognition Settings
- **Engine**: Google Speech Recognition
- **Language**: English (default)
- **Timeout**: 20 seconds inactivity
- **Format**: 16-bit PCM

### Microphone Configuration
```python
recognizer = sr.Recognizer()
mic = sr.Microphone()
```

### Custom Word Recognition
OPSIIE has enhanced recognition for specific phrases:

**Custom Audio Patterns:**
```python
custom_words = {
    "Opsie": [...],
    "Voice off": [...],
    "send Base Degen": [...],
    # ... custom patterns
}
```

Uses MFCC (Mel-frequency cepstral coefficients) for pattern matching.

## 💡 Best Practices

### For Best Recognition

**DO:**
- Speak clearly and at normal pace
- Use natural language
- Pause between commands
- Minimize background noise
- Position microphone correctly

**DON'T:**
- Speak too fast or mumble
- Use overly technical jargon
- Interrupt OPSIIE mid-response
- Use in very noisy environments

### For Best Experience

**Voice Mode Selection:**
```bash
# For hands-free operation
/voice

# For quiet response consumption
/voice1

# For hands-free input only
/voice2
```

**Timeout Management:**
- Voice mode auto-exits after 20 seconds silence
- Keep conversation flowing
- Say "voice off" to exit manually

**Command Clarity:**
```bash
# Clear commands
"recall project alpha"
"memorize deadline Friday"
"imagine cyberpunk city"

# Avoid ambiguous
"that thing"
"you know what I mean"
```

## 🔧 Troubleshooting

### Microphone Not Detected
```
Error: No microphone found
```

**Solutions:**
1. Check microphone connection
2. Verify microphone permissions
3. Set default microphone in Windows
4. Restart application

### Voice Synthesis Errors
```
Error with Eleven Labs API
```

**Solutions:**
1. Check API key validity
2. Verify VOICE_ID is correct
3. Check internet connection
4. Verify API usage limits
5. Check API status at elevenlabs.io

### Recognition Issues
```
Could not understand audio
```

**Solutions:**
1. Speak more clearly
2. Reduce background noise
3. Move closer to microphone
4. Adjust microphone gain
5. Check internet connection

### Voice Mode Won't Deactivate
```
Voice mode stuck
```

**Solutions:**
1. Say "voice off" clearly
2. Press Ctrl+C
3. Type /voiceoff in terminal
4. Restart application

## 🎯 Voice Mode Use Cases

### Research & Writing
```bash
/voice2                          # Hands-free input
[dictate] "Search for papers on quantum entanglement"
[dictate] "Summarize the key findings"
[dictate] "Add this to my research notes"
```

### Accessibility
```bash
/voice                           # Full voice interaction
[speak] commands and queries
[hear] all responses
# Fully hands-free operation
```

### Multitasking
```bash
/voice1                          # Type while hearing responses
[type] Complex queries
[listen] While doing other tasks
```

### Live Consultation
```bash
/ask g1 live                     # Real-time voice chat
[discuss] Technical problems
[get] Immediate responses
[iterate] On solutions
```

## 📊 Voice Statistics

Check voice system status:
```bash
/status
```

Shows:
- Voice mode (active/inactive)
- Current mode (voice/voice1/voice2)
- ElevenLabs API status
- Microphone status
- Speech recognition status

## 🔐 Privacy & Security

### What's Transmitted
- Voice audio to Google for recognition (temporary)
- Text to ElevenLabs for synthesis
- No voice recordings stored locally
- No voice data in conversation history

### Data Protection
- Voice processed in real-time
- No permanent voice storage
- Text-only conversation storage
- API communications encrypted

## 🚀 Advanced Usage

### Voice-Driven Workflows
```bash
# Morning briefing
/voice
[speak] "status"
[speak] "recall yesterday's tasks"
[speak] "what's on the schedule"

# Research session
/voice2
[speak] "read the paper on quantum computing"
[speak] "summarize the methodology"
[speak] "what are the key findings"

# Creative work
/voice
[speak] "imagine a futuristic laboratory"
[speak] "generate music ambient electronic"
[speak] "create video of abstract particles"
```

### Multi-Modal Interaction
```bash
# Mix voice and text
/voice
[speak] "markets tesla"        # Voice command
[read] Market data displayed
[type] /markets compare tsla nio  # Text command for complex syntax
[speak] "what do you think"    # Voice query
```

## 📚 Related Features

- **Live Conversations**: `/ask g1 live`, `/ask kronos live`
- **Command Help**: `/help voice`
- **Theme Changes**: Voice command "theme"
- **Multi-Agent**: Agent-specific voices in `/room`

---

**Voice interaction makes OPSIIE truly hands-free and accessible.** 🎤