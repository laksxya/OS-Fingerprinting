import socket
import ssl
import json
import platform


def get_specs():
    specs = {

        'System': platform.system(),
        'Processor': platform.processor(),
        'System Platform': platform.platform(),
        'Platform Release': platform.release(),
        'Platform Version': platform.version(),
        'Machine': platform.machine(),
        'Architecture': platform.architecture(),
        'Version': platform.version(),
        'Python Build Info': platform.python_build(),
    }
    return specs


def start_cli():
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_addr = ('172.20.10.4', 8080)  # put your server ip
    client_sock.connect(server_addr)
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    ssl_client_sock = ssl_context.wrap_socket(
        client_sock, server_hostname=server_addr[0])
    ssl_client_sock.sendall(b"HELLO_SERVER")

    client_specs = get_specs()
    json_specs = json.dumps(client_specs)
    ssl_client_sock.sendall(json_specs.encode())

    ssl_client_sock.close()


if __name__ == "__main__":
    start_cli()
