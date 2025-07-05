# bot/bot.py
"""
Мини-бот Telegram: спрашивает симптомы, подбирает врача (через OpenAI),
бронит слот в API /appointments и подтверждает запись.

Файл демонстрационный ‒ не входит в основной сервис.
"""

from __future__ import annotations

import os
from typing import Final

import requests
from openai import OpenAI
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

API_URL: Final = "http://localhost:8000/appointments"
OPENAI_MODEL: Final = "gpt-4o-mini"
client = OpenAI()


def llm_specialty(symptoms: str) -> str:
    """LLM простым промптом выдаёт подходящую специализацию врача."""
    prompt = f"Which medical specialty should treat: {symptoms}?"
    resp = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content.strip()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Здравствуйте! Опишите ваши симптомы.")


async def handle_symptoms(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    symptoms = update.message.text or ""
    specialty = llm_specialty(symptoms)

    data = {
        "doctor_id": 1,
        "patient_name": update.effective_user.full_name,
        "start_time": "2030-01-01T09:00:00",
    }
    try:
        requests.post(API_URL, json=data, timeout=5)
        msg = f"Записал вас к {specialty} на 1 января 2030 в 09:00.\n" "Хорошего дня!"
    except requests.RequestException:
        msg = "Не удалось создать запись ‒ попробуйте позже."
    await update.message.reply_text(msg)


def main() -> None:
    token = os.getenv("TG_BOT_TOKEN")
    if not token:
        raise RuntimeError("TG_BOT_TOKEN не задан в переменных окружения")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_symptoms))
    app.run_polling()


if __name__ == "__main__":
    main()
