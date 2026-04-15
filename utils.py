import os
import shutil
import tempfile
from pathlib import Path

def save_uploaded_file(uploaded_file) -> str:
    """
    Saves a Streamlit UploadedFile to a temporary directory and returns the path.
    """
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def cleanup_files(*file_paths):
    """
    Deletes the provided file paths to free up space.
    """
    for path in file_paths:
        if path and os.path.exists(path):
            try:
                os.remove(path)
            except Exception as e:
                print(f"Error deleting file {path}: {e}")
