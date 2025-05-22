import telebot
from flask import Flask
from threading import Thread
import os

API_TOKEN = os.getenv("API_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

bot = telebot.TeleBot(API_TOKEN)

# Flask-сервер для Render ping
app = Flask(__name__)

@app.route('/')
def home():
    return "I'm alive!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🇷🇺👋 Добро пожаловать!\n"
        "Вы можете анонимно отправить отзыв в виде текста, голосового сообщения или фотографии.\n\n"
        "🇺🇿👋 Xush kelibsiz!\n"
        "Matn, ovozli xabar yoki surat ko‘rinishida anonim fikr bildirishingiz mumkin.\n\n"
        "🇺🇸👋 Welcome!\n"
        "You can anonymously send feedback as text, voice message, or photo."
    )
    bot.send_message(message.chat.id, welcome_text)

# Текст
@bot.message_handler(func=lambda message: message.text and message.text != "/start")
def handle_text(message):
    reply_text = (
        "✅ Спасибо за ваш отзыв! Вы помогаете нам стать лучше.\n"
        "✅ Fikringiz uchun rahmat! Bizga yanada yaxshilanishga yordam beryapsiz.\n"
        "✅ Thank you for your feedback! You help us become better."
    )
    bot.send_message(message.chat.id, reply_text)
    feedback = f"📩 Новый текстовый отзыв от @{message.from_user.username or 'аноним'}:\n\n{message.text}"
    bot.send_message(ADMIN_CHAT_ID, feedback)

# Голос
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    reply_text = (
        "🎤 Спасибо за ваш голосовой отзыв!\n"
        "🎤 Ovozingiz uchun rahmat!\n"
        "🎤 Thank you for your voice message!"
    )
    bot.send_message(message.chat.id, reply_text)
    bot.forward_message(ADMIN_CHAT_ID, message.chat.id, message.message_id)

# Фото
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    reply_text = (
        "📷 Спасибо за фото! Мы обязательно его рассмотрим.\n"
        "📷 Surat uchun rahmat! Albatta ko‘rib chiqamiz.\n"
        "📷 Thank you for the photo! We will definitely review it."
    )
    bot.send_message(message.chat.id, reply_text)
    photo_file_id = message.photo[-1].file_id
    caption = f"🖼 Фотоотзыв от @{message.from_user.username or 'аноним'}"
    bot.send_photo(ADMIN_CHAT_ID, photo_file_id, caption=caption)

# Запуск
if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.polling()
