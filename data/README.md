# Data Folder - Resume PDFs

## 📂 Purpose

This folder is for storing your resume PDF files that contain multiple resumes (one resume per page).

## 📥 How to Use

1. **Place your PDF files here**
   - Example: `resumes.pdf`, `candidates_2024.pdf`, etc.

2. **Run the upload script**
   - Double-click `quick_upload.bat` in the root folder
   - Or use command line: `python upload_and_process.py --pdf "your_file.pdf"`

3. **The script will automatically find your PDF**
   - No need to specify full path
   - Just use the filename!

## ✅ Supported Format

- **File Type**: PDF only
- **Structure**: One resume per page
- **Text**: Must be text-based (not scanned images)
- **Size**: No strict limit (but smaller files process faster)

## 📝 Example Files

```
data/
├── software_engineer_resumes.pdf
├── data_scientist_candidates.pdf
├── frontend_developer_resumes.pdf
└── ml_engineer_applicants.pdf
```

## 🚀 Quick Usage

### Method 1: Double-Click Upload
```
1. Put your PDF here (e.g., resumes.pdf)
2. Go to root folder
3. Double-click quick_upload.bat
4. Enter filename: resumes.pdf
5. Done!
```

### Method 2: Command Line
```powershell
cd backend
.venv\Scripts\activate
python upload_and_process.py --pdf "resumes.pdf" --job-title "Developer"
```

### Method 3: With Full Options
```powershell
python upload_and_process.py --pdf "resumes.pdf" ^
    --job-title "Senior Python Developer" ^
    --skills "Python,Django,React" ^
    --experience 5
```

## 📊 What Happens

1. Script reads PDF from this folder
2. Extracts each page as individual resume
3. Parses name, email, skills, experience
4. Runs two-phase shortlisting
5. Shows results with confidence scores

## 💡 Tips

- Use descriptive filenames
- One resume per page works best
- Ensure PDFs are not password-protected
- Text-based PDFs work better than scans
- Keep originals backed up elsewhere

## 🔗 Need Help?

See: **UPLOAD_GUIDE.md** in the root folder for complete instructions!
