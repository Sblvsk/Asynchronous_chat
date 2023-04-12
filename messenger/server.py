import socket
import threading
import sqlite3
import json

"""
Module for running a server that handles clients' requests and stores them in a SQLite database.
"""


def handle_client(client_socket, client_address):
    """
    Handles a client's requests by parsing and executing them. Stores the client's login and IP address in the database.

    :param client_socket: socket object representing the client's socket connection
    :param client_address: tuple containing the client's IP address and port number
    """
    print(f"[+] Connected: {client_address}")
    client_login = client_socket.recv(1024).decode()
    print(f"Client login: {client_login}")
    add_history_query = f"INSERT INTO history (login, ip) VALUES ('{client_login}', '{client_address[0]}')"
    cursor.execute(add_history_query)
    db.commit()

    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            request = json.loads(data)
            action = request.get('action')
            if action == 'add_contact':
                contact_login = request.get('user_id')
                add_contact_query = f"INSERT INTO contacts (owner_id, contact_id) VALUES ((SELECT id FROM client WHERE login = '{client_login}'), (SELECT id FROM client WHERE login = '{contact_login}'))"
                cursor.execute(add_contact_query)
                db.commit()
                response = {'response': 200}
                client_socket.send(json.dumps(response).encode())
            elif action == 'del_contact':
                contact_login = request.get('user_id')
                del_contact_query = f"DELETE FROM contacts WHERE owner_id = (SELECT id FROM client WHERE login = '{client_login}') AND contact_id = (SELECT id FROM client WHERE login = '{contact_login}')"
                cursor.execute(del_contact_query)
                db.commit()
                response = {'response': 200}
                client_socket.send(json.dumps(response).encode())
            elif action == 'get_contacts':
                get_contacts_query = f"SELECT login FROM client WHERE id IN (SELECT contact_id FROM contacts WHERE owner_id = (SELECT id FROM client WHERE login = '{client_login}'))"
                cursor.execute(get_contacts_query)
                contacts = [row[0] for row in cursor.fetchall()]
                response = {'response': 202, 'alert': contacts}
                client_socket.send(json.dumps(response).encode())
        except Exception as e:
            print(f"[-] Error: {e}")
            response = {'response': 500}
            client_socket.send(json.dumps(response).encode())
            break

    print(f"[-] Disconnected: {client_address}")
    client_socket.close()


def run_server(host, port):
    """
    Runs the server by listening for incoming connections and creating a thread to handle each client.

    :param host: string representing the host's IP address or domain name
    :param port: integer representing the port number on which to listen for incoming connections
    """
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
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, login TEXT UNIQUE, info TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS history
                  (login TEXT, ip TEXT, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS contacts
                  (owner_id INTEGER, contact_id INTEGER,
                  FOREIGN KEY(owner_id) REFERENCES client(id),
                  FOREIGN KEY(contact_id) REFERENCES client(id))''')
db.commit()

run_server("localhost", 8888)
