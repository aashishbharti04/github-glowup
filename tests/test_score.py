"""Unit tests for the pure scoring logic (no network)."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from gpp.score import build_tips, compute


NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)


def make_user(**over):
    base = {
        "login": "octocat",
        "name": "The Octocat",
        "followers": 0,
        "following": 0,
        "public_repos": 0,
        "created_at": "2020-01-01T00:00:00Z",
        "bio": None,
        "blog": None,
        "location": None,
    }
    base.update(over)
    return base


def repo(name="r", stars=0, forks=0, language=None, fork=False):
    return {
        "name": name,
        "stargazers_count": stars,
        "forks_count": forks,
        "language": language,
        "fork": fork,
    }


def test_empty_profile_scores_low():
    report = compute(make_user(), [], now=NOW)
    assert 0 <= report.score < 30
    assert report.grade.startswith("E")


def test_strong_profile_scores_high():
    repos = [repo(f"r{i}", stars=300, forks=40, language=lang)
             for i, lang in enumerate(["Python", "Go", "Rust", "TS", "C"])]
    user = make_user(
        login="star", followers=5000, public_repos=80,
        bio="builder", blog="https://x.dev", location="earth",
        created_at="2012-01-01T00:00:00Z",
    )
    repos.append(repo("star"))  # profile README repo
    report = compute(user, repos, now=NOW)
    assert report.score > 75
    assert report.stats["has_profile_readme"] is True


def test_score_is_bounded():
    repos = [repo(f"r{i}", stars=10**6, forks=10**6, language="Q") for i in range(200)]
    user = make_user(followers=10**7, public_repos=10**5)
    report = compute(user, repos, now=NOW)
    assert report.score <= 100


def test_language_diversity_counts_distinct():
    repos = [repo("a", language="Python"), repo("b", language="Python"),
             repo("c", language="Go")]
    report = compute(make_user(), repos, now=NOW)
    assert report.stats["languages"] == ["Go", "Python"]


def test_profile_readme_detection_is_case_insensitive():
    user = make_user(login="MixedCase")
    report = compute(user, [repo("mixedcase")], now=NOW)
    assert report.stats["has_profile_readme"] is True


def test_forked_repos_excluded_from_own_count():
    repos = [repo("a"), repo("b", fork=True)]
    report = compute(make_user(), repos, now=NOW)
    assert report.stats["own_repos"] == 1


def test_tips_always_include_achievement_hunt():
    report = compute(make_user(), [], now=NOW)
    assert any("Pull Shark" in t for t in report.tips)


def test_tips_suggest_profile_readme_when_missing():
    report = compute(make_user(), [], now=NOW)
    assert any("profile README" in t for t in report.tips)


def test_metrics_never_exceed_max():
    repos = [repo(f"r{i}", stars=999999, forks=999999, language=str(i))
             for i in range(50)]
    report = compute(make_user(followers=999999, public_repos=9999), repos, now=NOW)
    for m in report.metrics:
        assert m.points <= m.max_points + 1e-9


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
