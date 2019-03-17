from models.FortressElement import FortressElement


class Sensor(FortressElement):
    """
    Базовый класс для всех сенсоров.
    """

    def __init__(self):
        super().__init__()
