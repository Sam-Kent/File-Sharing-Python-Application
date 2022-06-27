import os
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("", 4579))
sock.listen()
print("Waiting for your friend to finish setting up...")
con, addr = sock.accept()
print(f"Setup complete. Connection received from {addr}")

while True:
    choice = input("Do you want to (R)eceive or (S)end data: ")
    if choice == "R":
        data = con.recv(1024)
        data = data.decode("utf-8")
        list = data.split("/")
        filename = list[-1]
        data = con.recv(1024)
        filesize =  float(data)
        print(filesize)
        res = str(filesize/1024)
        num = res.split(".")
        x = int(num[0])
        data = "".encode("utf-8")
        while x != 0:
            data += con.recv(1024)
            x -= 1
        y = "0."+ num[-1]
        y = int(y)
        data += con.recv(y*1024)
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

            with open(filepath, "rb") as f:
                data = f.read()
            filesize = len(data)
            print(filesize)
            con.send(str(filesize).encode("utf-8"))
            con.send(data)
            print("Data Sent Successfully!!!")

        else:
            print("Make SURE the SYNTAX is CORRECT and the PATH given is VALID!!!")

    else:
        print("INVALID CHOICE")