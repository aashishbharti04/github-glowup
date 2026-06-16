"""Terminal rendering with ANSI colors (no third-party deps)."""

from __future__ import annotations

import os
import sys

from .score import Report

_RESET = "\033[0m"
_BOLD = "\033[1m"
_DIM = "\033[2m"
_CYAN = "\033[96m"
_MAGENTA = "\033[95m"
_GREEN = "\033[92m"
_YELLOW = "\033[93m"
_RED = "\033[91m"
_GREY = "\033[90m"


def _supports_color() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("FORCE_COLOR"):
        return True
    return sys.stdout.isatty()


def _supports_unicode() -> bool:
    enc = getattr(sys.stdout, "encoding", None) or "ascii"
    try:
        "█░╔╝✦".encode(enc)
        return True
    except (UnicodeEncodeError, LookupError):
        return False


class _Glyphs:
    def __init__(self, unicode_ok: bool):
        if unicode_ok:
            self.full, self.empty = "█", "░"
            self.tl, self.tr, self.bl, self.br = "╔", "╗", "╚", "╝"
            self.h, self.v, self.star = "═", "║", "✦"
        else:
            self.full, self.empty = "#", "-"
            self.tl, self.tr, self.bl, self.br = "+", "+", "+", "+"
            self.h, self.v, self.star = "=", "|", "*"


def _c(text: str, color: str, enabled: bool) -> str:
    return f"{color}{text}{_RESET}" if enabled else text


def _bar(fraction: float, width: int, enabled: bool, g: "_Glyphs") -> str:
    fraction = max(0.0, min(1.0, fraction))
    filled = round(fraction * width)
    if fraction >= 0.75:
        color = _GREEN
    elif fraction >= 0.45:
        color = _YELLOW
    else:
        color = _RED
    bar = g.full * filled + g.empty * (width - filled)
    return _c(bar, color, enabled)


def render(report: Report, color: bool | None = None, unicode_ok: bool | None = None) -> str:
    enabled = _supports_color() if color is None else color
    g = _Glyphs(_supports_unicode() if unicode_ok is None else unicode_ok)
    dash = "-" if g.star == "*" else "—"
    out: list[str] = []

    title = f"  GitHub Glow-Up {dash} @{report.username}  "
    out.append(_c(g.tl + g.h * (len(title)) + g.tr, _MAGENTA, enabled))
    out.append(_c(g.v, _MAGENTA, enabled) + _c(title, _BOLD + _CYAN, enabled)
               + _c(g.v, _MAGENTA, enabled))
    out.append(_c(g.bl + g.h * (len(title)) + g.br, _MAGENTA, enabled))
    out.append("")

    score_line = f"  Power Score: {report.score:.1f}/100"
    out.append(_c(score_line, _BOLD + _GREEN, enabled))
    out.append(_c(f"  Grade: {report.grade}", _BOLD + _YELLOW, enabled))
    out.append("")

    out.append(_c("  Breakdown", _BOLD, enabled))
    label_w = max(len(m.label) for m in report.metrics)
    for m in report.metrics:
        frac = m.points / m.max_points if m.max_points else 0.0
        line = (
            f"  {m.label.ljust(label_w)}  "
            f"{_bar(frac, 16, enabled, g)} "
            f"{m.points:5.1f}/{m.max_points:<4.0f}  "
            + _c(m.detail, _GREY, enabled)
        )
        out.append(line)
    out.append("")

    out.append(_c("  How to level up", _BOLD + _MAGENTA, enabled))
    for i, tip in enumerate(report.tips, 1):
        out.append(_c(f"  {i}. ", _CYAN, enabled) + tip)
    out.append("")
    out.append(_c(f"  {g.star} glow up your profile: "
                  "github.com/aashishbharti04/github-glowup", _DIM, enabled))
    return "\n".join(out)
