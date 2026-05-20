# Architecture

## High-level diagram

```text
                    ┌──────────────────────┐
                    │ OPSIIE_0_3_80_XP.py  │
                    │   (orchestrator)     │
                    └──────────┬───────────┘
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
   PostgreSQL            ChromaDB              Ollama
 (conversations)    (configured embed model)   (configured models)
         │                    │                    │
         └──────────┬─────────┴────────────────────┘
                    ▼
            Mnemonic store / recall
```

## Startup import order

On `python OPSIIE_0_3_80_XP.py`:

1. Heavy imports (`transformers`, `diffusers`, and others) run first.
2. `sys.path` is adjusted, then **`load_dotenv()`** runs so `.env` values are available before runtime service checks.
3. `web3_handler` is lazy-loaded only when Web3 is initialized or a Web3 command is used. Missing `AGENT_PRIVATE_KEY` or RPC URLs defer Web3 while allowing non-Web3 startup.
4. Other submodules (`utils`, `kun`, `agentic_network`, `markets`, `help`, `mail`, `dna`, `room`, `video`) load according to the import block in the main file.

### Critical coupling: `web3_handler`

`web3_handler` validates wallet and RPC environment variables when the handler is constructed. Non-Web3 features can boot without these values; `/0x` and related Web3 commands report the missing configuration when invoked. For a dedicated Web3 product line, see **[Hermes3](https://github.com/arpahls/Hermes3)**.

## Conversation state

| Symbol | Purpose |
|--------|---------|
| `convo` | Ollama message list; index `0` is the system prompt, rewritten at boot |
| `file_context` | Holds `last_file` text for TAF-3000 follow-ups |
| `current_room` | `Room` instance or `None` |
| `vector_db` | Chroma collection handle for `conversations` |
| `temporary_soul_sig` | Buffer for `/soulsig heal` |
| `webpage_char_limit` | Character cap for `describe_webpage` (500–5000, default 1000) |

## Dual command dispatch

The **main `while` loop** at the end of `OPSIIE_0_3_80_XP.py` intercepts:

- `/weblimit` (via `change_weblimit`)
- `exit` / `quit`
- `/recall`, `/forget`, `/memorize`
- `/help`, `/status`, `/voice`, `/theme`

All other lines, including slash commands not listed above, route to **`handle_user_query()`**.

**Master-only guard** appears in **both** places: `ask`, `markets`, `dna`, `send`, and **`0x`** in the main loop; `handle_user_query` uses a parsed first token list including `0x` for `/0x ...` forms.

## Streaming path

`stream_response` calls `ollama.chat()` using the configured chat model (defaults to `llama3`), prints `OPSIE:` with pastel styling, then `store_conversations` persists to PostgreSQL and Chroma using the configured embedding model. Optional ElevenLabs playback runs when voice flags are active.

## Room architecture

`room.py` defines `Room`:

- Injects OPSIE system text plus `get_agent_description()` for each summoned agent (`nyx`, `g1`; OPSIE always present).
- Maintains `conversation_history` and a **dedicated Chroma collection** named `room_<slug>`.
- Chooses responding agent via embedding similarity heuristics.
- On close, optional CSV export under `outputs/rooms/`.

For a **standalone** evolution of multi-agent rooms (outside this monolith), see **[arpahls/rooms](https://github.com/arpahls/rooms)**.

## Agentic network

See `agentic_network.py`:

- **Nyx:** OpenAI Assistants API (`ask_model`).
- **G1:** Google Gemini `generateContent`.
- **G1 live:** ElevenLabs ConvAI WebSocket (`G1_VOICE_LIVE`).
- **Kronos live:** Parallel scaffold using `KRONOS_LIVE`.

## Multimodal

| Capability | Implementation |
|------------|----------------|
| Image URLs | `describe_image` — BLIP (`Salesforce/blip-image-captioning-base`) |
| Web URLs | `describe_webpage` — `requests` + BeautifulSoup |
| `/imagine` | Hugging Face Inference HTTP POST; **`HUGGINGFACE_API_KEY` or `HF_TOKEN`** from `.env` |
| `/music` | MusicGen small (`facebook/musicgen-small`) |
| `/video` | `video.py` `handle_video_command` and `DiffusionPipeline` map |

## Persistence formats

- **PostgreSQL:** relational chat log with monotonic `id`.
- **Chroma:** embedding sidecar keyed by stringified `id`.
- **`kun.py`:** Python literal dict edited in place for soul signatures (via `save_known_user_names()`).

## Known structural notes (0.3.80 XP)

- **`toggle_voice_mode` and `load_custom_sounds`** each appear twice in `OPSIIE_0_3_80_XP.py`; Python retains the last definition. Treat behavior as **whatever the lower copy implements** until a refactor merges them.
- **Custom MFCC word map** uses hardcoded absolute WAV paths in the default `custom_words` dict; relocate for your machine.

See [BOOT_AND_SECURITY.md](BOOT_AND_SECURITY.md) and [SECURITY.md](../SECURITY.md).
