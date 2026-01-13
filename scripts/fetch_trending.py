import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os

URL = "https://github.com/trending"

headers = {
    "User-Agent": "Mozilla/5.0"
}

resp = requests.get(URL, headers=headers, timeout=20)
resp.raise_for_status()

soup = BeautifulSoup(resp.text, "html.parser")
repos = soup.select("article.Box-row")

now = datetime.utcnow()
date_str = now.strftime("%Y-%m-%d")
iso_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")

items = []

for idx, repo in enumerate(repos, start=1):
    full_name = repo.h2.get_text(strip=True).replace(" ", "")
    owner, name = full_name.split("/", 1)
    url = f"https://github.com/{full_name}"

    desc_tag = repo.find("p")
    description = desc_tag.get_text(strip=True) if desc_tag else ""

    lang_tag = repo.select_one("span[itemprop='programmingLanguage']")
    language = lang_tag.get_text(strip=True) if lang_tag else None

    star_tag = repo.select_one("a[href$='/stargazers']")
    stars = star_tag.get_text(strip=True) if star_tag else None

    items.append({
        "rank": idx,
        "repo": full_name,
        "owner": owner,
        "name": name,
        "url": url,
        "description": description,
        "language": language,
        "stars": stars,
        "raw": {
            "trending_rank": idx
        }
    })

data = {
    "meta": {
        "source": "github-trending",
        "since": "daily",
        "date": date_str,
        "generated_at": iso_time
    },
    "items": items
}

output_dir = "trending-data"
os.makedirs(output_dir, exist_ok=True)

json_path = os.path.join(output_dir, f"{date_str}.json")

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Trending raw data saved: {json_path}")
