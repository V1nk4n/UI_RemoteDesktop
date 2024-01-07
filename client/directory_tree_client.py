import os
import pickle
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import Button, Frame, Text, filedialog, messagebox

from constant import BACKGROUND, BUFSIZ

SEPARATOR = "<SEPARATOR>"


def list_directory(client, path):
    client.sendall(path.encode())

    data_size = int(client.recv(BUFSIZ))
    if data_size == -1:
        messagebox.showerror(
            message="Click SHOW button again to watch the new directory tree!"
        )
        return []
    client.sendall("received filesize".encode())
    data = b""
    while len(data) < data_size:
        packet = client.recv(999999)
        data += packet
    if data == "error":
        messagebox.showerror(message="Cannot open this directory!")
        return []

    loaded_list = pickle.loads(data)
    return loaded_list


class DirectoryTreeUI(Frame):
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

        self.client = client
        self.currPath = " "
        self.nodes = dict()

        self.frame = tk.Frame(self, height=200, width=500)
        self.tree = ttk.Treeview(self.frame)

        self.frame.place(x=53, y=102, width=713, height=404)

        self.insText1 = "Click SHOW button to show the server's directory tree."
        self.label1 = tk.Label(self.frame, text=self.insText1)
        self.label1.pack(fill=tk.X)

        ysb = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        xsb = ttk.Scrollbar(self.frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.tree.heading("#0", text="Server's Directory Tree", anchor="w")
        self.tree.pack(fill=tk.BOTH)

        self.tree.bind("<<TreeviewOpen>>", self.open_node)
        self.tree.bind("<<TreeviewSelect>>", self.select_node)

        self.insText2 = "Selected path.\n\
            Click SEND FILE TO FOLDER button to select a file you want to copy to this folder.\n\
            Click COPY THIS FILE to copy the selected file to your computer (client)\n\
            Click DELETE button to delete the file on this path.\nYou can click SHOW button again to see the changes."
        self.label2 = tk.Label(self.frame, text=self.insText2)
        self.label2.pack(fill=tk.X)
        self.path = Text(self.frame, height=1, width=26, state="disable")
        self.path.pack(fill=tk.X)

        self.button_2 = Button(
            self,
            text="SHOW",
            width=20,
            height=5,
            borderwidth=0,
            highlightthickness=0,
            command=self.show_tree_directory,
            bg="#fdebd3",
            fg="black",
            font="Calibri 15",
            relief="flat",
        )
        self.button_2.place(x=810, y=160, width=150, height=53)
        # chi gui vao folder th
        self.button_3 = Button(
            self,
            text="SEND FILE",
            width=20,
            height=5,
            borderwidth=0,
            highlightthickness=0,
            command=self.copy_file_to_server,
            bg="#fdebd3",
            fg="black",
            font="Calibri 15",
            relief="flat",
        )
        self.button_3.place(x=810, y=238, width=150, height=53)
        # chi copy file
        self.button_4 = Button(
            self,
            text="COPY FILE",
            width=20,
            height=5,
            borderwidth=0,
            highlightthickness=0,
            command=self.copy_file_to_client,
            bg="#fdebd3",
            fg="black",
            font="Calibri 15",
            relief="flat",
        )
        self.button_4.place(x=810, y=317, width=150, height=53)
        self.button_5 = Button(
            self,
            text="DELETE",
            width=20,
            height=5,
            borderwidth=0,
            highlightthickness=0,
            command=self.delete_file,
            bg="#fdebd3",
            fg="black",
            font="Calibri 15",
            relief="flat",
        )
        self.button_5.place(x=810, y=396, width=150, height=53)
        self.button_6 = Button(
            self,
            text="BACK",
            width=20,
            height=5,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.back(),
            bg="#fdebd3",
            fg="black",
            font="Calibri 15",
            relief="flat",
        )
        self.button_6.place(x=730, y=560, width=200, height=30)

    def insert_node(self, parent, text, abspath, isFolder):
        node = self.tree.insert(parent, "end", text=text, open=False)
        if abspath != "" and isFolder:
            self.nodes[node] = abspath
            self.tree.insert(node, "end")

    def open_node(self, event):
        node = self.tree.focus()
        abspath = self.nodes.pop(node, None)
        if abspath:
            self.tree.delete(self.tree.get_children(node))
            try:
                dirs = list_directory(self.client, abspath)
                for p in dirs:
                    self.insert_node(node, p[0], os.path.join(abspath, p[0]), p[1])
            except:
                messagebox.showerror(message="Cannot open this directory!")

    def select_node(self, event):
        item = self.tree.selection()[0]
        parent = self.tree.parent(item)
        self.currPath = self.tree.item(item, "text")
        while parent:
            self.currPath = os.path.join(self.tree.item(parent)["text"], self.currPath)
            item = parent
            parent = self.tree.parent(item)

        self.path.config(state="normal")
        self.path.delete("1.0", tk.END)
        self.path.insert(tk.END, self.currPath)
        self.path.config(state="disable")

    def deleteTree(self):
        self.currPath = " "
        self.path.config(state="normal")
        self.path.delete("1.0", tk.END)
        self.path.config(state="disable")
        for i in self.tree.get_children():
            self.tree.delete(i)

    def show_tree_directory(self):
        self.deleteTree()
        self.client.sendall("SHOW".encode())

        data_size = int(self.client.recv(BUFSIZ))
        self.client.sendall("received filesize".encode())
        data = b""
        while len(data) < data_size:
            packet = self.client.recv(999999)
            data += packet
        loaded_list = pickle.loads(data)

        for path in loaded_list:
            try:
                abspath = os.path.abspath(path)
                self.insert_node("", abspath, abspath, True)
            except:
                continue

    # copy file from client to server
    def copy_file_to_server(self):
        self.client.sendall("COPYTO".encode())
        isOk = self.client.recv(BUFSIZ).decode()
        if isOk == "OK":
            filename = filedialog.askopenfilename(
                title="Select File", filetypes=[("All Files", "*.*")]
            )
            if filename == None or filename == "":
                self.client.sendall("-1".encode())
                temp = self.client.recv(BUFSIZ)
                return
            destPath = self.currPath + "\\"
            filesize = os.path.getsize(filename)
            self.client.send(
                f"{filename}{SEPARATOR}{filesize}{SEPARATOR}{destPath}".encode()
            )
            isReceived = self.client.recv(BUFSIZ).decode()
            if isReceived == "received filename":
                try:
                    with open(filename, "rb") as f:
                        data = f.read()
                        self.client.sendall(data)
                except:
                    self.client.sendall("-1".encode())
                isReceivedContent = self.client.recv(BUFSIZ).decode()
                if isReceivedContent == "received content":
                    messagebox.showinfo(message="Copy successfully!")
                    return True
        messagebox.showerror(message="Cannot copy!")
        return False

    # copy file from server to client
    def copy_file_to_client(self):
        self.client.sendall("COPY".encode())
        isOk = self.client.recv(BUFSIZ).decode()
        if isOk == "OK":
            try:
                destPath = filedialog.askdirectory()
                if destPath == None or destPath == "":
                    self.client.sendall("-1".encode())
                    temp = self.client.recv(BUFSIZ)
                    return
                self.client.sendall(self.currPath.encode())
                filename = os.path.basename(self.currPath)
                filesize = int(self.client.recv(100))
                if filesize == -1:
                    messagebox.showerror(message="Cannot copy!")
                    return
                self.client.sendall("received filesize".encode())
                data = b""
                while len(data) < filesize:
                    packet = self.client.recv(999999)
                    data += packet
                with open(destPath + "\\" + filename, "wb") as f:
                    f.write(data)
                messagebox.showinfo(message="Copy successfully!")
            except:
                messagebox.showerror(message="Cannot copy!")
        else:
            messagebox.showerror(message="Cannot copy!")

    def delete_file(self):
        self.client.sendall("DEL".encode())
        isOk = self.client.recv(BUFSIZ).decode()
        if isOk == "OK":
            self.client.sendall(self.currPath.encode())
            res = self.client.recv(BUFSIZ).decode()
            if res == "ok":
                messagebox.showinfo(message="Delete successfully!")
            else:
                messagebox.showerror(message="Cannot delete!")
        else:
            messagebox.showerror(message="Cannot delete!")

    def back(self):
        return
