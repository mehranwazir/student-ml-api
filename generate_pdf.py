import markdown
import subprocess
import os
import shutil

def build_pdf():
    md_file = os.path.join(os.path.dirname(__file__), "SUBMISSION_REPORT.md")
    html_file = os.path.join(os.path.dirname(__file__), "report.html")
    pdf_file_primary = os.path.join(os.path.dirname(__file__), "MLOps_Assignment_1_Mehran_Hamayoon_22i-0810.pdf")
    pdf_file_secondary = os.path.join(os.path.dirname(__file__), "SUBMISSION_REPORT.pdf")

    with open(md_file, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Convert markdown to html
    html_body = markdown.markdown(
        md_content,
        extensions=["tables", "fenced_code", "toc"]
    )

    # CSS for high-quality printing
    css = """
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Fira+Code:wght@400;500&display=swap');

    @page {
        size: A4;
        margin: 20mm 18mm 20mm 18mm;
        @bottom-right {
            content: counter(page);
        }
    }

    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        color: #1f2937;
        line-height: 1.6;
        font-size: 13.5px;
        background-color: #ffffff;
    }

    h1 {
        font-size: 24px;
        color: #111827;
        border-bottom: 2px solid #2563eb;
        padding-bottom: 8px;
        margin-top: 0;
        margin-bottom: 16px;
        page-break-after: avoid;
    }

    h2 {
        font-size: 18px;
        color: #1e40af;
        border-bottom: 1px solid #e5e7eb;
        padding-bottom: 6px;
        margin-top: 24px;
        margin-bottom: 12px;
        page-break-after: avoid;
    }

    h3 {
        font-size: 15px;
        color: #374151;
        margin-top: 18px;
        margin-bottom: 8px;
        page-break-after: avoid;
    }

    p, ul, ol {
        margin-top: 6px;
        margin-bottom: 12px;
    }

    li {
        margin-bottom: 4px;
    }

    blockquote {
        background: #f0fdf4;
        border-left: 4px solid #16a34a;
        margin: 16px 0;
        padding: 12px 16px;
        color: #166534;
        border-radius: 0 6px 6px 0;
    }

    code {
        font-family: 'Fira Code', Consolas, Monaco, 'Courier New', monospace;
        font-size: 12px;
        background-color: #f3f4f6;
        color: #b91c1c;
        padding: 2px 5px;
        border-radius: 4px;
    }

    pre {
        background-color: #1e293b;
        color: #f8fafc;
        padding: 14px 16px;
        border-radius: 8px;
        overflow-x: auto;
        font-family: 'Fira Code', Consolas, Monaco, 'Courier New', monospace;
        font-size: 11.5px;
        line-height: 1.5;
        page-break-inside: avoid;
        margin: 12px 0 16px 0;
    }

    pre code {
        background-color: transparent;
        color: #f8fafc;
        padding: 0;
        border-radius: 0;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        margin: 16px 0;
        font-size: 12.5px;
        page-break-inside: avoid;
    }

    th, td {
        border: 1px solid #e2e8f0;
        padding: 8px 12px;
        text-align: left;
    }

    th {
        background-color: #f8fafc;
        font-weight: 600;
        color: #0f172a;
    }

    tr:nth-child(even) {
        background-color: #fcfcfd;
    }

    hr {
        border: none;
        border-top: 1px solid #e5e7eb;
        margin: 24px 0;
    }

    a {
        color: #2563eb;
        text-decoration: none;
    }
    """

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>MLOps Assignment 1 Report - Mehran Hamayoon (22i-0810)</title>
<style>{css}</style>
</head>
<body>
{html_body}
</body>
</html>
"""

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(full_html)

    # Find Chrome or Edge
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    browser = chrome_path if os.path.exists(chrome_path) else edge_path

    cmd = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_file_primary}",
        html_file
    ]

    print(f"Generating PDF with: {browser}")
    subprocess.run(cmd, check=True)

    # Create secondary copy with standard name
    shutil.copyfile(pdf_file_primary, pdf_file_secondary)
    print(f"PDF created successfully:\n1. {pdf_file_primary}\n2. {pdf_file_secondary}")

if __name__ == "__main__":
    build_pdf()
