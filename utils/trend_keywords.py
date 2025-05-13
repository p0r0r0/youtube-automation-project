# trend_keywords.py
# ✅ 이 파일은 Google Trends를 통해 실시간 검색 트렌드를 기반으로 유튜브 영상 주제, 썸네일, 음악 스타일 등을 자동 생성합니다.
# - 중복 주기 제한 기능이 포함되어 있어, 최근 사용된 주제나 제목은 일정 기간(또는 최근 N개) 동안 재사용되지 않도록 설계되어 있습니다.
# - 중복 회피를 위해 used_titles.json과 generation_log.csv를 참조하여 새롭고 신선한 콘텐츠를 자동 생성합니다.

from pytrends.request import TrendReq
import random
from utils.title_manager import load_used_titles
import csv
from datetime import datetime, timedelta

pytrends = TrendReq(hl='en-US', tz=540)

# 최근 사용된 제목 확인 (최근 10개 기준)
def is_recently_used(topic):
    used = [t['title'] for t in load_used_titles()[-10:]]
    return topic in used

# 최근 N일 이내 사용된 topic인지 확인 (기록 기반)
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

# 채널별 기본 키워드 매핑 → pytrends 사용
def get_google_trend_keyword(channel):
    base_keywords = {
        "studymooz": "study music",
        "whisperlullaby": "baby lullaby",
        "calmpet": "music for dogs"
    }

    keyword = base_keywords.get(channel, "relaxing music")
    pytrends.build_payload([keyword], cat=0, timeframe='now 7-d', geo='KR')

    try:
        related = pytrends.related_queries()[keyword]['top']
        if related is not None and not related.empty:
            top_keywords = related['query'].tolist()
            for word in top_keywords:
                candidate = f"{word.title()} for Focus"
                if not is_recently_used(candidate) and not is_topic_recent_in_log(candidate):
                    return candidate
    except:
        pass

    return keyword.title()

# 기존 get_trending_set 그대로 유지됨 (중복 회피 적용된 topic 사용)
def get_trending_set(channel):
    topic = get_google_trend_keyword(channel)

    if channel == "studymooz":
        return {
            "topic": topic,
            "concept": f"이 음악은 집중이 필요한 순간을 위해 설계되었습니다: {topic}",
            "styles": ["lofi beat (vinyl) - 85BPM", "jazz piano - 88BPM", "ambient pad + rain fx"],
            "exclude": "vocals, edm, trap",
            "tags": "#study #lofi #focus #rainyday",
            "mj_prompt": f"A girl writing in a notebook under soft morning light, cozy room, rainy window, focused emotion --ar 16:9 --style raw --v 6",
            "mj_expl": "공책에 필기하는 장면 + 창밖 비 + 집중을 유도하는 색감 조합",
            "rw_prompt": "Pencil moves softly, raindrops on window, warm light flickers every 2s. Loop 5s.",
            "rw_expl": "펜의 움직임, 조명 깜빡임, 창밖 비를 5초 루프로 자연스럽게 연결",
            "quote_en": "Success is the sum of small efforts, repeated day in and day out.",
            "quote_kr": "성공은 매일 반복된 작은 노력의 합이다."
        }

    elif channel == "whisperlullaby":
        return {
            "topic": topic,
            "concept": f"이 음악은 아기의 편안한 수면을 돕기 위해 제작되었습니다: {topic}",
            "styles": ["music box - 60BPM", "harp lullaby", "womb sound + soft pad"],
            "exclude": "vocals, sharp treble, kick",
            "tags": "#lullaby #babysleep #calm #soothing",
            "mj_prompt": f"A baby sleeping peacefully, star mobile above crib, pastel color scheme, warm nightlight glow --ar 16:9 --style raw --v 6",
            "mj_expl": "파스텔 조명과 별 모빌, 아기 침대 속 포근함 강조",
            "rw_prompt": "Mobile rotates, soft chest breathing every 2s, lights pulse gently. Loop 5s.",
            "rw_expl": "숨쉬기와 조명 루프만으로 아기의 안정감 표현",
            "quote_en": "Let her sleep, for when she wakes, she will move mountains.",
            "quote_kr": "아이가 잠들게 하라. 깨어났을 땐 세상을 움직일 것이다."
        }

    elif channel == "calmpet":
        return {
            "topic": topic,
            "concept": f"이 음악은 반려동물이 혼자 있는 시간을 편안하게 느낄 수 있도록 설계되었습니다: {topic}",
            "styles": ["nature ambient + low drone", "fireplace + heartbeat", "rainy pads for dogs"],
            "exclude": "vocals, high synth, metal FX",
            "tags": "#pet #calm #dogmusic #thunderrelief",
            "mj_prompt": f"A dog curled up near rainy window, warm cozy room, dim light, relaxing mood --ar 16:9 --style raw --v 6",
            "mj_expl": "비 오는 방 안에서 안락한 반려견을 표현하여 안정감 부여",
            "rw_prompt": "Rain slides down window, dog's ear twitch, lamp dims and pulses every 2s. Loop 5s.",
            "rw_expl": "미세한 움직임을 5초 루프 안에 자연스럽게 녹임",
            "quote_en": "Until one has loved an animal, a part of one's soul remains unawakened.",
            "quote_kr": "동물을 사랑해보지 않은 사람은, 영혼의 일부가 잠들어 있는 것이다."
        }

    # fallback (예외 채널용)
    return {
        "topic": topic,
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
