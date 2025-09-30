# Command Reference

Complete reference of all OPSIIE commands.

## 🧠 Memory Commands

### /recall
**Retrieve relevant memories**
```bash
/recall <keyword>
```
**Examples**: `/recall project x`, `/recall quantum computing`

### /memorize
**Store important information**
```bash
/memorize <message>
```
**Examples**: `/memorize Deadline is Friday`, `/memorize I prefer Python`

### /forget
**Exclude last interaction from memory**
```bash
/forget
```

### /soulsig
**Manage Soul Signature**
```bash
/soulsig                 # View
/soulsig <message>       # Add
/soulsig wipe            # Clear (permanent)
/soulsig heal            # Restore (if recent)
```

## 🎤 Voice Commands

### /voice
**Full voice mode (speak & listen)**
```bash
/voice
```
Exit: Say "voice off"

### /voice1
**OPSIIE speaks, you type**
```bash
/voice1
```

### /voice2
**You speak, OPSIIE types**
```bash
/voice2
```

### /voiceoff
**Disable voice mode**
```bash
/voiceoff
```

## 🎨 AI Generation Commands

### /imagine
**Generate images**
```bash
/imagine <description>
/imagine model                    # Check current model
/imagine model <model_name>       # Change model
```
**Examples**: `/imagine futuristic city`, `/imagine model hakurei/waifu-diffusion`

### /video
**Generate videos**
```bash
/video <description>
/video model                      # Check current model
/video model <model_name>         # Change model
```
**Examples**: `/video sunset timelapse`, `/video model zeroscope`

### /music
**Generate music**
```bash
/music <description>
```
**Examples**: `/music jazz piano`, `/music ambient soundscape`

## 📧 Communication Commands

### /mail
**Send emails**
```bash
/mail <emails> subject "<subject>" content "<message>"
```
**Examples**: 
- `/mail john@gmail.com subject "Hello" content "Test"`
- `/mail Ross subject "Update" content "Latest info"`

### /mail inbox
**View unread emails**
```bash
/mail inbox
```
Commands in inbox: number to read, `reply`, `inbox`, `exit`

## 📁 Document Commands

### /read
**Load and analyze files**
```bash
/read "<file_path>"
```
Supports: PDF, CSV, DOCX, TXT, XLSX
**Example**: `/read "C:\Documents\report.pdf"`

### /open
**Reopen last file context**
```bash
/open
```

### /close
**Close file context**
```bash
/close
```

## ⚙️ System Commands

### /status
**System diagnostics**
```bash
/status
```

### /theme
**Change color theme**
```bash
/theme
```
Options: Pastel, Vibrant

### /weblimit
**Set web content extraction limit**
```bash
/weblimit <number>
```
Range: 500-5000 characters
**Example**: `/weblimit 2000`

### /help
**Display help**
```bash
/help                    # Main menu
/help <command>          # Specific command help
```
**Examples**: `/help imagine`, `/help markets`

## 🤖 R-Grade: Agentic Network

### /ask
**Query AI agents**
```bash
/ask <agent> <prompt>
```
Agents: Nyx, G1, Kronos
**Examples**:
- `/ask Nyx Write Python blockchain code`
- `/ask G1 Analyze quantum computing`
- `/ask Kronos Greek audit procedures`

### /ask live
**Live voice conversations**
```bash
/ask g1 live             # G1 Black real-time voice
/ask kronos live         # Kronos real-time voice
```
Exit: Press Ctrl+C

### /room
**Create collaboration room**
```bash
/room <agent1, agent2...>: <theme>
```
**Examples**:
- `/room nyx, g1: Quantum computing applications`
- `/room nyx: Python microservices design`

Close room: `/close` (prompts to save as CSV)

## 📊 R-Grade: Financial Intelligence

### /markets
**Market data and analysis**
```bash
/markets <symbol>                  # Basic data
/markets <symbol> <extra>          # Detailed analysis
/markets compare <sym1> <sym2>     # Compare stocks
```

**Extras**: `statistics`, `history`, `profile`, `financials`, `analysis`, `options`, `holders`, `sustainability`

**Examples**:
- `/markets tesla`
- `/markets btc`
- `/markets shell statistics`
- `/markets compare tsla nio`

## 🧬 R-Grade: DNA Analysis

### /dna
**Analyze DNA/RNA/Protein sequences**
```bash
/dna <sequence> [options]
```

**Options**:
- `--verbose` - Detailed analysis
- `--type <dna|rna|protein>` - Force type
- `--format <format>` - Input format
- `--export <json|csv|txt>` - Export results
- `--homology` - Include similarity search
- `--structure` - Structure prediction
- `--patents` - Patent search
- `--literature` - Literature search

**Examples**:
- `/dna ATGCGTAACGGCATTAGC`
- `/dna --verbose --homology MAKVLISPKQW`
- `/dna --type rna AUGCGUAACGGCAUUAGC`

## 🔗 R-Grade: Web3 & Blockchain

### /0x buy
**Buy tokens**
```bash
/0x buy <amount> <token> using <token> on <chain>
```
**Example**: `/0x buy 10 degen using eth on base`

### /0x sell
**Sell tokens**
```bash
/0x sell <amount> <token> for <token> on <chain>
```
**Example**: `/0x sell 5 degen for eth on base`

### /0x send
**Send tokens**
```bash
/0x send <chain> <token> <amount> to <recipient>
```
**Example**: `/0x send base eth 0.1 to Ross`

### /0x receive
**View wallet addresses**
```bash
/0x receive
```

### /0x gas
**Set gas strategy**
```bash
/0x gas <low|medium|high>
```

### /0x new
**Add custom token/chain**
```bash
/0x new token <name> <chain> <address>
/0x new chain <name> <chain_id> <rpc_url>
```

### /0x forget
**Remove configuration**
```bash
/0x forget token <name>
/0x forget chain <name>
```
Note: Cannot remove Base, Ethereum, Polygon

## 🚪 Session Commands

### exit / quit
**Terminate OPSIIE session**
```bash
exit
quit
```
Do not use `/` prefix

## 📋 Command Categories

**All Users:**
- Memory: `/recall`, `/memorize`, `/forget`, `/soulsig`
- Voice: `/voice`, `/voice1`, `/voice2`, `/voiceoff`
- AI Gen: `/imagine`, `/video`, `/music`
- Email: `/mail`, `/mail inbox`
- Files: `/read`, `/open`, `/close`
- System: `/status`, `/theme`, `/weblimit`, `/help`

**R-Grade Only:**
- Agents: `/ask`, `/ask live`, `/room`
- Markets: `/markets`
- DNA: `/dna`
- Web3: `/0x`

## 🔑 Access Control

**R-Grade**: ARPA ID starts with 'R' (e.g., R001)
**A-Grade**: ARPA ID starts with 'A' (e.g., A001)

Check kun.py for your access level.

---

**Complete command reference.** 📚