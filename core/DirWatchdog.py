
class DirWatchdog(object):
    """
    Utility class for looking for changes in given directory.
    DirWatchdog will notify

    """
    watchdog_callback = None
    folder_to_watch = None

    def watch(self, folder, callback):
        self.watchdog_callback = callback
        self.folder_to_watch = folder




