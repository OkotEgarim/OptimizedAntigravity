# src/exclusions.py
import os
import fnmatch

def sanitize_paths(excludes):
    """Cleans manually provided exclusion paths."""
    cleaned = []
    for ex in excludes:
        ex_clean = ex.replace('\\', '/')
        if ex_clean.startswith('./'):
            ex_clean = ex_clean[2:]
        ex_clean = ex_clean.rstrip('/')
        if ex_clean:
            cleaned.append(ex_clean)
    return cleaned

def is_ignored(item_path, base_dir, manual_excludes, gitignore_patterns, out_filename):
    """Determines if a file or folder should be ignored based on all rules."""
    rel_path = os.path.relpath(item_path, base_dir).replace(os.sep, '/')
    item_name = os.path.basename(item_path)

    # core exclusions
    scripts = ['read_folder.py', 'read_files.py']
    if item_name == out_filename or item_name in scripts:
        return True
    if item_name.endswith(('.spec', '.spec.ts', '.spec.js')):
        return True

    # manual exclusions
    for ex in manual_excludes:
        if item_name == ex or rel_path == ex or rel_path.startswith(ex + '/'):
            return True

    # gitignore exclusions
    if gitignore_patterns:
        for pattern in gitignore_patterns:
            clean_pattern = pattern.strip('/')
            if (fnmatch.fnmatch(item_name, clean_pattern) or 
                fnmatch.fnmatch(rel_path, clean_pattern) or 
                rel_path.startswith(clean_pattern + '/')):
                return True

    return False
