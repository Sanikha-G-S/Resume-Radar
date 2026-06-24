import pdfplumber

with pdfplumber.open("sample_resume.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)