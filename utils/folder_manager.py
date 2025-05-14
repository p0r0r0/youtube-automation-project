# folder_manager.py
# ✅ inputs/채널명/001 등 작업 폴더 생성 또는 덮어쓰기
# ✅ 항상 mp3/ 폴더까지 포함되도록 수정

import os
import shutil

def create_or_overwrite_project(channel_name):
    base_path = os.path.join("inputs", channel_name)
    os.makedirs(base_path, exist_ok=True)

    existing = [f for f in os.listdir(base_path) if f.isdigit()]
    existing.sort()

    if existing:
        last = existing[-1]
        last_path = os.path.join(base_path, last)
        print(f"\n📁 현재 '{channel_name}' 채널의 마지막 작업 폴더: {last}")
        print("1) 기존 작업을 덮어씁니다 (초기화됨)")
        print("2) 새로운 작업 폴더를 생성합니다")
        choice = input("👉 번호를 선택하세요 (1/2): ")

        if choice == "1":
            shutil.rmtree(last_path)
            os.makedirs(last_path)
            # ✅ 덮어쓰기 시에도 mp3 폴더 생성
            os.makedirs(os.path.join(last_path, "mp3"), exist_ok=True)
            return last_path

    next_num = f"{len(existing)+1:03d}"
    next_path = os.path.join(base_path, next_num)
    os.makedirs(next_path)
    # ✅ 새 폴더 생성 시에도 mp3 폴더 생성 (기존 유지)
    os.makedirs(os.path.join(next_path, "mp3"), exist_ok=True)
    return next_path
