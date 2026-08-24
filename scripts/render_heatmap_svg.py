import json
from datetime import datetime

INPUT_FILE = "data/contributions.json"
OUTPUT_FILE = "contrib-heatmap.svg"

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)

days = data["days"]

# GitHub-style colors
PALETTE = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
]

CELL = 13
GAP = 4
STEP = CELL + GAP

LEFT = 30
TOP = 35

# Convert contribution days into a lookup table
day_map = {
    day["date"]: day["level"]
    for day in days
}

# Parse dates
dates = [
    datetime.strptime(day["date"], "%Y-%m-%d").date()
    for day in days
]

start = min(dates)

# Move start back to Sunday
start = start.fromordinal(
    start.toordinal() - ((start.weekday() + 1) % 7)
)

# Generate 53 weeks
weeks = 53

width = LEFT + weeks * STEP + 20
height = TOP + 7 * STEP + 40

svg = []

svg.append(
    f'''<svg xmlns="http://www.w3.org/2000/svg"
    width="{width}"
    height="{height}"
    viewBox="0 0 {width} {height}">
'''
)

svg.append("""
<style>
.cell {
    opacity: 0;
    animation: appear 0.35s ease forwards;
}

@keyframes appear {
    from {
        opacity: 0;
        transform: translateY(-8px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>
""")

svg.append("""
<text x="30" y="22"
      font-family="monospace"
      font-size="15"
      fill="#39d353">
    contributions.sh
</text>
""")

# Draw contribution cells
for week in range(weeks):
    for weekday in range(7):

        current = start.fromordinal(
            start.toordinal()
            + week * 7
            + weekday
        )

        date_string = current.isoformat()

        level = day_map.get(date_string, 0)

        if level < 0:
            level = 0

        if level > 4:
            level = 4

        x = LEFT + week * STEP
        y = TOP + weekday * STEP

        delay = (week * 7 + weekday) * 0.012

        svg.append(
            f'''
<rect
    class="cell"
    x="{x}"
    y="{y}"
    width="{CELL}"
    height="{CELL}"
    rx="3"
    fill="{PALETTE[level]}"
    style="animation-delay:{delay:.3f}s"
/>
'''
        )

# Legend
legend_y = height - 20

svg.append(
    f'''
<text x="{LEFT}" y="{legend_y}"
      font-family="monospace"
      font-size="11"
      fill="#8b949e">
    Less
</text>
'''
)

for i in range(5):
    x = LEFT + 35 + i * STEP

    svg.append(
        f'''
<rect
    x="{x}"
    y="{legend_y - 10}"
    width="{CELL}"
    height="{CELL}"
    rx="3"
    fill="{PALETTE[i]}"
/>
'''
    )

svg.append(
    f'''
<text x="{LEFT + 35 + 5 * STEP + 5}"
      y="{legend_y}"
      font-family="monospace"
      font-size="11"
      fill="#8b949e">
    More
</text>
'''
)

svg.append("</svg>")

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    file.write("".join(svg))

print(f"Created {OUTPUT_FILE}")
