import os
import shutil
from tkinter import Tk
from tkinter import filedialog

# Create a Tkinter root window (it won't be shown)
root = Tk()
root.withdraw()  # Hide the root window

# Open a dialog to select a folder
folder_path = filedialog.askdirectory(title="Select Folder Containing Excel Files")

# Check if a folder was selected
if not folder_path:
    print("No folder selected. Exiting.")
else:
    # List all files in the directory
    for filename in os.listdir(folder_path):
        # Check if the file is an Excel file
        if filename.endswith('.xlsx') or filename.endswith('.xls'):
            # Create a folder with the file name (without extension)
            folder_name = os.path.join(folder_path, os.path.splitext(filename)[0])
            os.makedirs(folder_name, exist_ok=True)

            # Move the Excel file into the new folder
            shutil.move(os.path.join(folder_path, filename), os.path.join(folder_name, filename))

    print("Files have been moved into their respective folders.")
