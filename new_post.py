#!/usr/bin/env python3
"""
Usage:
  python new_post.py
"""

import os
import re
import sys
from datetime import datetime


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text


def extract_iframe_src(iframe_code: str) -> str:
    match = re.search(r'src=["\']([^"\']+)["\']', iframe_code)
    return match.group(1) if match else iframe_code.strip()


def build_post(title: str, date: str, categories: list[str], tags: list[str],
               iframe_src: str, description: str) -> str:
    cats = "[" + ", ".join(categories) + "]"
    tag_list = "[" + ", ".join(tags) + "]"

    return f"""---
title: "{title}"
date: {date}
categories: {cats}
tags: {tag_list}
description: "{description}"
---

{f'> {description}' if description else ''}

<div style="position:relative;width:100%;padding-top:56.25%;margin:2rem 0;">
  <iframe
    src="{iframe_src}"
    style="position:absolute;top:0;left:0;width:100%;height:100%;border:none;"
    allowfullscreen="true"
    mozallowfullscreen="true"
    webkitallowfullscreen="true">
  </iframe>
</div>

<!-- 슬라이드 아래에 본문을 자유롭게 작성하세요 -->

"""


def main():
    print("=== GitHub Pages 블로그 포스트 생성기 ===\n")

    title = input("제목: ").strip()
    if not title:
        print("제목을 입력해야 합니다.")
        sys.exit(1)

    date_default = datetime.today().strftime("%Y-%m-%d")
    date_input = input(f"날짜 [{date_default}]: ").strip()
    date = date_input if date_input else date_default

    print("카테고리 (쉼표 구분, 예: AI, Paper Review): ", end="")
    cats_raw = input().strip()
    categories = [c.strip() for c in cats_raw.split(",") if c.strip()] or ["Uncategorized"]

    print("태그 (쉼표 구분, 예: LLM, Survey): ", end="")
    tags_raw = input().strip()
    tags = [t.strip() for t in tags_raw.split(",") if t.strip()]

    description = input("한 줄 설명 (선택): ").strip()

    print("\nGoogle Slides iframe 코드를 붙여넣으세요.")
    print("(전체 <iframe ...> 태그 또는 src URL만 입력 후 Enter 두 번)")
    lines = []
    while True:
        line = input()
        if line == "" and lines:
            break
        lines.append(line)
    iframe_raw = "\n".join(lines)
    iframe_src = extract_iframe_src(iframe_raw)

    posts_dir = os.path.join(os.path.dirname(__file__), "_posts")
    os.makedirs(posts_dir, exist_ok=True)

    slug = slugify(title)
    filename = f"{date}-{slug}.md"
    filepath = os.path.join(posts_dir, filename)

    content = build_post(title, date, categories, tags, iframe_src, description)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\n✓ 포스트 생성 완료: _posts/{filename}")
    print("\n다음 명령어로 배포하세요:")
    print("  git add .")
    print(f'  git commit -m "add: {title}"')
    print("  git push")


if __name__ == "__main__":
    main()
