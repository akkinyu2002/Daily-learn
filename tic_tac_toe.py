"""
Tic Tac Toe Game
Modern GUI with Player vs Player and Player vs AI modes
Features minimax algorithm for unbeatable AI
"""

import tkinter as tk
from tkinter import messagebox
import random


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("500x650")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(False, False)
        
        self.current_player = "X"
        self.board = [""] * 9
        self.game_mode = None  # "PvP" or "AI"
        self.buttons = []
        self.game_over = False
        
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.root,
            text="🎮 Tic Tac Toe",
            font=("Segoe UI", 28, "bold"),
            bg="#1e1e2e",
            fg="#cdd6f4"
        )
        title_label.pack(pady=20)
        
        # Mode selection frame
        self.mode_frame = tk.Frame(self.root, bg="#1e1e2e")
        self.mode_frame.pack(pady=15)
        
        mode_label = tk.Label(
            self.mode_frame,
            text="Choose Game Mode:",
            font=("Segoe UI", 14),
            bg="#1e1e2e",
            fg="#cdd6f4"
        )
        mode_label.pack(pady=10)
        
        button_frame = tk.Frame(self.mode_frame, bg="#1e1e2e")
        button_frame.pack()
        
        pvp_btn = tk.Button(
            button_frame,
            text="👥 Player vs Player",
            command=lambda: self.start_game("PvP"),
            font=("Segoe UI", 12, "bold"),
            bg="#89b4fa",
            fg="#1e1e2e",
            activebackground="#74c7ec",
            relief="flat",
            padx=20,
            pady=15,
            cursor="hand2",
            width=18
        )
        pvp_btn.pack(side="left", padx=10)
        
        ai_btn = tk.Button(
            button_frame,
            text="🤖 Player vs AI",
            command=lambda: self.start_game("AI"),
            font=("Segoe UI", 12, "bold"),
            bg="#a6e3a1",
            fg="#1e1e2e",
            activebackground="#94e2d5",
            relief="flat",
            padx=20,
            pady=15,
            cursor="hand2",
            width=18
        )
        ai_btn.pack(side="left", padx=10)
        
        # Status label
        self.status_label = tk.Label(
            self.root,
            text="Select a game mode to start",
            font=("Segoe UI", 14),
            bg="#1e1e2e",
            fg="#f9e2af"
        )
        self.status_label.pack(pady=15)
        
        # Game board frame
        self.board_frame = tk.Frame(self.root, bg="#1e1e2e")
        self.board_frame.pack(pady=10)
        
        # Create 3x3 grid
        for i in range(9):
            btn = tk.Button(
                self.board_frame,
                text="",
                font=("Segoe UI", 36, "bold"),
                width=4,
                height=2,
                bg="#313244",
                fg="#cdd6f4",
                activebackground="#45475a",
                relief="flat",
                borderwidth=2,
                command=lambda idx=i: self.make_move(idx),
                cursor="hand2",
                state="disabled"
            )
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)
        
        # Control buttons
        control_frame = tk.Frame(self.root, bg="#1e1e2e")
        control_frame.pack(pady=20)
        
        reset_btn = tk.Button(
            control_frame,
            text="🔄 Reset Game",
            command=self.reset_game,
            font=("Segoe UI", 11, "bold"),
            bg="#f38ba8",
            fg="#1e1e2e",
            activebackground="#eba0ac",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        reset_btn.pack()
    
    def start_game(self, mode):
        self.game_mode = mode
        self.reset_game()
        for btn in self.buttons:
            btn.config(state="normal")
        
        if mode == "PvP":
            self.status_label.config(text="Player X's turn", fg="#89b4fa")
        else:
            self.status_label.config(text="You are X, AI is O", fg="#a6e3a1")
    
    def make_move(self, index):
        if self.board[index] == "" and not self.game_over:
            self.board[index] = self.current_player
            self.buttons[index].config(
                text=self.current_player,
                fg="#89b4fa" if self.current_player == "X" else "#f38ba8"
            )
            
            if self.check_winner(self.current_player):
                self.end_game(f"Player {self.current_player} wins! 🎉")
                return
            
            if "" not in self.board:
                self.end_game("It's a tie! 🤝")
                return
            
            # Switch player
            self.current_player = "O" if self.current_player == "X" else "X"
            
            if self.game_mode == "PvP":
                self.status_label.config(text=f"Player {self.current_player}'s turn")
            else:
                if self.current_player == "O":
                    self.status_label.config(text="AI is thinking...")
                    self.root.after(500, self.ai_move)
                else:
                    self.status_label.config(text="Your turn (X)")
    
    def ai_move(self):
        """AI makes a move using minimax algorithm"""
        if self.game_over:
            return
        
        best_score = float('-inf')
        best_move = None
        
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"
                score = self.minimax(self.board, 0, False)
                self.board[i] = ""
                
                if score > best_score:
                    best_score = score
                    best_move = i
        
        if best_move is not None:
            self.board[best_move] = "O"
            self.buttons[best_move].config(text="O", fg="#f38ba8")
            
            if self.check_winner("O"):
                self.end_game("AI wins! 🤖")
                return
            
            if "" not in self.board:
                self.end_game("It's a tie! 🤝")
                return
            
            self.current_player = "X"
            self.status_label.config(text="Your turn (X)")
    
    def minimax(self, board, depth, is_maximizing):
        """Minimax algorithm for AI decision making"""
        if self.check_winner("O"):
            return 10 - depth
        if self.check_winner("X"):
            return depth - 10
        if "" not in board:
            return 0
        
        if is_maximizing:
            best_score = float('-inf')
            for i in range(9):
                if board[i] == "":
                    board[i] = "O"
                    score = self.minimax(board, depth + 1, False)
                    board[i] = ""
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == "":
                    board[i] = "X"
                    score = self.minimax(board, depth + 1, True)
                    board[i] = ""
                    best_score = min(score, best_score)
            return best_score
    
    def check_winner(self, player):
        """Check if the given player has won"""
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        
        for condition in win_conditions:
            if all(self.board[i] == player for i in condition):
                # Highlight winning combination
                for i in condition:
                    self.buttons[i].config(bg="#a6e3a1" if player == "X" else "#f38ba8")
                return True
        return False
    
    def end_game(self, message):
        """End the game and show result"""
        self.game_over = True
        self.status_label.config(text=message, fg="#a6e3a1")
        for btn in self.buttons:
            btn.config(state="disabled")
    
    def reset_game(self):
        """Reset the game board"""
        self.board = [""] * 9
        self.current_player = "X"
        self.game_over = False
        
        for btn in self.buttons:
            btn.config(
                text="",
                bg="#313244",
                state="normal" if self.game_mode else "disabled"
            )
        
        if self.game_mode == "PvP":
            self.status_label.config(text="Player X's turn", fg="#89b4fa")
        elif self.game_mode == "AI":
            self.status_label.config(text="You are X, AI is O", fg="#a6e3a1")
        else:
            self.status_label.config(text="Select a game mode to start", fg="#f9e2af")


def main():
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()


if __name__ == "__main__":
    main()
