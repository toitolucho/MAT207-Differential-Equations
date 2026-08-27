import json
import os
import shutil
import re
import argparse

def is_prose(text):
    if not isinstance(text, str): return False
    if (len(text) >= 5 or " " in text.strip()) and re.search(r'[a-zA-Z]{2,}', text):
        if not any(char in text for char in ['=', '+', '-', '<', '>', '/', '^', '_', '\\', '(', ')']):
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
            # Replace unsupported unicode chars
            text = text.replace("∂", "\\partial " if is_math else "$\\partial$ ")
            text = text.replace("⟹", "\\implies " if is_math else "$\\implies$ ")
            text = text.replace("→", "\\rightarrow " if is_math else "$\\rightarrow$ ")
            if is_math and is_prose(text):
                text = f"\\text{{{text}}}"
        elif block["type"] == "single":
            text = block.get("text", "")
        elif block["type"] == "composite":
            comp_text = block.get("text", "")
            elements = block.get("elements", {})
            if comp_text == "\\math-container":
                lines = elements.get("mathValue", {}).get("lines", [])
                text = "\n\\begin{gather*}\n" + parse_lines(lines, True) + "\\end{gather*}\n"
            elif comp_text == "\\frac":
                val = parse_lines(elements.get("value", {}).get("lines", []), True).strip('\n ')
                sub1 = parse_lines(elements.get("sub1", {}).get("lines", []), True).strip('\n ')
                text = f"\\frac{{{val}}}{{{sub1}}}"
                if not is_math: text = f"${text}$"
            elif comp_text == "\\power":
                power = parse_lines(elements.get("powerValue", {}).get("lines", []), True).strip('\n ')
                text = f"^{{{power}}}"
                if not is_math: text = f"${text}$"
            elif comp_text == "\\index":
                idx = parse_lines(elements.get("indexValue", {}).get("lines", []), True).strip('\n ')
                text = f"_{{{idx}}}"
                if not is_math: text = f"${text}$"
            elif comp_text == "\\int":
                text = "\\int " if is_math else "$\\int$"
            elif comp_text == "\\rightarrow":
                text = " \\rightarrow " if is_math else " $\\rightarrow$ "
            elif comp_text == "\\sqrt":
                val = parse_lines(elements.get("value", {}).get("lines", []), True).strip('\n ')
                text = f"\\sqrt{{{val}}}"
                if not is_math: text = f"${text}$"
            else:
                text = comp_text
                for k, v in elements.items():
                    if isinstance(v, dict) and "lines" in v:
                        text += "{" + parse_lines(v["lines"], is_math).strip('\n ') + "}"
        
        if is_bold:
            if is_math:
                text = f"\\mathbf{{{text}}}"
            else:
                text = f"\\textbf{{{text}}}"
                
        if bg_color:
            r, g, b = bg_color[0], bg_color[1], bg_color[2]
            if is_math:
                text = f"\\text{{\\colorbox[RGB]{{{r},{g},{b}}}{{${text}$}}}}"
            else:
                text = f"\\colorbox[RGB]{{{r},{g},{b}}}{{{text}}}"
                
        result += text
    return result

def parse_lines(lines, is_math=False):
    result = ""
    # filter out trailing empty lines to avoid blank lines at the end of gather*
    if is_math:
        while lines and (not lines[-1].get("blocks") or all(b.get("type") == "text" and not b.get("text", "").strip() for b in lines[-1].get("blocks", []))):
            lines.pop()
            
    for i, line in enumerate(lines):
        if "blocks" in line:
            line_str = parse_blocks(line["blocks"], is_math)
            if is_math:
                # If a line is empty, just output a small vertical space instead of a blank line
                if not line_str.strip():
                    result += "\\vspace{0.5em} \\\\" + ("\n" if i < len(lines)-1 else "")
                else:
                    result += line_str + (" \\\\" if i < len(lines)-1 else "") + "\n"
            else:
                result += line_str + "\n\n"
    
    # Remove any completely blank lines from math result
    if is_math:
        result = "\n".join([line for line in result.split("\n") if line.strip() != ""]) + "\n"
        
    return result

def parse_mathcha(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    result = "\\documentclass{article}\n\\usepackage{amsmath}\n\\usepackage{xcolor}\n\\begin{document}\n\n"
    if "lines" in data:
        result += parse_lines(data["lines"]) + "\n"
    result += "\\end{document}\n"
    return result

def main():
    parser = argparse.ArgumentParser(description="Convert Mathcha exported files to LaTeX.")
    parser.add_argument("--input", required=True, help="Input directory containing mathcha files")
    parser.add_argument("--output", required=True, help="Output directory for LaTeX files")
    parser.add_argument("--mapping", help="Optional JSON file mapping UUIDs to readable relative paths (without extension)")
    args = parser.parse_args()

    mapping = {}
    if args.mapping and os.path.exists(args.mapping):
        with open(args.mapping, 'r', encoding='utf-8') as f:
            mapping = json.load(f)

    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    for root, dirs, files in os.walk(args.input):
        for file in files:
            src_path = os.path.join(root, file)
            
            rel_path = None
            if mapping:
                for uuid, mapped in mapping.items():
                    if file.startswith(uuid):
                        rel_path = mapped
                        break
                        
            if rel_path is None:
                rel_dir = os.path.relpath(root, args.input)
                rel_path = os.path.join(rel_dir, file)
                
            # Check if JSON
            is_json = False
            try:
                with open(src_path, 'r', encoding='utf-8') as f:
                    json.load(f)
                is_json = True
            except:
                is_json = False

            if is_json:
                dest_path = os.path.join(args.output, rel_path + ".tex")
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                try:
                    tex_content = parse_mathcha(src_path)
                    with open(dest_path, 'w', encoding='utf-8') as f:
                        f.write(tex_content)
                    print(f"Converted {file} -> {dest_path}")
                except Exception as e:
                    print(f"Failed to convert {file}: {e}")
            else:
                dest_path = os.path.join(args.output, rel_path + ".png")
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                try:
                    shutil.copy2(src_path, dest_path)
                    print(f"Copied binary {file} -> {dest_path}")
                except Exception as e:
                    print(f"Failed to copy binary {file}: {e}")

if __name__ == "__main__":
    main()
