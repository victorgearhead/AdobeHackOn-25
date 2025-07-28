# Persona-Based PDF Content Extractor - Challenge 1b

## Overview
This solution is designed to process multiple document collections tailored to distinct personas and tasks. It extracts important sections and summarises relevant content from PDFs using font-size-based heuristics. Each `Collection X/` folder contains input configuration, PDFs, and outputs in a structured format.

## Approach & Methodology
The methodology revolves around scalable, rule-based content extraction and ranking:

1. **Input Structure**: Each `challenge1b_input.json` file defines the task, persona, and PDF filenames to be analyzed.

2. **Font Size-Based Heuristics**: The extractor opens each PDF and examines every text span's font size. The top three font sizes are mapped to heading levels H1, H2, and H3. Each heading is associated with a page number and importance rank derived from its level.

3. **Parallel Processing**: To handle collections efficiently, the script uses `ProcessPoolExecutor` for concurrent PDF processing, drastically reducing runtime across large document sets.

4. **Summarized Snippets**: For every heading identified, the script captures the first 200 characters of the full page’s text to provide a contextual snippet under `subsection_analysis`.

5. **Structured Output**: The final output is a JSON file conforming to a predefined schema containing:
   - Metadata (persona, job, documents)
   - Extracted sections with importance ranking
   - Summarized page-level content

This approach is lightweight, robust, and flexible, designed for fast extraction without needing machine learning or NLP libraries.

## Libraries & Technologies
- **Python 3.11**
- **PyMuPDF (`fitz`)** – PDF parsing and font-size span analysis
- **concurrent.futures** – For multi-process parallelism

## Project Structure
```
main.py
Collection X/
├── PDFs/                     # Contains PDF files
├── challenge1b_input.json    # Input persona + task + documents
├── challenge1b_output.json   # Output with extracted section analysis
requirements.txt
Dockerfile
```

## Build & Run Instructions

### Local
```bash
pip install -r requirements.txt
python main.py
```

### Docker
```bash
# Build the image
docker build -t persona-pdf-extractor .

# Run the container (mount collection directory)
docker run --rm \
  -v "${PWD}/Collection 1":/app/Collection_1 \
  persona-pdf-extractor
```

> Output will be written to each `Collection X/challenge1b_output.json` file.

## Expected Execution
When `main.py` is executed, it scans all collections under `Challenge_1b/`, reads input configurations, processes each document in parallel, and writes persona-specific extracted outlines and refined snippets into the expected output JSON structure.

