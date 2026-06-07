# 🚀 CareerMatch - AI Resume Analyzer

CareerMatch is a Flask-based web application that helps users analyze their resumes against specific career roles. The system extracts resume content from PDF files, compares user skills with industry-required skills, and generates a career readiness score.

---

## ✨ Features

- 📄 PDF Resume Upload
- 🔍 Automatic Resume Text Extraction
- 🎯 Role-Based Career Analysis
- 📊 Match Score Calculation
- ✅ Matched Skills Detection
- ❌ Missing Skills Identification
- 🚀 Career Readiness Status
- 🔎 Search and Filter Career Roles
- 📁 Secure File Upload Handling
- 🗑 Automatic File Cleanup
- 🎨 Interactive Multi-Step User Interface
- ⚡ Fast Resume Processing

---

## 🛠 Technologies Used

### Backend
- Python
- Flask
- Pandas
- PyMuPDF (fitz)

### Frontend
- HTML5
- CSS3
- JavaScript

### Database
- CSV Dataset (career.csv)

---

## 📂 Project Structure

```text
AI-Resume-Analyzer/
│
├── app.py
├── career.csv
│
├── static/
│   └── style.css
│
├── templates/
│   ├── index.html
│   └── result.html
│
├── uploads/
│
├── .gitignore
│
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/jamiMounika/AI-Resume-Analyzer.git
```

### Move into Project Folder

```bash
cd AI-Resume-Analyzer
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Required Packages

```bash
pip install flask pandas pymupdf
```

---

## ▶️ Run Application

```bash
python app.py
```

Open Browser:

```text
http://127.0.0.1:5000
```

---

## 🔄 How It Works

1. Upload Resume (PDF)
2. Select Target Career Role
3. System Extracts Resume Text
4. Required Skills are Loaded from Dataset
5. Skills are Compared with Resume Content
6. Match Score is Calculated
7. Missing Skills are Identified
8. Career Readiness Report is Generated

---

## 📈 Example Output

### Selected Role

Frontend Developer

### Match Score

60%

### Matched Skills

- HTML
- CSS
- JavaScript

### Missing Skills

- React
- Git

### Status

Partially Ready

---

## 🔒 Security Features

- File Type Validation
- Secure File Naming
- Maximum Upload Size Limit
- Automatic Temporary File Removal

---

## 👩‍💻 Author

**Jami Mounika**

B.Tech Computer Science Engineering

Sri Vasavi Engineering College

---

