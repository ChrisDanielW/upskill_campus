import tkinter as tk
import customtkinter as ctk
from tkinter import ttk


def display_table():
    data = [
        ("John", "Doe"),
        ("Jane", "Smith"),
        ("Bob", "Johnson"),
        ("Alice", "Williams"),
        ("Faith", "Connors"),
        ("Sam", "Fisher"),
        ("Sol", "Badguy"),
        ("Evie", "Frye"),
        ("Jesse", "Faden")
        # Add more data as needed
    ]

    # Clear previous table display
    table.delete(*table.get_children())

    # Insert data into the table
    for row in data:
        table.insert("", tk.END, values=row)


# Function to copy the selected item's text to the clipboard
def copy_text(event):
    selected_item = table.focus()
    if selected_item:
        column = table.identify_column(event.x)  # Get the column at the mouse cursor position
        column_index = table["columns"].index(column)  # Get the index of the column
        text = table.item(selected_item, "values")[column_index]  # Get the value from the column index
        if text:
            frame.clipboard_clear()
            frame.clipboard_append(text)


root = ctk.CTk()
root.title("Table Display")
root.geometry("400x300")

# Create a frame to hold the Treeview widget
frame = ctk.CTkFrame(root)
frame.pack(pady=10)

# Create a Scrollbar widget and associate it with the Treeview
scrollbar = ctk.CTkScrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

style = ttk.Style()
style.theme_use('clam')  # Use 'clam' theme as a dark theme option


# Create the Treeview widget with static dimensions
table = ttk.Treeview(frame, columns=("First Name", "Last Name"), show="headings", height=5, style="Custom.Treeview")
table.column("First Name", width=100)
table.column("Last Name", width=100)
table.heading("First Name", text="First Name")
table.heading("Last Name", text="Last Name")
table.pack(side=tk.LEFT, fill=tk.Y)
table.bind("<Control-c>", copy_text)

style.configure("Custom.Treeview",
                background="black",  # Set background color
                foreground="white")  # Set text color

style.map("Custom.Treeview.Item",
          background=[("selected", "black")])  # Set background color for selected item

# Configure the style for the Treeview when no entries are present
style.configure("Custom.Treeview.NoEntries",
                background="black")  # Set background color when no entries

# Attach the Scrollbar to the Treeview
table.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=table.yview)

button_display = ctk.CTkButton(root, text="Display Table", command=display_table)
button_display.pack(pady=10)

root.mainloop()