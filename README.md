# Piso en Tenerife o Gran Canaria – Januar 2027

Tägliches Screening des lokalen Mietmarkts (nicht Airbnb/Booking) nach einer Wohnung für
**1 Monat im Januar 2027**, 2–4 Personen, mind. 2 getrennte Betten, max. 2.000 €.

- **Dashboard „Wohnungsradar Kanaren“:** https://claude.ai/artifact/KvWpcNWSn7zDUM1Rfm8TYi (privat, nur für den Besitzer sichtbar)
  – Quelle der Einträge ist `data/dashboard.json`; Seitenquelltext in `dashboard/wohnungsradar.html`
- **[wohnungen.md](wohnungen.md)** – Kurzfassung: Suchprofil, Kostenregel, Radlage, Stand
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
Harte Grenze: 2.000 € **Gesamtkosten** (Miete + Maklergebühr + NK + Reinigung). Radlage je Ort: `scraper/bikezone.py`.
Filter: nur Teneriffa/Gran Canaria, Preis 450–2.000 €, Hinweise auf Kurzzeit („mínimo 1 mes“,
„por meses“, „corta temporada“ …), ohne Ausschlussgründe („mínimo 3 meses“, „larga temporada“,
„estudiantes“ …). Klasse **A** = 1 Monat ausdrücklich möglich + ≥ 2 Zimmer, **B** = anfragen.
Die Rohliste wird danach manuell geprüft und in `data/dashboard.json` übernommen.
`python3 scraper/refresh_dashboard.py` hält bestehende Einträge aktuell (lastSeen, Preis im Inseratskopf `listPrice`,
online-Status; fehlende Treffer werden über die Detailseite geprüft).

Fotos: `python3 scraper/thumbs.py OUT_DIR [key ...]` lädt bis zu 3 Bilder je neuem Eintrag (480×320 JPEG,
braucht Pillow: `pip install pillow`) und bereitet sie für die Dashboard-Collection `thumbs` vor.
