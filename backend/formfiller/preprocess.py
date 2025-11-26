import json
from pdfrw import PdfReader, PdfDict, PdfName, PdfString

def clean_pdf_string(s):
    """
    Convert pdfrw PdfString or raw string to clean Python string without parentheses.
    """
    if s is None:
        return ''
    if hasattr(s, 'to_unicode'):
        return s.to_unicode()
    s = str(s)
    if s.startswith('(') and s.endswith(')'):
        s = s[1:-1]
    return s.strip()

def extract_fields(pdf_path):
    """
    Extract all form fields with metadata from a PDF.
    Returns a list of dictionaries.
    """
    pdf = PdfReader(pdf_path)
    fields = []

    for page_num, page in enumerate(pdf.pages, start=1):
        annots = page.get('/Annots')
        if not annots:
            continue
        for annot in annots:
            if not isinstance(annot, PdfDict):
                continue  # skip invalid entries

            field_name = annot.get('/T')
            if not field_name:
                continue  # skip if no field name

            field = {}
            field['name'] = clean_pdf_string(field_name)
            field_type = annot.get('/FT')
            field['type'] = str(field_type) if field_type else 'Unknown'
            field['tooltip'] = clean_pdf_string(annot.get('/TU'))

            # Flags
            try:
                field['flags'] = int(annot.get('/Ff', 0))
            except Exception:
                field['flags'] = 0

            # Possible states (for checkboxes/radio buttons)
            states = annot.get('/_States_')
            if states:
                field['states'] = [clean_pdf_string(s) for s in states]
            elif field_type == '/Btn':
                field['states'] = ['/On', '/Off']
            else:
                field['states'] = []

            # Rect / position
            rect = annot.get('/Rect')
            if rect:
                try:
                    field['rect'] = [float(x) for x in rect]
                except Exception:
                    field['rect'] = []
            else:
                field['rect'] = []

            field['page'] = page_num
            fields.append(field)

    return fields

if __name__ == "__main__":
    input_pdf = "ex.pdf"

    # Extract fields
    fields = extract_fields(input_pdf)

    # Save to JSON
    with open("pdf_fields_clean.json", "w", encoding="utf-8") as f:
        json.dump(fields, f, indent=4)

    print("✅ Extracted fields saved to pdf_fields_clean.json")
