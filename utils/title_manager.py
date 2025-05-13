# title_manager.py
# ✅ 이 파일은 유튜브 제목 중복 방지를 위한 기능을 포함하고 있습니다.
# - used_titles.json 파일을 기반으로 이전에 사용된 제목을 추적합니다.
# - base 주제와 다양한 suffix를 조합하여 유니크한 제목을 생성합니다.
# - 만약 모든 조합이 중복될 경우, 날짜/시간을 붙여서 제목을 생성합니다.
# - 생성된 제목은 자동으로 기록됩니다.

import os
import json
from datetime import datetime

USED_TITLE_PATH = os.path.join("data", "used_titles.json")

# 예시 서브 문구 (각 채널에 따라 더 추가 가능)
SUFFIXES = [
    "for Focus", "to Boost Productivity", "with Rain Sounds",
    "during Exam Week", "with Calm Piano", "for Deep Sleep",
    "during Thunderstorm", "for Baby Nap", "to Relax Your Pet"
]

def load_used_titles():
    if not os.path.exists(USED_TITLE_PATH):
        return []
    with open(USED_TITLE_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_used_title(title):
    titles = load_used_titles()
    titles.append({
        "date": datetime.now().strftime('%Y-%m-%d'),
        "title": title
    })
    with open(USED_TITLE_PATH, 'w', encoding='utf-8') as f:
        json.dump(titles, f, ensure_ascii=False, indent=2)

def generate_unique_title(channel, base):
    used = [t['title'] for t in load_used_titles()]
    for suffix in SUFFIXES:
        candidate = f"{base} {suffix}"
        if candidate not in used:
            save_used_title(candidate)
            return candidate
    # fallback: 중복 다 될 경우 날짜 붙이기
    fallback = f"{base} {datetime.now().strftime('%Y%m%d_%H%M%S')}"
    save_used_title(fallback)
    return fallback
