#!/usr/bin/env python3
"""
Preserve complete extracted PDF text and produce heuristic navigation aids.
Raw text and page images remain the evidence; filtered text can omit content.

Text extracted from PDFs mixes body text with the axis labels, legends and panel
letters of every figure. The script suggests prose/caption blocks and page locations; these heuristics
can miss captions, merge body text into them, and discard short prose.

Usage:
  python extract_paper.py paper.pdf --out DIR
  python extract_paper.py paper.pdf --out DIR --render 2,4-6 [--dpi 110]

Writes to DIR:
  raw.md       complete extracted text, including short text and equations
  manifest.json  backend, page count, input hash, warnings and rendered pages
  prose.md     heuristically selected text (not complete), paragraph per line, with "[p.N]" page markers
  captions.md  candidate figure / table / Extended Data caption blocks, with its page
  index.md     page map: sections, figure captions, figure pages, numbered equations
  page-NN.png  (with --render) images of the requested pages, to view figures/equations

Backends: poppler CLI (pdftotext/pdftoppm) if installed, else PyMuPDF, else pypdf
(text only). If no renderer is available the script says so; never describe a figure
you have not seen.
"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys
from pathlib import Path

CAPTION = re.compile(r"^\s*((Extended Data |Supplementary )?(Fig\.|Figure|Table)\s*S?\d+[a-z]?\s*[|.:])", re.I)
SECTION = re.compile(r"^\s*(Abstract|Introduction|Background|Results|Discussion|Conclusions?|Methods|Materials and methods|"
                     r"Online methods|Experimental section|References|Acknowledg\w*|Data availability|Code availability|"
                     r"Supplementary information|Appendix\w*)\b", re.I)
EQNUM = re.compile(r"^\s*\((\d{1,3})\)\s*$")
FIGREF = re.compile(r"(Extended Data Fig\.|Fig\.|Figure)\s*(\d+)", re.I)


def page_texts(pdf):
    """Return all text, backend identity; never silently accept subprocess failures."""
    if shutil.which("pdftotext"):
        result = subprocess.run(["pdftotext", pdf, "-"], capture_output=True,
                                text=True, check=True)
        pages = result.stdout.split("\f")
        if pages and not pages[-1].strip():
            pages.pop()
        return pages, "poppler"
    try:
        import fitz
    except ImportError:
        fitz = None
    if fitz is not None:
        with fitz.open(pdf) as doc:
            if doc.needs_pass:
                raise ValueError("Encrypted PDF requires a password")
            return [page.get_text() for page in doc], "pymupdf"
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError("Need pdftotext, PyMuPDF, or pypdf for extraction") from exc
    reader = PdfReader(pdf)
    return [page.extract_text() or "" for page in reader.pages], "pypdf"


def is_prose(par):
    """Body text: long enough, mostly real words, lines not made of short labels."""
    words = re.findall(r"[A-Za-z]{3,}", par)
    lines = [l for l in par.splitlines() if l.strip()]
    if len(words) < 25 or not lines: return False
    short = sum(1 for l in lines if len(l.split()) < 4)
    return short / len(lines) < 0.5


def parse_pages(spec, n):
    pages = set()
    for part in spec.split(","):
        part = part.strip()
        if not re.fullmatch(r"\d+(?:-\d+)?", part):
            raise ValueError(f"Invalid page range: {part!r}")
        first, _, last = part.partition("-")
        first, last = int(first), int(last or first)
        if not 1 <= first <= last <= n:
            raise ValueError(f"Page range {part} outside 1..{n} or reversed")
        pages.update(range(first, last + 1))
    return sorted(pages)


def render(pdf, pages, out, dpi):
    if shutil.which("pdftoppm"):
        for p in pages:
            subprocess.run(["pdftoppm", "-r", str(dpi), "-png", "-singlefile", "-f", str(p), "-l", str(p),
                            pdf, os.path.join(out, f"page-{p:02d}")], check=True)
        return True
    try:
        import fitz
        with fitz.open(pdf) as doc:
            for p in pages:
                doc[p - 1].get_pixmap(dpi=dpi).save(os.path.join(out, f"page-{p:02d}.png"))
        return True
    except ImportError:
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf"); ap.add_argument("--out", required=True)
    ap.add_argument("--render", default=""); ap.add_argument("--dpi", type=int, default=110)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    if not 36 <= a.dpi <= 600:
        ap.error("--dpi must be between 36 and 600")
    texts, backend = page_texts(a.pdf)
    if not texts:
        raise ValueError("No pages extracted")
    pages = parse_pages(a.render, len(texts)) if a.render else []
    raw = "\n\n".join(f"[p.{i}]\n{t}" for i, t in enumerate(texts, 1))
    with open(os.path.join(a.out, "raw.md"), "w", encoding="utf-8") as f:
        f.write(raw)
    manifest = {
        "source": os.path.abspath(a.pdf), "sha256": hashlib.sha256(Path(a.pdf).read_bytes()).hexdigest(),
        "backend": backend, "page_count": len(texts), "page_numbering": "physical PDF pages, one-based",
        "warnings": ["prose, captions, and index are heuristic; consult raw.md and images"],
        "low_text_pages": [i for i, t in enumerate(texts, 1) if len(t.strip()) < 80],
        "render_requested": pages, "rendered_pages": [], "viewed_pages": "not tracked by this script"
    }
    if manifest["low_text_pages"]:
        manifest["warnings"].append("Low-text pages may need OCR; this helper does not perform OCR")

    prose, captions, index = [], [], []
    manifest["page_coverage"] = []
    for pno, t in enumerate(texts, 1):
        secs, caps, eqs, refs = [], [], [], set()
        for line in t.splitlines():
            if SECTION.match(line) and len(line.split()) <= 4 and not re.search(r"\d", line): secs.append(line.strip())
            m = EQNUM.match(line)
            if m: eqs.append(m.group(1))
            for r in FIGREF.finditer(line): refs.add(("ED " if r.group(1).lower().startswith("extended") else "") + r.group(2))
        prose_words = 0
        for par in re.split(r"\n\s*\n", t):
            lines = par.splitlines()
            # a caption can follow body text without a blank line: split it off
            cut = next((i for i, l in enumerate(lines) if CAPTION.match(l)), None)
            body, cap = (lines, []) if cut is None else (lines[:cut], lines[cut:])
            if cap:
                captions.append(f"[p.{pno}] " + " ".join(" ".join(cap).split()))
                caps.append(CAPTION.match(cap[0]).group(1).strip(" |.:"))
            body = "\n".join(body)
            if is_prose(body):
                prose.append(f"[p.{pno}] " + " ".join(body.split()))
                prose_words += len(body.split())
        all_words = len(t.split()) or 1
        manifest["page_coverage"].append({"page": pno, "raw_words": len(t.split()),
                                           "prose_words": prose_words})
        figure_page = prose_words / all_words < 0.35 and all_words > 80
        index.append(f"p.{pno}: " + "; ".join(filter(None, [
            "sections: " + ", ".join(secs) if secs else "",
            "captions: " + ", ".join(caps) if caps else "",
            "equations: (" + "), (".join(eqs) + ")" if eqs else "",
            "low prose retention (inspect raw/page)" if figure_page else ""])))

    (Path(a.out) / "prose.md").write_text("\n\n".join(prose), encoding="utf-8")
    (Path(a.out) / "captions.md").write_text("\n\n".join(captions), encoding="utf-8")
    (Path(a.out) / "index.md").write_text("\n".join(index), encoding="utf-8")
    print(f"{len(texts)} pages | {len(prose)} prose paragraphs | {len(captions)} captions -> {a.out}")
    print("\n".join(index))
    if a.render:
        if render(a.pdf, pages, a.out, a.dpi):
            manifest["rendered_pages"] = pages
            print("rendered:", ", ".join(f"page-{p:02d}.png" for p in pages))
        else:
            manifest["warnings"].append("No renderer available")
            print("NO RENDERER (install poppler-utils or pymupdf): figures cannot be viewed; say so in the output.",
                  file=sys.stderr)

    with open(os.path.join(a.out, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
