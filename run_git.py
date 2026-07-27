import os
import subprocess

def run_git():
    repo_dir = r"E:\Github\canal-tutorial-automation"
    print("Executing in:", repo_dir)
    os.chdir(repo_dir)
    
    print("--- git status ---")
    result = subprocess.run(["git", "status"], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("ERR:", result.stderr)

if __name__ == "__main__":
    run_git()
