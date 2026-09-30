"""Holt Mietangebote von Milanuncios (Teneriffa + Gran Canaria) und bewertet sie
grob nach den Suchkriterien. Ausgabe: data/milanuncios_latest.json

Aufruf: python3 scraper/milanuncios.py
"""
import json, re, time, random, subprocess, sys, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
PROVINCES = {"tenerife": "Teneriffa", "las_palmas": "Gran Canaria (Prov. Las Palmas)"}
QUERIES = ["enero", "temporada", "por meses", "invierno", "corta temporada", "mensual", "meses"]
MAX_PRICE = 2000
MIN_PRICE = 450  # darunter fast immer Zimmer/Fehlpreise

POS = [r"\benero\b", r"temporada", r"por meses", r"invierno", r"\b1 mes\b", r"\bun mes\b",
       r"m[ií]nimo (de )?(1|un) mes", r"corta", r"meses de invierno", r"vacacional", r"n[oó]madas?",
       r"\bmensual"]
NEG = [r"larga temporada", r"m[ií]nimo (de )?(6|seis|10|diez|11|once|12|doce|1 a[nñ]o) ?mes",
       r"m[ií]nimo (de )?(un|1) a[nñ]o", r"estudiantes", r"habitaci[oó]n (en|para)", r"compartid",
       r"\bse vende\b", r"solo (a )?(larga|todo el a[nñ]o)", r"contrato de 1 a[nñ]o", r"11 meses",
       r"hasta (el )?(\d+ de )?(diciembre|enero)", r"n[oó]mina"]


def fetch(url):
    out = subprocess.run(["curl", "-s", "-L", "--max-time", "30", "-A", UA, url],
                         capture_output=True, text=True)
    return out.stdout


def parse(html):
    m = re.search(r'window.__INITIAL_PROPS__ = JSON.parse\("((?:[^"\\]|\\.)*)"\)', html, re.S)
    if not m:
        return None
    try:
        return json.loads(json.loads('"' + m.group(1) + '"'))
    except ValueError:
        return None


def tag(ad, name):
    for t in ad.get("tags", []):
        if t.get("type") == name:
            return t.get("text")
    return None


def score(text):
    t = text.lower()
    pos = [p for p in POS if re.search(p, t)]
    neg = [n for n in NEG if re.search(n, t)]
    return len(pos) - 2 * len(neg), pos, neg


def main():
    ads = {}
    for prov, label in PROVINCES.items():
        for q in QUERIES:
            page = 1
            while True:
                url = (f"https://www.milanuncios.com/alquiler-de-viviendas-en-{prov}/"
                       f"?s={q.replace(' ', '+')}&hasta={MAX_PRICE}&desde={MIN_PRICE}&pagina={page}")
                d = parse(fetch(url))
                if not d:
                    print("WARN: keine Daten", url, file=sys.stderr)
                    break
                p = d["adListPagination"]
                for a in p["adList"]["ads"]:
                    price = (a.get("price") or {}).get("cashPrice", {}).get("value")
                    ads.setdefault(a["id"], {
                        "id": a["id"], "source": "milanuncios", "island": label,
                        "city": (a.get("city") or {}).get("name"), "title": a.get("title"),
                        "price": price, "bedrooms": tag(a, "dormitorios"), "baths": tag(a, "baños"),
                        "m2": tag(a, "metros cuadrados"), "seller": a.get("sellerType"),
                        "published": a.get("publishDate"), "updated": a.get("updateDate"),
                        "url": "https://www.milanuncios.com" + a["url"],
                        "description": a.get("description", ""), "queries": []})
                    ads[a["id"]]["queries"].append(q)
                tp = p["pagination"]["totalPages"]
                if page >= tp or page >= 12:
                    break
                page += 1
                time.sleep(random.uniform(1.0, 2.0))
            time.sleep(random.uniform(1.0, 2.0))
    res = []
    for a in ads.values():
        if a["price"] is None or not (MIN_PRICE <= a["price"] <= MAX_PRICE):
            continue
        s, pos, neg = score(a["title"] + " " + a["description"])
        a.update(score=s, pos=pos, neg=neg)
        res.append(a)
    res.sort(key=lambda a: (-a["score"], a["price"]))
    out = ROOT / "data" / "milanuncios_latest.json"
    out.write_text(json.dumps({"fetched": datetime.datetime.utcnow().isoformat() + "Z",
                               "count": len(res), "ads": res}, ensure_ascii=False, indent=1))
    print(f"{len(ads)} Anzeigen gesamt, {len(res)} im Preisrahmen -> {out}")


if __name__ == "__main__":
    main()
