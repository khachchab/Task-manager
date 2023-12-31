#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
import tkcalendar as cal
from tkinter import filedialog as fd
import json
import os
from datetime import date
from tkinter import messagebox as mb

font = "Arial"
tasks = []
newTask = {"title": "", "description": "", "start": None, "end": None}
currFile = None
changed = False
title = "Untitled"

AboutDisplayed = False
HelpDisplayed = False


def get_desc():
    return desc.get("1.0", tk.END+'-1c')


def save(event=None):
    global changed
    if titre.get() == "":
        sv.set("Le Titre???!")
    elif dated.get_date() > datef.get_date():
        sv.set("Date de Fin plus petite que la Date Debut!")
    elif get_desc() == "":
        sv.set("description vide!")
    else:
        sv.set("")
        task = {}
        task["title"] = titre.get()
        task["description"] = get_desc()
        task["start"] = str(dated.get_date())
        task["end"] = str(datef.get_date())
        act = listbox.get(listbox.curselection())

        if act == "+":
            listbox.delete(len(tasks))
            listbox.insert(tk.END, str(len(tasks)+1) + "- " + task["title"])
            tasks.append(task)
            listbox.insert(tk.END, "+")
            listbox.select_set(len(tasks)-1)
        else:
            index = int(act.split("-")[0])
            listbox.delete(index-1)
            listbox.insert(index-1, str(index) + "- " + task["title"])
            tasks[index - 1] = task
            listbox.select_set(index - 1)
        prog.title("TaskManager" + " - " + title + " *")
        changed = True
        B2["state"] = "normal"


def saveInFile(event=None):
    global currFile, tasks, title, changed
    if currFile is None:
        filename = fd.asksaveasfilename(initialdir="./Data",
                                        defaultextension=".json",
                                        filetypes=[("JSON Files", "*.json")])
        if filename == "" or len(filename) == 0:
            return
        with open(filename, "w") as f:
            json.dump(tasks, f)
            currFile = filename
            prog.title("TaskManager" + " - " + os.path.basename(filename))
            title = os.path.basename(filename)
    else:
        with open(currFile, "w") as f:
            json.dump(tasks, f, indent=4)
            prog.title("TaskManager" + " - " + title)
    filemenu.entryconfigure(3, state="normal")
    changed = False


def saveAs(event=None):
    global currFile, title, tasks, changed

    filename = fd.asksaveasfilename(initialdir="./Data",
                                    defaultextension=".json",
                                    filetypes=[("JSON Files", "*.json")])
    if filename == "" or len(filename) == 0:
        return
    with open(filename, "w") as f:
        json.dump(tasks, f)
        currFile = filename
        prog.title("TaskManager" + " - " + os.path.basename(filename))
        filemenu.entryconfigure(3, state="normal")
    title = os.path.basename(filename)
    changed = False


def openFile(event=None):
    global currFile, tasks, title, changed
    filename = fd.askopenfilename(initialdir="./Data",
                                  defaultextension=".json",
                                  filetypes=[("JSON Files", "*.json")])
    if filename == "" or len(filename) == 0:
        return
    res = closeFile()
    if not res:
        return
    with open(filename, "r") as f:
        changed = False
        tasks = json.load(f)
        prog.title("TaskManager" + " - " + os.path.basename(filename))
        title = os.path.basename(filename)
        currFile = filename
        listbox.delete(0, tk.END)
        for i, item in enumerate(tasks):
            listbox.insert(tk.END, str(i+1) + "- " + item["title"])
        listbox.insert(tk.END, "+")
        listbox.select_set(0)
        if len(tasks) > 0:
            svt.set(tasks[0]["title"])
            desc.delete(1.0, "end")
            desc.insert(1.0, tasks[0]["description"])
            dated.set_date(date.fromisoformat(tasks[0]["start"]))
            datef.set_date(date.fromisoformat(tasks[0]["end"]))
            filemenu.entryconfigure(3, state="normal")
            B2["state"] = "normal"
        else:
            svt.set("")
            desc.delete(1.0, "end")
            dated.set_date(date.today())
            datef.set_date(date.today())
            filemenu.entryconfigure(3, state="normal")
            B2["state"] = "disabled"


def onselect(event=None):
    global newTask
    if listbox.curselection() == tuple():
        listbox.select_set(tk.ACTIVE)
        return
    curr = listbox.get(listbox.curselection())
    if curr == "+":
        svt.set(newTask["title"])
        desc.delete(1.0, "end")
        desc.insert(1.0, newTask["description"])
        dated.set_date(date.today())
        datef.set_date(date.today())
        B2["state"] = "disabled"
    else:
        index = int(curr.split("-")[0])-1
        B2["state"] = "normal"
        if index < len(tasks):
            svt.set(tasks[index]["title"])
            desc.delete(1.0, "end")
            desc.insert(1.0, tasks[index]["description"])
            dated.set_date(date.fromisoformat(tasks[index]["start"]))
            datef.set_date(date.fromisoformat(tasks[index]["end"]))


def up(event=None):
    c = listbox.curselection()[0]
    if c > 0:
        listbox.selection_clear(0, 'end')
        listbox.select_set(c-1)
        onselect()


def down(event=None):
    global tasks
    c = listbox.curselection()[0]
    if c < len(tasks):
        listbox.selection_clear(0, 'end')
        listbox.select_set(c+1)
        onselect()


def closeFile(event=None):
    global currFile, tasks, changed, title

    if changed:
        msg = "T sur??"
        answer = mb.askyesnocancel(title="TaskManager - " + title, message=msg)
        if answer is None:
            return False
        if answer:
            with open(currFile, "w") as f:
                json.dump(tasks, f, indent=4)

    filemenu.entryconfigure(3, state="disabled")
    svt.set("")
    tasks = []
    desc.delete(1.0, "end")
    listbox.delete(0, tk.END)
    listbox.insert(tk.END, "+")
    currFile = None
    title = "Untitled"
    prog.title("TaskManager" + " - " + title)
    listbox.select_set(0)
    dated.set_date(date.today())
    datef.set_date(date.today())
    B2["state"] = "disabled"
    changed = False
    return True


def removeTask(event=None):
    global tasks, changed, title

    curr = listbox.get(listbox.curselection())
    if curr == "+":
        return
    changed = True
    prog.title("TaskManager" + " - " + title + " *")
    index = int(curr.split("-")[0])
    del tasks[index-1]
    listbox.delete(0, tk.END)
    for i, item in enumerate(tasks):
        listbox.insert(tk.END, str(i+1) + "- " + item["title"])
    listbox.insert(tk.END, "+")
    listbox.select_set(index-1)
    if index-1 >= len(tasks):
        svt.set("")
        desc.delete(1.0, "end")
        dated.set_date(date.today())
        datef.set_date(date.today())
        B2["state"] = "disabled"
    else:
        svt.set(tasks[index-1]["title"])
        desc.delete(1.0, "end")
        desc.insert(1.0, tasks[index-1]["description"])
        dated.set_date(date.fromisoformat(tasks[index-1]["start"]))
        datef.set_date(date.fromisoformat(tasks[index-1]["end"]))


def about(event=None):
    global AboutFrame, AboutDisplayed
    if not AboutDisplayed:
        AboutFrame.grid(row=7, column=0, columnspan=4, sticky="EW")
        AboutDisplayed = True
    else:
        AboutFrame.grid_forget()
        AboutDisplayed = False





def quitApp(event=None):
    global currFile, tasks, changed, title
    if changed:
        if currFile is None:
            msg = "EST CE QUE T VRAIMENT SUR?"
        else:
            msg = "ahh DACCORD T VRAIMENT SUR?"
        answer = mb.askyesnocancel(title="TaskManager - " + title, message=msg)
        if answer is None:
            return
        if answer:
            saveInFile()
    prog.quit()


def printPDF(event=None):
    msg = "ah la c trop!"
    mb.showinfo(title="TaskManager", message=msg)


prog = tk.Tk()
prog.title("TaskManager" + " - " + title)

# Menu

menubar = tk.Menu(prog)
filemenu = tk.Menu(menubar, tearoff=0)

filemenu.add_command(label="Ouvrir",  command=openFile)
filemenu.add_command(label="Engerister", command=saveInFile)
filemenu.add_command(label="Engeristrer sous ...", command=saveAs)
filemenu.add_command(label="Fermer",command=closeFile, state="disabled")
filemenu.add_command(label="Format PDF",command=printPDF)
filemenu.add_separator()
filemenu.add_command(label="Quitter", command=quitApp)
menubar.add_cascade(label="Fichier", menu=filemenu)

prog.config(menu=menubar)

# end Menu configuration

fen = ttk.Frame(prog, padding="10 10 10 10")
fen.pack()

cadre1 = ttk.Frame(fen, padding="5 5 5 5")
cadre1.grid(row=0, column=0, sticky="NWES")

listbox = tk.Listbox(cadre1, height=13, font="Arial", exportselection=0)
listbox.grid(row=0, column=0, sticky="NWES")

listbox.bind('<<ListboxSelect>>', onselect)
listbox.bind('<FocusIn>', lambda e: titre.focus_set())

for i, item in enumerate(tasks):
    listbox.insert(tk.END, str(i+1) + "- " + item["title"])
listbox.insert(tk.END, "+")
listbox.select_set(0)

# cadre 2
cadre2 = ttk.Frame(fen, padding="5 5 5 5")
cadre2.grid(row=0, column=1)

tk.Label(cadre2, text="Titre de tache: ", font="Arial").grid(
    row=0, column=0, columnspan=4, sticky="W")

svt = tk.StringVar()
titre = tk.Entry(cadre2, textvariable=svt, width=50, font="Arial",
                 highlightthickness=1)
titre.grid(row=1, column=0, columnspan=4)

tk.Label(cadre2, text="Date Debut: ", font="Arial").grid(row=2,
                                                         column=0, sticky="W")
dated = cal.DateEntry(cadre2, date_pattern="dd/mm/Y", font="Arial",
                      locale="fr_FR", borderwidth=1)
dated.grid(row=2, column=1)

tk.Label(cadre2, text="Date de Fin: ", font="Arial").grid(row=2, column=2,
                                                       sticky="W")
datef = cal.DateEntry(cadre2, date_pattern="dd/mm/Y", font="Arial",
                      locale="fr_FR", borderwidth=1)
datef.grid(row=2, column=3, sticky="E")

tk.Label(cadre2, text="Description: ", font="Arial").grid(row=3, column=0,
                                                          columnspan=4,
                                                          sticky="W")

desc = tk.Text(cadre2, width=22, height=6, font="Arial", highlightthickness=1)
scrollb = tk.Scrollbar(cadre2, command=desc.yview)
desc['yscrollcommand'] = scrollb.set
scrollb.grid(row=4, column=4, sticky='ns')
desc.grid(row=4, column=0, sticky="EW", columnspan=4)

sv = tk.StringVar()
sv.set("  ")
errLabel = tk.Label(cadre2, textvariable=sv, fg="red")
errLabel.grid(row=5, column=0, sticky="EW", columnspan=4)

B1 = tk.Button(cadre2, text="Valider", command=lambda: save(), font="Arial")
B1.grid(row=6, column=2, sticky="E", columnspan=2)
B2 = tk.Button(cadre2, text="Enlever", command=lambda: removeTask(),
               font="Arial", state="disabled")
B2.grid(row=6, column=0, sticky="W", columnspan=2)

# About Frame
AboutFrame = tk.Frame(fen)

built = tk.Label(AboutFrame, text="(built on 2023-10-25)")
copyRight = tk.Label(AboutFrame, text="Mohamed ELHAFA § Mohamed KHACHCHAB § Manal jawhar(c) 2023")
ttk.Separator(AboutFrame, orient=tk.HORIZONTAL).pack()
built.pack()
copyRight.pack()
tk.Button(AboutFrame, anchor="w",
          command=about).pack(side="right")



# detect window close
prog.protocol("WM_DELETE_WINDOW", quitApp)
prog.mainloop()
