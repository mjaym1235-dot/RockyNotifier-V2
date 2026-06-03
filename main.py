import telebot
from telebot.types import Message

# ============================
#   TOKEN
# ============================
TOKEN = "8982899307:AAEFJQmjcT2JnnUOqizbMFlxMVGbWG-B8-0"
bot = telebot.TeleBot(TOKEN)

# ============================
#   IMAGES (À REMPLIR PLUS TARD)
# ============================

IMAGE_WAR = ""       # file_id de l'image GUERRE
IMAGE_TOWER = ""     # file_id de l'image TOUR
IMAGE_BUILD = ""     # file_id de l'image CONSTRUCTION

# ============================
#   FONCTION MENTION ADMINS
# ============================

def get_admin_mentions(chat_id):
    members = bot.get_chat_administrators(chat_id)
    text = "👑 Mention des admins :\n"
    for m in members:
        if m.user.username:
            text += f"@{m.user.username}\n"
        else:
            text += f"{m.user.first_name}\n"
    return text

# ============================
#   /START
# ============================

@bot.message_handler(commands=['start'])
def start(message: Message):
    bot.reply_to(message, "Bot opérationnel ! 👌\nUtilise /command pour voir les commandes.")

# ============================
#   /HELP — GUERRE FR/ITA + ALL
# ============================

@bot.message_handler(commands=['help'])
def help_cmd(message: Message):
    chat_id = message.chat.id

    text = (
        "🟥🟥🟥  G U E R R E  🟥🟥🟥\n"
        "🟥🟥🟥  G U E R R A  🟥🟥🟥\n\n"
        "🔥 La bataille commence maintenant.\n"
        "🔥 La battaglia inizia adesso.\n\n"
        + get_admin_mentions(chat_id)
    )

    bot.send_photo(chat_id, IMAGE_WAR, caption=text)

# ============================
#   /COMMAND — LISTE FR + ITA
# ============================

@bot.message_handler(commands=['command'])
def command_list(message: Message):
    text = (
        "📜 Commandes disponibles / Comandi disponibili :\n\n"
        "🇫🇷 /start – Vérifier si le bot fonctionne\n"
        "🇫🇷 /help – Alerte guerre (image + FR/ITA + mentions)\n"
        "🇫🇷 /all – Mentionner les admins\n"
        "🇫🇷 /tower – Infos tour (image + mentions)\n"
        "🇫🇷 /build – Infos construction (image + mentions)\n\n"
        "🇮🇹 /start – Verificare se il bot funziona\n"
        "🇮🇹 /help – Allerta guerra (immagine + FR/ITA + menzioni)\n"
        "🇮🇹 /all – Menzionare gli admin\n"
        "🇮🇹 /tower – Info torre (immagine + menzioni)\n"
        "🇮🇹 /build – Info costruzione (immagine + menzioni)\n"
    )
    bot.reply_to(message, text)

# ============================
#   /ALL — MENTION DES ADMINS
# ============================

@bot.message_handler(commands=['all'])
def mention_all(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, get_admin_mentions(chat_id))

# ============================
#   /TOWER — IMAGE + TEXTE + ALL
# ============================

@bot.message_handler(commands=['tower'])
def tower(message: Message):
    chat_id = message.chat.id

    text = (
        "🗼 Tour actuelle / Torre attuale :\n"
        "• Niveau / Livello : 12\n"
        "• Défense / Difesa : 3400\n"
        "• Bonus armée / Bonus esercito : +18%\n\n"
        + get_admin_mentions(chat_id)
    )

    bot.send_photo(chat_id, IMAGE_TOWER, caption=text)

# ============================
#   /BUILD — IMAGE + TEXTE + ALL
# ============================

@bot.message_handler(commands=['build'])
def build(message: Message):
    chat_id = message.chat.id

    text = (
        "🏗️ Construction en cours / Costruzione in corso :\n"
        "• Caserne niv. 9 → 2h restantes\n"
        "• Mura → 45 min\n\n"
        + get_admin_mentions(chat_id)
    )

    bot.send_photo(chat_id, IMAGE_BUILD, caption=text)

# ============================
#   DÉTECTION D’IMAGES + COMMANDES
# ============================

@bot.message_handler(content_types=['photo'])
def detect_photo(message: Message):
    chat_id = message.chat.id
    file_id = message.photo[-1].file_id
    caption = message.caption.lower() if message.caption else ""

    # IMAGE + /all
    if "/all" in caption:
        bot.send_photo(chat_id, file_id, caption=get_admin_mentions(chat_id))
        return

    # IMAGE + /tower
    if "/tower" in caption:
        bot.send_photo(chat_id, IMAGE_TOWER, caption=get_admin_mentions(chat_id))
        return

    # IMAGE + /build
    if "/build" in caption:
        bot.send_photo(chat_id, IMAGE_BUILD, caption=get_admin_mentions(chat_id))
        return

    # IMAGE SIMPLE
    bot.reply_to(message, "📸 Image reçue !")

# ============================
#   DÉTECTION DE STICKERS
# ============================

@bot.message_handler(content_types=['sticker'])
def detect_sticker(message: Message):
    bot.reply_to(message, "✨ Sticker reçu !")

# ============================
#   DÉTECTION DE TEXTE
# ============================

@bot.message_handler(content_types=['text'])
def detect_text(message: Message):
    bot.reply_to(message, f"💬 Tu as dit : {message.text}")

# ============================
@bot.message_handler(commands=['getid'])
def get_id(message):
    if message.reply_to_message and message.reply_to_message.photo:
        file_id = message.reply_to_message.photo[-1].file_id
        bot.reply_to_message(message, f"File ID : {file_id}")
    else:
        bot.reply_to_message(message, "Réponds à une image avec /getid.")

#   LANCEMENT DU BOT
# ============================

print("Bot lancé…")
bot.infinity_polling(timeout=60, long_polling_timeout=60)


