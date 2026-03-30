# src/scanner.py
import os
from src import exclusions

def build_ascii_tree(dir_path, base_dir, prefix, manual_excludes, gitignore_patterns, out_filename):
    """Generates an ASCII representation of the directory tree."""
    tree_str = ""
    try:
        items = sorted(os.listdir(dir_path))
    except PermissionError:
        return tree_str + prefix + "[Access denied]\n"

    valid_items = []
    for item in items:
        item_path = os.path.join(dir_path, item)

        if not exclusions.is_ignored(item_path, base_dir, manual_excludes, gitignore_patterns, out_filename):
            valid_items.append(item)

    for i, item in enumerate(valid_items):
        is_last = (i == len(valid_items) - 1)
        item_path = os.path.join(dir_path, item)

        connector = "└── " if is_last else "├── "
        tree_str += f"{prefix}{connector}{item}\n"

        if os.path.isdir(item_path):
            extension = "    " if is_last else "│   "
            tree_str += build_ascii_tree(item_path, base_dir, prefix + extension, manual_excludes, gitignore_patterns, out_filename)

    return tree_str

def fetch_all_files(dir_path, base_dir, manual_excludes, gitignore_patterns, out_filename):
    """Recursively fetches all valid files in the directory."""
    files = []
    try:
        items = sorted(os.listdir(dir_path))
    except PermissionError:
        return files

    for item in items:
        item_path = os.path.join(dir_path, item)

        if exclusions.is_ignored(item_path, base_dir, manual_excludes, gitignore_patterns, out_filename):
            continue

        if os.path.isdir(item_path):
            files.extend(fetch_all_files(item_path, base_dir, manual_excludes, gitignore_patterns, out_filename))
        else:
            files.append(item_path)
    return files
