"""Emit a shields.io endpoint-badge JSON for a user's Profile Power Score.

Usage:  python scripts/make_badge.py <username>  > .github/badges/score.json
"""

from __future__ import annotations

import json
import sys

from gpp.api import fetch_repos, fetch_user, resolve_token
from gpp.score import compute


def color_for(score: float) -> str:
    bands = [
        (90, "brightgreen"),
        (80, "green"),
        (70, "yellowgreen"),
        (55, "yellow"),
        (40, "orange"),
        (0, "red"),
    ]
    for threshold, color in bands:
        if score >= threshold:
            return color
    return "red"


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print("usage: make_badge.py <username>", file=sys.stderr)
        return 2
    username = argv[0]
    token = resolve_token(None)

    user = fetch_user(username, token)
    repos = fetch_repos(username, token)
    report = compute(user, repos)

    badge = {
        "schemaVersion": 1,
        "label": "profile power",
        "message": f"{report.score:.0f}/100",
        "color": color_for(report.score),
    }
    print(json.dumps(badge))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
