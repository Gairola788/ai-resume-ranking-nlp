from parser import extract_text

with open("your_resume.pdf", "rb") as f:
    text = extract_text(f.read(), "your_resume.pdf")
    print(text[:500])  