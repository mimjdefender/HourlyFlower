# Hourly Flower Graphic Generator

This automation system generates and updates flower graphics for Meds Cafe stores, uploading them to GitHub for use with Prismic CMS.

## Setup

1. Install required Python packages:
```bash
pip install Pillow PyGithub
```

2. Configure GitHub:
   - Create a GitHub repository
   - Generate a Personal Access Token with `repo` permissions
   - Set the GitHub token as an environment variable:
     ```bash
     # Windows
     setx GITHUB_TOKEN "your-token-here"
     
     # Linux/Mac
     export GITHUB_TOKEN="your-token-here"
     ```
   - Update `GITHUB_REPO` in `flower_slide_component.py` with your repository name

3. Place your background image as `image_fx (10).jpg` in the directory

## Usage

Run the hourly update script:
```bash
.\run_flower_update_hourly.bat
```

This will:
1. Generate flower graphics for each store
2. Upload them to GitHub
3. Create Prismic CMS embed data
4. Repeat every hour

## Files

- `flower_slide_component.py` - Main script for generating graphics
- `github_upload.py` - Handles GitHub uploads
- `run_flower_update_hourly.bat` - Hourly update script
- `image_fx (10).jpg` - Background image for graphics

## Prismic CMS Integration

The script generates JSON files that can be used with Prismic CMS embed fields. The graphics are hosted on GitHub and will automatically update hourly.

## Security Note

Never commit your GitHub token to the repository. Always use environment variables to store sensitive information. 