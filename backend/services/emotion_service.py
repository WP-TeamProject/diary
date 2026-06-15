import os
import requests

PAPAGO_URL = "https://papago.apigw.ntruss.com/nmt/v1/translation"
HF_API_URL = "https://router.huggingface.co/hf-inference/models/j-hartmann/emotion-english-distilroberta-base"

SINGLE_EMOTION_RESPONSES = {
    'anger':   "화 삭히지 말고 수 틀리면 다 끝내버려 ㅋㅋ",
    'sadness': "내가 더 슬픈 얘기 해줄게",
    'joy':     "축하한다 좋으니깐 내일도 글 써줘 ~❤️",
    'surprise':"나도 너 글 보고 많이 놀랐어",
    'fear':    '"용기란 두려움이 없는 것이 아니라, 두려움을 이겨내는 것이다."— 넬슨 만델라',
    'disgust': "안 보면 그만이야~",
    'neutral': "무난하다.",
}

# 감정 두 개인 경우 (순서 무관, frozenset 키)
TWO_EMOTION_RESPONSES = {
    frozenset({'sadness', 'anger'}):    "눈물을 흘리며 씨를 뿌리는 자는 기쁨으로 거두리로다",
    frozenset({'joy', 'anger'}):        "좋은 일인데 왜 이렇게 화가 나 있지 아무튼 축하한다!! 좋으니까 내일도 글 써줘~ 안 쓰면 찾아간다❤️",
    frozenset({'joy', 'sadness'}):      "슬픔 ㅠㅠ",
    frozenset({'surprise', 'anger'}):   "진짜 어이가 없네,, 내용 좀 더 써봐",
    frozenset({'surprise', 'sadness'}): "시간이 해결해 주겠지...",
    frozenset({'surprise', 'joy'}):     "ㅁㅊ. 이런건 남들한테 숨겨라 세상엔 믿을 건 가족밖에 없다",
    frozenset({'fear', 'anger'}):       "이 놈 이거 무서운 놈이네. 조심해라 너는",
    frozenset({'fear', 'sadness'}):     "안 그래도 슬픈데 무섭기까지 하네...",
    frozenset({'fear', 'joy'}):         "잘됐다 근데 떨어지는 낙엽도 조심해",
    frozenset({'fear', 'surprise'}):    "내 무습다 ...",
    frozenset({'disgust', 'anger'}):    "싸따 내려라. 괜찮다 이거는",
    frozenset({'disgust', 'sadness'}):  "세번 참으면 호구다",
    frozenset({'disgust', 'joy'}):      "너무 맛있어서 봤더니 귀뚜라미 먹은 그런 느낌이겠다",
    frozenset({'disgust', 'surprise'}): "불쾌하다.",
    frozenset({'disgust', 'fear'}):     "어려운 길은 길이 아니래",
    frozenset({'neutral', 'anger'}):    "가는 말이 고우면 알본다. (ㅅㅂ)",
    frozenset({'neutral', 'sadness'}):  "하루가 참 무난하긴 한데 왜 이렇게 마음 한구석이 쓸쓸하죠? 연애하세요.",
    frozenset({'neutral', 'joy'}):      "평온하게 좋은게 최고야 지금이 딱이구나",
    frozenset({'neutral', 'surprise'}): "이야 이거 좀 놀라운데 막막막 그정돈 아니네 ~",
    frozenset({'neutral', 'fear'}):     "늦었다고 생각할 때는 늦은거야~ 안해도 돼!!!",
    frozenset({'neutral', 'disgust'}):  "세상은 넓고 할 일은 많지 않다",
}

FALLBACK = {"emotions": ["neutral"], "response": SINGLE_EMOTION_RESPONSES["neutral"]}


def _translate_to_english(korean_text):
    headers = {
        "x-ncp-apigw-api-key-id": os.getenv("PAPAGO_CLIENT_ID"),
        "x-ncp-apigw-api-key":    os.getenv("PAPAGO_CLIENT_SECRET"),
        "Content-Type": "application/json"
    }
    data = {"source": "ko", "target": "en", "text": korean_text}
    try:
        res = requests.post(PAPAGO_URL, headers=headers, json=data, timeout=5)
        if res.status_code == 200:
            return res.json()["message"]["result"]["translatedText"]
        print(f"[번역 에러] {res.status_code}: {res.text}")
    except Exception as e:
        print(f"[번역 예외] {e}")
    return None


def _analyze_with_hf(english_text):
    headers = {"Authorization": f"Bearer {os.getenv('HF_API_TOKEN')}"}
    try:
        res = requests.post(HF_API_URL, headers=headers, json={"inputs": english_text}, timeout=10)
        if res.status_code == 200:
            result = res.json()
            candidates = result[0] if isinstance(result[0], list) else result
            return sorted(candidates, key=lambda x: x['score'], reverse=True)
        print(f"[HF 에러] {res.status_code}: {res.text}")
    except Exception as e:
        print(f"[HF 예외] {e}")
    return None


def analyze_emotion(content):
    english_text = _translate_to_english(content)
    if not english_text:
        return FALLBACK

    candidates = _analyze_with_hf(english_text)
    if not candidates:
        return FALLBACK

    top_label = candidates[0]['label'].lower()
    top_score = candidates[0]['score']

    # 두 번째 감정이 0.2 이상이고 최고 감정이 0.75 이상이면 두 개 출력
    if top_score >= 0.75 and len(candidates) > 1:
        second_label = candidates[1]['label'].lower()
        second_score = candidates[1]['score']
        if second_score >= 0.2:
            pair = frozenset({top_label, second_label})
            response = TWO_EMOTION_RESPONSES.get(
                pair, SINGLE_EMOTION_RESPONSES.get(top_label, SINGLE_EMOTION_RESPONSES["neutral"])
            )
            return {"emotions": [top_label, second_label], "response": response}

    response = SINGLE_EMOTION_RESPONSES.get(top_label, SINGLE_EMOTION_RESPONSES["neutral"])
    return {"emotions": [top_label], "response": response}
