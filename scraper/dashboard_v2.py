"""Einmalig (30.09.2026): Dashboard-Daten mit Gesamtkosten (harte Grenze 2.000 € inkl. Makler)
und Radlage neu aufbauen. Kosten-Regeln:
  NK nicht inklusive -> +80 € geschätzt; übliche Maklergebühr bei Saisonmiete = 1 Monatsmiete + 7 % IGIC.
  total = sichere Kosten ohne unbekannte Gebühr; feeUnknown -> worstTotal = total + Standardgebühr,
  maxFee = 2000 - total (höchste Gebühr, bei der es noch passt).
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
fc = {a["id"]: a["url"] for a in json.load(open(ROOT / "data/fotocasa_latest.json"))["ads"]}
ma = {a["id"]: a["url"] for a in json.load(open(ROOT / "data/milanuncios_latest.json"))["ads"]}
D = "2026-09-30"
NK = 80
FEE = lambda rent: round(rent * 1.07)

BIKE = {
    "arona": "Liegt auf ca. 600 m direkt an der Straße über Vilaflor zum Teide.",
    "adeje": "Sonniger Südwesten. Anstiege nach Ifonche, Vilaflor und zum Teide ab Adeje.",
    "west": "Westküste. Der Anstieg über Chío zum Teide beginnt fast vor der Tür.",
    "golfsur": "Flacher Süden nahe Flughafen. Anstiege über San Miguel nach Vilaflor.",
    "gcsur": "Klassisches Winter-Radrevier: Fataga-Anstieg und Touren nach Soria oder Cerana ab Haustür.",
    "orotava": "Nordküste. Teide-Anstieg über La Orotava, im Januar aber öfter wolkig und feucht.",
    "gcost": "Ostküste, windig. Anstiege nach Agüimes, Temisas und Cazadores in der Nähe.",
    "medano": "Sehr windig. Anstiege über Granadilla nach Vilaflor.",
    "galdar": "Nordwesten. Küstenstraße nach Agaete und Anstieg nach Artenara, oft bewölkt.",
    "sc": "Stadtlage. Erst hoch nach La Laguna, dann Anaga oder über La Esperanza zum Teide.",
    "lpgc": "Stadtlage im wolkigeren Norden. Bis zu den Anstiegen erst durch die Stadt.",
    "candelaria": "Ostküste, windig. Anstieg über Arafo zum Teide in der Nähe.",
}


def L(*refs):
    out = []
    for r in refs:
        src, i, *label = r.split(":", 2)
        out.append({"label": label[0] if label else ("Fotocasa" if src == "fc" else "Milanuncios"),
                    "url": (fc if src == "fc" else ma)[i]})
    return out


def cost(rent, nk_incl, fee):
    """fee: 0 (keine), Zahl (bekannt) oder None (unbekannt)."""
    total = rent + (0 if nk_incl else NK) + (fee or 0)
    c = {"price": rent, "total": total, "feeUnknown": fee is None}
    parts = [f"Miete {rent:,} €".replace(",", ".")]
    parts.append("NK inklusive" if nk_incl else f"NK ca. {NK} € (geschätzt)")
    if fee is None:
        c["worstTotal"] = total + FEE(rent)
        c["maxFee"] = max(0, 2000 - total)
        parts.append("Maklergebühr unbekannt")
    elif fee:
        parts.append(f"Gebühr {fee:,} €".replace(",", "."))
    else:
        parts.append("keine Maklergebühr")
    c["costNote"] = " · ".join(parts)
    return c


rows = []
def add(key, tier, rank, isle, place, flat, terms, provider, bike, bikeKey, links, rent, nk_incl, fee, note="", pool=False, priceNote=""):
    r = dict(key=key, tier=tier, rank=rank, isle=isle, place=place, flat=flat, terms=terms, provider=provider,
             private=provider == "Privat", pool=pool, bike=bike, bikeNote=BIKE[bikeKey], note=note, links=links, priceNote=priceNote)
    r.update(cost(rent, nk_incl, fee))
    rows.append(r)

P = "Privat"
# ---------- TOP: 1 Monat ausdrücklich möglich, >= 2 getrennte Betten, Gesamtkosten sicher <= 2.000 € ----------
add("fc-189634737", "top", 1, "TF", "Arona-Ort · Finca im Süden", "2 Schlafzimmer · Garten · Pool · Parkplatz", "mind. 1 Monat, max. 2 Monate", P,
    "top", "arona", L("fc:189634737"), 1500, False, 0, pool=True,
    note="Im Inseratskopf stehen 1.300 €, im Text 1.500 €. Ich rechne mit 1.500 €. Laut Anbieter ist eventuell auch ein Auto verfügbar.")
add("ma-599524316", "top", 2, "TF", "Costa Adeje · San Eugenio", "3 Schlafzimmer · 2 Bäder · 82 m² · Pool", "ganzer Monat 1.200 €, auch wochenweise", P,
    "top", "adeje", L("ma:599524316"), 1200, True, 0, pool=True,
    note="Ferienwohnung mit Preisliste (Woche 450 €, Monat 1.200 €). Frag, ob der Monatspreis auch im Januar gilt.")
add("fc-184892391", "top", 3, "TF", "Santa Cruz · Zentrum (Duggi/Rambla)", "2 Schlafzimmer · 80 m² · Glasfaser", "nur monatsweise", P,
    "stadt", "sc", L("fc:184892391"), 1250, False, 0, priceNote="inkl. Bettwäsche und Reinigung",
    note="Laut Inserat ausdrücklich ohne Agenturkosten. Richtet sich an Sommer-Gäste, Januar anfragen. Kein Balkon.")
add("ma-616789046", "top", 4, "GC", "Las Palmas · Las Canteras (Sargento Llagas)", "Dachwohnung 44 m² · 2 Zimmer mit Tür: Doppelbett + kleines Bett · Meerblick",
    "1–6 Monate, flexibel nach Monaten", P, "stadt", "lpgc", L("ma:616789046", "fc:190965219"), 1500, True, 0,
    note="All-in-Preis. Ideal für 2, für 3–4 zu eng. Aufzug nur bis zum 6. Stock.")

# ---------- ANFRAGEN: Budget passt im besten Fall; Mindestdauer, Januar oder Gebühr offen ----------
add("fc-190896168", "ask", 5, "GC", "San Agustín · Playa del Águila", "2 Schlafzimmer · 55 m² · 1. Linie · Aufzug", "Saisonmiete bis Mai 2027, Mindestdauer nicht genannt",
    "Agentur J. C. Domínguez", "top", "gcsur", L("fc:190896168", "ma:615962722"), 900, False, None, pool=True,
    note="Selbst mit voller Maklergebühr knapp unter 2.000 €. Wasser und Internet inklusive, Strom extra.")
add("ma-597057750", "ask", 6, "TF", "Alcalá (Guía de Isora) · Westküste", "2 Schlafzimmer · 75 m² · sonniger Patio", "„nur Saisonvertrag“, Mindestdauer nicht genannt",
    "Agentur", "top", "west", L("ma:597057750"), 900, False, None, note="Selbst mit voller Maklergebühr knapp unter 2.000 €.")
add("fc-190706321", "ask", 7, "TF", "Las Chafiras (San Miguel) · Süden", "2 Zimmer · 49 m² · kleine Terrasse", "ab 1. Oktober, max. 6 Monate", P,
    "top", "golfsur", L("fc:190706321"), 795, False, 0, note="Sehr günstig. Frag, ob ein einzelner Monat geht; verlangt werden Kaution plus Vorauszahlung.")
add("ma-588831375", "ask", 8, "TF", "Playa San Juan · Westküste", "2 große Schlafzimmer · 80 m² · 40 m² Terrasse", "„apartamento de temporada“, Mindestdauer nicht genannt", P,
    "top", "west", L("ma:588831375"), 1290, False, 0)
add("fc-190149538", "ask", 9, "GC", "Maspalomas · San Fernando", "Maisonette · 2 Doppelzimmer + Ankleide · 80 m² · Sonnenterrasse", "„por temporada“, Mindestdauer nicht genannt", P,
    "top", "gcsur", L("fc:190149538", "fc:190225975:Fotocasa (2. Inserat)"), 1400, True, 0, note="Wasser und Strom bis 80 € inklusive.")
add("fc-188831802", "ask", 10, "GC", "Playa del Inglés · San Fernando", "2 Schlafzimmer · 75 m² · Parkplatz · Aufzug", "Mindestdauer nicht genannt", P,
    "top", "gcsur", L("fc:188831802"), 1500, True, 0, pool=True, note="Strom, Wasser, WLAN und Klimaanlage inklusive.")
add("fc-190961945", "ask", 11, "GC", "Maspalomas · Meloneras", "Bungalow-Maisonette · 2 Zimmer · 2 Bäder · Terrasse", "frei 01.10.–30.06., Mindestdauer nicht genannt", P,
    "top", "gcsur", L("fc:190961945", "ma:617080918"), 1500, False, 0, pool=True)
add("fc-189348450", "ask", 12, "TF", "Playa de las Américas · Compostela Beach", "2 Doppelzimmer · 75 m² · Terrasse", "Mindestdauer nicht genannt", P,
    "top", "adeje", L("fc:189348450"), 1650, False, 0, pool=True)
add("fc-184074438", "ask", 13, "GC", "Playa del Inglés · Strand-Bungalow", "2 Schlafzimmer · 70 m² · Solarium · Garage", "Winterpreis 2.000 €/Monat", P,
    "top", "gcsur", L("fc:184074438"), 2000, True, 0, pool=True, note="Passt nur, wenn Nebenkosten im Winterpreis enthalten sind. Nachfragen.")
add("fc-190149392", "ask", 14, "GC", "Playa del Inglés · nahe Yumbo", "1 Schlafzimmer + Schlafsofa · 40 m²", "Mindestdauer nicht genannt", P,
    "top", "gcsur", L("fc:190149392"), 1000, True, 0, pool=True, note="Nur für 2 Personen (Bett + Schlafsofa). Fahrradverleih 2 Minuten entfernt.")
add("fc-189764726", "ask", 15, "TF", "Puerto de la Cruz · Playa Jardín", "2 Schlafzimmer · 120 m² · 2 Terrassen · Garage", "„por temporada“, Mindestdauer nicht genannt", P,
    "gut", "orotava", L("fc:189764726"), 1350, True, 0, pool=True, note="Kontakt per WhatsApp, 1 Monat Kaution.")
add("fc-190683345", "ask", 16, "GC", "Ingenio (Sequero)", "Chalet · 2 Schlafzimmer · 198 m²", "„alquilo por meses“", P,
    "gut", "gcost", L("fc:190683345"), 800, False, 0, note="Sehr knappe Beschreibung. Fotos und Konditionen erfragen.")
add("ma-609226735", "ask", 17, "GC", "Playa de Vargas (Agüimes)", "2 Doppelzimmer · 2 Bäder · 120 m² · Terrasse", "monatsweise, max. 6 Monate",
    "Agentur Falena", "gut", "gcost", L("ma:609226735", "fc:190432876"), 1100, True, None,
    note="Gebühr wird im Inserat nicht erwähnt (nur Kaution). Nachfragen.")
add("fc-190646608", "ask", 18, "TF", "Candelaria · Playa La Viuda", "1 Schlafzimmer + Schlafsofa · 50 m²", "1–3 Monate", P,
    "stadt", "candelaria", L("fc:190646608"), 950, False, 0, note="Nur für 2 Personen (Bett + Schlafsofa).")
add("ma-601957797", "ask", 19, "TF", "Santa Cruz · Zentrum", "2 Schlafzimmer: Doppelbett + Einzelbett · 70 m² · Klimaanlage", "mind. 1 Monat, max. 10",
    "Agentur Atrium", "stadt", "sc", L("ma:601957797", "fc:190033150", "ma:551805025:Variante 75 m² (1.500 €)"), 1350, True, None)
add("fc-183165490", "ask", 20, "GC", "Las Palmas · Santa Catalina / Canteras", "2 Doppelzimmer · 2 Bäder · 75 m² · Balkon", "monats- oder wochenweise, max. 6 Monate",
    "Agentur RV Gestiones", "stadt", "lpgc", L("fc:183165490"), 1200, False, None)
add("ma-614618678", "ask", 21, "TF", "Santa Cruz · Tomé Cano", "2 Schlafzimmer · 56 m² · Terrasse", "Kurzzeit, Konditionen nicht genannt",
    "Agentur", "stadt", "sc", L("ma:614618678"), 1150, False, None, pool=True)
add("ma-611727783", "ask", 22, "TF", "Puerto de la Cruz", "2 Schlafzimmer · 80 m² Privatterrasse", "„corta temporada“",
    "Agentur Basualto", "gut", "orotava", L("ma:611727783", "fc:190562098"), 1300, False, None, pool=True)
add("fc-190804977", "ask", 23, "TF", "El Médano", "Dachwohnung · 2 Schlafzimmer · 50 m² Terrasse", "„por temporada“",
    "Agentur Credycasa", "gut", "medano", L("fc:190804977"), 1200, False, None)
add("fc-190860881", "ask", 24, "GC", "Las Palmas · Santa Catalina", "2 Schlafzimmer · 78 m²", "„de forma temporal“",
    "Agentur Remax", "stadt", "lpgc", L("fc:190860881"), 1050, False, None)
add("ma-617320108", "ask", 25, "TF", "Santa Cruz · Residencial Anaga", "Maisonette · 2 Doppelzimmer · 2 Bäder · 122 m²", "mind. 1 Monat · frei 08.11.–26.06.",
    "Agentur", "stadt", "sc", L("ma:617320108"), 1800, False, None, note="Tarif für 1–3 Monate. Passt nur ohne Maklergebühr.")
add("ma-523917709", "ask", 26, "GC", "Las Palmas · nahe Las Canteras", "2 Schlafzimmer · 2 Bäder · 90 m²", "monatsweise",
    "Agentur", "stadt", "lpgc", L("ma:523917709"), 1800, False, None, note="Passt nur ohne Maklergebühr.")
add("ma-545752732", "ask", 27, "GC", "Gáldar · Nordwesten", "Haus · 3 Doppelzimmer · bis 6 Personen", "wochen- oder monatsweise",
    "Agentur Canarias Paradise", "gut", "galdar", L("ma:545752732", "fc:186729195"), 1950, True, None, note="NK bis 150 € inklusive. Passt nur ohne Maklergebühr.")
add("ma-511056649", "ask", 28, "TF", "El Médano", "3 Schlafzimmer · 2 Bäder · 70 m²", "tage- oder monatsweise",
    "Agentur", "gut", "medano", L("ma:511056649"), 2000, True, None, note="Laut Inserat verhandelbar. Passt nur ohne Gebühr oder mit Rabatt.")
add("ma-611704711", "ask", 29, "TF", "El Médano · 2 Min. zum Strand", "Reihenhaus · 2 Doppelzimmer für bis zu 4 Personen · Garten", "nur Kurzzeit",
    "Agentur", "gut", "medano", L("ma:611704711"), 1800, False, None, note="Passt nur ohne Maklergebühr.")

# ---------- AUSSORTIERT ----------
def out(key, rank, isle, place, flat, provider, bike, bikeKey, links, rent, nk, fee, note):
    add(key, "out", rank, isle, place, flat, "", provider, bike, bikeKey, links, rent, nk, fee, note=note)

out("fc-187728705", 40, "TF", "Porís de Abona (Arico)", "2 Schlafzimmer · 72 m² · Pool", "Agentur Ifara Home", "gut", "medano",
    L("fc:187728705", "ma:560484597"), 1200, True, FEE(1200), "Über dem Limit: Die Agentur verlangt 1 Monatsmiete Gebühr + IGIC, gesamt ca. 2.480 €.")
out("ma-567291248", 41, "GC", "Bahía Feliz · Las Pitas", "2 Schlafzimmer · Garten", "Agentur", "top", "gcsur",
    L("ma:567291248"), 1400, True, FEE(1400), "Über dem Limit: 1 Monatsmiete Gebühr + IGIC, gesamt ca. 2.900 €.")
out("ma-512279795", 42, "TF", "Las Galletas / Golf del Sur (Inmogestión)", "mehrere Wohnungen mit 2 Schlafzimmern", "Agentur Inmogestión", "top", "golfsur",
    L("ma:512279795:Las Galletas 1.000 €", "ma:508937302:Golf del Sur 1.500 €"), 1000, True, FEE(1000) + 100 + 139,
    "Über dem Limit: Gebühr ≈ 1 Monatsmiete + 100 € NK-Pauschale + 139 € Endreinigung, gesamt ab ca. 2.310 €.")
out("ma-548079410", 43, "TF", "La Tejita (El Médano)", "2 Schlafzimmer · 1. Linie · Pool", "Agentur", "gut", "medano",
    L("ma:548079410"), 1900, False, None, "Schon ohne Gebühr mit Nebenkosten an der Grenze, mit jeder Gebühr darüber.")
out("fc-190947360", 44, "TF", "Torviscas (Adeje)", "2 Schlafzimmer · 120 m² · Pool", P, "top", "adeje",
    L("fc:190947360"), 850, True, 0, "Betrugsverdacht: weit unter Marktpreis, Text wie aus einem Airbnb-Inserat kopiert. Niemals vorab überweisen.")
out("fc-190441366", 45, "GC", "Puerto Rico (Mogán)", "1 Schlafzimmer · 80 m²", P, "top", "gcsur",
    L("fc:190441366"), 2200, True, 0, "Für genau 1 Monat 2.200 € (1.500 € nur bei langer Miete).")
out("ma-616656905", 46, "TF", "Fañabe (Costa Adeje)", "1 Schlafzimmer + Schlafsofa", P, "top", "adeje",
    L("ma:616656905"), 1950, True, 0, "Nur im Dezember 2026 frei.")
out("fc-190746734", 47, "GC", "San Agustín", "2 Zimmer · 40 m²", P, "top", "gcsur",
    L("fc:190746734", "ma:614388556"), 1300, False, 0, "Nur als Paket 01.10.–01.03. (5 Monate).")
out("fc-189065546", 48, "GC", "Bahía Feliz · Club Montemar", "2 Schlafzimmer · 110 m²", P, "top", "gcsur",
    L("fc:189065546"), 1980, False, 0, "Nur 2–5 Monate.")
out("fc-190928452", 49, "TF", "Cabo Blanco (Arona)", "2 Schlafzimmer · 79 m²", "Agentur Property Tenerife", "top", "arona",
    L("fc:190928452", "ma:616452880"), 880, True, None, "Nur als 6-Monats-Vertrag.")
out("fc-189890833", 50, "TF", "Adeje · Villa", "3 Schlafzimmer · 240 m²", P, "top", "adeje",
    L("fc:189890833"), 1800, False, 0, "Nur 6–8 Monate.")
out("ma-581485755", 51, "GC", "Telde · La Garita", "2 Schlafzimmer · 75 m²", "Agentur Surinka", "stadt", "lpgc",
    L("ma:581485755"), 900, False, None, "Nur für Lehrer und Gesundheitspersonal, max. 2 Personen.")
out("fc-184882441", 52, "TF", "Cabo Blanco (Inmogestión)", "2 Schlafzimmer · 73 m² · Pool", "Agentur", "top", "arona",
    L("fc:184882441"), 1050, True, None, "Nur bis 08.01.2027 frei.")
out("ma-616584519", 53, "GC", "Mogán", "1 Schlafzimmer · 45 m²", "Agentur", "top", "gcsur",
    L("ma:616584519"), 1600, False, None, "Erst ab 10.01.2027 frei, nur 1 Schlafzimmer.")
out("ma-617075724", 54, "TF", "San Miguel de Abona · Finca mit Privatpool", "3 Schlafzimmer · 182 m²", "Agentur", "top", "golfsur",
    L("ma:617075724"), 2000, False, None, "Erst ab 18.01.2027 frei.")
out("ma-615300358", 55, "GC", "Agaete", "2 Schlafzimmer · 105 m²", "Agentur", "gut", "galdar",
    L("ma:615300358"), 1200, True, None, "Erst ab 08.01.2027 und mindestens 3 Monate.")
out("fc-190641045", 56, "GC", "Melenara (Telde)", "2 Schlafzimmer · 65 m²", "Agentur", "stadt", "lpgc",
    L("fc:190641045"), 1300, False, None, "Nur Wintersaison, mindestens 5 Monate.")

for r in rows:
    r.update(firstSeen=D, lastSeen=D, online=True, priceHistory=[])
meta = {"lastUpdate": D, "firstRun": D, "screened": 3145, "sources": ["Milanuncios", "Fotocasa"], "nkEstimate": NK}
(ROOT / "data/dashboard.json").write_text(json.dumps({"meta": meta, "listings": rows}, ensure_ascii=False, indent=1))
from collections import Counter
print(len(rows), Counter(r["tier"] for r in rows), Counter((r["tier"], r["bike"]) for r in rows if r["tier"] != "out"))
for r in rows:
    if r["tier"] != "out" and (r["total"] > 2000):
        print("WARN over", r["key"], r["total"])
