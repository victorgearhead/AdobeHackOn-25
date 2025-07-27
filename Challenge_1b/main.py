import os
import json
import fitz
from concurrent.futures import ProcessPoolExecutor, as_completed

INPUT_DIR = "Challenge_1b/"


def load_input(input_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_outline(pdf_file):
    doc = fitz.open(pdf_file)
    spans = []
    for page in doc:
        try:
            blocks = page.get_text("dict")["blocks"]
        except RuntimeError:
            continue
        for b in blocks:
            if "lines" not in b:
                continue
            for line in b["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if text and len(text) <= 200:
                        spans.append({
                            "page": page.number + 1,
                            "size": span["size"],
                            "text": text
                        })
    sizes = sorted({s["size"] for s in spans}, reverse=True)
    level_map = {size: f"H{idx+1}" for idx, size in enumerate(sizes[:3])}

    sections = []
    snippets = []
    for span in spans:
        lvl = level_map.get(span["size"])
        if lvl:
            sections.append({
                "section_title": span["text"],
                "importance_rank": int(lvl[1:]),
                "page_number": span["page"]
            })
            page = doc[span["page"] - 1]
            text = page.get_text().replace("\n", " ").strip()
            snippet = text[:200] + ('...' if len(text) > 200 else '')
            snippets.append(snippet)
    filename = os.path.basename(pdf_file)
    return filename, sections, snippets


def plan_collection(collection_path):
    input_path = os.path.join(collection_path, 'challenge1b_input.json')
    cfg = load_input(input_path)

    docs = cfg['documents']
    persona = cfg['persona']['role']
    task = cfg['job_to_be_done']['task']

    output = {
        "metadata": {
            "input_documents": [d['filename'] for d in docs],
            "persona": persona,
            "job_to_be_done": task
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }

    pdf_paths = [os.path.join(collection_path, 'PDFs', d['filename']) for d in docs]

    with ProcessPoolExecutor() as executor:
        future_to_pdf = {executor.submit(extract_outline, path): path for path in pdf_paths if os.path.exists(path)}
        for future in as_completed(future_to_pdf):
            fname, sections, snippets = future.result()
            for sec, snip in zip(sections, snippets):
                output['extracted_sections'].append({
                    "document": fname,
                    **sec
                })
                output['subsection_analysis'].append({
                    "document": fname,
                    "refined_text": snip,
                    "page_number": sec['page_number']
                })

    out_path = os.path.join(collection_path, 'challenge1b_output.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"→ Wrote {out_path}")


def main():
    collections = [os.path.join(INPUT_DIR, d) for d in os.listdir(INPUT_DIR) if os.path.isdir(os.path.join(INPUT_DIR, d))]
    for col_path in collections:
        plan_collection(col_path)

if __name__ == '__main__':
    main()
