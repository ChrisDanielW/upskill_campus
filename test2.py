import customtkinter as ctk
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

    # Clear previous table display
    for widget in table_frame.winfo_children():
        widget.destroy()

    cursor.execute("SELECT original_url, shortened_url FROM urls")
    rows = cursor.fetchall()

    # Create column labels
    col_labels = ["Original URL", "Shortened URL"]
    for col, col_label in enumerate(col_labels):
        label = ctk.CTkLabel(table_frame, text=col_label)
        label.grid(row=0, column=col, padx=10, pady=5)

    # Insert rows into the table
    for row, data in enumerate(rows, start=1):
        for col, value in enumerate(data):
            label = ctk.CTkLabel(table_frame, text=value)
            label.grid(row=row, column=col, padx=10, pady=5)

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
