import rumps
import requests
import re
import json
import threading
import os
import os.path

dataFile = os.path.join(os.getenv("HOME"), ".rekarma", "user.txt")
dataDir = os.path.join(os.getenv("HOME"), ".rekarma")
class reKarma(rumps.App):
    def __init__(self):
        super(reKarma, self).__init__("reKarma - No user")
        self.user = None
        self.menu[0] = "No user"
        os.makedirs(dataDir, exist_ok=True)
        file = open(dataFile, "r")
        user = file.read()
        if(user != ""):
            self.user = user
            self.title = "k/0"
        file.close()
  
    @rumps.clicked("Change r/username")
    def ahoj(self, sendr):
        window = rumps.Window("Enter reddit username", "Enter r/username", dimensions=(300,50))
        response = window.run()
        if response.text != "":
            self.user = response.text
            file = open(dataFile, "w")
            file.write(self.user)
            file.close()
            self.title = "k/0"
            reload = threading.Thread(target=self.getKarma,args=[None])
            reload.start()

    @rumps.timer(300)
    def getKarma(self, sender):
        if(self.user == None):
            return
        self.menu[0].title = self.user
        data = requests.get("https://www.reddit.com/user/" + self.user, headers={"User-Agent": "linux:bo-Bo-t:v1.0.0 (by /u/nutellaordidnthappen)"})
        resp = re.findall("total.{1,5}?\d{1,10}(?=})", data.text, flags=re.S)
        if(len(resp)>0):
            karma = re.sub("\D","",resp[0])
            self.title = "k/" + str(karma)
        else:
            self.title = "N/A"

if __name__ == "__main__":
    reKarma().run()