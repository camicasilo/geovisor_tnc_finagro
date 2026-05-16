from pypdf import PdfReader
import os

def extract_all_pdfs():
    doc_dir = "Documentacion"
    scratch_dir = "scratch"
    
    if not os.path.exists(doc_dir):
        print(f"--- Directorio no encontrado: {doc_dir} ---")
        return

    pdf_files = [f for f in os.listdir(doc_dir) if f.lower().endswith(".pdf")]
    
    if not pdf_files:
        print("--- No se encontraron PDFs en Documentacion ---")
        return

    print(f"--- Procesando {len(pdf_files)} archivos PDF ---")

    for pdf in pdf_files:
        pdf_path = os.path.join(doc_dir, pdf)
        output_name = pdf.replace(" ", "_").replace(".pdf", "_text.txt")
        output_path = os.path.join(scratch_dir, output_name)
        
        print(f"Leyendo: {pdf}...")
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"  -> Guardado en: {output_path}")
        except Exception as e:
            print(f"  -> Error leyendo {pdf}: {e}")

if __name__ == "__main__":
    extract_all_pdfs()
