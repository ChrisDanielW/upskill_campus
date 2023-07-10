import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import sqlite3
from pyshorteners import Shortener as Sh

conn = sqlite3.connect("url_shortener.db")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS urls
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, original_url TEXT, shortened_url TEXT)''')

conn.commit()


def shorten_url():
    original_url = entry_url.get()
    shortened_url = Sh().tinyurl.short(original_url)

    # Insert the URLs into the database
    cursor.execute("INSERT INTO urls (original_url, shortened_url) VALUES (?, ?)",
                   (original_url, shortened_url))
    conn.commit()

    # Clear the entry control after insertion
    entry_url.delete(0, ctk.END)

    # Refresh the URL table
    display_urls()


def display_urls():
    cursor.execute("SELECT original_url, shortened_url FROM urls")
    rows = cursor.fetchall()

    # Clear previous table display
    for widget in table_frame.winfo_children():
        widget.destroy()

    # Create column labels
    col_labels = ["Original URL", "Shortened URL"]
    for col, col_label in enumerate(col_labels):
        label = ctk.CTkLabel(table_frame, text=col_label)
        label.grid(row=0, column=col, padx=10, pady=5)

    # Create a Canvas widget for the Treeview
    canvas = tk.Canvas(table_frame)
    canvas.grid(row=1, column=0, columnspan=2)

    # Create a Scrollbar and associate it with the Canvas
    scrollbar = tk.Scrollbar(table_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.grid(row=1, column=2, sticky='ns')
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the Canvas for the Treeview
    tree_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=tree_frame, anchor='nw')

    # Create the Treeview widget
    tree = ttk.Treeview(tree_frame, columns=col_labels, show='headings')
    tree.grid(row=0, column=0, sticky='nsew')

    # Configure column headings
    for col_label in col_labels:
        tree.heading(col_label, text=col_label)
        tree.column(col_label, width=200, anchor='center')

    # Configure the Scrollbar to scroll the Canvas and Treeview
    canvas.bind('<Configure>', lambda event: canvas.configure(scrollregion=canvas.bbox('all')))

    # Insert rows into the Treeview
    for data in rows:
        tree.insert('', tk.END, values=data)

    canvas.update_idletasks()


app = ctk.CTk()
app.title("URL Shortener")
app.geometry("800x600")

# Create the URL entry control
entry_url = ctk.CTkEntry(app)
entry_url.pack(pady=10)

# Create the URL Shorten button
button_shorten = ctk.CTkButton(app, text="Shorten URL", command=shorten_url)
button_shorten.pack(pady=10)

# Create the frame for the URL table
table_frame = ctk.CTkFrame(app)
table_frame.pack()

# Display the URLs initially
display_urls()

app.mainloop()

conn.close()
