# src/gitignore.py
import os

def parse_patterns(base_dir):
    """Reads .gitignore and returns a list of patterns to ignore."""
    patterns = ['.git']
    gitignore_path = os.path.join(base_dir, '.gitignore')

    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    patterns.append(line)
    return patterns
