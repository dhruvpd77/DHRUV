# 📝 Excel Upload Guide - Complete Instructions

## 🎯 What Gets Imported

### ✅ ONLY MCQs (Multiple Choice Questions)
The system now **ONLY imports questions where ALL 4 options have values**. This ensures only proper MCQs are added to the database.

### ❌ What Gets Skipped
- Questions with empty question text
- Questions with any empty option (A, B, C, or D)
- Rows with incomplete data

---

## 📊 Excel Column Format

### Required Columns (Exact Names):

| Column Name | Type | Required | Description |
|------------|------|----------|-------------|
| **unit_number** | Number | ✅ YES | Unit number (1-10) |
| **question_text** | Text | ✅ YES | The question (can include Python code) |
| **MCQ Answer** | Letter | ✅ YES | Correct answer (A, B, C, or D) |
| **option A** | Text | ✅ **YES** | Option A text - MUST have value |
| **option B** | Text | ✅ **YES** | Option B text - MUST have value |
| **option C** | Text | ✅ **YES** | Option C text - MUST have value |
| **option D** | Text | ✅ **YES** | Option D text - MUST have value |
| **Added By** | Text | ❌ No | (Optional) Who created |
| **Verified By** | Text | ❌ No | (Optional) Who verified |

---

## ✅ Valid Excel Row Examples

### Example 1: Simple Question
```
unit_number: 1
question_text: Which character is used to make a single line comment?
option A: /
option B: //
option C: #
option D: !
MCQ Answer: C
Added By: AKS
Verified By: MMS
```
✅ **Result**: Will be imported (all options filled)

### Example 2: Python Code Question
```
unit_number: 2
question_text: What will be the output of print(type(5))?
option A: <class 'int'>
option B: <class 'float'>
option C: <class 'double'>
option D: <class 'integer'>
MCQ Answer: A
Added By: AKS
Verified By: MMS
```
✅ **Result**: Will be imported (all options filled)

### Example 3: Multi-line Code
```
unit_number: 3
question_text: What is the output?
for i in range(3):
    print(i)

option A: 0 1 2
option B: 1 2 3
option C: 0
1
2
option D: Error
MCQ Answer: C
```
✅ **Result**: Will be imported (code indentation preserved)

---

## ❌ Invalid Examples (Will Be SKIPPED)

### Example 1: Missing Option
```
unit_number: 1
question_text: What is Python?
option A: A language
option B: A snake
option C: 
option D: A framework
MCQ Answer: A
```
❌ **Skipped**: Option C is empty

### Example 2: Missing Multiple Options
```
unit_number: 2
question_text: True or False question
option A: True
option B: False
option C: 
option D: 
MCQ Answer: A
```
❌ **Skipped**: Options C and D are empty (not a proper MCQ)

### Example 3: No Question Text
```
unit_number: 3
question_text: 
option A: Option 1
option B: Option 2
option C: Option 3
option D: Option 4
MCQ Answer: A
```
❌ **Skipped**: No question text

---

## 🔥 Special Features

### 1. Unit Number Extraction
- Reads from **"unit_number"** column
- Supports units 1-10
- Defaults to 1 if invalid/empty

### 2. Code Indentation Preservation
- **ALL whitespace preserved** from Excel
- Spaces, tabs, newlines maintained
- Perfect for Python code questions

### 3. MCQ Answer Format
- Accepts: `A`, `B`, `C`, `D`
- Also accepts: `A)`, `B.`, `C -`, etc. (extracts letter)
- Case insensitive

---

## 📋 Step-by-Step Upload Process

### Step 1: Prepare Your Excel File
1. Create Excel with exact column names
2. Fill in all questions
3. **Ensure ALL 4 options have values for each question**
4. Save as .xlsx or .xls

### Step 2: Upload
1. Login as admin/staff
2. Go to Admin Dashboard
3. Click "Upload Questions"
4. Select subject
5. Choose Excel file
6. Click "Upload Questions"

### Step 3: Review Results
You'll see a message like:
- ✅ "15 MCQ questions uploaded successfully! (Skipped 5 incomplete rows)"
- ⚠️ "No valid MCQ questions found. Skipped 20 rows. Make sure all 4 options (A, B, C, D) have values."

---

## 🎯 Best Practices

### ✅ DO:
```excel
✓ Use exact column names (case-sensitive)
✓ Fill ALL 4 options for every question
✓ Paste Python code directly (indentation preserved)
✓ Use clear, distinct options
✓ Verify unit numbers are 1-10
```

### ❌ DON'T:
```excel
✗ Leave any option empty
✗ Use different column names
✗ Mix question types (MCQ vs True/False)
✗ Forget to set correct answer
✗ Leave question text empty
```

---

## 📊 Sample Excel Template

Here's a complete valid row:

```
| unit_number | question_text | MCQ Answer | option A | option B | option C | option D | Added By | Verified By |
|-------------|---------------|------------|----------|----------|----------|----------|----------|-------------|
| 1 | Which character is used to make a single line comment? | C | / | // | # | ! | AKS | MMS |
| 1 | What will be the output of print(type(5))? | A | <class 'int'> | <class 'float'> | <class 'double'> | <class 'integer'> | AKS | MMS |
| 2 | What is output of: x=10; print(x+5) | B | 105 | 15 | x+5 | Error | AKS | MMS |
```

---

## 🔍 Validation Logic

The system checks each row:

1. ✅ Is `unit_number` valid? (converts to integer)
2. ✅ Is `question_text` filled?
3. ✅ Is `option A` filled?
4. ✅ Is `option B` filled?
5. ✅ Is `option C` filled?
6. ✅ Is `option D` filled?
7. ✅ Is `MCQ Answer` valid (A/B/C/D)?

**If ANY check fails → Row is SKIPPED**

---

## 💡 Tips for Python Code Questions

### Indentation Example:
```python
# In Excel cell for question_text:
What will be the output?
for i in range(3):
    print(i)
```

System displays it as:
```
What will be the output?
for i in range(3):
    print(i)
```

### Multi-line Options:
```python
# In Excel cell for option A:
0
1
2
```

Perfect! The newlines are preserved.

---

## 🚨 Common Errors & Solutions

### Error: "No valid MCQ questions found"
**Cause**: All rows have empty options  
**Solution**: Fill ALL 4 options for each question

### Error: "0 questions uploaded"
**Cause**: Column names don't match  
**Solution**: Use exact names: `unit_number`, `question_text`, `option A`, etc.

### Error: Questions showing wrong unit
**Cause**: unit_number column has wrong values  
**Solution**: Check unit_number is between 1-10

### Code indentation lost
**Cause**: Using old version  
**Solution**: This is already fixed! Indentation preserved automatically.

---

## ✅ Verification After Upload

1. Go to Django Admin: `/admin/`
2. Click "Questions"
3. Verify:
   - ✓ Correct number of questions imported
   - ✓ All questions have 4 options
   - ✓ Code indentation looks correct
   - ✓ Unit numbers are correct

---

## 📞 Quick Reference

**Column Names (Copy-Paste):**
```
unit_number
question_text
MCQ Answer
option A
option B
option C
option D
Added By
Verified By
```

**Valid MCQ Answer Values:**
- A, B, C, D (any case)
- A), B), C), D)
- a, b, c, d

**Valid Unit Numbers:**
- 1, 2, 3, 4, 5, 6, 7, 8, 9, 10

---

**Result**: Only complete MCQs with ALL 4 options will be imported! 🎯

