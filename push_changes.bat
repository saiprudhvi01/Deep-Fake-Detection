@echo off
echo Setting up Git configuration...
git config --global user.email "user@example.com"
git config --global user.name "User"

echo Adding files to Git...
git add .

echo Committing changes...
git commit -m "Fix OpenCV dependencies for Streamlit Cloud"

echo Pushing to GitHub...
git push origin main

echo Done!
