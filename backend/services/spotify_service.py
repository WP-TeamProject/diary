import os
import requests
import base64
import random
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com/v1"

def _get_access_token():
    if not CLIENT_ID or not CLIENT_SECRET:
        print("🚨 [Spotify] API 키가 없습니다. .env 파일을 확인하세요.")
        return None

    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    try:
        res = requests.post(SPOTIFY_TOKEN_URL, headers=headers, data=data, timeout=5)
        
        if res.status_code == 200:
            token = res.json().get("access_token")
            if not token:
                print(f"🚨 [Spotify] 통신은 성공했으나 토큰이 없습니다. 응답: {res.text}")
            return token
        else:
            print(f"🚨 [Spotify] 토큰 발급 에러 ({res.status_code}): {res.text}")
    except Exception as e:
        print(f"🚨 [Spotify] 토큰 통신 예외 발생: {e}")
        
    return None

def get_recommendation_by_emotion(emotion_key):
    error_fallback = {
        "title": "🎵 음악 정보를 불러오지 못했습니다",
        "artist": "서버 통신 지연 (새로고침을 해보세요)",
        "image_url": "https://developer.spotify.com/assets/branding-guidelines/icon3@2x.png",
        "preview_url": None,
        "spotify_url": "#"
    }

    token = _get_access_token()
    if not token:
        print("🚨 [Spotify] 엑세스 토큰이 없어 검색을 중단하고 기본 UI 카드를 반환합니다.")
        return error_fallback

    emotion_query_map = {
        "anger": "hard rock heavy metal",
        "sadness": "sad acoustic piano",
        "joy": "happy pop dance",
        "surprise": "exciting synth pop electronic",
        "fear": "ambient sleep relaxing",
        "disgust": "punk grunge dark",
        "neutral": "chill lofi study"
    }

    search_query = emotion_query_map.get(emotion_key, emotion_query_map["neutral"])

    query_params = {
        "q": search_query,
        "type": "track",
        "limit": 10,
        "market": "KR"
    }

    headers = {"Authorization": f"Bearer {token}"}

    try:
        res = requests.get(f"{SPOTIFY_API_BASE_URL}/search", headers=headers, params=query_params, timeout=5)

        if res.status_code == 200:
            tracks = res.json().get("tracks", {}).get("items", [])
            
            if tracks:
                track = random.choice(tracks)
                return {
                    "title": track.get("name", "알 수 없는 제목"),
                    "artist": track.get("artists", [{"name": "알 수 없는 아티스트"}])[0].get("name"),
                    "image_url": track.get("album", {}).get("images", [{"url": error_fallback["image_url"]}])[0].get("url"),
                    "preview_url": track.get("preview_url"),
                    "spotify_url": track.get("external_urls", {}).get("spotify", "#")
                }
            else:
                print(f"🚨 [Spotify] '{search_query}'에 대한 검색 결과가 0건입니다.")
        else:
            print(f"🚨 [Spotify] 검색 요청 에러 ({res.status_code}): {res.text}")

    except Exception as e:
        print(f"🚨 [Spotify] 검색 통신 중 예외 발생: {e}")

    return error_fallback