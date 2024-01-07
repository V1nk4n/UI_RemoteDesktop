import os

BUFFSIZE = 1024 * 4
def shutdown_logout(client):
    while(True):
        message = client.recv(BUFFSIZE).decode("utf8")
        if "SHUTDOWN" in message:
            os.system('shutdown -s -t 15')
        elif "LOGOUT" in message:
            os.system('shutdown -l')
        else:
            return
    return
    