import os
import telebot
from telebot import types
from flask import Flask, request
from dotenv import load_dotenv
import time

# .env fayldan o'zgaruvchilarni yuklash
load_dotenv()

# Bot tokeni (Render'da environment variable sifatida saqlanadi)
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Kanal username
CHANNEL_URL = "https://t.me/+LTnRUFYhvB0zODcy"

# Flask server yaratish
server = Flask(__name__)

# Botni yaratish
bot = telebot.TeleBot(BOT_TOKEN, parse_mode='HTML')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Start komandasi uchun handler"""
    
    # Inline klaviatura yaratish
    markup = types.InlineKeyboardMarkup()
    
    # URL tugma qo'shish
    btn = types.InlineKeyboardButton(
        text="Kanalga qo'shilish", 
        url=CHANNEL_URL
    )
    markup.add(btn)
    
    # Xabar yuborish
    bot.reply_to(
        message,
        "<blockquote><b>Naruto Animesini ko'rishni hohlasangiz unda pastdagi tugmasni bosing va kanalga qoshiling</b></blockquote>"
        ,
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    """Boshqa barcha xabarlar uchun handler"""
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(
        text="Kanalga qo'shilish", 
        url=CHANNEL_URL
    )
    markup.add(btn)
    
    bot.reply_to(
        message,
        "Bot faqat /start komandasi bilan ishlaydi.\n\nBizning asosiy kanalimizga qo'shiling",
        reply_markup=markup
    )

# Webhook uchun endpoint
@server.route('/' + BOT_TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    time.sleep(1)
    # Render'da WEBHOOK_URL environment variable sifatida saqlanadi
    bot.set_webhook(url=os.getenv('WEBHOOK_URL') + BOT_TOKEN)
    return "Bot ishga tushdi!", 200

# Lokal rivojlantirish uchun polling
if __name__ == "__main__":
    # Agar lokalda ishlatilsa, polling orqali
    if os.getenv('ENVIRONMENT') == 'local':
        print("Bot polling rejimida ishga tushdi...")
        bot.remove_webhook()
        bot.polling(none_stop=True)
    else:
        # Render'da webhook orqali ishlaydi
        port = int(os.getenv('PORT', 5000))
        server.run(host="0.0.0.0", port=port)
