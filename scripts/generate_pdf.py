"""Convierte priorizacion-atributos-calidad.md a PDF usando fpdf2 con fuente Unicode."""
import os
import re
from fpdf import FPDF

INPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "priorizacion-atributos-calidad.md")
OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "priorizacion-atributos-calidad.pdf")


def sanitize(text):
    """Replace unicode chars that may cause issues."""
    replacements = {
        '↑↑': '++', '↑': '+', '↓↓': '--', '↓': '-',
        '○': 'o', '●': '*', '→': '->', '←': '<-',
        '✓': '[OK]', '✗': '[X]', '—': '-', '–': '-',
        '\u25cb': 'o', '\u2191': '+', '\u2193': '-',
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    # Remove any remaining non-latin1 chars
    return text.encode('latin-1', errors='replace').decode('latin-1')


def parse_table(lines):
    rows = []
    for line in lines:
        line = line.strip()
        if line.startswith('|') and not re.match(r'^\|[\s\-\|:]+\|$', line):
            cells = [sanitize(c.strip()) for c in line.split('|')[1:-1]]
            rows.append(cells)
    return rows


def render_table(pdf, rows):
    if not rows:
        return
    num_cols = len(rows[0])
    page_width = pdf.w - pdf.l_margin - pdf.r_margin
    col_width = page_width / num_cols

    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_fill_color(45, 95, 138)
    pdf.set_text_color(255, 255, 255)
    for cell in rows[0]:
        pdf.cell(col_width, 7, cell[:40], border=1, fill=True, align='C')
    pdf.ln()

    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(0, 0, 0)
    for i, row in enumerate(rows[1:]):
        if i % 2 == 0:
            pdf.set_fill_color(245, 245, 245)
        else:
            pdf.set_fill_color(255, 255, 255)
        for cell in row:
            pdf.cell(col_width, 6, cell[:40], border=1, fill=True)
        pdf.ln()
    pdf.ln(3)


class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, 'Priorizacion de Atributos de Calidad - Sistema de Campanas TO-BE', align='R')
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Pagina {self.page_no()}', align='C')


pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()

with open(INPUT, 'r', encoding='utf-8') as f:
    lines = f.readlines()

i = 0
table_buffer = []
in_table = False

while i < len(lines):
    line = lines[i].rstrip()

    if line.startswith('|'):
        table_buffer.append(line)
        in_table = True
        i += 1
        continue
    elif in_table:
        rows = parse_table(table_buffer)
        render_table(pdf, rows)
        table_buffer = []
        in_table = False

    sline = sanitize(line)

    if line.startswith('# '):
        pdf.set_font('Helvetica', 'B', 16)
        pdf.set_text_color(26, 82, 118)
        pdf.ln(5)
        pdf.cell(0, 10, sanitize(line[2:]))
        pdf.ln(12)
    elif line.startswith('## '):
        pdf.set_font('Helvetica', 'B', 13)
        pdf.set_text_color(45, 95, 138)
        pdf.ln(4)
        pdf.cell(0, 8, sanitize(line[3:]))
        pdf.ln(10)
    elif line.startswith('### '):
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(74, 140, 92)
        pdf.ln(3)
        pdf.cell(0, 7, sanitize(line[4:]))
        pdf.ln(9)
    elif line.startswith('#### '):
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_text_color(107, 76, 154)
        pdf.ln(2)
        pdf.cell(0, 6, sanitize(line[5:]))
        pdf.ln(8)
    elif line.startswith('---'):
        pdf.ln(3)
        pdf.set_draw_color(200, 200, 200)
        pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
        pdf.ln(3)
    elif line.startswith('> '):
        pdf.set_font('Helvetica', 'I', 9)
        pdf.set_text_color(85, 85, 85)
        pdf.cell(5)
        pdf.multi_cell(0, 5, sanitize(line[2:]))
        pdf.ln(2)
    elif line.startswith('*') and line.endswith('*') and not line.startswith('**'):
        pdf.set_font('Helvetica', 'I', 9)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 5, sanitize(line.strip('*')))
        pdf.ln(6)
    elif line.strip() == '':
        pdf.ln(2)
    else:
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(0, 0, 0)
        clean = re.sub(r'\*\*(.*?)\*\*', r'\1', sline)
        pdf.multi_cell(0, 5, clean)
        pdf.ln(1)

    i += 1

if table_buffer:
    rows = parse_table(table_buffer)
    render_table(pdf, rows)

pdf.output(OUTPUT)
print(f"PDF generado: {OUTPUT}")
