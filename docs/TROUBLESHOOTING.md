# Troubleshooting

## Process exits immediately on import

**Symptom:** Red message from `web3_handler.py` about missing environment variables.

**Cause:** `AGENT_PRIVATE_KEY` or an RPC URL missing; the module calls `exit()` during import.

**Mitigation:** Populate `.env` with valid placeholders for development machines, or maintain a private fork that lazy-imports Web3 after a feature flag.

## Hugging Face `/imagine` errors

**Symptom:** `Missing HUGGINGFACE_API_KEY or HF_TOKEN in your .env file`.

**Cause:** 0.3.80 XP reads the bearer token only from the environment (no embedded token in source).

**Mitigation:** Add `HUGGINGFACE_API_KEY=hf_...` or `HF_TOKEN=hf_...` to `.env`.

## `load_dotenv` ordering

`load_dotenv()` is placed immediately before `from web3_handler import Web3Handler` so `.env` is visible during Web3 import validation.

## Camera or microphone failures during boot

**Mitigation:** Close other apps using the devices; check Windows privacy toggles; plug an external USB camera; for private development only, you may stub `facial_recognition_auth` in a fork.

## ElevenLabs 401 or 429

Verify `ELEVENLABS_API_KEY` and voice UUIDs.

## Ollama errors

- **`model 'llama3' not found`:** `ollama pull llama3`.
- **Embedding failures:** `ollama pull nomic-embed-text`.

## Chroma desync

If PostgreSQL has rows but Chroma was wiped, `ensure_vector_db_exists` repopulates when the collection exists with count zero.

## `/read` says no path

Regex expects a **double-quoted** path: `/read "D:\file.pdf"`.

## No face in enrollment image

Add a clear portrait at `assets/enrollment.jpg` (see `assets/README.txt`). Plain color JPEGs usually fail encoding.

## Music or video CUDA OOM

Reduce generation parameters in code or fall back to CPU.

## Hugging Face 503 on `/imagine`

Model cold start on Inference API — wait and retry.

## `is_current_user` unset

Room introductions may show `"User"`. Set `is_current_user` on the authenticated profile after login if you extend the auth layer.

## Unicode paths on Windows

Prefer ASCII-only directories for enrollment photos and media caches.
