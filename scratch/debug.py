import json
from convert_mathcha import parse_mathcha

with open(r"d:\Documents\USFX\MAT207\Texto Guia -Latex\MAT207-Differential-Equations\mathcha\Contenido 02-2026\01-Introduccion a las Ecuaciones Diferenciales\e39aaea1-f8b8-47fe-84f2-31186ca11e33", 'r', encoding='utf-8') as f:
    data = json.load(f)

from convert_mathcha import parse_blocks

# Find the math-container block
for line in data.get('lines', []):
    for block in line.get('blocks', []):
        if block.get('type') == 'composite' and block.get('text') == '\\math-container':
            lines = block['elements']['mathValue']['lines']
            from convert_mathcha import parse_lines
            print(repr(parse_lines(lines, True)))
            print("="*40)

