# Security policy

## Supported versions

Security updates, when available, apply to the latest tagged revision in this repository lineage maintained by ARPA Hellenic Logical Systems.

## Reporting a vulnerability

**Please do not file public issues for undisclosed vulnerabilities.**

Email: [security@arpacorp.net](mailto:security@arpacorp.net)

Include:

- A concise description of the issue and its impact
- Steps to reproduce (proof-of-concept if possible)
- Affected files or subsystems
- Whether you believe the issue is already exploitable in default configuration

We aim to acknowledge receipt within several business days. Coordinated disclosure is preferred.

## Known high-risk areas in this codebase

Review these carefully before any internet-facing deployment:

1. **Environment files:** `.env` must remain untracked. If credentials were ever committed, **rotate** them everywhere they were reused.
2. **`kun.py`:** Contains database parameters, mail, wallet metadata, and soul signatures. Treat as **confidential** for production profiles.
3. **`AGENT_PRIVATE_KEY`:** Grants on-chain asset control. Compromise is irreversible without key rotation and fund migration.
4. **`web3_handler.py`:** Missing required Web3 variables blocks Web3 commands at runtime, but non-Web3 startup can continue.
5. **Biometric authentication:** Still-image face matching is not liveness-proof. DeepFace emotion classes are coarse heuristics, not clinical instrumentation. For a **standalone gateway** focused on facial recognition and emotion policy (and room to add liveness and service boundaries), evaluate **[Gatekeeper](https://github.com/arpahls/gatekeeper)** alongside this monolith’s in-process boot gate.
6. **`/read`:** Resolves operator-supplied paths on the host. Only open paths you trust.
7. **Hugging Face `/imagine`:** Requires `HUGGINGFACE_API_KEY` or `HF_TOKEN` in `.env`. Do not embed inference tokens in source.

## Safe defaults for operators

- Run on dedicated hardware with disk encryption.
- Use least-privilege PostgreSQL roles per user profile.
- Maintain offline backups separate from live keys.
- Audit outbound network destinations (Ollama, ElevenLabs, OpenAI, Google, Yahoo Finance, NCBI, Hugging Face, RPC providers).

## Credential rotation (incident checklist)

If a repository copy was public with real `.env` or `kun.py` secrets:

- Rotate **all** API keys, SMTP passwords, Web3 keys, and database passwords that appeared in the leak.
- Invalidate Hugging Face, OpenAI, Google, ElevenLabs, and explorer API tokens.
- Regenerate wallet material if a private key was exposed.
