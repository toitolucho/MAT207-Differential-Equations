import json
import re

def is_prose(text):
    if not isinstance(text, str): return False
    if re.search(r'[a-zA-Z]{2,}', text) and " " in text.strip():
        if not any(char in text for char in ['=', '+', '-', '<', '>', '/', '^', '_', '\\']):
            return True
    return False

def parse_blocks(blocks, is_math=False):
    result = ""
    for block in blocks:
        style = block.get("style", {})
        is_bold = style and style.get("isBold", False)
        bg_color = style and style.get("bgColor", None)
        
        text = ""
        if "type" not in block or block["type"] == "text":
            text = block.get("text", "")
            if is_math and is_prose(text):
                text = f"\\text{{{text}}}"
        elif block["type"] == "single":
            text = block.get("text", "")
        elif block["type"] == "composite":
            comp_text = block.get("text", "")
            elements = block.get("elements", {})
            if comp_text == "\\math-container":
                lines = elements.get("mathValue", {}).get("lines", [])
                text = "\n\\begin{gather*}\n" + parse_lines(lines, True) + "\n\\end{gather*}\n"
            elif comp_text == "\\frac":
                val = parse_lines(elements.get("value", {}).get("lines", []), is_math).strip('\n \\')
                sub1 = parse_lines(elements.get("sub1", {}).get("lines", []), is_math).strip('\n \\')
                text = f"\\frac{{{val}}}{{{sub1}}}"
            elif comp_text == "\\power":
                power = parse_lines(elements.get("powerValue", {}).get("lines", []), is_math).strip('\n \\')
                text = f"^{{{power}}}"
            elif comp_text == "\\index":
                idx = parse_lines(elements.get("indexValue", {}).get("lines", []), is_math).strip('\n \\')
                text = f"_{{{idx}}}"
            elif comp_text == "\\int":
                text = "\\int "
            elif comp_text == "\\rightarrow":
                text = " \\rightarrow "
            elif comp_text == "\\sqrt":
                val = parse_lines(elements.get("value", {}).get("lines", []), is_math).strip('\n \\')
                text = f"\\sqrt{{{val}}}"
            else:
                text = comp_text
                for k, v in elements.items():
                    if isinstance(v, dict) and "lines" in v:
                        text += "{" + parse_lines(v["lines"], is_math).strip('\n \\') + "}"
        
        if is_bold:
            if is_math:
                text = f"\\mathbf{{{text}}}"
            else:
                text = f"\\textbf{{{text}}}"
                
        if bg_color:
            r, g, b = bg_color[0], bg_color[1], bg_color[2]
            if is_math:
                text = f"\\colorbox[RGB]{{{r},{g},{b}}}{{${text}$}}"
            else:
                text = f"\\colorbox[RGB]{{{r},{g},{b}}}{{{text}}}"
                
        result += text
    return result

def parse_lines(lines, is_math=False):
    result = ""
    for i, line in enumerate(lines):
        if "blocks" in line:
            line_str = parse_blocks(line["blocks"], is_math)
            if is_math:
                result += line_str + (" \\\\" if i < len(lines)-1 else "") + "\n"
            else:
                result += line_str + "\n\n"
    return result

def parse_mathcha(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    result = "\\documentclass{article}\n\\usepackage{amsmath}\n\\usepackage{xcolor}\n\\begin{document}\n\n"
    if "lines" in data:
        result += parse_lines(data["lines"]) + "\n"
    result += "\\end{document}\n"
    return result

with open('test_output.tex', 'w', encoding='utf-8') as f:
    f.write(parse_mathcha(r"d:\Documents\USFX\MAT207\Texto Guia -Latex\MAT207-Differential-Equations\mathcha\Contenido 02-2026\e39aaea1-f8b8-47fe-84f2-31186ca11e33"))
