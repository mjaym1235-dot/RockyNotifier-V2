# -----------------------------
#   ROCKY NOTIFIER BOT – WEBHOOK (VERSION FINALE)
# -----------------------------

import telebot
from telebot.types import Message
from flask import Flask, request
import threading
import requests
import time

# ============================
#   TOKEN
# ============================
TOKEN = "TON_TOKEN_ICI"  # Mets ton token ici
bot = telebot.TeleBot(TOKEN)

WEBHOOK_URL = "https://rockynotifier-v2-1.onrender.com/webhook"

# ============================
#   KEEP ALIVE
# ============================
def keep_alive():
    while True:
        try:
            requests.get("https://rockynotifier-v2-1.onrender.com/")
        except:
            pass
        time.sleep(300)

threading.Thread(target=keep_alive, daemon=True).start()

# ============================
#   IMAGES (FILE_ID)
# ============================
IMAGE_WAR = "AgACAgQAAxkBAAMXah_MDQX4s5kTHdtT3wkfsLQaEtQAAgsOaxtCV_lQbciX-WrPk5IBAAMCAAN4AAM7BA"
IMAGE_TOWER = "AgACAgQAAxkBAAM9ah_Rk8dMLVS5PBlCtQ138HBEXbIAAg8OaxtCV_lQ9Pmok24OOQ0BAAMCAANtAAM7BA"
IMAGE_CAP = "AgACAgQAAxkBAANBah_Y2KOjhTeoD0lgRxOPFlOKmIwAAhUOaxtCV_lQLTOTg-NKrkgBAAMCAAN4AAM7BA"

# ============================
#   FONCTION MENTION ADMINS
# ============================
def get_admin_mentions(chat_id):
    try:
        chat = bot.get_chat(chat_id)
        if chat.type not in ["group", "supergroup"]:
            return ""

        members = bot.get_chat_administrators(chat_id)
        text = ""
        for m in members:
            if m.user.username:
                text += f"@{m.user.username} "
            else:
                text += f"{m.user.first_name} "
        return text

    except Exception as e:
        print(f"Erreur get_admin_mentions: {e}")
        return ""

# ============================
#   /GETID — RÉPONSE À UNE IMAGE
# ============================
@bot.message_handler(commands=['getid'])
def get_id(message: Message):
    if message.reply_to_message and message.reply_to_message.photo:
        file_id = message.reply_to_message.photo[-1].file_id
        bot.reply_to(message, f"File ID : {file_id}")
    else:
        bot.reply_to(message, "Réponds à une image avec /getid.")

# ============================
#   /GETID2 — DERNIÈRE IMAGE
# ============================
last_photo_id = {}

@bot.message_handler(content_types=['photo'])
def detect_photo(message: Message):
    chat_id = message.chat.id
    file_id = message.photo[-1].file_id
    last_photo_id[chat_id] = file_id
    caption = message.caption.lower() if message.caption else ""

    if "/all" in caption:
        bot.send_photo(chat_id, file_id, caption=get_admin_mentions(chat_id))
        return

    if "/tower" in caption:
        bot.send_photo(chat_id, IMAGE_TOWER, caption=get_admin_mentions(chat_id))
        return

    if "/cap" in caption:
        bot.send_photo(chat_id, IMAGE_CAP, caption=get_admin_mentions(chat_id))
        return

    bot.reply_to(message, "📸 Image reçue !")

@bot.message_handler(commands=['getid2'])
def get_id2(message: Message):
    chat_id = message.chat.id
    if chat_id in last_photo_id:
        bot.reply_to(message, f"File ID : {last_photo_id[chat_id]}")
    else:
        bot.reply_to(message, "Aucune image reçue récemment.")

# ============================
#   COMMANDES
# ============================
@bot.message_handler(commands=['start'])
def start(message: Message):
    bot.reply_to(message, "Bot opérationnel ! 👌\nUtilise /command pour voir les commandes.")

# ============================
#   /WAR — VERSION HTML
# ============================
@bot.message_handler(commands=['war'])
def war_cmd(message: Message):
    chat_id = message.chat.id
    full = message.text
    cleaned = full.replace("/war", "").strip()

    alert = (
        "🟥🟥🟥  <b>G U E R R E</b>  🟥🟥🟥\n"
        "🟥🟥🟥  <b>G U E R R A</b>  🟥🟥🟥\n\n"
        f"{get_admin_mentions(chat_id)}"
    )

    if cleaned:
        cleaned = cleaned.upper()
        cleaned = f"🚨🚨🚨 <b>{cleaned}</b> 🚨🚨🚨"
        final_text = f"{cleaned}\n\n{alert}"
    else:
        final_text = alert

    bot.send_photo(chat_id, IMAGE_WAR, caption=final_text, parse_mode="HTML")

# ============================
#   /CAP — VERSION HTML (ÉTOILES)
# ============================
@bot.message_handler(commands=['cap'])
def cap(message: Message):
    chat_id = message.chat.id
    full = message.text
    cleaned = full.replace("/cap", "").strip()

    base = (
        "⭐ <b>C A P T U R E</b> ⭐\n"
        "⭐ <b>C A T T U R A</b> ⭐\n\n"
        f"{get_admin_mentions(chat_id)}"
    )

    if cleaned:
        cleaned = cleaned.upper()
        cleaned = f"⭐ <b>{cleaned}</b> ⭐"
        final_text = f"{cleaned}\n\n{base}"
    else:
        final_text = base

    bot.send_photo(chat_id, IMAGE_CAP, caption=final_text, parse_mode="HTML")

# ============================
#   /ALL — TEXTE AVANT + APRÈS
# ============================
@bot.message_handler(commands=['all'])
def mention_all(message: Message):
    chat_id = message.chat.id
    full = message.text
    cleaned = full.replace("/all", "").strip()

    mentions = get_admin_mentions(chat_id)

    if cleaned:
        final_text = f"{cleaned}\n{mentions}"
    else:
        final_text = mentions

    bot.send_message(chat_id, final_text)

# ============================
#   AUTRES COMMANDES
# ============================
@bot.message_handler(commands=['tower'])
def tower(message: Message):
    chat_id = message.chat.id
    text = "🗼 Tour / Torre :\n" + get_admin_mentions(chat_id)
    bot.send_photo(chat_id, IMAGE_TOWER, caption=text)

@bot.message_handler(commands=['command'])
def command_list(message: Message):
    text = (
        "📜 Commandes disponibles :\n\n"
        "/war – Alerte guerre\n"
        "/cap – Capture\n"
        "/all – Mention admins\n"
        "/tower – Infos tours\n"
        "/cap – Zones capturables\n"
    )
    bot.reply_to(message, text)

@bot.message_handler(content_types=['sticker'])
def detect_sticker(message: Message):
    bot.reply_to(message, "✨ Sticker reçu !")

@bot.message_handler(content_types=['text'])
def detect_text(message: Message):
    bot.reply_to(message, f"💬 Tu as dit : {message.text}")

# ============================
#   FLASK (WEBHOOK)
# ============================
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Bot actif 24/7 via webhook !"

@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

# ============================
#   LANCEMENT
# ============================
if __name__ == "__main__":
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url=WEBHOOK_URL)

    app.run(host='0.0.0.0', port=8080)











