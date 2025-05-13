# prompt_generator.py
# ✅ 이 파일은 자동화 프로젝트의 메인 실행기입니다.
# - 사장님이 직접 실행하는 유일한 파일이며, 실행 시 다음 기능이 수행됩니다:
#   1. StudyMooz / WhisperLullaby / CalmPet 중 채널 선택
#   2. 해당 채널의 작업 폴더(001, 002...) 자동 생성 또는 덮어쓰기 여부 선택
#   3. Google Trends 기반 실시간 트렌드 키워드 가져오기 (중복 제목 자동 회피)
#   4. 트렌드 기반 제목 생성 및 Suno/Midjourney/Runway 프롬프트 구성
#   5. 프롬프트를 텍스트 파일로 저장하여 영상 제작/업로드에 활용 가능하게 준비

from utils.folder_manager import create_or_overwrite_project
from utils.title_manager import generate_unique_title
from utils.trend_keywords import get_trending_set
from utils.prompt_template import build_prompt_file

# 채널 목록
CHANNELS = {
    "1": "studymooz",
    "2": "whisperlullaby",
    "3": "calmpet"
}

print("🎵 어떤 채널의 음악을 만드시겠습니까?")
print("1) StudyMooz (공부용 Lo-fi)")
print("2) WhisperLullaby (아기 수면 음악)")
print("3) CalmPet Melodies (반려동물 음악)")

channel_choice = input("👉 번호를 입력해주세요 (1/2/3): ")
if channel_choice not in CHANNELS:
    print("❌ 잘못된 선택입니다. 프로그램을 종료합니다.")
    exit()

channel = CHANNELS[channel_choice]
print(f"\n✅ 선택한 채널: {channel}\n")

# 폴더 생성 또는 덮어쓰기 선택
project_path = create_or_overwrite_project(channel)

# 실시간 트렌드 기반 주제 세트 가져오기
trending = get_trending_set(channel)
topic = trending["topic"]

# 중복 방지 제목 생성
final_title = generate_unique_title(channel, topic)
print(f"📢 생성된 유튜브 제목: {final_title}\n")

# 프롬프트 파일 생성
build_prompt_file(channel, project_path)
print(f"📄 프롬프트 파일 생성 완료: {project_path}/{channel}_prompt.txt")

print("\n🎉 자동화 프로젝트 준비 완료! 이제 Suno, Midjourney, Runway 작업을 시작하세요.")
