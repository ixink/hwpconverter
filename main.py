import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import olefile

def txt_to_pdf(txt_file, pdf_file):
    c = canvas.Canvas(pdf_file, pagesize=letter)
    width, height = letter
    with open(txt_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    y = height - 40
    for line in lines:
        if y < 40:
            c.showPage()
            y = height - 40
        c.drawString(40, y, line.strip())
        y -= 14
    c.save()

def convert_hwp_to_pdf(hwp_file, output_dir):
    # Open the HWP file
    f = olefile.OleFileIO(hwp_file)

    # Extract the content from the 'PrvText' stream (encoded in UTF-16)
    encoded_text = f.openstream('PrvText').read()
    txt_content = encoded_text.decode('utf-16')

    txt_file = os.path.join(output_dir, 'output.txt')
    pdf_file = os.path.join(output_dir, 'output.pdf')

    with open(txt_file, 'w', encoding='utf-8') as txt_output:
        txt_output.write(txt_content)

    txt_to_pdf(txt_file, pdf_file)
    print(f"Converted {hwp_file} to {pdf_file}")

def main():
    input_file = input("Enter the path to the HWP or HWPX file: ")
    output_dir = input("Enter the output directory path: ")

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Check file extension
    _, ext = os.path.splitext(input_file.lower())
    if ext == '.hwp':
        convert_hwp_to_pdf(input_file, output_dir)
    elif ext == '.hwpx':
        # Convert HWPX to HWP
        hwpx_file = HWPXFile.from_file(input_file)
        hwp_file = HWPFile.to_hwp(hwpx_file)
        HWPXWriter.to_filepath(hwp_file, os.path.join(output_dir, 'temp.hwp'))
        # Convert HWP to PDF
        convert_hwp_to_pdf(os.path.join(output_dir, 'temp.hwp'), output_dir)
        os.remove(os.path.join(output_dir, 'temp.hwp'))
    else:
        print("Unsupported file format. Please provide an HWP or HWPX file.")

if __name__ == "__main__":
    main()
