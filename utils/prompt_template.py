# prompt_template.py
# ✅ title / description / tags 부분만 트렌드 기반으로 개선됨
# ✅ 나머지 기능(프롬프트 생성, 파일 쓰기, suno 등)은 전혀 변경되지 않음

import os
import random
from utils.trend_keywords import get_trending_set

def build_prompt_file(channel, folder_path):
    trending = get_trending_set(channel)

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
    keywords = trending.get("keywords", [topic])
    concept = trending["concept"]
    styles = trending["styles"]
    exclude = trending["exclude"]
    tags = trending["tags"]
    mj_prompt = trending["mj_prompt"]
    rw_prompt = trending["rw_prompt"]

    # Suno 프롬프트 생성
    suno_prompts = []
    for _ in range(30):
        style = random.choice(styles)
        mood = random.choice(["calm", "gentle", "dreamy", "immersive", "emotional"])
        texture = random.choice(["mono reverb", "stereo spread", "lowpass filtered", "ambient pad background"])
        bpm = random.choice(["60BPM", "70BPM", "85BPM", "90BPM"])
        prompt = f"{style}, {bpm}, {texture}, designed to be {mood}"
        if len(prompt) <= 200:
            suno_prompts.append(prompt)

    # 업로드용 파일 출력
    upload_txt_path = os.path.join(folder_path, "upload_fields_for_api.txt")
    with open(upload_txt_path, 'w', encoding='utf-8') as up:

        main_topic = keywords[0]
        sub_keywords = keywords[1:5] if len(keywords) > 1 else ["relaxation", "calm focus", "mental clarity", "peaceful vibes"]
        tag_keywords = keywords[:5] if len(keywords) >= 1 else ["lofimusic", "relaxing", "calmmusic", "sleep", "focus"]

        title = random.choice([
            f"Let the sound of {main_topic} guide your flow",
            f"Lose yourself in the mood of {main_topic}",
            f"Focus deeply with this {main_topic} mix",
            f"Your moment of calm starts with {main_topic}"
        ])

        if channel == "studymooz":
            description_text = (
                f"Stay focused with this {main_topic} playlist.\n"
                f"It blends lo-fi, ambient textures, and soft beats for an ideal study environment.\n"
                f"Perfect for tasks like {', '.join(sub_keywords)} and more.\n"
                f"Use it for deep work, exam prep, or any time you need mental clarity.\n\n"
            )
        elif channel == "whisperlullaby":
            description_text = (
                f"Create a magical bedtime with this {main_topic} mix.\n"
                f"Featuring dreamy melodies and calming textures designed for {', '.join(sub_keywords)}.\n"
                f"Perfect for babies, toddlers, and peaceful sleep routines.\n"
                f"This playlist helps your little one drift off calmly.\n\n"
            )
        elif channel == "calmpet":
            description_text = (
                f"Ease your pet's mind with this {main_topic} playlist.\n"
                f"Ideal for times like {', '.join(sub_keywords)}, it helps pets stay calm and safe.\n"
                f"Perfect for anxiety relief, solo time, or recovery.\n"
                f"Give your furry friend the gift of peace.\n\n"
            )
        else:
            description_text = f"This relaxing playlist based on {main_topic} supports focus and calm.\n\n"

        base_tags = [f"#{kw.lower().replace(' ', '')}" for kw in tag_keywords]
        default_tags = ["#lofimusic", "#relaxing", "#focusmusic", "#deepwork", "#ambient"]
        final_tags = " ".join(list(dict.fromkeys(base_tags + default_tags)))

        up.write(f"[YouTube Title]\n{title}\n\n")
        up.write("[Description]\n")
        up.write(description_text)
        up.write(f"Quote: {quote_en}\n\n")
        up.write(f"[Tags]\n{final_tags}\n\n")

    # Midjourney, Runway, Suno 프롬프트 파일 출력
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