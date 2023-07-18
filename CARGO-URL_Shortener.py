import customtkinter as ctk
import requests
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # (Themed Tkinter)
import sqlite3 as sql
from pyshorteners import Shortener as Sh

ctk.set_appearance_mode("dark")  # Sets appearance to 'dark' in customtkinter
ctk.set_default_color_theme("green")  # Sets color theme to 'green' in customtkinter

# Creating (if the file doesn't exist already) and connecting to a .db file
conn = sql.connect("Shurl.db")
cur = conn.cursor()
# Creates a table in the above .db file if it doesn't already exist
cur.execute('''CREATE TABLE IF NOT EXISTS urls(id INTEGER PRIMARY KEY AUTOINCREMENT, short_url TEXT, og_url TEXT)''')


# Main class containing both the frames
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("URL Shortener")
        self.geometry("1280x720")
        self.minsize(1100, 720)

        # Refreshes and displays all elements in the database on the table
        def display():
            cur.execute("SELECT short_url, og_url FROM urls ORDER BY id DESC")  # Displays recent URLs first
            rows = cur.fetchall()
            conn.commit()
            table.delete(*table.get_children())
            for row in rows:
                table.insert("", tk.END, values=row)

        # Validates the URL
        def is_real(link):
            try:
                resp = requests.head(link)
                stat = resp.status_code
                check = requests.codes
                if stat == check.ok or stat == check.found or stat == check.not_allowed or stat == check.forbidden:
                    try:
                        Sh().tinyurl.short(link)
                        return True
                    except requests.exceptions.ReadTimeout:
                        return False
                else:
                    return False
            except requests.exceptions.RequestException:
                return False

        # Inserts the shortened and original URLs into the database and calls the display() function
        def insert(link_short, link):
            cur.execute("INSERT INTO urls (short_url, og_url) VALUES (?, ?)", (link_short, link))
            conn.commit()
            display()

        # Shortens the URL and calls the insert() and is_real() functions
        def cargo():
            link = self.blink.get()
            self.slink.set('')
            if is_real(link):
                self.slink.set(Sh().tinyurl.short(link))
                if self.check1.get() == 0:
                    link_short = self.slink.get()
                    insert(link_short, link)
            else:
                messagebox.showwarning("Invalid Input", "Please enter a valid URL or check your network connection")

        # Implementation of copy functionality within the table via a dropdown menu
        def copy_text():
            selected_item = table.focus()
            if selected_item:
                value = table.set(selected_item, "short-url")
                if value:
                    frame.clipboard_clear()
                    frame.clipboard_append(value)

        # Truncates the urls table in the database clearing all entries, and calls the display() function
        def clear_tab():
            choice = messagebox.askyesno("Deletion", "Are you sure you want to delete your history?")
            if choice:
                cur.execute("DELETE FROM urls")
                conn.commit()
                display()

        # Creates a simple but lengthy border that can be used for string value arguments
        def bigline():
            border = ''
            for x in range(500):
                border += '_'
            return border

        # Adds weight to a column in customtkinter's grid system to give it more preference
        self.grid_columnconfigure(0, weight=1)

        # The label consisting of the title
        self.logo = ctk.CTkLabel(self,
                                 text="CARGO",
                                 font=("Segoe UI Light", 40))

        self.logo.grid(sticky="e",
                       padx=15, pady=(15, 0))

        # Label that acts as a simple border
        self.label0 = ctk.CTkLabel(self,
                                   text=bigline(),
                                   font=("Segoe UI", 10),
                                   text_color="#5ba378")

        self.label0.grid(row=1,
                         column=0,
                         sticky="ew",
                         padx=15, pady=(0, 15))

        # Label prompting the user to enter a link
        self.label1 = ctk.CTkLabel(self,
                                   text="Enter a link to shorten:",
                                   font=("Segoe UI", 18),
                                   text_color="#70cc95")

        self.label1.grid(row=2,
                         column=0,
                         sticky="w",
                         padx=18, pady=(5, 0))

        # Entry handling the inputting of the link
        self.blink = ctk.StringVar()
        self.blink_entry = ctk.CTkEntry(self,
                                        width=650,
                                        height=32,
                                        textvariable=self.blink,
                                        font=("Calibri", 15))

        self.blink_entry.grid(row=3,
                              column=0,
                              sticky="ew",
                              padx=15, pady=10)

        # Checkbox allowing the user to not save shortened URLs in the database
        self.check1 = ctk.CTkCheckBox(self,
                                      text="Don't save in history",
                                      font=("Calibri", 19),
                                      corner_radius=100,
                                      checkmark_color="black",
                                      border_color="#5ba378")

        self.check1.grid(padx=18, pady=(5, 0),
                         sticky="w")

        # Label announcing the shortened URL
        self.label2 = ctk.CTkLabel(self,
                                   text="Shortened URL:",
                                   font=("Segoe UI", 18),
                                   text_color="#70cc95")

        self.label2.grid(sticky="ns",
                         padx=18, pady=(0, 0))

        # Entry that displays the output in the form of the shortened URL
        self.slink = ctk.StringVar()
        self.slink_entry = ctk.CTkEntry(self,
                                        width=300,
                                        height=32,
                                        textvariable=self.slink,
                                        justify="center",
                                        state="readonly",
                                        font=("Calibri", 17),
                                        corner_radius=100,
                                        fg_color="#2e4d36",
                                        border_color="#5ba378",
                                        text_color="#d4d4d4")

        self.slink_entry.grid(row=6,
                              column=0,
                              sticky="ns",
                              padx=15, pady=10)

        # Button with the cargo (URL Shortening) function bound to it
        self.shorts_button = ctk.CTkButton(self,
                                           text="Shorten URL",
                                           command=cargo,
                                           text_color="black",
                                           hover_color="#90f0b6",
                                           font=("TKDefaultFont", 15),
                                           corner_radius=15)

        self.shorts_button.grid(padx=20, pady=20)

        # Creates a second frame for the Treeview that will act as the table
        frame = ctk.CTkFrame(self)
        frame.grid(padx=10, pady=10)

        # Creates a Scrollbar widget and associate it with the Treeview
        scrollbar = ctk.CTkScrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Creates a Style in Themed Tkinter
        style = ttk.Style()
        style.theme_use('default')

        # Creates a Treeview widget with static dimensions
        table = ttk.Treeview(frame,
                             columns=("short-url", "og-url"),
                             show="headings",
                             height=4,
                             style="Custom.Treeview")

        table.column("short-url", width=200)
        table.column("og-url", width=850)
        table.heading("short-url", text="Shortened URL")
        table.heading("og-url", text="Original URL")
        table.pack(side=tk.LEFT, fill=tk.Y)

        # Creates a dropdown menu
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Copy Shortened URL", command=copy_text)
        menu.add_command(label="Clear History", command=clear_tab)

        # Binds the right-click event to show the dropdown menu
        def show_menu(event):
            if table.identify_region(event.x, event.y) == "cell":
                menu.post(event.x_root, event.y_root)

        table.bind("<Button-3>", show_menu)

        # Configures a style for the treeview elements to follow
        style.configure("Custom.Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=0,
                        padding=1,
                        font=("Arial", 10))

        # Configures a style for the treeview headers to follow
        style.configure("Treeview.Heading",
                        background="#5ba378",
                        foreground="black",
                        bordercolor="#343638",
                        borderwidth=0,
                        font=("TKDefaultFont", 11),
                        padding=2)

        # Attaches a Scrollbar widget to the Treeview
        table.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=table.yview)

        # Button with an event attached to clear the user's history
        self.clr_bt = ctk.CTkButton(self,
                                    text="Clear History",
                                    command=clear_tab,
                                    text_color="black",
                                    hover_color="#90f0b6",
                                    font=("TKDefaultFont", 16))

        self.clr_bt.grid(padx=20, pady=(20, 15))

        # Label that acts as a simple border
        self.label01 = ctk.CTkLabel(self,
                                    text=bigline(),
                                    font=("Segoe UI", 10),
                                    text_color="#5ba378")

        self.label01.grid(sticky="ew",
                          padx=15, pady=0)

        # Crediting statement
        self.madeby = ctk.CTkLabel(self,
                                   text="A simple URL shortener created by Chris Daniel Wilson",
                                   font=("Arial", 15, "italic"))

        self.madeby.grid(sticky="ws",
                         padx=15)

        # Filling the table
        display()


# Running the GUI in a loop
app = App()
app.mainloop()

# Closing the cursor and the connection
cur.close()
conn.close()
