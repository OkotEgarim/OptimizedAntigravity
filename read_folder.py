# read_folder.py
import os
import argparse
from datetime import datetime

def sanitize_excludes(excludes):
    cleaned = []
    for ex in excludes:
        ex_clean = ex.replace('\\', '/')
        if ex_clean.startswith('./'):
            ex_clean = ex_clean[2:]
        ex_clean = ex_clean.rstrip('/')
        if ex_clean:
            cleaned.append(ex_clean)
    return cleaned

def should_exclude(item_path, base_dir, excludes, out_filename):
    rel_path = os.path.relpath(item_path, base_dir).replace(os.sep, '/')
    item_name = os.path.basename(item_path)

    if item_name == out_filename or item_name == os.path.basename(__file__):
        return True
    if item_name.endswith(('.spec', '.spec.ts', '.spec.js')):
        return True

    for ex in excludes:
        if item_name == ex or rel_path == ex or rel_path.startswith(ex + '/'):
            return True
    return False

def generate_tree(dir_path, base_dir, prefix, excludes, out_filename):
    tree_str = ""
    try:
        items = sorted(os.listdir(dir_path))
    except PermissionError:
        return tree_str + prefix + "[Access denied]\n"

    valid_items = []
    for item in items:
        item_path = os.path.join(dir_path, item)
        if not should_exclude(item_path, base_dir, excludes, out_filename):
            valid_items.append(item)

    for i, item in enumerate(valid_items):
        is_last = (i == len(valid_items) - 1)
        item_path = os.path.join(dir_path, item)

        connector = "└── " if is_last else "├── "
        tree_str += f"{prefix}{connector}{item}\n"

        if os.path.isdir(item_path):
            extension = "    " if is_last else "│   "
            tree_str += generate_tree(item_path, base_dir, prefix + extension, excludes, out_filename)

    return tree_str

def get_all_files(dir_path, base_dir, excludes, out_filename):
    files = []
    try:
        items = sorted(os.listdir(dir_path))
    except PermissionError:
        return files

    for item in items:
        item_path = os.path.join(dir_path, item)
        if should_exclude(item_path, base_dir, excludes, out_filename):
            continue
        if os.path.isdir(item_path):
            files.extend(get_all_files(item_path, base_dir, excludes, out_filename))
        else:
            files.append(item_path)
    return files

def main():
    base_dir = os.getcwd()

    parser = argparse.ArgumentParser(description="Export the project tree and file contents into an AI-readable XML format.")
    parser.add_argument("root_alias", nargs="?", default=".", help="Alias for the root directory")
    parser.add_argument("--exclude", action="append", default=[], help="Folders/files to exclude")
    args = parser.parse_args()

    root_alias = args.root_alias
    excludes = sanitize_excludes(args.exclude)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_filename = f"out_{timestamp}.txt"
    out_filepath = os.path.join(base_dir, out_filename)

    if excludes:
        print(f"-> Active exclusions: {', '.join(excludes)}")

    with open(out_filepath, 'w', encoding='utf-8') as f_out:
        f_out.write("<project_context>\n\n")

        # project tree
        f_out.write("<project_tree>\n")
        f_out.write(f"{root_alias}\n")
        f_out.write(generate_tree(base_dir, base_dir, "", excludes, out_filename))
        f_out.write("</project_tree>\n\n")

        # file contents
        f_out.write("<file_contents>\n")
        all_files = get_all_files(base_dir, base_dir, excludes, out_filename)

        for file_path in all_files:
            rel_path = os.path.relpath(file_path, base_dir).replace(os.sep, '/')
            f_out.write(f'<file path="{rel_path}">\n')
            try:
                with open(file_path, 'r', encoding='utf-8') as f_in:
                    content = f_in.read()
                    if not content.endswith('\n') and content:
                        content += '\n'
                    f_out.write(content if content else "[Empty file]\n")
            except UnicodeDecodeError:
                f_out.write("[Binary file or unsupported encoding ignored]\n")
            except Exception as e:
                f_out.write(f"[Read error: {e}]\n")
            f_out.write("</file>\n\n")

        f_out.write("</file_contents>\n\n")
        f_out.write("</project_context>\n")

    print(f"\n✅ Done! The scan has been saved in: {out_filename}")

if __name__ == "__main__":
    main()
