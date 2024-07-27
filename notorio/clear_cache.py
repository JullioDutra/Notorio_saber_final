import os
import shutil

def clear_cache():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    for root, dirs, files in os.walk(base_dir):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                shutil.rmtree(os.path.join(root, dir_name))
        for file_name in files:
            if file_name.endswith('.pyc'):
                os.remove(os.path.join(root, file_name))

if __name__ == "__main__":
    clear_cache()
    print("Cache cleared.")
