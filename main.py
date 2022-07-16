from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import *
import os, sys
from parcing import *
import welcome, read_ranobe

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
}
titles_dict = {}

def get_data():
    if not os.path.exists("data"):
        os.mkdir("data")

    r = requests.get("https://ranobe.me/stat?top=stat_all", headers)
    soup = bs(r.text, "lxml")

    counter = soup.select(".paginator > span > a")[-1].text
    print(counter)

    for i in range(1, int(counter)+1):
        r = requests.get(f"https://ranobe.me/stat?top=stat_all&page={i}")
        soup = bs(r.text, "lxml")

        rating = soup.select(".fic > a")
        for item in rating:
            name = item.text
            href = "https://ranobe.me" + item.get("href")

            if not name in titles_dict and not href in titles_dict:
                titles_dict[name] = href

    with open("data/titles.json", "w") as file:
        json.dump(titles_dict, file, indent=4, ensure_ascii=False)  


def get_title(ranobe_title, ranobe_cahpter : int):
        with open("data/titles.json", "r") as file:
            src = json.load(file)

    #try:       
        r = requests.get(src[ranobe_title], headers)  
        soup = bs(r.text, "lxml")

    #except Exception as ex:
        #print("Your ranobe isn't in database") 


    #try:
        start_read = soup.select(".FicContentsChapterName > a")[ranobe_cahpter-1]
        r = requests.get("https://ranobe.me" + start_read.get("href"), headers)  
        soup = bs(r.text, "lxml")
                
        content = soup.select_one(".ReadContent").text
        return content

    #except Exception as ex:
     #   print(ex)       


class logic(QMainWindow):
    def __init__(self, parent=None):
        super(logic, self).__init__(parent=parent)
        loadUi("welcome.ui", self)
        self.read_ranobe_ui = read_ranobe.Ui_MainWindow()
        self.chapter = 0
        self.title = ""

        self.connect()

    def connect(self):
        self.pushButton.clicked.connect(self.find_ranobe)  

    def find_ranobe(self): 
            with open("data/titles.json", "r") as file:
                src = json.load(file)

        #try:       
            r = requests.get(src[self.title_inp.text()], headers)  
            soup = bs(r.text, "lxml")

        #except Exception as ex:
            #print("Your ranobe isn't in database") 


        #try:
            self.chapter = int(self.chapters_inp.text())            
            self.title = self.title_inp.text()
            

            self.read_ranobe_ui.setupUi(self)
            self.read_ranobe_ui.label.setText(get_title(self.title, self.chapter)) 
            self.connect2() 
              

        #except Exception as ex:
         #   print("Your chapter isn't in database because", ex)      

    def next_ranobe(self):
        print("next")
        self.read_ranobe_ui.label.setText(get_title(self.title, self.chapter-1)) 
        self.read_ranobe_ui.next_btn.clicked.connect(self.next_ranobe)   
        
       
    def connect2(self):
        self.read_ranobe_ui.next_btn.clicked.connect(self.next_ranobe)    



if __name__ == "__main__":
    app = QApplication(sys.argv)    
    log = logic()
    log.show()
    sys.exit(app.exec_())       
