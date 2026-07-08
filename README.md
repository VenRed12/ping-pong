# Project: Real-Time Ping Pong Game

This project is a terminal-based ping pong game using **Pygame**. It introduces students to interactive game design using object-oriented principles and real-time graphical rendering.

---
## Getting Started

### Setup

1. Clone the repo or download the project folder.
2. Make sure you have Python 3.10+ installed.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the game:

```bash
python main.py
```

---

## Expected Behavior

- Smooth paddle movement using `W` and `S`
- AI tracks and plays competitively
- Ball rebounds on paddle and wall hits
- Score updates on each miss
- Game ends and optionally restarts when limit reached

---

## Folder Structure

```
pygame-pingpong/
├── main.py
├── requirements.txt
├── game/
│   ├── game_engine.py
│   ├── paddle.py
│   └── ball.py
└── README.md

