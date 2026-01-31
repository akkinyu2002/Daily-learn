import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from datetime import datetime, timedelta
import threading

class AIStockAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Stock Market Analyzer 📈")
        self.root.geometry("1200x800")
        self.root.configure(bg="#0a0e27")
        
        # Data storage
        self.watchlist = []
        self.current_stock = None
        self.stock_data = None
        
        # Create UI
        self.create_header()
        self.create_main_layout()
        self.create_status_bar()
        
    def create_header(self):
        """Create the header section"""
        header_frame = tk.Frame(self.root, bg="#1a1f3a", height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="🤖 AI Stock Analyzer",
            font=("Segoe UI", 24, "bold"),
            bg="#1a1f3a",
            fg="#00d4ff"
        )
        title_label.pack(side=tk.LEFT, padx=30, pady=20)
        
        # Search section
        search_frame = tk.Frame(header_frame, bg="#1a1f3a")
        search_frame.pack(side=tk.RIGHT, padx=30, pady=20)
        
        tk.Label(
            search_frame,
            text="Stock Symbol:",
            font=("Segoe UI", 11),
            bg="#1a1f3a",
            fg="#ffffff"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.symbol_entry = tk.Entry(
            search_frame,
            font=("Segoe UI", 12),
            bg="#0f1729",
            fg="#ffffff",
            insertbackground="#00d4ff",
            bd=0,
            width=15
        )
        self.symbol_entry.pack(side=tk.LEFT, ipady=8, padx=(0, 10))
        self.symbol_entry.bind('<Return>', lambda e: self.analyze_stock())
        
        analyze_btn = tk.Button(
            search_frame,
            text="Analyze",
            font=("Segoe UI", 11, "bold"),
            bg="#00d4ff",
            fg="#0a0e27",
            activebackground="#00b4df",
            bd=0,
            cursor="hand2",
            command=self.analyze_stock,
            padx=20,
            pady=8
        )
        analyze_btn.pack(side=tk.LEFT)
        
    def create_main_layout(self):
        """Create main content area"""
        main_frame = tk.Frame(self.root, bg="#0a0e27")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel - Info and Watchlist
        left_panel = tk.Frame(main_frame, bg="#1a1f3a", width=350)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10), pady=0)
        left_panel.pack_propagate(False)
        
        self.create_info_panel(left_panel)
        self.create_watchlist_panel(left_panel)
        
        # Right panel - Charts and Analysis
        right_panel = tk.Frame(main_frame, bg="#0a0e27")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.create_chart_panel(right_panel)
        self.create_analysis_panel(right_panel)
        
    def create_info_panel(self, parent):
        """Create stock information panel"""
        info_frame = tk.LabelFrame(
            parent,
            text="📊 Stock Information",
            font=("Segoe UI", 12, "bold"),
            bg="#1a1f3a",
            fg="#00d4ff",
            bd=0
        )
        info_frame.pack(fill=tk.X, padx=15, pady=15)
        
        # Info labels
        self.info_labels = {}
        info_items = [
            ("Symbol:", "symbol"),
            ("Price:", "price"),
            ("Change:", "change"),
            ("Volume:", "volume"),
            ("Market Cap:", "market_cap"),
            ("P/E Ratio:", "pe_ratio")
        ]
        
        for label_text, key in info_items:
            frame = tk.Frame(info_frame, bg="#1a1f3a")
            frame.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(
                frame,
                text=label_text,
                font=("Segoe UI", 10),
                bg="#1a1f3a",
                fg="#8892b0",
                anchor="w",
                width=12
            ).pack(side=tk.LEFT)
            
            value_label = tk.Label(
                frame,
                text="-",
                font=("Segoe UI", 10, "bold"),
                bg="#1a1f3a",
                fg="#ffffff",
                anchor="w"
            )
            value_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.info_labels[key] = value_label
            
    def create_watchlist_panel(self, parent):
        """Create watchlist panel"""
        watchlist_frame = tk.LabelFrame(
            parent,
            text="⭐ Watchlist",
            font=("Segoe UI", 12, "bold"),
            bg="#1a1f3a",
            fg="#00d4ff",
            bd=0
        )
        watchlist_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Watchlist
        list_frame = tk.Frame(watchlist_frame, bg="#1a1f3a")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame, bg="#1a1f3a")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.watchlist_box = tk.Listbox(
            list_frame,
            font=("Segoe UI", 10),
            bg="#0f1729",
            fg="#ffffff",
            selectbackground="#00d4ff",
            selectforeground="#0a0e27",
            bd=0,
            yscrollcommand=scrollbar.set,
            highlightthickness=0
        )
        self.watchlist_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.watchlist_box.yview)
        
        # Buttons
        btn_frame = tk.Frame(watchlist_frame, bg="#1a1f3a")
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        add_btn = tk.Button(
            btn_frame,
            text="+ Add",
            font=("Segoe UI", 9, "bold"),
            bg="#00d4ff",
            fg="#0a0e27",
            activebackground="#00b4df",
            bd=0,
            cursor="hand2",
            command=self.add_to_watchlist,
            padx=15,
            pady=5
        )
        add_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        remove_btn = tk.Button(
            btn_frame,
            text="- Remove",
            font=("Segoe UI", 9, "bold"),
            bg="#ea5455",
            fg="#ffffff",
            activebackground="#fa6465",
            bd=0,
            cursor="hand2",
            command=self.remove_from_watchlist,
            padx=15,
            pady=5
        )
        remove_btn.pack(side=tk.LEFT)
        
    def create_chart_panel(self, parent):
        """Create chart display panel"""
        chart_frame = tk.LabelFrame(
            parent,
            text="📈 Price Chart",
            font=("Segoe UI", 12, "bold"),
            bg="#1a1f3a",
            fg="#00d4ff",
            bd=0
        )
        chart_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create matplotlib figure
        self.fig = Figure(figsize=(10, 5), facecolor="#1a1f3a")
        self.ax = self.fig.add_subplot(111, facecolor="#0f1729")
        
        # Style the plot
        self.ax.tick_params(colors="#8892b0", labelsize=9)
        self.ax.spines['bottom'].set_color('#8892b0')
        self.ax.spines['top'].set_color('#8892b0')
        self.ax.spines['left'].set_color('#8892b0')
        self.ax.spines['right'].set_color('#8892b0')
        self.ax.grid(True, alpha=0.2, color="#8892b0", linestyle="--")
        
        # Embed in tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, chart_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_analysis_panel(self, parent):
        """Create AI analysis panel"""
        analysis_frame = tk.LabelFrame(
            parent,
            text="🤖 AI Analysis & Indicators",
            font=("Segoe UI", 12, "bold"),
            bg="#1a1f3a",
            fg="#00d4ff",
            bd=0,
            height=200
        )
        analysis_frame.pack(fill=tk.X, pady=0)
        analysis_frame.pack_propagate(False)
        
        # Analysis text
        text_frame = tk.Frame(analysis_frame, bg="#1a1f3a")
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(text_frame, bg="#1a1f3a")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.analysis_text = tk.Text(
            text_frame,
            font=("Segoe UI", 10),
            bg="#0f1729",
            fg="#ffffff",
            bd=0,
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
            state=tk.DISABLED
        )
        self.analysis_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.analysis_text.yview)
        
    def create_status_bar(self):
        """Create status bar"""
        self.status_bar = tk.Label(
            self.root,
            text="Ready | Enter a stock symbol to analyze",
            font=("Segoe UI", 9),
            bg="#1a1f3a",
            fg="#8892b0",
            anchor="w",
            padx=20,
            pady=8
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def analyze_stock(self):
        """Analyze the selected stock"""
        symbol = self.symbol_entry.get().strip().upper()
        
        if not symbol:
            messagebox.showwarning("Input Error", "Please enter a stock symbol!")
            return
            
        self.status_bar.config(text=f"Fetching data for {symbol}...")
        self.current_stock = symbol
        
        # Run in separate thread to prevent UI freezing
        thread = threading.Thread(target=self.fetch_and_analyze, args=(symbol,))
        thread.daemon = True
        thread.start()
        
    def fetch_and_analyze(self, symbol):
        """Fetch stock data and perform analysis"""
        try:
            print(f"Fetching data for {symbol}...")  # Debug
            # Fetch stock data
            stock = yf.Ticker(symbol)
            
            # Get historical data (6 months)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=180)
            print(f"Fetching history from {start_date} to {end_date}...")  # Debug
            self.stock_data = stock.history(start=start_date, end=end_date)
            
            if self.stock_data.empty:
                print(f"No data found for {symbol}")  # Debug
                self.root.after(0, lambda: self.update_status(f"Error: No data found for {symbol}"))
                self.root.after(0, lambda: messagebox.showerror("Error", f"No data found for {symbol}. Please check the symbol and try again."))
                return
                
            print(f"Got {len(self.stock_data)} days of data")  # Debug
            
            # Get current info
            try:
                info = stock.info
                print(f"Got stock info: {list(info.keys())[:5]}...")  # Debug
            except Exception as info_error:
                print(f"Warning: Could not fetch full info: {info_error}")
                info = {}
            
            # Update UI in main thread
            self.root.after(0, lambda: self.update_stock_info(info, self.stock_data))
            self.root.after(0, lambda: self.plot_chart(self.stock_data, symbol))
            self.root.after(0, lambda: self.perform_technical_analysis(self.stock_data, info))
            self.root.after(0, lambda: self.update_status(f"Analysis complete for {symbol}"))
            print(f"Analysis complete for {symbol}")  # Debug
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"Exception in fetch_and_analyze: {error_msg}")  # Debug
            import traceback
            traceback.print_exc()  # Print full error trace
            self.root.after(0, lambda: self.update_status(error_msg))
            self.root.after(0, lambda: messagebox.showerror("Analysis Error", f"Failed to analyze {symbol}:\n\n{str(e)}\n\nPlease check your internet connection and try again."))
            
    def update_stock_info(self, info, data):
        """Update stock information display"""
        try:
            current_price = data['Close'].iloc[-1]
            prev_close = data['Close'].iloc[-2] if len(data) > 1 else current_price
            change = current_price - prev_close
            change_percent = (change / prev_close) * 100
            
            self.info_labels['symbol'].config(text=self.current_stock)
            self.info_labels['price'].config(text=f"${current_price:.2f}")
            
            change_text = f"${change:.2f} ({change_percent:+.2f}%)"
            change_color = "#00ff88" if change >= 0 else "#ff5555"
            self.info_labels['change'].config(text=change_text, fg=change_color)
            
            volume = info.get('volume', data['Volume'].iloc[-1])
            self.info_labels['volume'].config(text=f"{volume:,}")
            
            market_cap = info.get('marketCap', 'N/A')
            if isinstance(market_cap, (int, float)):
                if market_cap >= 1e12:
                    market_cap_text = f"${market_cap/1e12:.2f}T"
                elif market_cap >= 1e9:
                    market_cap_text = f"${market_cap/1e9:.2f}B"
                elif market_cap >= 1e6:
                    market_cap_text = f"${market_cap/1e6:.2f}M"
                else:
                    market_cap_text = f"${market_cap:,.0f}"
            else:
                market_cap_text = "N/A"
            self.info_labels['market_cap'].config(text=market_cap_text)
            
            pe_ratio = info.get('trailingPE', 'N/A')
            pe_text = f"{pe_ratio:.2f}" if isinstance(pe_ratio, (int, float)) else "N/A"
            self.info_labels['pe_ratio'].config(text=pe_text)
            
        except Exception as e:
            print(f"Error updating info: {e}")
            
    def plot_chart(self, data, symbol):
        """Plot stock price chart with technical indicators"""
        self.ax.clear()
        
        # Calculate moving averages
        data['SMA20'] = data['Close'].rolling(window=20).mean()
        data['SMA50'] = data['Close'].rolling(window=50).mean()
        
        # Plot price and moving averages
        self.ax.plot(data.index, data['Close'], label='Price', color='#00d4ff', linewidth=2)
        self.ax.plot(data.index, data['SMA20'], label='SMA 20', color='#00ff88', linewidth=1.5, alpha=0.7)
        self.ax.plot(data.index, data['SMA50'], label='SMA 50', color='#ffa500', linewidth=1.5, alpha=0.7)
        
        # Style
        self.ax.set_title(f"{symbol} - 6 Month Price Chart", color="#ffffff", fontsize=14, pad=15)
        self.ax.set_xlabel("Date", color="#8892b0", fontsize=10)
        self.ax.set_ylabel("Price ($)", color="#8892b0", fontsize=10)
        self.ax.legend(loc='upper left', framealpha=0.9, facecolor="#1a1f3a", edgecolor="#8892b0", labelcolor="#ffffff")
        self.ax.grid(True, alpha=0.2, color="#8892b0", linestyle="--")
        self.ax.tick_params(colors="#8892b0", labelsize=9)
        
        # Rotate date labels
        self.fig.autofmt_xdate()
        
        self.canvas.draw()
        
    def perform_technical_analysis(self, data, info):
        """Perform AI-powered technical analysis"""
        analysis = []
        
        # Calculate technical indicators
        current_price = data['Close'].iloc[-1]
        sma20 = data['Close'].rolling(window=20).mean().iloc[-1]
        sma50 = data['Close'].rolling(window=50).mean().iloc[-1]
        
        # RSI calculation
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        current_rsi = rsi.iloc[-1]
        
        # Add header
        analysis.append(f"🤖 AI TECHNICAL ANALYSIS - {self.current_stock}\n")
        analysis.append("=" * 60 + "\n\n")
        
        # Price trend analysis
        analysis.append("📊 TREND ANALYSIS:\n")
        if current_price > sma20 > sma50:
            analysis.append("✅ Strong Uptrend - Price above both moving averages\n")
        elif current_price > sma20:
            analysis.append("⚠️ Bullish - Price above 20-day MA\n")
        elif current_price < sma20 < sma50:
            analysis.append("❌ Downtrend - Price below both moving averages\n")
        else:
            analysis.append("⚠️ Bearish - Price below 20-day MA\n")
        
        analysis.append(f"   Current: ${current_price:.2f}\n")
        analysis.append(f"   SMA 20: ${sma20:.2f}\n")
        analysis.append(f"   SMA 50: ${sma50:.2f}\n\n")
        
        # RSI analysis
        analysis.append("📈 RSI INDICATOR:\n")
        analysis.append(f"   RSI (14): {current_rsi:.2f}\n")
        if current_rsi > 70:
            analysis.append("   ⚠️ OVERBOUGHT - Potential sell signal\n")
        elif current_rsi < 30:
            analysis.append("   ✅ OVERSOLD - Potential buy signal\n")
        else:
            analysis.append("   ➡️ NEUTRAL - No extreme signal\n")
        analysis.append("\n")
        
        # Volatility analysis
        volatility = data['Close'].pct_change().std() * np.sqrt(252) * 100
        analysis.append("💹 VOLATILITY:\n")
        analysis.append(f"   Annualized: {volatility:.2f}%\n")
        if volatility > 40:
            analysis.append("   ⚠️ HIGH - Higher risk/reward\n")
        elif volatility < 20:
            analysis.append("   ✅ LOW - More stable\n")
        else:
            analysis.append("   ➡️ MODERATE\n")
        analysis.append("\n")
        
        # AI Recommendation
        analysis.append("🎯 AI RECOMMENDATION:\n")
        score = 0
        if current_price > sma20:
            score += 1
        if current_price > sma50:
            score += 1
        if 30 < current_rsi < 70:
            score += 1
        if volatility < 30:
            score += 1
            
        if score >= 3:
            analysis.append("   💚 BULLISH - Strong buy signals\n")
        elif score == 2:
            analysis.append("   💛 NEUTRAL - Hold or wait for confirmation\n")
        else:
            analysis.append("   ❤️ BEARISH - Caution advised\n")
            
        # Update analysis text
        self.analysis_text.config(state=tk.NORMAL)
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(1.0, "".join(analysis))
        self.analysis_text.config(state=tk.DISABLED)
        
    def add_to_watchlist(self):
        """Add current stock to watchlist"""
        if self.current_stock and self.current_stock not in self.watchlist:
            self.watchlist.append(self.current_stock)
            self.watchlist_box.insert(tk.END, self.current_stock)
            self.update_status(f"Added {self.current_stock} to watchlist")
        elif self.current_stock in self.watchlist:
            messagebox.showinfo("Info", f"{self.current_stock} is already in watchlist")
            
    def remove_from_watchlist(self):
        """Remove selected stock from watchlist"""
        selection = self.watchlist_box.curselection()
        if selection:
            index = selection[0]
            symbol = self.watchlist_box.get(index)
            self.watchlist_box.delete(index)
            self.watchlist.remove(symbol)
            self.update_status(f"Removed {symbol} from watchlist")
            
    def update_status(self, message):
        """Update status bar message"""
        self.status_bar.config(text=message)

def main():
    root = tk.Tk()
    app = AIStockAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
