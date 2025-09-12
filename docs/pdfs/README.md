# Source Documents Directory

## Purpose
This directory contains the original Hebrew regulatory documentation used as source material for the business licensing requirements.

## Expected Files

### Hebrew Regulatory PDF
**Filename**: Place your Hebrew business licensing PDF here (any name ending in `.pdf`)  
**Content**: Israeli restaurant/business licensing regulations  
**Language**: Hebrew  
**Usage**: Source material for manual curation into `data/requirements.json`

**Example filenames**:
- `israeli-restaurant-licensing-requirements.pdf`
- `business-licensing-regulations-hebrew.pdf`
- `restaurant-permit-requirements.pdf`

## Processing Approach

The PDF content has been **manually curated** rather than automatically extracted:

1. **Manual Analysis**: Expert review of Hebrew regulatory text
2. **Rule Extraction**: Identification of key licensing requirements
3. **Translation**: Hebrew → English descriptions  
4. **Structuring**: Mapping to JSON schema with triggers
5. **Source References**: Page/section citations maintained

## File Usage

- **Scripts Reference**: `scripts/parse_pdf.py` can validate against PDF if needed
- **Documentation**: Source file serves as ground truth for rule accuracy
- **Audit Trail**: Maintains traceability from source to processed data

## Security Note

- PDF files are included in `.gitignore` by default
- Remove the `# *.pdf` comment in root `.gitignore` if you want to commit the source PDF
- Consider if the PDF contains sensitive regulatory information before committing

---

**Place your Hebrew regulatory PDF file in this directory for reference and processing.**