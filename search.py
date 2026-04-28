import os
import time
import string
import subprocess
import concurrent.futures
from ctypes import windll

class FastSearcher:
    def __init__(self, max_workers=10):
        self.max_workers = max_workers
        self.results = []
        self.scanned_count = 0

    def get_drives(self):
        """Returns a list of all active drive letters on Windows."""
        drives = []
        bitmask = windll.kernel32.GetLogicalDrives()
        for letter in string.ascii_uppercase:
            if bitmask & 1:
                drives.append(f"{letter}:\\")
            bitmask >>= 1
        return drives

    def scan_dir(self, path, target_name):
        """Recursively scan a directory for the target filename using os.scandir."""
        matches = []
        try:
            with os.scandir(path) as it:
                for entry in it:
                    self.scanned_count += 1
                    try:
                        if target_name.lower() in entry.name.lower():
                            matches.append(entry.path)
                        
                        if entry.is_dir(follow_symlinks=False):
                            matches.extend(self.scan_dir(entry.path, target_name))
                    except (PermissionError, OSError):
                        continue
        except (PermissionError, OSError):
            pass
        return matches

    def open_location(self, path):
        """Opens the file location in Windows Explorer and selects the file."""
        if os.path.exists(path):
            subprocess.run(['explorer', '/select,', os.path.normpath(path)])
        else:
            print(f"Error: Path does not exist: {path}")

    def search(self, target_name):
        """Starts a multi-threaded search across all detected drives."""
        drives = self.get_drives()
        print(f"Detecting drives: {', '.join(drives)}")
        print(f"Searching for: '{target_name}'...")
        
        start_time = time.time()
        self.results = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Map search across drives
            future_to_drive = {executor.submit(self.scan_dir, drive, target_name): drive for drive in drives}
            
            for future in concurrent.futures.as_completed(future_to_drive):
                drive = future_to_drive[future]
                try:
                    data = future.result()
                    self.results.extend(data)
                except Exception as exc:
                    print(f"Drive {drive} generated an exception: {exc}")

        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\nSearch complete in {duration:.2f} seconds.")
        print(f"Total items scanned: {self.scanned_count}")
        print(f"Found {len(self.results)} matches:")
        
        for idx, match in enumerate(self.results, 1):
            # Print as clickable file link for modern terminals + index for manual entry
            link_path = match.replace('\\', '/')
            link = f"file:///{link_path}"
            print(f"[{idx}] {match}")
            print(f"    Link: {link}")
        
        if self.results:
            self.interactive_loop()
        
        return self.results

    def interactive_loop(self):
        """Prompt the user to open a file from the results."""
        while True:
            try:
                choice = input("\nEnter result number to open location (or 'q' to quit): ").strip().lower()
                if choice == 'q':
                    break
                
                idx = int(choice)
                if 1 <= idx <= len(self.results):
                    path = self.results[idx-1]
                    print(f"Opening: {path}")
                    self.open_location(path)
                else:
                    print(f"Invalid index. Please enter a number between 1 and {len(self.results)}.")
            except ValueError:
                print("Please enter a valid number or 'q'.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python search.py <filename_to_find>")
        target = input("Enter filename to search for: ")
    else:
        target = sys.argv[1]
    
    if target.strip():
        searcher = FastSearcher()
        searcher.search(target)
    else:
        print("No target specified.")
