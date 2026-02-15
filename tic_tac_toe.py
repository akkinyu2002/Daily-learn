"""
Tic Tac Toe Game
Simple two-player game with 9 boxes
Win by getting 3 in a row (straight or diagonal)
"""

import tkinter as tk
from tkinter import messagebox


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe - 9 Boxes")
        self.root.geometry("600x800")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(False, False)
        
        self.current_player = "X"
        self.board = [""] * 9
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
        
        # Status label
        self.status_label = tk.Label(
            self.root,
            text="Player X's turn - Select a box!",
            font=("Segoe UI", 16),
            bg="#1e1e2e",
            fg="#89b4fa"
        )
        self.status_label.pack(pady=15)
        
        # Game board frame
        self.board_frame = tk.Frame(self.root, bg="#1e1e2e")
        self.board_frame.pack(pady=20)
        
        # Create 3x3 grid (9 boxes)
        for i in range(9):
            btn = tk.Button(
                self.board_frame,
                text="",
                font=("Segoe UI", 40, "bold"),
                width=5,
                height=1,
                bg="#313244",
                fg="#cdd6f4",
                activebackground="#45475a",
                relief="flat",
                borderwidth=3,
                command=lambda idx=i: self.make_move(idx),
                cursor="hand2"
            )
            btn.grid(row=i // 3, column=i % 3, padx=8, pady=8)
            self.buttons.append(btn)
        
        # Control buttons
        control_frame = tk.Frame(self.root, bg="#1e1e2e")
        control_frame.pack(pady=25)
        
        reset_btn = tk.Button(
            control_frame,
            text="🔄 New Game",
            command=self.reset_game,
            font=("Segoe UI", 12, "bold"),
            bg="#a6e3a1",
            fg="#1e1e2e",
            activebackground="#94e2d5",
            relief="flat",
            padx=30,
            pady=12,
            cursor="hand2"
        )
        reset_btn.pack()
    
    def make_move(self, index):
        """Handle player selecting a box"""
        if self.board[index] == "" and not self.game_over:
            # Mark the box with current player's symbol
            self.board[index] = self.current_player
            self.buttons[index].config(
                text=self.current_player,
                fg="#89b4fa" if self.current_player == "X" else "#f38ba8"
            )
            
            # Check if current player won
            if self.check_winner(self.current_player):
                self.end_game(f"🎉 Player {self.current_player} Wins!")
                return
            
            # Check for tie
            if "" not in self.board:
                self.end_game("🤝 It's a Tie!")
                return
            
            # Switch to other player
            self.current_player = "O" if self.current_player == "X" else "X"
            self.status_label.config(
                text=f"Player {self.current_player}'s turn - Select a box!",
                fg="#89b4fa" if self.current_player == "X" else "#f38ba8"
            )
    
    def check_winner(self, player):
        """Check if player has 3 in a row (straight or diagonal)"""
        win_conditions = [
            # Straight rows (horizontal)
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            # Straight columns (vertical)
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            # Diagonal
            [0, 4, 8], [2, 4, 6]
        ]
        
        for condition in win_conditions:
            if all(self.board[i] == player for i in condition):
                # Highlight the winning boxes
                for i in condition:
                    self.buttons[i].config(
                        bg="#a6e3a1" if player == "X" else "#f38ba8",
                        fg="#1e1e2e"
                    )
                return True
        return False
    
    def end_game(self, message):
        """End the game and display result"""
        self.game_over = True
        self.status_label.config(text=message, fg="#a6e3a1")
        
        # Disable all boxes
        for btn in self.buttons:
            btn.config(state="disabled")
    
    def reset_game(self):
        """Start a new game"""
        self.board = [""] * 9
        self.current_player = "X"
        self.game_over = False
        
        # Reset all boxes
        for btn in self.buttons:
            btn.config(
                text="",
                bg="#313244",
                fg="#cdd6f4",
                state="normal"
            )
        
        self.status_label.config(
            text="Player X's turn - Select a box!",
            fg="#89b4fa"
        )


def main():
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()


if __name__ == "__main__":
    main()
