import fitz  # PyMuPDF
import os

class IngestionModule:
    def __init__(self, output_image_dir="extracted_images"):
        self.output_image_dir = output_image_dir
        os.makedirs(self.output_image_dir, exist_ok=True)

    def process_pdf(self, pdf_path: str, source_type: str) -> dict:
        """
        Reads a PDF, extracts text per page, and extracts images.
        source_type is typically "Inspection" or "Thermal".
        """
        text_content = []
        image_metadata = []

        try:
            doc = fitz.open(pdf_path)
            for page_num in range(len(doc)):
                page = doc[page_num]
                # Extract text
                text = page.get_text()
                if text.strip():
                    text_content.append({"page": page_num + 1, "text": text})
                
                # Extract images
                image_list = page.get_images(full=True)
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    image_filename = f"{source_type}_p{page_num+1}_i{img_index}.{image_ext}"
                    image_path = os.path.join(self.output_image_dir, image_filename)
                    
                    with open(image_path, "wb") as f:
                        f.write(image_bytes)
                        
                    image_metadata.append({
                        "page": page_num + 1,
                        "path": image_path,
                        "source": source_type
                    })
                    
        except Exception as e:
            print(f"Error processing PDF {pdf_path}: {e}")
            
        return {
            "source": source_type,
            "text": text_content,
            "images": image_metadata
        }

    def cleanup_images(self):
        """Removes extracted images directory to clean up after processing."""
        import shutil
        if os.path.exists(self.output_image_dir):
            shutil.rmtree(self.output_image_dir)
