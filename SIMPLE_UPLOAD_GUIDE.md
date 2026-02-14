# 🚀 SIMPLE UPLOAD - Quick Guide

## ✨ Super Simple! Just 2 Steps!

---

## Step 1: Edit the Variables (One Time Setup)

Open: **`backend/simple_upload.py`**

Find this section at the top:

```python
# ============================================================================
# 👇 CHANGE THESE VARIABLES - THAT'S ALL YOU NEED TO DO!
# ============================================================================

# PDF Configuration
PDF_PATH = "F:/projects/ruya_AI_hackathon/data/resumes.pdf"  # Change this!

# Job Configuration
JOB_TITLE = "Software Engineer"
JOB_DESCRIPTION = "Looking for experienced software engineer"
REQUIRED_SKILLS = ["Python", "JavaScript", "React", "Docker"]
MINIMUM_EXPERIENCE = 3
HIRING_SLOTS = 2

# Shortlisting Configuration
PHASE1_SHORTLIST_COUNT = 10
PHASE2_SHORTLIST_COUNT = 5
```

**Change these to your needs!**

---

## Step 2: Run It!

### Option A: Double-Click
```
Double-click: run_simple_upload.bat
```

### Option B: Command Line
```powershell
cd backend
.venv\Scripts\activate
python simple_upload.py
```

**DONE! Results in 3 minutes!**

---

## 📝 Examples

### Example 1: Python Developer Job

Edit `simple_upload.py`:

```python
PDF_PATH = "F:/my_resumes/python_developers.pdf"

JOB_TITLE = "Senior Python Developer"
JOB_DESCRIPTION = "Looking for experienced Python backend developer"
REQUIRED_SKILLS = ["Python", "Django", "FastAPI", "PostgreSQL", "Docker"]
MINIMUM_EXPERIENCE = 5
HIRING_SLOTS = 2

PHASE1_SHORTLIST_COUNT = 10
PHASE2_SHORTLIST_COUNT = 5
```

Then run: `run_simple_upload.bat`

---

### Example 2: Frontend Developer Job

Edit `simple_upload.py`:

```python
PDF_PATH = "C:/Users/YourName/Documents/frontend_resumes.pdf"

JOB_TITLE = "Frontend Developer"
JOB_DESCRIPTION = "Looking for React expert"
REQUIRED_SKILLS = ["React", "TypeScript", "JavaScript", "CSS", "HTML"]
MINIMUM_EXPERIENCE = 2
HIRING_SLOTS = 1

PHASE1_SHORTLIST_COUNT = 8
PHASE2_SHORTLIST_COUNT = 3
```

Then run: `run_simple_upload.bat`

---

### Example 3: Data Scientist Job

Edit `simple_upload.py`:

```python
PDF_PATH = "D:/recruitment/data_scientist_candidates.pdf"

JOB_TITLE = "Data Scientist"
JOB_DESCRIPTION = "Looking for ML expert with Python"
REQUIRED_SKILLS = ["Python", "Machine Learning", "TensorFlow", "Pandas", "NumPy"]
MINIMUM_EXPERIENCE = 4
HIRING_SLOTS = 1

PHASE1_SHORTLIST_COUNT = 12
PHASE2_SHORTLIST_COUNT = 6
```

Then run: `run_simple_upload.bat`

---

## 🎯 What You'll See

```
================================================================================
🎯 SIMPLE RESUME UPLOADER
================================================================================

📋 Configuration:
   PDF: F:/projects/ruya_AI_hackathon/data/resumes.pdf
   Job: Software Engineer
   Skills: Python, JavaScript, React, Docker
   Experience: 3 years
   Phase 1 Count: 10
   Phase 2 Count: 5

✅ Backend is running

📝 Creating job posting...
   Title: Software Engineer
   Skills: Python, JavaScript, React, Docker
   Experience: 3 years
✅ Job created! ID: abc-123

📤 Uploading: F:/projects/ruya_AI_hackathon/data/resumes.pdf
✅ Uploaded! Processed 20 resumes

🚀 Starting shortlisting process...
✅ Shortlisting started!

⏳ Monitoring progress (press Ctrl+C to stop)...

📊 Status: PHASE1
   Total: 20 | Phase1: 10 | Phase2: 0 | Shortlisted: 0

📊 Status: PHASE2
   Total: 20 | Phase1: 10 | Phase2: 5 | Shortlisted: 5

✅ Completed!

📋 Fetching results...

✨ 5 Candidates Shortlisted!

================================================================================

1. John Smith
   📧 Email: john@example.com
   🎯 Confidence: 95.0%
   💼 Experience: 5 years
   🛠️  Skills: Python, Django, React, Docker, AWS
   💬 Cover Letter: I am excited to apply for the Software Engineer position...

--------------------------------------------------------------------------------

[... more candidates ...]

💾 Results saved to: shortlisted_abc-123.json

================================================================================
✅ DONE!
================================================================================

💡 View in browser: http://localhost:3000
💡 Job ID: abc-123
```

---

## 📂 PDF Path Examples

### Windows Paths (use forward slashes `/` or double backslashes `\\`):

```python
# Option 1: Forward slashes (RECOMMENDED)
PDF_PATH = "F:/projects/ruya_AI_hackathon/data/resumes.pdf"

# Option 2: Double backslashes
PDF_PATH = "F:\\projects\\ruya_AI_hackathon\\data\\resumes.pdf"

# Option 3: Raw string
PDF_PATH = r"F:\projects\ruya_AI_hackathon\data\resumes.pdf"

# All work the same!
```

### Common Locations:

```python
# Project data folder
PDF_PATH = "F:/projects/ruya_AI_hackathon/data/resumes.pdf"

# Desktop
PDF_PATH = "C:/Users/YourName/Desktop/resumes.pdf"

# Documents
PDF_PATH = "C:/Users/YourName/Documents/resumes.pdf"

# Downloads
PDF_PATH = "C:/Users/YourName/Downloads/resumes.pdf"

# External drive
PDF_PATH = "D:/recruitment/resumes.pdf"
```

---

## ⚙️ Variable Explanations

### PDF Configuration:
- **PDF_PATH**: Full path to your PDF file (one resume per page)

### Job Configuration:
- **JOB_TITLE**: The job position title
- **JOB_DESCRIPTION**: Optional description of the job
- **REQUIRED_SKILLS**: List of required skills (comma-separated in brackets)
- **MINIMUM_EXPERIENCE**: Minimum years of experience required
- **HIRING_SLOTS**: Number of positions to fill

### Shortlisting Configuration:
- **PHASE1_SHORTLIST_COUNT**: How many to keep after keyword matching
- **PHASE2_SHORTLIST_COUNT**: Final shortlist size after AI review

---

## 💡 Tips

1. **Use forward slashes** in paths (easier): `"F:/path/to/file.pdf"`
2. **Full path required** - not just filename
3. **One resume per page** in the PDF
4. **Adjust phase counts** based on total resumes:
   - 20 resumes → Phase1: 10, Phase2: 5
   - 50 resumes → Phase1: 20, Phase2: 10
   - 100 resumes → Phase1: 30, Phase2: 15

---

## ✅ Checklist Before Running

- ☐ Backend is running (`python main.py` in backend folder)
- ☐ Ollama is running (`ollama serve`)
- ☐ PDF_PATH is correct and file exists
- ☐ Variables are set correctly
- ☐ Virtual environment is activated

---

## 🐛 Common Issues

### "File not found"
**Problem**: PDF_PATH is wrong
**Solution**: 
- Use full path
- Check file exists
- Use forward slashes: `/` not `\`

### "Backend is not running"
**Solution**:
```powershell
# In separate terminal:
cd backend
.venv\Scripts\activate
python main.py
```

### "No module named 'requests'"
**Solution**:
```powershell
cd backend
.venv\Scripts\activate
pip install requests
```

---

## 🎉 Quick Start

### 1. Edit Variables
Open: `backend/simple_upload.py`

Change:
```python
PDF_PATH = "YOUR/PATH/TO/resumes.pdf"
JOB_TITLE = "Your Job Title"
REQUIRED_SKILLS = ["Skill1", "Skill2", "Skill3"]
```

### 2. Run
Double-click: `run_simple_upload.bat`

### 3. Done!
Results displayed automatically + saved to JSON file!

---

## 📞 Need Help?

- **This file**: Simple instructions
- **UPLOAD_GUIDE.md**: More detailed guide
- **README.md**: Full documentation

---

## 🌟 That's It!

**Just 2 steps:**
1. Edit variables in `simple_upload.py`
2. Run `run_simple_upload.bat`

**No command line arguments needed!**
**No parsing!**
**Just variables!**

🚀 **Happy shortlisting!**
