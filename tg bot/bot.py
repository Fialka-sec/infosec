# bot.py
import telebot
from config import TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_help(message):
    help_text = (
        "Привет! Я валютный бот.\n"
        "Чтобы получить цену, отправьте сообщение в формате:\n"
        "<валюта_покупки> <валюта_продажи> <количество>\n"
        "Например:\n"
        "доллар евро 10\n\n"
        "Команды:\n"
        "/start или /help — это сообщение\n"
        "/values — список поддерживаемых валют"
    )
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['values'])
def send_values(message):
    values_text = (
        "Доступные валюты:\n"
        "- евро\n"
        "- доллар\n"
        "- рубль"
    )
    bot.send_message(message.chat.id, values_text)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    try:
        parts = message.text.strip().split()
        if len(parts) != 3:
            raise APIException('Неверный формат. Используйте:\n<валюта_покупки> <валюта_продажи> <количество>')

        base_currency, quote_currency, amount_str = parts

        try:
            amount = float(amount_str.replace(',', '.'))
        except:
            raise APIException('Некорректное число. Проверьте формат количества.')

        total = CryptoConverter.get_price(base_currency, quote_currency, amount)
        reply = f'{amount} {base_currency} стоит {total} {quote_currency}'
        bot.send_message(message.chat.id, reply)
    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла неожиданная ошибка: {type(e).__name__}')

if __name__ == '__main__':
    bot.polling(none_stop=True)