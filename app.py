import telepot
import time
import logging
from summit import summit_list
import os


class Handler():
    def __init__(self):
        token = os.getenv("CIMS_BOT_TOKEN")
        self.bot = telepot.Bot(token)
        self.bot.message_loop(self.handle)
        self.summits = summit_list.load_from_file(os.path.join(os.pardir(__file__), "test","100cims.csv"))

    def command_from_text(self, text):
        args_list = text.split()
        if len(args_list) < 1:
            return ""
        return args_list[0]

    def rest_of_message(self, text):
        args_list = text.split()
        if len(args_list) < 2:
            return ""
        return " ".join(args_list[1:])

    def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type != 'text':
            self.bot.sendMessage(chat_id, "This is not a command!")
            return
        chat_id = msg['chat']['id']
        chat_text = msg['text']
        command = self.command_from_text(chat_text)
        print('Got command %s' % command)
        print('From ID ', chat_id)
        if command == '/closest':
            # TODO get limit (num) and get limit (distance)
            MAX_DIST = 30
            location = self.rest_of_message(chat_text)
            list_summits = self.summits.get_closest_summits(location)
            print(list_summits)
            # TODO : Make answer




if __name__ == "__main__":
    h = Handler()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("telegram_bot.log")
        ]
    )

    while True:
        time.sleep(10)