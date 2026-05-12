# Contributing

Thank you for helping improve OPSIIE documentation and code quality.

## Principles

- **Scope control:** Open pull requests that address one concern (documentation versus feature versus refactor) so review stays tractable.
- **Security first:** Never commit live API keys, Web3 private keys, database passwords, biometric enrollment photos, or production `kun.py` profiles. Use `.env` and local-only assets.
- **Reproducibility:** When behavior changes, update the matching section in `README.md` or under `docs/`.

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

## Pull request checklist

- [ ] No secrets or personal data in the diff
- [ ] Documentation updated when commands or environment variables change
- [ ] Smoke run: import chain or boot reaches the interactive loop on a development machine
- [ ] For security-relevant edits, describe risk surface (Web3, network, biometric, mail)

## Communication

- Technical contact: [input@arpacorp.net](mailto:input@arpacorp.net)
- For security-sensitive reports, see [SECURITY.md](SECURITY.md).

## Licensing

Contributions are licensed under the same terms as [LICENSE](LICENSE): permissive use with **OPSIE** and **ARPA Hellenic Logical Systems** attribution. By submitting a pull request, you agree your contributed material is available under those terms unless you state otherwise clearly in the pull request description.
