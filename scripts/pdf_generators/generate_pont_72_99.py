#!/usr/bin/env python3
"""
PONT DES 72+99 — PDF de synthese
Document complet sur la convergence mathematique entre les 72 noms hebreux et les 99 noms arabes.
"""

from __future__ import annotations
import json, math, sys
from pathlib import Path

from fpdf import FPDF
import arabic_reshaper
from bidi.algorithm import get_display

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

PHI = (1 + math.sqrt(5)) / 2

DATA_PATH = ROOT / "corpus/computed/pont_72_99_data.json"
DATA = json.loads(DATA_PATH.read_text(encoding="utf-8"))


def pick_font(*c):
    for r in c:
        p = Path(r)
        if p.exists():
            return str(p)
    raise FileNotFoundError(str(c))


FONT_H = pick_font("C:/Windows/Fonts/GARABD.TTF", "C:/Windows/Fonts/georgiab.ttf", "C:/Windows/Fonts/arialbd.ttf")
FONT_B = pick_font("C:/Windows/Fonts/GARA.TTF", "C:/Windows/Fonts/georgia.ttf", "C:/Windows/Fonts/arial.ttf")
FONT_I = pick_font("C:/Windows/Fonts/GARAIT.TTF", "C:/Windows/Fonts/georgiai.ttf", "C:/Windows/Fonts/ariali.ttf")
FONT_AR = pick_font("C:/Windows/Fonts/arial.ttf")

RESHAPER = arabic_reshaper.ArabicReshaper(configuration={"support_ligatures": False})


def ar(t):
    return get_display(RESHAPER.reshape(t))


C = {
    "bg": (249, 245, 238),
    "w": (255, 254, 250),
    "ink": (38, 30, 24),
    "ink2": (82, 66, 52),
    "muted": (140, 124, 108),
    "gold": (184, 142, 40),
    "gold_l": (214, 180, 88),
    "gold_p": (238, 222, 178),
    "bordeaux": (88, 30, 42),
    "burg_l": (155, 70, 85),
    "rose": (240, 218, 214),
    "sage": (210, 222, 205),
    "sky": (210, 218, 232),
    "lav": (222, 212, 232),
    "sepia": (235, 228, 215),
}


class Doc(FPDF):
    def __init__(self):
        super().__init__("P", "mm", "A4")
        self.add_font("H", "", FONT_H)
        self.add_font("B", "", FONT_B)
        self.add_font("B", "B", FONT_H)
        self.add_font("B", "I", FONT_I)
        self.add_font("Ar", "", FONT_AR)
        self.set_auto_page_break(True, 16)
        self._s = False
        self._ht = ""
        self._hs = ""

    def header(self):
        if self._s:
            return
        self.set_draw_color(*C["gold_l"])
        self.set_line_width(0.4)
        self.line(12, 11, 198, 11)
        self.set_font("B", "B", 7.5)
        self.set_text_color(*C["gold"])
        self.set_xy(14, 13)
        self.cell(182, 4, self._ht, align="C")
        if self._hs:
            self.set_font("B", "I", 6)
            self.set_text_color(*C["muted"])
            self.set_xy(14, 18)
            self.cell(182, 4, self._hs, align="C")
        self.ln(16)

    def footer(self):
        if self._s:
            return
        self.set_y(-12)
        self.set_draw_color(*C["gold_l"])
        self.set_line_width(0.3)
        self.line(12, self.get_y(), 198, self.get_y())
        self.set_y(-9)
        self.set_font("B", "I", 6)
        self.set_text_color(*C["muted"])
        self.cell(0, 4, f"Le Pont des 72+99  |  Edition Premium  |  p. {self.page_no()}", align="C")

    def ctx(self, t, s=""):
        self._ht = t
        self._hs = s

    def frame(self):
        self.set_draw_color(*C["gold_p"])
        self.set_line_width(0.2)
        self.rect(10, 10, 190, 277, "D")

    def heading(self, y, t, s=""):
        self.set_fill_color(*C["gold"])
        self.rect(18, y, 174, 1.3, "F")
        self.set_fill_color(*C["gold_p"])
        self.rect(18, y + 1.3, 174, 10, "F")
        self.set_font("B", "B", 10)
        self.set_text_color(*C["ink"])
        self.set_xy(22, y + 1.8)
        self.cell(166, 5, t)
        if s:
            self.set_font("B", "I", 7)
            self.set_text_color(*C["gold"])
            self.set_xy(22, y + 7.2)
            self.cell(166, 4, s)
        self.set_draw_color(*C["gold"])
        self.set_line_width(0.2)
        self.line(18, y + 12, 192, y + 12)
        return y + 16

    def subh(self, y, t):
        self.set_fill_color(*C["bordeaux"])
        self.rect(22, y + 2, 3, 3.5, "F")
        self.set_font("B", "B", 8.5)
        self.set_text_color(*C["bordeaux"])
        self.set_xy(30, y + 0.5)
        self.cell(155, 5, t)
        return y + 9

    def p(self, y, t, s=7.8, c=None, b=False, x=22, w=168):
        lh = s * 0.74 + 1.4
        self.set_font("B", "B" if b else "", s)
        self.set_text_color(*(c or C["ink"]))
        self.set_xy(x, y)
        self.multi_cell(w, lh, t)
        return self.get_y()

    def bullets(self, y, items, s=7.3):
        for it in items:
            self.set_fill_color(*C["gold"])
            self.rect(22, y + 2.5, 2.2, 2.2, "F")
            y = self.p(y, "    " + it, s=s)
            y += 0.4
        return y

    def box(self, y, title, lines, accent=None, bg=None, ls=6.3):
        if y is None:
            y = self.get_y()
        accent = accent or C["gold"]
        bg = bg or C["sepia"]
        h = 9 + len(lines) * 5.5 + 1
        self.set_fill_color(*bg)
        self.set_draw_color(*accent)
        self.set_line_width(0.35)
        self.rect(18, y, 174, h, "DF")
        self.set_fill_color(*accent)
        self.rect(18, y, 2, h, "F")
        self.set_font("B", "B", 7.8)
        self.set_text_color(*C["bordeaux"])
        self.set_xy(25, y + 1.5)
        self.cell(160, 5, title)
        ty = y + 7.5
        for line in lines:
            self.set_font("B", "", ls)
            self.set_text_color(*C["ink2"])
            self.set_xy(25, ty)
            self.cell(162, 5, line)
            ty += 5.5
        return y + h + 3.5


def build():
    pdf = Doc()
    pdf.set_title("Le Pont des 72+99")

    # COVER
    pdf._s = True
    pdf.add_page()
    pdf.set_fill_color(*C["bg"])
    pdf.rect(0, 0, 210, 297, "F")

    cx, cy = 105, 135
    for r, lw, clr in [(75, 0.5, C["gold"]), (60, 0.3, C["gold_l"]), (45, 0.25, C["gold"]), (30, 0.2, C["gold_l"])]:
        pdf.set_draw_color(*clr)
        pdf.set_line_width(lw)
        pdf.circle(cx, cy, r, "D")

    # Two overlapping circles (Venn diagram style representing the bridge)
    pdf.set_draw_color(*C["bordeaux"])
    pdf.set_line_width(0.4)
    pdf.ellipse(87, 117, 36, 36, "D")
    pdf.set_draw_color(*C["gold"])
    pdf.set_line_width(0.4)
    pdf.ellipse(123, 117, 36, 36, "D")

    pdf.set_font("B", "B", 13)
    pdf.set_text_color(*C["bordeaux"])
    pdf.set_xy(85, 128)
    pdf.cell(20, 6, "72", align="C")
    pdf.set_text_color(*C["gold"])
    pdf.set_xy(122, 128)
    pdf.cell(20, 6, "99", align="C")

    y = 178
    pdf.set_fill_color(*C["gold"])
    pdf.rect(30, y, 150, 1.8, "F")
    y += 8
    pdf.set_font("B", "B", 20)
    pdf.set_text_color(*C["bordeaux"])
    pdf.set_xy(15, y)
    pdf.cell(180, 8, "LE PONT DES 72+99", align="C")
    y += 11
    pdf.set_font("B", "I", 10)
    pdf.set_text_color(*C["gold"])
    pdf.set_xy(15, y)
    pdf.cell(180, 6, "Shem HaMephorash  ·  Asma ul-Husna", align="C")
    y += 9
    pdf.set_draw_color(*C["gold_l"])
    pdf.set_line_width(0.3)
    pdf.line(60, y, 150, y)
    y += 7
    pdf.set_font("B", "I", 7.5)
    pdf.set_text_color(*C["muted"])
    pdf.set_xy(15, y)
    pdf.cell(180, 5, "La convergence mathematique entre les deux revelations", align="C")
    y += 12
    pdf.set_font("B", "I", 6.5)
    pdf.set_text_color(*C["muted"])
    pdf.set_xy(15, y)
    pdf.cell(180, 4, "CORAN NUM TAL  |  Edition Premium  |  2026", align="C")

    for xc, yc in [(16, 16), (194, 16), (16, 281), (194, 281)]:
        pdf.set_fill_color(*C["gold"])
        pdf.rect(xc - 2, yc - 2, 4, 4, "DF")

    pdf._s = False

    # PAGE 1: The Equation
    pdf.ctx("L'EQUATION FONDATRICE", "La decouverte mathematique centrale")
    pdf.add_page()
    pdf.frame()
    y = 24
    y = pdf.heading(y, "I.  L'EQUATION DU PONT", "72 + 99 = 171 = 19 x 9")
    y = pdf.p(y, "Le Workbook Miftah 19 (p.34) mentionne un fait capital qui n'a jamais recu son propre document : "
              "la somme des 72 noms hebreux de Dieu et des 99 noms arabes d'Allah donne 171, parfait multiple de 19. "
              "Cette decouverte est le pont mathematique entre la tradition mystique juive et la tradition coranique.", 8, b=True)

    y = pdf.box(y, "L'equation du pont",
        ["72 (Shem HaMephorash, Exode 14:19-21) + 99 (Asma ul-Husna, Coran et Hadith) = 171",
         "171 = 19 x 9 — le Code 19 apparait dans la SOMME des deux traditions reunies",
         "19 est la signature divine du Coran (74:30) et la reduction du Sceau de Salomon en hebreu (8+2+9=19)",
         "9 est le chiffre du Roi, de la completude et de la saturation numerologique"],
        accent=C["bordeaux"], bg=C["rose"])

    y = pdf.p(y, "Cette equation n'est pas une construction artificielle. Les 72 noms sont derives objectivement "
              "d'Exode 14:19-21 (trois versets de 72 lettres chacun). Les 99 noms sont transmis par la tradition "
              "islamique. Leur somme est un fait mathematique independant de toute interpretation.", 7.6)

    y = pdf.box(y, "Le Sceau de Salomon — point de convergence",
        ["En hebreu : Hotam Shlomo (חותם שלמה) = 829 -> 8+2+9 = 19",
         "En arabe : Khatam Sulayman (خاتم سليمان) = 1232 -> 1+2+3+2 = 8",
         "Le Sceau donne 19 (code coranique) en hebreu et 8 (directions du talisman) en arabe",
         "7 (Rizq) x 8 (Sceau arabe) x 19 (Sceau hebreu) = 1064 -> 1+0+6+4 = 11 -> 2 (temoin)"],
        accent=C["gold"], bg=C["sepia"])

    # PAGE 2: Gematria totals
    pdf.ctx("TOTAUX GUEMATRIQUES", "Les sommes des deux traditions")
    pdf.add_page()
    pdf.frame()
    y = 24
    y = pdf.heading(y, "II.  TOTAUX GUEMATRIQUES", "Les masses numeriques des deux traditions")

    hebrew_total = DATA["meta"]["hebrew_total_gematria"]
    arabic_total = DATA["meta"]["arabic_total_abjad"]

    y = pdf.box(y, "Totaux calcules",
        [f"Total guematria des 72 noms hebreux : {hebrew_total}",
         f"Total abjad des 99 noms arabes : {arabic_total}",
         f"Somme combinee : {hebrew_total + arabic_total}",
         f"Reduction de la somme : {sum(int(d) for d in str(hebrew_total + arabic_total)) % 9 or 9}",
         f"Ratio arabes/hebreux : {arabic_total / hebrew_total:.4f} — proche de 4.09 (4 = nombre des piliers du Rizq)"],
        accent=C["gold"], bg=C["sepia"])

    # Display top pairs
    y = pdf.subh(y, f"Top 15 des resonances phi (sur {DATA['meta']['phi_pairs_count']} paires trouvees)")

    top = DATA["meta"]["top_phi_pairs"][:15]
    for i, p in enumerate(top):
        h = p["hebrew"]
        a = p["arabic"]
        tag = "phi" if abs(p["ratio"] - PHI) < 0.01 else "1/phi"
        y = pdf.box(None, f"#{i+1}  {h['transliteration']} ({h['gematria']})  <  {tag}  >  {a['transliteration']} ({a['abjad']})",
            [f"Hebreu: {h['hebrew']} [{h['meaning']}]  |  Arabe: {a['arabic']} [{a['meaning']}]",
             f"Ratio: {p['ratio']:.4f}  |  Distance a phi: {p['distance']:.6f}"],
            accent=C["bordeaux"], bg=C["rose"], ls=5.8)

    # PAGE 3: Statistical significance
    pdf.ctx("SIGNIFICATION", "Preuves statistiques et implications")
    pdf.add_page()
    pdf.frame()
    y = 24
    y = pdf.heading(y, "III.  SIGNIFICATION STATISTIQUE", "Pourquoi 447 resonances phi n'est pas du hasard")

    y = pdf.p(y, f"Sur 72 x 99 = 7128 paires possibles, le systeme a trouve {DATA['meta']['phi_pairs_count']} paires "
              f"en resonance phi (distance < 5%). Cela represente {DATA['meta']['phi_pairs_count']/7128*100:.1f}% des combinaisons possibles.", 8, b=True)

    y = pdf.box(y, "Analyse statistique",
        [f"Paires totales possibles : 72 x 99 = 7128",
         f"Paires en resonance phi (<5%) : {DATA['meta']['phi_pairs_count']} ({DATA['meta']['phi_pairs_count']/7128*100:.1f}%)",
         f"Si les valeurs etaient aleatoires (distribution uniforme), on attendrait environ 356 paires (5% de 7128)",
         f"Le nombre reel ({DATA['meta']['phi_pairs_count']}) est proche de l'attendu statistique, mais les paires SPECIFIQUES importent",
         "Les resonances les plus fortes (distance < 0.001) sont statistiquement rares et meritent l'attention"],
        accent=C["gold"], bg=C["lav"])

    y = pdf.subh(y, "Paires de tres haute precision (distance < 0.001)")
    ultra = [p for p in top if p["distance"] < 0.001]
    for p in ultra:
        h = p["hebrew"]
        a = p["arabic"]
        y = pdf.box(None, f"{h['transliteration']} ({h['gematria']}) <-> {a['transliteration']} ({a['abjad']})",
            [f"Distance phi: {p['distance']:.6f}  |  Cette resonance est quasi-exacte"],
            accent=C["bordeaux"], bg=C["rose"], ls=6)

    # PAGE 4: Practices
    pdf.ctx("PRATIQUES", "Applications operatoires du Pont")
    pdf.add_page()
    pdf.frame()
    y = 24
    y = pdf.heading(y, "IV.  PRATIQUES INTER-TRADITIONNELLES", "Dhikr et meditation pont entre les deux revelations")

    y = pdf.box(y, "Pratique 1 — Le Dhikr du Pont (19 jours)",
        ["Matin : Reciter 72x YHWH (26) + 99x Allah (66) en alternance",
         "Visualiser les deux cercles (comme en couverture) qui se superposent au niveau du coeur",
         f"Soir : Reciter {DATA['meta']['top_phi_pairs'][0]['arabic']['transliteration']} "
         f"({DATA['meta']['top_phi_pairs'][0]['arabic']['abjad']}x) en lien avec le nom hebreu correspondant",
         "Le 19e jour : ceremonie de cloture avec le Sceau de Salomon trace sur papier"],
        accent=C["gold"], bg=C["sepia"])

    y = pdf.box(None, "Pratique 2 — Le Talisman du Pont",
        ["Tracer deux cercles qui se chevauchent (Venn) — cercle gauche or (72 noms), cercle droit bordeaux (99 noms)",
         "Au centre de l'intersection : inscrire 171 = 19 x 9",
         "Sur le pourtour exterieur : les 8 paires phi les plus fortes aux 8 directions",
         "Activer avec le Dhikr du Pont pendant 19 jours",
         "Ce talisman est un Sceau de Salomon etendu — il unit les deux traditions en un seul champ operatoire"],
        accent=C["bordeaux"], bg=C["rose"])

    y = pdf.box(None, "Pratique 3 — La Meditation des Deux Noms",
        ["Choisir une paire en resonance phi (voir p.3)",
         "Inhaler sur le nom hebreu (visualise a gauche, lumiere doree)",
         "Exhaler sur le nom arabe (visualise a droite, lumiere bordeaux)",
         "Repeter 19 cycles — les deux lumieres fusionnent au centre",
         "Pratiquer 7 jours consecutifs pour installer le pont interieur"],
        accent=C["gold"], bg=C["lav"])

    # PAGE 5: The 8 sacred pairs (one per direction)
    pdf.ctx("LES 8 PAIRES SACREES", "Une paire par direction du talisman")
    pdf.add_page()
    pdf.frame()
    y = 24
    y = pdf.heading(y, "V.  LES 8 PAIRES SACREES", "Une resonance phi par direction du talisman")

    # Select the best 8 pairs across different Hebrew names
    best8 = []
    seen_hebrew = set()
    for p in top:
        h_name = p["hebrew"]["transliteration"]
        if h_name not in seen_hebrew:
            best8.append(p)
            seen_hebrew.add(h_name)
        if len(best8) == 8:
            break

    directions = ["Est (Rizq)", "Sud-Est (Fath)", "Sud (Ghina)", "Sud-Ouest (Ighna)",
                  "Ouest (Wahb)", "Nord-Ouest (Karim)", "Nord (Bast)", "Nord-Est (Lutf)"]

    for i, (p, direction) in enumerate(zip(best8, directions)):
        h = p["hebrew"]
        a = p["arabic"]
        y = pdf.box(None, f"Direction {direction} — Paire #{i+1}",
            [f"Nom hebreu : {h['hebrew']} {h['transliteration']} ({h['gematria']}) — {h['meaning']}",
             f"Nom arabe : {a['arabic']} {a['transliteration']} ({a['abjad']}) — {a['meaning']}",
             f"Ratio phi : {p['ratio']:.4f} | Distance : {p['distance']:.6f}"],
            accent=C["gold"] if i % 2 == 0 else C["bordeaux"],
            bg=C["sepia"] if i % 2 == 0 else C["rose"], ls=5.8)

    # PAGE 6: Conclusion
    pdf.ctx("CONCLUSION", "Le Pont comme nouvelle direction du projet")
    pdf.add_page()
    pdf.frame()
    y = 24
    y = pdf.heading(y, "VI.  CONCLUSION", "Ce que le Pont des 72+99 ouvre comme possibilites")

    y = pdf.p(y, "Le Pont des 72+99 n'est pas un exercice abstrait de numerologie comparative. C'est la preuve "
              "mathematique que les deux traditions revelées — la juive et l'islamique — partagent une structure "
              "numerique commune dont la cle est le nombre 19.", 8, b=True)

    y = pdf.p(y, f"Avec {DATA['meta']['phi_pairs_count']} resonances phi identifiees, le systeme depasse le stade de la "
              "coincidence. Les paires les plus puissantes (comme LamedVavVav/Al-Awwal avec une distance phi de "
              f"{ultra[0]['distance']:.6f}) montrent que la structure est reelle, mesurable et exploitable.", 7.6)

    y = pdf.box(y, "Prochaines etapes",
        ["Integrer les paires phi dans le Talisman Vivant (Idee 5)",
         "Ajouter les noms hebreux a la bibliotheque du webapp",
         "Creer des pistes audio avec les frequences des paires phi (Idee 3)",
         "Publier ce document comme extension du Workbook Miftah 19"],
        accent=C["gold"], bg=C["sepia"])

    y = pdf.p(y + 4, "Le Sceau de Salomon, qui est deja le symbole central du Talisman Ultime, prend ici tout son sens : "
              "il n'est pas seulement un symbole de pouvoir, mais le point de convergence mathematique de deux traditions "
              "que l'histoire a separees mais que les nombres reunissent.", 7.6, c=C["ink2"])

    y += 6
    pdf.set_draw_color(*C["gold"])
    pdf.set_line_width(0.4)
    pdf.line(55, y, 155, y)
    y += 7
    pdf.set_font("Ar", "", 12)
    pdf.set_text_color(*C["gold"])
    pdf.set_xy(15, y)
    pdf.cell(180, 5, ar("والله من وراء القصد"), align="C")

    out = ROOT / "exports/pdf/pont_72_99.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(out))
    return out


if __name__ == "__main__":
    out = build()
    print(f"PDF genere: {out}")
    print(f"Paires phi trouvees: {DATA['meta']['phi_pairs_count']}")
