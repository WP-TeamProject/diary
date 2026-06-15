import requests
import os
from dotenv import load_dotenv

load_dotenv()
DEEPL_URL = "https://api-free.deepl.com/v2/translate"
DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")

def transDL_korean_to_english(korean_text):
    if not korean_text or korean_text.strip() == "":
        return None

    try: # 네트워크 에러나 응답 오류로 인한 프로그램 다운을 막기 위해 예외 처리 블록.
        # DeepL API가 요구하는 헤더 딕셔너리.
        headers = {
            "Authorization": f"DeepL-Auth-Key {DEEPL_AUTH_KEY}",
            "Content-Type": "application/json"
        }
        
        # 번역 요청에 필요한 필수 파라미터들을 딕셔너리로 구성.
        data = {
            # 번역할 텍스트를 리스트 형식 안에 담아서 보냄. (DeepL 규격)
            "text": [korean_text],
            # 도착 언어(Target Language)를 미국 영어(EN-US)로 지정.
            "target_lang": "EN-US"
        }
        
        response = requests.post(DEEPL_URL, headers=headers, json=data)
        
        # 서버에서 응답한 HTTP 상태 코드
        if response.status_code == 200:
            result_json = response.json()
            translated_text = result_json["translations"][0]["text"]
            return translated_text
        else:
            # 200이 아니라면 (키 오류 등) 에러 코드와 에러 메시지를 터미널에 출력.
            print(f"❌ DeepL API 에러 [{response.status_code}]: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 번역 모듈 에러: {e}")
        return None


if __name__ == "__main__":
    # DeepL의 번역 뉘앙스를 테스트하기 위한 샘플 한글 문장입니다.
    sample = "키보드 왜 안되는데 샤갈"
    
    print("========== DeepL 번역 API 단독 테스트 ==========")
    print(f"[입력] {sample}")
    print(f"[출력] {transDL_korean_to_english(sample)}")