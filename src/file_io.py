# src/file_io.py

def read_file(file_path):
    """Reads a file and returns its content, handling common errors gracefully."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f_in:
            content = f_in.read()
            if not content.endswith('\n') and content:
                content += '\n'
            return content if content else "[Empty file]\n"
    except FileNotFoundError:
        return f"[ERROR: The file {file_path} is missing]\n"
    except UnicodeDecodeError:
        return "[ERROR: Binary file or unsupported encoding ignored]\n"
    except Exception as e:
        return f"[ERROR during reading: {e}]\n"
