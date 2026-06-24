import pdfplumber

SKILLS_DB = [
    "python",
    "java",
    "c",
    "c++",
    "html",
    "css",
    "sql",
    "dbms",
    "data structures",
    "algorithms",
    "oop",
    "linux",
    "ubuntu",
    "oracle",
    "web development"
]

with pdfplumber.open("sample_resume.pdf") as pdf:
    text = ""

    for page in pdf.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text.lower()

found_skills = []

for skill in SKILLS_DB:
    if skill.lower() in text:
        found_skills.append(skill)

print("Skills Found:")
print(found_skills)