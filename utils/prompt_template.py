# prompt_template.py
# ✅ 프롬프트 자동 생성기 (유튜브 자동화용)
# - 영어 전용 설명문 생성
# - 명언 랜덤 추출 (영어)
# - 태그 자동 확장 및 중복 제거
# - 프롬프트(썸네일/영상/음악) 구분 저장
# - 설명용 한국어는 별도 txt 파일에 분리됨

import os
import random
from utils.trend_keywords import get_trending_set

def build_prompt_file(channel, folder_path):
    trending = get_trending_set(channel)

    # 명언 랜덤 선택
    quote_pool = [
        ("Success is the sum of small efforts, repeated day in and day out.", "성공은 매일 반복된 작은 노력의 합이다."),
        ("Let her sleep, for when she wakes, she will move mountains.", "아이가 잠들게 하라. 깨어났을 땐 세상을 움직일 것이다."),
        ("Until one has loved an animal, a part of one's soul remains unawakened.", "동물을 사랑해보지 않은 사람은 영혼의 일부가 잠든 것이다."),
        ("The future depends on what you do today.", "미래는 오늘 당신이 하는 일에 달려 있다."),
        ("Peace is always beautiful.", "평화는 언제나 아름답다."),
        ("Let your soul catch up with your body.", "당신의 영혼이 몸을 따라잡게 하라.")
    ]
    quote_en, quote_kr = random.choice(quote_pool)

    topic = trending["topic"]
    concept = trending["concept"]
    styles = trending["styles"]
    exclude = trending["exclude"]
    tags = trending["tags"]
    mj_prompt = "A beautiful young woman studying with a pen on a notebook, soft lighting, cozy indoor study environment, bookshelf behind, cinematic composition --ar 16:9 --style raw --v 6" if channel == "studymooz" else trending["mj_prompt"]
    rw_prompt = trending["rw_prompt"]

    thumbnail_text_options = [
        f"Focus deeply with this {topic} mix",
        f"Let the sound of {topic} guide your flow",
        f"Find peace in a {topic} atmosphere",
        f"Your moment of calm starts with {topic}",
        f"Lose yourself in the mood of {topic}"
    ]
    thumbnail_text = random.choice(thumbnail_text_options)
    title = thumbnail_text

    # Suno 프롬프트 30개 생성
    suno_prompts = []
    for _ in range(30):
        style = random.choice(styles)
        mood = random.choice(["calm", "gentle", "dreamy", "immersive", "emotional"])
        texture = random.choice(["mono reverb", "stereo spread", "lowpass filtered", "ambient pad background"])
        bpm = random.choice(["60BPM", "70BPM", "85BPM", "90BPM"])
        prompt = f"{style}, {bpm}, {texture}, designed to be {mood}"
        if len(prompt) <= 200:
            suno_prompts.append(prompt)

    # 유튜브 업로드용 파일 (영문 전용)
    upload_txt_path = os.path.join(folder_path, "upload_fields_for_api.txt")
    with open(upload_txt_path, 'w', encoding='utf-8') as up:
        up.write(f"[YouTube Title]\n{title}\n\n")
        up.write("[Description]\n")
        up.write(
            "This ambient lo-fi mix is perfect for working, studying, or relaxing.\n"
            "Immerse yourself in deep focus with piano textures, soft rhythmic layers, and cozy rain sounds.\n"
            "Stay grounded and productive during any moment of stress or distraction.\n"
            f"Quote: {quote_en}\n\n"
        )
        tag_list = tags.split()
        extended_tags = tag_list + ["#lofimusic", "#instrumental", "#focusmusic", "#relaxingvibes", "#ambient", "#calm", "#studymusic", "#deepwork"]
        final_tags = " ".join(list(dict.fromkeys(extended_tags)))
        up.write(f"[Tags]\n{final_tags}\n\n")

    # 영어 전용 프롬프트 파일
    prompt_file = os.path.join(folder_path, "prompts.txt")
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write("[Midjourney Prompt]\n")
        f.write(f"{mj_prompt}\n\n")
        f.write("[Runway Prompt]\n")
        f.write(f"{rw_prompt}\n\n")
        f.write("[Suno Prompts - 30]\n")
        f.write(f"Exclude Styles: {exclude}\n\n")
        for idx, prompt in enumerate(suno_prompts, 1):
            f.write(f"{idx:02d}. Style of Music: {prompt}\n")

    # 한글 설명 파일 분리 출력
    desc_path = os.path.join(folder_path, "프롬프트_설명.txt")
    with open(desc_path, 'w', encoding='utf-8') as desc:
        desc.write(f"[Quote Translation]\n{quote_kr}\n")
        desc.write("\n- 유튜브 설명란에 들어갈 명언 번역입니다.\n")
        desc.write("- Midjourney 프롬프트는 썸네일 이미지 생성에 사용됩니다.\n")
        desc.write("- Runway 프롬프트는 5초 루프 기반 배경 영상 설명입니다.\n")
        desc.write("- Suno 프롬프트는 30곡 자동 생성됩니다.\n")
