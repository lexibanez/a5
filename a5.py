'''This module is the entry point for the Direct
Messaging Chat application. It contains the main function
that creates the main window for the application and runs
the main event loop. The main window is created using the tkinter
library'''
import tkinter as tk
from tkinter import ttk
from gui import MainApp


def main():

    main = tk.Tk()
    style = ttk.Style(main)
    style.theme_use('clam')
    main.configure(bg='gray9')
    main.title("Direct Messenging Chat")
    main.geometry("720x480")
    main.option_add('*tearOff', False)
    app = MainApp(main)
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    main.mainloop()


if __name__ == '__main__':
    main()
