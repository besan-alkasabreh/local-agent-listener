import socket

HOST = "127.0.0.1"
PORT = 4444

s = socket.socket()
s.bind((HOST, PORT))
s.listen(1)

print(f"[+] Listening on {HOST}:{PORT}")
conn, addr = s.accept()
print("[+] Connected:", addr)

while True:
    cmd = input("listener> ")
    conn.send(cmd.encode())

    if cmd.strip().lower() == "quit":
        break

    data = conn.recv(4096).decode(errors="replace")
    print(data)

conn.close()
s.close()
