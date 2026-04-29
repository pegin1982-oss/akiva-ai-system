from flask import Flask, request, jsonify
import json
import os
from datetime import datetime
from ai_engine.classifier import IntentClassifier

app = Flask(__name__)

# Загружаем классификатор
classifier = IntentClassifier()

# Путь к файлу логов
LOGS_PATH = "data/logs.json"

def log_interaction(user_message, intent, response):
    """Логирование каждого запроса и ответа в logs.json"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_message": user_message,
        "intent": intent,
        "response": response
    }

    # Загружаем существующие логи (если файл есть)
    logs = []
    if os.path.exists(LOGS_PATH):
        with open(LOGS_PATH, "r", encoding="utf-8") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []

    logs.append(log_entry)

    # Сохраняем обратно
    with open(LOGS_PATH, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

@app.route("/chat", methods=["POST"])
def chat():
    """
    Обработка POST-запроса с JSON {"message": "текст запроса"}
    Возвращает intent и ответ системы
    """
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Неверный запрос. Ожидается поле 'message'"}), 400

    user_message = data["message"].strip()
    if not user_message:
        return jsonify({"error": "Сообщение не может быть пустым"}), 400

    # Классифицируем запрос
    result = classifier.classify(user_message)
    intent = result["intent"]
    response = result["response"]

    # Логируем взаимодействие
    log_interaction(user_message, intent, response)

    return jsonify({
        "intent": intent,
        "response": response
    })

@app.route("/logs", methods=["GET"])
def get_logs():
    """Эндпоинт для просмотра логов (для администратора)"""
    if os.path.exists(LOGS_PATH):
        with open(LOGS_PATH, "r", encoding="utf-8") as f:
            logs = json.load(f)
        return jsonify(logs)
    else:
        return jsonify([])

if __name__ == "__main__":
    # Запуск Flask-сервера
    app.run(debug=True, host="0.0.0.0", port=5000)
