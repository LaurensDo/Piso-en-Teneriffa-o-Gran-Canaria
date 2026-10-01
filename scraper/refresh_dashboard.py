"""Hält bestehende Dashboard-Einträge aktuell (nach scraper/daily.py ausführen).

- Eintrag in den heutigen Suchergebnissen -> lastSeen = heute, listPrice = Preis im Inseratskopf
- fehlt er dort, wird die Detailseite geprüft (Fotocasa liefert nicht jeden Tag alle Treffer)
- listPrice geändert -> Meldung + priceHistory (die Kosten-Felder prüft man dann von Hand,
  weil price/total teils aus dem Inseratstext stammen, z. B. Tarif für 1 Monat)
- seit > 2 Tagen nicht gesehen -> online = False
Gibt geänderte Keys als JSON-Liste nach stdout (letzte Zeile) aus.
"""
import datetime, json, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
TODAY = datetime.date.today().isoformat()
latest = {}
for name, prefix in (("fotocasa", "fc-"), ("milanuncios", "ma-")):
    for a in json.load(open(ROOT / "data" / f"{name}_latest.json"))["ads"]:
        latest[prefix + a["id"]] = a


def detail_price(url):
    """Preis von der Detailseite, None wenn das Inserat dort nicht (mehr) auftaucht."""
    h = subprocess.run(["curl", "-s", "-L", "--max-time", "25", "-A", UA, url], capture_output=True, text=True, errors="ignore").stdout
    lid = re.search(r"(\d{6,})(?:/d|\.htm)$", url).group(1)
    if lid not in h:
        return None
    if "fotocasa" in url:
        seg = h[h.find('"realEstate":{'):][:60000]
        m = re.search(r'"rawPrice":(\d+)', seg) or re.search(r'"price":(\d+)', seg)
    else:
        m = re.search(r'"cashPrice":\{"value":(\d+)', h.replace('\\"', '"'))
    return int(m.group(1)) if m else -1


path = ROOT / "data" / "dashboard.json"
d = json.load(open(path))
changed = set()
for l in d["listings"]:
    a = latest.get(l["key"])
    price = a["price"] if a else detail_price(l["links"][0]["url"])
    if price is not None:
        if l.get("lastSeen") != TODAY:
            l["lastSeen"] = TODAY; changed.add(l["key"])
        if not l.get("online", True):
            l["online"] = True; changed.add(l["key"])
        if price > 0:
            old = l.get("listPrice")
            if old is not None and old != price:
                l.setdefault("priceHistory", []).append([TODAY, old])
                print(f"PREISÄNDERUNG {l['key']} {l['place']}: {old} -> {price} € (Kosten prüfen)", file=sys.stderr)
            if old != price:
                l["listPrice"] = price; changed.add(l["key"])
    else:
        print(f"NICHT GEFUNDEN {l['key']} {l['place']} (zuletzt {l['lastSeen']})", file=sys.stderr)
    days = (datetime.date.fromisoformat(TODAY) - datetime.date.fromisoformat(l["lastSeen"])).days
    if days > 2 and l.get("online", True):
        l["online"] = False; changed.add(l["key"])
        print(f"OFFLINE {l['key']} {l['place']}", file=sys.stderr)
path.write_text(json.dumps(d, ensure_ascii=False, indent=1))
print(json.dumps(sorted(changed)))
