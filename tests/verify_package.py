import os

'''
Internal script to verify that all python directory is contains __init__.py
'''

def check_init_files(build_dir=os.path.join(os.path.dirname(os.path.dirname(__file__)), "src")):
    paths = []
    for root, dirs, files in os.walk(build_dir):
        has_python_files = any(file.endswith('.py') for file in files)
        if has_python_files and '__init__.py' not in files:
            paths.append(root)
            
    if len(paths) == 0:
        print("No missing __init__ files.")
        return
    for path in paths:
        print(f"Missing __init__ file at {path}")


if __name__ == "__main__":
    check_init_files()