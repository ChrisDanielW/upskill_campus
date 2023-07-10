import pyshorteners
import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()
app.geometry("600x400")


def b_short():
    print("Placeholder")


my_label = customtkinter.CtkLabel(app, text="Enter Link To Shorten", font=("Helvetica", 34))
my_label.pack(pady=20)

my_entry = customtkinter.CtkEntry(app, font=("Helvetica", 24))
my_entry.pack(pady=20)

my_button = customtkinter.CtkButton(app, text="Shorten Link", command=shorten, font=("Helvetica", 24))
my_button.pack(pady=20)

shorty_label = customtkinter.CtkLabel(app, text="Shortened Link", font=("Helvetica", 14))
shorty_label.pack(pady=50)

shorty = customtkinter.CtkEntry(app, font=("Helvetica", 22), justify=CENTER, width=30, bd=0, bg="systembuttonface")
shorty.pack(pady=10)


# entry_1 = customtkinter.CTkEntry(master=app, placeholder_text="CTkEntry")
# entry_1.pack(pady=120)
# 
# button = customtkinter.CTkButton(master=app, text="Convert Link", command=b_short)
# button.pack(pady=0)

app.mainloop()
