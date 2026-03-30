# read_files.py
import os
import argparse
from datetime import datetime
from src import gitignore, exclusions, file_io

def process_files(input_file, use_gitignore):
    """Core logic to read a specific list of files and output them in XML format."""
    base_dir = os.getcwd()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"out_read_{timestamp}.txt"

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            file_paths = f.readlines()
    except FileNotFoundError:
        print(f"Error: The input list file '{input_file}' does not exist.")
        return

    ignore_patterns = gitignore.parse_patterns(base_dir) if use_gitignore else []

    with open(output_file, 'w', encoding='utf-8') as f_out:
        f_out.write("<selected_files>\n\n")

        for file_path in file_paths:
            file_path = file_path.strip()

            if not file_path:
                continue

            f_out.write(f'<file path="{file_path}">\n')

            if use_gitignore and exclusions.is_ignored(file_path, base_dir, [], ignore_patterns, output_file):
                f_out.write("[ERROR: This file is excluded by .gitignore rules]\n</file>\n\n")
                continue

            content = file_io.read_file(file_path)
            f_out.write(content)

            f_out.write("</file>\n\n")

        f_out.write("</selected_files>\n")

    print(f"✅ Done! The selected files have been compiled into: {output_file}")


def main():
    """CLI entry point for argument parsing."""
    parser = argparse.ArgumentParser(description="Compile selected files into an AI-readable XML format.")
    parser.add_argument(
        "input_file", 
        nargs="?", 
        default="list.txt", 
        help="Text file containing the list of paths to read (default: list.txt)"
    )
    parser.add_argument(
        "--exclude-gitignore", 
        action="store_true", 
        help="Ignore files that match patterns in the local .gitignore file"
    )
    args = parser.parse_args()

    process_files(args.input_file, args.exclude_gitignore)

if __name__ == "__main__":
    main()
