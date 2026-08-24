import json
import requests
from bs4 import BeautifulSoup

USERNAME = "pranshi2300"
URL = f"https://github.com/users/{USERNAME}/contributions"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

days = []

for cell in soup.select("td.ContributionCalendar-day"):
    date = cell.get("data-date")
    level = cell.get("data-level")

    if date and level:
        days.append({
            "date": date,
            "level": int(level)
        })

if not days:
    raise RuntimeError("No contribution data found.")

# Calculate useful statistics
levels = [day["level"] for day in days]

current_streak = 0
for day in reversed(days):
    if day["level"] > 0:
        current_streak += 1
    else:
        break

longest_streak = 0
streak = 0

for day in days:
    if day["level"] > 0:
        streak += 1
        longest_streak = max(longest_streak, streak)
    else:
        streak = 0

best_day = max(days, key=lambda x: x["level"])

data = {
    "username": USERNAME,
    "days": days,
    "total_days": len(days),
    "current_streak": current_streak,
    "longest_streak": longest_streak,
    "best_day": best_day
}
import os

os.makedirs("data", exist_ok=True)

with open("data/contributions.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2)

print(f"Fetched {len(days)} contribution days.")
print(f"Current streak: {current_streak}")
print(f"Longest streak: {longest_streak}")
