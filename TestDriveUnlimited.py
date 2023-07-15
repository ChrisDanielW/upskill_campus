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
conn = sql.connect("C:\\SQLITE\\Shurl.db")
cur = conn.cursor()
# Creates a table in the above .db file if it doesn't already exist
cur.execute('''CREATE TABLE IF NOT EXISTS urls(id INTEGER PRIMARY KEY AUTOINCREMENT, short_url TEXT, og_url TEXT)''')


# Main class containing both the frames
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("URL Shortener")
        self.geometry("1140x540")

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
        def cargo():
            link = self.blink.get()
            self.slink.set('')
            if is_real(link):
                self.slink.set(Sh().tinyurl.short(link))
                link_short = self.slink.get()
                insert(link_short, link)
            else:
                messagebox.showwarning("Invalid Input", "Please enter a valid URL")

        # Implementation of copy functionality within the table
        def copy_text():
            selected_item = table.focus()
            if selected_item:
                value = table.set(selected_item, "short-url")
                if value:
                    self.clipboard_clear()
                    self.clipboard_append(value)

        # Truncates the urls table in the database and clears all entries
        def clearTab():
            choice = messagebox.askyesno("Confirmation", "Are you sure you want to delete your history?")
            if choice:
                cur.execute("DELETE FROM urls")
                conn.commit()
                display()

        # UI elements

        self.label1 = ctk.CTkLabel(self, text="Enter a link to shorten:")
        self.label1.pack(padx=10, pady=10)

        self.blink = ctk.StringVar()
        self.blink_entry = ctk.CTkEntry(self, width=650, height=28, textvariable=self.blink)
        self.blink_entry.pack()

        self.label2 = ctk.CTkLabel(self, text="Shortened URL:")
        self.label2.pack(padx=10, pady=10)

        self.slink = ctk.StringVar()
        self.slink_entry = ctk.CTkEntry(self, width=300, height=28, textvariable=self.slink, state="readonly")
        self.slink_entry.pack()

        # Button with an event attached to shorten URLs
        self.shorts_button = ctk.CTkButton(self, text="Shorten URL", command=cargo, text_color="black", hover_color="#90f0b6")
        self.shorts_button.pack(padx=20, pady=20)

        # Creates a second frame for the Treeview that will act as the table
        frame = ctk.CTkFrame(self)
        frame.pack(padx=15, pady=15)

        # Creates a Scrollbar widget and associate it with the Treeview
        scrollbar = ctk.CTkScrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Creates a Style in Themed Tkinter
        style = ttk.Style()
        style.theme_use('default')

        # Creates a Treeview widget with static dimensions
        table = ttk.Treeview(frame, columns=("short-url", "og-url"), show="headings", height=4,
                             style="Custom.Treeview")
        table.column("short-url", width=200)
        table.column("og-url", width=700)
        table.heading("short-url", text="Shortened URL")
        table.heading("og-url", text="Original URL")
        table.pack(side=tk.LEFT, fill=tk.Y)

        # Creates a dropdown menu
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Copy", command=copy_text)

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
                        borderwidth=0)

        # Configures a style for the treeview headers to follow
        style.configure("Treeview.Heading",
                        background="#5ba378",
                        foreground="black",
                        bordercolor="#343638",
                        borderwidth=0,
                        font=("TKDefaultFont", 11),
                        padding=1)

        # Attaches a Scrollbar widget to the Treeview
        table.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=table.yview)

        # Button with an event attached to clear the user's history
        self.clr_bt = ctk.CTkButton(self, text="Clear History", command=clearTab, text_color="black", hover_color="#90f0b6")
        self.clr_bt.pack(padx=20, pady=20)

        display()


app = App()
app.mainloop()

cur.close()
conn.close()
