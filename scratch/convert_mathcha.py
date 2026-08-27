import json
import os
import shutil

mathcha_dir = r"d:\Documents\USFX\MAT207\Texto Guia -Latex\MAT207-Differential-Equations\mathcha"
target_dir = r"d:\Documents\USFX\MAT207\Texto Guia -Latex\MAT207-Differential-Equations\latex"

mapping = {
    # Contenido 01-2025
    "20b41620-6a0d-4cd5-b240-0433b65d8c9e": r"Contenido 01-2025\04 - Ecuaciones Diferenciales de Orden Superior",
    "54e19f4a-eedc-45ed-afaf-fdb27217f460": r"Contenido 01-2025\01-Introduccion a las E.D.",
    "5d542d3d-bb73-4298-81a1-96d0dc1ce4b1": r"Contenido 01-2025\Modeling Problems for 2nd Order Differential Equations",
    "8981901e-d57c-4b2d-8c21-99f210f96bae": r"Contenido 01-2025\Problemas de Modelado",
    "d258b5ed-89d1-4688-a3c7-dc965fc5bf1d": r"Contenido 01-2025\Power of Series",
    "68d88c9b-d67b-488f-96bd-5f53b9e72be4": r"Contenido 01-2025\Cauchy Euler 01-2025",
    "170733fc-b49f-457b-bff0-443c85d4c9bf": r"Contenido 01-2025\Variacion de Parametros",
    "799e148f-7cce-4a71-808a-ec20c8eb3d94": r"Contenido 01-2025\E.D. Primer Orden Exactas",
    "5a59e11f-bdcd-4356-8c8d-9fa3e2aa4626": r"Contenido 01-2025\Contenido 02-2025",
    
    # Contenido 01-2026
    "6a59b895-4c92-4af4-859c-331c6e19e89f": r"Contenido 01-2026\Chap 01",
    "0f0a61a3-437a-4652-a355-cf3cb5d3e884": r"Contenido 01-2026\Chap 02 - First Order Differential Equations",
    
    # Contenido 02-2025
    "85eaef4a-a748-44f9-8f21-e7384aeff3ec": r"Contenido 02-2025\00 Clase Introductoria",
    "d3cdac7a-2d01-4b55-933b-c370ba00e680": r"Contenido 02-2025\01 Introduction to Differential Equations",
    "31a127bf-f1f3-4adf-9e27-db74b76f32c7": r"Contenido 02-2025\02-A-E.D. de Primer Orden-Clasificacion",
    "6d3652ff-8bcf-4512-9149-25d0e3bf611c": r"Contenido 02-2025\02-B-E.D. de Primer Orden - Variable Separable - Homogeneas",
    "d6bd6a6d-b645-4d4a-acb9-065ba5f18803": r"Contenido 02-2025\03 - Aplicaciones de Modelado para E.D. de Primer Orden",
    "90d8d228-3b7c-482b-9130-7ef2ad0cbd40": r"Contenido 02-2025\03-C-E.D. Lineales y de Bernoulli",
    "21892674-62bb-4cfd-8373-0447e6d77fe7": r"Contenido 02-2025\04-A Ecuaciones Diferenciales de Orden Superior - CC Homogeneas",
    "6b046d8f-6209-4447-9e3f-8a0346c1a84e": r"Contenido 02-2025\04-B Ecuaciones Diferenciales de Orden Superior - CC No Homogeneas",
    "6c627e89-a310-4897-ac20-b8be5c9c909d": r"Contenido 02-2025\04-C- Ecuaciones Diferenciales de Orden Superior - CC NO Homogeneas - Variacion de Parametros",
    "1ecae673-0043-431f-9499-1d2487b8990a": r"Contenido 02-2025\04-D- Ecuaciones Diferenciales Orden Superior - Cauchy Euler",
    "43df8be4-a45c-4180-b74b-f2e02cf737a2": r"Contenido 02-2025\04-D-E.D. Exactas y Factores de Integracion",
    "63a56c7d-c719-47ee-b2c6-316d4c069cef": r"Contenido 02-2025\06-A-Series de Potencia - Introduccion",
    
    # Contenido 02-2026
    "e39aaea1-f8b8-47fe-84f2-31186ca11e33": r"Contenido 02-2026\01-Introduccion a las Ecuaciones Diferenciales\01-Introduccion",
    "7c894871-7a79-416f-b3a4-8a6cb49c66ec": r"Contenido 02-2026\02 E.D. de Primer Orden\01-02-Introduccion y Tipos de E.D.",
    "8d050894-7004-481c-bcdf-9cde4afe6fa6": r"Contenido 02-2026\02 E.D. de Primer Orden\02-02-Variable Separable - Homogeneas",
    "72baa12f-cb85-4cc2-8f87-9cf380fb63c0": r"Contenido 02-2026\02 E.D. de Primer Orden\03-02-Lineal and Bernoulli",
    "c85f8253-7edb-4b13-8e4e-f06380707c28": r"Contenido 02-2026\02 E.D. de Primer Orden\04-02-Exactas y Factor de Integracion",
}

import re

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

if not os.path.exists(target_dir):
    os.makedirs(target_dir)

for root, dirs, files in os.walk(mathcha_dir):
    for file in files:
        if len(file) > 10:  # Check if it's a UUID style name
            src_path = os.path.join(root, file)
            
            # Determine mapping name
            rel_path = None
            for uuid, mapped in mapping.items():
                if file.startswith(uuid):
                    rel_path = mapped
                    break
                    
            if rel_path is None:
                # If not mapped, preserve original UUID name inside the target directory's subfolder
                rel_dir = os.path.relpath(root, mathcha_dir)
                rel_path = os.path.join(rel_dir, file)
            
            # See if it's JSON or binary
            is_json = False
            try:
                with open(src_path, 'r', encoding='utf-8') as f:
                    json.load(f)
                is_json = True
            except:
                is_json = False

            if is_json:
                dest_path = os.path.join(target_dir, rel_path + ".tex")
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                try:
                    tex_content = parse_mathcha(src_path)
                    with open(dest_path, 'w', encoding='utf-8') as f:
                        f.write(tex_content)
                    print(f"Converted {file} -> {dest_path}")
                except Exception as e:
                    print(f"Failed to convert {file}: {e}")
            else:
                dest_path = os.path.join(target_dir, rel_path + ".png")
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                try:
                    shutil.copy2(src_path, dest_path)
                    print(f"Copied binary {file} -> {dest_path}")
                except Exception as e:
                    print(f"Failed to copy binary {file}: {e}")
