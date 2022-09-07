import requests
from bs4 import BeautifulSoup

url = 'https://isle.island.edu.hk/login/index.php'
values = {'username': open("login.txt", "r").readlines()[0].replace("\n", ""),
          'password': open("login.txt", "r").readlines()[1].replace("\n", "")}

classes = []
with requests.Session() as s:
    r = s.post(url, data=values)
    #print(r.text)
    index_page = s.get("https://isle.island.edu.hk/")
    soup = BeautifulSoup(index_page.text, 'html.parser')
    mydivs = soup.find_all("div", {"class": "greeting"})
    try:
        tdTags = mydivs[0].find_all("div")
    except IndexError:
        raise KeyError("Invalid username/password")
    correctdiv = tdTags[0]
    txt = correctdiv.text
    
    today = correctdiv.text[:txt.find("DawnBreakfast")]
    today_table = correctdiv.find_all("table")[0]
    tr = today_table.find_all("tr")
    for a in tr[1]:
        classes.append({
            "class": a.text[:7],
            "room": a.text[10:]
        })
    
    
    index_page = s.get("https://isle.island.edu.hk/local/mis/reports/unitview.php")
    soup = BeautifulSoup(index_page.text, 'html.parser')
    spans = soup.find_all("span", {"class": "title"})
    yeargroup = ""
    for a in spans:
        if "Yr" in a.text:
            yeargroup = a.text.replace("Yr ", "")

    if int(yeargroup) == 11:
        mydivs = soup.find_all("div", {"class": "row-fluid"})
        tablesneeded = []
        for a in mydivs[1]:
            table = a.find_all("table")
            tablesneeded.append(table[0])
        
        tr1 = tablesneeded[0].find_all("tr")
        tr1.pop(0)
        
        for tr1a in tr1:
            tr1barray = []
            for tr1b in tr1a:
                tr1barray.append(tr1b.text)
            try:
                print(f"{tr1barray[0]}:\nYellis predicted: {tr1barray[1]}\nActual Grade: {tr1barray[3]}\n")
            except IndexError:
                print(f"{tr1barray[0]}:\nYellis predicted: {tr1barray[1]}\nActual Grade: Missing\n")
    else:
        raise KeyError("Grades could not be loaded because format has not been initiated. Please contact the administrator of this program")

from tkinter import *
window=Tk()
window.title('Timetable')
window.geometry("250x350")
classccount = 1
lbl=Label(window, text=f"{today}", fg='black', font=("Helvetica", 16))
lbl.place(x=5, y=5)
cury = 30
for classc in classes:
    lbl=Label(window, text=f"Period {classccount}: {classc['class']} in room {classc['room']}", fg='red', font=("Helvetica", 16))
    lbl.place(x=5, y=cury)
    cury+=30
    classccount += 1
    
def exitProgram():
   exit()

btn = Button(window, text="Exit", command=exitProgram)
btn.place(x=5, y=270)
window.mainloop()
