# Configuration

## `.env` variables (aggregate)

Loaded via `python-dotenv`. **`load_dotenv()`** is invoked in `OPSIIE_0_3_80_XP.py` before runtime service checks. Template: **`.env.example`**.

| Variable | Consumed by | Purpose |
|----------|-------------|---------|
| `OPENAI_API_KEY` | `agentic_network`, boot | Nyx assistant calls |
| `ORG_ID` | `agentic_network`, boot | OpenAI organization |
| `NYX_ASSISTANT_ID` | `agentic_network`, boot | Nyx deployment id |
| `GOOGLE_API_KEY` | `agentic_network` | Gemini (G1) |
| `G1_VOICE_LIVE` | `agentic_network`, `/ask g1 live` | ElevenLabs ConvAI websocket |
| `KRONOS_LIVE` | `agentic_network`, boot | Kronos agent id |
| `ELEVENLABS_API_KEY` | TTS, live agents, boot | Voice synthesis and sessions |
| `VOICE_ID`, `NYX_VOICE_ID`, `G1_VOICE_ID` | Main file | Per persona TTS |
| `HUGGINGFACE_API_KEY` or `HF_TOKEN` | `/imagine` | Hugging Face Inference bearer (**required for default image path**) |
| `AGENT_PRIVATE_KEY` | `web3_handler` | Signing wallet for Web3 commands |
| `BASE_RPC_URL`, `ETHEREUM_RPC_URL`, `POLYGON_RPC_URL` | `web3_handler` | RPC endpoints for Web3 commands |
| `SENDER_EMAIL`, `SENDER_PASSWORD` | `mail.py` | SMTP and IMAP |
| `NCBI_EMAIL` | `dna.py` | Entrez polite usage |

Global `DB_NAME` style variables in `.env.example` are **documentation helpers**; live connections use **`kun.py` `db_params`** for the authenticated user.

## `kun.py` profile schema

Each key is a **directory name** string (used only for persistence and some lookups). **`full_name`** is what authentication sets as `current_user` and must match the key used when indexing `known_user_names[current_user]` during boot for soul signatures.

| Field | Usage |
|-------|--------|
| `full_name` | Formal identity string; after auth equals `current_user` |
| `call_name` | Casual address, voice prompts |
| `arpa_id` | `R###` master versus `A###` standard gating |
| `public0x` | Web3 receive display and routing |
| `db_params` | `psycopg.connect(**db_params)` |
| `picture` | Still image path for `face_recognition` enrollment |
| `mail` | Mail identity and contact resolution |
| `soul_sig` | Lines appended to system prompt at boot |

**`is_current_user`:** Referenced in `room.py` and room introductions in the main file. Stock template does not set it; intros may fall back to `"User"` until you set the flag on the active profile in memory if you extend auth.

## Output directories (0.3.80 XP defaults)

| Feature | Path under repository |
|---------|------------------------|
| Images | `outputs/images/` |
| Music | `outputs/music/` |
| Video | `outputs/videos/` |
| Room CSV | `outputs/rooms/` |

Boot and help audio use **`system_sounds/`** next to the main script (`opsiieboot.mp3`, `gb.mp3`, `alert.mp3`, `heal.mp3`, `helpbell.mp3`).

## Ollama models

```powershell
ollama pull llama3
ollama pull nomic-embed-text
```

## PostgreSQL DDL starter

```sql
CREATE DATABASE mnemonic_computer;
\c mnemonic_computer;
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    prompt TEXT NOT NULL,
    response TEXT NOT NULL
);
```

Repeat per-user databases as referenced in `kun.py`.
### Ollama Configuration
You can configure the models and host used by OPSIE for chat and embeddings via the `.env` file. If not set, OPSIE falls back to the default models.

* `OLLAMA_MODEL`: The main chat model used for conversational streams and queries. (Default: `llama3`)
* `OLLAMA_EMBED_MODEL`: The embedding model used for Chroma storage and retrieval. (Default: `nomic-embed-text`)
* `OLLAMA_HOST`: The host URL for a remote Ollama instance. (Must remain in the `.env` file so the Ollama SDK automatically picks it up from the environment. Default: `http://localhost:11434`)