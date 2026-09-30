"""Täglicher Lauf: Portale abrufen, filtern, mit data/seen.json abgleichen und neue
Kandidaten nach data/neu/YYYY-MM-DD.md schreiben (zur manuellen Prüfung).

Aufruf: python3 scraper/daily.py            (holt frische Daten, ~7 Min.)
        python3 scraper/daily.py --no-fetch (nutzt vorhandene *_latest.json)
"""
import datetime, json, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scraper"))
from filter import OTHER_RE, SHORT, STRONG, LONGONLY, snippet  # noqa: E402

TODAY = datetime.date.today().isoformat()
SEEN = ROOT / "data" / "seen.json"


def load(name):
    p = ROOT / "data" / f"{name}_latest.json"
    return json.load(open(p))["ads"] if p.exists() else []


def on_target_island(a):
    if a["source"] == "fotocasa":
        return a.get("county") in ("Tenerife", "Gran Canaria")
    return not OTHER_RE.search((a.get("city") or "").lower())


def classify(a):
    """None = uninteressant, sonst 'A' (explizit 1 Monat möglich + >=2 Zi.) oder 'B' (anfragen)."""
    if not (a.get("bedrooms") or a.get("m2")):
        return None  # keine Wohnung (Möbel, Handys ...)
    if a.get("price") is None or not 450 <= a["price"] <= 2000:
        return None
    t = ((a.get("title") or "") + " " + a.get("description", "")).lower()
    explicit_1m = re.search(r"m[ií]nim[oa] (de )?(1|un|una?) mes|(de|entre) (1|un) a \d+ meses", t)
    if not explicit_1m and any(re.search(p, t) for p in LONGONLY):
        return None
    strong = [p for p in STRONG if re.search(p, t)]
    short = [p for p in SHORT if re.search(p, t)]
    beds = int(a.get("bedrooms") or 0)
    a["_strong"], a["_short"] = strong, short
    if strong and beds >= 2:
        return "A"
    if strong or ((short or a.get("temporary")) and beds >= 2):
        return "B"
    return None


def main():
    if "--no-fetch" not in sys.argv:
        for s in ("milanuncios.py", "fotocasa.py"):
            subprocess.run([sys.executable, str(ROOT / "scraper" / s)], check=False)
    seen = json.load(open(SEEN)) if SEEN.exists() else {}
    new = []
    for a in load("milanuncios") + load("fotocasa"):
        if not on_target_island(a):
            continue
        cls = classify(a)
        if not cls:
            continue
        key = f"{a['source']}:{a['id']}"
        if key in seen:
            if seen[key].get("price") != a["price"]:
                seen[key].setdefault("price_history", []).append([TODAY, a["price"]])
                seen[key]["price"] = a["price"]
            seen[key]["last_seen"] = TODAY
            continue
        seen[key] = {"first_seen": TODAY, "last_seen": TODAY, "price": a["price"], "class": cls,
                     "url": a["url"], "city": a.get("city")}
        a["_class"] = cls
        new.append(a)
    SEEN.write_text(json.dumps(seen, ensure_ascii=False, indent=1, sort_keys=True))
    out_dir = ROOT / "data" / "neu"
    out_dir.mkdir(exist_ok=True)
    new.sort(key=lambda a: (a["_class"], a["price"]))
    lines = [f"# Neue Kandidaten {TODAY} ({len(new)})\n"]
    for a in new:
        lines.append(f"## [{a['_class']}] {a.get('city')} {a.get('zone') or ''} – {a['price']} € – "
                     f"{a.get('bedrooms')} Zi. – {str(a.get('m2')).replace(' m²', '')} m² – {a.get('seller')} {a.get('agency') or ''}")
        lines.append(a["url"])
        pats = (a["_strong"] or a["_short"])[:3]
        for s in (snippet(a["description"], pats, 140) if pats else [a["description"][:400]]):
            lines.append("> " + s.replace("\n", " "))
        lines.append("")
    out = out_dir / f"{TODAY}.md"
    if new:  # bei mehreren Läufen am selben Tag anhängen statt überschreiben
        with open(out, "a") as f:
            f.write(("\n" if out.exists() and out.stat().st_size else "") + "\n".join(lines))
    print(f"{len(new)} neue Kandidaten -> data/neu/{TODAY}.md  (bekannt: {len(seen)})")


if __name__ == "__main__":
    main()
