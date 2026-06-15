import re

with open("C:\\Users\\cheng\\research-department\\PEN_V22_主报告_合并V2.2.md", "r", encoding="utf-8") as f:
    text = f.read()

# Fix all unescaped @ in table rows that are followed by digits or letters
# Replace @ with \\@ to prevent pandoc from treating as citation
lines = text.split('\n')
fixed_lines = []
for line in lines:
    s = line.strip()
    if s.startswith('|') and '@' in s:
        # Escape @ in table cells (but not already escaped ones)
        # Pattern: @ followed by digit or letter (like @10GHz, @1MHz, @BTNR)
        s = re.sub(r'(?<!\|)@([a-zA-Z0-9])', r'\\@\1', s)
        # Restore original indentation
        orig_indent = line[:len(line) - len(line.lstrip())]
        line = orig_indent + s
    fixed_lines.append(line)

text = '\n'.join(fixed_lines)

# Verify
issues = []
for i, line in enumerate(text.split('\n'), 1):
    s = line.strip()
    if s.startswith('|') and '@' in s:
        if re.search(r'(?<!\|)@(?!\s)', s) and '\\@' not in s:
            issues.append(f"L{i}: {s[:100]}")

if issues:
    print("Remaining unescaped @ in tables:")
    for iss in issues:
        print(f"  {iss}")
else:
    print("All @ signs properly escaped!")

with open("C:\\Users\\cheng\\research-department\\PEN_V22_主报告_合并V2.2.md", "w", encoding="utf-8") as f:
    f.write(text)

print(f"Done: {len(text)} chars")
