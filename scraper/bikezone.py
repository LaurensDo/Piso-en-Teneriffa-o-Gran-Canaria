"""Radlage je Ort (Rennrad-Winterquartier): 'top', 'gut' oder 'stadt'. Nur die Lage zählt."""
import re

ZONES = [
    # Gran Canaria – sonniger Süden: klassisches Winterrevier, Anstiege (Fataga, Soria, Cerana) ab Haustür
    ("top", "GC", r"maspalomas|playa del ingl|san agust|bah[ií]a feliz|meloneras|san fernando|sonnenland|campo internacional|"
                  r"el tablero|san bartolom[eé] de tirajana|arguineg|puerto rico|mog[aá]n|playa del cura|taurito|playa del [aá]guila|las burras|el veril|patalavaca|amadores"),
    # Teneriffa – Süden/Westen: sonnig, direkte Teide-Anstiege über Vilaflor oder Chío
    ("top", "TF", r"adeje|arona|los cristianos|am[eé]ricas|palm.?mar|fa[nñ]abe|torviscas|san eugenio|callao salvaje|playa para[ií]so|"
                  r"gu[ií]a de isora|playa (de )?san juan|alcal[aá]|santiago del teide|los gigantes|puerto de santiago|la arena|vilaflor|"
                  r"san miguel|golf del sur|amarilla|las galletas|costa del silencio|guargacho|chayofa|cabo blanco|las chafiras|los abrigos"),
    # Gut: starke Anstiege, aber windiger/wolkiger oder etwas Anfahrt
    ("gut", "GC", r"ag[uü]imes|arinaga|vargas|ingenio|santa luc[ií]a|vecindario|g[aá]ldar|agaete|gu[ií]a|aldea de san nicol|"
                  r"santa br[ií]gida|san mateo|teror|valsequillo|tejeda|firgas|moya|sobradillo"),
    ("gut", "TF", r"granadilla|m[eé]dano|tejita|arico|por[ií]s|abona|puerto de la cruz|orotava|realejos|icod|garachico|buenavista|"
                  r"los silos|san juan de la rambla|la guancha|g[uü][ií]mar|arafo|fasnia"),
    # Stadt/Anfahrt: erst aus der Stadt heraus, mehr Verkehr
    ("stadt", "GC", r"las palmas|telde|arucas|la garita|melenara|taliarte|marzag"),
    ("stadt", "TF", r"santa cruz|la laguna|candelaria|tacoronte|sauzal|santa [uú]rsula|victoria|matanza|bajamar|punta del hidalgo|valle de guerra|tegueste"),
]


def bike_zone(text):
    t = (text or "").lower()
    for level, _, pat in ZONES:
        if re.search(pat, t):
            return level
    return None
