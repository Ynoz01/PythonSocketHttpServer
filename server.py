# Uncomment this to pass the first stage
import socket
import threading
import os


def handler_get(target, file_name, lines, file_data):
    response = ""
    if (target == "/"):
        with open(r'D:/Studium/Projects/HttpServer/codecrafters-http-server-python/files/index.html', 'r') as index:
            response_body = index.read()
        response_header = 'HTTP/1.1 200 OK\r\n'
        response_header += 'Content-Type: text/html\r\n'
        response_header += f'Content-Length: {len(response_body.encode("utf-8"))}\r\n'
        response_header += 'Connection: close\r\n\r\n'
        response = response_header + response_body

    elif(target == "/user-agent"):
        user_agent_data = lines[2].split(": ")[-1]
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: ", str(len(user_agent_data)), "\r\n\r\n", user_agent_data
        response = "".join(response)

    elif(target.startswith("/echo/")):
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: ", str(len(file_name)), "\r\n\r\n", file_name
        response = "".join(response)
    elif(target.startswith("/files/")): 
        try:
            print("reading file")
           
            with open(r'/tmp/data/codecrafters.io/http-server-tester/'+ file_name, 'r') as fpR:
                file_data = fpR.read()            
            response = "HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: ", str(len(file_data)), "\r\n\r\n", file_data
            response = "".join(response)
           
        except FileNotFoundError:
            print(f"File'{file_name}' not found.")
            return "HTTP/1.1 404 Not Found\r\n\r\n"
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n"

    return response

def handler_post(target, file_name, file_data):
    print(file_data)
    file_data = create_file(file_name, file_data, target)
    
    if file_data:
        response = "HTTP/1.1 201 Created\r\nContent-Type: text/plain\r\nContent-Length: ", str(len(file_data)), "\r\n\r\n", file_data
        response = "".join(response)
    else:
        print("else")
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
    return response

def create_file(file_name, file_data, target):
    file_path = os.path.join('/tmp/data/codecrafters.io/http-server-tester', file_name)

    try:
        with open(file_path, 'w') as file:
            file.write(file_data)
        return file_data
    except Exception as e:
        print(f"Error writing to file {file_path}: {e}")
        return None
    


def handle_request(client_socket: socket, client_address):
    print(f"Verbindung von {client_address} akzeptiert.")
    try:
        while True:

            request_data = client_socket.recv(1024).decode('utf-8')
            if not request_data:
                break

            lines = request_data.split("\r\n")
            request_line = lines[0]
            print(request_line)
            file_data = lines[-1]
            print(file_data)

            if(len(request_line) >= 3):
                method, target, version = request_line.split()
                req = target.split("/")
                file_name = req[-1]


            if(method == "GET"):
                response = handler_get(target, file_name, lines, file_data)
            elif(method == "POST"):
                response = handler_post(target, file_name, file_data)

            print(response)
            client_socket.send(response.encode())
    finally:
        print(f"Verbindung zu {client_address} wird geschlossen")
        client_socket.close()
        


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221))
    

    while True:

        client, addr = server_socket.accept()
        t = threading.Thread(target = handle_request, args = (client, addr))
        t.start()

     

if __name__ == "__main__":
    main()
    
