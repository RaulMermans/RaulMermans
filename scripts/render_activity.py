
#!/usr/bin/env python3
"""Generate an editorial GitHub profile SVG from GitHub's contribution calendar.

Production: GH_TOKEN=... python scripts/render_activity.py
Visual test: python scripts/render_activity.py --demo
No third-party Python dependencies. No synthetic data in production mode.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta, timezone
from html import escape
from pathlib import Path

USER = os.getenv("GITHUB_REPOSITORY_OWNER", "RaulMermans")
DEST = Path("dist/activity-signal.svg")
API_QUERY = """
query($login:String!){
  user(login:$login){
    contributionsCollection{
      contributionCalendar{
        totalContributions
        weeks{contributionDays{date contributionCount contributionLevel}}
      }
    }
  }
}
"""

# Historically verified merged upstream pull requests.
MILESTONES = [
    (
        "29 SEP 2026",
        "LEMONADE",
        "Backend config safety",
        "https://github.com/lemonade-sdk/lemonade/pull/3684",
    ),
    (
        "21 OCT 2026",
        "OPENLIT",
        "LangGraph memory connector",
        "https://github.com/openlit/openlit/pull/1667",
    ),
    (
        "02 NOV 2026",
        "OPENJUDGE",
        "Grader correctness fix",
        "https://github.com/agentscope-ai/OpenJudge/pull/200",
    ),
]

W, H = 1400, 680
BG = "#0B0F14"
FG = "#F0EEE7"
DIM = "#9AA6B0"
LOW = "#596875"
ACC = "#81E6CF"
WARM = "#EAC797"


def github_calendar(login: str) -> tuple[list[dict], int]:
    token = os.getenv("GH_TOKEN", "").strip()
    if not token:
        raise RuntimeError(
            "GH_TOKEN is required: refusing to publish fictional activity."
        )

    data = json.dumps({
        "query": API_QUERY,
        "variables": {"login": login}
    }).encode()

    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=data,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "raulmermans-activity-signal-v2",
        },
    )

    with urllib.request.urlopen(req, timeout=30) as response:
        payload = json.load(response)

    if payload.get("errors"):
        raise RuntimeError(
            "GraphQL API error: " + str(payload["errors"])[:450]
        )

    user = (payload.get("data") or {}).get("user")
    if not user:
        raise RuntimeError("GitHub user not found in GraphQL response")

    cal = user["contributionsCollection"]["contributionCalendar"]

    by_date = {}

    for week in cal["weeks"]:
        for day in week["contributionDays"]:
            by_date[date.fromisoformat(day["date"])] = int(
                day["contributionCount"]
            )

    if not by_date:
        raise RuntimeError(
            "Empty contribution calendar — refusing to publish"
        )

    days = [
        {"date": d, "count": c}
        for d, c in sorted(by_date.items())
    ]

    return days, int(cal["totalContributions"])


def visual_demo() -> tuple[list[dict], int]:
    # Clearly synthetic; only generated when --demo is passed.
    rng = random.Random(20261113)
    end = date(2026, 11, 13)
    days = []

    for i in range(365):
        d = end - timedelta(days=364-i)
        active = (
            rng.random() < 0.60
            if i > 80
            else rng.random() < 0.22
        )
        n = rng.randint(1, 16) if active else 0

        if d.weekday() == 6:
            n = int(n * 0.6)

        days.append({"date": d, "count": n})

    return days, sum(x["count"] for x in days)


def streaks(days: list[dict]) -> tuple[int, int]:
    counts = {
        entry["date"]: entry["count"]
        for entry in days
    }

    # Today's contributions may still be in progress.
    final_day = max(counts)

    if not counts[final_day]:
        final_day -= timedelta(days=1)

    active_streak = 0
    d = final_day

    while d in counts and counts[d] > 0:
        active_streak += 1
        d -= timedelta(days=1)

    longest = 0
    run = 0

    for v in days:
        if v["count"] > 0:
            run += 1
            longest = max(longest, run)
        else:
            run = 0

    return active_streak, longest


def prepare_grid(
    days: list[dict]
) -> tuple[list[tuple[date, int]], list[tuple[int, str]], list[int]]:

    # 53 weeks, Sunday-first, with current data in the last week.
    by_date = {
        entry["date"]: entry["count"]
        for entry in days
    }

    end = max(by_date)
    last_sun = end + timedelta(days=(6 - end.weekday()) % 7)
    start = last_sun - timedelta(days=370)

    items = []
    month_marks = []
    totals = [0] * 53
    last_month = None

    for col in range(53):
        for row in range(7):
            d = start + timedelta(days=col * 7 + row)
            count = by_date.get(d, 0) if d <= end else -1

            items.append((d, count))

            if count > 0:
                totals[col] += count

            if count != -1 and d.month != last_month:
                if d.day < 8 or col == 0:
                    month_marks.append(
                        (col, d.strftime("%b").upper())
                    )
                last_month = d.month

    return items, month_marks, totals


def render_svg(
    days: list[dict],
    total: int,
    *,
    demo: bool
) -> str:

    if not days or total < 0:
        raise ValueError("Invalid contribution data")

    login = escape(USER)
    today = max(x["date"] for x in days)
    active_days = sum(1 for x in days if x["count"] > 0)
    current, longest = streaks(days)

    cells, months, weekly = prepare_grid(days)

    peak = max(weekly)
    peak_ix = weekly.index(peak)

    generated = datetime.now(timezone.utc).strftime(
        "%d %b %Y / %H:%M UTC"
    ).upper()

    grid_x = 64
    grid_y = 330
    dx = 24
    dy = 25
    cell_w = 18
    cell_h = 18

    svg = []
    add = svg.append

    add(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" '
        f'aria-labelledby="title desc">'
    )

    add(
        f'<title id="title">'
        f'Engineering, in motion — {login}'
        f'</title>'
    )

    add(
        '<desc id="desc">'
        'Last year of GitHub contributions visualized as a heatmap. '
        'Includes active days, contributions, longest recent streak '
        'and three verified merged pull requests.'
        '</desc>'
    )

    add('''
<defs>
  <linearGradient id="ink" x1="0" y1="0" x2="1" y2="0">
    <stop stop-color="#81E6CF"/>
    <stop offset="100%" stop-color="#A5BDFF"/>
  </linearGradient>

  <linearGradient id="thread" x1="0" y1="0" x2="1" y2="0">
    <stop stop-color="#81E6CF" stop-opacity="0.15"/>
    <stop offset="50%" stop-color="#81E6CF" stop-opacity="0.9"/>
    <stop offset="100%" stop-color="#A5BDFF" stop-opacity="0.20"/>
  </linearGradient>

  <style>
    .mono {
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    }

    .sans {
      font-family: Inter, Arial, Helvetica, sans-serif;
    }

    .upper {
      letter-spacing: 2.4px;
    }

    .pulse {
      transform-origin: center;
      animation: breath 6s ease-in-out infinite;
    }

    .shift {
      stroke-dasharray: 14 26;
      animation: flow 22s linear infinite;
    }

    @keyframes breath {
      0%, 100% { opacity: .65; }
      50% { opacity: 1; }
    }

    @keyframes flow {
      to { stroke-dashoffset: -400; }
    }

    @media (prefers-reduced-motion: reduce) {
      .pulse, .shift { animation: none !important; }
    }
  </style>
</defs>
''')

    add(
        f'<rect width="{W}" height="{H}" '
        f'rx="16" fill="{BG}"/>'
    )

    add(
        '<rect x="24" y="24" width="1352" height="632" '
        'rx="8" fill="none" stroke="#29313A" stroke-width="1"/>'
    )

    # Editorial header
    add(
        f'<text x="63" y="69" class="mono upper" '
        f'font-size="16" fill="{ACC}">'
        f'RM / ENGINEERING FIELD NOTES</text>'
    )

    add(
        f'<text x="1336" y="69" class="mono upper" '
        f'font-size="15" text-anchor="end" fill="{DIM}">'
        f'NO. 002 / LIVE GITHUB DATA</text>'
    )

    add(
        f'<text x="62" y="145" class="sans" '
        f'font-weight="700" font-size="62" '
        f'letter-spacing="-2.6" fill="{FG}">'
        f'Engineering, in motion'
        f'<tspan fill="{ACC}">.</tspan></text>'
    )

    add(
        f'<text x="65" y="180" class="sans" '
        f'font-size="19" fill="{DIM}">'
        f'An evolving record of building, testing, '
        f'and contributing beyond my own repositories.'
        f'</text>'
    )

    add(
        '<line x1="63" y1="208" x2="1337" y2="208" '
        'stroke="#34404A" stroke-width="1"/>'
    )

    # Metrics row
    labels = [
        ("CONTRIBUTIONS / 12M", f"{total:,}"),
        ("ACTIVE DAYS / WINDOW", f"{active_days}"),
        ("LONGEST STREAK / 12M", f"{longest}d"),
        ("UPSTREAM PRS / MERGED", "03"),
    ]

    for k, (label, val) in enumerate(labels):
        x = 64 + k * 325

        add(
            f'<text x="{x}" y="242" class="mono upper" '
            f'font-size="14" fill="{DIM}">'
            f'{escape(label)}</text>'
        )

        add(
            f'<text x="{x}" y="296" class="sans" '
            f'font-weight="600" font-size="49" '
            f'letter-spacing="-1.4" fill="{FG}">'
            f'{val}</text>'
        )

        if k:
            add(
                f'<line x1="{x - 24}" y1="229" '
                f'x2="{x - 24}" y2="294" stroke="#29323B"/>'
            )

    add(
        '<line x1="63" y1="315" x2="1337" y2="315" '
        'stroke="#34404A" stroke-width="1"/>'
    )

    # Month labels
    for col, m in months:
        x = grid_x + dx * col

        add(
            f'<text x="{x}" y="349" class="mono" '
            f'font-size="13" fill="{DIM}" '
            f'letter-spacing="1.0">{m}</text>'
        )

    # 53-week contribution calendar
    for col in range(53):
        for row in range(7):
            d, count = cells[col * 7 + row]

            x = grid_x + dx * col
            y = grid_y + 28 + dy * row

            if count == -1:
                fill = "#121920"
            elif count == 0:
                fill = "#1B2630"
            elif count <= 2:
                fill = "#355E63"
            elif count <= 6:
                fill = "#418F88"
            elif count <= 12:
                fill = "#6AC4B3"
            else:
                fill = ACC

            add(
                f'<rect x="{x}" y="{y}" '
                f'width="{cell_w}" height="{cell_h}" '
                f'rx="3" fill="{fill}">'
                f'<title>{d.isoformat()}: '
                f'{max(count, 0)} contributions</title>'
                f'</rect>'
            )

    # Weekly activity line derived from real contribution totals
    top = 556
    bottom = 581
    max_t = max(peak, 1)

    coords = []

    for i, t in enumerate(weekly):
        coords.append((
            grid_x + i * dx + cell_w / 2,
            bottom - (t / max_t) * (bottom - top)
        ))

    path = " ".join(
        ("M" if i == 0 else "L") + f"{x:.1f},{y:.1f}"
        for i, (x, y) in enumerate(coords)
    )

    add(
        f'<path d="{path}" fill="none" '
        f'stroke="#2C5661" stroke-width="7" '
        f'opacity="0.20"/>'
    )

    add(
        f'<path d="{path}" fill="none" '
        f'stroke="url(#thread)" stroke-width="2.5" '
        f'class="shift"/>'
    )

    add(
        f'<circle class="pulse" '
        f'cx="{coords[peak_ix][0]:.1f}" '
        f'cy="{coords[peak_ix][1]:.1f}" '
        f'r="5" fill="{ACC}"/>'
    )

    add(
        f'<text x="64" y="539" class="mono upper" '
        f'font-size="13" fill="{DIM}">'
        f'WEEKLY VOLUME / PEAK {peak}</text>'
    )

    add(
        f'<text x="1337" y="539" class="mono upper" '
        f'font-size="13" fill="{DIM}" text-anchor="end">'
        f'LAST DATA POINT {today.isoformat()}</text>'
    )

    # Verified historical open-source contribution milestones
    add(
        '<line x1="63" y1="600" x2="1337" y2="600" '
        'stroke="#34404A" stroke-width="1"/>'
    )

    add(
        f'<text x="64" y="626" class="mono upper" '
        f'font-size="13" fill="{ACC}">'
        f'EXTERNAL VALIDATION</text>'
    )

    for i, (dt, project, desc, url) in enumerate(MILESTONES):
        x = 366 + i * 328

        add(
            f'<circle cx="{x}" cy="622" r="3" '
            f'fill="{WARM}"/>'
        )

        add(
            f'<text x="{x + 13}" y="626" class="mono" '
            f'font-size="14" fill="{FG}">'
            f'{project}</text>'
        )

        add(
            f'<text x="{x + 13}" y="645" class="mono" '
            f'font-size="12" fill="{DIM}">'
            f'{dt}</text>'
        )

    if demo:
        add(
            '<rect x="430" y="14" width="540" height="28" '
            'fill="#54352E" rx="4"/>'
        )

        add(
            '<text x="700" y="33" class="mono" '
            'text-anchor="middle" fill="#FFE3D8" font-size="13">'
            'VISUAL PROTOTYPE · SYNTHETIC ACTIVITY DATA'
            '</text>'
        )

    add("</svg>")

    return "\n".join(svg)


def main():
    p = argparse.ArgumentParser()

    p.add_argument(
        "--demo",
        action="store_true",
        help="Render visual prototype with labeled synthetic data"
    )

    p.add_argument(
        "--out",
        default=str(DEST)
    )

    args = p.parse_args()

    if args.demo:
        days, total = visual_demo()
    else:
        days, total = github_calendar(USER)

    out = render_svg(days, total, demo=args.demo)

    if (
        "<svg " not in out
        or "</svg>" not in out
        or len(out) < 10000
    ):
        raise RuntimeError("Generated SVG failed sanity checks")

    path = Path(args.out)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(out, encoding="utf-8")

    print(
        f"Created {path}: {len(out):,} bytes; "
        f"mode={'DEMO' if args.demo else 'REAL'}; "
        f"last={max(d['date'] for d in days)}"
    )


if __name__ == "__main__":
    try:
        main()
    except (
        OSError,
        ValueError,
        RuntimeError,
        urllib.error.URLError
    ) as err:
        print(f"ERROR: {err}", file=sys.stderr)
        sys.exit(1)
