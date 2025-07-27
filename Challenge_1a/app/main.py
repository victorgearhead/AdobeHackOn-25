import os
import json
import fitz 

INPUT_DIR = "app/input"
OUTPUT_DIR = "app/output"

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    title = ""
    headings = []

    page1 = doc[0]
    blocks = page1.get_text("dict")["blocks"]
    spans = []
    for b in blocks:
        if "lines" not in b: continue
        for line in b["lines"]:
            for span in line["spans"]:
                spans.append(span)
    if spans:
        top = max(spans, key=lambda s: s["size"])
        title = top["text"].strip()

    for page_number, page in enumerate(doc, start=1):
        spans = []
        for b in page.get_text("dict")["blocks"]:
            if "lines" not in b: continue
            for line in b["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text or len(text)>200: 
                        continue
                    spans.append(span)
        sizes = sorted({s["size"] for s in spans}, reverse=True)
        levels = sizes[:3]
        for span in spans:
            try:
                lvl = levels.index(span["size"])
            except ValueError:
                continue
            level = f"H{lvl+1}"
            headings.append({
                "level": level,
                "text": span["text"].strip(),
                "page": page_number
            })
    return {"title": title, "outline": headings}


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for fname in os.listdir(INPUT_DIR):
        if not fname.lower().endswith(".pdf"):
            continue
        inpath = os.path.join(INPUT_DIR, fname)
        outname = os.path.splitext(fname)[0] + ".json"
        outpath = os.path.join(OUTPUT_DIR, outname)
        result = extract_outline(inpath)
        with open(outpath, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"→ Wrote {outpath}")

if __name__ == "__main__":
    main()
