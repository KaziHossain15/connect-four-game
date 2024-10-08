from flask import Flask, render_template, request, jsonify, send_from_directory
import random

app = Flask(__name__)

class Board:
    def __init__(self, height, width):
        "constructor method"
        self.height = height
        self.width = width
        self.slots = [[' '] * self.width for _ in range(self.height)]

    def add_checker(self, checker, col):
        """Add a checker to the specified column."""
        for row in range(self.height - 1, -1, -1):
            if self.slots[row][col] == ' ':
                self.slots[row][col] = checker
                return True
        return False

    def is_win_for(self, checker):
        """Check if the current player has won the game."""
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # down, right, diagonal-right, diagonal-left
        for row in range(self.height):
            for col in range(self.width):
                if self.slots[row][col] == checker:
                    for direction in directions:
                        if self.check_win_from(row, col, direction[0], direction[1], checker):
                            return True
        return False

    def check_win_from(self, row, col, d_row, d_col, checker):
        """Check for 4 checkers in a row in the given direction."""
        for i in range(1, 4):  # Check the next 3 positions (since first position is already checker)
            r, c = row + d_row * i, col + d_col * i
            if r < 0 or r >= self.height or c < 0 or c >= self.width or self.slots[r][c] != checker:
                return False
        return True

    def can_add_to(self, col):
        """Check if a checker can be added to the column (if it's not full)."""
        return self.slots[0][col] == ' '

    def reset(self):
        """Reset the board to its initial empty state."""
        self.slots = [[' '] * self.width for _ in range(self.height)]

    def is_full(self):
        """Check if the entire board is full."""
        for col in range(self.width):
            if self.can_add_to(col):
                return False
        return True


class AIPlayer:
    def __init__(self, checker):
        "constructor method for AI"
        self.checker = checker

    def next_move(self, board):
        """AI chooses a random valid column to place a checker."""
        valid_moves = [col for col in range(board.width) if board.can_add_to(col)]
        return random.choice(valid_moves)


board = Board(6, 7)  # Standard Connect Four board size
ai_player = AIPlayer('O')  # AI plays as 'O'

@app.route('/')
def index():
    """Serve the main game interface (e.g., index.html)."""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/move', methods=['POST'])
def move():
    """Handle a player move, followed by the AI's move."""
    data = request.get_json()
    checker = data['checker']  # 'X' for player, 'O' for AI
    col = data['col']  # Column chosen by the player

    # Player move
    if board.add_checker(checker, col):
        # Check if player wins
        if board.is_win_for(checker):
            return jsonify({'status': 'win', 'checker': checker})

        # Check for a tie (if the board is full)
        if board.is_full():
            return jsonify({'status': 'tie'})

        # AI move
        ai_col = ai_player.next_move(board)
        board.add_checker(ai_player.checker, ai_col)

        # Check if AI wins
        if board.is_win_for(ai_player.checker):
            return jsonify({'status': 'continue', 'ai_col': ai_col, 'ai_status': 'win'})

        return jsonify({'status': 'continue', 'ai_col': ai_col})

    return jsonify({'status': 'invalid'})  # Return 'invalid' if the player tries an illegal move

@app.route('/reset', methods=['POST'])
def reset():
    """Reset the board to start a new game."""
    board.reset()
    return jsonify({'status': 'reset'})

if __name__ == '__main__':
    app.run(debug=True)
