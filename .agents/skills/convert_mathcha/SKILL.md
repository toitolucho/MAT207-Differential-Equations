---
name: convert-mathcha
description: >-
  Use this skill when the user asks to convert Mathcha.io files (.mathcha format/JSON) into LaTeX (.tex) format.
---

# Convert Mathcha Files to LaTeX

This skill provides a robust parser to convert Mathcha's proprietary JSON-based exports into proper, compilable LaTeX files, preserving text, layout, colors, and complex math environments.

## How it works

Mathcha exports are structured as JSON files with nested layout blocks.
You have access to a custom python parser script: [`mathcha_parser.py`](./scripts/mathcha_parser.py).

The script accepts three arguments:
- `--input`: The path to the folder containing the raw Mathcha JSON exports.
- `--output`: The path to the destination folder where `.tex` files should be generated.
- `--mapping` (Optional): The path to a `mapping.json` file. If provided, the script will rename UUID-style files to human-readable filenames.

## Steps to Convert

1. **Identify the input and output directories:**
   Locate the folder containing the `.mathcha` files provided by the user, and determine where the generated `.tex` files should be saved.

2. **(Optional) Create a mapping file:**
   Mathcha exports files with UUID names (e.g. `170733fc-b49f-457b-bff0-443c85d4c9bf`). If the user provides a map (such as an image showing which UUID corresponds to which real filename), create a temporary `mapping.json` file.
   Format of `mapping.json`:
   ```json
   {
       "170733fc-b49f-457b-bff0-443c85d4c9bf": "Contenido 01/Variacion de Parametros",
       "20b41620-6a0d-4cd5-b240-0433b65d8c9e": "Contenido 01/04 - Ecuaciones Diferenciales"
   }
   ```
   *Note: Do not include the `.tex` extension in the mapping values.*

3. **Execute the parser:**
   Run the python script from your current directory.
   ```bash
   python .agents/skills/convert_mathcha/scripts/mathcha_parser.py --input "path/to/mathcha" --output "path/to/latex" --mapping "path/to/mapping.json"
   ```

4. **Verify the conversion:**
   Check the output directory to ensure `.tex` files and any binary files (like `.png` images) were successfully copied. You can run `pdflatex` to test compilation if it's available in the workspace.
