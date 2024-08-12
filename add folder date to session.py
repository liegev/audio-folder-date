import os
import subprocess
from datetime import datetime

def get_creation_date(file_path):
    try:
        result = subprocess.run(['stat', '-f', '%Sc', file_path], capture_output=True, text=True)
        creation_date_str = result.stdout.strip()
        return datetime.strptime(creation_date_str, '%b %d %H:%M:%S %Y')
    except Exception as e:
        print(f"Error retrieving creation date for {file_path}: {e}")
        return None

def find_oldest_date(directory):
    oldest_date = None
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_creation_date = get_creation_date(file_path)
            if file_creation_date and (oldest_date is None or file_creation_date < oldest_date):
                oldest_date = file_creation_date
    
    return oldest_date

def rename_folder_with_date_prefix(folder_path, date_text):
    """
    Rename the folder by prefixing the date text to its name.

    :param folder_path: Path to the folder to be renamed.
    :param date_text: Text to be prefixed to the folder name.
    """
    if not os.path.exists(folder_path):
        print(f"The folder {folder_path} does not exist.")
        return

    # Extract the folder name and its parent directory
    parent_dir = os.path.dirname(folder_path)
    folder_name = os.path.basename(folder_path)
    
    # Construct the new folder name
    new_folder_name = f"{date_text} {folder_name}"
    new_folder_path = os.path.join(parent_dir, new_folder_name)

    # Rename the folder
    try:
        os.rename(folder_path, new_folder_path)
        print(f"Folder renamed to: {new_folder_path}")
    except Exception as e:
        print(f"Error renaming folder: {e}")

def rename_all_folders_in_directory(parent_directory):
    """
    Rename all folders in the specified parent directory by prefixing the oldest file's creation date.

    :param parent_directory: Path to the parent directory containing folders to be renamed.
    """
    for item in os.listdir(parent_directory):
        folder_path = os.path.join(parent_directory, item)
        if os.path.isdir(folder_path):
            oldest_date = find_oldest_date(folder_path)
            if oldest_date:
                date_text = oldest_date.strftime('%Y-%m-%d')
                rename_folder_with_date_prefix(folder_path, date_text)
            else:
                print(f"No valid creation dates found in folder: {folder_path}")

if __name__ == "__main__":
    parent_directory = '/Volumes/MUSIC/staging'  # Change this to the parent directory you want to check
    rename_all_folders_in_directory(parent_directory)
