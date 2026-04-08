from pypdf import PdfReader, PdfWriter
import sys
import os

def protect_pdf(input_pdf_path, output_pdf_path, password):
    """
    Adds a password to a PDF file.
    
    :param input_pdf_path: Path to the original PDF file
    :param output_pdf_path: Path where the protected PDF will be saved
    :param password: Password to apply to the PDF
    """
    if not os.path.exists(input_pdf_path):
        print(f"Error: The file {input_pdf_path} does not exist.")
        return

    try:
        # Create PDF reader and writer objects
        reader = PdfReader(input_pdf_path)
        writer = PdfWriter()

        # Add all pages from the reader to the writer
        for page in reader.pages:
            writer.add_page(page)

        # Encrypt the PDF with the given password
        writer.encrypt(password)

        # Save the new password-protected PDF
        with open(output_pdf_path, "wb") as output_file:
            writer.write(output_file)
            
        print(f"Successfully created password-protected PDF: {output_pdf_path}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) == 4:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        password = sys.argv[3]
        protect_pdf(input_file, output_file, password)
    else:
        print("Usage: python password_protect_pdf.py <input_pdf> <output_pdf> <password>")
        print("Example: python password_protect_pdf.py my_doc.pdf protected_doc.pdf mySecretPassword")
