# PowerShell script to upload Healo Mental Health Chatbot to GitHub
# Run this script from the project directory

Write-Host "🚀 Healo Mental Health Chatbot - GitHub Upload Script" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

# Check if git is installed
try {
    $gitVersion = git --version
    Write-Host "✅ Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git is not installed. Please install Git first." -ForegroundColor Red
    Write-Host "Download from: https://git-scm.com/downloads" -ForegroundColor Yellow
    exit 1
}

# Check if we're in a git repository
if (Test-Path ".git") {
    Write-Host "✅ Git repository already initialized" -ForegroundColor Green
} else {
    Write-Host "🔧 Initializing Git repository..." -ForegroundColor Yellow
    git init
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to initialize Git repository" -ForegroundColor Red
        exit 1
    }
}

# Add all files
Write-Host "📁 Adding files to Git..." -ForegroundColor Yellow
git add .

# Check if there are changes to commit
$status = git status --porcelain
if ($status) {
    Write-Host "📝 Committing changes..." -ForegroundColor Yellow
    git commit -m "Initial commit: Healo Mental Health Chatbot v1.0.0 - Advanced AI mental health support with 100% training accuracy"
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to commit changes" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "ℹ️ No changes to commit" -ForegroundColor Blue
}

# Get GitHub repository URL
Write-Host ""
Write-Host "🔗 GitHub Repository Setup" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan
Write-Host "Please follow these steps:" -ForegroundColor Yellow
Write-Host "1. Go to https://github.com and sign in" -ForegroundColor White
Write-Host "2. Click the '+' icon and select 'New repository'" -ForegroundColor White
Write-Host "3. Repository name: 'healo-mental-health-chatbot'" -ForegroundColor White
Write-Host "4. Description: 'AI-powered mental health chatbot providing empathetic and professional support'" -ForegroundColor White
Write-Host "5. Choose Public or Private" -ForegroundColor White
Write-Host "6. DO NOT initialize with README, .gitignore, or license (we already have them)" -ForegroundColor White
Write-Host "7. Click 'Create repository'" -ForegroundColor White
Write-Host ""

$githubUrl = Read-Host "Enter your GitHub repository URL (e.g., https://github.com/username/healo-mental-health-chatbot.git)"

if ($githubUrl -eq "") {
    Write-Host "❌ No repository URL provided. Exiting." -ForegroundColor Red
    exit 1
}

# Add remote origin
Write-Host "🔗 Adding remote origin..." -ForegroundColor Yellow
git remote add origin $githubUrl

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️ Remote origin might already exist. Continuing..." -ForegroundColor Yellow
    git remote set-url origin $githubUrl
}

# Set main branch
Write-Host "🌿 Setting main branch..." -ForegroundColor Yellow
git branch -M main

# Push to GitHub
Write-Host "⬆️ Pushing to GitHub..." -ForegroundColor Yellow
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "🎉 SUCCESS! Your Healo Mental Health Chatbot has been uploaded to GitHub!" -ForegroundColor Green
    Write-Host "================================================================" -ForegroundColor Green
    Write-Host "Repository URL: $githubUrl" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Visit your repository on GitHub" -ForegroundColor White
    Write-Host "2. Check that all files are uploaded correctly" -ForegroundColor White
    Write-Host "3. Verify the README.md displays properly" -ForegroundColor White
    Write-Host "4. Consider enabling GitHub Pages for hosting" -ForegroundColor White
    Write-Host "5. Set up branch protection rules" -ForegroundColor White
    Write-Host "6. Create your first release" -ForegroundColor White
    Write-Host ""
    Write-Host "📚 For detailed setup instructions, see GITHUB_SETUP_GUIDE.md" -ForegroundColor Blue
} else {
    Write-Host ""
    Write-Host "❌ Failed to push to GitHub. Common issues:" -ForegroundColor Red
    Write-Host "1. Authentication failed - use Personal Access Token" -ForegroundColor Yellow
    Write-Host "2. Repository doesn't exist - create it on GitHub first" -ForegroundColor Yellow
    Write-Host "3. Network issues - check your internet connection" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Manual steps:" -ForegroundColor Cyan
    Write-Host "1. Create repository on GitHub" -ForegroundColor White
    Write-Host "2. Run: git push -u origin main" -ForegroundColor White
    Write-Host "3. Or use GitHub Desktop for easier upload" -ForegroundColor White
}

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
