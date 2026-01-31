import tkinter as tk
from tkinter import ttk
import math

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("420x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a2e")
        
        # Variables
        self.current_input = ""
        self.result_var = tk.StringVar()
        self.result_var.set("0")
        self.memory = 0
        self.is_radian = True  # Angle mode (True for radians, False for degrees)
        
        # Create UI
        self.create_display()
        self.create_buttons()
        
        # Keyboard bindings
        self.root.bind('<Key>', self.key_press)
        self.root.bind('<Return>', lambda e: self.calculate())
        self.root.bind('<Escape>', lambda e: self.clear_all())
        
    def create_display(self):
        # Display frame
        display_frame = tk.Frame(self.root, bg="#1a1a2e", pady=20)
        display_frame.pack(fill=tk.BOTH)
        
        # Mode indicator (RAD/DEG)
        self.mode_label = tk.Label(
            display_frame,
            text="RAD",
            font=("Segoe UI", 10),
            bg="#1a1a2e",
            fg="#00d4ff",
            anchor="e"
        )
        self.mode_label.pack(fill=tk.X, padx=20)
        
        # Result display
        result_display = tk.Entry(
            display_frame,
            textvariable=self.result_var,
            font=("Segoe UI", 28, "bold"),
            bg="#16213e",
            fg="#ffffff",
            bd=0,
            justify="right",
            state="readonly",
            readonlybackground="#16213e"
        )
        result_display.pack(fill=tk.X, padx=20, ipady=15)
        
    def create_buttons(self):
        # Button frame
        button_frame = tk.Frame(self.root, bg="#1a1a2e")
        button_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Button configuration
        button_style = {
            'font': ('Segoe UI', 11, 'bold'),
            'bd': 0,
            'relief': 'flat',
            'cursor': 'hand2'
        }
        
        # Color schemes
        colors = {
            0: {'bg': '#2d4059', 'fg': '#ffffff', 'active': '#3d5069'},  # Numbers
            1: {'bg': '#ea5455', 'fg': '#ffffff', 'active': '#fa6465'},  # Operators
            2: {'bg': '#0f3460', 'fg': '#00d4ff', 'active': '#1f4470'},  # Functions
            3: {'bg': '#ea5455', 'fg': '#ffffff', 'active': '#fa6465'},  # Special (clear, delete)
        }
        
        # Complete button layout [text, row, col, rowspan, colspan, color_type]
        # Grid: 7 rows × 6 columns
        buttons = [
            # Row 0 - Memory and Clear functions
            ('C', 0, 0, 1, 1, 3), ('⌫', 0, 1, 1, 1, 3), ('M+', 0, 2, 1, 1, 2), 
            ('MR', 0, 3, 1, 1, 2), ('MC', 0, 4, 1, 1, 2), ('÷', 0, 5, 1, 1, 1),
            
            # Row 1 - Trig functions
            ('sin', 1, 0, 1, 1, 2), ('cos', 1, 1, 1, 1, 2), ('tan', 1, 2, 1, 1, 2), 
            ('π', 1, 3, 1, 1, 0), ('e', 1, 4, 1, 1, 0), ('×', 1, 5, 1, 1, 1),
            
            # Row 2 - Power functions
            ('√', 2, 0, 1, 1, 2), ('x²', 2, 1, 1, 1, 2), ('xʸ', 2, 2, 1, 1, 2), 
            ('(', 2, 3, 1, 1, 1), (')', 2, 4, 1, 1, 1), ('-', 2, 5, 1, 1, 1),
            
            # Row 3 - Log functions + numbers
            ('ln', 3, 0, 1, 1, 2), ('log', 3, 1, 1, 1, 2), ('1/x', 3, 2, 1, 1, 2), 
            ('7', 3, 3, 1, 1, 0), ('8', 3, 4, 1, 1, 0), ('9', 3, 5, 1, 1, 0),
            
            # Row 4 - Special functions + numbers
            ('RAD', 4, 0, 1, 1, 2), ('|x|', 4, 1, 1, 1, 2), ('n!', 4, 2, 1, 1, 2), 
            ('4', 4, 3, 1, 1, 0), ('5', 4, 4, 1, 1, 0), ('6', 4, 5, 1, 1, 0),
            
            # Row 5 - Hyperbolic functions + numbers
            ('sinh', 5, 0, 1, 1, 2), ('cosh', 5, 1, 1, 1, 2), ('tanh', 5, 2, 1, 1, 2), 
            ('1', 5, 3, 1, 1, 0), ('2', 5, 4, 1, 1, 0), ('3', 5, 5, 1, 1, 0),
            
            # Row 6 - Bottom row
            ('.', 6, 0, 1, 1, 0), ('0', 6, 1, 1, 2, 0), ('±', 6, 3, 1, 1, 2), 
            ('+', 6, 4, 1, 1, 1), ('=', 6, 5, 1, 1, 1),
        ]
        
        # Create all buttons
        for btn_data in buttons:
            text, row, col, rowspan, colspan, color_type = btn_data
            color = colors[color_type]
            
            btn = tk.Button(
                button_frame,
                text=text,
                **button_style,
                bg=color['bg'],
                fg=color['fg'],
                activebackground=color['active'],
                activeforeground=color['fg'],
                command=lambda t=text: self.button_click(t)
            )
            btn.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan, 
                    sticky="nsew", padx=2, pady=2)
        
        # Configure grid weights for responsive resizing
        for i in range(7):
            button_frame.rowconfigure(i, weight=1)
        for i in range(6):
            button_frame.columnconfigure(i, weight=1)
    
    def button_click(self, value):
        """Handle button clicks"""
        try:
            if value == 'C':
                self.clear_all()
            elif value == '⌫':
                self.backspace()
            elif value == '=':
                self.calculate()
            elif value == 'M+':
                self.memory_add()
            elif value == 'MR':
                self.memory_recall()
            elif value == 'MC':
                self.memory_clear()
            elif value == 'RAD':
                self.toggle_angle_mode()
            elif value in ['sin', 'cos', 'tan', 'sinh', 'cosh', 'tanh', 'ln', 'log', '√', '|x|', 'n!', '1/x']:
                self.apply_function(value)
            elif value == 'x²':
                self.current_input += '**2'
                self.result_var.set(self.current_input)
            elif value == 'xʸ':
                self.current_input += '**'
                self.result_var.set(self.current_input)
            elif value == 'π':
                self.current_input += str(math.pi)
                self.result_var.set(self.current_input)
            elif value == 'e':
                self.current_input += str(math.e)
                self.result_var.set(self.current_input)
            elif value == '±':
                self.toggle_sign()
            elif value == '÷':
                self.current_input += '/'
                self.result_var.set(self.current_input)
            elif value == '×':
                self.current_input += '*'
                self.result_var.set(self.current_input)
            else:
                self.current_input += value
                self.result_var.set(self.current_input)
        except Exception as e:
            self.result_var.set("Error")
    
    def clear_all(self):
        """Clear all input"""
        self.current_input = ""
        self.result_var.set("0")
    
    def backspace(self):
        """Delete last character"""
        self.current_input = self.current_input[:-1]
        self.result_var.set(self.current_input if self.current_input else "0")
    
    def calculate(self):
        """Evaluate the expression"""
        try:
            if self.current_input:
                # Replace display symbols with Python operators
                expression = self.current_input.replace('×', '*').replace('÷', '/')
                result = eval(expression)
                self.result_var.set(str(result))
                self.current_input = str(result)
        except Exception:
            self.result_var.set("Error")
            self.current_input = ""
    
    def apply_function(self, func):
        """Apply mathematical function to current value"""
        try:
            if not self.current_input or self.current_input == "0":
                return
            
            value = float(eval(self.current_input))
            
            if func == 'sin':
                result = math.sin(value if self.is_radian else math.radians(value))
            elif func == 'cos':
                result = math.cos(value if self.is_radian else math.radians(value))
            elif func == 'tan':
                result = math.tan(value if self.is_radian else math.radians(value))
            elif func == 'sinh':
                result = math.sinh(value)
            elif func == 'cosh':
                result = math.cosh(value)
            elif func == 'tanh':
                result = math.tanh(value)
            elif func == 'ln':
                result = math.log(value)
            elif func == 'log':
                result = math.log10(value)
            elif func == '√':
                result = math.sqrt(value)
            elif func == '|x|':
                result = abs(value)
            elif func == 'n!':
                result = math.factorial(int(value))
            elif func == '1/x':
                result = 1 / value
            
            self.current_input = str(result)
            self.result_var.set(self.current_input)
        except Exception:
            self.result_var.set("Error")
            self.current_input = ""
    
    def toggle_sign(self):
        """Toggle between positive and negative"""
        try:
            if self.current_input and self.current_input != "0":
                if self.current_input.startswith('-'):
                    self.current_input = self.current_input[1:]
                else:
                    self.current_input = '-' + self.current_input
                self.result_var.set(self.current_input)
        except Exception:
            pass
    
    def memory_add(self):
        """Add current value to memory"""
        try:
            if self.current_input:
                self.memory += float(eval(self.current_input))
        except Exception:
            pass
    
    def memory_recall(self):
        """Recall memory value"""
        self.current_input = str(self.memory)
        self.result_var.set(self.current_input)
    
    def memory_clear(self):
        """Clear memory"""
        self.memory = 0
    
    def toggle_angle_mode(self):
        """Toggle between radians and degrees"""
        self.is_radian = not self.is_radian
        self.mode_label.config(text="RAD" if self.is_radian else "DEG")
    
    def key_press(self, event):
        """Handle keyboard input"""
        key = event.char
        if key.isdigit() or key in ['.', '+', '-', '*', '/', '(', ')']:
            self.current_input += key
            self.result_var.set(self.current_input)
        elif event.keysym == 'BackSpace':
            self.backspace()

def main():
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
