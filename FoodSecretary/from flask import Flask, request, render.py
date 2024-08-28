from flask import Flask, request, render_template
import requests
import json
import pandas as pd

# Flask 애플리케이션 인스턴스 생성
app = Flask(__name__)

OLLAMA_URL = 'http://localhost:11434/api/generate'
OLLAMA_MODEL = 'llama3.1'
DATA_FILE = r'C:\Users\Administrator\Desktop\학교\방학 S-AI training\project\food dataset.csv'

def load_data():
    """CSV 파일에서 데이터를 읽어옵니다."""
    return pd.read_csv(DATA_FILE)

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
    age = request.form['age']
    weight = request.form['weight']
    height = request.form['height']
    goal = request.form['goal']

    # 데이터 기반 분석 및 추천
    data = load_data()
    prompt = f"User information: Age {age}, Weight {weight}, Height {height}, Goal: {goal}. Recommend a suitable diet."
    result = evaluate_diet(prompt)

    return render_template('result.html', recommendation=result)

if __name__ == '__main__':
    app.run(debug=True)  # Flask 애플리케이션 실행
