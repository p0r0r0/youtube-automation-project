# trend_keywords.py
# ✅ 각 채널별 트렌드 기반 프롬프트 생성기
# ✅ 트렌드 키워드가 부족할 경우 유사 인기 채널의 대표 키워드로 보완하여 SEO 최적화 강화

from pytrends.request import TrendReq
import random
from utils.title_manager import load_used_titles
import csv
from datetime import datetime, timedelta

pytrends = TrendReq(hl='en-US', tz=540)

def is_recently_used(topic):
    used = [t['title'] for t in load_used_titles()[-10:]]
    return topic in used

def is_topic_recent_in_log(topic, days=14):
    try:
        with open('logs/generation_log.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            cutoff_date = datetime.now() - timedelta(days=days)
            for row in reader:
                if row['topic'] == topic:
                    created = datetime.strptime(row['date'], "%Y-%m-%d")
                    if created > cutoff_date:
                        return True
    except:
        pass
    return False

def get_google_trend_keyword(channel):
    base_keywords = {
        "studymooz": "study music",
        "whisperlullaby": "baby lullaby",
        "calmpet": "music for dogs"
    }

    fallback_keywords = {
        "studymooz": [
            "Exam Music", "Lo-fi for Studying", "Deep Work Focus", "Study With Me", "Chillhop"
        ],
        "whisperlullaby": [
            "Baby Sleep Music", "Soft Lullabies", "Newborn Calm", "Crib Soothing", "Nap Time Sound"
        ],
        "calmpet": [
            "Music for Dogs", "Dog Relaxation", "Pet Anxiety Relief", "Calming Sounds for Pets", "Thunder Music"
        ]
    }

    keyword = base_keywords.get(channel, "relaxing music")
    pytrends.build_payload([keyword], cat=0, timeframe='now 7-d', geo='KR')

    try:
        related = pytrends.related_queries()[keyword]['top']
        if related is not None and not related.empty:
            top_keywords = related['query'].tolist()
            keywords = [keyword.title()] + [kw.title() for kw in top_keywords[:9]]
            if len(keywords) < 5:
                extra = fallback_keywords.get(channel, [])
                keywords += [kw for kw in extra if kw not in keywords][:5 - len(keywords)]
            return keywords
    except:
        pass

    return [keyword.title()] + fallback_keywords.get(channel, [])[:4]

def get_trending_set(channel):
    keywords = get_google_trend_keyword(channel)
    topic = keywords[0]

    ethnicity = random.choice(["Korean", "Japanese", "European", "Southeast Asian"])
    hairstyle = random.choice(["long straight black hair", "short brown bob", "wavy chestnut hair", "ponytail with side bangs"])
    face = random.choice(["idol-like visuals", "delicate facial features", "glamorous beauty", "celebrity-style makeup"])
    outfit = random.choice(["knit sweater", "white blouse", "school uniform", "pastel cardigan"])
    mood = random.choice(["dreamy", "focused", "cheerful", "peaceful"])

    mj_prompt_text = (
        f"A stunningly beautiful {ethnicity} girl with {hairstyle}, {face}, wearing a {outfit}, "
        f"writing in a notebook with a pen, cozy study desk, soft sunlight, {mood} expression, "
        f"cinematic lighting, ultra-realistic --ar 16:9 --style raw"
    )

    rw_prompt_text = (
        "She writes gently with her pen, her eyes blink subtly, hair moves softly, "
        "sunlight glows on her face, emotional cinematic loop. Loop 5s."
    )

    if channel == "studymooz":
        return {
            "topic": topic,
            "keywords": keywords,
            "concept": f"이 음악은 집중이 필요한 순간을 위해 설계되었습니다: {topic}",
            "styles": [
                "lofi beat (vinyl) - 85BPM",
                "jazz piano - 88BPM",
                "ambient textures + soft strings - 80BPM"
            ],
            "exclude": "vocals, edm, trap",
            "tags": "#study #lofi #focus #cozy",
            "mj_prompt": mj_prompt_text,
            "mj_expl": "연예인급 여자 캐릭터가 공책에 글을 쓰는 감성 썸네일",
            "rw_prompt": rw_prompt_text,
            "rw_expl": "눈 깜빡임, 머리카락 흔들림 중심의 감성 루프",
            "quote_en": "Success is the sum of small efforts, repeated day in and day out.",
            "quote_kr": "성공은 매일 반복된 작은 노력의 합이다."
        }

    elif channel == "whisperlullaby":
        return {
            "topic": topic,
            "keywords": keywords,
            "concept": f"이 음악은 아기의 편안한 수면을 돕기 위해 제작되었습니다: {topic}",
            "styles": [
                "soft music box - 60BPM",
                "gentle harp melody",
                "warm ambient pad + lullaby chime"
            ],
            "exclude": "vocals, sharp treble, kick, womb",
            "tags": "#lullaby #babysleep #calm #soothing",
            "mj_prompt": "a smiling cartoon baby playing in a fantastical rainbow nursery, wearing a colorful onesie, surrounded by glowing toys like whales, bunnies, star-shaped balloons, floating moons and clouds, soft sparkling pastel lights, dreamy magical atmosphere, highly detailed ghibli-style fantasy illustration with glitter and shimmer effects --ar 16:9 --style raw",
            "mj_expl": "아기들이 좋아할만한 동화적 분위기의 밝고 귀여운 상상 속 유치원",
            "rw_prompt": "Cartoon baby claps happily, colorful whale plush floats in the air, star mobiles sparkle and twinkle, glowing pastel rainbow lights shift gently, fantasy dream nursery animation. Loop 5s.",
            "rw_expl": "아기의 동작, 인형, 모빌, 빛이 부드럽게 루프처럼 연출되는 귀여운 환상 장면",
            "quote_en": "Let her sleep, for when she wakes, she will move mountains.",
            "quote_kr": "아이가 잠들게 하라. 깨어났을 땐 세상을 움직일 것이다."
        }

    elif channel == "calmpet":
        return {
            "topic": topic,
            "keywords": keywords,
            "concept": f"이 음악은 반려동물이 혼자 있는 시간을 편안하게 느낄 수 있도록 설계되었습니다: {topic}",
            "styles": [
                "fireplace crackling + soft heartbeat",
                "calming bell chime + soft piano",
                "rainy day piano + soft textures"
            ],
            "exclude": "vocals, high synth, metal FX, low drone",
            "tags": "#pet #calm #dogmusic #thunderrelief",
            "mj_prompt": "A cute puppy and kitten sitting together happily on a sunny windowsill, cozy colorful room, warm soft lighting, ghibli-style happiness --ar 16:9 --style raw",
            "mj_expl": "햇살 아래 앉아있는 귀여운 강아지와 고양이의 행복한 모습 표현",
            "rw_prompt": "Puppy wags its tail slowly, kitten blinks eyes with soft head tilt, sunlight sparkles on fur, gentle movements in a warm cozy room. Loop 5s.",
            "rw_expl": "꼬리 흔들기와 눈 깜빡임 중심의 감성 루프 연출",
            "quote_en": "Until one has loved an animal, a part of one's soul remains unawakened.",
            "quote_kr": "동물을 사랑해보지 않은 사람은, 영혼의 일부가 잠들어 있는 것이다."
        }

    return {
        "topic": topic,
        "keywords": keywords,
        "concept": f"실시간 트렌드를 기반으로 생성된 주제입니다: {topic}",
        "styles": ["ambient piano"],
        "exclude": "vocals",
        "tags": "#music",
        "mj_prompt": f"An aesthetic background for '{topic}'",
        "mj_expl": f"'{topic}' 감성에 맞는 무드 썸네일",
        "rw_prompt": f"Loop video concept for '{topic}'",
        "rw_expl": f"5초 루프 기반 무드 영상",
        "quote_en": "Peace is always beautiful.",
        "quote_kr": "평화는 언제나 아름답다."
    }
