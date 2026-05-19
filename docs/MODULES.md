# Module reference

## `OPSIIE_0_3_80_XP.py`

**Responsibilities:** ANSI theme helpers; global state; splash; voice capture and speak; biometric authentication; `boot_up_sequence`; SQL and Chroma memory; `/recall` query expansion; BLIP and webpage enrichment; `/imagine`, `/music`; command router; main loop.

**Key globals:** `convo`, `vector_db`, `file_context`, `current_room`, `webpage_char_limit`, voice flags, lazy `web3_handler`.

**Note:** Duplicate function definitions exist (`toggle_voice_mode`, `load_custom_sounds`); Python uses the last binding in the file.

## `terminal_colors.py`

Pastel and Vibrant palettes, `select_theme()`, and helpers consumed by the main file for printing.

## `utils.py`

Extended OPSIE system prompt (identity, ethics, capability catalog); random dreaming strings; directory helpers; safe filename from prompt; master greetings; `AGENT_DISPLAY_NAMES` and `get_agent_intro` templates.

## `kun.py`

Canonical user directory; **`save_known_user_names()`** rewrites the dict literal in-file while preserving helper functions.

## `kun.example.py`

Large commented template for teams that need many profiles — copy patterns into private `kun.py` as needed.

## `help.py`

`display_help()` grouped listing; `detailed_help_texts` long-form per command; pygame bell.

## `agentic_network.py`

API clients; `ask_model` router; `start_live_g1_conversation`; asyncio websocket loops for G1 and Kronos; PyAudio duplex streaming for live modes.

## `markets.py` + `markets_mappings.py`

Keyword resolution; sector batch quotes; company panels; currency and crypto panels; `compare`; extras such as `statistics`, `financials`, and others per `help.py`.

## `web3_handler.py`

Multi-chain Web3 connections; gas strategy; ERC20 ABI subset; router swaps; user name to address resolution via `kun.py`; runtime mutation of token and chain tables for `/0x new` and `/0x forget`.

## `mail.py`

Regex-based unstructured composer; SMTP send; IMAP inbox browser.

## `dna.py`

GDDA toolkit: sequence classification, reports, NCBI tooling, RNA and protein analytics.

## `video.py`

Lazy `VideoGenerator`; model switch; MP4 export under `outputs/videos/`; optional browser open.

## `room.py`

**Responsibilities:** `Room` class; MiniLM embeddings for response scoring; Chroma logging; CSV export prompt on close under `outputs/rooms/`.

**Related:** **[arpahls/rooms](https://github.com/arpahls/rooms)** — standalone multi-agent room runtime and tooling; use when collaboration spaces should be decoupled from the OPSIIE process.

## Cross-module constants

- `MODEL_APIS` in `agentic_network.py` enumerates remote endpoints for boot messaging.
- `keyword_mapping` in `markets_mappings.py` drives `/markets` resolution.

## Suggested refactor map (non-binding)

| Concern | Suggested direction |
|---------|---------------------|
| Secrets | `.env` only; never literals in Python |
| Paths | Single `paths.py` or config module |
| Web3 import | Lazy import after optional feature flag |
| Duplicate defs | Merge `toggle_voice_mode` / `load_custom_sounds` |
