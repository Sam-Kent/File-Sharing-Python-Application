import os
import socket

con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
con.connect(("192.168.43.54", 4579))

while True:
    choice = input("Do you want to (R)eceive or (S)end data: ")
    if choice == "R":
        data1 = con.recv(1024)
        data1 = data1.decode("utf-8")
        list = data1.split("/")
        filename = list[-1]
        data = con.recv(1024)
        with open("filesize.txt", "wb") as f:
            f.write(data)
        data = data.decode("utf-8")
        filesize = int(data)
        print(filesize)
        res = str(filesize/1024000)
        num = res.split(".")
        x = int(num[0])
        count = ((1/x)*100)
        c = x
        data = "".encode("utf-8")
        while x != 0:
            data += con.recv(1024000)
            x -= 1
            try:
                print(((c-x)/c)*100)
            except ZeroDivisionError:
                pass

        data += con.recv(1024000)
        if os.path.exists("/root/Desktop/KentShare"):
            pass
        else:
            os.mkdir("/root/Desktop/KentShare")
        with open(f"/root/Desktop/KentShare/{filename}", "wb") as f:
            f.write(data)
        print("Transfer Complete!!!")

    elif choice == "S":
        command = input(">>>")
        con.send(command.encode("utf-8"))
        filepath = command.split(" ", 1)[-1]
        if command[:4] == "send" and os.path.exists(filepath):
            filesize = os.path.getsize(filepath)
            con.send((str(filesize).encode("utf-8")))

            with open(filepath, "rb") as f:
                data = f.read()
            con.send(data)
            print("Data Sent Successfully!!!")

        else:
            print("Make SURE the SYNTAX is CORRECT and the PATH given is VALID!!!")

    else:
        print("INVALID CHOICE")