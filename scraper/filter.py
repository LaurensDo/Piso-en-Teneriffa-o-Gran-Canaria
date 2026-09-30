"""Filtert data/milanuncios_latest.json auf Teneriffa/Gran Canaria und Kurzzeit-Signale."""
import json, re, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OTHER_RE = re.compile(r"\b(" + "|".join(re.escape(x) for x in
    ["arrecife", "barcelona", "valencia", "caldereta", "castillo de caleta", "corralejo", "costa teguise",
     "esquinzo", "la antigua", "teguise", "la oliva", "la santa", "lajares", "montaña blanca", "morro jable",
     "pajara", "playa blanca", "playa honda", "puerto del carmen", "puerto del rosario", "tuineje",
     "casas de la guirra", "guime", "tajaste", "guisguey", "gran tarajal", "yaiza", "tias", "haria",
     "alajero", "alojera", "playa de santiago", "gomera", "hermigua", "vallehermoso", "valle gran rey",
     "barlovento", "breña", "el paso", "retamar", "san andres y sauces", "santa cruz de la palma",
     "las indias", "tazacorte", "fuencaliente", "puntagorda", "garafia", "tijarafe"]) + r")\b")

STRONG = [r"m[ií]nim[oa] (de )?(1|un|una?) mes", r"desde (1|un) mes", r"(de|entre) (1|un|15 d[ií]as) a \d+ meses",
          r"por meses", r"estancias? mensual", r"\bpor mes(es)? o\b", r"tanto por d[ií]as como por meses",
          r"(1|un) mes (o|y) m[aá]s"]
SHORT = [r"m[ií]nimo (de )?(1|un|una?) mes", r"desde (1|un) mes", r"por meses", r"de (1|un) a \d+ meses",
         r"estancias? (cortas?|de (1|un) mes|mensual)", r"temporadas? cortas?", r"corta temporada",
         r"\benero\b", r"meses de invierno", r"temporada de invierno", r"invierno", r"n[oó]madas? digital",
         r"(1|un|uno|dos|2|3|tres) meses?\b.{0,40}(m[aá]ximo|min)", r"alquiler temporal", r"por semanas"]
LONGONLY = [r"larga temporada", r"(estancia|duraci[oó]n|per[ií]odo) m[ií]nim[oa] (de )?(2|dos|3|tres|4|cuatro|5|cinco|6|seis)\b",
            r"m[ií]nimo (de )?(2|dos|3|tres) meses", r"(estancias?|alquiler|duraci[oó]n|per[ií]odo) (de|entre) (3|tres|4|cuatro|5|cinco|6|seis) a \d+ meses",
            r"curso escolar", r"(septiembre|octubre) a (junio|julio)", r"m[ií]nimo (de )?(3|tres|4|cuatro|5|cinco|6|seis|10|diez|11|once|12|doce) ?mes",
            r"m[ií]nimo (de )?(un|1) a[nñ]o", r"(curso|a[nñ]o) (escolar|acad[eé]mico)", r"estudiantes",
            r"contrato (de )?(1|un) a[nñ]o", r"\b11 meses", r"hasta (el )?(\d+ de )?(diciembre|enero)",
            r"n[oó]mina", r"habitaci[oó]n (en|para)", r"compartid", r"\bse vende\b",
            r"(desde|a partir de|disponible) (el )?(\d+ de )?(febrero|marzo|abril)"]


def snippet(text, pats, w=90):
    out = []
    for p in pats:
        for m in re.finditer(p, text, re.I):
            s, e = max(0, m.start() - w), min(len(text), m.end() + w)
            out.append("…" + text[s:e].replace("\n", " ") + "…")
            break
    return out


def run(min_short=1):
    d = json.load(open(ROOT / "data" / "milanuncios_latest.json"))
    res = []
    for a in d["ads"]:
        city = (a["city"] or "").lower()
        text = (a["title"] + " " + a["description"])
        if OTHER_RE.search(city):
            continue
        tl = text.lower()
        short = [p for p in SHORT if re.search(p, tl)]
        long_ = [p for p in LONGONLY if re.search(p, tl)]
        if len(short) < min_short:
            continue
        a["short"], a["long"] = short, long_
        res.append(a)
    res.sort(key=lambda a: (len(a["long"]) > 0, -len(a["short"]), a["price"]))
    return res


if __name__ == "__main__":
    res = run()
    print(len(res), "Kandidaten,", sum(1 for a in res if not a["long"]), "ohne Langzeit-Signal")
    for a in res:
        if a["long"] and "-a" not in sys.argv:
            continue
        print(f"\n### {a['id']} | {a['island'][:5]} | {a['city']} | {a['price']}€ | dorm={a['bedrooms']} | {a['m2']} | {a['seller']} | upd {a['updated'][:10]}")
        print("short:", a["short"], "long:", a["long"])
        for s in snippet(a["description"], a["short"][:3] + a["long"][:2], 110):
            print("  ", s)
