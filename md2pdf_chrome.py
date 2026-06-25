#!/usr/bin/env python3
"""Convert markdown to professional PDF via pandoc + Chrome headless."""
import subprocess, tempfile, os, sys

MD = sys.argv[1] if len(sys.argv) > 1 else "个人闲置算力出租市场调研报告.md"
OUT = os.path.splitext(MD)[0] + ".pdf"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
BROWSER = CHROME if os.path.exists(CHROME) else EDGE

CSS = """
@page { size: A4; margin: 37mm 26mm 35mm 28mm; }
body {
  font-family: 'FangSong', '仿宋', 'SimFang', 'FangSong_GB2312', 'STFangsong', serif;
  font-size: 16pt; line-height: 28pt; color: #000;
}
h1 { font-family: 'SimSun','宋体',serif; font-size: 22pt; font-weight: bold; text-align: center; page-break-before: always; }
h2 { font-family: 'SimHei','黑体',sans-serif; font-size: 16pt; font-weight: normal; margin-top: 12pt; }
h3 { font-family: 'KaiTi','楷体',serif; font-size: 16pt; font-weight: bold; margin-top: 8pt; }
h4 { font-family: 'FangSong','仿宋',serif; font-size: 16pt; font-weight: bold; }
p { margin: 0; text-indent: 2em; text-align: justify; }
p:first-of-type, h2+p, h3+p, h4+p { text-indent: 0; }
table { font-size: 10.5pt; line-height: 16pt; border-collapse: collapse; width: 100%; margin: 8pt 0; }
th { font-family: 'SimHei','黑体',sans-serif; font-weight: bold; background: #E8E8E8; border: 0.5pt solid #000; padding: 3pt 5pt; }
td { font-family: 'FangSong','仿宋',serif; border: 0.5pt solid #000; padding: 2pt 5pt; }
pre, code { font-family: 'SimHei','黑体','Courier New',monospace; font-size: 9pt; background: #f5f5f5; padding: 4pt; white-space: pre-wrap; text-indent: 0; }
hr { border: 0.5pt solid #ccc; margin: 12pt 0; }
strong { font-weight: bold; }
ul, ol { padding-left: 2em; }
.pagebreak { page-break-before: always; }
"""

# Step 1: Pandoc to HTML with embedded CSS
print("[1/2] Converting markdown to HTML...")
html_body = subprocess.run([
    "pandoc", MD, "-f", "markdown+pipe_tables", "-t", "html5",
    "--metadata", "lang=zh-CN"
], capture_output=True, text=True, check=True).stdout

html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="utf-8"><style>{CSS}</style></head>
<body>{html_body}</body>
</html>"""

with tempfile.NamedTemporaryFile(suffix=".html", mode="w", encoding="utf-8", delete=False) as f:
    f.write(html)
    html_path = f.name

# Step 2: Chrome headless to PDF
print(f"[2/2] Rendering PDF via Chrome...")
subprocess.run([
    BROWSER, "--headless", "--disable-gpu", "--no-sandbox",
    "--no-pdf-header-footer",
    f"--print-to-pdf={os.path.abspath(OUT)}",
    f"file:///{html_path.replace(os.sep, '/')}"
], check=True, timeout=60)

os.unlink(html_path)
size_kb = os.path.getsize(OUT) / 1024
print(f"✅ PDF: {OUT} ({size_kb:.0f} KB)")
