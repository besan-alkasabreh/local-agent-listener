import socket
import os
import getpass
import platform
from datetime import datetime

HOST = "127.0.0.1"
PORT = 4444

cwd = os.getcwd()         
history = []               
MAX_READ = 8000            

def send(sock, text: str):
    sock.send(text.encode())

s = socket.socket()
s.connect((HOST, PORT))

while True:
    raw = s.recv(4096).decode(errors="replace")
    if not raw:
        break

    cmdline = raw.strip()
    if not cmdline:
        continue

    history.append(cmdline)

    parts = cmdline.split(maxsplit=1)
    cmd = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else ""

   
    if cmd == "quit":
        send(s, "Goodbye!\n")
        break

    elif cmd == "help":
        send(s,
            "Commands:\n"
            "  help                 show this list\n"
            "  ping                 returns PONG\n"
            "  time                 current time\n"
            "  whoami               current username\n"
            "  sysinfo              basic system info\n"
            "  pwd                  show current working dir (inside agent)\n"
            "  ls [path]            list files in cwd or in path\n"
            "  cd <path>            change cwd (inside agent)\n"
            "  cat <file>           read small text file (<= 8KB)\n"
            "  size <file>          file size in bytes\n"
            "  mkdir <name>         create folder inside current directory\n"
            "  history              show last commands\n"
            "  quit                 close session\n"
        )

    elif cmd == "ping":
        send(s, "PONG\n")

    elif cmd == "time":
        send(s, datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")

    elif cmd == "whoami":
        send(s, getpass.getuser() + "\n")

    elif cmd == "sysinfo":
        info = (
            f"OS: {platform.system()} {platform.release()}\n"
            f"Node: {platform.node()}\n"
            f"Machine: {platform.machine()}\n"
            f"Python: {platform.python_version()}\n"
        )
        send(s, info)

    elif cmd == "pwd":
        send(s, cwd + "\n")

    elif cmd == "ls":
        path = arg.strip() or cwd
        if not os.path.isabs(path):
            path = os.path.join(cwd, path)

        try:
            items = os.listdir(path)
            items.sort()
            out = f"[LS] {os.path.abspath(path)}\n" + "\n".join(items) + "\n"
            send(s, out if items else f"[LS] {os.path.abspath(path)}\n<empty>\n")
        except Exception as e:
            send(s, f"[ERROR] ls: {e}\n")

    elif cmd == "cd":
        if not arg.strip():
            send(s, "[ERROR] cd needs a path\n")
            continue

        new_path = arg.strip().strip('"')
        if not os.path.isabs(new_path):
            new_path = os.path.join(cwd, new_path)

        try:
            if os.path.isdir(new_path):
                cwd = os.path.abspath(new_path)
                send(s, f"[OK] cwd = {cwd}\n")
            else:
                send(s, "[ERROR] not a directory\n")
        except Exception as e:
            send(s, f"[ERROR] cd: {e}\n")

    elif cmd == "cat":
        if not arg.strip():
            send(s, "[ERROR] cat needs a file path\n")
            continue

        file_path = arg.strip().strip('"')
        if not os.path.isabs(file_path):
            file_path = os.path.join(cwd, file_path)

        try:
            if not os.path.isfile(file_path):
                send(s, "[ERROR] not a file\n")
                continue

            with open(file_path, "rb") as f:
                data = f.read(MAX_READ + 1)

            if len(data) > MAX_READ:
                send(s, f"[ERROR] file too large (> {MAX_READ} bytes)\n")
                continue

            text = data.decode("utf-8", errors="replace")
            send(s, f"[CAT] {os.path.abspath(file_path)}\n{text}\n")
        except Exception as e:
            send(s, f"[ERROR] cat: {e}\n")

    elif cmd == "size":
        if not arg.strip():
            send(s, "[ERROR] size needs a file path\n")
            continue

        file_path = arg.strip().strip('"')
        if not os.path.isabs(file_path):
            file_path = os.path.join(cwd, file_path)

        try:
            if not os.path.isfile(file_path):
                send(s, "[ERROR] not a file\n")
                continue

            send(s, f"{os.path.getsize(file_path)}\n")
        except Exception as e:
            send(s, f"[ERROR] size: {e}\n")

    elif cmd == "mkdir":
        if not arg.strip():
            send(s, "[ERROR] mkdir needs a folder name\n")
            continue

        folder_name = arg.strip().strip('"')
        new_dir = os.path.join(cwd, folder_name)

        try:
            if os.path.exists(new_dir):
                send(s, "[ERROR] folder already exists\n")
            else:
                os.mkdir(new_dir)
                send(s, f"[OK] folder created: {new_dir}\n")
        except Exception as e:
            send(s, f"[ERROR] mkdir: {e}\n")

    elif cmd == "history":
        last = history[-10:]
        out = "[HISTORY]\n" + "\n".join(last) + "\n"
        send(s, out)

    else:
        send(s, "Unknown command. Type: help\n")

s.close()
