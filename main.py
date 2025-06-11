import telebot

BOT_TOKEN = '7538576701:AAGs2yI8WRqPBdPwPcauFMhkPszlxt52NYE'
ADMIN_ID = 1114737366  # Sizning Telegram ID'ingiz

bot = telebot.TeleBot(BOT_TOKEN)

# Start menyusi
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('🚛 Mashinalar ro‘yxati', '📝 Buyurtma berish')
    markup.row('💰 To‘lov', '📞 Yordam')
    bot.send_message(message.chat.id, f"Salom {message.from_user.first_name}! Yuk tashish xizmatiga xush kelibsiz.", reply_markup=markup)

# Mashinalar ro'yxati
@bot.message_handler(func=lambda message: message.text == '🚛 Mashinalar ro‘yxati')
def show_trucks(message):
    mashinalar = "🚛 Mavjud yuk mashinalari:\n\n"
    mashinalar += "1. MAN TGX 18.500\n"
    mashinalar += "2. Volvo FH16\n"
    mashinalar += "3. Mercedes-Benz Actros\n"
    mashinalar += "4. DAF XF\n"
    mashinalar += "5. KamAZ 5490\n"
    bot.send_message(message.chat.id, mashinalar)

# Buyurtma holati
user_orders = {}

@bot.message_handler(func=lambda message: message.text == '📝 Buyurtma berish')
def order_start(message):
    bot.send_message(message.chat.id, "Yuk turini kiriting (masalan: Qurilish materiallari):")
    bot.register_next_step_handler(message, get_yuk_turi)

def get_yuk_turi(message):
    user_orders[message.chat.id] = {'yuk': message.text}
    bot.send_message(message.chat.id, "Yuboriladigan manzilni kiriting:")
    bot.register_next_step_handler(message, get_manzil)

def get_manzil(message):
    user_orders[message.chat.id]['manzil'] = message.text
    bot.send_message(message.chat.id, "Yuk mashinasini tanlang (masalan: MAN TGX 18.500):")
    bot.register_next_step_handler(message, get_mashina)

def get_mashina(message):
    user_orders[message.chat.id]['mashina'] = message.text
    bot.send_message(message.chat.id, "Bog‘lanish uchun telefon raqamingizni yozing:")
    bot.register_next_step_handler(message, finish_order)

def finish_order(message):
    user_orders[message.chat.id]['phone'] = message.text
    data = user_orders[message.chat.id]
    order_text = f"""✅ Buyurtma qabul qilindi:

📦 Yuk turi: {data['yuk']}
📍 Manzil: {data['manzil']}
🚛 Mashina: {data['mashina']}
📞 Telefon: {data['phone']}
👤 Buyurtmachi: @{message.from_user.username or message.from_user.first_name}
"""
    bot.send_message(message.chat.id, "Buyurtma qabul qilindi. To‘lov uchun pastdagi tugmani bosing:")
    pay_link = "https://pay.binance.com/"  # Bu yerga haqiqiy to‘lov linki integratsiya qilinadi
    bot.send_message(message.chat.id, f"💳 To‘lov havolasi: {pay_link}")

    # Adminga xabar
    bot.send_message(ADMIN_ID, "📥 Yangi buyurtma:\n\n" + order_text)

# To‘lov bo‘limi
@bot.message_handler(func=lambda message: message.text == '💰 To‘lov')
def payment_info(message):
    text = "💸 To‘lovni quyidagi havola orqali amalga oshiring:\n"
    text += "➡️ https://pay.binance.com\n\n"
    text += "To‘lov qilganingizdan so‘ng bizga xabar bering."
    bot.send_message(message.chat.id, text)

# Yordam
@bot.message_handler(func=lambda message: message.text == '📞 Yordam')
def help_info(message):
    bot.send_message(message.chat.id, "Biz bilan bog‘lanish: @ShaxriyorXolmuminov")

# Ishga tushirish
bot.polling(none_stop=True)
