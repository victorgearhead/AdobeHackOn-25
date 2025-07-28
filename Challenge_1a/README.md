# PDF Outline Extractor - Challenge 1a

## Overview

This solution is an efficient PDF outline extractor. It processes all PDF files in the `app/input` directory, infers section headings based on font size, and outputs structured JSON files in `app/output`, conforming to the schema defined in `app/schema/output_schema.json`.

## Approach & Methodology

1. **Font‑Size Inference**: We scan every text span on each PDF page, collect font sizes, and dynamically map the three largest sizes to heading levels H1, H2, and H3.
2. **Title Extraction**: On the first page, we identify the single largest font span as the document title.

This method balances accuracy and performance, requiring no OCR or heavy machine‑learning models and leveraging PyMuPDF’s native text extraction.

## Libraries & Technologies

- **Python 3.11**
- **PyMuPDF (**``**)**: Fast, native PDF parsing and text extraction.
- **Concurrent Processing**: `concurrent.futures.ProcessPoolExecutor` to parallelize extraction across multiple PDFs.

## Project Structure

```
app/
  input/                # Source PDFs (.pdf)
  output/               # Generated outlines (.json)
  schema/               # JSON schema (output_schema.json)
main.py                 # Extraction script
requirements.txt        # Python dependencies
Dockerfile              # Containerization instructions
README.md               # This documentation
```

## Build & Run Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run Locally**
   ```bash
   python main.py
   ```
   Results will appear under `app/output`.

## Docker

Build and run in a container to ensure environment consistency:

```bash
# Build image
docker build -t pdf-outline-extractor .

# Run container (mount local input/output)
docker run --rm \
  -v "${PWD}/app/input":/app/app/input \
  -v "${PWD}/app/output":/app/app/output \
  pdf-outline-extractor
```

## Expected Execution

The container or local script will iterate over every `.pdf` in `app/input`, extract the outline, validate it, and write JSON files to `app/output`. Each output file matches the schema in `app/schema/output_schema.json`.
