# GitHub Setup Guide - SH Hostel Leave Management System

## Step-by-Step Instructions to Connect to GitHub

### **Step 1: Create a GitHub Repository**

1. Go to [GitHub.com](https://github.com)
2. Sign in to your account (or create one if you don't have an account)
3. Click the **"+"** icon in the top right corner
4. Select **"New repository"**
5. Fill in the details:
   - **Repository name**: `sh-hostel-leave-management` (or your preferred name)
   - **Description**: "Professional SH Hostel Student Leave Management System with Flask, SQLite, and animated UI"
   - **Visibility**: Choose **Public** (if you want to share) or **Private** (if personal)
   - **Initialize with**: Leave unchecked (we already have files)
6. Click **"Create repository"**

---

### **Step 2: Copy Your Repository URL**

After creating the repository, you'll see a page with your repository URL.
- Copy the **HTTPS URL** (looks like: `https://github.com/yourusername/sh-hostel-leave-management.git`)

---

### **Step 3: Add Remote and Push to GitHub**

Open PowerShell in the project directory and run:

```powershell
cd 'd:\project\leave takes'

# Add remote repository (replace with your URL)
git remote add origin https://github.com/yourusername/sh-hostel-leave-management.git

# Rename branch to main (if needed)
git branch -M main

# Push your code to GitHub
git push -u origin main
```

---

### **Step 4: Verify on GitHub**

1. Go to your GitHub repository URL
2. You should see all your files uploaded
3. Done! ✅

---

## Complete Git Commands Summary

```powershell
# Navigate to project
cd 'd:\project\leave takes'

# Configure Git (first time only)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Initialize repository (already done)
git init

# Add files (already done)
git add .

# Create initial commit (already done)
git commit -m "Initial commit: SH Hostel Leave Management System"

# Add remote and push
git remote add origin https://github.com/yourusername/sh-hostel-leave-management.git
git branch -M main
git push -u origin main
```

---

## Future Commits (After Changes)

After making changes, use these commands:

```powershell
# Check status
git status

# Add changed files
git add .

# Commit changes
git commit -m "Description of changes"

# Push to GitHub
git push
```

---

## Project Contents on GitHub

Your repository will include:

✅ **Backend**
- `app.py` - Main Flask application with all routes
- `seed_db.py` - Database seeding script

✅ **Frontend**
- `templates/` - All HTML templates
- `static/css/styles.css` - Professional animated styling
- `static/js/scripts.js` - JavaScript functionality

✅ **Database**
- `instance/leave_management.db` - SQLite database (excluded in .gitignore)

✅ **Documentation**
- `README.md` - Project overview
- `.gitignore` - Git ignore file

✅ **Utilities**
- `show_db.py` - Database viewer script
- `view_database.py` - Database viewer script

---

## Important Notes

⚠️ **Security:**
- The `.gitignore` file excludes:
  - Virtual environment (`.venv/`)
  - Database files (`*.db`)
  - Python cache files (`__pycache__/`)
  - IDE files (`.vscode/`, `.idea/`)

💡 **Tips:**
- Keep your repository public to showcase your work
- Write clear commit messages
- Pull before pushing if working in a team
- Create branches for new features

---

## Need Help?

If you encounter any issues:
1. Make sure Git is installed: `git --version`
2. Check your GitHub credentials
3. Ensure internet connection
4. Verify the repository URL is correct

