import socket
from _thread import start_new_thread

server = "localhost"
port = 5555

# Initialize Server Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((server, port))
s.listen(2)
print("Server started. Waiting for players...")

players = [None, None]
current_player = 0

def threaded_client(conn, player):
    conn.send(str.encode(str(player)))
    while True:
        try:
            data = conn.recv(2048).decode()
            if not data:
                break
            print(f"Player {player}: {data}")
            opponent = 1 - player
            if players[opponent]:
                players[opponent].sendall(str.encode(data))
        except:
            break
    print(f"Player {player} disconnected")
    players[player] = None
    conn.close()

while True:
    conn, addr = s.accept()
    print(f"Connected to {addr}")
    players[current_player] = conn
    start_new_thread(threaded_client, (conn, current_player))
    current_player += 1
