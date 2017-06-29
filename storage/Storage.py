# -*- coding: utf-8 -*-


class StorageApi(object):
    """
    Абстрактное хранилище.
    Для использования другого - достаточно заменить этот класс другим.
    По умолчанию будет использоваться sqllite.

    По идее неплохо было бы при первом запуске воссоздавать структуру базы.
    При этом каждый модуль может при первом обращении сам задать эту структуру..

    Например,

    В модуле температуры

    db_info = {
        "tables": [
            {
                "name": "temperature",
                "fields": [
                    {
                        "name": "id",
                        "type": "int",
                        "isPrimaryKey":"true"
                    }
                ]
            }
        ]

        "values"
    }

    tempStorage = StorageApi(db_info)

    """

    db_fname = ""  # path to sqllite db file

    initial_structure = {}  # to check and recreate at first time

    def __init__(self, db_filename, initial_struct=None):
        if initial_struct is None:
            initial_struct = {}
        self.db_file = db_filename
        self.initial_structure = initial_struct

    def insert(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def recreate(self):
        """
        Воссоздание нужных таблиц, если необходимо
        :return:
        """
        pass





