import watchdog
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
            if self.callback_handle is not None:
                self.callback_handle(event.src_path)
