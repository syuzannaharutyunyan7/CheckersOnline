import socket, threading, json

HOST, PORT = "0.0.0.0", 5555
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(2)

game_state = {
    "turn": 0, "must_jump": None,
    "board": [
        ["", "b", "", "b", "", "b", "", "b"], ["b", "", "b", "", "b", "", "b", ""],
        ["", "b", "", "b", "", "b", "", "b"], ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""], ["r", "", "r", "", "r", "", "r", ""],
        ["", "r", "", "r", "", "r", "", "r"], ["r", "", "r", "", "r", "", "r", ""],
    ]
}

def get_flying_moves(board, x, y, player):
    moves = []
    piece = board[y][x]
    is_king = piece.isupper()
    # Red (0) moves UP (-1), Black (1) moves DOWN (+1). Kings move all 4.
    dirs = [(-1,-1), (1,-1), (-1,1), (1,1)] if is_king else ([(-1,-1), (1,-1)] if player==0 else [(-1,1), (1,1)])
    
    for dx, dy in dirs:
        dist = 1
        while True:
            nx, ny = x + dx*dist, y + dy*dist
            if not (0 <= nx < 8 and 0 <= ny < 8): break
            target = board[ny][nx]
            if target == "":
                moves.append({"to": (nx, ny), "capture": None})
                if not is_king: break 
            else:
                if target.lower() != piece.lower():
                    jx, jy = nx + dx, ny + dy
                    if 0 <= jx < 8 and 0 <= jy < 8 and board[jy][jx] == "":
                        moves.append({"to": (jx, jy), "capture": (nx, ny)})
                break 
            dist += 1
    return moves

def handle_client(conn, player_id):
    # Send initial state immediately
    try: conn.sendall(json.dumps({"player": player_id, "board": game_state["board"], "turn": game_state["turn"]}).encode())
    except: return
    
    while True:
        try:
            data = conn.recv(4096)
            if not data: break
            msg = json.loads(data.decode())
            if msg.get("type") == "move" and player_id == game_state["turn"]:
                fx, fy = msg["from"]; tx, ty = msg["to"]
                valid = get_flying_moves(game_state["board"], fx, fy, player_id)
                move_obj = next((m for m in valid if m["to"] == (tx, ty)), None)
                
                if move_obj:
                    p = game_state["board"][fy][fx]
                    game_state["board"][ty][tx] = p
                    game_state["board"][fy][fx] = ""
                    if move_obj["capture"]:
                        cx, cy = move_obj["capture"]
                        game_state["board"][cy][cx] = ""
                    
                    if p == "r" and ty == 0: game_state["board"][ty][tx] = "R"
                    if p == "b" and ty == 7: game_state["board"][ty][tx] = "B"
                    
                    game_state["turn"] = 1 - game_state["turn"]
                    broadcast()
        except: break

def broadcast():
    msg = json.dumps(game_state).encode()
    for c in clients:
        try: c.sendall(msg)
        except: pass

clients = []
print("✨ SyuzCheckers Server is Live! ✨")
while True:
    c, a = server.accept()
    if len(clients) < 2:
        clients.append(c)
        threading.Thread(target=handle_client, args=(c, len(clients)-1), daemon=True).start()
        broadcast()