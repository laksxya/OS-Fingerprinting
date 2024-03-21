import socket
import ssl
import json
import os
import tkinter as tk


def display_specs(specs):
    root = tk.Tk()
    root.title("Client Sys Specs")
    text = tk.Text(root)
    text.pack()
    for key, value in specs.items():
        text.insert(tk.END, f"{key}: {value}\n")
    root.mainloop()


def handle_cli(server_sock):

    client_data = server_sock.recv(4096).decode()
    client_specs = json.loads(client_data)

    display_specs(client_specs)


def start_ser():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('0.0.0.0', 8080))
    server_sock.listen(5)

    print("Server on 8080")

    while True:
        client_sock, addr = server_sock.accept()
        print(f"Accepted connection from {addr}")
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(certfile=os.path.join(
            script_dir, "server.crt"), keyfile=os.path.join(script_dir, "server.key"))
        ssl_client_sock = ssl_context.wrap_socket(
            client_sock, server_side=True)
        dummy_request = ssl_client_sock.recv(1024)

        handle_cli(ssl_client_sock)


if __name__ == "__main__":
    start_ser()
