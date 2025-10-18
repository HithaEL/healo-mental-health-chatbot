# PowerShell script to upload Complete Psykh Mental Health Platform to GitHub
# Run this script from the project directory

Write-Host "🚀 Complete Psykh Mental Health Platform - GitHub Upload Script" -ForegroundColor Green
Write-Host "===============================================================" -ForegroundColor Green

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
Write-Host "📁 Adding all project files to Git..." -ForegroundColor Yellow
git add .

# Check if there are changes to commit
$status = git status --porcelain
if ($status) {
    Write-Host "📝 Committing complete project..." -ForegroundColor Yellow
    git commit -m "Initial commit: Complete Psykh Mental Health Platform v1.0.0

Features:
- Rasa conversational AI with NLU and dialogue management
- Django web application with full UI
- Flask API server with RESTful endpoints  
- Advanced ML models with 100% training accuracy
- Comprehensive mental health dataset (762 examples)
- Modern responsive frontend
- Complete testing and evaluation suite
- 13 mental health categories coverage
- Professional documentation and setup guides

Components:
- Rasa: actions.py, config.yml, domain.yml, data/nlu.yml, data/stories.yml
- Django: psykh_web/ with complete web application
- Flask: api_server.py with AI endpoints
- ML: advanced_model_training.py, improved_ai_backend.py
- Frontend: index.html, chatbot.html, articles.html, videos.html
- Data: 762 training examples across 13 mental health categories
- Testing: comprehensive evaluation and accuracy testing
- Documentation: complete setup and usage guides"
    
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
Write-Host "3. Repository name: 'psykh-mental-health-platform'" -ForegroundColor White
Write-Host "4. Description: 'Complete mental health AI platform with Rasa, Django, Flask, and advanced ML models'" -ForegroundColor White
Write-Host "5. Choose Public or Private" -ForegroundColor White
Write-Host "6. DO NOT initialize with README, .gitignore, or license (we already have them)" -ForegroundColor White
Write-Host "7. Click 'Create repository'" -ForegroundColor White
Write-Host ""

$githubUrl = Read-Host "Enter your GitHub repository URL (e.g., https://github.com/username/psykh-mental-health-platform.git)"

if ($githubUrl -eq "") {
    Write-Host "❌ No repository URL provided. Exiting." -ForegroundColor Red
    exit 1
}

# Add remote origin
Write-Host "🔗 Adding remote origin..." -ForegroundColor Yellow
git remote add origin $githubUrl

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️ Remote origin might already exist. Updating..." -ForegroundColor Yellow
    git remote set-url origin $githubUrl
}

# Set main branch
Write-Host "🌿 Setting main branch..." -ForegroundColor Yellow
git branch -M main

# Push to GitHub
Write-Host "⬆️ Pushing complete project to GitHub..." -ForegroundColor Yellow
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "🎉 SUCCESS! Complete Psykh Mental Health Platform uploaded to GitHub!" -ForegroundColor Green
    Write-Host "=================================================================" -ForegroundColor Green
    Write-Host "Repository URL: $githubUrl" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📊 What was uploaded:" -ForegroundColor Yellow
    Write-Host "✅ Rasa conversational AI components" -ForegroundColor White
    Write-Host "✅ Django web application (psykh_web/)" -ForegroundColor White
    Write-Host "✅ Flask API server with AI endpoints" -ForegroundColor White
    Write-Host "✅ Advanced ML models (100% training accuracy)" -ForegroundColor White
    Write-Host "✅ Complete frontend (HTML, CSS, JS)" -ForegroundColor White
    Write-Host "✅ Training data (762 examples, 13 categories)" -ForegroundColor White
    Write-Host "✅ Testing and evaluation suite" -ForegroundColor White
    Write-Host "✅ Professional documentation" -ForegroundColor White
    Write-Host "✅ Setup and deployment guides" -ForegroundColor White
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Visit your repository on GitHub" -ForegroundColor White
    Write-Host "2. Check that all components are uploaded" -ForegroundColor White
    Write-Host "3. Enable Issues, Projects, Wiki, and Discussions" -ForegroundColor White
    Write-Host "4. Add topics: mental-health, ai, chatbot, rasa, django, flask" -ForegroundColor White
    Write-Host "5. Create your first release (v1.0.0)" -ForegroundColor White
    Write-Host "6. Set up branch protection rules" -ForegroundColor White
    Write-Host "7. Share with the community!" -ForegroundColor White
    Write-Host ""
    Write-Host "📚 For detailed setup instructions, see COMPLETE_PROJECT_UPLOAD.md" -ForegroundColor Blue
} else {
    Write-Host ""
    Write-Host "❌ Failed to push to GitHub. Common issues:" -ForegroundColor Red
    Write-Host "1. Authentication failed - use Personal Access Token" -ForegroundColor Yellow
    Write-Host "2. Repository doesn't exist - create it on GitHub first" -ForegroundColor Yellow
    Write-Host "3. Network issues - check your internet connection" -ForegroundColor Yellow
    Write-Host "4. Large files - check .gitignore is working" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Manual steps:" -ForegroundColor Cyan
    Write-Host "1. Create repository on GitHub" -ForegroundColor White
    Write-Host "2. Run: git push -u origin main" -ForegroundColor White
    Write-Host "3. Or use GitHub Desktop for easier upload" -ForegroundColor White
}

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
