CheckersOnline (SyuzChecker)
CheckersOnline is a two-player online Checkers game built in Python.
It allows two people to connect from different computers and play against each other in real time over the internet or local Wi-Fi.
This project was created as a learning project to understand how networked games, client–server communication, and game interfaces work together.
What this game does
Lets two players play Checkers online
Works across different Wi-Fi networks
Shows a clean Pygame-based board
Highlights valid moves
Supports captures and king pieces
Automatically switches turns
Keeps both players perfectly in sync
How it works
The project has two parts:
Server
The server is the brain of the game. It:
Stores the game board
Checks if moves are legal
Handles captures and king promotion
Sends updates to both players
It is written using:
socket for networking
threading to handle two players
json to send game data
Client
Each player runs the client. It:
Draws the board using Pygame
Lets the player click pieces to move
Sends moves to the server
Receives real-time updates from the server
The server is always in control, so cheating is not possible and both players see the same game.
Game rules
Red moves upward, Black moves downward
Kings can move in all directions
You capture by jumping over the opponent
Reaching the opposite side turns a piece into a King
Only the current player can move
How to run the game
1. Install Python
Make sure Python 3 is installed on both computers.
2. Install Pygame
Run on both machines:
pip install pygame
3. Start the server
On one computer:
python server.py
This computer must have port 5555 open.
4. Start the clients
On both players’ computers:
python client.py
Enter the IP address of the server when asked.
How to play
Click one of your pieces to select it
Green squares show valid moves
Click a green square to move
The game changes turns automatically
Why this project
I wanted to build a real online game, not just something that works on one computer.
This project helped me learn:
Networking with sockets
Multiplayer game logic
Client-server architecture
Python and Pygame
It’s a great project for a GitHub portfolio.
Author
Syuzanna Harutyunyan
