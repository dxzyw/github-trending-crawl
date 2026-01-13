import requests
from bs4 import BeautifulSoup
from datetime import date

URL = "https://github.com/trending"

headers = {
    "User-Agent": "Mozilla/5.0"
}

resp = requests.get(URL, headers=headers, timeout=20)
resp.raise_for_status()

soup = BeautifulSoup(resp.text, "html.parser")
repos = soup.select("article.Box-row")

today = date.today().isoformat()

lines = []
lines.append(f"# GitHub Trending (Daily)\n")
lines.append(f"> Date: {today}\n")

for idx, repo in enumerate(repos[:10], start=1):
    title = repo.h2.get_text(strip=True).replace(" ", "")
    repo_url = "https://github.com/" + title
    desc_tag = repo.find("p")
    desc = desc_tag.get_text(strip=True) if desc_tag else "No description"

    lines.append(f"## {idx}. {title}")
    lines.append(f"- 🔗 {repo_url}")
    lines.append(f"- 📝 {desc}\n")

with open("trending.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("trending.md generated successfully")
