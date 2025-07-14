import tkinter as tk
import random
from tkinter import messagebox

class TicTacGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Custom Tic Tac Toe")
        self.current_player = "X"
        self.board = [" " for _ in range(9)]
        self.difficulty = "medium"  # Default
        
        self.setup_gui()
        
    def setup_gui(self):
        # Menu for difficulty
        menubar = tk.Menu(self.root)
        diff_menu = tk.Menu(menubar, tearoff=0)
        diff_menu.add_command(label="Easy", command=lambda: self.set_difficulty("easy"))
        diff_menu.add_command(label="Medium", command=lambda: self.set_difficulty("medium"))
        diff_menu.add_command(label="Hard", command=lambda: self.set_difficulty("hard"))
        menubar.add_cascade(label="Difficulty", menu=diff_menu)
        self.root.config(menu=menubar)

        # Game board
        self.buttons = []
        for i in range(9):
            btn = tk.Button(self.root, text=" ", font=('Helvetica', 24), height=2, width=5,
                          command=lambda idx=i: self.player_move(idx))
            btn.grid(row=i//3, column=i%3, sticky="nsew")
            self.buttons.append(btn)
            
        # Reset button
        reset_btn = tk.Button(self.root, text="New Game", command=self.reset_game)
        reset_btn.grid(row=3, column=0, columnspan=3, sticky="nsew")

    def set_difficulty(self, level):
        self.difficulty = level
        messagebox.showinfo("Difficulty Set", f"Changed to {level.capitalize()} mode")

    def player_move(self, position):
        if self.board[position] == " " and not self.check_winner():
            self.update_board(position, "X")
            if not self.check_winner() and " " in self.board:
                self.ai_move()

    def ai_move(self):
        available = [i for i, x in enumerate(self.board) if x == " "]
        
        if not available:
            return
            
        if self.difficulty == "easy":
            move = random.choice(available)
        elif self.difficulty == "medium":
            # Sometimes block, sometimes random
            move = self.find_winning_move("O") or self.find_winning_move("X") or random.choice(available)
        else:  # hard
            move = self.find_best_move()
            
        self.update_board(move, "O")
        self.current_player = "X"  # Switch back to player

    def find_winning_move(self, player):
        for move in [i for i, x in enumerate(self.board) if x == " "]:
            temp_board = self.board.copy()
            temp_board[move] = player
            if self.check_winner(temp_board):
                return move
        return None

    def find_best_move(self):
        # Simple scoring system (not minimax)
        best_score = -100
        best_move = None
        
        for move in [i for i, x in enumerate(self.board) if x == " "]:
            temp_board = self.board.copy()
            temp_board[move] = "O"
            
            score = 0
            # Prioritize center
            if move == 4: score += 3
            
            # Check for wins
            if self.check_winner(temp_board):
                score += 10
            
            # Check if player can win next
            temp_board[move] = "X"
            if self.check_winner(temp_board):
                score += 5
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move

    def update_board(self, position, player):
        self.board[position] = player
        self.buttons[position].config(text=player, state="disabled")
        
        winner = self.check_winner()
        if winner:
            self.end_game(f"{winner} wins!")
        elif " " not in self.board:
            self.end_game("It's a tie!")

    def check_winner(self, board=None):
        board = board or self.board
        lines = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for a,b,c in lines:
            if board[a] == board[b] == board[c] != " ":
                return board[a]
        return None

    def end_game(self, msg):
        for btn in self.buttons:
            btn.config(state="disabled")
        messagebox.showinfo("Game Over", msg)

    def reset_game(self):
        self.current_player = "X"
        self.board = [" " for _ in range(9)]
        for btn in self.buttons:
            btn.config(text=" ", state="normal")

if __name__ == "__main__":
    window = tk.Tk()
    game = TicTacGame(window)  # Fixed class name
    window.mainloop()
