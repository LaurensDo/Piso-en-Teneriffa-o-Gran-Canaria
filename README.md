# Piso en Tenerife o Gran Canaria – Januar 2027

Tägliches Screening des lokalen Mietmarkts (nicht Airbnb/Booking) nach einer Wohnung für
**1 Monat im Januar 2027**, 2–4 Personen, mind. 2 getrennte Betten, max. 2.000 €.

- **[wohnungen.md](wohnungen.md)** – aktuelle Shortlist, Anfrage-Kandidaten, Markteinschätzung
- `data/neu/JJJJ-MM-TT.md` – automatisch gefundene neue Inserate des jeweiligen Tages (Rohliste)
- `data/seen.json` – bereits bekannte Inserate (für den Neu-Abgleich und Preisänderungen)

## Quellen
| Portal | Status |
|--------|--------|
| Milanuncios (Suchbegriffe: enero, temporada, por meses, invierno, corta temporada, mensual, meses) | automatisch |
| Fotocasa (alle Mietinserate 450–2.000 €, beide Provinzen) | automatisch |
| Idealista | blockiert automatische Abrufe → eigenen Suchalarm anlegen |
| Facebook-Gruppen, Wallapop | nicht automatisierbar |

## Ablauf
```
python3 scraper/daily.py          # holt Daten (~7 Min.), filtert, schreibt data/neu/<datum>.md
python3 scraper/daily.py --no-fetch   # nur neu filtern
```
Filter: nur Teneriffa/Gran Canaria, Preis 450–2.000 €, Hinweise auf Kurzzeit („mínimo 1 mes“,
„por meses“, „corta temporada“ …), ohne Ausschlussgründe („mínimo 3 meses“, „larga temporada“,
„estudiantes“ …). Klasse **A** = 1 Monat ausdrücklich möglich + ≥ 2 Zimmer, **B** = anfragen.
Die Rohliste wird danach manuell geprüft und in `wohnungen.md` übernommen.
