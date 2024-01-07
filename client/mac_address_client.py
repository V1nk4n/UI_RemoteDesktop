import tkinter as tk

BUFFSIZE = 1024 * 4

def mac_address(client):
    try:
        result = client.recv(BUFFSIZE).decode("utf8")
        result = result[2:].upper()
        result = ':'.join(result[i:i + 2] for i in range(0, len(result), 2))
        tk.messagebox.showinfo(title='MAC Address', message=result)
    except:
        message = "Check the connection again"
        tk.messagebox.showerror(title='MAC Address', message=message)