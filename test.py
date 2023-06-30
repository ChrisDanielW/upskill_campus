import customtkinter


def button_clicked():
    print("Boom the butt was clicked")


app = customtkinter.CTk()
app.title("My First GUI based app")
app.geometry("640x360")

button = customtkinter.CTkButton(app, text="my butt", command=button_clicked)
button.grid(row=0, column=0, padx=20, pady=20)

app.mainloop()
