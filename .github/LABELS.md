# OPSIE label guide

This document defines the label taxonomy for [ARPAHLS/OPSIE](https://github.com/ARPAHLS/OPSIE). Labels are declared in [labels.json](labels.json) and synced to GitHub by the [Sync GitHub labels](../workflows/sync-labels.yml) workflow (or manually on first setup).

Implements **Option A**: reporters file issues quickly; maintainers apply **area** and **work-type** labels during triage.

Closes the label-strategy portion of [#21](https://github.com/ARPAHLS/OPSIE/issues/21); contributes to [#20](https://github.com/ARPAHLS/OPSIE/issues/20).

---

## How labeling works (Option A)

### At issue creation (reporter, ~1–2 minutes)

1. Choose one of six [issue templates](ISSUE_TEMPLATE/).
2. Fill required fields, including **one primary area** (dropdown).
3. Optionally pick **one** secondary area (or `None`).
4. GitHub applies **kind** labels from the template (e.g. `bug`, `enhancement`) plus **`needs-triage`**.

The dropdown value is stored in the issue body. It does **not** auto-apply `area:*` labels (GitHub limitation).

### During triage (maintainer, first response)

1. Read **Primary area** (and **Also affects** if set) from the issue body.
2. Add the matching **`area:*`** label (one primary; at most one secondary).
3. Remove **`needs-triage`** and add **`confirmed`** when scope is accepted.
4. Add **work-type** labels if not already clear: `refactor`, `infrastructure`, `dependencies`, `testing`.
5. Add **`priority:high`** or **`priority:low`** only when needed (maintainers; not reporters).
6. Use **`blocked`**, **`help wanted`**, **`good first issue`**, **`duplicate`**, **`invalid`**, **`wontfix`** as usual.

### Rules (avoid noise)

| Rule | Detail |
|------|--------|
| One kind | Prefer a single kind label: `bug`, `enhancement`, `documentation`, `question`, `security`, or maintenance kinds added at triage |
| One primary area | Exactly one `area:*` for ownership |
| One secondary area max | Only when the fix clearly spans two subsystems |
| No conflicting workflow | Do not keep `needs-triage` and `confirmed` together |
| No duplicate vocabulary | Use `area:voice`, not a separate `voice` label |
| Priority | `priority:high` / `priority:low` are maintainer-only |
| Secrets | Never ask reporters to label `security` for paste-in keys; use coordinated disclosure |

---

## Label groups

### Kind (what type of work)

| Label | When to use |
|-------|-------------|
| `bug` | Incorrect or broken behavior |
| `enhancement` | New feature or meaningful improvement |
| `documentation` | Docs-only change |
| `question` | Information or discussion |
| `security` | Security template; policy or hardening |
| `refactor` | Same behavior, structural change (often from Maintenance triage) |
| `infrastructure` | `.github`, CI, repo layout |
| `dependencies` | `requirements.txt`, Ollama/Chroma/Postgres pins |
| `testing` | Tests and smoke harness |

GitHub defaults retained: `duplicate`, `invalid`, `wontfix`, `good first issue`, `help wanted`.

### Area (where in OPSIE)

| Label | Module / scope |
|-------|----------------|
| `area:core` | `OPSIIE_0_3_80_XP.py` — router, boot, streaming, globals |
| `area:boot-auth` | Gate, `kun.py`, `arpa_id`, `/status` |
| `area:memory` | PostgreSQL, Chroma, `/recall`, `/forget`, `/memorize` |
| `area:terminal` | `terminal_colors.py`, `help.py`, themes, slash UX |
| `area:persona` | System prompt, Soul Signature, `utils.py` persona text |
| `area:config` | `.env`, `kun.example.py`, configuration docs |
| `area:agentic` | `agentic_network.py`, `/ask`, live agents |
| `area:markets` | `markets.py`, `markets_mappings.py`, `/markets` |
| `area:web3` | `web3_handler.py`, `/0x`, `receive` |
| `area:mail` | `mail.py`, `/mail` |
| `area:dna` | `dna.py`, `/dna` |
| `area:genai` | `/imagine`, `/music`, `video.py`, `/video` |
| `area:rooms` | `room.py`, `/room`, `outputs/rooms/` |
| `area:voice` | `/voice*`, TTS/STT, system sounds |

### Workflow (issue state)

| Label | When to use |
|-------|-------------|
| `needs-triage` | Default on new templated issues |
| `confirmed` | Repro or scope accepted |
| `blocked` | Waiting on dependency or decision |

### Priority (maintainers only)

| Label | When to use |
|-------|-------------|
| `priority:high` | Target next patch |
| `priority:low` | Backlog |

---

## Template to label mapping

| Template | Labels applied on create | Maintainer adds |
|----------|---------------------------|-----------------|
| Bug report | `bug`, `needs-triage` | `area:*`, `confirmed`, optional `priority:*` |
| Feature request | `enhancement`, `needs-triage` | `area:*`, `confirmed` |
| Documentation | `documentation`, `needs-triage` | `area:*` if subsystem-specific |
| Security | `security`, `needs-triage` | `area:*`, `priority:high` if urgent |
| Question | `question`, `needs-triage` | `area:*`; convert to `bug`/`enhancement` if needed |
| Maintenance | `needs-triage` only | `refactor` / `infrastructure` / `dependencies` / `testing`, `area:*` |

### Dropdown value to area label

Copy the label name before the em dash in the primary area dropdown:

| Dropdown prefix | GitHub label |
|-----------------|--------------|
| `area:core` | `area:core` |
| `area:boot-auth` | `area:boot-auth` |
| `area:memory` | `area:memory` |
| `area:terminal` | `area:terminal` |
| `area:persona` | `area:persona` |
| `area:config` | `area:config` |
| `area:agentic` | `area:agentic` |
| `area:markets` | `area:markets` |
| `area:web3` | `area:web3` |
| `area:mail` | `area:mail` |
| `area:dna` | `area:dna` |
| `area:genai` | `area:genai` |
| `area:rooms` | `area:rooms` |
| `area:voice` | `area:voice` |
| `Other / unsure` | Ask reporter; leave only `needs-triage` until clarified |

---

## Pastel color reference

Colors are set in [labels.json](labels.json). Adjust in the GitHub UI if a label already existed with a different color.

| Group | Example labels | Hex (no `#`) |
|-------|----------------|--------------|
| Kind | `bug` | `e8b4b4` |
| Kind | `enhancement` | `b8d4e8` (former documentation blue) |
| Kind | `documentation` | `f0e8c8` (same as `dependencies`, near triage) |
| Kind | `good first issue` | `c8f030` (lime, high contrast) |
| Kind | `help wanted` | `f5e020` (bright yellow) |
| Area | all `area:*` | `d0f5f0` (shared; matches former `area:dna`) |
| Workflow | `needs-triage` | `f0f0d8` |
| Workflow | `confirmed` | `d8f0d8` |
| Priority | `priority:high` | `f0b8b8` |

---

## Syncing labels to GitHub

**Automatic (after merge to `main`):**

1. Merge a PR that includes `.github/labels.json` (or workflow changes).
2. Workflow **Sync GitHub labels** runs on push, or run it manually: **Actions** → **Sync GitHub labels** → **Run workflow** → branch **`main`**.

The workflow uses the GitHub API to **create and update** labels (including **color** changes). Re-run after editing colors in `labels.json`.

**Manual (without Actions):**

1. Open **Issues** → **Labels** → edit each label, or use `gh label edit <name> --color <hex> --description "..."`.

Labels not listed in `labels.json` are kept (nothing is deleted).

---

## Examples

### Voice bug

- **Reporter:** Bug report, primary area `area:voice`, steps, no secrets.
- **On create:** `bug`, `needs-triage`
- **Maintainer:** add `area:voice`, `confirmed`, remove `needs-triage`

### Cross-cutting boot + voice

- **Reporter:** Bug, primary `area:core`, secondary `area:voice`
- **Maintainer:** `area:core`, `area:voice`, `confirmed`

### CI workflow only

- **Reporter:** Maintenance, work type Infrastructure, primary Infrastructure / .github only
- **Maintainer:** `infrastructure`, `area:config` or no area if purely `.github`, `confirmed`

---

## Related files

| File | Role |
|------|------|
| [ISSUE_TEMPLATE/](ISSUE_TEMPLATE/) | Six issue forms + `config.yml` |
| [labels.json](labels.json) | Label definitions for sync |
| [pull_request_template.md](pull_request_template.md) | PR checklist |
| [../CONTRIBUTING.md](../CONTRIBUTING.md) | Contributor overview |

Future: GitHub Action to parse `primary_area` from issue body and apply `area:*` automatically (optional; not in scope for #21).
