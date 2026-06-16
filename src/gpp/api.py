"""Thin, zero-dependency GitHub REST API client (stdlib only)."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

API_ROOT = "https://api.github.com"
USER_AGENT = "github-glowup"


class GitHubError(Exception):
    """Raised when the GitHub API cannot satisfy a request."""


def _request(path: str, token: str | None) -> Any:
    url = path if path.startswith("http") else f"{API_ROOT}{path}"
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/vnd.github+json",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            raise GitHubError("user not found") from exc
        if exc.code == 403:
            raise GitHubError(
                "rate limit reached — pass a token with --token or set GITHUB_TOKEN"
            ) from exc
        raise GitHubError(f"GitHub returned HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise GitHubError(f"network error: {exc.reason}") from exc


def resolve_token(explicit: str | None) -> str | None:
    """Pick a token from the flag or common environment variables."""
    return explicit or os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")


def fetch_user(username: str, token: str | None) -> dict[str, Any]:
    return _request(f"/users/{username}", token)


def fetch_repos(username: str, token: str | None, max_pages: int = 3) -> list[dict[str, Any]]:
    """Fetch up to ``max_pages`` pages (100 repos each) of public repos."""
    repos: list[dict[str, Any]] = []
    for page in range(1, max_pages + 1):
        batch = _request(
            f"/users/{username}/repos?per_page=100&page={page}&sort=updated", token
        )
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
    return repos
