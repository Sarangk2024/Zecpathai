# utils/split_jds.py - Utility to split a single PDF containing 81 JDs into text files.

import os
import re
from PyPDF2 import PdfReader
from utils.logger import logger

def clean_filename(title):
    # Remove non-alphanumeric characters, replace spaces/hyphens with single underscore
    slug = re.sub(r"[^a-zA-Z0-9\s\-]", "", title)
    slug = re.sub(r"[\s\-]+", "_", slug).lower()
    return slug.strip("_")

def main():
    logger.info("Initializing Job Description PDF Splitting Process...")
    
    pdf_path = os.path.join("data", "Tool & Die Maker Models.pdf")
    output_dir = os.path.join("data", "jd")
    
    if not os.path.exists(pdf_path):
        logger.error(f"Source PDF file not found at: {pdf_path}")
        print(f"Error: Source PDF not found at {pdf_path}")
        return

    os.makedirs(output_dir, exist_ok=True)
    
    try:
        reader = PdfReader(pdf_path)
        full_text = ""
        for idx, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"
        
        # Normalize carriage returns and spacing
        full_text = re.sub(r"\r\n", "\n", full_text)
        
        # Match "number. title" line at the start of a line or text block
        matches = list(re.finditer(r"(?:^|\n)(\d+)\.\s+([^\n\r]+)", full_text))
        
        if not matches:
            logger.error("No job description headers found in PDF.")
            print("Error: Could not find any job descriptions matching the expected pattern in the PDF.")
            return
            
        print(f"Found {len(matches)} job descriptions in the PDF. Splitting...")
        
        section_headers = ['job summary', 'job sum mary', 'key responsibilities', 'required skills', 'qualification', 'experience', 'salary']
        
        for i in range(len(matches)):
            start_idx = matches[i].start()
            end_idx = matches[i+1].start() if i < len(matches)-1 else len(full_text)
            block = full_text[start_idx:end_idx].strip()
            
            lines = block.split("\n")
            title_lines = [lines[0]]
            body_start_line = 1
            
            # Check if title spans multiple lines before section headers start
            while body_start_line < len(lines):
                next_line = lines[body_start_line].strip().lower()
                if any(next_line.startswith(h) for h in section_headers) or not next_line:
                    break
                if next_line.startswith('•') or next_line.startswith('-'):
                    break
                title_lines.append(lines[body_start_line])
                body_start_line += 1
                
            raw_title = " ".join(title_lines)
            # Remove leading number prefix (e.g. "1. ")
            title = re.sub(r"^\d+\.\s*", "", raw_title)
            title = re.sub(r"\s+", " ", title).strip()
            
            # Reconstruct clean text of the JD
            jd_num = int(matches[i].group(1))
            cleaned_title_line = f"{jd_num}. {title}"
            jd_body = "\n".join(lines[body_start_line:]).strip()
            full_jd_text = f"{cleaned_title_line}\n\n{jd_body}"
            
            # Save file
            file_slug = clean_filename(title)
            filename = f"jd_{jd_num:02d}_{file_slug}.txt"
            output_path = os.path.join(output_dir, filename)
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(full_jd_text)
                
            logger.debug(f"Extracted: {filename}")
            
        logger.info(f"Successfully split and stored {len(matches)} job descriptions in {output_dir}")
        print(f"Success: Split and stored {len(matches)} job descriptions in '{output_dir}'.")
        
    except Exception as e:
        logger.error(f"Error splitting PDF: {str(e)}")
        print(f"An error occurred while splitting the PDF: {e}")

if __name__ == "__main__":
    main()
