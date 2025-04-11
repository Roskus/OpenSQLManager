"""
 OpenSQLManager
 @author Gustavo Novaro
 @license MIT
 @version 1.0.1
"""
import os
import sys
import pymysql
import i18n
import yaml
import tkinter as tk

from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import *

from i18n import *
from version import VERSION_STR


class SQL:
    keywords = [
        'ADD',
        'ALTER',
        'AND',
        'AS',
        'ASC',
        'AVG',
        'BETWEEN',
        'BTREE',
        'BY',
        'CASE',
        'COUNT',
        'CREATE',
        'CHAR',
        'CHARSET',
        'CONSTRAINT',
        'DATABASE',
        'DECIMAL',
        'DEFAULT',
        'DELETE',
        'DESC',
        'DISTINCT',
        'DROP',
        'END',
        'ENGINE',
        'FROM',
        'FULL',
        'FUNCTION',
        'GROUP'
        'HAVING',
        'IF',
        'IN',
        'INDEX',
        'INSERT',
        'INTO',
        'JOIN',
        'KEY',
        'LEFT',
        'LIKE',
        'LIMIT',
        'MAX',
        'MIN',
        'NOT',
        'NULL',
        'ON',
        'OR',
        'ORDER',
        'OUTER',
        'PRIMARY',
        'PROCEDURE',
        'RIGHT',
        'SELECT',
        'SUM',
        'TABLE',
        'THEN',
        'TRUNCATE',
        'UPDATE',
        'USING',
        'UNION',
        'UNIQUE',
        'VARCHAR',
        'VALUES',
        'VIEW',
        'WHERE',
        'WHEN',
        'NOW',
        'DATE',
        'TIME',
        'YEAR',
        'MONTH',
        'DAY',
        'HOUR',
        'MINUTE',
        'SECOND',
        'MICROSECOND',
        'RETURN',
        'SET',
        'INTEGER',
        'TEXT',
        'REAL',
        'FLOAT',
        'DOUBLE',
        'DECIMAL',
        'BOOLEAN',
        'BLOB',
        'TRIGGER',
        'FOREIGN',
        'KEYS',
        'DEFINER'
    ]


class Connection:
    _name = None
    _db = None
    _type = None


class MySQLConnection(Connection):
    _host = None
    _user = None
    _password = None
    _port = None

    def __init__(self):
        self._type = 'mysql'


class SQLite(Connection):
    def __init__(self):
        self._type = 'sqlite'


class Config:
    @staticmethod
    def load():
        with open(r'config.yaml') as file:
            return yaml.load(file, Loader=yaml.FullLoader)


# Main Class
class OpenSQLManager:
    TITLE = 'OpenSQLManager | Open Source SQL Administration Manager'
    _title = 'Untitled* - ' + TITLE
    _application = None
    _path = None
    _window = None
    _locale = None
    _locales = ['en', 'es']
    _tree_view = None
    _config = None

    _query_frame = None
    _query_text = None

    # Editor
    _file_name = None  # Must be a collection..? for multitabs

    # Constructor
    def __init__(self):
        # Load Configuration
        self._config = Config.load()
        print(self._config)

        # Get app path
        self._path = os.path.abspath(os.getcwd())
        print(self._path)

        # Setting i18n file format
        i18n.load_path.append('./locale')
        i18n.set('locale', self._config["locale"]["lang"])
        i18n.set('fallback', 'en')

        # Set UI
        self._window = Tk()
        self._window.geometry("1024x768")
        # Default maximized
        self._window.attributes('-zoomed', True)
        self._window.title(self._title)

        # Set app icon
        icon_path = os.path.join(self._path, 'db.png')
        icon_img = PhotoImage(file=icon_path)
        self._window.iconphoto(True, icon_img)

        # Render menu
        self.main_menu_render()

        # Render sidebar
        self.sidebar_render()
        self.query_render()
        self.status_bar_render()
        self._window.mainloop()

    def sidebar_render(self):
        sidebar = LabelFrame(self._window, text='Connections')
        sidebar.pack(side=tk.LEFT)
        # sidebar.grid(row=1, column=0, pady=20, sticky=W)

        self._tree_view = ttk.Treeview(sidebar, height=240)
        self._tree_view.heading('#0', text="Databases")
        self._tree_view.pack(side=tk.LEFT)
        # self._tree_view.grid(row=1, column=0)

    def query_render(self):
        self._query_frame = LabelFrame(self._window, text='Query')
        self._query_frame.pack(side=tk.LEFT, fill=tk.X)
        # query_frame.grid(row=1, column=1, pady=20, sticky=E)
        # Crear caja de texto.
        self._query_text = scrolledtext.ScrolledText(self._query_frame, width=400, height=240, wrap=tk.WORD, undo=True)
        self._query_text.pack(side=tk.LEFT, fill=tk.X)

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
        file_menu.add_command(label=i18n.t("osqlm.New"), command=self.donothing, accelerator='Ctrl+N')
        file_menu.add_command(label=i18n.t("osqlm.Open"), command=self.open, accelerator='Ctrl+O')
        file_menu.add_command(label=i18n.t("osqlm.Save"), command=self.save, accelerator='Ctrl+S')
        file_menu.add_command(label=i18n.t("osqlm.Save as"), command=self.donothing)
        file_menu.add_command(label=i18n.t("osqlm.Close"), command=self.donothing)
        file_menu.add_separator()
        file_menu.add_command(label=i18n.t("osqlm.Exit"), command=self.exit, accelerator='Alt+F4')

        main_menu.add_cascade(label=i18n.t("osqlm.File"), menu=file_menu)

        # Edit
        edit_menu = Menu(main_menu, tearoff=0)
        edit_menu.add_command(label=i18n.t("osqlm.Undo"), command=self.donothing, accelerator='Ctrl+Z')
        edit_menu.add_command(label=i18n.t("osqlm.Redo"), command=self.donothing, accelerator='Ctrl+R')
        edit_menu.add_separator()

        edit_menu.add_command(label=i18n.t("osqlm.Cut"), command=self.donothing, accelerator='Ctrl+X')
        edit_menu.add_command(label=i18n.t("osqlm.Copy"), command=self.donothing, accelerator='Ctrl+C')
        edit_menu.add_command(label=i18n.t("osqlm.Paste"), command=self.donothing, accelerator='Ctrl+P')
        edit_menu.add_command(label=i18n.t("osqlm.Delete"), command=self.donothing)
        edit_menu.add_command(label=i18n.t("osqlm.Select all"), command=self.donothing, accelerator='Ctrl+A')
        main_menu.add_cascade(label=i18n.t("osqlm.Edit"), menu=edit_menu)

        # Designer
        designer_menu = Menu(main_menu, tearoff=0)
        designer_menu.add_command(label="EER", command=self.designer_render)
        main_menu.add_cascade(label=i18n.t("osqlm.Designer"), menu=designer_menu)

        # About
        about_menu = Menu(main_menu, tearoff=0)
        about_menu.add_command(label=i18n.t("osqlm.Help"), command=self.donothing)
        about_menu.add_separator()
        about_menu.add_command(label=i18n.t("osqlm.About"), command=self.about)
        main_menu.add_cascade(label=i18n.t("osqlm.About"), menu=about_menu)

        # display the menu
        self._window.config(menu=main_menu)

    def status_bar_render(self):
        status_bar = Label(self._window, text="Not connected", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def open(self):
        file = filedialog.askopenfile(filetypes=[("SQL files", ".sql")])
        self._file_name = file.name
        self._query_text.insert(tk.INSERT, file.read())

    def save(self):
        if self._file_name is None:
            path = filedialog.asksaveasfilename(filetypes=[("SQL files", ".sql")])
            self._file_name = path
            write = open(self._file_name, mode='w')
            text = self._query_text.get("1.0", tk.END)
            lines = write.write(text)

    def exit(self):
        ans = messagebox.askquestion(title=i18n.t("osqlm.Exit"), message=i18n.t("osqlm.Do you want to exit?"), icon='warning')
        if ans == 'yes':
            self._window.destroy()

    def about(self):
        messagebox.showinfo(i18n.t("osqlm.About"), 
                           self.TITLE + 
                           f"\nVersion: {VERSION_STR}" +
                           "\nCreated in Python using Tkinter" +
                           "\nby Gustavo Novaro")

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
