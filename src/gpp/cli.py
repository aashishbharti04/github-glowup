"""Command-line entry point for github-glowup."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict

from . import __version__
from .api import GitHubError, fetch_repos, fetch_user, resolve_token
from .render import render
from .score import compute


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="glowup",
        description="Score and supercharge any GitHub profile from your terminal.",
    )
    parser.add_argument("username", help="GitHub username to analyze")
    parser.add_argument(
        "--token", help="GitHub token (else uses $GITHUB_TOKEN / $GH_TOKEN)"
    )
    parser.add_argument(
        "--json", action="store_true", help="emit raw JSON instead of a report"
    )
    color = parser.add_mutually_exclusive_group()
    color.add_argument("--color", dest="color", action="store_true", help="force color")
    color.add_argument("--no-color", dest="color", action="store_false", help="disable color")
    parser.set_defaults(color=None)
    parser.add_argument("--version", action="version", version=f"glowup {__version__}")
    return parser


def main(argv: list[str] | None = None) -> int:
    # Prefer UTF-8 output where the terminal allows it (Windows consoles default
    # to legacy code pages); render.py still falls back to ASCII if this fails.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError, OSError):
        pass

    args = build_parser().parse_args(argv)
    token = resolve_token(args.token)

    try:
        user = fetch_user(args.username, token)
        repos = fetch_repos(args.username, token)
    except GitHubError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    report = compute(user, repos)

    if args.json:
        print(json.dumps(asdict(report), indent=2, default=str))
    else:
        print(render(report, color=args.color))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
