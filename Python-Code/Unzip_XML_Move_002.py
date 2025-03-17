import os
import pyzipper
import shutil
import tkinter as tk
from tkinter import simpledialog, messagebox

def extract_zip(zip_path, extract_to, password):
    """Extracts a password-protected zip file."""
    try:
        with pyzipper.AESZipFile(zip_path) as zf:
            zf.pwd = password
            zf.extractall(path=extract_to)
            print(f"Extracted: {zip_path}")
    except Exception as e:
        print(f"Failed to extract {zip_path}: {e}")

def delete_sig_files(folder):
    """Deletes all .sig files in a folder and its subfolders."""
    for root, dirs, files in os.walk(folder):
        for file_name in files:
            if file_name.endswith(".sig"):
                try:
                    file_path = os.path.join(root, file_name)
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")

def move_xml_files(source_folder, destination_folder):
    """Moves all .xml files from the source folder to the destination folder."""
    # Ensure the destination folder exists
    os.makedirs(destination_folder, exist_ok=True)

    # Traverse all subdirectories to find .xml files
    for root, dirs, files in os.walk(source_folder):
        for file_name in files:
            if file_name.endswith(".xml"):
                source_path = os.path.join(root, file_name)
                destination_path = os.path.join(destination_folder, file_name)

                try:
                    # If the file already exists in the destination, rename it to avoid overwriting
                    if os.path.exists(destination_path):
                        base_name, ext = os.path.splitext(file_name)
                        count = 1
                        while os.path.exists(destination_path):
                            destination_path = os.path.join(
                                destination_folder, f"{base_name}_{count}{ext}"
                            )
                            count += 1

                    # Move the file
                    shutil.move(source_path, destination_path)
                    print(f"Moved: {source_path} -> {destination_path}")
                except Exception as e:
                    print(f"Failed to move {source_path}: {e}")

def get_input(prompt, width=200, height=200):
    """Displays a simple pop-up to get user input."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Set the geometry of the dialog window (size and position)
    root.geometry(
        f"{width}x{height}+{int((root.winfo_screenwidth() - width) / 2)}+{int((root.winfo_screenheight() - height) / 2)}")

    # Get user input via simpledialog
    user_input = simpledialog.askstring("Input", prompt, parent=root)

    return user_input

def main():
    # Initialize Tkinter root window (hidden)
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Ask for user inputs using pop-up windows
    base_folder = get_input("Enter the base folder path: ")
    password = get_input("Enter the password for zip files: ")
    source_folder = get_input("Enter the source folder path: ")
    destination_folder = get_input("Enter the destination folder path: ")

    if not base_folder or not password or not source_folder or not destination_folder:
        messagebox.showerror("Input Error", "All fields must be filled!")
        return

    # Convert password to bytes
    password = password.encode()

    # Extract and process files
    for root, dirs, files in os.walk(base_folder):
        for file_name in files:
            if file_name.endswith(".zip"):
                zip_path = os.path.join(root, file_name)
                extract_to = root  # Extract to the current folder
                extract_zip(zip_path, extract_to, password)

        # After processing all zip files in a folder, delete .sig files
        delete_sig_files(root)

    print("Extraction and cleanup completed.")

    # Move .xml files
    move_xml_files(source_folder, destination_folder)

    print("All .xml files have been moved.")

    # Show a message box when the process is complete
    messagebox.showinfo("Process Complete", "All files have been processed.")

    source_folder1 = destination_folder

    # Check if the source folder exists
    if not os.path.exists(source_folder1):
        print("The specified source folder does not exist.")
        exit()

    # Iterate through the files in the folder
    xml_files = [f for f in os.listdir(source_folder1) if f.endswith(".xml")]

    # Group files by their base name (ignoring extensions and numbering)
    grouped_files = {}
    for file in xml_files:
        # Extract the base name by removing extensions and numbering
        base_name = ''.join([char for char in file.split(".")[0] if not char.isdigit()])
        grouped_files.setdefault(base_name, []).append(file)

    # Process each group and move files to their respective folders
    for base_name, files in grouped_files.items():
        # Define the target folder for this base name
        target_folder = os.path.join(source_folder1, base_name)

        # Create the target folder if it doesn't exist
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        # Move each file in the group to the target folder
        for file in files:
            shutil.move(os.path.join(source_folder1, file), os.path.join(target_folder, file))

    print("Files have been organized into folders based on their base names.")

if __name__ == "__main__":
    main()
