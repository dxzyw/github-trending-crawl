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
cn_date = now.strftime("%Y年%m月%d日")

output_dir = "trending"
os.makedirs(output_dir, exist_ok=True)

filename = f"公众号草稿-GitHub热榜-{date_str}.md"
filepath = os.path.join(output_dir, filename)

lines = []

# ===== 标题 =====
lines.append(f"# GitHub 今日热榜精选（{cn_date}）\n")

# ===== 导语 =====
lines.append(
    "GitHub 每天都会涌现出大量值得关注的新项目，"
    "它们往往代表着**最新的技术趋势、开发方向和工具选择**。\n"
)
lines.append(
    "本文为你精选 **今日 GitHub Trending 热度最高的项目**，"
    "并用中文做了简要解读，帮助你快速判断：\n\n"
    "👉 这个项目是做什么的？\n"
    "👉 值不值得关注或上手？\n"
)
lines.append("---\n")

def cn_explain(desc: str) -> str:
    if not desc:
        return (
            "这是一个近期热度快速上升的开源项目，"
            "目前在开发者社区中受到广泛关注，"
            "适合持续观察其后续发展。"
        )

    return (
        f"从官方描述来看，该项目主要用于：{desc}。\n\n"
        "结合当前 GitHub 热度判断，"
        "它很可能解决了某一类开发者的实际痛点，"
        "或者在现有方案上提供了更高效的实现方式。"
    )

for idx, repo in enumerate(repos[:8], start=1):
    title = repo.h2.get_text(strip=True).replace(" ", "")
    repo_url = "https://github.com/" + title

    desc_tag = repo.find("p")
    desc = desc_tag.get_text(strip=True) if desc_tag else ""

    star_tag = repo.select_one("a[href$='/stargazers']")
    stars = star_tag.get_text(strip=True) if star_tag else "N/A"

    lang_tag = repo.select_one("span[itemprop='programmingLanguage']")
    language = lang_tag.get_text(strip=True) if lang_tag else "未知"

    lines.append(f"## 🔥 {idx}. {title}\n")

    lines.append("**这个项目是做什么的？**\n")
    lines.append(cn_explain(desc) + "\n")

    lines.append("**为什么值得关注？**\n")
    lines.append(
        "从 Trending 榜单表现来看，"
        "该项目在短时间内获得了大量开发者的 Star，"
        "说明它在实用性、话题性或技术实现上具有明显亮点。\n"
    )

    lines.append("**项目信息速览**")
    lines.append(f"- ⭐ GitHub Star：{stars}")
    lines.append(f"- 💻 主要语言：{language}")
    lines.append(f"- 🔗 项目地址：{repo_url}\n")

    lines.append("---\n")

# ===== 结尾 =====
lines.append(
    "以上就是今日 GitHub 热榜的精选项目。\n\n"
    "如果你关注 **AI / 后端 / 架构 / 工程效率** 相关内容，"
    "欢迎持续关注，后续会定期整理：\n\n"
    "- GitHub 热榜解读\n"
    "- 值得尝试的开源项目\n"
    "- 开发者工具与实践经验\n"
)

with open(filepath, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"{filepath} generated successfully")
