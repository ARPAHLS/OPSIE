# Command reference (0.3.80 XP)

Slash commands are evaluated **case-insensitively** for the leading token. Natural language without a leading `/` follows the conversational path (memory substring check, URL expansion, file follow-up, or `stream_response`).

**Master-only** commands when `arpa_id` does **not** start with `R`: **`ask`**, **`markets`**, **`dna`**, **`0x`**, and legacy first-token **`send`** (migration notice only). Enforcement exists in **`handle_user_query()`** and in the **main input loop** (including **`0x`** so `/0x` cannot bypass tier checks).

---

## Session lifecycle

| Input | Behavior |
|-------|----------|
| `exit` or `quit` | In the **main loop**, breaks the `while True` session. Inside `handle_user_query`, first-token `exit`/`quit` calls `sys.exit()`. |
| `/status` | Speaks a short line, prints reboot text, sleeps, then runs **`boot_up_sequence()`** again (full camera auth). |

---

## `/help` and `/help <name>`

- **`/help`** — `display_help()` grouped listing; plays `system_sounds/helpbell.mp3` next to `help.py`.
- **`/help <command>`** — Looks up `<command>` in `detailed_help_texts` (`help.py`). Examples: `/help markets`, `/help 0x`, `/help soulsig`, `/help room`.

Keys include: `recall`, `forget`, `memorize`, `ask`, `markets`, `dna`, `0x`, `receive`, `imagine`, `music`, `read`, `open`, `close`, `weblimit`, `status`, `voice`, `vision`, `mail`, `help`, `soulsig`, `room`, `video`.

---

## Mnemonic matrix (memory)

### `/recall <keyword>`

1. Expands text into search queries via Ollama (`create_queries`).
2. Embeds queries with the configured embedding model, queries Chroma conversations, classifies hits (classify_embedding), merges snippets into convo, then streams a new reply.

Implemented in **both** the main loop and `handle_user_query` with the same high-level pattern.

**Example**

```text
/recall budget spreadsheet assumptions
```

### `/forget`

Deletes the latest PostgreSQL row (max `id`) and the Chroma document with that id; removes the last user/assistant pair from RAM `convo`.

### `/memorize <text>`

Stores a user message with assistant reply `Memory specimen successfully implanted.` so the pair is embedded.

**Example**

```text
/memorize Weekly backup runs Sunday 02:00 local time.
```

---

## Voice

| Command | Description |
|---------|-------------|
| `/voice` | Full duplex voice loop until timeout or `/voiceoff`. |
| `/voice1` | Assistant speaks; you type in the main loop. |
| `/voice2` | You speak; assistant responds in text. |
| `/voiceoff` | Clears voice flags. |

**Boot latch:** `listen_for_voice_command(5)` after boot listens for the word **`voice`** to auto-enable `/voice`.

See [VOICE.md](VOICE.md).

---

## Agentic matrix

### `/ask <model> <prompt>`

- Regex in handler: model first token, remainder is prompt (see `handle_user_query`).
- **`/ask g1 live`** — `start_live_g1_conversation()`; requires `G1_VOICE_LIVE` in `.env`.
- **Nyx** — OpenAI Assistants (`NYX_ASSISTANT_ID`, `OPENAI_API_KEY`, `ORG_ID`).
- **G1** — Google Gemini via `google.generativeai`.

**Examples**

```text
/ask Nyx Outline a minimal REST client with retries and backoff.
/ask G1 Compare optimistic and zk rollups for a settlement layer pitch.
/ask g1 live
```

### `/room <agents>: <theme>`

- Pattern: `/room nyx, g1: fault tolerant control plane design`
- Valid agents (case-insensitive): **`nyx`**, **`g1`** (OPSIE always included internally).
- Regex: `^/room\s+([^:]+):\s*(.+)$` — comma-separated agent list before the colon.

**Standalone rooms:** The in-repo `/room` flow is the **integrated temporal nexus** inside one OPSIIE session. For a **decoupled** multi-agent room runtime and related tooling, see **[arpahls/rooms](https://github.com/arpahls/rooms)** on GitHub.

### `/close`

- If a room is active: `Room.close()` then clears `current_room`.
- If in **file** workflow: clears `file_context` when routed as the `close` command inside `handle_user_query`.

---

## `/markets`

Full resolution lives in `markets.py` / `markets_mappings.py`.

**Shapes**

```text
/markets <sector>
/markets <company_or_alias>
/markets <currency>
/markets <crypto_alias>
/markets <company> <extra>
/markets compare <ticker_or_alias> <ticker_or_alias>
```

**Company extras:** `statistics`, `history`, `profile`, `financials`, `analysis`, `options`, `holders`, `sustainability` (see `/help markets`).

Data source: **yfinance** (network required).

---

## Web3: `/0x` family

Handled by `Web3Handler` (`web3_handler.py`).

For a **standalone, advanced Web3 agent** (dynamic parsing, multi-chain workflows, and analytics-oriented evolution of this stack), see **[Hermes3](https://github.com/arpahls/Hermes3)** in the ARPAHLS organization. OPSIIE keeps `/0x` for integrated terminal sessions; Hermes3 is the better fit when Web3 is the primary product surface.

```text
/0x buy <amount> <token> using <token> on <chain>
/0x sell <amount> <token> for <token> on <chain>
/0x send <chain> <token> <amount> to <recipient>
/0x receive
/0x gas low|medium|high
/0x new token <name> <chain> <address>
/0x new chain <name> <chain_id> <rpc_url>
/0x forget token <name>
/0x forget chain <name>
```

**Legacy:** first token **`send`** prints migration text toward `/0x send ...`.

**Quirk:** **`receive`** without a leading slash is still handled as a command word inside `handle_user_query` (first token `receive`). Prefer **`/0x receive`** for clarity.

---

## `/mail`

```text
/mail inbox
/mail user@example.com subject "Title" content "Body"
```

Natural-language variants are parsed by `send_mail()` (see `/help mail`). **`/mail inbox`** opens the IMAP interaction loop.

---

## `/read`, `/open`, `/close` (TAF-3000)

- **`/read "<path>"`** — Optional trailing text is treated as an immediate follow-up question.
- Extensions handled in code: **`.csv`**, **`.pdf`**, **`.docx`**, **`.txt`**, **`.xlsx`**.
- **`/open`** — Re-arms last file context (does not reload from disk).
- **`/close`** — Clears `file_context`.

**Example**

```text
/read "D:\Reports\quarterly.pdf" Summarize risks in one paragraph.
```

---

## Dreaming (generation)

### `/imagine`

- POSTs to **`HF_API_URL`** (default Hugging Face Inference **FLUX.1-dev** endpoint).
- Bearer token from **`HUGGINGFACE_API_KEY`** or **`HF_TOKEN`** in `.env` (no hardcoded token in 0.3.80 XP).
- **`/imagine model <hf_model_id>`** — Probes with GET then switches URL to `https://api-inference.huggingface.co/models/<id>`.
- Saves PNG under **`outputs/images/`** (created next to the repo) and opens the image viewer when possible.

### `/music`

Local **MusicGen small** (`facebook/musicgen-small`). Saves WAV under **`outputs/music/`** and plays via pygame.

### `/video`

Delegates to `video.py`. Saves MP4 under **`outputs/videos/`** and may open a browser.

---

## `/dna`

Minimum:

```text
/dna ATGCGTAC
```

Flags and extended modes are documented in `/help dna` and implemented in `dna.py`. Remote etiquette may require **`NCBI_EMAIL`**.

---

## `/weblimit`

```text
/weblimit
/weblimit 2000
/weblimit default
```

Controls HTML paragraph extraction length for `describe_webpage` (default **1000**, allowed band **500–5000**). The main loop calls `change_weblimit()`; `handle_user_query` routes `weblimit` through `handle_weblimit_command()` for alternate parsing — both target the same global.

---

## `/soulsig`

```text
/soulsig
/soulsig Prefer concise bullet answers for design reviews.
/soulsig wipe
/soulsig heal
```

Persisted through `save_known_user_names()` rewriting `kun.py`.

---

## `/theme`

Invokes `select_theme()` from `terminal_colors.py` during a session. Voice shortcut **`theme`** is recognized in `handle_voice_command`.

---

## URL and vision (no slash)

If a conversational line contains:

- **Image URL** ending in `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.tiff`, `.webp` — BLIP caption replaces the URL token inline.
- **Other HTTP(S) URLs** — `describe_webpage` injects truncated text honoring `/weblimit`.

---

## Conversational memory short-circuit

`handle_conversational_query` calls `recall_information` for **substring** matches across the PostgreSQL table before hitting the LLM.

---

## Command routing quirks

1. **Dual paths:** `/recall`, `/forget`, `/memorize`, `/help`, `/status`, `/voice`, `/theme`, `/weblimit`, and `exit`/`quit` are handled in the **main loop** before `handle_user_query`.
2. **Web3 import coupling:** Missing Web3 env vars **exit during import** — see [ARCHITECTURE.md](ARCHITECTURE.md).
3. **`is_current_user`:** Optional; room intros may read `"User"` if unset.

---

For environment tables see [CONFIGURATION.md](CONFIGURATION.md). For boot policy see [BOOT_AND_SECURITY.md](BOOT_AND_SECURITY.md).
