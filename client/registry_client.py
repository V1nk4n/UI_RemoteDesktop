import json
import os  # cung cap chuc nang tuong tac voi he dieu hanh
import sys

# Tkinter
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile

from constant import BACKGROUND
from PIL import Image, ImageTk

BUFSIZ = 32768


class RegistryUI(Frame):
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
        # attributes of registry keys/values
        self.action_ID = None
        self.key = None
        self.name = None
        self.data = None
        self.data_type = 1
        # attributes for response of action
        self.res1 = None
        self.res2 = None
        # initialize status ready to use
        self.status = True

        ##########Tkinter widgets############################
        # KEY
        self.key_label = tk.Label(
            self,
            text="Key",
            bg="#fdebd3",
            fg="black",
            font="Calibri 15",
            relief="flat",
        )
        self.key_label.place(x=50, y=50, width=90, height=25)
        self.key_txt = tk.Text(self)
        self.key_txt.place(x=150, y=50, width=300, height=25)

        # NAME VALUE
        self.name_label = tk.Label(
            self,
            text="Name Value",
            bg="#fdebd3",
            fg="black",
            font="Calibri 15",
            relief="flat",
        )
        self.name_label.place(x=500, y=120, width=150, height=25)
        self.name_txt = tk.Text(self)
        self.name_txt.place(x=660, y=120, width=200, height=25)
        # self.ex2 = tk.Label(self, text='Use only for Get Value / Set Value', anchor='w',bg = "#FCD0E8")
        # self.ex2.place(x=660,y=150,width=200,height=25)

        # DATA VALUE
        self.data_label = tk.Label(
            self,
            text="Data Value",
            bg="#fdebd3",
            fg="black",
            font="Calibri 15",
            relief="flat",
        )
        self.data_label.place(x=500, y=160, width=150, height=25)
        self.data_txt = tk.Text(self)
        self.data_txt.place(x=660, y=160, width=200, height=25)
        # self.ex3 = tk.Label(self, text='Use only for Set Value', anchor='w',bg = "#FCD0E8")
        # self.ex3.place(x=660,y=230,width=200,height=25)

        # DATA TYPE
        self.data_type_label = tk.Label(
            self,
            text="Data Type",
            bg="#fdebd3",
            fg="black",
            font="Calibri 15",
            relief="flat",
        )
        self.data_type_label.place(x=500, y=200, width=150, height=25)
        self.data_type_txt = tk.Text(self)
        self.data_type_txt.place(x=660, y=200, width=200, height=25)
        self.data_type_txt.insert(tk.END, "Input an integer number")
        self.ex4 = tk.Label(
            self,
            text="0 - REG_SZ",
            bg="#fdebd3",
            fg="black",
            font="Calibri 15",
        )
        self.ex4.place(x=500, y=310, width=200, height=25)
        self.ex5 = tk.Label(
            self,
            text="1 - REG_BINARY",
            bg="#fdebd3",
            fg="black",
            font="Calibri 15",
        )
        self.ex5.place(x=750, y=310, width=200, height=25)
        self.ex6 = tk.Label(
            self,
            text="2 - REG_DWORD",
            bg="#fdebd3",
            fg="black",
            font="Calibri 15",
        )
        self.ex6.place(x=500, y=340, width=200, height=25)
        self.ex7 = tk.Label(
            self,
            text="3 - REG_QWORD",
            bg="#fdebd3",
            fg="black",
            font="Calibri 15",
        )
        self.ex7.place(x=750, y=340, width=200, height=25)
        self.ex8 = tk.Label(
            self,
            text="4 - REG_MULTI_SZ",
            bg="#fdebd3",
            fg="black",
            font="Calibri 15",
        )
        self.ex8.place(x=500, y=370, width=200, height=25)
        self.ex9 = tk.Label(
            self,
            text="5 - REG_EXPAND_SZ",
            bg="#fdebd3",
            fg="black",
            font="Calibri 15",
        )
        self.ex9.place(x=750, y=370, width=200, height=25)

        # REG CONTENT
        self.content = tk.Text(self)
        self.content.place(x=78, y=136, width=395, height=205)
        self.content.configure(font=("Times New Roman", 10))

        self.btn_get_value = tk.Button(
            self,
            text="Get Value",
            bg="#fdebd3",
            fg="black",
            font="Calibri 15",
            command=lambda: self.get_value(),
            relief="flat",
        )
        self.btn_get_value.place(x=100, y=480, width=150, height=50)

        self.btn_set_value = tk.Button(
            self,
            text="Set Value",
            bg="#fdebd3",
            fg="black",
            font="Calibri 15",
            command=lambda: self.set_value(),
            relief="flat",
        )
        self.btn_set_value.place(x=300, y=480, width=150, height=50)

        self.btn_create_key = tk.Button(
            self,
            text="Create Key",
            bg="#fdebd3",
            fg="black",
            font="Calibri 15",
            command=lambda: self.create_key(),
            relief="flat",
        )
        self.btn_create_key.place(x=500, y=480, width=150, height=50)

        self.btn_delete_key = tk.Button(
            self,
            text="Delete Key",
            bg="#fdebd3",
            fg="black",
            font="Calibri 15",
            command=lambda: self.delete_key(),
            relief="flat",
        )
        self.btn_delete_key.place(x=700, y=480, width=150, height=50)

        self.btn_open = tk.Button(
            self,
            text="BROWSER",
            bg="#fdebd3",
            fg="black",
            font="Calibri 15",
            command=lambda: self.open_file(),
            relief="flat",
        )
        self.btn_open.place(x=78, y=400, width=120, height=50)

        self.btn_send_detail = tk.Button(
            self,
            text="SEND",
            bg="#fdebd3",
            fg="black",
            font="Calibri 15",
            command=lambda: self.send_detail(),
            relief="flat",
        )
        self.btn_send_detail.place(x=220, y=400, width=120, height=50)

        # a button to stop receiving and return to main interface
        self.btn_back = tk.Button(
            self,
            text="Back",
            command=lambda: self.click_back(),
            relief="flat",
            bg="#fdebd3",
            fg="black",
            font="Calibri 15",
        )
        self.btn_back.place(x=730, y=560, width=200, height=30)

    def get_input(self):
        self.key = self.key_txt.get("1.0", "end").rstrip()
        self.name = self.name_txt.get("1.0", "end").rstrip()
        self.data = self.data_txt.get("1.0", "end").rstrip()
        dtypes = [
            "REG_SZ",
            "REG_BINARY",
            "REG_DWORD",
            "REG_QWORD",
            "REG_MULTI_SZ",
            "REG_EXPAND_SZ",
        ]
        try:
            t_num = int(self.data_type_txt.get("1.0", "end").rstrip())
            if 0 <= t_num and t_num <= 5:
                self.data_type = dtypes[t_num]
            else:
                self.data_type = dtypes[0]
        except:
            self.data_type = dtypes[0]

    def get_value(self):
        self.get_input()
        self.action_ID = 1
        self.send_msg()

    def set_value(self):
        self.get_input()
        self.action_ID = 2
        self.send_msg()

    def create_key(self):
        self.get_input()
        self.action_ID = 3
        self.send_msg()

    def delete_key(self):
        self.get_input()
        self.action_ID = 4
        self.send_msg()

    def send_detail(self):
        self.get_input()
        s = self.content.get("1.0", "end")
        self.key = s
        self.action_ID = 0
        self.send_msg()

    def open_file(self):
        file = filedialog.askopenfilename()
        if file == None or file == "":
            return
        self.content.delete("1.0", "end")
        s = ""
        with open(file, "r") as input_file:
            s = input_file.read()
        for line in s:
            self.content.insert(tk.END, line)

    def send_msg(self):
        msg = {
            "ID": self.action_ID,
            "path": self.key,
            "name_value": self.name,
            "value": self.data,
            "v_type": self.data_type,
        }
        msg = json.dumps(msg)
        msg_bytes = bytes(msg, "utf8")
        msg_sz = str(len(msg_bytes))
        self.client.sendall(bytes(msg_sz, "utf8"))
        self.client.sendall(msg_bytes)
        self.res1 = self.client.recv(BUFSIZ).decode("utf8")
        self.res2 = self.client.recv(BUFSIZ).decode("utf8")
        if self.action_ID == 1:
            if "0" in self.res1:
                tk.messagebox.showerror(
                    title="Thông báo", message="Thao tác không hợp lệ"
                )
            else:
                tk.messagebox.showinfo(title="Thông báo", message=self.res2)
        else:
            if "0" in self.res1:
                tk.messagebox.showerror(
                    title="Thông báo", message="Thao tác không hợp lệ"
                )
            else:
                tk.messagebox.showinfo(title="Thông báo", message="Thành công")

    def click_back(self):
        self.status = False
        self.client.sendall(bytes("STOP_EDIT_REGISTRY", "utf8"))
        return
