# parsers/resume_extractor.py - Resume PDF/DOCX text parsing and normalization.

import os
import re
import sys

# Add parent directory to path to support direct script execution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyPDF2 import PdfReader
from docx import Document
from utils.logger import logger

def extract_text_from_pdf(file_path):
    """
    Extract raw text from a PDF file.
    """
    logger.info(f"Extracting raw text from PDF: {file_path}")
    text = ""
    try:
        reader = PdfReader(file_path)
        for idx, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        logger.error(f"Failed to read PDF {file_path}: {str(e)}")
        raise e

def extract_text_from_docx(file_path):
    """
    Extract raw text from a DOCX file.
    """
    logger.info(f"Extracting raw text from DOCX: {file_path}")
    try:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        logger.error(f"Failed to read DOCX {file_path}: {str(e)}")
        raise e

def clean_text(text):
    """
    Remove special characters, normalize spaces, and standardize bullet points.
    """
    if not text:
        return ""
    
    # Standardize dashes before stripping special characters (using unicode escapes to prevent encoding mismatch)
    text = text.replace("\u2013", "-").replace("\u2014", "-").replace("\u2012", "-").replace("\u2212", "-").replace("•", " - ").replace("●", " - ").replace("▪", " - ")
    
    # Remove unwanted special characters, keeping alphanumeric, spaces, punctuation, hyphens, and newlines
    text = re.sub(r"[^a-zA-Z0-9\s\.\,\-\n:@]", "", text)
    
    # Standardize spaces (turn multiple inline spaces into a single space)
    text = re.sub(r"[ \t]+", " ", text)
    
    # Trim leading/trailing whitespace
    text = text.strip()
    
    return text

def normalize_sections(text):
    """
    Standardize common section headings to a unified format.
    """
    if not text:
        return ""
        
    replacements = {
        r"(?i)\bWORK EXPERIENCE\b": "Experience",
        r"(?i)\bPROFESSIONAL EXPERIENCE\b": "Experience",
        r"(?i)\bEMPLOYMENT HISTORY\b": "Experience",
        r"(?i)\bEDUCATION DETAILS\b": "Education",
        r"(?i)\bACADEMIC BACKGROUND\b": "Education",
        r"(?i)\bSKILLS SET\b": "Skills",
        r"(?i)\bCORE COMPETENCIES\b": "Skills",
        r"(?i)\bTECHNICAL SKILLS\b": "Skills",
        r"(?i)\bCERTIFICATIONS\b": "Certifications"
    }
    
    normalized = text
    for regex_pattern, standard_heading in replacements.items():
        normalized = re.sub(regex_pattern, standard_heading, normalized)
        
    return normalized

def extract_resume(file_path):
    """
    Extracts text from PDF/DOCX, cleans it, and normalizes standard headings.
    Returns:
        dict: containing file name, raw text, and cleaned text.
    """
    if not os.path.exists(file_path):
        logger.error(f"Resume file path not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
        
    ext = file_path.split(".")[-1].lower()
    if ext == "pdf":
        raw_text = extract_text_from_pdf(file_path)
    elif ext in ["docx", "doc"]:
        raw_text = extract_text_from_docx(file_path)
    else:
        logger.error(f"Unsupported file format extension: {ext}")
        raise ValueError("Unsupported file format. Only PDF and DOCX files are supported.")
        
    cleaned = clean_text(raw_text)
    normalized = normalize_sections(cleaned)
    
    logger.info(f"Resume text cleaned and normalized for {os.path.basename(file_path)}")
    return {
        "file_name": os.path.basename(file_path),
        "raw_text": raw_text,
        "cleaned_text": normalized
    }

def save_cleaned_text(output_path, data):
    """
    Saves cleaned resume text to a target file.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(data["cleaned_text"])
    logger.info(f"Saved parsed resume content to: {output_path}")

if __name__ == "__main__":
    # Standalone script test block
    print("\n--- ZECPATH STANDALONE RESUME PARSER TEST ---")
    sample_dir = os.path.join("data", "resumes")
    processed_dir = os.path.join("data", "processed_resumes")
    
    if os.path.exists(sample_dir):
        files = [f for f in os.listdir(sample_dir) if f.split(".")[-1].lower() in ["pdf", "docx", "doc"]]
        
        if files:
            test_file = os.path.join(sample_dir, files[0])
            print(f"Executing extraction test on: {test_file}")
            try:
                # Run extraction
                res = extract_resume(test_file)
                
                # SAVE the parsed output to processed_resumes/ folder
                output_name = files[0].rsplit(".", 1)[0] + "_cleaned.txt"
                output_path = os.path.join(processed_dir, output_name)
                save_cleaned_text(output_path, res)
                
                print("\n[Raw Text Sample (First 150 chars)]:")
                print("--------------------------------------------------")
                print(res["raw_text"][:150].strip() + "...")
                print("--------------------------------------------------")
                print("\n[Cleaned & Normalized Text (First 150 chars)]:")
                print("--------------------------------------------------")
                print(res["cleaned_text"][:150].strip() + "...")
                print("--------------------------------------------------")
                print(f"\nCleaned file created at: {output_path}")
                print("--- Standalone parsing check completed successfully ---\n")
            except Exception as ex:
                print(f"Error parsing: {ex}")
        else:
            print("No resumes found in data/resumes/. Run 'python -m utils.generate_resumes' first.")
    else:
        print("Data directories not found. Please run this command from the repository root.")
