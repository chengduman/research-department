#!/usr/bin/env python3
"""Fix formatting issues in the merged PEN report."""
import re

OUTPUT_PATH = r'C:\Users\cheng\research-department\PEN_V22_主报告_合并V2.2.md'

with open(OUTPUT_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix double --- lines (from section boundary + insertion boundary)
content = re.sub(r'---\s*\n\s*---', '---', content)

# 2. Fix sub-headers in §5.6 that have emoji-replaced text like "#### [3D打印] 4) 3D打印/增材制造"
# These should become "#### 4) 3D打印/增材制造"
content = re.sub(r'#### \[(航空航天|储能|机器人|3D打印|通信|涂层)\]\s*(\d+)\)', r'#### \2)', content)

# 3. Fix section numbering inside §5.6 - "### 4.1" etc. should become "#### 4.1" (one level deeper)
# Actually these are sub-sections within 5.6, so they should use ####
# But looking at the output, the headers are #### already, so this is fine

# 4. Remove blank lines inside tables more aggressively
lines = content.split('\n')
result = []
in_table = False
for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped.startswith('|') and stripped.endswith('|'):
        in_table = True
        result.append(line)
    elif stripped == '|------|-------|------|--------|------|---------|' or \
         stripped == '|------|------|--------|------|' or \
         stripped.startswith('|---') and stripped.endswith('---') and in_table:
        # Table separator lines
        result.append(line)
    elif in_table and stripped == '':
        # Skip blank lines inside tables
        continue
    elif in_table and not (stripped.startswith('|') or stripped.startswith('|---')):
        in_table = False
        result.append(line)
    else:
        if in_table and not (stripped.startswith('|') or stripped.startswith('|---')):
            in_table = False
        result.append(line)

content = '\n'.join(result)

# 5. Clean up excess blank lines (keep max 2)
content = re.sub(r'\n{3,}', '\n\n', content)

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("Formatting fixes applied successfully.")
print(f"Output file: {OUTPUT_PATH}")

# Count lines
with open(OUTPUT_PATH, 'r', encoding='utf-8') as f:
    final_lines = f.readlines()
print(f"Final file: {len(final_lines)} lines")
