import logging
from telegram.ext import Application, CommandHandler, filters, MessageHandler
from telegram import ReplyKeyboardMarkup
import sqlite3

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
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
user_id = [""]

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


async def profile(update, context):
    # У объекта класса Updater есть поле message,
    # являющееся объектом сообщения.
    # У message есть поле text, содержащее текст полученного сообщения,
    # а также метод reply_text(str),
    # отсылающий ответ пользователю, от которого получено сообщение.
    data = update.message.text.split("\n")
    data = (user_id[0], data[0], data[1], data[2], "\n".join(data[3:]))
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
