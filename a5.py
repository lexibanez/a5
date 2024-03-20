import tkinter as tk
from tkinter import ttk
from gui import *


def main():

    main = tk.Tk()

    style = ttk.Style(main)
    style.theme_use('clam')
    main.configure(bg='gray9')
    main.title("ICS 32 Distributed Social Messenger")
    main.geometry("720x480")
    main.option_add('*tearOff', False)
    app = MainApp(main)
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    main.mainloop()

if __name__ == '__main__':
    main()