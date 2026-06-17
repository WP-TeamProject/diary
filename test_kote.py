"""KOTE 모델 테스트"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = "https://router.huggingface.co/hf-inference/models/Jinuuuu/KoELECTRA_fine_tunning_emotion"
API_TOKEN = os.getenv("HF_API_TOKEN")

HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

def analyze_emotion_korean(korean_text):
    try:
        payload = {"inputs": korean_text}
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        raw_result = response.json()
        return raw_result
    except Exception as e:
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    sample_text = "오늘 진짜 너무 행복했다"

    print(f"[입력 텍스트] {sample_text}")

    result_data = analyze_emotion_korean(sample_text)

    print("[API 원시 데이터 결과]")
    print(result_data)
