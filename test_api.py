import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = "https://router.huggingface.co/hf-inference/models/j-hartmann/emotion-english-distilroberta-base"
API_TOKEN = os.getenv("HF_API_TOKEN")

HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

def analyze_emotion(english_text): # 영문 텍스트를 인자로 받아 AI 감정 분석 결과를 반환하는 함수.
    try: # 네트워크 에러나 일시적인 서버 오류로 프로그램이 종료되지 않도록 예외 처리 블록.
        # 허깅페이스 API 서버가 인식할 수 있도록, "inputs"라는 키에 영문 텍스트를 담아 페이로드(데이터) 딕셔너리를 만듭니다.
        payload = {"inputs": english_text}
        # 지정된 URL로 헤더와 JSON 페이로드를 담아 POST 방식으로 데이터를 전송하고, 서버의 응답을 response 변수에 받음
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        
        # 서버에서 받은 응답(JSON 형식의 문자열)을 파이썬에서 다루기 쉬운 리스트/딕셔너리 객체로 변환하여 변수에 저장
        raw_result = response.json()
        
        # [수정됨] 페르소나 매핑 과정 없이, 모델이 계산한 7가지 감정 확률 원시 데이터를 그대로 함수 호출자에게 반환
        return raw_result
            
    except Exception as e:
        # 발생한 에러의 상세 내용을 개발자가 볼 수 있도록 터미널에 출력
        print(f"API 통신 에러: {e}")
        return None


if __name__ == "__main__":
    # 데이터 통신이 잘 되는지 단독으로 테스트해 볼 영문 문장
    sample_text = "Why isn't the keyboard working fuck"

    print(f"[입력 텍스트] {sample_text}")
    
    result_data = analyze_emotion(sample_text)
    
    # 원시 데이터 확인
    print("[API 원시 데이터 결과]")
    print(result_data)