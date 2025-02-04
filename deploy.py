import os
import subprocess
import tempfile

def deploy_repository(repo_url):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_name = repo_url.split("/")[-1].replace(".git", "")
            repo_path = os.path.join(temp_dir, repo_name)

            # Clone Repository
            subprocess.run(["git", "clone", repo_url, repo_path], check=True)

            # Install Dependencies
            subprocess.run(["pip", "install", "-r", os.path.join(repo_path, "requirements.txt")], check=True)

            # Deploy Script Execution
            deploy_script = os.path.join(repo_path, "deploy.py")

            if os.path.exists(deploy_script):
                subprocess.run(["python", deploy_script], check=True)
                return True, f"Repository `{repo_name}` deployed successfully!"
            else:
                return False, "No `deploy.py` found in repository."

    except subprocess.CalledProcessError as e:
        return False, f"Deployment failed with error: {str(e)}"