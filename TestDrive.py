import customtkinter as ctk
# import tkinter as tk
from pyshorteners import Shortener as Sh


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("URL Shortener")
        self.geometry("640x270")

        def button_pressed():
            self.slink.set(Sh().tinyurl.short(blink.get()))

        self.l_1 = ctk.CTkLabel(self, text="Enter a link to shorten:")
        self.l_1.pack(padx=10, pady=10)

        blink = ctk.StringVar()
        self.b_blink = ctk.CTkEntry(self, width=450, height=28, textvariable=blink)
        self.b_blink.pack()

        self.l_2 = ctk.CTkLabel(self, text="Shortened URL:")
        self.l_2.pack(padx=10, pady=10)

        self.slink = ctk.StringVar()
        self.b_slink = ctk.CTkEntry(self, width=350, height=28, textvariable=self.slink)
        self.b_slink.pack()

        self.button = ctk.CTkButton(self, text="Shorten URL", command=button_pressed)
        self.button.pack(padx=20, pady=20)
        # self.grid_columnconfigure(0, weight=1)
        # self.button.grid(row=0, column=0, padx=20, pady=20, sticky="e")


app = App()
app.mainloop()
