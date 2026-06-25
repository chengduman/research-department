// GB/T 9704-2012 typst template for pandoc
#set page(
  paper: "a4",
  margin: (top: 37mm, bottom: 35mm, left: 28mm, right: 26mm),
  numbering: "1",
)

// Set CJK-capable fonts
#set text(
  font: ("SimFang", "FangSong", "仿宋", "Noto Serif CJK SC"),
  size: 16pt,
  lang: "zh",
)

// Headings
#set heading(numbering: "1.")
#show heading.where(level: 1): it => {
  set text(font: ("SimSun", "宋体", "Noto Serif CJK SC"), size: 22pt, weight: "bold")
  align(center, it)
}
#show heading.where(level: 2): it => {
  set text(font: ("SimHei", "黑体", "Noto Sans CJK SC"), size: 16pt)
  it
}
#show heading.where(level: 3): it => {
  set text(font: ("SimKai", "KaiTi", "楷体", "Noto Serif CJK SC"), size: 16pt, weight: "bold")
  it
}
#show heading.where(level: 4): it => {
  set text(font: ("SimFang", "FangSong", "仿宋"), size: 16pt, weight: "bold")
  it
}

// Paragraph indent
#set par(first-line-indent: 2em, spacing: 0pt, leading: 0.8em)

// Tables - full borders, auto columns
#show table: it => {
  set table(
    inset: (x: 5pt, y: 3pt),
    align: (x: left, y: top),
  )
  // Make all cells use smaller font
  show table.cell: set text(size: 10.5pt)
  // Header row styling
  show table.cell.where(y: 0): set text(
    font: ("SimHei", "黑体", "Noto Sans CJK SC"),
    weight: "bold",
    fill: rgb("#E8E8E8"),
  )
  it
}

// Code blocks
#show raw: set text(font: ("SimHei", "Courier New"), size: 9pt)
