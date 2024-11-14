import json
import time
import tkinter as tk
from pynput import keyboard

import DecisionTreeClassifier
import new
import svm_classifier

import svm

time_between_keys = []
arrTimeOnRel = []
hold_time = []
arrTimeOnPress = []
arrkeys = []


def on_press(key):
    global timeonpress
    arrkeys.append(str(key))
    timeonpress = time.time()
    arrTimeOnPress.append(timeonpress)
    return timeonpress


def on_release(key):
    global timeonrel
    timeonrel = time.time()
    arrTimeOnRel.append(timeonrel)
    difference = timeonrel - timeonpress
    hold_time.append(difference)
    return difference, timeonrel


def writejson():
    data = {
        "keys": arrkeys,
        "time_on_press": arrTimeOnPress,
        "time_on_release": arrTimeOnRel,
        "hold_time": hold_time,
        "time_between_keys": time_between_keys,
    }

    for i in range(len(arrTimeOnRel)):
        if i == 0:
            time_between_keys.insert(i, 0)
        else:
            a = arrTimeOnRel[i] - arrTimeOnPress[i - 1]
            time_between_keys.insert(i, a)
    DecisionTreeClassifier.predict(data)
def gui():
    rootroot = tk.Tk()
    x = (rootroot.winfo_screenwidth() - rootroot.winfo_reqwidth()) / 2
    y = (rootroot.winfo_screenheight() - rootroot.winfo_reqheight()) / 2
    rootroot.wm_geometry("+%d+%d" % (x, y))
    rootroot.geometry("400x200")
    appael = tk.Label(text="Напишите около 5 строк текста.\n После закрытия этого окна, нажмите кнопку "'Start'",\n  наберите текст и нажмите кнопку "'Stop'".\n Спасибо ")
    appael.grid()
    rootroot.mainloop()

    root = tk.Tk()
    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
    root.wm_geometry("+%d+%d" % (x, y))
    root.geometry("500x500")
    root["bg"] = "gray39"
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release,
    ) as listener:
        listener.join

    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release,
        suppress=False)
    listener.stop

    def jsonstop():
        def test():
            writejson()
            print("all done")
            listener.stop()
            exit(0)

        test()

    btn = tk.Button(text='start', padx="20", pady="8", background="#154", foreground="#ccc", command=listener.start)
    btn1 = tk.Button(text='stop', padx="20", pady="8", background="#710", foreground="#ccc", command=jsonstop)




    name_entry = tk.Entry(bg="gray59")
    surname_entry = tk.Entry(bg="gray59")

    text = tk.Text(state="normal", bg="gray59")
    text.place(x=10, y=60, width=400, height=355)


    btn.place(x=30, y=420)
    btn1.place(x=110, y=420)


    root.mainloop()


if __name__ == '__main__':
    gui()

