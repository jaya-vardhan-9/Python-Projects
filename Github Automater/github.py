import os
import time
import shutil
import subprocess
import concurrent.futures
from tqdm import tqdm

# Set the list of Git repository directories
git_repos = [
    # "D:\git-test",
    "Enter the path"
]

# Source directory containing files to be added
source_directory = "enter the path"

# Set the file extension of the files to be added to each repository
file_ext = ".txt"

# Define a function to add files to each repository
def add_files_to_repo(repo_dir):
    # Copy files from source directory to repository directory
    for file_name in os.listdir(source_directory):
        if file_name.endswith(file_ext):
            source_file_path = os.path.join(source_directory, file_name)
            destination_file_path = os.path.join(repo_dir, file_name)
            shutil.copy(source_file_path, destination_file_path)

# Define a function to run the Git operations for each repository
def run_git_operations(repo_dir):
    # Change the current working directory to the Git repository
    os.chdir(repo_dir)

    # Add all files with the specified extension to the Git repository
    subprocess.run(["git", "add", "*" + file_ext])

    # Commit the changes with a message
    subprocess.run(["git", "commit", "-m", "Adding temporary files"])

    # Push the changes to the remote GitHub repository
    subprocess.run(["git", "push", "origin", "main"], check=True)

    # Wait for a few minutes before deleting the files
    for remaining_time in tqdm(range(180, 0, -1), desc="Sleep Time", unit="s"):
        time.sleep(180)

    # Delete all files with the specified extension from the Git repository
    for file_name in os.listdir("."):
        if file_name.endswith(file_ext):
            os.remove(file_name)

    # Add the deleted files to the Git index
    subprocess.run(["git", "add", "-u"])

    # Commit the changes with a message
    subprocess.run(["git", "commit", "-m", "Deleting temporary files"])

    # Push the changes to the remote GitHub repository
    subprocess.run(["git", "push", "origin", "main"], check=True)

# Create a ThreadPoolExecutor to run the Git operations in parallel
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Copy files to each repository before running Git operations
    for repo in git_repos:
        executor.submit(add_files_to_repo, repo)

    # Submit the Git operations for each repository
    for repo in git_repos:
        executor.submit(run_git_operations, repo)
