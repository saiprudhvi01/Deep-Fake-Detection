# Set up Git configuration
$email = "saiprudhvibodempudi11@gmail.com"
$name = "saiprudhvi01"

try {
    # Configure Git
    git config --global user.email $email
    git config --global user.name $name
    
    Write-Host "Git configuration updated successfully!" -ForegroundColor Green
    
    # Add all files
    git add .
    
    # Commit changes
    git commit -m "Fix OpenCV dependencies for Streamlit Cloud deployment"
    
    # Push to GitHub
    git push origin main
    
    Write-Host "\n✅ Changes pushed to GitHub successfully!" -ForegroundColor Green
    Write-Host "You can now deploy to Streamlit Cloud: https://share.streamlit.io/deploy" -ForegroundColor Cyan
} catch {
    Write-Host "\n❌ Error occurred: $_" -ForegroundColor Red
    Write-Host "Please check your Git configuration and try again." -ForegroundColor Yellow
}

# Keep the window open
Write-Host "\nPress any key to exit..."
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
