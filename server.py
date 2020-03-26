import socket
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
network = '192.168.1.'

def main():
    islem = input("Dosya almak için '1', dosya göndermek için ise '2' yazınız.")
    islemle(islem)

def islemle(islem):
    if islem == str(1):
        findUsers()
    elif islem == str(2):
        Sender()
    else:
        print("Hatalı bir işlem yaptınız. Lütfen tekrar deneyin.")
        main()

def Sender():
    port = 8080
    s = socket.socket()
    host = socket.gethostname()
    s.bind((host, port))
    s.listen(5)

    # Service_Listener
    print(host)
    print("Cihaz bağlantısı için bekleniyor...")
    try:
        conn, addr = s.accept()
        for ip in range(1, 256):
            addr = network + str(ip)
            if is_up(addr):
                fqdn = socket.getfqdn(addr)
        print(addr, fqdn, "- Server'a giriş yaptı.")
    except:
        print("Cihaz Bağlanamadı")
        s.close()
        conn.close()
        Sender()

    try:
        filename = input(str("Gönderilecek Olan dosyanın yolunu yazın : "))
        file = open(filename, 'rb')
        file_path = filename
        file_stats = os.stat(file_path)
        size = str(file_stats.st_size)
        print("'" + size + "'KB")
    except:
        s.close()
        conn.close()
        Sender()

    # P2P_Uploader/Server
    try:
        file_data = file.read(file_stats.st_size)
        conn.send(file_data)
        print("Dosya Başarıyla Gönderildi.")
    except:
        print("Beklenmedik bir hata oluştu.")
        print("Dosya Gönderilemedi")
        s.close()
        conn.close()
        Sender()

    try:
        s.close()
        conn.close()
        print("Server Kapatıldı.")
    except:
        print("SERVER KAPANIRKEN BEKLENMEDİK BİR HATA OLUŞTU LÜTFEN PROGRAMI KAPATIP YENİDEN AÇIN YA DA PORT ADRESİNİ DEĞİŞTİRİN")

    try:
        gonderildilogla(fqdn, host, filename, size)
    except:
        print("Log Dosyası Oluşturulamadı.")
        main()

def Receiver(hostAdi):
    s = socket.socket()
    host = hostAdi
    port = 8080
    size = 1

    try:
        s.connect((host, port))
        print("Giriş Sağlandı.")
    except:
        print("Eksik, hatalı isim girdiniz veya cihaz dinleme durumunda değil, lütfen tekrar deneyin.")
        hostadiAl()

    # Service_Advertiser
    filename = input(str("Almak istediğiniz dosyanın bilgisayarınıza gelecek olan yolunu ve adını yazın *Örnek klasör/dosya.jpg* :")) #Örnek:folder/file.jpg
    file = open(filename, 'wb')
    size = input("Lütfen dosya boyutunu KB olarak yazın : ") #Örnek:120
    print("Lütfen karşı cihazın onayını bekleyin.")

    # P2P_Downloader
    try:
        file_Data = s.recv((int(size)));
        file.write(file_Data)
        print("Dosya Başarıyla Alındı.")
    except:
        print("Beklenmedik bir hata oluştu.")
        s.close()
        file.close()
        main()
    try:
        file.close()
        s.close()
        print("Sever Kapatıldı.")
    except:
        print("SERVER KAPANIRKEN BEKLENMEDİK BİR HATA OLUŞTU LÜTFEN PROGRAMI KAPATIP YENİDEN AÇIN YA DA PORT ADRESİNİ DEĞİŞTİRİN")
    try:
        for ip in range(1, 256):
            addr = network + str(ip)
            if is_up(addr):
                fqdn = socket.getfqdn(addr)
        alındılogla(fqdn, host, filename, size)
    except:
        print("Log Dosyası Oluşturulamadı.")
        s.close()
        file.close()
        main()

def is_up(addr):
        s = socket.socket()
        s.settimeout(0.01)
        if not s.connect_ex((addr, 135)):
            return 1

def findUsers():
    print("LAN'daki windows cihazları aranıyor. Lütfen bekleyin.")
    print(' ')
    for ip in range(1, 256):
        addr = network + str(ip)
        if is_up(addr):
            fqdn = socket.getfqdn(addr)
            print('%s - %s' % (addr, fqdn))
    print("-----------------------------------------")
    hostadiAl()

def hostadiAl():
    hostAdi = input(str("Lütfen dosya alacağınız cihazın adını yazın : "))
    Receiver(hostAdi)

def alındılogla(fqdn, host, filename, size):
    try:
        LOG_FILENAME = datetime.now().strftime('log/logfile_%H_%M_%S_%d_%m_%Y.log')
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
        logging.info("Dosya Alındı")
        logging.info("Tarih-Saat: {a}".format(a=datetime.now()))
        logging.info("Gönderici Adı: {a}".format(a=host))
        logging.info("Alıcı Adı: {a}".format(a=fqdn))
        logging.info("Dosya Adı: {a}".format(a=filename))
        logging.info("Dosya Boyutu: {a}".format(a=size))
        main()
    except:
        print("Log Dosyası Oluşturulamadı.")
        main()

def gonderildilogla(fqdn, host, filename, size):
    try:
        LOG_FILENAME = datetime.now().strftime('log/logfile_%H_%M_%S_%d_%m_%Y.log')
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
        logging.info("Dosya Gönderildi")
        logging.info("Tarih-Saat: {a}".format(a=datetime.now()))
        logging.info("Gönderici Adı:{a}".format(a=host))
        logging.info("Alıcı Adı:{a}".format(a=fqdn))
        logging.info("Dosya Adı:{a}".format(a=filename))
        logging.info("Dosya Boyutu:{a}".format(a=size))
        main()
    except:
        print("Log Dosyası Oluşturulamadı.")
        main()

main()
