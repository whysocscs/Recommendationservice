## Personal Recommendation Meal Service

## 목적
운동을 시작하는 사람에게 각자의 체형과 취향에 맞게 음식을 추천 할 수 있는 프로그램을 만들자.

## 개발 기간
2024.08.28 ~ 2024.08.30

인공지능 기반 상명 AI training

아이디어 노트 작성

발표 평가

## 개발자소개

유현영 

김기원

이상호

## 기술 스택
Ollama(Python)

Front-end(Not yet decided)

## 프로젝트 아키텍쳐

![image](https://github.com/user-attachments/assets/c15ceca1-7aab-4338-8ab5-cab300bedd9c)

## 페이지별 기능

## [초기화면]
+사용자의 인적 정보를 받아들 일 수 있는 ui를 설정하였습니다.
+그리고 바로 사용자의 bmi수치를 확인 할 수 있도록 수정하였습니다.
![image](https://github.com/user-attachments/assets/1c7815c2-a512-4701-ac96-dace796b88b0)

## [결과 화면]
+ 사용자의 인적 정보를 바탕으로 사용자에 최적화 된 식단을 추천합니다.
+ 사용자가 먹기 싫은 음식과 좋아하는 음식을 바탕으로 재추천을 받을 수 있습니다.

![image](https://github.com/user-attachments/assets/98330f2e-15b2-4a36-bc5d-cf9643cd58dd )


## 주요 기능
+ 사용자의 인적 정보 수집
    + 사용자의 키, 몸무게, 목표, 성별, 활동량을 입력 받아서 Ollama Ai에 입력한다.
+ 식단 검색
  + Ollama ai를 활영하여 사용자의 인적 정보 수집을 바탕으로 어떤 식단을 먹어야 하는지 파악 후 사용자에게 전달한다.
  + 사용자가 식단이 마음에 들지 않을 경우 좋아하는 식품과 싫어하는 식품을 다시 입력 받아 식단을 다시 받을 수 있게 한다.



## 개선 목표
+ Api가 개인의 ip로 설정이 되어있어서 이것을 하나의 api 서버를 통해 다른 사용자들도 ip설정을 하지 않고 사용할 수 있도록 수정
+ ollama Ai의 답변에 필요없는 내용이 포함되어 있을 때가 있고 ollama Ai의 답변 속도가 느려 다른 ai api를 사용하기
+ 골격근량과 체지방률을 사용하여 더 정확한 식단을 내놓을 수 있도록 수정
+ 처음 사이트에서 BMI 표의 x축이 움직이지 않아 표를 수정
