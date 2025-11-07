# Push QuizNjoy to GitHub - Quick Guide

## Repository Details
- **Repository URL:** `https://github.com/dhruvpd77/quiznjoy.git`
- **Branch Name:** `quiznjoyfinal`
- **Repository Type:** Private

## Quick Setup (After Installing Git)

### Option 1: Use the Automated Script (Recommended)

1. **Install Git** (if not installed):
   - Download: https://git-scm.com/download/win
   - Install with default settings
   - **Restart your terminal/PowerShell**

2. **Run the script:**
   ```bash
   push_to_github.bat
   ```

3. **If prompted for credentials:**
   - Username: `dhruvpd77`
   - Password: Use a **Personal Access Token** (not your GitHub password)
   
   **To create a Personal Access Token:**
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Name: "QuizNjoy Project"
   - Select scope: `repo` (full control of private repositories)
   - Click "Generate token"
   - **Copy the token immediately** (you won't see it again)
   - Use this token as your password when pushing

### Option 2: Manual Commands

If you prefer to run commands manually:

```bash
# 1. Initialize git (if not already done)
git init

# 2. Add remote repository
git remote add origin https://github.com/dhruvpd77/quiznjoy.git

# 3. Add all files
git add .

# 4. Create initial commit
git commit -m "Initial commit: QuizNjoy Django project - Full implementation"

# 5. Create and switch to quiznjoyfinal branch
git checkout -b quiznjoyfinal

# 6. Push to GitHub
git push -u origin quiznjoyfinal
```

## Future Updates

After the initial push, to update your repository:

```bash
# Add changes
git add .

# Commit changes
git commit -m "Description of changes"

# Push to quiznjoyfinal branch
git push origin quiznjoyfinal
```

## Troubleshooting

### "Git is not recognized"
- Install Git from https://git-scm.com/download/win
- Restart terminal after installation

### "Authentication failed"
- Use Personal Access Token instead of password
- Generate token: https://github.com/settings/tokens
- Select `repo` scope

### "Remote already exists"
- Update remote: `git remote set-url origin https://github.com/dhruvpd77/quiznjoy.git`

### "Branch already exists"
- Switch to branch: `git checkout quiznjoyfinal`
- Or delete and recreate: `git branch -D quiznjoyfinal` then `git checkout -b quiznjoyfinal`

### "Permission denied"
- Make sure you have access to the repository
- Check that you're using the correct username
- Verify your Personal Access Token has `repo` permissions

## View Your Code on GitHub

After pushing, view your code at:
**https://github.com/dhruvpd77/quiznjoy/tree/quiznjoyfinal**

---

**Need Help?** 
- GitHub Docs: https://docs.github.com
- Git Docs: https://git-scm.com/doc

