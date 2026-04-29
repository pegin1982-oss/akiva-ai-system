import re
import json
from pymorphy2 import MorphAnalyzer

# Инициализация морфологического анализатора (русский язык)
morph = MorphAnalyzer()

def normalize_text(text):
    """
    Приведение текста к нормальной форме (лемматизация).
    Удаляем знаки пунктуации, приводим к нижнему регистру.
    """
    # Приводим к нижнему регистру и удаляем всё, кроме букв и пробелов
    text = text.lower()
    words = re.findall(r'\b[а-яё]+\b', text)
    # Лемматизация каждого слова
    normalized_words = [morph.parse(word)[0].normal_form for word in words]
    return " ".join(normalized_words)
