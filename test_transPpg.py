import requests
import os
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv("PAPAGO_CLIENT_ID")
CLIENT_SECRET = os.getenv("PAPAGO_CLIENT_SECRET")

# 파파고 NMT(신경망 기계 번역)
PAPAGO_URL = "https://papago.apigw.ntruss.com/nmt/v1/translation"

def transPpg_korean_to_english(korean_text):
    try: # 네트워크 오류 등 예외 상황으로 인해 프로그램이 다운되는 것을 막기 위해 try 블록을 엽니다.
        # 파파고 API가 인증을 위해 요구하는 헤더 정보
        headers = {
            "x-ncp-apigw-api-key-id": CLIENT_ID,
            "x-ncp-apigw-api-key": CLIENT_SECRET,
            "Content-Type": "application/json"
        }
        
        # 파파고 API가 요구하는 본문 데이터
        data = {
            "source": "ko", # source = ko 설정
            "target": "en", # target = en 설정
            "text": korean_text # 사용자가 입력한 실제 한글 텍스트를 변수로 전달.
        }
        
        # requests의 post 메서드를 사용하여 파파고 서버로 헤더와 데이터를 전송하고, 서버의 응답을 받음.
        response = requests.post(PAPAGO_URL, headers=headers, json=data)
        
        # 서버에서 반환한 HTTP 상태 코드가 200(정상 작동)인지 확인.
        if response.status_code == 200:
            result_json = response.json()
            translated_text = result_json["message"]["result"]["translatedText"]
            return translated_text
        else:
            # 200이 아니라면 에러 코드와 내용을 터미널에 출력.
            print(f"❌ 파파고 API 에러 [{response.status_code}]: {response.text}")
            return None
            
    except Exception as e:
        # 구체적인 에러 내용을 터미널에 출력.
        print(f"❌ 번역 모듈 에러: {e}")
        return None


if __name__ == "__main__":
    # 파파고의 번역 뉘앙스를 테스트하기 위한 샘플 한글 문장입니다.
    sample = "키보드 왜 안되는데 샤갈"

    print("========== 파파고 번역 API 단독 테스트 ==========")
    print(f"[입력] {sample}")
    print(f"[출력] {transPpg_korean_to_english(sample)}")