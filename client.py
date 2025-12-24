import pygame, socket, json, threading

pygame.init()
WIDTH, CELL = 640, 80
screen = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("✨ SyuzCheckers Online ✨")

# Original Colors
WHITE, GREEN = (235, 235, 208), (119, 148, 85)
RED, BLACK, GOLD, HIGH = (200, 0, 0), (20, 20, 20), (255, 215, 0), (0, 255, 0)

board, turn, player, selected, valid_moves, connected = [], 0, None, None, [], False
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = input("Enter Public IP Address: ")
try:
    sock.connect((ip, 5555))
    connected = True
except:
    print("Connection failed! Check Port Forwarding.")

def receive():
    global board, turn, player, connected
    while True:
        try:
            data = sock.recv(4096).decode()
            if not data: continue
            msg = json.loads(data)
            if "player" in msg and player is None: player = msg["player"]
            if "board" in msg: board, turn, connected = msg["board"], msg["turn"], True
        except: break

threading.Thread(target=receive, daemon=True).start()

def get_moves(x, y):
    moves = []
    p = board[y][x]
    is_king = p.isupper()
    # Direction logic: Red (Player 0) up, Black (Player 1) down
    dirs = [(-1,-1),(1,-1),(-1,1),(1,1)] if is_king else ([(-1,-1),(1,-1)] if player==0 else [(-1,1),(1,1)])
    for dx, dy in dirs:
        dist = 1
        while True:
            nx, ny = x + dx*dist, y + dy*dist
            if not (0 <= nx < 8 and 0 <= ny < 8): break
            if board[ny][nx] == "":
                moves.append((nx, ny))
                if not is_king: break
            else:
                if board[ny][nx].lower() != p.lower():
                    jx, jy = nx+dx, ny+dy
                    if 0<=jx<8 and 0<=jy<8 and board[jy][jx]=="": moves.append((jx, jy))
                break
            dist += 1
    return moves

while True:
    screen.fill((0,0,0))
    for y in range(8):
        for x in range(8):
            pygame.draw.rect(screen, WHITE if (x+y)%2==0 else GREEN, (x*CELL, y*CELL, CELL, CELL))
            if (x,y) in valid_moves: pygame.draw.rect(screen, HIGH, (x*CELL, y*CELL, CELL, CELL), 5)
            p = board[y][x] if board else ""
            if p:
                c = RED if p.lower() == "r" else BLACK
                pygame.draw.circle(screen, c, (x*CELL+40, y*CELL+40), 30)
                if p.isupper(): pygame.draw.circle(screen, GOLD, (x*CELL+40, y*CELL+40), 10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); exit()
        if connected and board and event.type == pygame.MOUSEBUTTONDOWN and turn == player:
            x, y = event.pos[0]//CELL, event.pos[1]//CELL
            if (x, y) in valid_moves:
                sock.sendall(json.dumps({"type":"move","player":player,"from":selected,"to":(x,y)}).encode())
                selected, valid_moves = None, []
            elif board[y][x] and board[y][x].lower() == ("r" if player == 0 else "b"):
                selected, valid_moves = (x, y), get_moves(x, y)
    
    pygame.display.update()