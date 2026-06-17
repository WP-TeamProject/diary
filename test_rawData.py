# 원시 데이터 반환 테스트
import requests
import json
import os


API_URL = "https://router.huggingface.co/hf-inference/models/j-hartmann/emotion-english-distilroberta-base"
API_TOKEN = os.getenv("HF_API_TOKEN")

headers = {"Authorization": f"Bearer {API_TOKEN}"}

test_inputs = [
    "I am so happy that I passed the exam!", # 명백히 긍정적이고 기쁜 뉘앙스의 텍스트
    "I passed the exam, but I feel empty inside.", # 긍정적인 결과지만 공허하고 슬픈 뉘앙스가 섞인 텍스트
    "How could you do this to me?", # 분노 또는 배신감이 포함된 공격적인 뉘앙스의 텍스트
    "I guess it's okay.", # 감정이 크게 치우치지 않은 중립적인 뉘앙스의 텍스트
]


for text in test_inputs:
    payload = {"inputs": text}
    
    response = requests.post(API_URL, headers=headers, json=payload)
    
    result = response.json()
    
    print(f"입력 텍스트: {text}")
    print("전체 반환 데이터 (원시 형태):")
    
    print(json.dumps(result, indent=2))
    
    if isinstance(result, list) and len(result) > 0:
        
        sorted_emotions = sorted(result[0], key=lambda x: x['score'], reverse=True)
        
        top_1_emotion = sorted_emotions[0]['label']
        top_1_score = sorted_emotions[0]['score']
        
        top_2_emotion = sorted_emotions[1]['label']
        top_2_score = sorted_emotions[1]['score']
        
        print(f"분석 결과 -> 1위 감정: {top_1_emotion} ({top_1_score:.4f}), 2위 감정: {top_2_emotion} ({top_2_score:.4f})")
    
    print("-" * 50)