# read_files.py
import argparse
from datetime import datetime

def compile_files(input_file):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"out_read_{timestamp}.txt"

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            file_paths = f.readlines()
    except FileNotFoundError:
        print(f"Error: The input list file '{input_file}' does not exist.")
        return

    with open(output_file, 'w', encoding='utf-8') as f_out:
        f_out.write("<selected_files>\n\n")

        for file_path in file_paths:
            file_path = file_path.strip()

            if not file_path:
                continue

            f_out.write(f'<file path="{file_path}">\n')
            try:
                with open(file_path, 'r', encoding='utf-8') as f_in:
                    content = f_in.read()
                    # Ensure the file ends with a newline
                    if not content.endswith('\n') and content:
                        content += '\n'
                    f_out.write(content if content else "[Empty file]\n")
            except FileNotFoundError:
                f_out.write(f"[ERROR: The file {file_path} is missing]\n")
            except UnicodeDecodeError:
                f_out.write("[ERROR: Binary file or unsupported encoding ignored]\n")
            except Exception as e:
                f_out.write(f"[ERROR during reading: {e}]\n")
            f_out.write("</file>\n\n")

        f_out.write("</selected_files>\n")

    print(f"✅ Done! The selected files have been compiled into: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compile selected files into an AI-readable XML format.")
    parser.add_argument(
        "input_file", 
        nargs="?", 
        default="list.txt", 
        help="Text file containing the list of paths to read (default: list.txt)"
    )

    args = parser.parse_args()
    compile_files(args.input_file)
