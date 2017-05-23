# DCS-930LB2016062021103401.jpg
# bot token 180821508:AAFq2zwPfUObGYpIRjG97mMMEIMlVboi2Xk

import logging
import telegram
import time
import os
import os.path
import collections
import NewFileEventHandler

from psutil import virtual_memory
from telegram.ext import CommandHandler
from watchdog.observers import Observer
from telegram.ext import MessageHandler, Filters
from requests import get
from requests.auth import HTTPBasicAuth

#FTP_DIR = '/home/pi/ftp'
FTP_DIR = '/Users/icewind/ftp'
active_chats = []
active_cameras = [
    {
        "id": 0,
        "title": "HighResZenfone",
        "ip": "192.168.0.102:8080",
        "type": "android"
    },
    {
        "id": 1,
        "title": "OldDesire",
        "ip": "192.168.0.105:8080",
        "type": "android"
    },
    {
        "id": 2,
        "title": "IP camera",
        "ip": "192.168.0.101",
        "type": "ipcam"
    }
]


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
        observer.schedule(handler, self.folder_to_watch, recursive=False)
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
        bot.sendMessage(chat_id=update.message.chat_id, text='Ага. Буду присылать тебе фотки обнаружения движения')
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text='Я итак присылаю обнаружение движения')


def echo(bot, update):
    text = update.message.text
    print("received:", text)
    understood = False

    if text.lower() == "камера":
        bot.sendMessage(chat_id = update.message.chat_id, text='Сейчас посмотрю. 5сек')
        info = tell_full_status()
        file_count_msg = 'Сейчас у меня {} файла(ов) с камеры.'.format(info['file_count'])
        last_file_msg = 'Последний из них был {}'.format(info['last_modified'])
        bot.sendMessage(chat_id = update.message.chat_id, text = file_count_msg)
        bot.sendMessage(chat_id = update.message.chat_id, text = last_file_msg)
        understood = True

    if text.lower() == "камеры":
        bot.sendMessage(chat_id = update.message.chat_id, text='Сейчас посмотрю. 5сек')
        info = active_cameras_list()
        bot.sendMessage(chat_id = update.message.chat_id, text = info)

        custom_keyboard = [['фото 1','фото 2','вспышка вкл 1', 'вспышка выкл 1']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.sendMessage(chat_id = update.message.chat_id, text = "Stay here, I'll be back.", reply_markup = reply_markup)
        understood = True

    if text.startswith("вспышка вкл"):
        cam_id = text[12:]
        toggle_torch(cam_id, True)
        understood = True

    if text.startswith("вспышка выкл"):
        cam_id = text[13:]
        toggle_torch(cam_id, False)
        understood = True

    if text.startswith("фото"):
        cam_id = text[5:]
        photo = get_cam_photo(cam_id)

        understood = True

    if text.lower() == "как дела?" or text.lower() == "че как":
        bot.sendMessage(chat_id = update.message.chat_id, text='Нормал')
        info = tell_self_status()
        file_count_msg = 'Сейчас у меня {} места свободно'.format(info['disk_free'])
        last_file_msg = 'Памяти свободно {} Мб'.format(info['memory_usage'])
        bot.sendMessage(chat_id = update.message.chat_id, text = file_count_msg)
        bot.sendMessage(chat_id = update.message.chat_id, text = last_file_msg)
        understood = True

    if text == "погода":
        bot.sendMessage(chat_id = update.message.chat_id, text = 'Купите мне термометр электронный и будет погода')
        understood = True

    if text == "марко":
        bot.sendMessage(chat_id = update.message.chat_id, text = 'поло')
        understood = True

    if text == "как":
        bot.sendMessage(chat_id = update.message.chat_id, text = 'Могу рассказать че как. Погоду. Подписать тебя на '
                                                                 'обнаружение движения от камеры')
        understood = True

    if not understood:
        bot.sendMessage(chat_id = update.message.chat_id, text = 'я короче не понял) сорян борян')


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

_ntuple_diskusage = collections.namedtuple('usage', 'total used free')


def disk_usage(path):
    st = os.statvfs(path)
    free = st.f_bavail * st.f_frsize
    total = st.f_blocks * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    return _ntuple_diskusage(total, used, free)


def memory_usage():
    mem = virtual_memory()
    return mem.available/1024/1024


def tell_self_status():
    disk_total, disk_used, disk_free = disk_usage(os.getcwd())
    usage_memory = memory_usage()

    info = {'memory_usage': usage_memory, 'disk_free': (disk_free/1024/1024)}

    return info


def toggle_torch(camera_id=0, state=False):
    current_camera = None
    for cam in active_cameras:
        if str(cam["id"]) == camera_id:
            current_camera = cam

    if current_camera is None:
        print("error : cam not found")
        return None
    action = "disabletorch"
    if state:
        action = "enabletorch"

    get("http://{}/{}".format(current_camera["ip"], action))


def get_cam_photo(cam_id):
    current_camera = None
    for cam in active_cameras:
        if str(cam["id"]) == cam_id:
            current_camera = cam

    if current_camera is None:
        print("error : cam not found")
        return None
    if current_camera["type"] == "android":
        action = "photo.jpg"
        for c in active_chats:
            print("http://{}/{}".format(current_camera["ip"], action))
            sendingBot.sendPhoto(c, photo = "http://{}/{}".format(current_camera["ip"], action))
    else:
        action = "image/jpeg.cgi"
        r = get("http://{}/{}".format(current_camera["ip"], action), auth=HTTPBasicAuth('admin', 't5atigeno2t'))
        with open("temp.jpg", "wb") as f:
            f.write(r.content)
        for c in active_chats:
            sendingBot.sendPhoto(c, photo=open("temp.jpg", "rb"))


def active_cameras_list():
    result = ""
    for x in active_cameras:
        print(x["title"])
        result = "\n{}\n{}:{}".format(result, x["id"], x["title"])
    return result

def temp(bot, update):
    pass



def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='Мучо грасиас, Шалом энд велкам!')

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






