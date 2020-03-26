"""
 OpenSQLManager
 @author Gustavo Novaro
 @license MIT
 @version 0.1.3
"""
import os
import sys
import pymysql
import json
import i18n
import tkinter as tk

from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import *

from i18n import *


class SQL:
    keywords = [
        'ADD',
        'ALTER',
        'BTREE',
        'BY',
        'CREATE',
        'CHAR',
        'CHARSET',
        'DROP',
        'ENGINE',
        'FROM',
        'UPDATE',
        'SELECT',
        'TABLE',
        'PROCEDURE',
        'FUNCTION',
        'INDEX',
        'VARCHAR',
        'UNIQUE',
        'USING',
        'NOT',
        'NULL',
        'IF',
        'UNIQUE',
        'PRIMARY',
        'KEY',
        'GROUP'
        'ORDER',
        'ASC',
        'DESC',
        'DEFAULT'
    ]


class Connection:
    _host = None
    _db = None
    _user = None
    _password = None
    _port = None


# Main Class
class OpenSQLManager:
    TITLE = 'OpenSQLManager | Open Source SQL Administration Manager'
    _title = TITLE
    _application = None
    _path = None
    _window = None
    _locale = None
    _locales = ['en', 'es']
    _tree_view = None

    _query_frame = None
    _query_text = None

    # Editor
    _file_name = None  # Must be a collection..? for multitabs

    # Constructor
    def __init__(self):
        self._window = Tk()
        self._window.geometry("1024x768")
        # Default maximized
        self._window.attributes('-zoomed', True)
        self._window.title(self._title)
        self._path = os.path.abspath(os.getcwd())
        print(self._path)
        icon_path = os.path.join(self._path, 'db.png')
        icon_img = PhotoImage(file=icon_path)
        self._window.iconphoto(True, icon_img)
        self.main_menu_render()
        # Render sidebar
        self.sidebar_render()
        self.query_render()
        self.status_bar_render()
        self._window.mainloop()

    def sidebar_render(self):
        sidebar = LabelFrame(self._window, text='Connections')
        sidebar.pack(side=LEFT)
        # sidebar.grid(row=1, column=0, pady=20, sticky=W)

        self._tree_view = ttk.Treeview(sidebar, height=240)
        self._tree_view.heading('#0', text="Databases")
        self._tree_view.pack(side=LEFT)
        # self._tree_view.grid(row=1, column=0)

    def query_render(self):
        self._query_frame = LabelFrame(self._window, text='Query')
        self._query_frame.pack(side=LEFT, fill=X)
        # query_frame.grid(row=1, column=1, pady=20, sticky=E)
        # Crear caja de texto.
        self._query_text = scrolledtext.ScrolledText(self._query_frame, width=400, height=240, wrap=tk.WORD, undo= True)
        self._query_text.pack(side=LEFT, fill=X)

    # def load_lang(self):
    # i18n.set('file_format', 'json')
    # i18n.set('locale', 'es')
    # i18n.set('fallback', 'en')
    # i18n.load_path.('lang')

    def change_locale(self, locale):
        if locale not in self._locales:
            raise NameError
        self._locale = locale
        # TIMEZONE = TIMEZONES[LOCALE]

    def main_menu_render(self):
        # create a toplevel menu
        main_menu = Menu(self._window)
        # File
        file_menu = Menu(main_menu, tearoff=0)
        file_menu.add_command(label="New", command=self.donothing)
        file_menu.add_command(label="Open", command=self.open)
        file_menu.add_command(label="Save", command=self.save)
        file_menu.add_command(label="Save as...", command=self.donothing)
        file_menu.add_command(label="Close", command=self.donothing)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit)

        main_menu.add_cascade(label="File", menu=file_menu)

        # Edit
        edit_menu = Menu(main_menu, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.donothing)
        edit_menu.add_separator()

        edit_menu.add_command(label="Cut", command=self.donothing)
        edit_menu.add_command(label="Copy", command=self.donothing)
        edit_menu.add_command(label="Paste", command=self.donothing)
        edit_menu.add_command(label="Delete", command=self.donothing)
        edit_menu.add_command(label="Select All", command=self.donothing)
        main_menu.add_cascade(label="Edit", menu=edit_menu)

        # Designer
        designer_menu = Menu(main_menu, tearoff=0)
        designer_menu.add_command(label="EER", command=self.designer_render)
        main_menu.add_cascade(label="Designer", menu=designer_menu)

        # About
        about_menu = Menu(main_menu, tearoff=0)
        about_menu.add_command(label="Help", command=self.donothing)
        about_menu.add_separator()
        about_menu.add_command(label="About", command=self.about)
        main_menu.add_cascade(label="About", menu=about_menu)

        # display the menu
        self._window.config(menu=main_menu)

    def status_bar_render(self):
        status_bar = Label(self._window, text="Not connected", bd=1, relief=SUNKEN, anchor=W)
        status_bar.pack(side=BOTTOM, fill=X)

    def open(self):
        file = filedialog.askopenfile(filetypes=[("SQL files", ".sql")])
        file_name = file.name
        self._query_text.insert(INSERT, file.read())

    def save(self):
        if self._file_name is None:
            path = filedialog.asksaveasfilename(filetypes=[("SQL files", ".sql")])
            self._file_name = path
            write = open(self._file_name, mode='w')
            text = self._query_text.get("1.0", tk.END)
            lines = write.write(text)

    def exit(self):
        ans = messagebox.askquestion(title="Exit", message="Do you want to exit?", icon='warning')
        if ans == 'yes':
            self._window.destroy()

    def about(self):
        messagebox.showinfo("About", self.TITLE + "\nCreated in Python using Tkinter\nby Gustavo Novaro")

    def donothing(self):
        # nothig
        print("")

    def designer_render(self):
        db_designer = DbDesigner(self._window)


class DbDesigner:
    def __init__(self, application):
        self.application = application
        self.application.geometry("300x300+500+200")
        self.application["bg"] = "navy"


# Run App
application = OpenSQLManager()
