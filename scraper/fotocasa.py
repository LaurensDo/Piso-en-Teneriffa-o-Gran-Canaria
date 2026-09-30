"""Holt alle Mietangebote <= 2000 EUR von Fotocasa (Provinzen Santa Cruz de Tenerife + Las Palmas).
Ausgabe: data/fotocasa_latest.json   Aufruf: python3 scraper/fotocasa.py
"""
import json, re, time, random, subprocess, sys, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
PROVINCES = {"santa-cruz-de-tenerife-provincia": "Teneriffa", "las-palmas-provincia": "Gran Canaria (Prov. Las Palmas)"}
MIN_PRICE, MAX_PRICE = 450, 2000


def fetch(url):
    return subprocess.run(["curl", "-s", "-L", "--max-time", "30", "-A", UA, url],
                          capture_output=True, text=True).stdout


def parse(html):
    m = re.search(r'<script[^>]*id="__initial_props__"[^>]*>(.*?)</script>', html, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))["initialSearch"]["result"]
    except (ValueError, KeyError):
        return None


def feat(x, key):
    for f in x.get("features", []):
        if f.get("key") == key:
            return f.get("value")
    return None


def main():
    ads = {}
    for slug, label in PROVINCES.items():
        page = 1
        while True:
            suffix = "" if page == 1 else f"/{page}"
            url = (f"https://www.fotocasa.es/es/alquiler/viviendas/{slug}/todas-las-zonas/l{suffix}"
                   f"?minPrice={MIN_PRICE}&maxPrice={MAX_PRICE}")
            r = parse(fetch(url))
            if not r or not r.get("realEstates"):
                if not r:
                    print("WARN: keine Daten", url, file=sys.stderr)
                break
            for x in r["realEstates"]:
                a = x.get("address") or {}
                det = (x.get("detail") or {}).get("es-ES", "")
                ads[str(x["id"])] = {
                    "id": str(x["id"]), "source": "fotocasa", "island": label,
                    "county": a.get("county"), "city": a.get("municipality") or a.get("city"),
                    "zone": a.get("neighborhood") or a.get("district"),
                    "title": x.get("buildingSubtype"), "price": x.get("rawPrice"),
                    "bedrooms": feat(x, "rooms"), "baths": feat(x, "bathrooms"), "m2": feat(x, "surface"),
                    "seller": x.get("clientType"), "agency": x.get("clientAlias"),
                    "temporary": x.get("isTemporaryRental"),
                    "published": datetime.datetime.utcfromtimestamp(
                        (x.get("dateOriginal") or {}).get("timestamp", 0) / 1000).isoformat() + "Z",
                    "url": "https://www.fotocasa.es" + det, "description": x.get("description") or ""}
            total = r.get("count", 0)
            if page * 30 >= total or page >= 60:
                break
            page += 1
            time.sleep(random.uniform(1.0, 2.0))
    out = ROOT / "data" / "fotocasa_latest.json"
    res = sorted(ads.values(), key=lambda a: a["price"] or 0)
    out.write_text(json.dumps({"fetched": datetime.datetime.utcnow().isoformat() + "Z",
                               "count": len(res), "ads": res}, ensure_ascii=False, indent=1))
    print(f"{len(res)} Anzeigen -> {out}")


if __name__ == "__main__":
    main()
