from models.FortressElement import FortressElement


class Camera(FortressElement):
    """
    Базовый класс для всех камер.
    """

    def __init__(self):
        super().__init__()
        self.ip = ""
        self.port = ""
        self.type = ""
        self.desc = ""
        self.photo_method_url = "/image/jpeg.cgi"  # default
        self.supports_images = True
        self.supports_video = False

    def supports_img_capture(self):
        return self.supports_images

    def supports_video_capture(self):
        return self.supports_video

    def get_url(self):
        return "{}:{}".format(self.ip, self.port)
