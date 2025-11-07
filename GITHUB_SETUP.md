# GitHub Setup Guide for QuizNjoy

## Step 1: Install Git (if not installed)

### For Windows:
1. Download Git from: https://git-scm.com/download/win
2. Run the installer and follow the setup wizard
3. Restart your terminal/PowerShell after installation

### Verify Installation:
```bash
git --version
```

## Step 2: Configure Git (First Time Only)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Step 3: Initialize Git Repository

```bash
cd "C:\Users\Dhruv\Desktop\B4 QUIZ"
git init
```

## Step 4: Add All Files

```bash
git add .
```

## Step 5: Create Initial Commit

```bash
git commit -m "Initial commit: QuizNjoy Django project"
```

## Step 6: Create GitHub Repository

1. Go to https://github.com
2. Click the **"+"** icon in the top right
3. Select **"New repository"**
4. Repository name: `QuizNjoy` (or any name you prefer)
5. Description: "Django Quiz Platform with Tailwind CSS"
6. Choose **Public** or **Private**
7. **DO NOT** initialize with README, .gitignore, or license (we already have these)
8. Click **"Create repository"**

## Step 7: Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/QuizNjoy.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 8: Future Updates

Whenever you make changes:

```bash
# Check what changed
git status

# Add changes
git add .

# Commit changes
git commit -m "Description of your changes"

# Push to GitHub
git push
```

## Important Notes:

1. **Never commit sensitive data:**
   - SECRET_KEY in settings.py (use environment variables)
   - Database passwords
   - API keys

2. **The .gitignore file** already excludes:
   - Database files (db.sqlite3)
   - Media files
   - Static files
   - Python cache files
   - Environment variables

3. **For production**, consider:
   - Using environment variables for SECRET_KEY
   - Creating a separate settings file for production
   - Using a proper database (PostgreSQL, MySQL)

## Quick Commands Reference:

```bash
git status              # Check repository status
git add .               # Stage all changes
git commit -m "message"  # Commit changes
git push                 # Push to GitHub
git pull                 # Pull from GitHub
git log                  # View commit history
```

## Troubleshooting:

### If you get "fatal: not a git repository":
```bash
git init
```

### If you get authentication errors:
- Use GitHub Personal Access Token instead of password
- Generate token: GitHub Settings → Developer settings → Personal access tokens

### If you want to change remote URL:
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/QuizNjoy.git
```

---

**Need Help?** Check GitHub documentation: https://docs.github.com

