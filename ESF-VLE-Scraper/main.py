import os, json, datetime

now = datetime.datetime.now()
timenow = (int(now.strftime("%H")), int(now.strftime("%M")), int(now.strftime("%S")))
print(timenow)
timetable = [[(8, 20, 0), (9, 0, 0)], [(9, 0, 1), (9, 40, 0),], [(9, 45, 0), (10, 25, 0)], [(10, 25, 1), (11, 0, 0)], [(11, 25, 0), (12, 5, 0)], [(12, 5, 1), (12, 45, 0)], [(13, 40, 0), (14, 20, 0)], [(14, 20, 1), (15, 0, 0)]]

a = json.load(open("settings.json", "r+"))
if not a['reqinstalled']:
    os.system("pip3 install -r requirements.txt")
    a['reqinstalled'] = True
    json.dump(a, open("settings.json", "w"), indent=4)
else:
    print("pip3 installation skipped as requirements are installed")

import requests, sys
from bs4 import BeautifulSoup

args = sys.argv

domain = sys.argv[1]

url = f'https://{domain}/login/index.php'
values = {'username': open("login.txt", "r").readlines()[0].replace("\n", ""),
          'password': open("login.txt", "r").readlines()[1].replace("\n", "")}

classes = []
with requests.Session() as s:
    r = s.post(url, data=values)
    #print(r.text)
    index_page = s.get(f"https://{domain}/")
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
    
    
    index_page = s.get(f"https://{domain}/local/mis/reports/unitview.php")
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
    
if "Friday" in today:
    del classes[-2:]

from tkinter import *
from tkinter import colorchooser
if "--nogui" in args:
    if sys.platform == "darwin":
        try:
            file = open("timetable.txt", "x")
        except FileExistsError:
            os.remove("timetable.txt")
            file = open("timetable.txt", "x")
            
        file.write("Timetable\n")
        classccount = 1
        for classc in classes:
            file.write(f"Period {classccount}: {classc['class']} in room {classc['room']} ({timetable[classccount-1][0]}-{timetable[classccount-1][1]})\n")
            classccount += 1
            
        import subprocess
        subprocess.call(['open', "timetable.txt"])
    else:
        raise IndexError("No GUI mode not supported for windows. Please remove the --nogui tag when running this program")
else:
    a = json.load(open("settings.json", "r+"))
    window=Tk()
    window.title('Timetable')
    window.geometry("250x350")
    window.configure(background=a['backgroundcolour'])
    classccount = 1
    lbl=Label(window, text=f"{today}", fg=a['titlecolour'], font=("Helvetica", 16))
    lbl.place(x=5, y=5)
    cury = 30
    for classc in classes:
        lbl=Label(window, text=f"Period {classccount}: {classc['class']} in room {classc['room']}", fg=a['textcolour'], font=("Helvetica", 16))
        lbl.place(x=5, y=cury)
        cury+=30
        classccount += 1
        
    def exitProgram():
        exit()

    btn = Button(window, text="Exit", command=exitProgram)
    btn.place(x=5, y=270)
    
    def choosetextcolour():
        color_code = colorchooser.askcolor(title ="Choose text colour")
        a['textcolour'] = color_code[1]
        json.dump(a, open("settings.json", "w"), indent=4)
        
    def choosebgcolour():
        color_code = colorchooser.askcolor(title ="Choose background colour")
        a['backgroundcolour'] = color_code[1]
        json.dump(a, open("settings.json", "w"), indent=4)
        
    def choosetitlecolour():
        color_code = colorchooser.askcolor(title ="Choose title colour")
        a['titlecolour'] = color_code[1]
        json.dump(a, open("settings.json", "w"), indent=4)
    
    def okbutton():
        exit("Program closed")
    
    def applychanges():
        new=Toplevel(window)
        new.geometry("400x50")
        new.title("Reload your app to confirm the changes")
        btn = Button(new, text="Ok", command=okbutton)
        btn.place(x=5, y=5)
    
    def settings():
        new= Toplevel(window)
        new.geometry("200x150")
        new.title("Settings")
        btn = Button(new, text="Text Colour Pick", command=choosetextcolour)
        btn.place(x=5, y=5)
        btn = Button(new, text="Background Colour Pick", command=choosebgcolour)
        btn.place(x=5, y=35)
        btn = Button(new, text="Title Colour Pick", command=choosetitlecolour)
        btn.place(x=5, y=65)
        btn = Button(new, text="Apply Changes", command=applychanges)
        btn.place(x=5, y=95)
        
        
    btn = Button(window, text="Settings", command=settings)
    btn.place(x=5, y=290)
    window.mainloop()
