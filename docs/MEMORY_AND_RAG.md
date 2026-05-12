# Memory, embeddings, and RAG behavior

## PostgreSQL

### Connection

After authentication, `db_params` on the active `kun.py` profile is used for `psycopg.connect(**db_params)`.

### Table shape (expected)

The code issues selects and inserts against **`conversations`** with columns including **`id`**, **`timestamp`**, **`prompt`**, **`response`**.

### Normalization

`normalize_text` applies Unicode NFKC before insert.

## ChromaDB

- Client: `chromadb.Client()` (ephemeral in-process in the reference build).
- **Global collection:** `conversations`.
- **IDs:** stringified PostgreSQL `id`.
- **Document payload:** concatenation `prompt: {text} response: {text}`.

### Hydration

If the collection is empty but SQL has rows, `create_vector_db` embeds historical rows using Ollama **`nomic-embed-text`**.

## Recall pipeline (`/recall`)

1. **`create_queries(prompt)`** — Asks `llama3` for a Python-parseable list of search strings; `ast.literal_eval` parses with fallback.
2. **`retrieve_embeddings`** — Embeds each query, queries Chroma, applies **`classify_embedding`** gating.
3. Accepted snippets become a `Retrieved memory:` system message; **`stream_response`** runs on the recall text.

## `/forget`

Deletes the **latest** SQL row (max `id`) and matching Chroma id; trims **two** tail messages from RAM `convo`.

## `/memorize`

Stores the text as a user message with assistant reply `Memory specimen successfully implanted.` so the pair embeds like normal dialogue.

## Substring memory (`recall_information`)

Used on the conversational path: scans the **entire** table for case-insensitive substring matches in prompt or response. Cost grows with table size.

## Room memory

`Room` maintains a **separate** Chroma collection (`room_<slug>`). It is orthogonal to the global mnemonic unless you merge exports manually.

Session exports and a longer-lived room product surface may also align with **[arpahls/rooms](https://github.com/arpahls/rooms)** if you outgrow the bundled `room.py` workflow.

## Backup guidance

- Dump PostgreSQL regularly (`pg_dump`).
- Treat SQL as **source of truth**; re-embed into Chroma if the in-process collection is lost.
