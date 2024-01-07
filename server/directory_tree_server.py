import os
import pickle

from constant import BUFSIZ

SEPARATOR = "<SEPARATOR>"


def showTree(sever):
    ListDirectoryTree = []
    for c in range(ord("A"), ord("Z") + 1):
        path = chr(c) + ":\\"
        if os.path.isdir(path):
            ListDirectoryTree.append(path)
    data = pickle.dumps(ListDirectoryTree)
    sever.sendall(str(len(data)).encode())
    temp = sever.recv(BUFSIZ)
    sever.sendall(data)


def sendListDirs(sever):
    path = sever.recv(BUFSIZ).decode()
    if not os.path.isdir(path):
        return [False, path]

    try:
        listTree = []
        ListDirectoryTree = os.listdir(path)
        for d in ListDirectoryTree:
            listTree.append((d, os.path.isdir(path + "\\" + d)))

        data = pickle.dumps(listTree)
        sever.sendall(str(len(data)).encode())
        temp = sever.recv(BUFSIZ)
        sever.sendall(data)
        return [True, path]
    except:
        sever.sendall("error".encode())
        return [False, "error"]


def deleteFile(sever):
    file_name = sever.recv(BUFSIZ).decode()
    if os.path.exists(file_name):
        try:
            os.remove(file_name)
            sever.sendall("ok".encode())
        except:
            sever.sendall("error".encode())
            return
    else:
        sever.sendall("error".encode())
        return


# copy file from client to server
def copyFileToServer(sever):
    received = sever.recv(BUFSIZ).decode()
    if received == "-1":
        sever.sendall("-1".encode())
        return
    filename, filesize, path = received.split(SEPARATOR)
    filename = os.path.basename(filename)
    filesize = int(filesize)
    sever.sendall("received filename".encode())
    data = b""
    while len(data) < filesize:
        packet = sever.recv(999999)
        data += packet
    if data == "-1":
        sever.sendall("-1".encode())
        return
    try:
        with open(path + filename, "wb") as file:
            file.write(data)
        sever.sendall("received content".encode())
    except:
        sever.sendall("-1".encode())


# copy file from server to client
def copyFileToClient(sever):
    filename = sever.recv(BUFSIZ).decode()
    if filename == "-1" or not os.path.isfile(filename):
        sever.sendall("-1".encode())
        return
    filesize = os.path.getsize(filename)
    sever.sendall(str(filesize).encode())
    temp = sever.recv(BUFSIZ)
    with open(filename, "rb") as f:
        data = f.read()
        sever.sendall(data)


def directory(client):
    isMod = False

    while True:
        if not isMod:
            mod = client.recv(BUFSIZ).decode()

        if mod == "SHOW":
            showTree(client)
            while True:
                check = sendListDirs(client)
                if not check[0]:
                    mod = check[1]
                    if mod != "error":
                        isMod = True
                        break

        # copy file from client to server
        elif mod == "COPYTO":
            client.sendall("OK".encode())
            copyFileToServer(client)
            isMod = False

        # copy file from server to client
        elif mod == "COPY":
            client.sendall("OK".encode())
            copyFileToClient(client)
            isMod = False

        elif mod == "DEL":
            client.sendall("OK".encode())
            deleteFile(client)
            isMod = False

        elif mod == "QUIT":
            return

        else:
            client.sendall("-1".encode())
