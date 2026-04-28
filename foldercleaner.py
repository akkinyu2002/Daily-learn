import os
import shutil
from pathlib import Path

def clean_folder(folder_path):
    """
    Scans the given folder and sorts files into subfolders based on their extensions.
    """
    # Mapping of extensions to their respective categories
    CATEGORIES = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
        'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.xls', '.pptx', '.ppt', '.csv', '.md'],
        'Videos': ['.mp4', '.mkv', '.flv', '.mpeg', '.mov', '.avi'],
        'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
        'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
        'Executables': ['.exe', '.msi', '.bat', '.sh'],
        'Others': [] # Fallback for unknown types
    }

    path = Path(folder_path)
    if not path.exists():
        print(f"Error: The folder {folder_path} does not exist.")
        return

    print(f"Scanning folder: {path}")
    
    files_moved = 0
    
    for item in path.iterdir():
        # Skip directories
        if item.is_dir():
            continue
            
        # Skip the script itself if it's in the same folder
        if item.name == "foldercleaner.py":
            continue

        file_extension = item.suffix.lower()
        category_found = "Others"
        
        for category, extensions in CATEGORIES.items():
            if file_extension in extensions:
                category_found = category
                break
        
        # Create category folder if it doesn't exist
        dest_folder = path / category_found
        dest_folder.mkdir(exist_ok=True)
        
        # Define destination path
        dest_path = dest_folder / item.name
        
        # Handle filename collisions
        if dest_path.exists():
            count = 1
            while True:
                new_name = f"{item.stem}_{count}{item.suffix}"
                dest_path = dest_folder / new_name
                if not dest_path.exists():
                    break
                count += 1
        
        try:
            shutil.move(str(item), str(dest_path))
            print(f"Moved: {item.name} -> {category_found}/")
            files_moved += 1
        except Exception as e:
            print(f"Failed to move {item.name}: {e}")

    print(f"\nCleanup complete. Total files moved: {files_moved}")

if __name__ == "__main__":
    # Get the default Downloads folder for the current user as a suggestion
    default_path = str(Path.home() / "Downloads")
    
    print("--- Folder Cleaner ---")
    user_path = input(f"Enter the folder path to clean (Press Enter for default '{default_path}'): ").strip()
    
    target_folder = user_path if user_path else default_path
    
    # Expand ~ if used in path
    target_folder = os.path.expanduser(target_folder)
    
    confirm = input(f"This will organize the files in '{target_folder}'. Proceed? (y/n): ")
    if confirm.lower() == 'y':
        clean_folder(target_folder)
    else:
        print("Operation cancelled.")
