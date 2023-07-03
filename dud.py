import customtkinter as ctk


app = ctk.CTk()
app.title("User Interface")
app.geometry("400x170")

label1 = ctk.CTkLabel(app, text="This is a Label")
label1.pack(padx=10, pady=10)

entry1 = ctk.CTkEntry(app, placeholder_text="This is an Entry")
entry1.pack(padx=10, pady=10)

button1 = ctk.CTkButton(app, text="This is a Button")
button1.pack(padx=10, pady=10)

app.mainloop()
