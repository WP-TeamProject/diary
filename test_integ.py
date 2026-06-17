""" !! papago 파일인지, deepl 파일인지 확인 !! """
# j-hartmann & translate API 통합 파이프라인 테스트

from test_transDeepL import transDL_korean_to_english
from test_transPpg import transPpg_korean_to_english
from test_api import analyze_emotion

def run_pipeline(korean_diary): 
    """한글 일기 -> 번역 -> AI 페르소나 발급의 전체 흐름을 제어"""
    print(f"\n[입력] 원본 텍스트: {korean_diary}")
    
    # 1단계: 번역 모듈 호출
    english_text = transDL_korean_to_english(korean_diary)
    if not english_text:
        print("❌ 번역 실패로 분석을 중단")
        return
    print(f"  -> [1단계] 번역 완료: {english_text}")
    
    # 2단계: 감정 분석 모듈 호출
    raw_result = analyze_emotion(english_text)
    if not raw_result:
        print("❌ API 통신 실패로 중단")
        return
        
    # 3단계: 최종 결과 출력
    print(f"  -> [2단계] AI 감정 분석 완료")
    print(f"  => [API 원시 데이터 결과]")
    print(f"  => 💬: {raw_result}")


if __name__ == "__main__":
    print("========== 파이프라인 통합 테스트 ==========")
    test_diaries = [
    "너 나빠"
    ]
    
    for diary in test_diaries:
        run_pipeline(diary)
        print("-" * 50)