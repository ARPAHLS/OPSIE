<div align="center">

```
 ███             ███████    ███████████   █████████  █████ █████ ██████████
░░░███         ███░░░░░███ ░░███░░░░░███ ███░░░░░███░░███ ░░███ ░░███░░░░░█
  ░░░███      ███     ░░███ ░███    ░███░███    ░░░  ░███  ░███  ░███  █ ░ 
    ░░░███   ░███      ░███ ░██████████ ░░█████████  ░███  ░███  ░██████   
     ███░    ░███      ░███ ░███░░░░░░   ░░░░░░░░███ ░███  ░███  ░███░░█   
   ███░      ░░███     ███  ░███         ███    ░███ ░███  ░███  ░███ ░   █
 ███░         ░░░███████░   █████       ░░█████████  █████ █████ ██████████
░░░             ░░░░░░░    ░░░░░         ░░░░░░░░░  ░░░░░ ░░░░░ ░░░░░░░░░░ 
```

### OPSIIE 0.3.80 XP

**A Self-Centered Intelligence (SCI) Prototype**

*By ARPA HELLENIC LOGICAL SYSTEMS · 03 Jul 2025 · Main entry `OPSIIE_0_3_80_XP.py`*

[![Python](https://img.shields.io/badge/Python-3.8%2B-bdd7ff?style=flat-square)](https://www.python.org/downloads/)
[![Ollama](https://img.shields.io/badge/Ollama-0.3%2B-cfe8d6?style=flat-square)](https://ollama.com/)
[![Llama 3](https://img.shields.io/badge/Chat-llama3-f4d7ff?style=flat-square)](https://ollama.com/library/llama3)
[![nomic-embed-text](https://img.shields.io/badge/Embed-nomic--embed--text-f8e7c9?style=flat-square)](https://ollama.com/library/nomic-embed-text)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14%2B-e8d6ff?style=flat-square)](https://www.postgresql.org/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-0.4%2B-bdd7ff?style=flat-square)](https://www.trychroma.com/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%28primary%29-cfe8d6?style=flat-square)](https://www.microsoft.com/windows)
[![ARPA](https://img.shields.io/badge/ARPA-Hellenic%20Logical%20Systems-e8d6ff?style=flat-square)](https://arpacorp.net)

OPSIE is a **terminal personality with agency and memory** that can act as a **daily driver assistant for technical work**: recall what you said last week, riff on files and URLs, spin up images or clips, pull market or chain data, draft and send mails, and run structured DNA workflows, all under **one session** and **your own infrastructure**. Slash commands, boot flow, and module layout are documented in [`docs/`](docs/README.md).

<p align="center">
  <a href="#mission">Mission</a> ·
  <a href="#repository-layout">Layout</a> ·
  <a href="#quick-start">Quick start</a> ·
  <a href="#documentation-map">Docs</a> ·
  <a href="#runtime-dependencies">Runtime</a> ·
  <a href="#access-control">Access</a> ·
  <a href="#related-arpa-repositories">ARPA links</a> ·
  <a href="#license-and-support">License</a>
</p>

</div>

---

## Related ARPA repositories

| Project | Use when you need |
|--------|-------------------|
| [**Skillware**](https://github.com/arpahls/skillware) | Modular, installable agent **skills** (logic + governance + tool schemas) decoupled from a single monolith. |
| [**Hermes3**](https://github.com/arpahls/Hermes3) | Standalone, production-oriented **Web3** agent and parsing stack beyond the bundled `/0x` handler here. |
| [**Gatekeeper**](https://github.com/arpahls/gatekeeper) | Standalone **facial recognition and emotion** gateway patterns (liveness, policy layers) instead of only the built-in boot gate. |
| [**Rooms**](https://github.com/arpahls/rooms) | **Standalone multi-agent room runtime** and tooling when you want collaboration spaces decoupled from the OPSIIE monolith; the bundled `/room` command here is the in-session counterpart. |
| [**vic_aisaq_demo**](https://github.com/arpahls/vic_aisaq_demo) | Reference demos around **VIC / AISAQ** style agent and evaluation flows. |

For coordinated disclosure and secret handling, see [SECURITY.md](SECURITY.md).

---

## Mission

OPSIIE (also referred to as **OPSIE**) is a terminal-first SCI prototype: a single long-running Python application that combines **local LLM conversation** (Ollama), **durable conversation storage** (PostgreSQL), **semantic recall** (ChromaDB with query expansion and embedding classification), **multimodal tooling** (image via Hugging Face Inference, music via MusicGen, video via diffusers, URL vision via BLIP, web text extraction), **agent routing** (OpenAI Assistants for Nyx, Google Gemini for G1, ElevenLabs for TTS and live G1), **Yahoo Finance markets**, **Web3** (`/0x`), **SMTP and IMAP mail**, **collaborative multi-agent rooms** (see also the standalone [**Rooms**](https://github.com/arpahls/rooms) project), and **GDDA biosequence analysis**. It is designed as an integrated research and demonstration stack rather than a minimal chat wrapper.

Boot-time logs mirror the experience you see when running locally: **[Security]** facial and emotion checks, **[System]** prompt and SoulSig verification, **[Network]** mnemonic matrix and mail, **[Hardware]** Chroma population (for example a full progress bar when hydrating embeddings), **[SCI Systems]** response engine, sensors, dream engine, DNA and market probes, and agentic nexus readiness—aligned with the **OPSIIE** branding in the splash and terminal gradient.

## Repository layout

| Path | Role |
|------|------|
| `OPSIIE_0_3_80_XP.py` | Entry point: theme selection, splash, biometric gate, boot sequence, command router, memory I/O, voice orchestration, streaming chat, URL and file enrichment |
| `terminal_colors.py` | Pastel and Vibrant ANSI palettes and `select_theme()` |
| `utils.py` | System prompt, agent display metadata, dreaming phrases, filename helpers, master greetings |
| `kun.py` | User registry: ARPA ID, wallet, PostgreSQL `db_params`, enrollment photo path, mail, soul signature; `save_known_user_names()` persists edits |
| `kun.example.py` | Large multi-user template for copying into private `kun.py` if you outgrow the default profile |
| `help.py` | `/help` screen and per-command narrative help (`detailed_help_texts`) |
| `agentic_network.py` | Nyx (OpenAI), G1 (Gemini), live G1 WebSocket session, Kronos live scaffold, model dispatch |
| `markets.py` / `markets_mappings.py` | Yahoo Finance-backed `/markets` with sector maps and company extras |
| `web3_handler.py` | `/0x` family: swaps, sends, gas, custom tokens and chains (**exits process if env incomplete at import**) |
| `mail.py` | SMTP send and IMAP inbox loop |
| `dna.py` | GDDA DNA, RNA, and protein pipelines |
| `video.py` | Local diffusers-based text-to-video with pluggable model keys |
| `room.py` | In-process **temporal nexus** (`/room`): multi-agent scoring, Chroma-backed session log, CSV export under `outputs/rooms/`. For a **standalone** room stack, see [arpahls/rooms](https://github.com/arpahls/rooms). |
| `requirements.txt` | Dependency intent for the full stack (Python, Ollama client, ChromaDB, and stack versions are reflected in the badges above) |
| `.env.example` | Environment variable template (copy to `.env`) |
| `docs/opsiie-splash.png` | Local copy of the [OPSIE splash asset](https://github.com/ARPAHLS/OPSIE/blob/main/opsiie%20splash.png); shown under [Quick start](#quick-start) in this README |
| `assets/README.txt` | Guidance for biometric enrollment image `enrollment.jpg` |

## Quick start

<div align="center">

<img src="./docs/opsiie-splash.png" alt="OPSIIE splash" width="100%" />

</div>

### 1. Prerequisites

- **Python 3.8+** (GPU strongly recommended for `/music` and `/video`)
- **PostgreSQL 14+** with a `conversations` table in each database referenced by `kun.py` (see [docs/CONFIGURATION.md](docs/CONFIGURATION.md))
- **Ollama** **0.3+** with **`llama3`** and **`nomic-embed-text`** available locally
- **ChromaDB** **0.4+** (via `pip` / `requirements.txt`; in-process client in the stock build)
- **Camera and microphone** for default authentication and voice paths
- **Windows** is the primary tested platform; paths in optional voice assets may use drive letters

### 2. Install

```powershell
cd d:\Agents\OPSIIE_0_3_80_XP
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### 3. Configure

1. Copy `.env.example` to `.env` and fill values. Web3 variables are **mandatory for import** (see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)).
2. Set **`HUGGINGFACE_API_KEY`** or **`HF_TOKEN`** for default `/imagine` (Hugging Face Inference API).
3. Edit `kun.py`: replace the template `Demo Operator` profile with your `db_params`, `mail`, `arpa_id`, and paths. Add **`assets/enrollment.jpg`** (see [assets/README.txt](assets/README.txt)).
4. Align optional **custom voice shortcut** media paths in `OPSIIE_0_3_80_XP.py` (`custom_words` dictionary) if you use MFCC hooks; defaults reference developer machine paths.

### 4. Run

```powershell
python OPSIIE_0_3_80_XP.py
```

Session flow: **theme selection** → **splash** → **face and emotion gate** → **PostgreSQL and Chroma mnemonic checks** → **Ollama probe** → **sensor check** → **Web3 handler construction** → **mail check** → **dream engine probes** → **advanced analysis smoke** → **agentic network probe** → **optional five-second voice latch** → interactive loop.

## Documentation map

| Document | Contents |
|----------|----------|
| [docs/COMMANDS.md](docs/COMMANDS.md) | Slash commands, subcommands, voice phrasing, dual dispatch notes, examples |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Module graph, globals, Web3 import coupling, streaming path |
| [docs/BOOT_AND_SECURITY.md](docs/BOOT_AND_SECURITY.md) | Boot stages, DeepFace policy, face match, `/status` behavior |
| [docs/MEMORY_AND_RAG.md](docs/MEMORY_AND_RAG.md) | PostgreSQL schema, Chroma collection, recall and forget semantics |
| [docs/VOICE.md](docs/VOICE.md) | `/voice`, `/voice1`, `/voice2`, ElevenLabs, Google STT, custom sounds |
| [docs/CONFIGURATION.md](docs/CONFIGURATION.md) | Environment variables, `kun.py` schema, output directories |
| [docs/MODULES.md](docs/MODULES.md) | File-by-file responsibilities and extension points |
| [docs/PROMPTS_AND_SOULSIG.md](docs/PROMPTS_AND_SOULSIG.md) | System prompt role, Soul Signature hierarchy, `utils.py` overview |
| [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Common failures, path migration, model cold starts |
| [docs/README.md](docs/README.md) | Index inside the `docs/` folder |

## Runtime dependencies

- **Ollama:** `llama3` for chat and query expansion; `nomic-embed-text` for mnemonic embeddings (pull both in Ollama).
- **PostgreSQL:** per-user `dbname` from the authenticated `kun.py` entry.
- **ChromaDB:** in-process client; global collection name **`conversations`**; room sessions use separate collections.
- **Optional and remote APIs:** OpenAI (Nyx), Google Generative AI (G1), ElevenLabs (TTS and live agents), Hugging Face Inference (default `/imagine`), Yahoo Finance, NCBI e-utilities (polite `NCBI_EMAIL`).

## Access control

- **`arpa_id` starting with `R`:** Master access to experimental commands: `/ask`, `/markets`, `/dna`, **`/0x`** (and legacy **`send`** shows migration text).
- **Other IDs:** Restricted; attempts print a denial path via `handle_restricted_command()`.

The **main input loop** and **`handle_user_query()`** both enforce gating. **`0x`** is included in the main-loop check so non-master users cannot bypass Web3 commands.

## License and support

- **Proprietary:** see [LICENSE](LICENSE).
- **Email:** [opsiebyarpa@gmail.com](mailto:opsiebyarpa@gmail.com)
- **Web:** [https://arpacorp.net](https://arpacorp.net) | [https://arpa.systems](https://arpa.systems)
- **Governance:** [CONTRIBUTING.md](CONTRIBUTING.md), [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md), [SECURITY.md](SECURITY.md)

---

<div align="center">
    <img src="https://raw.githubusercontent.com/ARPAHLS/.github/main/Group%202061.png" alt="ARPA Logo" width="50" />
    <br/>
    Built & Maintained by ARPA Hellenic Logical Systems & the Community
</div>

*"We move where life is gonna be, not where it was."*  
— Ross Peili, Main Human @ ARPA Corp.
