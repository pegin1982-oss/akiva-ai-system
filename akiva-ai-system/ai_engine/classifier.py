import json
import os
from .nlp import normalize_text

class IntentClassifier:
    def __init__(self, data_path="data/train_data.json"):
        """Загружаем обучающие данные при инициализации"""
        self.data_path = data_path
        self.intents = self._load_data()

    def _load_data(self):
        """Загрузка intents из JSON-файла"""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Файл {self.data_path} не найден")
        with open(self.data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data["intents"]

    def classify(self, message):
        """
        Классификация сообщения: определяет intent по ключевым словам.
        Возвращает dict с intent и response.
        """
        normalized_msg = normalize_text(message)

        best_intent = None
        best_score = 0

        for intent_item in self.intents:
            patterns = intent_item["patterns"]
            score = 0
            # Подсчитываем, сколько шаблонных фраз входит в нормализованное сообщение
            for pattern in patterns:
                normalized_pattern = normalize_text(pattern)
                if normalized_pattern in normalized_msg:
                    score += 1
            # Если нашли хотя бы одно совпадение и это лучше предыдущего
            if score > best_score:
                best_score = score
                best_intent = intent_item

        if best_intent and best_score > 0:
            return {
                "intent": best_intent["intent"],
                "response": best_intent["response"]
            }
        else:
            # Ответ по умолчанию, если не распознали намерение
            return {
                "intent": "unknown",
                "response": "Извините, я не понял ваш запрос. Обратитесь к оператору."
            }
