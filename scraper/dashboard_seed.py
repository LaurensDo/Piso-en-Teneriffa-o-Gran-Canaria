"""Einmalig: baut data/dashboard.json (Quelle für das Dashboard) aus der Erstauswertung vom 30.09.2026."""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
fc = {a["id"]: a["url"] for a in json.load(open(ROOT / "data/fotocasa_latest.json"))["ads"]}
ma = {a["id"]: a["url"] for a in json.load(open(ROOT / "data/milanuncios_latest.json"))["ads"]}
D = "2026-09-30"


def L(*refs):
    out = []
    for r in refs:
        src, i, *label = r.split(":", 2)
        url = (fc if src == "fc" else ma)[i]
        out.append({"label": label[0] if label else ("Fotocasa" if src == "fc" else "Milanuncios"), "url": url})
    return out


rows = [
 # --- Top-Treffer ---
 dict(key="fc-184892391", tier="top", rank=1, isle="TF", place="Santa Cruz · Zentrum (Duggi/Rambla)", price=1250, priceNote="inkl. Bettwäsche und Reinigung",
      flat="2 Schlafzimmer · 80 m² · Glasfaser", terms="nur monatsweise", provider="Privat", private=True, pool=False,
      note="Inserat nennt Sommer-Gäste als Zielgruppe, Januar direkt anfragen. Schlafzimmer innenliegend (mit Fenster), kein Balkon.",
      links=L("fc:184892391")),
 dict(key="fc-187728705", tier="top", rank=2, isle="TF", place="Porís de Abona (Arico) · Südostküste", price=1200, priceNote="inkl. Wasser, Strom und WLAN",
      flat="2 Schlafzimmer: 1 Doppelbett + 2 Einzelbetten · 72 m² · Terrasse · Parkplatz", terms="mind. 1 Monat, max. 10", provider="Agentur Ifara Home",
      private=False, pool=True, note="Ruhiges Fischerdorf, Auto nötig. Agenturgebühr erfragen.", links=L("fc:187728705", "ma:560484597")),
 dict(key="ma-601957797", tier="top", rank=3, isle="TF", place="Santa Cruz · Zentrum", price=1350, priceNote="inkl. Nebenkosten",
      flat="2 Schlafzimmer: Doppelbett + Einzelbett · 70 m² · Klimaanlage", terms="mind. 1 Monat, max. 10", provider="Agentur Atrium",
      private=False, pool=False, note="Dieselbe Agentur hat eine 75-m²-Variante für 1.500 €.",
      links=L("ma:601957797", "fc:190033150", "ma:551805025:Variante 75 m²")),
 dict(key="ma-616789046", tier="top", rank=4, isle="GC", place="Las Palmas · Las Canteras (Sargento Llagas)", price=1500, priceNote="all-in: Nebenkosten, WLAN, Gemeinde",
      flat="Dachwohnung 44 m² · 2 Zimmer mit Tür: Doppelbett + kleines Bett · Meerblick", terms="1–6 Monate, flexibel nach Monaten", provider="Privat",
      private=True, pool=False, note="Ideal für 2 Personen, für 3–4 zu eng. Aufzug fährt nur bis zum 6. Stock.",
      links=L("ma:616789046", "fc:190965219")),
 dict(key="fc-183165490", tier="top", rank=5, isle="GC", place="Las Palmas · Santa Catalina / Canteras", price=1200, priceNote="",
      flat="2 Doppelzimmer · 2 Bäder · 75 m² · Balkon · Aufzug", terms="monats- oder wochenweise, max. 6 Monate", provider="Agentur RV Gestiones",
      private=False, pool=False, note="Älteres Inserat, noch online. Verfügbarkeit prüfen.", links=L("fc:183165490")),
 dict(key="ma-609226735", tier="top", rank=6, isle="GC", place="Playa de Vargas (Agüimes) · Ostküste", price=1100, priceNote="inkl. WLAN",
      flat="2 Doppelzimmer · 2 Bäder · 120 m² · Terrasse", terms="monatsweise, max. 6 Monate", provider="Agentur Falena",
      private=False, pool=False, note="Windsurf-Spot, ruhig. Auto nötig, Flughafen nah.", links=L("ma:609226735", "fc:190432876")),
 dict(key="ma-617320108", tier="top", rank=7, isle="TF", place="Santa Cruz · Residencial Anaga", price=1800, priceNote="+ Nebenkosten (Tarif für 1–3 Monate)",
      flat="Maisonette · 2 Doppelzimmer · 2 Bäder · 122 m²", terms="mind. 1 Monat · frei 08.11.–26.06.", provider="Agentur",
      private=False, pool=False, note="Grund der Befristung muss nachgewiesen werden, z. B. Telearbeit.", links=L("ma:617320108")),
 dict(key="ma-523917709", tier="top", rank=8, isle="GC", place="Las Palmas · 2 Min. zu Las Canteras", price=1800, priceNote="",
      flat="2 Schlafzimmer · 2 Bäder · 90 m² · Neubau im Souterrain", terms="monatsweise", provider="Agentur",
      private=False, pool=False, note="", links=L("ma:523917709")),
 dict(key="ma-545752732", tier="top", rank=9, isle="GC", place="Gáldar · Nordwesten", price=1950, priceNote="inkl. Nebenkosten bis 150 €",
      flat="Haus · 3 Doppelzimmer · bis 6 Personen", terms="wochen- oder monatsweise", provider="Agentur Canarias Paradise",
      private=False, pool=False, note="Liegt an der Schmerzgrenze.", links=L("ma:545752732", "fc:186729195")),
 dict(key="ma-511056649", tier="top", rank=10, isle="TF", place="El Médano · Süden", price=2000, priceNote="laut Inserat verhandelbar",
      flat="3 Schlafzimmer · 2 Bäder · 70 m²", terms="tage- oder monatsweise", provider="Agentur",
      private=False, pool=False, note="Kite- und Surfort, oft windig.", links=L("ma:511056649")),
 # --- Anfragen ---
 dict(key="fc-189764726", tier="ask", rank=11, isle="TF", place="Puerto de la Cruz · Playa Jardín", price=1350, priceNote="inkl. Nebenkosten und Internet",
      flat="2 Schlafzimmer · 120 m² · 2 Terrassen · Garage", terms="„por temporada“, Mindestdauer nicht genannt", provider="Privat",
      private=True, pool=True, note="Kontakt per WhatsApp, 1 Monat Kaution.", links=L("fc:189764726")),
 dict(key="ma-614618678", tier="ask", rank=12, isle="TF", place="Santa Cruz · Tomé Cano", price=1150, priceNote="+ Nebenkosten",
      flat="2 Schlafzimmer · 56 m² · Terrasse", terms="Kurzzeit, Konditionen nicht genannt", provider="Agentur",
      private=False, pool=True, note="Pool und Sportanlagen im Gebäude.", links=L("ma:614618678")),
 dict(key="ma-611727783", tier="ask", rank=13, isle="TF", place="Puerto de la Cruz", price=1300, priceNote="",
      flat="2 Schlafzimmer · 80 m² Privatterrasse", terms="„corta temporada“", provider="Agentur Basualto",
      private=False, pool=True, note="", links=L("ma:611727783", "fc:190562098")),
 dict(key="fc-190804977", tier="ask", rank=14, isle="TF", place="El Médano", price=1200, priceNote="",
      flat="Dachwohnung · 2 Schlafzimmer · 50 m² Terrasse · Aufzug", terms="„por temporada“", provider="Agentur Credycasa",
      private=False, pool=False, note="", links=L("fc:190804977")),
 dict(key="ma-611704711", tier="ask", rank=15, isle="TF", place="El Médano · 2 Min. zum Strand", price=1800, priceNote="",
      flat="Reihenhaus · 2 Doppelzimmer für bis zu 4 Personen · 2 Bäder · Garten", terms="nur Kurzzeit", provider="Agentur",
      private=False, pool=False, note="", links=L("ma:611704711")),
 dict(key="ma-548079410", tier="ask", rank=16, isle="TF", place="La Tejita (El Médano)", price=1900, priceNote="",
      flat="2 Schlafzimmer · 95 m² · 1. Linie · Garage", terms="„temporadas cortas“, Verfügbarkeit anfragen", provider="Agentur",
      private=False, pool=True, note="", links=L("ma:548079410")),
 dict(key="fc-190646608", tier="ask", rank=17, isle="TF", place="Candelaria · Playa La Viuda", price=950, priceNote="+ Nebenkosten (gering)",
      flat="1 Schlafzimmer + Schlafsofa · 50 m² · Blick auf den Hafen", terms="1–3 Monate", provider="Privat",
      private=True, pool=False, note="Nur für 2 Personen geeignet (Bett + Schlafsofa).", links=L("fc:190646608")),
 dict(key="fc-190896168", tier="ask", rank=18, isle="GC", place="San Agustín · Playa del Águila", price=900, priceNote="",
      flat="2 Schlafzimmer · 55 m² · 1. Linie · Aufzug", terms="Saisonmiete bis Mai 2027, Mindestdauer nicht genannt", provider="Agentur J. C. Domínguez",
      private=False, pool=True, note="Für die Lage sehr günstig. Konditionen genau prüfen.", links=L("fc:190896168")),
 dict(key="fc-190860881", tier="ask", rank=19, isle="GC", place="Las Palmas · Santa Catalina", price=1050, priceNote="",
      flat="2 Schlafzimmer · 78 m²", terms="„de forma temporal“", provider="Agentur Remax",
      private=False, pool=False, note="", links=L("fc:190860881")),
 dict(key="fc-190683345", tier="ask", rank=20, isle="GC", place="Ingenio (Sequero)", price=800, priceNote="",
      flat="Chalet · 2 Schlafzimmer · 198 m²", terms="„alquilo por meses“", provider="Privat",
      private=True, pool=False, note="Sehr knappe Beschreibung. Fotos und Konditionen erfragen.", links=L("fc:190683345")),
 dict(key="ma-567291248", tier="ask", rank=21, isle="GC", place="Bahía Feliz · Las Pitas", price=1400, priceNote="+ 1 Monatsmiete Agenturgebühr", estMonth=2800,
      flat="2 Schlafzimmer: Doppel + Einzel (Durchgangszimmer) · Garten", terms="frei bis 31.03.2027", provider="Agentur",
      private=False, pool=False, note="Mit Gebühr real ca. 2.800 € für einen Monat. Nur interessant, wenn die Gebühr entfällt.", links=L("ma:567291248")),
 dict(key="ma-512279795", tier="ask", rank=22, isle="TF", place="Las Galletas / Golf del Sur (Inmogestión)", price=1000, priceNote="ab, + Gebühr ≈ 1 Monatsmiete + 150 € NK + 155 € Reinigung", estMonth=2300,
      flat="mehrere Wohnungen mit 2 Schlafzimmern, meist mit Pool", terms="nur Kurzzeit, Termine je Wohnung", provider="Agentur Inmogestión Tenerife",
      private=False, pool=True, note="Real ca. 2.300 € und mehr für einen Monat.", links=L("ma:512279795:Las Galletas 1.000 €", "ma:508937302:Golf del Sur 1.500 €")),
 # --- Aussortiert ---
 dict(key="fc-190947360", tier="out", rank=30, isle="TF", place="Torviscas (Adeje)", price=850, flat="2 Schlafzimmer · 120 m² · Pool", provider="Privat",
      note="Betrugsverdacht: weit unter Marktpreis, Text wie aus einem Airbnb-Inserat kopiert. Niemals vorab überweisen.", links=L("fc:190947360")),
 dict(key="fc-190441366", tier="out", rank=31, isle="GC", place="Puerto Rico (Mogán)", price=1500, flat="1 Schlafzimmer · 80 m²", provider="Privat",
      note="Für genau 1 Monat 2.200 € (1.500 € nur bei langer Miete).", links=L("fc:190441366")),
 dict(key="ma-581485755", tier="out", rank=32, isle="GC", place="Telde · La Garita", price=900, flat="2 Schlafzimmer · 75 m²", provider="Agentur Surinka",
      note="Nur für Lehrer und Gesundheitspersonal, max. 2 Personen.", links=L("ma:581485755")),
 dict(key="fc-184882441", tier="out", rank=33, isle="TF", place="Cabo Blanco (Inmogestión)", price=1050, flat="2 Schlafzimmer · 73 m² · Pool", provider="Agentur",
      note="Nur bis 08.01.2027 frei.", links=L("fc:184882441")),
 dict(key="ma-616584519", tier="out", rank=34, isle="GC", place="Mogán", price=1600, flat="1 Schlafzimmer · 45 m²", provider="Agentur",
      note="Erst ab 10.01.2027 frei, nur 1 Schlafzimmer.", links=L("ma:616584519")),
 dict(key="ma-617075724", tier="out", rank=35, isle="TF", place="San Miguel de Abona · Finca mit Privatpool", price=2000, flat="3 Schlafzimmer · 182 m²", provider="Agentur",
      note="Erst ab 18.01.2027 frei.", links=L("ma:617075724")),
 dict(key="ma-615300358", tier="out", rank=36, isle="GC", place="Agaete", price=1200, flat="2 Schlafzimmer · 105 m²", provider="Agentur",
      note="Erst ab 08.01.2027 und mindestens 3 Monate.", links=L("ma:615300358")),
 dict(key="fc-190641045", tier="out", rank=37, isle="GC", place="Melenara (Telde)", price=1300, flat="2 Schlafzimmer · 65 m² · am Strand", provider="Agentur",
      note="Nur Wintersaison, mindestens 5 Monate.", links=L("fc:190641045")),
]
for r in rows:
    r.setdefault("priceNote", ""); r.setdefault("terms", ""); r.setdefault("private", r.get("provider") == "Privat"); r.setdefault("pool", False)
    r.update(firstSeen=D, lastSeen=D, online=True, priceHistory=[])
meta = {"lastUpdate": D, "firstRun": D, "screened": 3145, "sources": ["Milanuncios", "Fotocasa"]}
(ROOT / "data/dashboard.json").write_text(json.dumps({"meta": meta, "listings": rows}, ensure_ascii=False, indent=1))
print(len(rows), "Einträge")
