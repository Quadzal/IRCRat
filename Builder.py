import xml.etree.ElementTree as ET
import codecs, shutil, os

os.system("pip3 install -r requirements.txt")

tree = ET.parse("data.xml")
root = tree.getroot()
for data in root.iter("A1"):
    new_email = input("EMAİL Giriniz: ")
    if new_email == "":
        print("Boş Bırakılamaz Çıkılıyor.")
        exit()
    encode_email=codecs.encode(bytes(new_email, "utf-8"), "base64_codec")
    data.text = str(encode_email.decode())

for data in root.iter("A2"):
    new_pass = input("Email Şifrenizi Giriniz: ")
    encode_pass = codecs.encode(bytes(new_pass, "utf-8"), "base64_codec")
    data.text = str(encode_pass.decode())

for data in root.iter("A3"):
    new_channel = input("Kanal İsmi Giriniz Başında # Olmak Şartıyla: ")
    if "#" not in new_channel:
        print("Hata!")
        continue
    else:
        encode_channel = codecs.encode(bytes(new_channel,"utf-8"),"base64_codec")
        data.text = str(encode_channel.decode())

tree.write("data.xml")
os.system('pyinstaller --onefile IRCRat.py')
shutil.copy("data.xml",os.getcwd()+"/dist")
