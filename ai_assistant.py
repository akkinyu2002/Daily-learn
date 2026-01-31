import tkinter as tk
from tkinter import scrolledtext, messagebox
import speech_recognition as sr
import pyttsx3
import os
import subprocess
import datetime
import webbrowser
import psutil
import threading
from pathlib import Path

class VoiceAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Voice Assistant - Jarvis 🤖")
        self.root.geometry("900x700")
        self.root.configure(bg="#0a0e27")
        
        # Initialize speech engines
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.setup_voice()
        
        # Assistant state
        self.listening = False
        self.continuous_mode = False
        self.assistant_name = "Jarvis"
        
        # Conversation context
        self.conversation_history = []
        self.last_topic = None
        self.awaiting_confirmation = None
        self.user_name = None
        
        # Create UI
        self.create_ui()
        
        # Welcome message
        self.speak("Hello! I'm your AI assistant. How can I help you today?")
        self.add_message("Assistant", "Hello! I'm your AI assistant. How can I help you today?")
        
    def setup_voice(self):
        """Configure text-to-speech settings"""
        voices = self.engine.getProperty('voices')
        # Set to female voice if available, otherwise use default
        if len(voices) > 1:
            self.engine.setProperty('voice', voices[1].id)
        self.engine.setProperty('rate', 180)  # Speed
        self.engine.setProperty('volume', 0.9)  # Volume
        
    def create_ui(self):
        """Create the user interface"""
        # Header
        header_frame = tk.Frame(self.root, bg="#1a1f3a", height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="🤖 AI Voice Assistant",
            font=("Segoe UI", 24, "bold"),
            bg="#1a1f3a",
            fg="#00d4ff"
        ).pack(side=tk.LEFT, padx=30, pady=20)
        
        # Status indicator
        self.status_label = tk.Label(
            header_frame,
            text="● Ready",
            font=("Segoe UI", 12),
            bg="#1a1f3a",
            fg="#00ff88"
        )
        self.status_label.pack(side=tk.RIGHT, padx=30)
        
        # Chat display
        chat_frame = tk.Frame(self.root, bg="#0a0e27")
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            chat_frame,
            text="💬 Conversation",
            font=("Segoe UI", 14, "bold"),
            bg="#0a0e27",
            fg="#00d4ff",
            anchor="w"
        ).pack(fill=tk.X, pady=(0, 10))
        
        # Scrolled text for chat
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            font=("Segoe UI", 11),
            bg="#16213e",
            fg="#ffffff",
            wrap=tk.WORD,
            state=tk.DISABLED,
            bd=0,
            padx=15,
            pady=15
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for colors
        self.chat_display.tag_config("user", foreground="#00d4ff", font=("Segoe UI", 11, "bold"))
        self.chat_display.tag_config("assistant", foreground="#00ff88", font=("Segoe UI", 11, "bold"))
        self.chat_display.tag_config("system", foreground="#ffa500", font=("Segoe UI", 10, "italic"))
        
        # Input area
        input_frame = tk.Frame(self.root, bg="#1a1f3a")
        input_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Text input
        self.text_input = tk.Entry(
            input_frame,
            font=("Segoe UI", 12),
            bg="#0f1729",
            fg="#ffffff",
            insertbackground="#00d4ff",
            bd=0
        )
        self.text_input.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=12, padx=(15, 10))
        self.text_input.bind('<Return>', lambda e: self.process_text_input())
        
        # Send button
        tk.Button(
            input_frame,
            text="Send",
            font=("Segoe UI", 11, "bold"),
            bg="#00d4ff",
            fg="#0a0e27",
            activebackground="#00b4df",
            bd=0,
            cursor="hand2",
            command=self.process_text_input,
            padx=25,
            pady=10
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Voice button
        self.voice_btn = tk.Button(
            input_frame,
            text="🎤 Voice",
            font=("Segoe UI", 11, "bold"),
            bg="#00ff88",
            fg="#0a0e27",
            activebackground="#00df78",
            bd=0,
            cursor="hand2",
            command=self.toggle_listening,
            padx=20,
            pady=10
        )
        self.voice_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Continuous mode button
        self.continuous_btn = tk.Button(
            input_frame,
            text="� Continuous",
            font=("Segoe UI", 11, "bold"),
            bg="#8892b0",
            fg="#0a0e27",
            activebackground="#7882a0",
            bd=0,
            cursor="hand2",
            command=self.toggle_continuous_mode,
            padx=15,
            pady=10
        )
        self.continuous_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # Commands info
        info_text = "💡 Continuous mode for natural conversation | Say naturally: 'my name is...', 'remember that...', 'what did I say about...'"
        tk.Label(
            self.root,
            text=info_text,
            font=("Segoe UI", 9),
            bg="#1a1f3a",
            fg="#8892b0",
            pady=10,
            padx=20,
            anchor="w"
        ).pack(fill=tk.X, side=tk.BOTTOM)
        
    def add_message(self, sender, message):
        """Add a message to the chat display"""
        self.chat_display.config(state=tk.NORMAL)
        
        # Add timestamp
        timestamp = datetime.datetime.now().strftime("%H:%M")
        
        if sender == "You":
            self.chat_display.insert(tk.END, f"\n[{timestamp}] ", "system")
            self.chat_display.insert(tk.END, f"{sender}: ", "user")
        else:
            self.chat_display.insert(tk.END, f"\n[{timestamp}] ", "system")
            self.chat_display.insert(tk.END, f"{sender}: ", "assistant")
            
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
    def speak(self, text):
        """Convert text to speech"""
        def speak_thread():
            self.engine.say(text)
            self.engine.runAndWait()
        
        thread = threading.Thread(target=speak_thread)
        thread.daemon = True
        thread.start()
        
    def toggle_listening(self):
        """Toggle voice listening mode"""
        if not self.listening:
            self.start_listening()
        else:
            self.stop_listening()
            
    def start_listening(self):
        """Start listening for voice commands"""
        self.listening = True
        self.voice_btn.config(text="⏹ Stop", bg="#ea5455")
        self.status_label.config(text="● Listening...", fg="#ea5455")
        
        thread = threading.Thread(target=self.listen_for_command)
        thread.daemon = True
        thread.start()
        
    def stop_listening(self):
        """Stop listening for voice commands"""
        self.listening = False
        if not self.continuous_mode:
            self.voice_btn.config(text="🎤 Voice", bg="#00ff88")
            self.status_label.config(text="● Ready", fg="#00ff88")
        else:
            # In continuous mode, restart listening after a short delay
            self.root.after(1000, self.start_listening)
            
    def toggle_continuous_mode(self):
        """Toggle continuous conversation mode"""
        self.continuous_mode = not self.continuous_mode
        
        if self.continuous_mode:
            self.continuous_btn.config(bg="#00d4ff", text="🔄 Active")
            self.add_message("System", "Continuous mode ON - I'll keep listening after each response")
            self.speak("Continuous conversation mode activated. I'm all ears!")
            if not self.listening:
                self.start_listening()
        else:
            self.continuous_btn.config(bg="#8892b0", text="🔄 Continuous")
            self.add_message("System", "Continuous mode OFF")
            self.speak("Continuous mode deactivated")
            if self.listening:
                self.stop_listening()
        
    def listen_for_command(self):
        """Listen for voice input"""
        try:
            with sr.Microphone() as source:
                self.add_message("System", "Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                self.add_message("System", "Processing...")
                command = self.recognizer.recognize_google(audio).lower()
                
                self.add_message("You", command)
                self.process_command(command)
                
        except sr.WaitTimeoutError:
            self.add_message("System", "No speech detected. Try again.")
        except sr.UnknownValueError:
            self.add_message("System", "Sorry, I couldn't understand that.")
        except sr.RequestError:
            self.add_message("System", "Speech recognition service unavailable.")
        except Exception as e:
            self.add_message("System", f"Error: {str(e)}")
        finally:
            self.stop_listening()
            
    def process_text_input(self):
        """Process text input from entry field"""
        command = self.text_input.get().strip()
        if command:
            self.add_message("You", command)
            self.text_input.delete(0, tk.END)
            self.process_command(command.lower())
            
    def process_command(self, command):
        """Process and execute commands with context awareness"""
        response = ""
        
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": command, "time": datetime.datetime.now()})
        
        # Keep only last 10 exchanges
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
        
        try:
            # Handle conversation context
            if self.awaiting_confirmation:
                if any(word in command for word in ["yes", "yeah", "sure", "ok", "confirm", "do it"]):
                    return self.execute_pending_action()
                elif any(word in command for word in ["no", "nope", "cancel", "don't", "stop"]):
                    self.awaiting_confirmation = None
                    response = "Okay, cancelled. What else can I help you with?"
                    self.add_message("Assistant", response)
                    self.speak(response)
                    return
            
            # Learn user name
            if "my name is" in command or "i am" in command or "i'm" in command:
                name_parts = command.replace("my name is", "").replace("i am", "").replace("i'm", "").strip()
                self.user_name = name_parts.split()[0].capitalize()
                response = f"Nice to meet you, {self.user_name}! I'll remember your name. How can I help you today?"
                
            # Remember information
            elif "remember" in command or "note that" in command:
                info = command.replace("remember", "").replace("note that", "").replace("that", "", 1).strip()
                self.last_topic = info
                response = f"Got it! I'll remember: {info}"
                
            # Recall information
            elif "what did i say" in command or "what do you remember" in command or "remind me" in command:
                if self.last_topic:
                    response = f"You told me to remember: {self.last_topic}"
                elif len(self.conversation_history) > 2:
                    last_user_msg = [msg for msg in self.conversation_history if msg["role"] == "user"][-2]
                    response = f"Earlier you said: {last_user_msg['content']}"
                else:
                    response = "We just started talking. I don't have much context yet!"
                    
            # Follow-up questions
            elif command in ["why", "how", "what", "when", "where", "who"] or command.startswith(("why", "how", "what")):
                if len(self.conversation_history) > 1:
                    response = f"I'm still learning to handle complex questions. Could you be more specific about '{command}'?"
                else:
                    response = "What would you like to know about?"
                    
            # Greetings with personalization
            elif any(word in command for word in ["hello", "hi", "hey"]):
                if self.user_name:
                    response = f"Hello {self.user_name}! How can I assist you today?"
                else:
                    response = "Hello! How can I assist you today? Feel free to tell me your name!"
                
            # Time
            elif "time" in command:
                current_time = datetime.datetime.now().strftime("%I:%M %p")
                response = f"The current time is {current_time}"
                
            # Date
            elif "date" in command or "today" in command:
                current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
                response = f"Today is {current_date}"
                
            # Open applications
            elif "open" in command:
                app_name = command.replace("open", "").strip()
                response = self.open_application(app_name)
                
            # Close applications
            elif "close" in command or "kill" in command:
                app_name = command.replace("close", "").replace("kill", "").strip()
                response = self.close_application(app_name)
                
            # System control with natural confirmation
            elif "shutdown" in command or "shut down" in command:
                self.awaiting_confirmation = "shutdown"
                response = "Are you sure you want to shutdown the system? Just say yes or no."
                
            elif "restart" in command or "reboot" in command:
                self.awaiting_confirmation = "restart"
                response = "Are you sure you want to restart the system? Just say yes or no."
                
            # Cancel shutdown
            elif "cancel" in command and ("shutdown" in command or "restart" in command):
                os.system("shutdown /a")
                response = "Shutdown cancelled."
                
            # Search
            elif "search" in command or "google" in command:
                query = command.replace("search", "").replace("google", "").strip()
                if query:
                    webbrowser.open(f"https://www.google.com/search?q={query}")
                    response = f"Searching for '{query}' on Google."
                else:
                    response = "What would you like me to search for?"
                    
            # YouTube
            elif "youtube" in command:
                query = command.replace("youtube", "").strip()
                if query:
                    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
                    response = f"Searching YouTube for '{query}'."
                else:
                    webbrowser.open("https://www.youtube.com")
                    response = "Opening YouTube."
                    
            # List files
            elif "list files" in command or "show files" in command:
                path = command.replace("list files in", "").replace("show files in", "").strip()
                if not path or path == "":
                    path = os.getcwd()
                response = self.list_files(path)
                
            # Read file
            elif "read file" in command or "open file" in command:
                filepath = command.replace("read file", "").replace("open file", "").strip()
                response = self.read_file(filepath)
                
            # System info
            elif "system info" in command or "system status" in command:
                response = self.get_system_info()
                
            # Running processes
            elif "running" in command and "process" in command:
                response = self.list_running_processes()
                
            # Conversational responses
            elif any(word in command for word in ["thank", "thanks", "appreciate"]):
                responses = [
                    "You're welcome!",
                    "Happy to help!",
                    "Anytime!",
                    "My pleasure!"
                ]
                import random
                response = random.choice(responses)
                
            elif any(word in command for word in ["bye", "goodbye", "see you"]):
                response = f"Goodbye{' ' + self.user_name if self.user_name else ''}! Talk to you soon!"
                
            elif "how are you" in command or "how's it going" in command:
                response = "I'm doing great! Thanks for asking. Ready to help you with anything you need!"
                
            elif "who are you" in command or "what are you" in command:
                response = "I'm your personal AI assistant. I can control your system, answer questions, and have conversations with you!"
                
            # Help
            elif "help" in command or "what can you do" in command:
                response = self.get_help_text()
                
            # Smart default response
            else:
                if len(command.split()) <= 3:
                    response = "I'm not sure what you mean. Could you elaborate?"
                else:
                    response = "I'm still learning! I can help with opening apps, system info, searches, and more. Say 'help' for commands."
                
        except Exception as e:
            response = f"Sorry, I encountered an error: {str(e)}"
            
        # Send response
        self.conversation_history.append({"role": "assistant", "content": response, "time": datetime.datetime.now()})
        self.add_message("Assistant", response)
        self.speak(response)
        
    def execute_pending_action(self):
        """Execute action awaiting confirmation"""
        action = self.awaiting_confirmation
        self.awaiting_confirmation = None
        
        if action == "shutdown":
            response = "Alright, shutting down in 10 seconds..."
            self.add_message("Assistant", response)
            self.speak(response)
            os.system("shutdown /s /t 10")
        elif action == "restart":
            response = "Okay, restarting in 10 seconds..."
            self.add_message("Assistant", response)
            self.speak(response)
            os.system("shutdown /r /t 10")
        else:
            response = "Confirmed!"
            self.add_message("Assistant", response)
            self.speak(response)
        
    def open_application(self, app_name):
        """Open an application"""
        apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
            "browser": "start msedge",
            "chrome": "start chrome",
            "edge": "start msedge",
            "firefox": "start firefox",
            "explorer": "explorer.exe",
            "cmd": "cmd.exe",
            "powershell": "powershell.exe"
        }
        
        for key, value in apps.items():
            if key in app_name:
                try:
                    os.system(value)
                    return f"Opening {key}..."
                except:
                    return f"Couldn't open {key}."
                    
        return f"I don't know how to open '{app_name}'. Try: notepad, calculator, browser, etc."
        
    def close_application(self, app_name):
        """Close a running application"""
        app_processes = {
            "notepad": "notepad.exe",
            "calculator": "CalculatorApp.exe",
            "paint": "mspaint.exe",
            "chrome": "chrome.exe",
            "edge": "msedge.exe",
            "firefox": "firefox.exe"
        }
        
        for key, process in app_processes.items():
            if key in app_name:
                try:
                    os.system(f"taskkill /f /im {process}")
                    return f"Closed {key}."
                except:
                    return f"Couldn't close {key}."
                    
        return f"I don't know how to close '{app_name}'."
        
    def list_files(self, path):
        """List files in a directory"""
        try:
            path = Path(path).expanduser()
            if not path.exists():
                return f"Path '{path}' doesn't exist."
                
            files = list(path.iterdir())[:10]  # Limit to 10 items
            if not files:
                return f"No files found in {path}"
                
            file_list = "\n".join([f"  • {f.name}" for f in files])
            return f"Files in {path}:\n{file_list}\n(Showing first 10 items)"
        except Exception as e:
            return f"Error listing files: {str(e)}"
            
    def read_file(self, filepath):
        """Read and display file contents (text files only)"""
        try:
            filepath = Path(filepath).expanduser()
            if not filepath.exists():
                return f"File '{filepath}' doesn't exist."
                
            # Check file size (limit to 1KB for voice)
            if filepath.stat().st_size > 1000:
                return f"File is too large to read aloud. It contains {filepath.stat().st_size} bytes."
                
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            return f"Content of {filepath.name}:\n{content[:500]}"
        except UnicodeDecodeError:
            return "This appears to be a binary file. I can only read text files."
        except Exception as e:
            return f"Error reading file: {str(e)}"
            
    def get_system_info(self):
        """Get system information"""
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        info = f"System Status:\n"
        info += f"  • CPU Usage: {cpu}%\n"
        info += f"  • Memory: {memory.percent}% ({memory.used / (1024**3):.1f}GB / {memory.total / (1024**3):.1f}GB)\n"
        info += f"  • Disk: {disk.percent}% ({disk.used / (1024**3):.1f}GB / {disk.total / (1024**3):.1f}GB)"
        
        return info
        
    def list_running_processes(self):
        """List running processes"""
        processes = []
        for proc in psutil.process_iter(['name']):
            try:
                processes.append(proc.info['name'])
            except:
                pass
                
        # Get unique process names, limit to 10
        unique_processes = list(set(processes))[:10]
        proc_list = "\n".join([f"  • {p}" for p in unique_processes])
        
        return f"Running processes (showing 10):\n{proc_list}"
        
    def get_help_text(self):
        """Return help information"""
        help_text = """I can help you with:

🗣️ Voice Commands:
  • "What time is it?"
  • "What's the date?"
  • "Open [notepad/calculator/browser]"
  • "Close [application]"
  • "Shutdown/Restart system"
  • "Search [query]"
  • "YouTube [search]"
  
📁 File Operations:
  • "List files in [path]"
  • "Read file [filepath]"
  
💻 System Info:
  • "System info"
  • "Running processes"
  
Just speak naturally or type your command!"""
        
        return help_text

def main():
    root = tk.Tk()
    app = VoiceAssistant(root)
    root.mainloop()

if __name__ == "__main__":
    main()
