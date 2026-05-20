# Contributing

Thank you for helping improve OPSIE documentation and code quality.

## Principles

- **Scope control:** Open pull requests that address one concern (documentation versus feature versus refactor) so review stays tractable.
- **Security first:** Never commit live API keys, Web3 private keys, database passwords, biometric enrollment photos, or production `kun.py` profiles. Use `.env` and local-only assets.
- **Reproducibility:** When behavior changes, update the matching section in `README.md` or under `docs/`.

## Issues and labels

We use **Option A** triage: reporters pick a template and one **primary area**; maintainers add matching `area:*` labels and move `needs-triage` to `confirmed`.

| I want to… | Template |
|------------|----------|
| Report broken behavior | **Bug report** |
| Propose new behavior | **Feature request** |
| Fix README or `docs/` | **Documentation** |
| Discuss setup or design | **Question** |
| Security (public tracking only) | **Security** — see [SECURITY.md](SECURITY.md) for undisclosed reports |
| Refactor, CI, deps, tests | **Maintenance** |

- Full label rules: [.github/LABELS.md](.github/LABELS.md)
- Blank issues are disabled; use a template or the security contact link in [config.yml](.github/ISSUE_TEMPLATE/config.yml)
- After merge to `main`, labels sync from [.github/labels.json](.github/labels.json) via the **Sync GitHub labels** workflow (or create labels manually from that file on first setup)

**Do not** paste secrets in issues. **Do not** set `priority:high` or `priority:low` on your own issue unless a maintainer asks you to.

## Development setup

```powershell
cd d:\Agents\OPSIIE_0_3_80_XP
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Run the main entry only on machines you control and with credentials you own.

## Style

- Prefer **PEP 8** for Python.
- Match existing naming (`pastel_*`, `handle_*`, global orchestration style) unless a dedicated refactor pull request is agreed.
- Keep user-visible strings professional and consistent with ARPA branding.

## Tests

`pytest` appears in `requirements.txt`. Automated coverage is minimal today. If you add tests, place them under `tests/` and document how to invoke them in the pull request.

## Pull requests

New PRs use a short [.github/pull_request_template.md](.github/pull_request_template.md) (related issues, summary, type, area, testing, security, checklist). Agents and humans should keep it brief; use `Fixes #N` when the PR closes an issue.

## Pull request checklist

- [ ] No secrets or personal data in the diff
- [ ] Documentation updated when commands or environment variables change
- [ ] Primary `area:*` noted in the PR description when the change is subsystem-specific
- [ ] Smoke run: import chain or boot reaches the interactive loop on a development machine
- [ ] For security-relevant edits, describe risk surface (Web3, network, biometric, mail)

## Communication

- Technical contact: [input@arpacorp.net](mailto:input@arpacorp.net)
- For security-sensitive reports, see [SECURITY.md](SECURITY.md).

## Licensing

Contributions are licensed under the same terms as [LICENSE](LICENSE): permissive use with **OPSIE** and **ARPA Hellenic Logical Systems** attribution. By submitting a pull request, you agree your contributed material is available under those terms unless you state otherwise clearly in the pull request description.
