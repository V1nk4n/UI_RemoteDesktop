import socket
import tkinter as tk

import app_process_server as ap
import directory_tree_server as dt
import keylogger_server as kl
import live_screen_server as lss
import mac_address_server as mac
import registry_server as rs
import shutdown_logout_server as sl
from constant import BACKGROUND_COLOR

main = tk.Tk()
main.geometry("200x200")
main.title("Server")
main["bg"] = BACKGROUND_COLOR

# Global variables
global client
BUFSIZ = 1024 * 4


def live_screen():
    global client
    lss.capture_screen(client)
    return


def mac_address():
    global client
    mac.mac_address(client)
    return


def keylogger():
    global client
    kl.keylog(client)
    return


def app_process():
    global client
    ap.app_process(client)
    return


def directory_tree():
    global client
    dt.directory(client)
    return


def registry():
    global client
    rs.registry(client)
    return


def shutdown_logout():
    global client
    sl.shutdown_logout(client)
    return


# Connect
###############################################################################
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = ""
    port = 5656
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(100)
    global client
    client, addr = s.accept()
    while True:
        msg = client.recv(BUFSIZ).decode("utf8")
        if "KEYLOG" in msg:
            keylogger()
        elif "SD_LO" in msg:
            shutdown_logout()
        elif "LIVESCREEN" in msg:
            live_screen()
        elif "APP_PRO" in msg:
            app_process()
        elif "MAC" in msg:
            mac_address()
        elif "DIRECTORY" in msg:
            directory_tree()
        elif "REGISTRY" in msg:
            registry()
        elif "QUIT" in msg:
            client.close()
            s.close()
            return


###############################################################################

tk.Button(
    main,
    text="OPEN",
    width=10,
    height=2,
    fg="white",
    bg="#264e70",
    borderwidth=0,
    highlightthickness=0,
    command=connect,
    relief="flat",
).place(x=100, y=100, anchor="center")
main.mainloop()
