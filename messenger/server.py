import socket
import threading
import sqlite3


def handle_client(client_socket, client_address):
    print(f"[+] Connected: {client_address}")
    client_login = client_socket.recv(1024).decode()
    print(f"Client login: {client_login}")
    add_history_query = f"INSERT INTO history (login, ip) VALUES ('{client_login}', '{client_address[0]}')"
    cursor.execute(add_history_query)
    db.commit()

    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        client_socket.sendall(data.encode())
    print(f"[-] Disconnected: {client_address}")
    client_socket.close()


def run_server(host, port):
    print(f"[*] Starting server at {host}:{port}")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("[*] Server is ready to accept connections")
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()


db = sqlite3.connect("database.db")
cursor = db.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS client
                  (login TEXT UNIQUE, info TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS history
                  (login TEXT, ip TEXT, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS contacts
                  (owner_id INTEGER, contact_id INTEGER)''')
db.commit()

run_server("localhost", 8888)
