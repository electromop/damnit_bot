import telebot
from telebot import types

token = "6330998613:AAHlP3A6M__dswFAJPIqz3HlQ7YO--B2sP8"
group_chat_id = "-4158177073"
users_categories = {"delivery":"@astromop", "products":"@lowbrains"}

bot = telebot.TeleBot(token)

@bot.message_handler(commands=["start"])
def start(message):
    if str(message.chat.id) == group_chat_id:
        bot.send_message(message.chat.id, "Бот работает, новые сообщения появятся сразу как только появятся!")
    else:
        markup = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton(text="Вопрос по доставке", callback_data="delivery")
        button2 = types.InlineKeyboardButton(text="Вопрос по товару", callback_data="product")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, "Привет, выбери, что тебе непонятно", reply_markup=markup)

@bot.callback_query_handler(func = lambda call: call.data == "delivery")
def delivery(call):
    bot.send_message(call.message.chat.id, "Напиши свой вопрос")
    bot.register_next_step_handler(call.message, answer_and_send_delivery)

def answer_and_send_delivery(message):
    bot.send_message(message.chat.id, "Твой вопрос принят! Ожидай ответа администратора")
    bot.send_message(group_chat_id, f"Назначен: {users_categories['delivery']}\nВопрос от: {message.chat.id}\nТекст вопроса: {message.text}")

@bot.callback_query_handler(func = lambda call: call.data == "product")
def delivery(call):
    bot.send_message(call.message.chat.id, "Напиши свой вопрос")
    bot.register_next_step_handler(call.message, answer_and_send_products)

def answer_and_send_products(message):
    bot.send_message(message.chat.id, "Твой вопрос принят! Ожидай ответа администратора")
    bot.send_message(group_chat_id, f"Назначен: {users_categories['products']}\nВопрос от: {message.chat.id}\nТекст вопроса: {message.text}")

@bot.message_handler(commands=['answer'])
def unmute_user(message):
    if str(message.chat.id) == group_chat_id:
        if message.reply_to_message:
            text = message.reply_to_message.text
            text = text[text.find("Вопрос от: ") + 11:]
            chat_id_question = text[:text.find("\n")]
            bot.send_message(chat_id_question, f"Вам пришел ответ на ваш вопрос!\n{message.text[7:]}")
            bot.send_message(group_chat_id, "Ваше сообщение отправлено!", reply_to_message_id=message.id)
        else:
            bot.reply_to(message, "Это сообщение должно быть отправлено с ответом на сообщение с вопросом")
    else:
        bot.send_message(message.chat.id, "Неизвестная команда")

bot.polling()
