# DCS-930LB2016062021103401.jpg
# bot token 180821508:AAFq2zwPfUObGYpIRjG97mMMEIMlVboi2Xk

import logging
import telegram
import time
import os
import os.path
import NewFileEventHandler
from telegram.ext import CommandHandler
from watchdog.observers import Observer
from telegram.ext import MessageHandler, Filters

#FTP_DIR = '/home/pi/ftp'
FTP_DIR = '/Users/icewind/ftp'
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
        if args.endswith('.jpg'):
            sendingBot.sendPhoto(c, photo=open(args, 'rb'))
        else:
            print('Ignored file with name {}', args)



def status(bot, update):
    if update.message.chat_id not in active_chats:
        active_chats.append(update.message.chat_id)
        bot.sendMessage(chat_id = update.message.chat_id, text = 'Ага. Буду присылать тебе фотки обнаружения движения')
    else:
        bot.sendMessage(chat_id = update.message.chat_id, text = 'Я итак тебе присылаю обнаружение движения. Не '
                                                                 'писькуй давай')


def echo(bot, update):
    text = update.message.text

    if text == "че как" or text == "Че как":
        bot.sendMessage(chat_id = update.message.chat_id, text='Сейчас посмотрю. 5сек')
        info = tell_full_status()
        file_count_msg = 'Сейчас у меня {} файлов с камеры.'.format(info['file_count'])
        last_file_msg = 'Последний из них был {}'.format(info['last_modified'])
        bot.sendMessage(chat_id = update.message.chat_id, text = file_count_msg)
        bot.sendMessage(chat_id = update.message.chat_id, text = last_file_msg)

    if text == "погода":
        bot.sendMessage(chat_id = update.message.chat_id, text = 'Купите мне термометр электронный и будет погода')

    if text == "марко":
        bot.sendMessage(chat_id = update.message.chat_id, text = 'поло')


def tell_full_status():
    # files count
    count = 0
    total_info = {}
    last_time = None
    for name in os.listdir(FTP_DIR):
        if os.path.isfile(os.path.join(FTP_DIR, name)):
            mtime = os.path.getmtime(os.path.join(FTP_DIR, name))
            if last_time is None:
                last_time = mtime
            if mtime > last_time:
                last_time = mtime
            count += 1
    total_info['file_count'] = count
    total_info['last_modified'] = time.ctime(last_time)
    return total_info




def temp(bot, update):
    pass



def start(bot, update):
    bot.sendMessage(chat_id = update.message.chat_id, text='Мучо грасиас, Шалом энд велкам!')

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
    wdog.watch(FTP_DIR, new_file_found)






