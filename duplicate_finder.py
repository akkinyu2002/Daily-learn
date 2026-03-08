"""
Duplicate File Detector
=======================
Detects duplicate files by comparing their content using SHA-256 hashing.
Works with ALL file types: documents, images, videos, audio, PDFs, etc.
Keeps the file with the highest size and asks permission to delete duplicates.

Usage:
    python duplicate_finder.py
"""

import os
import sys
import hashlib
import time
from collections import defaultdict


# ─────────────────────────────────────────────
#  Constants
# ─────────────────────────────────────────────
CHUNK_SIZE = 8192  # Read files in 8 KB chunks for memory efficiency
SUPPORTED_EXTENSIONS = None  # None = all file types supported


# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────
def format_size(size_bytes):
    """Convert bytes to a human-readable string."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"


def get_file_hash(filepath):
    """
    Compute the SHA-256 hash of a file's content.
    Reads in chunks to handle very large files without running out of memory.
    """
    sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break
                sha256.update(chunk)
        return sha256.hexdigest()
    except (PermissionError, OSError) as e:
        print(f"  ⚠  Could not read: {filepath} ({e})")
        return None


def collect_files(directory):
    """Recursively collect all files in a directory."""
    files = []
    for root, _, filenames in os.walk(directory):
        for name in filenames:
            full_path = os.path.join(root, name)
            try:
                size = os.path.getsize(full_path)
                files.append((full_path, size))
            except OSError:
                pass
    return files


def group_by_size(files):
    """
    First-pass optimization: group files by size.
    Files with unique sizes cannot be duplicates, so we skip them.
    """
    size_map = defaultdict(list)
    for path, size in files:
        size_map[size].append(path)
    # Only return groups with more than one file (potential duplicates)
    return {size: paths for size, paths in size_map.items() if len(paths) > 1}


def find_duplicates(directory):
    """
    Scan a directory and find duplicate files based on content hash.
    Returns a dict: { hash: [list of file paths] }
    """
    print(f"\n{'═' * 60}")
    print(f"  📂  Scanning: {directory}")
    print(f"{'═' * 60}\n")

    # Step 1: Collect all files
    print("  [1/3] Collecting files...")
    all_files = collect_files(directory)
    print(f"         Found {len(all_files)} files.\n")

    if not all_files:
        print("  ❌  No files found in the specified directory.")
        return {}

    # Step 2: Group by size (quick filter)
    print("  [2/3] Grouping by file size (quick filter)...")
    size_groups = group_by_size(all_files)
    candidates = sum(len(paths) for paths in size_groups.values())
    print(f"         {candidates} files are potential duplicates (same size).\n")

    # Step 3: Hash the candidate files
    print("  [3/3] Computing content hashes...")
    hash_map = defaultdict(list)
    hashed_count = 0

    for size, paths in size_groups.items():
        for path in paths:
            file_hash = get_file_hash(path)
            if file_hash:
                hash_map[file_hash].append(path)
            hashed_count += 1
            # Progress indicator
            if hashed_count % 50 == 0 or hashed_count == candidates:
                print(f"         Hashed {hashed_count}/{candidates} files...", end="\r")

    print(f"         Hashed {hashed_count}/{candidates} files. ✔\n")

    # Filter to only actual duplicates (hash appears more than once)
    duplicates = {h: paths for h, paths in hash_map.items() if len(paths) > 1}
    return duplicates


def display_and_handle_duplicates(duplicates):
    """
    Display duplicate groups and let the user decide what to delete.
    Keeps the file with the largest size in each group.
    """
    if not duplicates:
        print("  ✅  No duplicate files found! Your directory is clean.\n")
        return

    total_groups = len(duplicates)
    total_dupes = sum(len(paths) - 1 for paths in duplicates.values())
    total_recoverable = 0

    print(f"{'═' * 60}")
    print(f"  🔍  Found {total_groups} group(s) of duplicates ({total_dupes} extra files)")
    print(f"{'═' * 60}\n")

    deleted_count = 0
    skipped_count = 0
    freed_space = 0

    for group_num, (file_hash, paths) in enumerate(duplicates.items(), 1):
        # Get sizes for each file in the group
        file_info = []
        for p in paths:
            try:
                size = os.path.getsize(p)
                file_info.append((p, size))
            except OSError:
                file_info.append((p, 0))

        # Sort by size descending — keep the largest
        file_info.sort(key=lambda x: x[1], reverse=True)

        keeper = file_info[0]
        to_delete = file_info[1:]

        recoverable = sum(size for _, size in to_delete)
        total_recoverable += recoverable

        # Display group info
        print(f"  ┌── Group {group_num}/{total_groups} ──────────────────────────")
        print(f"  │  Hash: {file_hash[:16]}...")
        print(f"  │  Files: {len(file_info)} duplicates found")
        print(f"  │  Recoverable space: {format_size(recoverable)}")
        print(f"  │")
        print(f"  │  ✅ KEEP: {keeper[0]}")
        print(f"  │          Size: {format_size(keeper[1])}")

        for i, (path, size) in enumerate(to_delete):
            print(f"  │")
            print(f"  │  🗑️  DELETE candidate {i + 1}: {path}")
            print(f"  │          Size: {format_size(size)}")

        print(f"  └{'─' * 50}\n")

        # Ask user for permission — one file at a time
        for i, (path, size) in enumerate(to_delete):
            print(f"  ❓ Delete this duplicate?")
            print(f"     File : {path}")
            print(f"     Size : {format_size(size)}")

            while True:
                choice = input("     ➤  (y = yes / n = skip / q = quit): ").strip().lower()

                if choice == "y":
                    try:
                        os.remove(path)
                        print(f"     🗑️  Deleted!\n")
                        deleted_count += 1
                        freed_space += size
                    except OSError as e:
                        print(f"     ⚠  Failed to delete: {e}\n")
                    break

                elif choice == "n":
                    print(f"     ⏭️  Skipped.\n")
                    skipped_count += 1
                    break

                elif choice == "q":
                    print("\n  🛑  Quitting. No more files will be deleted.\n")
                    print_summary(deleted_count, skipped_count, freed_space)
                    return

                else:
                    print("     Invalid choice. Please enter y, n, or q.")

    print_summary(deleted_count, skipped_count, freed_space)


def print_summary(deleted, skipped, freed):
    """Print a final summary of actions taken."""
    print(f"{'═' * 60}")
    print(f"  📊  Summary")
    print(f"{'═' * 60}")
    print(f"  │  Files deleted : {deleted}")
    print(f"  │  Files skipped : {skipped}")
    print(f"  │  Space freed   : {format_size(freed)}")
    print(f"{'═' * 60}\n")


# ─────────────────────────────────────────────
#  Main
# ─────────────────────────────────────────────
def main():
    print()
    print("╔════════════════════════════════════════════════════════╗")
    print("║          🔎  DUPLICATE FILE DETECTOR  🔍              ║")
    print("║   Finds duplicate files by content comparison         ║")
    print("║   Supports: docs, images, videos, audio, PDFs, etc.  ║")
    print("╚════════════════════════════════════════════════════════╝")
    print()

    # Get directory from user
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = input("  📁 Enter the directory path to scan: ").strip()
        # Remove surrounding quotes if present
        directory = directory.strip('"').strip("'")

    # Validate directory
    if not os.path.isdir(directory):
        print(f"\n  ❌  Error: '{directory}' is not a valid directory.\n")
        sys.exit(1)

    # Confirm scan
    print(f"\n  📌 Target: {os.path.abspath(directory)}")
    confirm = input("  ❓ Proceed with scan? (y/n): ").strip().lower()
    if confirm != "y":
        print("  🛑  Scan cancelled.\n")
        sys.exit(0)

    # Run the duplicate finder
    start_time = time.time()
    duplicates = find_duplicates(directory)
    elapsed = time.time() - start_time
    print(f"  ⏱️  Scan completed in {elapsed:.2f} seconds.\n")

    # Handle results
    display_and_handle_duplicates(duplicates)

    print("  👋  Done! Goodbye.\n")


if __name__ == "__main__":
    main()
