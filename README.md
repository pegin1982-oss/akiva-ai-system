akiva-ai-system/
│
├── app.py
├── ai_engine/
│   ├── classifier.py
│   └── nlp.py
│
├── data/
│   ├── train_data.json
│   └── logs.json
│
├── requirements.txt
└── README.md

# AI-система поддержки ООО "АКИВА"
 
## Описание
Проект разработан в рамках производственной практики.
 
Цель — внедрение искусственного интеллекта в бизнес-процессы компании.
 
## Функции
- обработка запросов пользователей
- автоматические ответы
- классификация обращений
- логирование
 
## Технологии
- Python
- Flask
- NLP (обработка текста)
 
## Запуск
 
pip install -r requirements.txt  
python app.py
 
## Пример запроса
 
POST /chat  
{
  "message": "привет"
}
 
## Результат
 
{
  "intent": "greeting",
  "response": "Здравствуйте!"
}
