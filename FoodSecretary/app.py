from flask import Flask, request, render_template, redirect, url_for, session
import requests
import json
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a real secret key

# Fat Secret API 설정
TOKEN_URL = 'https://oauth.fatsecret.com/connect/token'
FOOD_SEARCH_URL = 'https://platform.fatsecret.com/rest/server.api'
FOOD_GET_URL = 'https://platform.fatsecret.com/rest/server.api'
RECIPE_SEARCH_URL = 'https://platform.fatsecret.com/rest/server.api'
RECIPE_GET_URL = 'https://platform.fatsecret.com/rest/server.api'

CLIENT_ID = '2c91f28e84ba4471820a106ea8abc0dc'  # 실제 Client ID로 변경
CLIENT_SECRET = '27f217b350a645fa99b6c91de4e5b800'  # 실제 Client Secret으로 변경

OLLAMA_URL = 'http://localhost:11434/api/generate'
OLLAMA_MODEL = 'llama3.1'

def get_access_token():
    response = requests.post(TOKEN_URL, data={
        'grant_type': 'client_credentials',
        'scope': 'basic',
    }, auth=(CLIENT_ID, CLIENT_SECRET))

    if response.status_code != 200:
        raise Exception("Failed to obtain access token")

    token_response = response.json()
    return token_response.get('access_token')

def calculate_bmr(gender, weight, height, age):
    """Harris-Benedict 공식을 사용하여 BMR(기초대사량)을 계산합니다."""
    if gender == '남':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    return bmr

def adjust_calories_for_goal(bmr, goal):
    """사용자의 목표에 따라 칼로리 섭취량을 조정합니다."""
    if goal == '체중 감량':
        return max(bmr - 400, 1200)  # 다이어트: BMR에서 400 칼로리 차감, 최소 1200kcal 유지
    elif goal == '근육 증가':
        return bmr + 300  # 린매스업: BMR에 300 칼로리 추가
    else:
        return bmr  # 유지

def search_foods(query):
    """음식 검색 API를 통해 키워드에 맞는 음식 리스트를 가져옵니다."""
    access_token = get_access_token()

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        'method': 'foods.search',
        'search_expression': query,
        'format': 'json'
    }
    try:
        response = requests.get(FOOD_SEARCH_URL, headers=headers, params=params)
        response.raise_for_status()
        foods_data = response.json()
        return foods_data.get('foods', {}).get('food', [])
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return []

def get_food_info(food_id):
    """음식 ID를 사용해 음식의 상세 정보를 가져옵니다."""
    access_token = get_access_token()

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        'method': 'food.get',
        'food_id': food_id,
        'format': 'json'
    }
    try:
        response = requests.get(FOOD_GET_URL, headers=headers, params=params)
        response.raise_for_status()
        food_data = response.json()
        return food_data.get('food')
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return None

def search_recipes(query):
    """레시피 검색 API를 통해 키워드에 맞는 레시피 리스트를 가져옵니다."""
    access_token = get_access_token()

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        'method': 'recipes.search',
        'search_expression': query,
        'format': 'json'
    }
    try:
        response = requests.get(RECIPE_SEARCH_URL, headers=headers, params=params)
        response.raise_for_status()
        recipes_data = response.json()
        return recipes_data.get('recipes', {}).get('recipe', [])
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return []

def get_recipe_info(recipe_id):
    """레시피 ID를 사용해 레시피의 상세 정보를 가져옵니다."""
    access_token = get_access_token()

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        'method': 'recipe.get',
        'recipe_id': recipe_id,
        'format': 'json'
    }
    try:
        response = requests.get(RECIPE_GET_URL, headers=headers, params=params)
        response.raise_for_status()
        recipe_data = response.json()
        return recipe_data.get('recipe')
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return None

def evaluate_diet(prompt):
    """Ollama 모델을 사용하여 식단 평가."""
    data = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "options": {
            "temperature": 0.7,
            "max_tokens": 200,
        }
    }

    response = requests.post(OLLAMA_URL, json=data)
    response.raise_for_status()

    responses = response.content.decode('utf-8').splitlines()
    final_response = ""

    for json_str in responses:
        json_data = json.loads(json_str)
        final_response += json_data.get("response", "")
        if json_data.get("done", False):
            break

    return final_response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    # 사용자 입력 수집
    age = int(request.form['age'])
    gender = request.form['gender']
    weight = float(request.form['weight'])
    height = float(request.form['height'])
    goal = request.form['goal']
    activity = request.form.get('activity', '')

    # 필수 항목이 모두 선택되었는지 확인
    if not all([age, gender, weight, height, goal, activity]):
        return render_template('result.html', recommendation="모든 항목을 선택해주세요.")

    # BMR 계산
    bmr = calculate_bmr(gender, weight, height, age)
    target_calories = adjust_calories_for_goal(bmr, goal)

    if activity == '적음':
        target_calories = target_calories * 1.2
    elif activity == '보통':
        target_calories = target_calories * 1.4
    elif activity == '많음':
        target_calories = target_calories * 1.7

    # 음식 및 레시피 키워드로 검색하기
    keywords = ["닭가슴살", "두부", "고구마", "계란", "샐러드"]  # 예시 음식 키워드 리스트
    recipe_keywords = ["닭가슴살 요리", "채소 볶음", "저칼로리 스낵"]  # 예시 레시피 키워드 리스트
    food_info = []
    recipe_info = []

    try:
        for keyword in keywords:
            searched_foods = search_foods(keyword)
            if searched_foods:
                food_id = searched_foods[0].get('food_id')  # 첫 번째 검색 결과의 food_id 사용
                food_detail = get_food_info(food_id)
                if food_detail:
                    food_info.append(food_detail)

        for keyword in recipe_keywords:
            searched_recipes = search_recipes(keyword)
            if searched_recipes:
                recipe_id = searched_recipes[0].get('recipe_id')  # 첫 번째 검색 결과의 recipe_id 사용
                recipe_detail = get_recipe_info(recipe_id)
                if recipe_detail:
                    recipe_info.append(recipe_detail)
    except Exception as e:
        return render_template('result.html', recommendation=f"음식 데이터를 가져오는 중 오류 발생: {e}")
    
    prompt = f"""
유저 정보: 성별 : {gender}, 나이 : {age}, 체중: {weight}, 키 : {height}, 목표 : {goal}, 하루 섭취 칼로리: {target_calories:.1f}.

사용자의 하루 목표 칼로리는 {target_calories:.1f} kcal입니다. 이 칼로리를 아래의 규칙에 따라 탄수화물, 단백질, 지방으로 나누어야 합니다:

- 운동을 하지 않는 경우: 탄수화물 50%, 단백질 30%, 지방 20%
- 운동을 하는 경우: 탄수화물 40%, 단백질 40%, 지방 20%

각각의 매크로영양소(탄수화물, 단백질, 지방)를 몇 g씩 섭취해야 하는지 계산하고, 이를 기준으로 아침, 점심, 저녁 식단을 작성해주세요. **모든 식사는 서로 다른 음식으로 구성되어야 하며, 동일한 음식이 반복되지 않도록 해주세요.** 식단은 한국 음식과 퓨전 음식을 포함하여 다양한 요리로 구성되어야 하며, 모든 음식과 레시피는 API에서 제공한 데이터를 기반으로 해야 합니다.

음식 데이터:
{food_info}

레시피 데이터:
{recipe_info}
아래에 있는 음식명이랑 레시피는 위에 나와 있는 음식 데이터랑 레시피 데이터를 활용해서 보여줘. 그냥 음식명1, 음식명2가 아니라. 레시피도 똑같이 레시피 데이터를 활용해서 보여줘야 해
아침:
- [음식명1]: [칼로리] kcal, [단백질] g 단백질, [탄수화물] g 탄수화물, [지방] g 지방
- [음식명2]: [칼로리] kcal, [단백질] g 단백질, [탄수화물] g 탄수화물, [지방] g 지방
- [레시피명1]: [칼로리] kcal, [단백질] g 단백질, [탄수화물] g 탄수화물, [지방] g 지방

점심:
- [음식명3]: [칼로리] kcal, [단백질] g 단백질, [탄수화물] g 탄수화물, [지방] g 지방
- [음식명4]: [칼로리] kcal, [단백질] g 단백질, [탄수화물] g 탄수화물, [지방] g 지방
- [레시피명2]: [칼로리] kcal, [단백질] g 단백질, [탄수화물] g 탄수화물, [지방] g 지방

저녁:
- [음식명5]: [칼로리] kcal, [단백질] g 단백질, [탄수화물] g 탄수화물, [지방] g 지방
- [음식명6]: [칼로리] kcal, [단백질] g 단백질, [탄수화물] g 탄수화물, [지방] g 지방
- [레시피명3]: [칼로리] kcal, [단백질] g 단백질, [탄수화물] g 탄수화물, [지방] g 지방

각 식단에서 제공된 칼로리 비율에 따라 탄수화물, 단백질, 지방의 양을 계산하고, 이를 한국어로 출력해주세요. **모든 식단은 서로 다른 음식과 레시피로 구성되어야 하며, 동일한 음식이 반복되지 않도록 해주세요.** 총 섭취 칼로리와 탄수화물, 단백질, 지방의 총량을 요약해서 보여주세요.
"""

    result = evaluate_diet(prompt)

    # 결과 출력
    return render_template('result.html', recommendation=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
