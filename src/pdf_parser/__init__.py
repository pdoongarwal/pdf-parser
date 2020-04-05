import tabula

def parse_pdf_to_csv(pdf_path):
    df = tabula.read_pdf(pdf_path, stream=True)
    df[0].to_csv('./parsed_csv/parsed.csv', index=False)