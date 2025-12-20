import re
from datetime import datetime
from typing import List, Dict, Tuple
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def extract_text_from_pdf(pdf_file) -> str:
    """Extract text from a PDF file-like object."""
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def _find_date_in_text(text: str):
    """Find an invoice date in text using common date patterns; return ISO string or None."""
    date_patterns = [
        r"\b(\d{4})[-/](\d{1,2})[-/](\d{1,2})\b",            # YYYY-MM-DD or YYYY/MM/DD
        r"\b(\d{1,2})[-/](\d{1,2})[-/](\d{2,4})\b",          # DD-MM-YYYY or DD/MM/YYYY
        r"\b(\d{1,2})\s+([A-Za-z]{3,9})\s+(\d{4})\b",       # DD Month YYYY
    ]
    for pat in date_patterns:
        m = re.search(pat, text)
        if m:
            try:
                if len(m.groups()) == 3 and m.group(2).isalpha():
                    day, mon, year = m.groups()
                    dt = datetime.strptime(f"{day} {mon} {year}", "%d %B %Y")
                elif len(m.groups()) == 3 and len(m.group(1)) == 4:
                    year, month, day = m.groups()
                    dt = datetime(int(year), int(month), int(day))
                else:
                    d, mth, y = m.groups()
                    y = int(y)
                    if y < 100:
                        y += 2000
                    dt = datetime(int(y), int(mth), int(d))
                return dt.date().isoformat()
            except Exception:
                continue
    return None


def _extract_price(line: str):
    """Extract a price numeric value from a line; return normalized string or None."""
    price_regex = r"(?:USD|INR|AED|SAR|GBP|EUR|Rs|₹|£|€|\$)?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})|\d+\.\d{2}|\d+)"
    matches = re.findall(price_regex, line)
    if not matches:
        return None
    raw = matches[-1]
    return raw.replace(",", "")


def parse_invoice_items(text: str, source_file: str) -> List[Dict[str, str]]:
    """Parse invoice lines to extract product, price and date; heuristic-based."""
    items = []
    inv_date = _find_date_in_text(text) or None
    skip_keywords = {"subtotal", "total", "tax", "vat", "grand total", "balance", "discount", "amount"}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if any(k in line.lower() for k in skip_keywords):
            continue
        price = _extract_price(line)
        if price is None:
            continue
        price_pos = line.rfind(price)
        product = line[:price_pos].strip(" -:\t")
        product = re.sub(r"\s{2,}", " ", product)
        if not product or product.lower() in skip_keywords:
            continue
        items.append({
            "product": product,
            "price": price,
            "date": inv_date,
            "source": source_file,
        })
    return items


def split_text(texts: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    return splitter.split_text(texts)


def build_ingestion_stats(all_text: str, chunks: List[str], embeddings, embedding_model: str) -> Dict[str, object]:
    try:
        emb_dim = len(embeddings.embed_query("diagnostic"))
    except Exception:
        emb_dim = None
    return {
        "char_count": len(all_text),
        "chunk_count": len(chunks),
        "avg_chunk_len": int(sum(len(c) for c in chunks) / len(chunks)) if chunks else 0,
        "embedding_dim": emb_dim,
        "embedding_model": embedding_model,
        "sample_chunk": (chunks[0][:500] + ("..." if chunks and len(chunks[0]) > 500 else "")) if chunks else "",
    }
