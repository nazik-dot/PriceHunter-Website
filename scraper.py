import re
import time
import threading
import requests
from bs4 import BeautifulSoup

BASE = "https://drops.in.ua"
HEADERS = {"User-Agent": "Mozilla/5.0"}
CACHE_TTL = 1200
_cache = {}
_lock = threading.Lock()

class SupplierError(Exception):
    pass

def _fetch_html(query):
    try:
        r = requests.get(f"{BASE}/catalog", params={"q": query}, headers=HEADERS, timeout=15)
        r.raise_for_status()
    except requests.RequestException as er:
        raise SupplierError(str(er)) from er
    return r.text

def _parse(html, limit):
    soup = BeautifulSoup(html, "html.parser")
    items, seen = [], set()

    for img in soup.select('img[src*="/img/p/"]'):
        src = img["src"]
        if src in seen:
            continue

        text, node = None, img 
        for _ in range(8):
            node = node.parent
            if node is None or len(node.select('img[src*="/img/p/"]')) > 1:
                break
            t = node.get_text(" ", strip=True)
            if "Роздріб" in t and "ID" in t:
                text = t
                break
        if not text:
            continue

        price_m = re.search(r"Роздріб[^\d]*(\d[\d\s]*(?:[.,]\d+)?)\s*₴", text)
        code_m = re.search(r"ID:\s*([\w-]+)", text)
        if not price_m or not code_m:
            continue

        price = float(re.sub(r"\s", "", price_m.group(1)).replace(",", "."))
        seen.add(src)
        items.append({
            "id": code_m.group(1),
            "name": img.get("alt", "").strip(),
            "price": int(round(price)),
            "image": BASE + src if src.startswith("/") else src,
        })
        if len(items) >= limit:
            break

    return items

def search_products(query, limit=20000):
    query = query.strip()
    if not query:
        return []
    key = query.lower()
    with _lock:
        hit = _cache.get(key)
        if hit and time.time() - hit[0] < CACHE_TTL:
            return hit[1]
    items = _parse(_fetch_html(query), limit)
    with _lock:
        _cache[key] = (time.time(), items)
    return items

def get_product_by_code(code):
    code = (code or "").strip()
    if not code:
        return None
    for item in _parse(_fetch_html(code), 50):
        if item["id"] == code:
            return item
    return None