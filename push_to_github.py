import subprocess
import sys

def push_to_github(commit_message, remote_url=None):
    """
    Automates the git add, commit, and push process, with an option to set the remote URL.
    
    This function assumes that Git is installed and the current directory is a Git repository.
    
    Args:
        commit_message (str): The commit message for the changes.
        remote_url (str, optional): The URL of the remote repository to set or add.
                                    If not provided, the script assumes the remote is already configured.
    """
    try:
        # Check if a remote 'origin' already exists
        subprocess.run(["git", "remote", "get-url", "origin"], check=True, capture_output=True)
        print("Remote 'origin' already exists. Updating its URL.")
        # If it exists, set the URL.
        subprocess.run(["git", "remote", "set-url", "origin", remote_url], check=True)
    except subprocess.CalledProcessError:
        print("No remote 'origin' found. Adding the remote with the provided URL.")
        # If it doesn't exist, add it.
        subprocess.run(["git", "remote", "add", "origin", remote_url], check=True)
    
    try:
        print("\nStaging all changes...")
        subprocess.run(["git", "add", "."], check=True)
        print("Changes staged successfully.")

        print(f"Committing with message: '{commit_message}'")
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        print("Commit successful.")

        print("Pushing to remote repository...")
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
        print("Push successful. All files have been pushed to GitHub.")
    
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running a git command: {e.stderr}", file=sys.stderr)
        print("Please ensure your Git repository is correctly set up and you have the necessary permissions.", file=sys.stderr)
    except FileNotFoundError:
        print("Error: The 'git' command was not found. Please ensure Git is installed and accessible from your system's PATH.", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        commit_msg_parts = sys.argv[1:-1]
        commit_msg = " ".join(commit_msg_parts)
        remote_url_arg = sys.argv[-1]
    else:
        print("Please provide both a commit message and the remote URL.")
        print("Example: python push_to_github.py \"Initial commit\" https://github.com/your-username/your-repo.git")
        sys.exit(1)
    
    push_to_github(commit_msg, remote_url_arg)