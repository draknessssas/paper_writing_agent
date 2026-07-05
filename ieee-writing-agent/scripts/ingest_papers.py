#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except Exception:
    fitz = None

try:
    import docx
except Exception:
    docx = None


SECTION_PATTERNS = [
    "abstract",
    "introduction",
    "background",
    "literature review",
    "system description",
    "modeling",
    "modelling",
    "analysis",
    "proposed",
    "method",
    "control",
    "design",
    "implementation",
    "simulation",
    "experimental",
    "experiment",
    "results",
    "discussion",
    "conclusion",
    "references",
    "appendix",
]

SUPPORTED_EXTENSIONS = [".pdf", ".docx", ".tex", ".txt", ".md"]


def read_pdf(path: Path) -> str:
    if fitz is None:
        raise RuntimeError("PyMuPDF is not installed. Run: pip install pymupdf")
    doc = fitz.open(path)
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text("text")
        pages.append(f"\n\n[PAGE {i + 1}]\n\n{text}")
    return "\n".join(pages)


def read_docx(path: Path) -> str:
    if docx is None:
        raise RuntimeError("python-docx is not installed. Run: pip install python-docx")
    document = docx.Document(path)
    return "\n\n".join(p.text for p in document.paragraphs if p.text.strip())


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"-\n(?=[a-z])", "", text)
    text = re.sub(r"(?<![.!?:;])\n(?!\n)", " ", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def detect_section(line: str) -> str | None:
    stripped = line.strip()
    normalized = re.sub(r"^[IVXLC\d]+[\.\)]\s*", "", stripped, flags=re.I)
    normalized = re.sub(r"^[A-Z]\.\s*", "", normalized)
    normalized_low = normalized.lower().strip(": ")
    for pattern in SECTION_PATTERNS:
        if re.fullmatch(pattern, normalized_low, flags=re.I):
            return pattern.title()
        if len(normalized_low) < 80 and re.search(rf"\b{pattern}\b", normalized_low, flags=re.I):
            return normalized.title()
    return None


def split_sections(text: str) -> list[tuple[str, str]]:
    lines = text.splitlines()
    sections: list[tuple[str, str]] = []
    current_title = "Front Matter"
    current: list[str] = []

    for line in lines:
        title = detect_section(line)
        if title and len(line.strip()) < 100:
            if current:
                sections.append((current_title, "\n".join(current).strip()))
            current_title = title
            current = []
        else:
            current.append(line)

    if current:
        sections.append((current_title, "\n".join(current).strip()))
    return sections


def split_paragraphs(section_text: str) -> list[str]:
    raw_paragraphs = re.split(r"\n\s*\n", section_text)
    paragraphs = []
    for paragraph in raw_paragraphs:
        paragraph = re.sub(r"\s+", " ", paragraph).strip()
        if len(paragraph) >= 80:
            paragraphs.append(paragraph)
    return paragraphs


def output_name(input_root: Path, source: Path) -> str:
    rel = source.relative_to(input_root)
    parts = list(rel.with_suffix("").parts)
    return "__".join(parts) + ".md"


def convert_one(input_root: Path, path: Path, out_dir: Path) -> Path | None:
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        text = read_pdf(path)
    elif suffix == ".docx":
        text = read_docx(path)
    elif suffix in [".tex", ".txt", ".md"]:
        text = read_text(path)
    else:
        print(f"[SKIP] unsupported file: {path}")
        return None

    text = clean_text(text)
    sections = split_sections(text)

    out_path = out_dir / output_name(input_root, path)
    with out_path.open("w", encoding="utf-8") as handle:
        handle.write(f"# Source: {path.name}\n\n")
        handle.write(f"- Source path: `{path}`\n")
        handle.write("- Use: style/process/reference analysis only\n\n")
        for title, body in sections:
            handle.write(f"## {title}\n\n")
            paragraphs = split_paragraphs(body)
            if not paragraphs and body.strip():
                handle.write(body.strip() + "\n\n")
                continue
            for idx, paragraph in enumerate(paragraphs, start=1):
                handle.write(f"### P{idx}\n\n{paragraph}\n\n")

    print(f"[OK] {path} -> {out_path}")
    return out_path


def find_files(input_dir: Path) -> list[Path]:
    files: list[Path] = []
    for extension in SUPPORTED_EXTENSIONS:
        files.extend(input_dir.rglob(f"*{extension}"))
    return sorted(files)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input corpus directory")
    parser.add_argument("--output", required=True, help="Output processed directory")
    args = parser.parse_args()

    input_dir = Path(args.input).expanduser().resolve()
    output_dir = Path(args.output).expanduser().resolve()

    if not input_dir.exists():
        print(f"Input folder does not exist: {input_dir}", file=sys.stderr)
        return 2
    if not input_dir.is_dir():
        print(f"Input path is not a directory: {input_dir}", file=sys.stderr)
        return 2

    output_dir.mkdir(parents=True, exist_ok=True)
    files = find_files(input_dir)

    if not files:
        print(f"No supported files found in {input_dir}")
        return 1

    converted = []
    failures = []
    for path in files:
        try:
            out_path = convert_one(input_dir, path, output_dir)
            if out_path is not None:
                converted.append(out_path)
        except Exception as exc:
            failures.append((path, exc))
            print(f"[FAIL] {path}: {exc}", file=sys.stderr)

    print("\nSummary")
    print(f"- input: {input_dir}")
    print(f"- output: {output_dir}")
    print(f"- supported files found: {len(files)}")
    print(f"- converted: {len(converted)}")
    print(f"- failed: {len(failures)}")
    if failures:
        print("- failures:")
        for path, exc in failures:
            print(f"  - {path}: {exc}")
        return 1
    print("- extraction risk: PDF two-column reading order may require spot checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
