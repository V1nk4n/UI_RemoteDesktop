import io
import tkinter as tk
from threading import Thread
from tkinter import Frame
from tkinter.filedialog import asksaveasfile

from constant import BACKGROUND
from PIL import Image, ImageTk


class DesktopUI(Frame):
    def __init__(self, parent, client):
        Frame.__init__(self, parent)
        self.configure(
            bg=BACKGROUND,
            height=600,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        parent.geometry("1000x600+200+200")
        self.grid(row=0, column=0, sticky="nsew")

        # copy socket connection to own attribute
        self.client = client

        # initialize status to ready receiving data
        self.status = True

        # initialize the sentinel of saving image command
        self.on_save = False

        # label to display frames received from server
        self.label = tk.Label(self)
        self.label.place(x=20, y=0, width=960, height=540)

        # a button to save captured screen
        self.button_save = tk.Button(
            self,
            text="Save",
            bg="#fdebd3",
            fg="black",
            font="Calibri 15",
            command=lambda: self.click_save(),
            relief="flat",
        )
        self.button_save.place(x=120, y=560, width=200, height=30)

        # a button to stop receiving and return to main interface
        self.button_back = tk.Button(
            self,
            text="Back",
            bg="#fdebd3",
            fg="black",
            font="Calibri 15",
            command=lambda: self.click_back(),
            relief="flat",
        )
        self.button_back.place(x=730, y=560, width=200, height=30)

        # thread
        self.start = Thread(target=self.ChangeImage, daemon=True)
        self.start.start()

    # display frames continously
    def ChangeImage(self):
        while self.status:
            size = int(self.client.recv(100))
            # self.client.sendall(bytes("READY", "utf8"))

            data = b""
            while len(data) < size:
                packet = self.client.recv(999999)
                data += packet

            image_PIL = Image.open(io.BytesIO(data)).resize((960, 540))
            image_tk = ImageTk.PhotoImage(image_PIL)
            self.label.configure(image=image_tk)
            self.label.image = image_tk

            # check save image command
            # while saving image, server will delay capturing and wait for the next command from client
            if self.on_save:
                self.frame = data
                self.save_img()
                self.on_save = False

            # check stop command
            if self.status:
                self.client.sendall(bytes("NEXT_FRAME", "utf8"))
            else:
                self.client.sendall(bytes("STOP_RECEIVING", "utf8"))
        # Return the main UI
        self.destroy()

    def click_back(self):
        self.status = False

    def click_save(self):
        self.on_save = True

    def save_img(self):
        if self.frame == None:
            return

        types = [("Portable Network Graphics", "*.png"), ("All Files", "*.*")]
        image_file = asksaveasfile(mode="wb", filetypes=types, defaultextension="*.png")
        if image_file == None:
            return
        image_file.write(self.frame)
