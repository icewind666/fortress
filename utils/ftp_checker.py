#!/usr/bin/env python
import ftplib

FTP_HOST = 'localhost'
FTP_PORT = 21
FTP_USER = 'ftp_user'
FTP_PASSWORD = 'ftp_user'

ftp = ftplib.FTP()
ftp.connect(FTP_HOST, FTP_PORT)
ftp.login(FTP_USER, FTP_PASSWORD)

files = ftp.dir()
print(files)
# Открываем файл для передачи в бинарном режиме
# f = open(filename, "rb")
# Передаем файл на сервер
# send = con.storbinary("STOR "+ filename, f)
# Закрываем FTP соединение
ftp.close()
