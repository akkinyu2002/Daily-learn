"""
Image to Icon Converter
Converts JPG, PNG, and other image formats to .ico files
Supports batch conversion and multiple icon sizes
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import threading


class ImageToIconConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to Icon Converter")
        self.root.geometry("700x550")
        self.root.configure(bg="#1e1e2e")
        
        self.selected_files = []
        self.output_folder = ""
        
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.root,
            text="🎨 Image to Icon Converter",
            font=("Segoe UI", 20, "bold"),
            bg="#1e1e2e",
            fg="#cdd6f4"
        )
        title_label.pack(pady=20)
        
        # File selection frame
        file_frame = tk.Frame(self.root, bg="#1e1e2e")
        file_frame.pack(pady=10, padx=20, fill="x")
        
        select_btn = tk.Button(
            file_frame,
            text="📁 Select Images",
            command=self.select_images,
            font=("Segoe UI", 11),
            bg="#89b4fa",
            fg="#1e1e2e",
            activebackground="#74c7ec",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        select_btn.pack(side="left", padx=5)
        
        self.file_count_label = tk.Label(
            file_frame,
            text="No files selected",
            font=("Segoe UI", 10),
            bg="#1e1e2e",
            fg="#a6adc8"
        )
        self.file_count_label.pack(side="left", padx=10)
        
        # File list
        list_frame = tk.Frame(self.root, bg="#1e1e2e")
        list_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.file_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=("Consolas", 9),
            bg="#313244",
            fg="#cdd6f4",
            selectbackground="#89b4fa",
            relief="flat",
            borderwidth=0,
            highlightthickness=0
        )
        self.file_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.file_listbox.yview)
        
        # Icon size selection
        size_frame = tk.Frame(self.root, bg="#1e1e2e")
        size_frame.pack(pady=10, padx=20, fill="x")
        
        size_label = tk.Label(
            size_frame,
            text="Icon Sizes:",
            font=("Segoe UI", 11),
            bg="#1e1e2e",
            fg="#cdd6f4"
        )
        size_label.pack(side="left", padx=5)
        
        self.size_var = tk.StringVar(value="Multi-size (16,32,48,64,128,256)")
        sizes = [
            "Multi-size (16,32,48,64,128,256)",
            "16x16",
            "32x32",
            "48x48",
            "64x64",
            "128x128",
            "256x256"
        ]
        
        size_menu = ttk.Combobox(
            size_frame,
            textvariable=self.size_var,
            values=sizes,
            state="readonly",
            font=("Segoe UI", 10),
            width=30
        )
        size_menu.pack(side="left", padx=5)
        
        # Output folder selection
        output_frame = tk.Frame(self.root, bg="#1e1e2e")
        output_frame.pack(pady=10, padx=20, fill="x")
        
        output_btn = tk.Button(
            output_frame,
            text="📂 Output Folder",
            command=self.select_output_folder,
            font=("Segoe UI", 11),
            bg="#94e2d5",
            fg="#1e1e2e",
            activebackground="#89dceb",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        output_btn.pack(side="left", padx=5)
        
        self.output_label = tk.Label(
            output_frame,
            text="Same as source",
            font=("Segoe UI", 10),
            bg="#1e1e2e",
            fg="#a6adc8"
        )
        self.output_label.pack(side="left", padx=10)
        
        # Convert button
        convert_btn = tk.Button(
            self.root,
            text="✨ Convert to Icons",
            command=self.convert_images,
            font=("Segoe UI", 13, "bold"),
            bg="#a6e3a1",
            fg="#1e1e2e",
            activebackground="#94e2d5",
            relief="flat",
            padx=30,
            pady=15,
            cursor="hand2"
        )
        convert_btn.pack(pady=15)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self.root,
            orient="horizontal",
            length=660,
            mode="determinate"
        )
        self.progress.pack(pady=10, padx=20)
        
        # Status label
        self.status_label = tk.Label(
            self.root,
            text="Ready to convert images",
            font=("Segoe UI", 10),
            bg="#1e1e2e",
            fg="#f9e2af"
        )
        self.status_label.pack(pady=5)
    
    def select_images(self):
        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[
                ("All Images", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.webp"),
                ("JPEG", "*.jpg *.jpeg"),
                ("PNG", "*.png"),
                ("BMP", "*.bmp"),
                ("GIF", "*.gif"),
                ("TIFF", "*.tiff"),
                ("WebP", "*.webp"),
                ("All Files", "*.*")
            ]
        )
        
        if files:
            self.selected_files = list(files)
            self.file_listbox.delete(0, tk.END)
            for file in self.selected_files:
                self.file_listbox.insert(tk.END, os.path.basename(file))
            
            self.file_count_label.config(
                text=f"{len(self.selected_files)} file(s) selected",
                fg="#a6e3a1"
            )
    
    def select_output_folder(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder = folder
            self.output_label.config(text=folder, fg="#a6e3a1")
    
    def get_icon_sizes(self):
        size_option = self.size_var.get()
        if "Multi-size" in size_option:
            return [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        else:
            size = int(size_option.split('x')[0])
            return [(size, size)]
    
    def convert_single_image(self, image_path, output_path, sizes):
        try:
            img = Image.open(image_path)
            
            # Convert RGBA if needed
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Save as ICO with specified sizes
            img.save(output_path, format='ICO', sizes=sizes)
            return True, None
        except Exception as e:
            return False, str(e)
    
    def convert_images(self):
        if not self.selected_files:
            messagebox.showwarning("No Files", "Please select images to convert!")
            return
        
        # Run conversion in a separate thread to avoid blocking UI
        thread = threading.Thread(target=self._convert_thread)
        thread.daemon = True
        thread.start()
    
    def _convert_thread(self):
        sizes = self.get_icon_sizes()
        total_files = len(self.selected_files)
        success_count = 0
        error_count = 0
        
        self.progress['maximum'] = total_files
        self.progress['value'] = 0
        
        for idx, image_path in enumerate(self.selected_files):
            # Update status
            filename = os.path.basename(image_path)
            self.status_label.config(text=f"Converting: {filename}")
            
            # Determine output path
            if self.output_folder:
                output_dir = self.output_folder
            else:
                output_dir = os.path.dirname(image_path)
            
            # Create output filename
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            output_path = os.path.join(output_dir, f"{base_name}.ico")
            
            # Convert
            success, error = self.convert_single_image(image_path, output_path, sizes)
            
            if success:
                success_count += 1
            else:
                error_count += 1
                print(f"Error converting {filename}: {error}")
            
            # Update progress
            self.progress['value'] = idx + 1
            self.root.update_idletasks()
        
        # Show completion message
        if error_count == 0:
            self.status_label.config(
                text=f"✅ Successfully converted {success_count} image(s)!",
                fg="#a6e3a1"
            )
            messagebox.showinfo(
                "Success",
                f"Successfully converted {success_count} image(s) to icons!"
            )
        else:
            self.status_label.config(
                text=f"⚠️ Converted {success_count}, {error_count} failed",
                fg="#f9e2af"
            )
            messagebox.showwarning(
                "Partial Success",
                f"Converted {success_count} image(s).\n{error_count} file(s) failed."
            )


def main():
    root = tk.Tk()
    app = ImageToIconConverter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
