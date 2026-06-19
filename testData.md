### **Case 1. 극대노 + 신조어 (팀플 잠수 빌런, 댕빡친다)**

- **[Papago]** 번역: "...Team diving villains make me stay uping mad" (문법 파괴/직역)
- 감정: 😡 **Anger (0.57)** > 😲 Surprise
- **[DeepL]** 번역: "...villain who's ghosting the group project. This is so frustrating, lol." (완벽한 원어민 슬랭 의역)
- 감정: 😢 **Sadness (0.37)** > 😐 Neutral (0.23)
- 💡 **분석:** 번역 품질은 'ghosting(잠수)'을 정확히 짚어낸 DeepL의 압승입니다. 하지만 감정 모델은 DeepL의 고급 표현("frustrating, lol")을 분노가 아닌 '체념/슬픔(Sadness)'으로 오해했습니다. 반면 파파고는 문법이 틀린 "mad"라는 1차원적 단어를 던져서 오히려 감정 모델이 Anger를 쉽게 잡았습니다.

### **Case 2. 비꼬기 (과장님 아이디어 스틸 ^^ 참 재밌다 하하하)**

- **[Papago]** 번역: "...Social life is really fun hahaha"
- 감정: 😄 **Joy (0.94)**
- **[DeepL]** 번역: "...Working life is really fun, haha"
- 감정: 😄 **Joy (0.95)**
- 💡 **분석:** **두 파이프라인 모두의 완벽한 실패이자 한계점**입니다. 번역기들은 문자 그대로 "fun(재밌다)", "haha"로 번역했고, 감정 모델 역시 이를 '비꼬는 분노(Anger)'가 아닌 '순수한 기쁨(Joy)'으로 100% 오해했습니다. (이건 번역기의 잘못이라기보단 텍스트 기반 감정 AI의 태생적 한계입니다.)

### **Case 3. 깊은 우울 (다 부질없는 것 같아. 내일이 무섭다)**

- **[Papago]** 번역: "I think it's all useless... scared that tomorrow will come"
- 감정: 😨 **Fear (0.98)**
- **[DeepL]** 번역: "It all just feels so pointless... I’m so scared of tomorrow coming."
- 감정: 😨 **Fear (0.76)** > 😢 Sadness (0.18)
- 💡 **분석:** 두 번역기 모두 무난하게 번역했습니다. DeepL은 "pointless"라는 단어를 써서 2위 감정으로 Sadness(슬픔)를 꽤 높게 잡아내며 뉘앙스를 조금 더 살렸습니다.

### **Case 4. 극강의 기쁨 (미쳤다!! 티켓팅 드디어 성공함 ㅠㅠ)**

- **[Papago]** 번역: "It's crazy!... ticket is finally succ(essful)"
- 감정: 😄 **Joy (0.67)** > 😲 Surprise (0.28)
- **[DeepL]** 번역: "I can't believe it!! ... T_T"
- 감정: 😲 **Surprise (0.91)** > 😄 Joy (0.05)
- 💡 **분석:** 파파고는 "성공(success)"을 직역해 기쁨을 이끌어냈습니다. DeepL은 한국인의 "미쳤다!!"를 "I can't believe it(믿을 수 없어)"으로 초월 번역했는데, 감정 모델이 이를 '경악/놀람(Surprise)'으로 압도적으로 분류해 버렸습니다.

### **Case 5. 당혹/절망 (액정 바사삭됨... 알바비 날아감)**

- **[Papago]** 번역: "...screen is crispy... I'm going to (lose) pay."
- 감정: 😲 **Surprise (0.62)** > 😢 Sadness (0.19)
- *[DeepL]**번역: "...screen shattered... I'm freaking out..."
- 감정: 😲 **Surprise (0.72)** > 😢 Sadness (0.10)
- 💡 **분석:** 파파고의 "바사삭 -> crispy(바삭바삭한)" 번역은 치명적인 오역입니다. 반면 DeepL은 "shattered(박살난)", "freaking out(멘탈 나간)"으로 완벽하게 번역했고, 둘 다 놀람/당혹(Surprise)으로 잘 매핑되었습니다.

### **Case 6. 불안 (면접, 심장 튀어나올듯, 청심환 ㄷㄷ)**

- **[Papago]** 번역: "...It's gsimhwan(청심환 영문표기)."
- 감정: 😢 **Sadness (0.62)** > 😨 Fear (0.29)
- **[DeepL]** 번역: "...calming pill isn't helping... 😱😱😱"
- 감정: 😢 **Sadness (0.53)** > 😨 Fear (0.33)
- 💡 **분석:** 고유명사인 '청심환'을 DeepL이 'calming pill(신경 안정제)'로 의역해 낸 놀라운 결과입니다. 특이한 점은, 영어권에서 심장이 튀어나올 것 같고 약이 안 듣는다는 상황을 감정 모델이 두려움(Fear)보다 슬픔/절망(Sadness)으로 먼저 인지한다는 점입니다.

### **Case 7. 혐오 (땀 냄새 진짜 토할 뻔. 눈치 챙겨)**

- **[Papago]** 번역: "...almost threw up... my manners..."
- 감정: 🤢 **Disgust (0.97)**
- **[DeepL]** 번역: "...almost made me throw up... Ugh, please be more considerate."
- 감정: 🤢 **Disgust (0.94)**
- 💡 **분석:** 두 파이프라인 모두 완벽하게 혐오(Disgust)를 잡아냈습니다. 번역의 자연스러움은 "Ugh(아오)", "considerate(배려하는/눈치 챙기는)"를 쓴 DeepL이 압도적입니다.

### **Case 8. 복합 감정 (폭망... 오늘은 울고 내일부터 파이팅)**

- **[Papago]** 번역: "...let's cry today and cheer up from tomorrow"
- 감정: 😢 **Sadness (0.49)** > 😄 Joy (0.28)
- **[DeepL]** 번역: "...total disaster... I'll give it my all again."
- 감정: 😐 **Neutral (0.44)** > 😢 Sadness (0.27)
- 💡 **분석:** 긍정과 부정이 섞인 문장입니다. 감정 모델은 DeepL의 번역을 읽고 감정이 상쇄되었다고 판단해 중립(Neutral)을 던졌습니다. 가장 판단하기 어려운 케이스입니다.

### **Case 9. 평온 (따뜻한 라떼 한 잔. 노래 좋고 여유롭다)**

- **[Papago]** 번역: "...it's been a while I was relaxed"
- 감정: 😄 **Joy (0.88)** > 😐 Neutral (0.03)
- **[DeepL]** 번역: "...it’s been a while since I’ve felt this relaxed."
- 감정: 😄 **Joy (0.94)** > 😐 Neutral (0.02)
- 💡 **분석:** AI 감정 모델은 보통 '평화/여유(Relaxed)'를 중립이 아닌 기쁨(Joy)으로 강하게 맵핑하는 경향이 있다는 것을 보여주는 데이터입니다. (추후 페르소나 매핑 시 참고할 부분입니다.)

### **Case 10. 감탄 (와 씨 이거 대체 뭐임?? 대박 ㅋㅋㅋㅋ)**

- **[Papago]** 번역: "Wow, what the hell is this?? Awesome. LOL"
- 감정: 😲 **Surprise (0.95)**
- **[DeepL]** 번역: "Whoa, what the heck is this?? This is insane lol"
- 감정: **Disgust (0.40)** > Surprise (0.35)
- 💡 **분석:** DeepL의 번역("heck", "insane")은 완벽한 인터넷 슬랭입니다. 하지만 `j-hartmann` 모델은 "heck(씨/망할)"이나 "insane(미친)" 같은 거친 단어가 들어가면 부정적 감정인 역겨움(Disgust)이나 분노(Anger)로 오인하는 경향이 강하게 나타났습니다.