import requests
from bs4 import BeautifulSoup
from datetime import datetime
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
time_str = now.strftime("%Y-%m-%d %H:%M UTC")

# 输出目录
output_dir = "trending"
os.makedirs(output_dir, exist_ok=True)

filename = f"github-trending-{date_str}.md"
filepath = os.path.join(output_dir, filename)

lines = []
lines.append(f"# GitHub 今日热门项目（{date_str}）\n")
lines.append(f"> 数据来源：GitHub Trending")
lines.append(f"> 更新时间：{time_str}\n")
lines.append("---\n")

def simple_cn_intro(desc: str) -> str:
    """不依赖 API 的简要中文解释（规则+直译）"""
    if not desc:
        return "暂无项目描述。"

    return (
        f"{desc}。"
        "这是一个当前在 GitHub 社区中关注度快速上升的开源项目，"
        "适合关注其技术实现和应用场景。"
    )

for idx, repo in enumerate(repos[:10], start=1):
    title = repo.h2.get_text(strip=True).replace(" ", "")
    repo_url = "https://github.com/" + title

    desc_tag = repo.find("p")
    desc = desc_tag.get_text(strip=True) if desc_tag else ""

    star_tag = repo.select_one("a[href$='/stargazers']")
    stars = star_tag.get_text(strip=True) if star_tag else "N/A"

    lang_tag = repo.select_one("span[itemprop='programmingLanguage']")
    language = lang_tag.get_text(strip=True) if lang_tag else "N/A"

    lines.append(f"## {idx}️⃣ {title}\n")
    lines.append(f"**项目地址**  ")
    lines.append(f"{repo_url}\n")

    lines.append("**项目简介（中文）**  ")
    lines.append(simple_cn_intro(desc) + "\n")

    if desc:
        lines.append("**项目简介（原文）**  ")
        lines.append(desc + "\n")

    lines.append("**主要信息**")
    lines.append(f"- ⭐ Star 数：{stars}")
    lines.append(f"- 🧑‍💻 主要语言：{language}\n")
    lines.append("---\n")

with open(filepath, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"{filepath} generated successfully")
