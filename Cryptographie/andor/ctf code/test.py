import socket

HOST = "crypto.heroctf.fr"
PORT = 9000

SAMPLES = 400

A = []
O = []

s = socket.socket()
s.connect((HOST, PORT))

for _ in range(SAMPLES):
    page = s.recv(4096).decode()

    # Extraction d'un seul sample
    for line in page.splitlines():
        if line.startswith("a ="):
            A.append(bytes.fromhex(line.split("=",1)[1].strip()))
        elif line.startswith("o ="):
            O.append(bytes.fromhex(line.split("=",1)[1].strip()))

    # Le serveur attend un ENTER pour envoyer le suivant
    s.sendall(b"\n")

# Reconstruction
flag_left  = bytes([max(col) for col in zip(*A)])
flag_right = bytes([min(col) for col in zip(*O)])

flag_bytes = flag_left + flag_right
flag_printable = bytes([b if 32 <= b <= 126 else ord('?') for b in flag_bytes])

print("FLAG RAW:   ", flag_bytes)
print("FLAG ASCII: ", flag_printable.decode())
