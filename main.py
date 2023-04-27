import logging
from telegram.ext import Application, CommandHandler, filters, MessageHandler
from telegram import ReplyKeyboardMarkup
import sqlite3
import random

BOT_TOKEN = "5726600026:AAFYoGWEVQ8oWlJZJMQRLYTk_G-thDQFbQQ"
conn = sqlite3.connect('profiles.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS profiles(
   id INT PRIMARY KEY,
   name TEXT,
   gender TEXT,
   age TEXT,
   info TEXT);
""")
conn.commit()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
reply_keyboard = [['boy', 'girl']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
user_id = [""]
data_buttons = ['парень', 'девушка', '14-18', '18-25', '25-35', '35-60', '+', '-']
gender_pers = ['']
age_pers = ['']
result = []


# Определяем функцию-обработчик сообщений.
# У неё два параметра, updater, принявший сообщение и контекст - дополнительная информация о сообщении.
async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    user_id[0] = user.id
    t = '\n'
    await update.message.reply_html(
        rf"Приветик, {user.mention_html()}! Я бот для знакомств. Чтобы начать общение, тебе нужно сделать анкету в следующем формате:"
        rf"{t}"
        rf"Имя"
        rf"{t}"
        rf"Девушка/парень"
        rf"{t}"
        rf"Возраст"
        rf"{t}"
        rf"Что-нибудь о себе!",
    )


async def boy(update, context):
    await update.message.reply_html(rf"Хорошо! Какой возраст тебя интересует?")


async def profile(update, context):
    t = '\n'
    if update.message.text == data_buttons[0]:
        reply_keyboard[0] = ['14-18', '18-25', '25-35', '35-90']
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        await update.message.reply_text(rf"Хорошо! Теперь укажи возраст, который тебя интересует.", reply_markup=markup)
        gender_pers[0] = update.message.text
        return 0

    elif update.message.text == data_buttons[1]:
        reply_keyboard[0] = ['14-18', '18-25', '25-35', '35-90']
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        await update.message.reply_text(rf"Хорошо! Теперь укажи возраст, который тебя интересует.", reply_markup=markup)
        gender_pers[0] = update.message.text
        return 0

    elif update.message.text == data_buttons[2]:
        reply_keyboard[0] = ['+', '-']
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        await update.message.reply_text(
            rf"Хорошо! Теперь давай начнем искать тебе собеседника :3{t}Нажми - чтобы начать! ", reply_markup=markup)
        age_pers[0] = update.message.text
        return 0

    elif update.message.text == data_buttons[3]:
        reply_keyboard[0] = ['+', '-']
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        await update.message.reply_text(
            rf"Хорошо! Теперь давай начнем искать тебе собеседника :3{t}Нажми - чтобы начать! ", reply_markup=markup)
        age_pers[0] = update.message.text
        return 0

    elif update.message.text == data_buttons[4]:
        reply_keyboard[0] = ['+', '-']
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        await update.message.reply_text(
            rf"Хорошо! Теперь давай начнем искать тебе собеседника :3{t}Нажми - чтобы начать! ", reply_markup=markup)
        age_pers[0] = update.message.text
        return 0

    elif update.message.text == data_buttons[5]:
        reply_keyboard[0] = ['+', '-']
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        await update.message.reply_text(
            rf"Хорошо! Теперь давай начнем искать тебе собеседника :3{t}Нажми - чтобы начать! ", reply_markup=markup)
        age_pers[0] = update.message.text
        return 0

    elif update.message.text == data_buttons[6]:
        reply_keyboard[0] = ['+', '-']
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        await update.message.reply_text(
            rf"Прикольно", reply_markup=markup)
        return 0

    elif update.message.text == data_buttons[7]:
        reply_keyboard[0] = ['+', '-']
        cur.execute("SELECT * FROM profiles;")
        all_result = cur.fetchall()
        print(all_result)
        all_result = list(filter(
            lambda x: x[2].lower() == gender_pers[0] and int(age_pers[0][0:2]) <= int(x[3]) <= int(age_pers[0][3:]) and
                      x[0] not in result,
            all_result))
        if len(all_result) == 0:
            await update.message.reply_text("К сожалению, анкет больше нет :(. Возвращайтесь позже!")
            return 0
        a = random.choice(all_result)
        result.append(a[0])
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        await update.message.reply_text(
            rf"{a[1]}{t}{a[2]}{t}{a[3]}{t}{a[4]}", reply_markup=markup)
        return 0

    data = update.message.text.split("\n")
    data = (user_id[0], data[0], data[1].lower(), int(data[2]), "\n".join(data[3:]))
    reply_keyboard[0] = ['парень', 'девушка']
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text(
        rf"Готово! Теперь ты можешь начать общение! Выбери, кто тебя интересует больше?", reply_markup=markup
    )

    cur.execute("INSERT INTO profiles VALUES(?, ?, ?, ?, ?);", data)
    conn.commit()


def main():
    # Создаём объект Application.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("boy", boy))
    # Создаём обработчик сообщений типа filters.TEXT
    # из описанной выше асинхронной функции echo()
    # После регистрации обработчика в приложении
    # эта асинхронная функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.
    text_handler = MessageHandler(filters.TEXT, profile)
    # Регистрируем обработчик в приложении.
    application.add_handler(text_handler)
    # Запускаем приложение.
    application.run_polling()

    # Запускаем функцию main() в случае запуска скрипта.


if __name__ == '__main__':
    main()
