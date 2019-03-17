"""
Обработчик на события файловой системы.
А точнее - событие появляения нового файла в заданной папке.
По событию просто вызывает callback и в качестве агрумента отдает
путь к новому файлу.

"""
import time
from watchdog.events import FileCreatedEvent
from watchdog.events import FileSystemEventHandler


class NewFileEventHandler(FileSystemEventHandler):
    """
    Handles events for new files in folder
    """

    callback_handle = None

    def on_created(self, event):
        if isinstance(event, FileCreatedEvent):
            print("File created!!")
            print(event.src_path)
            print('Waiting for copy to complete. 2 secs')

            if self.callback_handle is not None:
                time.sleep(2)
                print('Calling handler function')
                self.callback_handle(event.src_path)
