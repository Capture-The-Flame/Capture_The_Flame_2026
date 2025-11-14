#!/usr/bin/env python3
# dragon_server.py - minimal Dragon's Breath CTF service
import socket
import threading

HOST = "0.0.0.0"
PORT = 4444
FLAG = "FLAME{dragon_protocol_master}"

def handle_client(conn, addr):
    riddles = [
        (
            "I guard the keep yet never sleep.\n"
            "I'm raised high when danger is nigh,\n"
            "And lowered only when peace draws by.",
            "drawbridge"
        ),
        (
            "Born of legends ancient and old,\n"
            "My scales shimmer like minted gold.\n"
            "Knights seek me for glory untold,\n"
            "Yet few survive to see me unfold.",
            "dragon"
        ),
        (
            "In the castle's halls I am clear,\n"
            "Carrying secrets for all to hear.\n"
            "Though I have no tongue nor ear,\n"
            "Your words awaken me, far and near.",
            "echo"
        )
    ]

    conn.sendall(b"Welcome, traveler... The dragon presents three trials.\n")
    conn.sendall(b"Answer each medieval riddle to earn the flame.\n\n")

    for idx, (riddle, answer) in enumerate(riddles, start=1):
        conn.sendall(f"Riddle {idx}:\n{riddle}\nYour answer: ".encode())
        while True:
            data = conn.recv(1024)
            if not data:
                return
            guess = data.decode(errors='ignore').strip().lower()
            if guess == answer:
                if idx < len(riddles):
                    conn.sendall(b"\nCorrect, traveler. The dragon narrows its eyes...\n\n")
                else:
                    conn.sendall(b"\nThe dragon roars in triumph!\n")
                    conn.sendall(f"FLAME{{dragon_protocol_master}}\n".encode())
                break
            else:
                conn.sendall(b"Wrong! The dragon growls. Try again.\nYour answer: ")

def run():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"Dragon's Breath listening on {HOST}:{PORT}")
    try:
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("Shutting down.")

if __name__ == "__main__":
    run()
