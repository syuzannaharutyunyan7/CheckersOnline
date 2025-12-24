Here you go — clean, simple, and ready to **copy-paste as your README.md**:

---

# ♟️ CheckersOnline

CheckersOnline is a two-player **online Checkers game** built using **Python** and **Pygame**.
It allows two people to connect from different computers and play against each other in real time over the internet or local Wi-Fi.

This project was created to learn how **online multiplayer games work**, how computers communicate using **sockets**, and how to build a graphical game interface in Python.

---

## Features

* Online multiplayer (two players)
* Works over local network or the internet
* Clean and simple Pygame interface
* Valid moves are highlighted
* Supports captures and king pieces
* Automatic turn switching
* Real-time board synchronization

---

## How it works

The project consists of two programs:

### Server

The server controls the game. It:

* Stores the game board
* Checks if moves are valid
* Handles captures and king promotion
* Sends the updated board to both players

It uses sockets for networking and threads to handle two players at the same time.

---

### Client

Each player runs the client. It:

* Displays the board using Pygame
* Lets players click pieces to move them
* Sends moves to the server
* Receives live updates from the server

The server is always responsible for the rules, which keeps the game fair and synchronized.

---

## Game rules

* Red moves upward, Black moves downward
* Kings can move in all directions
* Pieces capture by jumping over the opponent
* Reaching the opposite side turns a piece into a King
* Only the player whose turn it is can move

---

## How to run

### 1. Install Python

Make sure Python 3 is installed on both computers.

### 2. Install Pygame

Run this on both machines:

```
pip install pygame
```

### 3. Start the server

On one computer:

```
python server.py
```

Make sure port **5555** is open on this computer.

### 4. Start the clients

On both players’ computers:

```
python client.py
```

When asked, enter the **IP address** of the computer running the server.

---

## How to play

* Click a piece to select it
* Green squares show where you can move
* Click a green square to move
* Turns change automatically

---

## Author

Syuzanna Harutyunyan


---
