import os
import shutil

# Source and destination directory paths
source_dir = "Enter the path"
destination_dir = "Enter the path"

# Get a list of all files in the source directory
files_to_copy = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]

# Copy each file from the source directory to the destination directory
for file_name in files_to_copy:
    source_file_path = os.path.join(source_dir, file_name)
    destination_file_path = os.path.join(destination_dir, file_name)
    shutil.copy(source_file_path, destination_file_path)

print("Files copied successfully from", source_dir, "to", destination_dir)
