import telegram


class TelegramClient:
    def __init__(self, token):
        self.bot = telegram.Bot(token)

    def send_message(self, chat_id, message):
        self.bot.send_message(chat_id, message, parse_mode="HTML")
