# read_folder.py
import os
import argparse
from datetime import datetime
from src import gitignore, exclusions, file_io, scanner

def process_folder(root_alias, raw_excludes, use_gitignore):
    """Core logic to scan the directory and output the tree and contents in XML format."""
    base_dir = os.getcwd()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_filename = f"out_{timestamp}.txt"
    out_filepath = os.path.join(base_dir, out_filename)

    # process exclusions
    manual_excludes = exclusions.sanitize_paths(raw_excludes)
    gitignore_patterns = gitignore.parse_patterns(base_dir) if use_gitignore else []

    if manual_excludes:
        print(f"-> Active manual exclusions: {', '.join(manual_excludes)}")
    if use_gitignore:
        print("-> Using .gitignore rules for exclusions")

    with open(out_filepath, 'w', encoding='utf-8') as f_out:
        f_out.write("<project_context>\n\n")

        # project tree
        f_out.write("<project_tree>\n")
        f_out.write(f"{root_alias}\n")

        tree_structure = scanner.build_ascii_tree(base_dir, base_dir, "", manual_excludes, gitignore_patterns, out_filename)
        f_out.write(tree_structure)

        f_out.write("</project_tree>\n\n")

        # file contents
        f_out.write("<file_contents>\n")
        all_files = scanner.fetch_all_files(base_dir, base_dir, manual_excludes, gitignore_patterns, out_filename)

        for file_path in all_files:
            rel_path = os.path.relpath(file_path, base_dir).replace(os.sep, '/')
            f_out.write(f'<file path="{rel_path}">\n')

            content = file_io.read_file(file_path)
            f_out.write(content)

            f_out.write("</file>\n\n")

        f_out.write("</file_contents>\n\n")
        f_out.write("</project_context>\n")

    print(f"\n✅ Done! The scan has been saved in: {out_filename}")

def main():
    """CLI entry point for argument parsing."""
    parser = argparse.ArgumentParser(description="Export the project tree and file contents into an AI-readable XML format.")
    parser.add_argument(
        "root_alias", 
        nargs="?", 
        default=".", 
        help="Alias for the root directory"
    )
    parser.add_argument(
        "--exclude", 
        action="append", 
        default=[], 
        help="Folders/files to exclude manually"
    )
    parser.add_argument(
        "--exclude-gitignore", 
        action="store_true", 
        help="Ignore files matching patterns in .gitignore"
    )
    args = parser.parse_args()

    process_folder(args.root_alias, args.exclude, args.exclude_gitignore)

if __name__ == "__main__":
    main()
