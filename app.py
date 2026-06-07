import fitz
import os
import re
import pandas as pd
from flask import Flask, render_template, request, jsonify
 
app = Flask(__name__)
 
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)   # FIX 1: create folder if missing
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # FIX 2: 10 MB limit
 
# Read CSV
df = pd.read_csv("career.csv")
 
# Career Names — strip emoji/whitespace from column name
title_col = [c for c in df.columns if "Career" in c or "Job" in c][0]
career_list = df[title_col].dropna().str.strip().tolist()
 
 
def extract_text_from_pdf(pdf_path):
    """Extract all text from a PDF file."""
    text = ""
    try:
        pdf = fitz.open(pdf_path)
        for page in pdf:
            text += page.get_text()
        pdf.close()
    except Exception as e:
        print(f"PDF extraction error: {e}")
    return text
 
 
def get_skills_for_career(selected_role):
    """Return list of cleaned skills for the given career title."""
    # FIX 3: robust column matching for multi-line CSV headers
    skill_col = [c for c in df.columns if "Hard" in c or "Technical" in c][0]
 
    career_row = df[df[title_col].str.strip() == selected_role.strip()]
    if career_row.empty:
        return []
 
    skills_text = str(career_row.iloc[0][skill_col])
 
    # FIX 4: smarter skill splitting — handles "(x/y)" grouped items
    # Split on commas that are NOT inside parentheses
    skills = re.split(r',\s*(?![^()]*\))', skills_text)
    return [s.strip() for s in skills if s.strip() and s.strip().lower() != "nan"]
 
 
def match_skills(resume_text, required_skills):
    """
    FIX 5: smarter matching — tokenise each skill and check all tokens present.
    e.g. 'React/Vue/Angular' is matched if any variant appears in the resume.
    """
    resume_lower = resume_text.lower()
    matched = []
    missing = []
 
    for skill in required_skills:
        # Split compound skills like "Python/R" or "TensorFlow/PyTorch" into variants
        variants = re.split(r'[/|]', skill)
        # Also consider the full skill phrase as one variant
        variants.append(skill)
 
        found = False
        for variant in variants:
            # Clean punctuation from variant for matching
            clean = re.sub(r'[().,]', ' ', variant).strip().lower()
            # Match as a whole word or phrase
            if clean and re.search(r'\b' + re.escape(clean) + r'\b', resume_lower):
                found = True
                break
 
        if found:
            matched.append(skill.title())
        else:
            missing.append(skill.title())
 
    return matched, missing
 
 
@app.route('/')
def home():
    return render_template("index.html", careers=career_list)
 
 
@app.route('/upload', methods=['POST'])
def upload():
    # FIX 6: validate inputs before processing
    if 'resume' not in request.files:
        return "No file uploaded", 400
 
    file = request.files['resume']
    selected_role = request.form.get('role', '').strip()
 
    if not file or file.filename == '':
        return "No file selected", 400
    if not selected_role:
        return "No role selected", 400
    if not file.filename.lower().endswith('.pdf'):
        return "Only PDF files are supported", 400
 
    # FIX 7: secure the filename
    from werkzeug.utils import secure_filename
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
 
    resume_text = extract_text_from_pdf(filepath)
 
    required_skills = get_skills_for_career(selected_role)
 
    if not required_skills:
        return f"Career '{selected_role}' not found in database", 404
 
    matched, missing = match_skills(resume_text, required_skills)
 
    total = len(required_skills)
    # FIX 8: guard against division by zero
    score = int(len(matched) / total * 100) if total > 0 else 0
 
    if score >= 80:
        status = "Ready for this Career"
    elif score >= 50:
        status = "Partially Ready"
    else:
        status = "Need More Skills"
 
    # FIX 9: clean up uploaded file after processing
    try:
        os.remove(filepath)
    except Exception:
        pass
 
    return render_template(
        "result.html",
        role=selected_role,
        score=score,
        status=status,
        matched=matched,
        missing=missing,
    )
 
 
if __name__ == '__main__':
    app.run(debug=True)
 