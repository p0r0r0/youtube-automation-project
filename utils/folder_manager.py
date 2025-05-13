# folder_manager.py
# ✅ 이 파일은 자동으로 입력 작업 폴더를 생성하거나 덮어쓸지 선택하는 기능을 담당합니다.
# - inputs/채널명/ 아래에 001, 002, 003... 형식으로 폴더를 자동 생성합니다.
# - 기존 폴더가 있을 경우 덮어쓸지, 새로운 폴더를 생성할지 사용자에게 물어봅니다.
# - 선택된 폴더 안에 mp3/ 하위 폴더도 자동 생성됩니다.
# - 이후 이 폴더 경로가 prompt_generator.py로 반환되어 프롬프트 저장 위치로 사용됩니다.

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
            return last_path

    next_num = f"{len(existing)+1:03d}"
    next_path = os.path.join(base_path, next_num)
    os.makedirs(next_path)
    os.makedirs(os.path.join(next_path, "mp3"), exist_ok=True)
    return next_path
