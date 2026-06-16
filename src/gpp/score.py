"""Profile Power Score: pure functions, fully unit-testable, no network."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class Metric:
    key: str
    label: str
    points: float
    max_points: float
    detail: str


@dataclass
class Report:
    username: str
    name: str
    score: float
    grade: str
    metrics: list[Metric] = field(default_factory=list)
    tips: list[str] = field(default_factory=list)
    stats: dict[str, Any] = field(default_factory=dict)


def _log_scale(value: float, full_at: float, cap: float) -> float:
    """Diminishing-returns curve: 0 -> 0, ``full_at`` -> ~``cap``."""
    if value <= 0:
        return 0.0
    ratio = math.log10(value + 1) / math.log10(full_at + 1)
    return min(cap, cap * ratio)


def _grade(score: float) -> str:
    bands = [
        (90, "S — legendary"),
        (80, "A — powerful"),
        (70, "B — strong"),
        (55, "C — solid"),
        (40, "D — getting there"),
        (0, "E — just starting"),
    ]
    for threshold, label in bands:
        if score >= threshold:
            return label
    return "E — just starting"


def _account_age_years(created_at: str, now: datetime) -> float:
    created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    return max(0.0, (now - created).days / 365.25)


def compute(
    user: dict[str, Any],
    repos: list[dict[str, Any]],
    now: datetime | None = None,
) -> Report:
    """Compute the Profile Power Score from a user payload and repo list."""
    now = now or datetime.now(timezone.utc)

    total_stars = sum(r.get("stargazers_count", 0) for r in repos)
    total_forks = sum(r.get("forks_count", 0) for r in repos)
    own_repos = [r for r in repos if not r.get("fork")]
    languages = sorted({r["language"] for r in repos if r.get("language")})
    followers = user.get("followers", 0)
    public_repos = user.get("public_repos", 0)
    age_years = _account_age_years(user["created_at"], now) if user.get("created_at") else 0.0
    has_profile_readme = any(
        r.get("name", "").lower() == user.get("login", "").lower() for r in repos
    )

    metrics = [
        Metric("reach", "Reach (followers)", _log_scale(followers, 1000, 22), 22,
               f"{followers} followers"),
        Metric("stars", "Stars earned", _log_scale(total_stars, 2000, 25), 25,
               f"{total_stars} stars across repos"),
        Metric("output", "Output (public repos)", _log_scale(public_repos, 60, 15), 15,
               f"{public_repos} public repos"),
        Metric("diversity", "Language diversity", min(12, len(languages) * 2.0), 12,
               f"{len(languages)} languages: {', '.join(languages[:6]) or 'none'}"),
        Metric("forks", "Forks of your work", _log_scale(total_forks, 500, 8), 8,
               f"{total_forks} forks"),
        Metric("polish", "Profile polish", _polish_points(user, has_profile_readme), 10,
               _polish_detail(user, has_profile_readme)),
        Metric("tenure", "Tenure", min(8, age_years * 1.6), 8,
               f"{age_years:.1f} years on GitHub"),
    ]

    score = round(sum(m.points for m in metrics), 1)
    report = Report(
        username=user.get("login", "?"),
        name=user.get("name") or user.get("login", "?"),
        score=score,
        grade=_grade(score),
        metrics=metrics,
        stats={
            "followers": followers,
            "following": user.get("following", 0),
            "public_repos": public_repos,
            "total_stars": total_stars,
            "total_forks": total_forks,
            "languages": languages,
            "own_repos": len(own_repos),
            "has_profile_readme": has_profile_readme,
            "age_years": round(age_years, 1),
        },
    )
    report.tips = build_tips(report)
    return report


def _polish_points(user: dict[str, Any], has_profile_readme: bool) -> float:
    points = 0.0
    if user.get("bio"):
        points += 2
    if user.get("blog"):
        points += 2
    if user.get("name"):
        points += 1
    if user.get("location"):
        points += 1
    if user.get("company") or user.get("twitter_username"):
        points += 1
    if has_profile_readme:
        points += 3
    return min(10.0, points)


def _polish_detail(user: dict[str, Any], has_profile_readme: bool) -> str:
    have = []
    if user.get("bio"):
        have.append("bio")
    if user.get("blog"):
        have.append("website")
    if has_profile_readme:
        have.append("profile README")
    return "has: " + (", ".join(have) if have else "nothing yet")


def build_tips(report: Report) -> list[str]:
    """Actionable, achievement-aware suggestions, weakest areas first."""
    tips: list[str] = []
    s = report.stats
    weak = sorted(report.metrics, key=lambda m: m.points / m.max_points)

    suggestions = {
        "stars": "Ship one genuinely useful repo with a great README — earns the "
                 "Starstruck achievement and the most score per unit effort.",
        "reach": "Engage: open PRs to projects you use, write issues, and follow people "
                 "back. Followers compound.",
        "output": "Publish small focused projects regularly instead of one big private one.",
        "diversity": "Add a repo in a language you don't have yet to widen your stack.",
        "polish": "Fill in bio, website, and add a username/username profile README repo.",
        "forks": "Make your best repo reusable (clear docs, examples) so others fork it.",
        "tenure": "Just keep shipping — tenure grows on its own.",
    }
    for m in weak[:3]:
        if m.points < m.max_points * 0.85:
            tips.append(suggestions[m.key])

    if not s["has_profile_readme"]:
        tips.append(
            "Create a repo named exactly your username to unlock the special profile "
            "README that shows at the top of your page."
        )
    tips.append(
        "Achievement hunt: merge a PR (Pull Shark), co-author a commit (Pair "
        "Extraordinaire), answer a discussion (Galaxy Brain), and react quickly to "
        "issues (Quickdraw)."
    )
    return tips
