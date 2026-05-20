# Agent contribution workflow

You are welcome here.

OPSIE is a terminal-native self-centered intelligence prototype: one long-lived session, local models, memory, commands, and real integrations (Web3, mail, markets, voice, and more). Agents that help improve this repository extend what every future operator and contributor can run. Your operator reviews plans and merges; **you** prepare analysis, implementation, and verification with care.

This guide is written **for you**, the contributing agent. Read it before you edit the tree. Humans should also skim it when pairing with an agent on a fork-based PR.

For repository standards, see [CONTRIBUTING.md](../CONTRIBUTING.md). For vulnerabilities, see [SECURITY.md](../SECURITY.md).

---

## How you should operate

1. **Issue-first** — Read the linked GitHub issue and acceptance criteria. Pick the right [issue template](../.github/ISSUE_TEMPLATE/). If there is no issue, ask your operator to open one or confirm scope with maintainers.
2. **Plan before large diffs** — For non-trivial work, produce a short written plan and wait for operator approval.
3. **One concern per PR** — Docs, feature, refactor, or fix; do not mix unrelated modules.
4. **OPSIE security** — Never commit `.env`, production `kun.py`, enrollment images, or private keys. Use coordinated disclosure for undisclosed vulns (email in SECURITY.md), not public issue bodies with exploit detail.
5. **No emojis** — Not in code, docs, commits, or PR titles.
6. **Operator owns git** — You propose branch names, commits, and PR text. Do not merge or force-push `ARPAHLS/OPSIE` `main` unless instructed.

---

## Workflow (seven stages)

| Stage | You do | Done when |
|-------|--------|-----------|
| **1. Prepare** | Clone operator fork; add `upstream` → `ARPAHLS/OPSIE`; branch `feat/issue-<n>-short-desc`; venv + `pip install -r requirements.txt`; local `.env` and `kun.py` from examples only | Branch tracks issue; no secrets in git |
| **2. Analyze** | Read issue, CONTRIBUTING, area docs (table below); list affected files, risks, out-of-scope | Written plan only; no implementation yet |
| **3. Approve** | Send plan to operator; incorporate feedback | Explicit "proceed" from operator |
| **4. Implement** | Minimal diff per approved plan; match existing style (`pastel_*`, `handle_*`, globals) | Code/docs match plan |
| **5. Verify** | Run checks for your change type (checklist below); honest test notes | Criteria mapped to diff or tests |
| **6. Commit** | Imperative message; `Fixes #N` when closing; scoped `git add` | No secrets in diff |
| **7. PR** | Fork → `ARPAHLS/OPSIE` `main`; fill [PR template](../.github/pull_request_template.md); fix CI if it fails | Reviewable PR linked to issue |

Reference snapshot branch `0_3_80_XP` is a frozen backup; develop on `main`.

---

## What to read by area

Use the issue **primary area** dropdown and add the matching `area:*` label at triage ([LABELS.md](../.github/LABELS.md)).

| Area | Start here |
|------|------------|
| Core | `OPSIIE_0_3_80_XP.py`, [ARCHITECTURE.md](ARCHITECTURE.md), [COMMANDS.md](COMMANDS.md) |
| Boot / auth | [BOOT_AND_SECURITY.md](BOOT_AND_SECURITY.md), `kun.example.py` (patterns only) |
| Memory | [MEMORY_AND_RAG.md](MEMORY_AND_RAG.md) |
| Terminal / help | `terminal_colors.py`, `help.py` |
| Persona | [PROMPTS_AND_SOULSIG.md](PROMPTS_AND_SOULSIG.md), `utils.py` |
| Config | [CONFIGURATION.md](CONFIGURATION.md), `.env.example` |
| Agentic | `agentic_network.py` |
| Markets | `markets.py`, `markets_mappings.py` |
| Web3 | `web3_handler.py`, [SECURITY.md](../SECURITY.md) Web3 section |
| Mail | `mail.py` |
| DNA | `dna.py` |
| GenAI | `video.py`, `/imagine` and `/music` in [COMMANDS.md](COMMANDS.md) |
| Rooms | `room.py`, [arpahls/rooms](https://github.com/arpahls/rooms) for standalone context |
| Voice | [VOICE.md](VOICE.md) |
| Infrastructure | `.github/`, workflows, [CONTRIBUTING.md](../CONTRIBUTING.md) |

Full module map: [MODULES.md](MODULES.md). Failures: [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

---

## OPSIE cautions (read once)

- **Master gating** — Commands such as `/ask`, `/markets`, `/dna`, `/0x` require `arpa_id` starting with `R`. Do not weaken checks in the main loop or `handle_user_query()`.
- **Boot and hardware** — Full smoke tests may need camera, mic, PostgreSQL, and Ollama on the operator machine.
- **Lazy Web3** — `web3_handler` may be deferred at startup; understand before "fixing" imports.
- **Globals** — Much state lives in the main module; cross-cutting changes have wide blast radius.
- **Paths** — Windows-first; `/read` and voice assets may use operator-specific paths.
- **Related ARPA repos** — [Skillware](https://github.com/arpahls/skillware), [Hermes3](https://github.com/arpahls/Hermes3), [Gatekeeper](https://github.com/arpahls/gatekeeper), [Rooms](https://github.com/arpahls/rooms): integrate via issues, do not silently duplicate whole stacks in one PR.

---

## Verify before PR

**All changes**

- [ ] Issue acceptance criteria met
- [ ] No secrets, real `kun.py`, or enrollment images in diff
- [ ] No emojis in touched prose
- [ ] [PR template](../.github/pull_request_template.md) filled; `Fixes #N` when applicable

**Code**

- [ ] Smoke: imports or boot-to-loop on operator dev machine (note if not run and why)
- [ ] Docs updated if commands or env vars changed (`README.md`, relevant `docs/`)

**Bug fix**

- [ ] Repro understood; fix minimal; regression test if feasible

**Security**

- [ ] Public issue only for non-sensitive tracking; sensitive detail to security@arpacorp.net

When CI is enabled on the repo, run the same lint/test commands maintainers expect and report results in the PR.

---

## Quick self-check

- Did I read the full issue and the right docs for this area?
- Did I get approval before a large implementation?
- Does every file in the diff serve the issue?
- Did I state testing honestly (pass / fail / not run)?

---

## Related documents

- [CONTRIBUTING.md](../CONTRIBUTING.md)
- [SECURITY.md](../SECURITY.md)
- [LABELS.md](../.github/LABELS.md)
- [Pull request template](../.github/pull_request_template.md)
- [Docs index](README.md)
- [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md)

---

Ship small, verifiable work: clear analysis, tight scope, and respect for operator secrets and access control. That is how OPSIE improves, and how you build reliable skill on a real agent stack.
