#!/usr/bin/env python3
import socket
import threading
import time
import os

# Configuration
STONE_PORTS = [10001, 10002, 10003, 10004]
CORRECT_SEQUENCE = [10002, 10004, 10001, 10003]
FLAG_PORT = 1337
FLAG = os.getenv('CTF_FLAG', 'flame{all_steps_taken}')

class EnchantedStones:
    def __init__(self):
        self.expected_sequence = CORRECT_SEQUENCE.copy()
        self.current_step = 0
        self.flag_server_running = False
        self.lock = threading.Lock()
    
    def handle_stone_connection(self, client_socket, port):
        with self.lock:
            if not self.expected_sequence:
                client_socket.send(b"The path is complete! The blessing awaits at port 1337.\n")
            elif port == self.expected_sequence[0]:
                self.expected_sequence.pop(0)
                steps_left = len(self.expected_sequence)
                client_socket.send(f"Correct! {steps_left} stones remaining.\n".encode())
                
                if not self.expected_sequence and not self.flag_server_running:
                    self.start_flag_server()
            else:
                self.expected_sequence = CORRECT_SEQUENCE.copy()
                self.current_step = 0
                client_socket.send(b"Wrong stone! The path has reset.\n")
        
        client_socket.close()
    
    def start_stone_server(self, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', port))
        server.listen(5)
        print(f"Stone listening on port {port}")
        
        while True:
            client, addr = server.accept()
            threading.Thread(target=self.handle_stone_connection, args=(client, port)).start()
    
    def handle_flag_connection(self, client_socket):
        client_socket.send(f"Congratulations! You have proven your wisdom.\n\nYour enchanted blessing: {FLAG}\n\n".encode())
        client_socket.close()
    
    def start_flag_server(self):
        self.flag_server_running = True
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', FLAG_PORT))
        server.listen(5)
        print(f"Flag server now listening on port {FLAG_PORT}!")
        
        while True:
            client, addr = server.accept()
            threading.Thread(target=self.handle_flag_connection, args=(client,)).start()
    
    def run(self):
        print("Enchanted Stepping Stones challenge starting...")
        print(f"Stones: {STONE_PORTS}")
        print(f"Final blessing will appear on port {FLAG_PORT}")
        print("Find the correct sequence!")
        
        for port in STONE_PORTS:
            threading.Thread(target=self.start_stone_server, args=(port,), daemon=True).start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down...")

if __name__ == "__main__":
    challenge = EnchantedStones()
    challenge.run()