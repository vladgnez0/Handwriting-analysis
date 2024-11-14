import DecisionTreeClassifier
import  data_collection_online
from tkinter import *

import new
import knc

import auth_enter
import svm


def reg():
    global window
    window.destroy()
    data_collection_online.gui()
def auth():
    global window
    window.destroy()
    auth_enter.gui()
def gui_start(window):
    DecisionTreeClassifier.start()
    window.geometry('400x400')
    btn_reg =  Button(window,text= "Регистрация",bg="green",command=reg).place(relx= 0.37,rely=0.5)
    btn_auth = Button(window,text= "Проверка",bg="green",command=auth).place(relx= 0.37,rely=0.6)
    text_top = Label(window,text="Меню авторизации").place(relx=0.35,rely=0)

    window.mainloop()
window = Tk()
gui_start(window)
