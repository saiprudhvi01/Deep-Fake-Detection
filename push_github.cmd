@echo off
echo Setting up Git configuration...
call git config user.email saiprudhvibodempudi11@gmail.com
call git config user.name saiprudhvi01

echo Adding files to Git...
call git add .

echo Committing changes...
call git commit -m "Fix OpenCV dependencies for Streamlit Cloud"

echo Pushing to GitHub...
call git push origin main

echo.
echo ✅ Changes pushed to GitHub successfully!
echo You can now deploy to Streamlit Cloud: https://share.streamlit.io/deploy

pause
