# DCS-930LB2016062021103401.jpg
# bot token 180821508:AAFq2zwPfUObGYpIRjG97mMMEIMlVboi2Xk

import logging
import telegram
import time
from telegram.ext import CommandHandler
from watchdog.observers import Observer
import NewFileEventHandler
from telegram.ext import MessageHandler, Filters


active_chats = []


class DirWatchdog(object):
    """
    Utility class for looking for changes in given directory.
    DirWatchdog will notify

    """
    watchdog_callback = None
    folder_to_watch = None

    def watch(self, folder, callback):
        """
        Here we start watching folder.
        Watcher starts in separate thread
        :param folder: folder to watch changes in
        :param callback: is called when new file detected
                         Callback will receive file path in first argument
        :return: nothing to return
        """

        self.watchdog_callback = callback
        self.folder_to_watch = folder
        handler = NewFileEventHandler.NewFileEventHandler()
        handler.callback_handle = self.watchdog_callback
        observer = Observer()
        observer.schedule(handler, self.folder_to_watch, recursive = False)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()




def new_file_found(args):
    for c in active_chats:
        sendingBot.sendPhoto(c, photo=open(args, 'rb'))



def status(bot, update):
    if update.message.chat_id not in active_chats:
        active_chats.append(update.message.chat_id)
        bot.sendMessage(chat_id = update.message.chat_id, text = 'You will recieve it')
    else:
        bot.sendMessage(chat_id = update.message.chat_id, text = 'you are already subscribed!')


def echo(bot, update):
    text = update.message.text;
    if text == "че как":
        bot.sendMessage(chat_id = update.message.chat_id, text='Все хорошо. Больше пока не готов сказать')


def start(bot, update):
    bot.sendMessage(chat_id = update.message.chat_id, text='Hello, master')

if __name__ == '__main__':
    print('Starting watchdog on folder')
    logging.basicConfig(level = logging.DEBUG,
                        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # starting telegram bot
    bot = telegram.ext.Updater(token='180821508:AAFq2zwPfUObGYpIRjG97mMMEIMlVboi2Xk')
    sendingBot = telegram.Bot(token='180821508:AAFq2zwPfUObGYpIRjG97mMMEIMlVboi2Xk')
    dispatcher = bot.dispatcher
    status_handler = CommandHandler('status', status)
    dispatcher.add_handler(status_handler)

    echo_handler = MessageHandler([Filters.text], echo)
    dispatcher.add_handler(echo_handler)

    bot.start_polling()
    print("something goes here")

    # starting folder watching
    wdog = DirWatchdog()
    wdog.watchdog_callback = new_file_found
    wdog.watch('/home/pi/ftp', new_file_found)






