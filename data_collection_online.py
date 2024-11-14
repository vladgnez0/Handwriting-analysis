import json
import time
import tkinter as tk
from pynput import keyboard
import os

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


def writejson(name, lastname):
    data = {
        "name+lastname": name.get() + " " + lastname.get(),
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
    name = name.get()
    lastname = lastname.get()

    folderpath = 'database'
    os.makedirs(folderpath, exist_ok=True)

    filename = f'{name}-{lastname}.json'
    filepath = os.path.join(folderpath, filename)
    if os.path.exists(filepath):
        attempt = 1
        while True:
            new_filename = f'{name}-{lastname}_attempt{attempt}.json'
            new_filepath = os.path.join(folderpath, new_filename)
            if not os.path.exists(new_filepath):
                filepath = new_filepath
                break
            attempt += 1

    with open(filepath, 'a+', encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=2, default=str, ensure_ascii=False)
        json_file.write('\n')
def gui():
    rootroot = tk.Tk()
    x = (rootroot.winfo_screenwidth() - rootroot.winfo_reqwidth()) / 2
    y = (rootroot.winfo_screenheight() - rootroot.winfo_reqheight()) / 2
    rootroot.wm_geometry("+%d+%d" % (x, y))
    rootroot.geometry("400x200")
    appael = tk.Label(text="Напишите около 5 строк текста.\n После закрытия этого окна, нажмите кнопку "'Start'",\n введите имя и фамилию, затем наберите текст и нажмите кнопку "'Stop'".\n Спасибо ")
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
            writejson(name_entry, surname_entry)
            print("all done")
            listener.stop()
            exit(0)

        test()

    btn = tk.Button(text='start', padx="20", pady="8", background="#154", foreground="#ccc", command=listener.start)
    btn1 = tk.Button(text='stop', padx="20", pady="8", background="#710", foreground="#ccc", command=jsonstop)

    name_label = tk.Label(text="Введите имя:", bg="gray39")
    surname_label = tk.Label(text="Введите фамилию:", bg="gray39")


    name_label.place(x=0, y=0)
    surname_label.place(x=0, y=25)

    name_entry = tk.Entry(bg="gray59")
    surname_entry = tk.Entry(bg="gray59")

    text = tk.Text(state="normal", bg="gray59")
    text.place(x=10, y=60, width=400, height=355)

    name_entry.place(x=125, y=0)
    surname_entry.place(x=125, y=25)

    btn.place(x=30, y=420)
    btn1.place(x=110, y=420)


    root.mainloop()


if __name__ == '__main__':
    gui()

