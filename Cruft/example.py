import customtkinter as ctk
import requests
import tkinter as tk
from tkinter import ttk
import sqlite3 as sql
from pyshorteners import Shortener as Sh

# Creating (if the file doesn't exist already) and connecting to a .db file
conn = sql.connect("C:\\SQLITE\\Shurl.db")
cur = conn.cursor()
# Creates a table in the above .db file if it doesn't already exist
cur.execute('''CREATE TABLE IF NOT EXISTS urls(id INTEGER PRIMARY KEY AUTOINCREMENT, short_url TEXT, og_url TEXT)''')


# Main class containing both the frames
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("URL Shortener")
        self.geometry("1040x500")

        # Refreshes and displays all elements in the database on the table
        def display():
            cur.execute("SELECT short_url, og_url FROM urls")
            rows = cur.fetchall()
            conn.commit()
            table.delete(*table.get_children())
            for row in rows:
                table.insert("", tk.END, values=row)

        # Validates the URL
        def is_real(link):
            try:
                resp = requests.head(link)
                return resp.status_code == requests.codes.ok
            except requests.exceptions.RequestException:
                return False

        # Inserts the shortened and original URLs into the database
        def insert(link_short, link):
            cur.execute("INSERT INTO urls (short_url, og_url) VALUES (?, ?)", (link_short, link))
            conn.commit()
            display()

        # Shortens the URL and calls the insert() and is_real() functions
        def button_pressed():
            link = self.blink.get()
            self.slink.set('')
            if is_real(link):
                self.disclaimer.set('')
                self.slink.set(Sh().tinyurl.short(link))
                link_short = self.slink.get()
                insert(link_short, link)
            else:
                self.disclaimer.set('Please type a valid URL')

        # UI elements

        self.label1 = ctk.CTkLabel(self, text="Enter a link to shorten:")
        self.label1.pack(padx=10, pady=10)

        self.blink = ctk.StringVar()
        self.blink_entry = ctk.CTkEntry(self, width=650, height=28, textvariable=self.blink)
        self.blink_entry.pack()

        self.label2 = ctk.CTkLabel(self, text="Shortened URL:")
        self.label2.pack(padx=10, pady=10)

        self.slink = ctk.StringVar()
        self.slink_entry = ctk.CTkEntry(self, width=350, height=28, textvariable=self.slink)
        self.slink_entry.pack()

        self.shorts_button = ctk.CTkButton(self, text="Shorten URL", command=button_pressed)
        self.shorts_button.pack(padx=20, pady=20)

        self.disclaimer = ctk.StringVar()
        self.disclaimer_label = ctk.CTkLabel(self, textvariable=self.disclaimer)
        self.disclaimer_label.pack(padx=5, pady=5)

        # Creates a second frame for the Treeview that will act as the table
        frame = ctk.CTkFrame(self)
        frame.pack()

        # Sets a style
        style = ttk.Style()
        style.theme_use('clam')

        # Creates a Treeview widget with static dimensions
        table = ttk.Treeview(frame, columns=("short-url", "og-url"), show="headings", height=5,
                             style="Custom.Treeview")
        table.column("short-url", width=200)
        table.column("og-url", width=700)
        table.heading("short-url", text="Shortened URL")
        table.heading("og-url", text="Original URL")
        table.pack(side=tk.LEFT, fill=tk.Y)

        style.configure("Custom.Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=0)  # Sets background and text color

        display()
        

app = App()
app.mainloop()

cur.close()
conn.close()
