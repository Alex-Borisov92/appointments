<!-- docs/bot_scenario.md -->

# Telegram-бот c ИИ-подбором врача

## 1. Диалоговый сценарий

| Шаг | Сообщение бота | Действие пользователя | Внутренняя логика |
|-----|----------------|-----------------------|-------------------|
| 1   | «Здравствуйте! Опишите, что вас беспокоит, или назовите желаемого врача.» | «У меня сильное давление и головная боль.» | Бот передаёт текст в LLM-модель → получает вывод «кардиолог» |
| 2   | «Подойдёт врач-кардиолог. Когда удобно: завтра 15:00, послезавтра 11:00?» | «Завтра 15:00.» | Бот вызывает `GET /availability?doctor_id=5` или держит слоты локально. |
| 3   | — | — | Бот формирует `POST /appointments` с `{doctor_id: 5, patient_name, start_time}` |
| 4   | «Готово! Вы записаны к д-ру Иванову завтра в 15:00. Номер брони #123.» | — | При 409 бот переспрашивает и показывает новые слоты. |

## 2. Подбор врача — ИИ / ML

* **Библиотека / API:** OpenAI GPT-4o (`openai` Python SDK) либо open-source LLM через **LangChain**.  
* Промпт-шаблон:  
  *«Пациент жалуется: “{symptoms}”. Какой медицинский специалист ему нужен? Ответь одним словом.»*  
* Для начинающего прототипа можно заменить на словарь (`"давление" → "кардиолог"`) до подключения LLM.

## 3. Алгоритм бота

1. Получить текст симптомов.  
2. → LLM → получить специальность.  
3. Выбрать врача данной специальности с ближайшим свободным слотом (алгоритм round-robin или «первый свободный»).  
4. Спросить подтверждение у пациента.  
5. Отправить `POST /appointments`.  
6. Сообщить результат (успех / слот занят).

## 4. Права доступа и безопасность

* Бот хранит только имя пользователя Telegram → передаёт в `patient_name`.  
* Ключ к API хранится в переменной окружения `API_TOKEN`.  
* Запросы к FastAPI выполняются через HTTPS или через Docker-сеть, если бот работает внутри того же compose.

---

## 5. Stub-код бота (bot/bot.py)

```python
# bot/bot.py
import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

API_URL = os.getenv("APPOINTMENTS_API_URL", "http://api:8000")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

def llm_specialty(symptoms: str) -> str:
    """Наивный LLM-вызов; замените на реальный SDK."""
    import openai
    openai.api_key = OPENAI_KEY
    msg = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a medical triage assistant."},
            {"role": "user", "content": f"Patient symptoms: {symptoms}. Single word specialty?"},
        ],
    )
    return msg.choices[0].message.content.strip().lower()

async def start(update: Update, _):
    await update.message.reply_text("Здравствуйте! Опишите ваши симптомы.")

async def handle(update: Update, _):
    symptoms = update.message.text
    spec = llm_specialty(symptoms)
    # условно получаем врача ID=1 и слот
    slot = "2030-01-01T09:00:00"
    payload = {"doctor_id": 1, "patient_name": update.effective_user.full_name, "start_time": slot}
    resp = requests.post(f"{API_URL}/appointments", json=payload)
    if resp.status_code == 201:
        await update.message.reply_text(f"Записал к {spec} на {slot}.")
    else:
        await update.message.reply_text("Увы, время занято. Попробуйте другое.")

def main():
    app = ApplicationBuilder().token(os.getenv("TG_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.run_polling()

if __name__ == "__main__":
    main()
