<div align="center">

# ⚡ GitHub Glow-Up

### Score and supercharge any GitHub profile — right from your terminal.

<p>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.9%2B-00E5FF?style=for-the-badge&logo=python&logoColor=white&labelColor=0D1117">
  <img alt="Zero deps" src="https://img.shields.io/badge/Dependencies-ZERO-FF2E97?style=for-the-badge&labelColor=0D1117">
  <img alt="License" src="https://img.shields.io/badge/License-MIT-9D4EDD?style=for-the-badge&labelColor=0D1117">
  <img alt="CI" src="https://img.shields.io/github/actions/workflow/status/aashishbharti04/github-glowup/ci.yml?style=for-the-badge&logo=githubactions&logoColor=white&labelColor=0D1117&color=00FFA3">
  <img alt="PyPI" src="https://img.shields.io/pypi/v/github-glowup?style=for-the-badge&logo=pypi&logoColor=white&labelColor=0D1117&color=00E5FF">
</p>

<p>
  <img alt="Profile Power" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/aashishbharti04/github-glowup/main/.github/badges/score.json&style=for-the-badge&labelColor=0D1117">
</p>

<p><i>A pure-stdlib CLI that grades a GitHub profile out of 100 and tells you exactly how to earn more achievements.</i></p>

</div>

---

```text
╔═════════════════════════════════════╗
║  GitHub Glow-Up — @aashishbharti04  ║
╚═════════════════════════════════════╝

  Power Score: 53.4/100
  Grade: D — getting there

  Breakdown
  Reach (followers)      █████░░░░░░░░░░░   6.2/22    6 followers
  Stars earned           ███░░░░░░░░░░░░░   5.3/25    4 stars across repos
  Output (public repos)  ███████████████░  14.3/15    49 public repos
  Language diversity     ████████████████  12.0/12    6 languages
  Forks of your work     ░░░░░░░░░░░░░░░░   0.0/8     0 forks
  Profile polish         ████████████████  10.0/10    has: bio, website, profile README
  Tenure                 ███████████░░░░░   5.6/8     3.5 years on GitHub

  How to level up
  1. Make your best repo reusable so others fork it.
  2. Ship one genuinely useful repo with a great README — earns Starstruck.
  3. Achievement hunt: Pull Shark, Pair Extraordinaire, Galaxy Brain, Quickdraw.
```

## ✨ Why

Your GitHub profile is your developer résumé. **GitHub Glow-Up** turns it into a number you can move — and gives you a concrete to-do list to climb the [GitHub Achievements](https://github.com/Schweinepriester/github-profile-achievements) ladder.

- 🧮 **Power Score (0–100)** across 7 weighted dimensions
- 🎯 **Achievement-aware tips** — Pull Shark, Starstruck, Galaxy Brain, Quickdraw & more
- 🌈 **Dark-neon terminal output** with graceful ASCII + no-color fallbacks
- 📦 **Zero dependencies** — just the Python standard library
- 🤖 **`--json`** mode for dashboards, Actions, and bots

## 🚀 Install

```bash
pip install github-glowup
```

Or run straight from source (no install needed):

```bash
git clone https://github.com/aashishbharti04/github-glowup
cd github-glowup
python -m gpp <username>   # PYTHONPATH=src if not installed
```

## 🕹️ Usage

```bash
glowup torvalds                 # score any public profile
glowup aashishbharti04 --json   # machine-readable output
glowup yourname --no-color      # plain text
```

> [!TIP]
> Unauthenticated GitHub API calls are rate-limited to ~60/hour. Pass a token to
> raise the limit: `glowup yourname --token <PAT>` or set `GITHUB_TOKEN`.

### Options

| Flag | Description |
|------|-------------|
| `--token` | GitHub token (falls back to `$GITHUB_TOKEN` / `$GH_TOKEN`) |
| `--json` | Emit raw JSON instead of the report |
| `--color` / `--no-color` | Force or disable ANSI color |
| `--version` | Print version |

## 🧮 How the score works

| Dimension | Max | What it measures |
|-----------|----:|------------------|
| Stars earned | 25 | Total stars across your repos (log-scaled) |
| Reach | 22 | Followers (log-scaled) |
| Output | 15 | Public repo count |
| Language diversity | 12 | Distinct primary languages |
| Profile polish | 10 | Bio, website, profile README, etc. |
| Forks | 8 | How often your work gets forked |
| Tenure | 8 | Years on GitHub |

All high-volume metrics use a diminishing-returns curve, so the score stays meaningful from beginner to legend.

## 🛠️ Develop

```bash
pip install -e ".[dev]"
pytest -q
```

## 🏅 Live score badge

This repo ships a workflow ([`score-badge.yml`](.github/workflows/score-badge.yml))
that recomputes the owner's Power Score weekly and commits
[`.github/badges/score.json`](.github/badges/score.json). Drop this anywhere
(README, profile) to show a live badge — swap in your username:

```md
![Profile Power](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/aashishbharti04/github-glowup/main/.github/badges/score.json)
```

## 📦 Publishing (maintainers)

Releases publish to PyPI automatically via
[`publish.yml`](.github/workflows/publish.yml) using **Trusted Publishing** — no
API tokens stored anywhere.

**One-time PyPI setup:**

1. Sign in at [pypi.org](https://pypi.org) → *Your projects* → *Publishing*.
2. Add a **pending publisher** with:
   - Project name: `github-glowup`
   - Owner: `aashishbharti04`
   - Repository: `github-glowup`
   - Workflow: `publish.yml`
   - Environment: `pypi`
3. On GitHub, create a Release (tag `v0.1.0`). The workflow builds and uploads.

After that, anyone can `pip install github-glowup`.

## 🤝 Contributing

PRs welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). Good first issues are labeled
[`good first issue`](https://github.com/aashishbharti04/github-glowup/labels/good%20first%20issue).

## 📄 License

[MIT](LICENSE) © Aashish Bharti

<div align="center">
<sub>⭐ If this helped your profile glow up, consider starring the repo — it directly earns you the <b>Starstruck</b> achievement once it spreads.</sub>
</div>
