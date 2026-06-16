# Contributing to GitHub Glow-Up

Thanks for helping make profiles glow! ✨ Contributions of all sizes are welcome.

## Quick start

```bash
git clone https://github.com/aashishbharti04/github-glowup
cd github-glowup
pip install -e ".[dev]"
pytest -q
```

## Ground rules

- **Keep it zero-dependency.** Runtime code uses only the Python standard library.
- **Add a test** for any behavior change — the scoring logic in `src/gpp/score.py`
  is pure and easy to cover.
- **Run the suite** (`pytest -q`) before opening a PR; CI runs it on 3.9–3.13.
- Keep functions small and the style consistent with the surrounding code.

## Good first issues

- New scoring dimensions (e.g. recent commit activity, README quality).
- More achievement-specific tips.
- Additional output formats (Markdown badge, SVG card).

## Reporting bugs

Open an issue with the command you ran, the username, and the full output. Redact
any tokens.

By contributing you agree your work is licensed under the project's [MIT License](LICENSE).
