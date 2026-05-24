"""
Genera PDFs de todos los documentos en docs/ y los guarda en entregables/.
Ejecutar: python scripts/generate_all_pdfs.py
"""
import os
import re
from fpdf import FPDF

DOCS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'docs')
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'entregables')


def sanitize(text):
    replacements = {
        '↑↑': '++', '↑': '+', '↓↓': '--', '↓': '-',
        '○': 'o', '●': '*', '→': '->', '←': '<-',
        '✓': '[OK]', '✗': '[X]', '—': '-', '–': '-',
        '\u25cb': 'o', '\u2191': '+', '\u2193': '-',
        '≥': '>=', '≤': '<=', '\u2265': '>=', '\u2264': '<=',
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.encode('latin-1', errors='replace').decode('latin-1')


def parse_table(lines):
    rows = []
    for line in lines:
        line = line.strip()
        if line.startswith('|') and not re.match(r'^\|[\s\-\|:]+\|$', line):
            cells = [sanitize(c.strip()) for c in line.split('|')[1:-1]]
            rows.append(cells)
    return rows


class DocPDF(FPDF):
    def __init__(self, title_text=""):
        super().__init__()
        self.title_text = title_text

    def header(self):
        self.set_font('Helvetica', 'B', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, sanitize(self.title_text), align='R')
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Pagina {self.page_no()}', align='C')


def render_table(pdf, rows):
    if not rows:
        return
    num_cols = len(rows[0])
    page_width = pdf.w - pdf.l_margin - pdf.r_margin
    col_width = page_width / num_cols
    if col_width < 20:
        col_width = 20

    pdf.set_font('Helvetica', 'B', 7)
    pdf.set_fill_color(45, 95, 138)
    pdf.set_text_color(255, 255, 255)
    for cell in rows[0]:
        pdf.cell(col_width, 6, cell[:45], border=1, fill=True, align='C')
    pdf.ln()

    pdf.set_font('Helvetica', '', 7)
    pdf.set_text_color(0, 0, 0)
    for i, row in enumerate(rows[1:]):
        if i % 2 == 0:
            pdf.set_fill_color(245, 245, 245)
        else:
            pdf.set_fill_color(255, 255, 255)
        for cell in row:
            pdf.cell(col_width, 5, cell[:45], border=1, fill=True)
        pdf.ln()
    pdf.ln(3)


def md_to_pdf(md_path, pdf_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Extract title from first H1
    title = os.path.basename(md_path)
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
            break

    pdf = DocPDF(title_text=title)
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # Skip YAML front matter
    i = 0
    if lines and lines[0].strip() == '---':
        i = 1
        while i < len(lines) and lines[i].strip() != '---':
            i += 1
        i += 1  # skip closing ---

    table_buffer = []
    in_table = False
    in_code = False

    while i < len(lines):
        line = lines[i].rstrip()

        # Code blocks - skip mermaid/code
        if line.startswith('```'):
            in_code = not in_code
            if not in_code:
                pdf.set_font('Helvetica', 'I', 8)
                pdf.set_text_color(100, 100, 100)
                pdf.cell(0, 5, '[Diagrama - ver archivo PNG adjunto]')
                pdf.ln(6)
            i += 1
            continue
        if in_code:
            i += 1
            continue

        # Tables
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
        elif line.strip() == '':
            pdf.ln(2)
        else:
            pdf.set_font('Helvetica', '', 10)
            pdf.set_text_color(0, 0, 0)
            clean = re.sub(r'\*\*(.*?)\*\*', r'\1', sline)
            pdf.multi_cell(0, 5, clean)
            pdf.ln(1)

        i += 1

    # Flush remaining table
    if table_buffer:
        rows = parse_table(table_buffer)
        render_table(pdf, rows)

    pdf.output(pdf_path)


def needs_rebuild(md_path, pdf_path):
    """Retorna True si el PDF no existe o el MD fue modificado después del PDF."""
    if not os.path.exists(pdf_path):
        return True
    return os.path.getmtime(md_path) > os.path.getmtime(pdf_path)


def main():
    import sys
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Si se pasa un archivo específico como argumento, solo genera ese
    # Uso: python generate_all_pdfs.py 06-arquitectura-software.md
    target_file = sys.argv[1] if len(sys.argv) > 1 else None

    generated = 0
    skipped = 0

    # Main docs
    docs_files = sorted([f for f in os.listdir(DOCS_DIR) if f.endswith('.md')])
    for f in docs_files:
        if target_file and f != target_file:
            continue
        md_path = os.path.join(DOCS_DIR, f)
        pdf_name = f.replace('.md', '.pdf')
        pdf_path = os.path.join(OUTPUT_DIR, pdf_name)
        if target_file or needs_rebuild(md_path, pdf_path):
            md_to_pdf(md_path, pdf_path)
            print(f"  PDF generado: {pdf_name}")
            generated += 1
        else:
            skipped += 1

    # Anexos
    anexos_dir = os.path.join(DOCS_DIR, 'anexos')
    if os.path.exists(anexos_dir):
        anexos_files = sorted([f for f in os.listdir(anexos_dir) if f.endswith('.md')])
        for f in anexos_files:
            if target_file and f != target_file:
                continue
            md_path = os.path.join(anexos_dir, f)
            pdf_name = f.replace('.md', '.pdf')
            pdf_path = os.path.join(OUTPUT_DIR, pdf_name)
            if target_file or needs_rebuild(md_path, pdf_path):
                md_to_pdf(md_path, pdf_path)
                print(f"  PDF generado: {pdf_name}")
                generated += 1
            else:
                skipped += 1

    print(f"\nResultado: {generated} generados, {skipped} sin cambios (omitidos)")


if __name__ == '__main__':
    main()
