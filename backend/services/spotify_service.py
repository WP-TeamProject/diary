import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_URL = "https://api.spotify.com/v1"


def _get_access_token():
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        print("[Spotify 에러] 환경변수에 API Key가 없습니다.")
        return None

    auth_string = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    try:
        res = requests.post(SPOTIFY_AUTH_URL, headers=headers, data=data, timeout=5)
        if res.status_code == 200:
            return res.json().get("access_token")
        else:
            print(f"[Spotify 인증 에러] {res.status_code}: {res.text}")
    except Exception as e:
        print(f"[Spotify 인증 예외] {e}")
    return None

# 감정에 맞는 음악 추천 1곡 가져오기
def get_recommendation_by_emotion(emotion_key):
    token = _get_access_token()
    if not token:
        return None

    # 감정별 Spotify 타겟 파라미터 매핑
    emotion_map = {
        "anger": {"seed_genres": "hard-rock,heavy-metal", "target_energy": 0.9, "target_valence": 0.2},
        "sadness": {"seed_genres": "acoustic,piano,rainy-day", "target_energy": 0.2, "target_valence": 0.2},
        "joy": {"seed_genres": "pop,happy,dance", "target_energy": 0.8, "target_valence": 0.9},
        "surprise": {"seed_genres": "electronic,synth-pop", "target_energy": 0.7, "target_valence": 0.6},
        "fear": {"seed_genres": "ambient,sleep", "target_energy": 0.1, "target_valence": 0.3},
        "disgust": {"seed_genres": "punk,grunge", "target_energy": 0.8, "target_valence": 0.3},
        "neutral": {"seed_genres": "lo-fi,study,chill", "target_energy": 0.4, "target_valence": 0.5}
    }

    # 기본값은 neutral
    params = emotion_map.get(emotion_key, emotion_map["neutral"])
    # 1곡만 추천받기 위해 limit=1 추가
    query_params = {
        "seed_genres": params["seed_genres"],
        "target_energy": params["target_energy"],
        "target_valence": params["target_valence"],
        "limit": 1
    }

    headers = {"Authorization": f"Bearer {token}"}

    try:
        res = requests.get(f"{SPOTIFY_API_URL}/recommendations", headers=headers, params=query_params, timeout=5)
        if res.status_code == 200:
            tracks = res.json().get("tracks", [])
            if tracks:
                track = tracks[0]
                return {
                    "title": track["name"],
                    "artist": track["artists"][0]["name"],
                    "image_url": track["album"]["images"][0]["url"] if track["album"]["images"] else "",
                    "preview_url": track["preview_url"], # 30초 미리듣기 (None일 수 있음)
                    "spotify_url": track["external_urls"]["spotify"]
                }
        else:
            print(f"[Spotify 검색 에러] {res.status_code}: {res.text}")
    except Exception as e:
        print(f"[Spotify 검색 예외] {e}")
    
    return None