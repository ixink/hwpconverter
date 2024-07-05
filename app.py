import os
from flask import Flask, request, render_template
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import olefile

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            # Save the uploaded file to a temporary location
            temp_path = os.path.join('/tmp', uploaded_file.filename)
            uploaded_file.save(temp_path)

            # Call your HWP to PDF conversion function
            output_dir = '/path/to/output/directory'
            convert_hwp_to_pdf(temp_path, output_dir)

            # Clean up the temporary file
            os.remove(temp_path)

            return "File upload successful! Converted to PDF."
        else:
            return "No file selected."
    except Exception as e:
        return f"Error during file upload: {str(e)}"

if __name__ == '__main__':
    app.run(debug=False)
