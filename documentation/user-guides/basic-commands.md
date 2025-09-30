# Basic Commands

Essential OPSIIE commands for daily use.

## 🧠 Memory Commands

```bash
/recall <keyword>        # Retrieve memories
/memorize <message>      # Store information  
/forget                  # Exclude last interaction
/soulsig <message>       # Add to Soul Signature
/soulsig                 # View Soul Signature
/soulsig wipe            # Clear Soul Signature
/soulsig heal            # Restore Soul Signature
```

## 🎤 Voice Commands

```bash
/voice          # Full voice mode (speak & listen)
/voice1         # OPSIIE speaks, you type
/voice2         # You speak, OPSIIE types
/voiceoff       # Disable voice mode
```

## 🎨 AI Generation

```bash
/imagine <description>         # Generate image
/imagine model                 # Check current model
/imagine model <name>          # Change model

/video <description>           # Generate video
/video model                   # Check current model
/video model <name>            # Change model

/music <description>           # Generate music
```

## 📧 Communication

```bash
/mail <email> subject "<subject>" content "<message>"
/mail inbox                    # View unread emails
# In email: reply, inbox, exit
```

## 📁 Document Intelligence

```bash
/read "<file_path>"     # Load file (PDF, CSV, DOCX, TXT, XLSX)
<ask questions>         # Query file content
/open                   # Reopen last file
/close                  # Close file context
```

## ⚙️ System Commands

```bash
/status         # System diagnostics
/theme          # Change color theme
/weblimit <n>   # Set web content limit (500-5000)
/help           # Show help menu
/help <command> # Detailed command help
```

## 🤖 R-Grade Commands

**Agentic Network:**
```bash
/ask <agent> <prompt>    # Query AI agent
/ask g1 live             # Live voice with G1
/ask kronos live         # Live voice with Kronos
/room <agents>: <theme>  # Create collaboration room
```

**Markets:**
```bash
/markets <stock>          # Stock data
/markets <crypto>         # Crypto data
/markets <company> <extra>  # Detailed analysis
/markets compare <a> <b>  # Compare stocks
```

**DNA:**
```bash
/dna <sequence>          # Analyze DNA/RNA/Protein
/dna --verbose <seq>     # Detailed analysis
/dna --homology <seq>    # With homology search
```

**Web3:**
```bash
/0x buy <amt> <token> using <token> on <chain>
/0x sell <amt> <token> for <token> on <chain>
/0x send <chain> <token> <amt> to <recipient>
/0x receive              # View wallets
/0x gas <low|medium|high>  # Set gas strategy
```

## 💡 Tips

**Memory Best Practices:**
- Be specific in /memorize
- Use keywords in /recall
- Build your Soul Signature

**Voice Tips:**
- Clear speech for recognition
- Use voice commands naturally
- "voice off" to exit

**File Processing:**
- Use full file paths
- Ask specific questions
- Close context when done

## 📚 Learn More

- [Memory Management](memory-management.md)
- [First Time User](first-time-user.md)
- [Command Reference](../api-reference/command-reference.md)

---

**Master the essentials.** ✨