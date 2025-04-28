import os
import base64
from github import Github
from datetime import datetime

def upload_to_github(image_path, repo_name, branch="main"):
    """
    Upload an image to GitHub repository.
    
    Args:
        image_path (str): Path to the image file
        repo_name (str): GitHub repository name (format: "username/repo")
        branch (str): Branch name to upload to
    """
    try:
        # Get GitHub token from environment variable
        github_token = os.getenv('GITHUB_TOKEN')
        if not github_token:
            raise ValueError("GITHUB_TOKEN environment variable not set")

        # Initialize GitHub client
        g = Github(github_token)
        repo = g.get_repo(repo_name)

        # Read image file
        with open(image_path, 'rb') as image_file:
            image_content = image_file.read()
            image_base64 = base64.b64encode(image_content).decode()

        # Create file path in repo
        filename = os.path.basename(image_path)
        file_path = f"flower-graphics/{filename}"

        try:
            # Try to get the file first
            contents = repo.get_contents(file_path, ref=branch)
            # Update existing file
            repo.update_file(
                path=file_path,
                message=f"Update flower graphic - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                content=image_base64,
                sha=contents.sha,
                branch=branch
            )
        except Exception:
            # Create new file if it doesn't exist
            repo.create_file(
                path=file_path,
                message=f"Add flower graphic - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                content=image_base64,
                branch=branch
            )

        # Generate raw content URL
        raw_url = f"https://raw.githubusercontent.com/{repo_name}/{branch}/{file_path}"
        return raw_url

    except Exception as e:
        print(f"Error uploading to GitHub: {str(e)}")
        return None

if __name__ == "__main__":
    # Example usage
    image_path = "flower_slide_cheboygan.png"
    repo_name = "your-username/your-repo"  # Replace with your GitHub repo
    
    raw_url = upload_to_github(image_path, repo_name)
    if raw_url:
        print(f"✅ Image uploaded successfully!")
        print(f"🔗 Raw URL: {raw_url}") 