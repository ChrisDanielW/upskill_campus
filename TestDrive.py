import customtkinter as ctk
import requests
# import tkinter as tk
from pyshorteners import Shortener as Sh


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("URL Shortener")
        self.geometry("640x270")

        def is_real(link):
            try:
                response = requests.head(link)
                return response.status_code == requests.codes.ok
            except requests.exceptions.RequestException:
                return False

        def button_pressed():
            link = self.blink.get()
            self.slink.set('')
            if is_real(link):
                self.disclaimer.set('')
                self.slink.set(Sh().tinyurl.short(link))
            else:
                self.disclaimer.set('Please type a valid URL')

        self.label1 = ctk.CTkLabel(self, text="Enter a link to shorten:")
        self.label1.pack(padx=10, pady=10)

        self.blink = ctk.StringVar()
        self.blink_entry = ctk.CTkEntry(self, width=450, height=28, textvariable=self.blink)
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
        # self.grid_columnconfigure(0, weight=1)
        # self.button.grid(row=0, column=0, padx=20, pady=20, sticky="e")


app = App()
app.mainloop()
