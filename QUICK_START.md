# Quick Start Guide

## 🚀 Getting Started in 5 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Create Database
```bash
python manage.py migrate
```

### Step 3: Create Admin User
```bash
python manage.py createsuperuser
```
- Enter username (e.g., admin)
- Enter password (e.g., admin123)
- Confirm password

### Step 4: (Optional) Create Test Data
```bash
python manage.py shell < create_test_data.py
```

### Step 5: Run Server
```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

---

## 📝 Admin Workflow

1. **Login as Staff/Admin**
   - Go to: http://127.0.0.1:8000/semesters/admin/dashboard/

2. **Create Semester**
   - Click "Create Semester"
   - Enter name (e.g., "Semester 1", "Semester 2")

3. **Create Subject**
   - Click "Create Subject"
   - Select semester
   - Enter subject name (e.g., "Python Programming")

4. **Upload Questions from Excel**
   - Click "Upload Questions"
   - Select the subject
   - Upload your Excel file

### Excel Format:
```
| unit_number | question_text | MCQ Answer | option A | option B | option C | option D | Added By | Verified By |
|-------------|---------------|------------|----------|----------|----------|----------|----------|-------------|
| 1           | Question?     | A          | Option A | Option B | Option C | Option D | AKS      | MMS         |
```

**Important for Python Code:**
- Excel preserves indentation automatically
- Just paste your Python code in cells as-is
- The system will display it with proper formatting

---

## 👤 User Workflow

1. **Sign Up / Login**
   - Go to: http://127.0.0.1:8000/
   - Create account or login

2. **Take Quiz**
   - Select Semester
   - Select Subject
   - **Select Unit (1-10)** ← Important!
   - Take quiz (10 random questions from that unit)
   - Submit and see results

3. **View Profile**
   - Click "Profile" in navbar
   - See quiz history and statistics

---

## 🔑 Key Features

### ✅ Unit-Based Quiz System
- User selects specific unit (1-10)
- Gets **10 random questions from ONLY that unit**
- If unit has <10 questions, all questions shown

### ✅ Code Indentation Preserved
- Python code displayed with proper formatting
- Uses monospace font (Fira Code)
- Maintains tabs and spaces from Excel

### ✅ Immediate Results
- See score instantly after submission
- View all correct answers
- Track performance over time

---

## 📊 Excel Column Details

| Column | Required | Description | Example |
|--------|----------|-------------|---------|
| unit_number | Yes | Unit number (1-10) | 1 |
| question_text | Yes | The question | What is Python? |
| MCQ Answer | Yes | Correct option (A/B/C/D) | D |
| option A | **YES** | First option (MUST have value) | A programming language |
| option B | **YES** | Second option (MUST have value) | A snake |
| option C | **YES** | Third option (MUST have value) | A framework |
| option D | **YES** | Fourth option (MUST have value) | All of the above |
| Added By | No | Who added | AKS |
| Verified By | No | Who verified | MMS |

**⚠️ IMPORTANT**: All 4 options (A, B, C, D) MUST have values. Rows with any empty option will be skipped!

---

## 🎨 Technology Used

- **Backend**: Django 5.1.13
- **Frontend**: Tailwind CSS
- **Database**: SQLite
- **Excel**: pandas + openpyxl

---

## ⚡ Common Commands

```bash
# Run server
python manage.py runserver

# Create migrations (after model changes)
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Open Django shell
python manage.py shell
```

---

## 🐛 Troubleshooting

**Q: Questions not showing up?**
- Make sure you uploaded to correct subject
- Check unit number in Excel (Bar column)

**Q: Code indentation lost?**
- Make sure using updated Excel upload
- System now preserves all whitespace

**Q: Less than 10 questions in quiz?**
- That unit has less than 10 questions
- Add more questions or it will show all available

---

## 📞 Need Help?

- Check README.md for detailed documentation
- Review Django documentation: https://docs.djangoproject.com/

