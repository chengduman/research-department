#!/usr/bin/env python3
"""Merge PEN V2.2 competitive intelligence supplement into the main PEN report."""

SUPP_PATH = r'C:\Users\cheng\research-department\PEN_V22_竞争情报补强.md'
MAIN_PATH = r'C:\Users\cheng\中普咨询\项目文档\2024-聚芳醚腈产业调研\02-聚芳醚腈PEN产业调研报告.md'
OUTPUT_PATH = r'C:\Users\cheng\research-department\PEN_V22_主报告_合并V2.2.md'

# ── Read both files ──
with open(MAIN_PATH, 'r', encoding='utf-8') as f:
    main_lines = f.readlines()

with open(SUPP_PATH, 'r', encoding='utf-8') as f:
    supp_lines = f.readlines()

# ── Extract supplement sections ──

def extract_section(lines, start_marker, end_marker=None):
    """Extract lines between markers (inclusive start, exclusive end)."""
    start_idx = None
    end_idx = len(lines)
    for i, line in enumerate(lines):
        if start_marker in line and start_idx is None:
            start_idx = i
        elif end_marker and end_marker in line and start_idx is not None and end_idx == len(lines):
            end_idx = i
            break
    if start_idx is not None:
        # Remove leading blank lines from section
        real_start = start_idx
        while real_start < len(lines) and lines[real_start].strip() == '':
            real_start += 1
        # If end_marker is None, go to end of file minus trailing blank lines
        if end_marker is None:
            real_end = len(lines)
            while real_end > real_start and lines[real_end-1].strip() == '':
                real_end -= 1
        else:
            real_end = end_idx
        # Remove section header/separator lines
        result = lines[real_start:real_end]
        # Remove any leading --- or > lines from the result
        while result and (result[0].strip().startswith('---') or result[0].strip().startswith('>')):
            result = result[1:]
        return ''.join(result)
    return ''

# Extract section 1: International Patents (lines 9-75 in supplement)
sec1_patents = extract_section(supp_lines, '## 一、PEN在航空航天领域的国际专利', '## 二、')

# Extract section 2: Bidding info (lines 78-113)
sec2_bidding = extract_section(supp_lines, '## 二、PEN相关招标采购信息', '## 三、')

# Extract section 3: Market competition (lines 117-187)
sec3_comp = extract_section(supp_lines, '## 三、最新市场竞争动态', '## 四、')

# Extract section 4: New applications (lines 190-271)
sec4_apps = extract_section(supp_lines, '## 四、新的应用领域突破', '## 五、')

# Extract section 5: Summary (lines 275-313)
sec5_summary = extract_section(supp_lines, '## 五、关键情报总结与建议')

# ── Find insertion points in main report ──

# Find exact line numbers for insertion points
def find_line(lines, pattern, start_from=0):
    for i, line in enumerate(lines):
        if i >= start_from and pattern in line:
            return i
    return -1

# 1. End of §2 (after the --- at end of section 2, before §3)
# Line ~300 is `|---`
end_s2 = find_line(main_lines, '## 3. 生产工艺与原料供应链')
# Go back to find the --- before it
for i in range(end_s2, -1, -1):
    if main_lines[i].strip() == '---':
        end_s2_insert = i
        break
else:
    end_s2_insert = end_s2

# 2. End of §4 (after line ~845, the --- before §5)
start_s5 = find_line(main_lines, '## 5. 需求端深度分析')
for i in range(start_s5, -1, -1):
    if main_lines[i].strip() == '---':
        end_s4_insert = i
        break
else:
    end_s4_insert = start_s5

# 3. End of §5 (after line ~1205, the --- before §6)
start_s6 = find_line(main_lines, '## 6. 竞争格局与情报')
for i in range(start_s6, -1, -1):
    if main_lines[i].strip() == '---':
        end_s5_insert = i
        break
else:
    end_s5_insert = start_s6

# 4. End of §6 (after line ~1503, the --- before §7)
start_s7 = find_line(main_lines, '## 7. 产业链结构与价值分布')
for i in range(start_s7, -1, -1):
    if main_lines[i].strip() == '---':
        end_s6_insert = i
        break
else:
    end_s6_insert = start_s7

print(f"Insertion points:")
print(f"  §2 end: line {end_s2_insert} ('{main_lines[end_s2_insert].strip()}')")
print(f"  §4 end: line {end_s4_insert} ('{main_lines[end_s4_insert].strip()}')")
print(f"  §5 end: line {end_s5_insert} ('{main_lines[end_s5_insert].strip()}')")
print(f"  §6 end: line {end_s6_insert} ('{main_lines[end_s6_insert].strip()}')")

# ── Build the merged content ──

# Helper to clean emoji and fix E notation
def clean_text(text):
    """Replace emoji with text equivalents and fix formatting."""
    replacements = {
        '⚠️': '[注意]',
        '🚀': '[航空航天]',
        '🔬': '[储能]',
        '🤖': '[机器人]',
        '🖨': '[3D打印]',
        '📡': '[通信]',
        '🛡': '[涂层]',
        '✅': '[已商用]',
        '🧪': '[研发中]',
    }
    for emoji, text_repl in replacements.items():
        text = text.replace(emoji, text_repl)
    # Fix E notation in tables - replace "E" followed by digits at end of cells
    # This handles things like "2026E"
    return text

def clean_table_blank_lines(text):
    """Remove blank lines inside markdown tables."""
    lines = text.split('\n')
    result = []
    in_table = False
    for line in lines:
        stripped = line.strip()
        if stripped == '' and in_table:
            # Check if next line is also table-related
            continue
        if stripped.startswith('|') and stripped.endswith('|'):
            in_table = True
            result.append(line)
        elif stripped == '---' and in_table:
            # This is the separator line inside a table
            result.append(line)
        elif in_table and not (stripped.startswith('|') or stripped.startswith('---')):
            in_table = False
            result.append(line)
        else:
            result.append(line)
    return '\n'.join(result)

def ensure_newline(text):
    """Make sure text ends with exactly one newline."""
    text = text.rstrip('\n')
    return text + '\n\n'

# ── §2.6: International Patent Landscape ──
patent_insert = f"""
### 2.6 国际专利格局 [CI补强]

> 数据来源：专利数据库检索（2026-06-11），覆盖中国、美国、日本、欧洲近5年公开专利

{clean_text(sec1_patents).strip()}

"""

# ── §4.6: Bidding Analysis ──
bidding_insert = f"""
### 4.6 招标采购分析 [CI补强]

> 数据来源：全军武器装备采购信息网、航空工业电子采购平台、阳光七采、剑鱼标讯等公开招标平台检索（2026-06-11）

{clean_text(sec2_bidding).strip()}

"""

# ── §5.6: New Application Breakthroughs ──
apps_insert = f"""
### 5.6 新兴应用领域突破（2024-2026）[CI补强]

> 数据来源：学术期刊（Polymers、Adv. Funct. Mater.、J. Membrane Sci.、Nano Research等）及企业公告（2024-2026）

以下内容为V2.2补充的最新应用领域突破数据，涵盖航空航天、新型储能、机器人、3D打印、5G/6G通信及防腐涂层六大方向。

{clean_text(sec4_apps).strip()}

"""

# ── §6.7: Updated Market Competition (2025-2026) ──
comp_insert = f"""
### 6.7 市场竞争动态更新（2025-2026）[CI补强]

> 数据来源：24MarketReports、PW Consulting、QY Research、智研咨询、DataInsightsMarket（2025-2026年报告）

以下为V2.2补充的最新全球及中国PEN市场数据、竞争格局更新及近期重要事件。

{clean_text(sec3_comp).strip()}

"""

# ── §6.8: Summary (integrated from §五) ──
summary_insert = f"""
### 6.8 关键情报总结与建议 [CI补强]

{clean_text(sec5_summary).strip()}

"""

# ── Build the merged file ──

# Split main content at insertion points
part1 = ''.join(main_lines[:end_s2_insert+1])
part2 = ''.join(main_lines[end_s2_insert+1:end_s4_insert+1])
part3 = ''.join(main_lines[end_s4_insert+1:end_s5_insert+1])
part4 = ''.join(main_lines[end_s5_insert+1:end_s6_insert+1])
part5 = ''.join(main_lines[end_s6_insert+1:])

merged = part1 + patent_insert + '---\n\n' + part2 + bidding_insert + '---\n\n' + part3 + apps_insert + part4 + comp_insert + summary_insert + part5

# ── Fix formatting issues ──

# 1. Remove blank lines inside markdown tables
merged = clean_table_blank_lines(merged)

# 2. Replace emoji with text equivalents
merged = clean_text(merged)

# 3. Fix E notation in table content (replace "E)" with "E)" but keep as is - these are column values like "2026E"
# Already handled by clean_text if needed

# 4. Remove double or more blank lines (keep max 2 consecutive blank lines)
import re
merged = re.sub(r'\n{3,}', '\n\n', merged)

# ── Write output ──
with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write(merged)

# ── Stats ──
orig_main_len = len(''.join(main_lines))
orig_supp_len = len(''.join(supp_lines))
new_len = len(merged)
added = new_len - orig_main_len

print(f"\nMerge complete!")
print(f"  Original main report: {orig_main_len} chars, ~{len(main_lines)} lines")
print(f"  Supplement: {orig_supp_len} chars, ~{len(supp_lines)} lines")
print(f"  Merged output: {new_len} chars")
print(f"  Added: {added} chars")
print(f"  Output: {OUTPUT_PATH}")
print(f"  Insertions made:")
print(f"    §2.6 国际专利格局 (after line {end_s2_insert})")
print(f"    §4.6 招标采购分析 (after line {end_s4_insert})")
print(f"    §5.6 新兴应用领域突破 (after line {end_s5_insert})")
print(f"    §6.7 市场竞争动态更新 (after line {end_s6_insert})")
print(f"    §6.8 关键情报总结与建议 (after line {end_s6_insert})")
