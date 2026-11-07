#!/usr/bin/env python3
"""Render the weekly contribution density bar shown on the profile page.

The strip condenses the last twelve months into one row: each column is one
week, and the column shade is that week's relative contribution intensity
(0-4), so quiet stretches and busy stretches read at a glance.

Data sources, tried in order:
  1. https://github-contributions-api.jogruber.de  (JSON mirror, gives counts)
  2. https://github.com/users/<user>/contributions (GitHub's own calendar)

Both the light and the dark variant land in BAR_OUT_DIR (default: assets/). If
every source fails the script leaves the existing files alone and exits 0, so a
scheduled run never breaks the page or wipes a bar that is already there.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
from datetime import date

USER = os.environ.get("GITHUB_USER", "Beatrice-betty")
ASSET_DIR = os.environ.get("BAR_OUT_DIR", "assets")
BAR_WIDTH = 830
BAR_HEIGHT = 10
GAP = 3
CORNER = 3
TIMEOUT = 20

PALETTES = {
    "light": ["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"],
    "dark": ["#21262d", "#0e4429", "#006d32", "#26a641", "#39d353"],
}

USER_AGENT = "Beatrice-betty-profile-readme"


def _get(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        return response.read().decode("utf-8", "replace")


def weeks_from_api(user: str) -> list[float]:
    payload = json.loads(_get(f"https://github-contributions-api.jogruber.de/v4/{user}?y=last"))
    buckets: dict[tuple[int, int], float] = {}
    for entry in payload.get("contributions") or []:
        raw, count = entry.get("date"), entry.get("count")
        if not raw or not isinstance(count, int):
            continue
        key = _week_key(raw)
        if key:
            buckets[key] = buckets.get(key, 0) + count
    return [buckets[key] for key in sorted(buckets)]


def weeks_from_calendar(user: str) -> list[float]:
    html = _get(f"https://github.com/users/{user}/contributions")
    buckets: dict[tuple[int, int], float] = {}
    for tag in re.findall(r"<td\b[^>]*>", html):
        day = re.search(r'data-date="(\d{4}-\d{2}-\d{2})"', tag)
        level = re.search(r'data-level="(\d)"', tag)
        if not day or not level:
            continue
        key = _week_key(day.group(1))
        if key:
            buckets[key] = buckets.get(key, 0) + int(level.group(1))
    return [buckets[key] for key in sorted(buckets)]


def _week_key(raw: str) -> tuple[int, int] | None:
    try:
        iso = date.fromisoformat(raw).isocalendar()
    except ValueError:
        return None
    return (iso[0], iso[1])


def load_weeks(user: str) -> list[float]:
    for name, loader in (("json api", weeks_from_api), ("github calendar", weeks_from_calendar)):
        try:
            weeks = loader(user)
        except Exception as error:  # any failure simply moves on to the next source
            print(f"::warning::{name} unavailable: {error}")
            continue
        if len(weeks) >= 40:
            print(f"source: {name}, {len(weeks)} weeks, {sum(weeks):.0f} total")
            return weeks
        print(f"::warning::{name} returned only {len(weeks)} weeks")
    return []


def to_levels(weeks: list[float]) -> list[int]:
    """Bucket the newest 53 weekly totals into five shades by quartile."""
    series = weeks[-53:]
    busy = sorted(value for value in series if value > 0)
    if len(busy) >= 8:
        first, second, third = (busy[len(busy) // 4], busy[len(busy) // 2], busy[(3 * len(busy)) // 4])
    else:
        top = max(series) if series else 1
        first = second = third = max(top / 4, 1)
    levels = []
    for value in series:
        if value <= 0:
            levels.append(0)
        elif value <= first:
            levels.append(1)
        elif value <= second:
            levels.append(2)
        elif value <= third:
            levels.append(3)
        else:
            levels.append(4)
    return levels


def render(levels: list[int], palette: list[str]) -> str:
    count = len(levels)
    segment = (BAR_WIDTH - GAP * (count - 1)) / count
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{BAR_WIDTH}" height="{BAR_HEIGHT}" '
        f'viewBox="0 0 {BAR_WIDTH} {BAR_HEIGHT}" role="img" '
        f'aria-label="{USER} 过去一年每周贡献相对强度">',
        f"  <title>{USER} 过去一年每周贡献相对强度</title>",
    ]
    for index, level in enumerate(levels):
        x = index * (segment + GAP)
        parts.append(
            f'  <rect x="{x:.2f}" y="0" width="{segment:.2f}" height="{BAR_HEIGHT}" '
            f'rx="{CORNER}" fill="{palette[level]}"/>'
        )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main() -> int:
    weeks = load_weeks(USER)
    if not weeks:
        print("::warning::no contribution data available, keeping the current bars")
        return 0

    levels = to_levels(weeks)
    os.makedirs(ASSET_DIR, exist_ok=True)
    for mode, palette in PALETTES.items():
        path = os.path.join(ASSET_DIR, f"contribution-bar-{mode}.svg")
        with open(path, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(render(levels, palette))
        print(f"wrote {path}")

    shades = " ".join(str(levels.count(level)) for level in range(5))
    print(f"weeks: {len(levels)} | shades 0-4: {shades}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
