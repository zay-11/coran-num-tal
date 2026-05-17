#!/usr/bin/env python3
"""
SYNTHESE DE RECHERCHE — CORAN NUM TAL
Analyse transversale des 10 PDFs du projet.
Fil conducteur, architecture unifiee, ponts caches, schismes, idees nouvelles.
"""

from __future__ import annotations

import math
from pathlib import Path
import sys

from fpdf import FPDF
import arabic_reshaper
from bidi.algorithm import get_display

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

PHI = (1 + math.sqrt(5)) / 2

from core.project_paths import ensure_layout

ensure_layout()


def pick_font(*candidates: str) -> str:
    for raw in candidates:
        path = Path(raw)
        if path.exists():
            return str(path)
    raise FileNotFoundError(f"Font not found: {candidates}")


FONT_H = pick_font("C:/Windows/Fonts/GARABD.TTF", "C:/Windows/Fonts/georgiab.ttf", "C:/Windows/Fonts/arialbd.ttf")
FONT_B = pick_font("C:/Windows/Fonts/GARA.TTF", "C:/Windows/Fonts/georgia.ttf", "C:/Windows/Fonts/arial.ttf")
FONT_I = pick_font("C:/Windows/Fonts/GARAIT.TTF", "C:/Windows/Fonts/georgiai.ttf", "C:/Windows/Fonts/ariali.ttf")
FONT_AR = pick_font("C:/Windows/Fonts/arial.ttf")

RESHAPER = arabic_reshaper.ArabicReshaper(configuration={"support_ligatures": False})

C = {
    "bg": (249, 245, 238),
    "white": (255, 254, 250),
    "ink": (42, 34, 28),
    "ink2": (88, 72, 58),
    "muted": (145, 130, 115),
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


def ar(text: str) -> str:
    return get_display(RESHAPER.reshape(text))


class Doc(FPDF):
    def __init__(self):
        super().__init__("P", "mm", "A4")
        self.add_font("H", "", FONT_H)
        self.add_font("B", "", FONT_B)
        self.add_font("B", "B", FONT_H)
        self.add_font("B", "I", FONT_I)
        self.add_font("Ar", "", FONT_AR)
        self.set_auto_page_break(True, 16)
        self._skip = False
        self._htitle = ""
        self._hsub = ""

    def header(self):
        if self._skip:
            return
        self.set_draw_color(*C["gold_l"])
        self.set_line_width(0.4)
        self.line(12, 11, 198, 11)
        self.set_font("B", "B", 7.5)
        self.set_text_color(*C["gold"])
        self.set_xy(14, 13)
        self.cell(182, 4, self._htitle, align="C")
        if self._hsub:
            self.set_font("B", "I", 6)
            self.set_text_color(*C["muted"])
            self.set_xy(14, 18)
            self.cell(182, 4, self._hsub, align="C")
        self.ln(16)

    def footer(self):
        if self._skip:
            return
        self.set_y(-12)
        self.set_draw_color(*C["gold_l"])
        self.set_line_width(0.3)
        self.line(12, self.get_y(), 198, self.get_y())
        self.set_y(-9)
        self.set_font("B", "I", 6)
        self.set_text_color(*C["muted"])
        self.cell(0, 4, f"Synthese de Recherche CORAN NUM TAL  |  p. {self.page_no()}", align="C")

    def ctx(self, title, sub=""):
        self._htitle = title
        self._hsub = sub

    # --- drawing helpers ---

    def frame(self):
        self.set_draw_color(*C["gold_p"])
        self.set_line_width(0.2)
        self.rect(10, 10, 190, 277, "D")

    def heading(self, y, title, sub=""):
        self.set_fill_color(*C["gold"])
        self.rect(18, y, 174, 1.3, "F")
        self.set_fill_color(*C["gold_p"])
        self.rect(18, y + 1.3, 174, 10, "F")
        self.set_font("B", "B", 10)
        self.set_text_color(*C["ink"])
        self.set_xy(22, y + 1.8)
        self.cell(166, 5, title)
        if sub:
            self.set_font("B", "I", 7)
            self.set_text_color(*C["gold"])
            self.set_xy(22, y + 7.2)
            self.cell(166, 4, sub)
        self.set_draw_color(*C["gold"])
        self.set_line_width(0.2)
        self.line(18, y + 12, 192, y + 12)
        return y + 16

    def subh(self, y, title):
        self.set_fill_color(*C["bordeaux"])
        self.rect(22, y + 2, 3, 3.5, "F")
        self.set_font("B", "B", 8.5)
        self.set_text_color(*C["bordeaux"])
        self.set_xy(30, y + 0.5)
        self.cell(155, 5, title)
        return y + 9

    def p(self, y, txt, s=7.8, c=None, b=False, x=22, w=168, lh=None):
        if lh is None:
            lh = s * 0.74 + 1.4
        self.set_font("B", "B" if b else "", s)
        self.set_text_color(*(c or C["ink"]))
        self.set_xy(x, y)
        self.multi_cell(w, lh, txt)
        return self.get_y()

    def bullets(self, y, items, s=7.4):
        for it in items:
            self.set_fill_color(*C["gold"])
            self.rect(22, y + 2.5, 2.2, 2.2, "F")
            y = self.p(y, "    " + it, s=s)
            y += 0.4
        return y

    def box(self, y, title, lines, accent=None, bg=None, ls=6.3):
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

    def table_3col(self, y, headers, rows, col_w=None):
        col_w = col_w or [60, 55, 55]
        self.set_fill_color(*C["bordeaux"])
        self.set_draw_color(*C["bordeaux"])
        self.set_line_width(0.3)
        x0 = 18
        self.set_font("B", "B", 6.5)
        self.set_text_color(*C["white"])
        cx = x0
        for i, hdr in enumerate(headers):
            self.set_xy(cx, y)
            self.cell(col_w[i], 5.5, hdr, fill=True, align="C")
            cx += col_w[i]
        y += 6
        for row in rows:
            self.set_font("B", "", 6.2)
            self.set_text_color(*C["ink2"])
            cx = x0
            bg = C["sepia"] if rows.index(row) % 2 == 0 else C["white"]
            self.set_fill_color(*bg)
            for i, cell in enumerate(row):
                self.set_xy(cx, y)
                self.cell(col_w[i], 5, str(cell), fill=True, align="C")
                cx += col_w[i]
            y += 5
        return y + 3

    def number_callout(self, y, num, meaning, source=""):
        self.set_font("B", "B", 20)
        self.set_text_color(*C["bordeaux"])
        self.set_xy(22, y - 2)
        self.cell(20, 8, str(num))
        self.set_font("B", "", 7.5)
        self.set_text_color(*C["ink2"])
        self.set_xy(45, y)
        self.cell(145, 5, meaning)
        if source:
            self.set_font("B", "I", 6.2)
            self.set_text_color(*C["muted"])
            self.set_xy(45, y + 5)
            self.cell(145, 4, source)
        return y + 11


def build():
    pdf = Doc()
    pdf.set_title("CORAN NUM TAL — Synthese de Recherche")

    # ====== COVER ======
    pdf._skip = True
    pdf.add_page()
    pdf.set_fill_color(*C["bg"])
    pdf.rect(0, 0, 210, 297, "F")

    # Mandala minimal
    cx, cy = 105, 140
    for r, lw, clr in [(72, 0.5, C["gold"]), (58, 0.3, C["gold_l"]), (44, 0.25, C["gold"]), (30, 0.2, C["gold_l"])]:
        pdf.set_draw_color(*clr)
        pdf.set_line_width(lw)
        pdf.circle(cx, cy, r, "D")
    for i in range(8):
        ang = 3.14159 * 2 / 8 * i - 3.14159 / 2
        x = cx + 36 * math.cos(ang)
        y = cy - 36 * math.sin(ang)
        pdf.set_fill_color(*C["gold"])
        pdf.circle(x, y, 1.8, "F")

    # Title
    y = 205
    pdf.set_fill_color(*C["gold"])
    pdf.rect(28, y, 154, 1.8, "F")
    y += 8
    pdf.set_font("B", "B", 22)
    pdf.set_text_color(*C["bordeaux"])
    pdf.set_xy(15, y)
    pdf.cell(180, 8, "CORAN NUM TAL", align="C")
    y += 11
    pdf.set_font("B", "I", 11)
    pdf.set_text_color(*C["gold"])
    pdf.set_xy(15, y)
    pdf.cell(180, 6, "Synthese de Recherche  —  Meta-Analyse", align="C")
    y += 10
    pdf.set_draw_color(*C["gold_l"])
    pdf.set_line_width(0.3)
    pdf.line(60, y, 150, y)
    y += 8
    pdf.set_font("B", "I", 7.5)
    pdf.set_text_color(*C["muted"])
    pdf.set_xy(15, y)
    pdf.cell(180, 5, "Analyse transversale des 10 PDFs du projet  |  Fil conducteur unifie", align="C")
    y += 6
    pdf.set_xy(15, y)
    pdf.cell(180, 5, "Architecture commune  |  Ponts caches entre traditions  |  6 idees nouvelles", align="C")
    y += 12
    pdf.set_font("B", "I", 7)
    pdf.set_text_color(*C["muted"])
    pdf.set_xy(15, y)
    pdf.cell(180, 4, "Mai 2026  |  Document interne de recherche", align="C")

    # Corner ornaments
    for x, yc in [(16, 16), (194, 16), (16, 281), (194, 281)]:
        pdf.set_fill_color(*C["gold"])
        pdf.set_draw_color(*C["gold"])
        pdf.rect(x - 2, yc - 2, 4, 4, "DF")

    pdf._skip = False

    # ====== PAGE 1: INVENTORY ======
    pdf.ctx("INVENTAIRE", "Les 10 PDFs analyses et leurs themes")
    pdf.add_page()
    pdf.frame()
    y = 24
    y = pdf.heading(y, "I.  INVENTAIRE DES DOCUMENTS", "Les 10 PDFs du projet, classes par famille thematique")

    y = pdf.subh(y, "Famille 1 — Miftah 19 (Systeme central)")
    y = pdf.bullets(y, [
        "Cadran Lunaire Miftah 19 (2p) — Roue divinatoire lunaire, 28 mansions arabes, codes Grabovoi, nombres porte-bonheur",
        "Rituel Miftah 19 (7p) — Rituel 1-7-19-33-1=61, version express 60s, carre magique Buduh",
        "Talisman Ultime Miftah 19 (1p) — Synthese Sceau de Salomon + Abjad arabe + Guematria hebraique + Grabovoi",
        "Workbook Miftah 19 Premium (36p) — Cours complet : Code 19, Basmala, Ya-Sin, Waqiah, Rizq, rituel, talisman, techniques avancees",
    ], 7.3)

    y = pdf.subh(y, "Famille 2 — Radionique (Dispositifs physiques)")
    y = pdf.bullets(y, [
        "Module Radionique Rizq Phi (8p) — Bobine cuivre + quartz, specifications basees sur phi",
        "Radionique Amplifiee Miftah 19 (7p) — Systeme 7 couches : aimants neodyme + spirales cuivre + quartz + photo + geometrie sacree",
        "Radionique Sacree Miftah 19 (2p) — Version simplifiee : spirale cuivre 7 tours + quartz + codes",
    ], 7.3)

    y = pdf.subh(y, "Famille 3 — Richesse & Abondance (Decouvertes Phi)")
    y = pdf.bullets(y, [
        "Decouverte Phi Coran Rizq (11p) — Les 5 decouvertes phi, dhikrs, talisman, calendrier operatif",
        "Secret Rizq Phi Deluxe (8p) — Architecture Source-Issue-Pluie-Couloir, protocole 21 jours",
        "Secret Rizq Phi Grabovoi Esoterique (12p) — Synthese esoterique complete : racines, portes phi, corridor Fibonacci, dhikr, talisman, radionique",
    ], 7.3)

    y = pdf.heading(y + 3, "II.  STATISTIQUES DU CORPUS")
    rows = [
        ["Miftah 19 (systeme central)", "4 PDFs", "46 pages"],
        ["Radionique (dispositifs)", "3 PDFs", "17 pages"],
        ["Richesse & Abondance (phi)", "3 PDFs", "31 pages"],
        ["TOTAL", "10 PDFs", "94 pages"],
    ]
    y = pdf.table_3col(y, ["Famille", "Documents", "Pages totales"], rows, [85, 44, 44])

    # ====== PAGE 2: THE TRIPLE SIGNATURE ======
    pdf.ctx("LA TRIPLE SIGNATURE", "7 · 8 · 19 — le coeur mathematique du projet")
    pdf.add_page()
    pdf.frame()
    y = 24
    y = pdf.heading(y, "III.  LA TRIPLE SIGNATURE : 7 · 8 · 19", "Ces trois nombres apparaissent dans chaque document sans exception")

    y = pdf.number_callout(y, "7", "Multiplicateur divin du Rizq (2:261), 7 cieux, 7 terres, Fatiha en 7 versets, 7 niveaux de purification de l'istighfar")
    y = pdf.number_callout(y, "8", "Directions du talisman, etoile a 8 branches, 8 phases lunaires du Cadran, Sceau de Salomon en arabe = 1232 -> 1+2+3+2 = 8")
    y = pdf.number_callout(y, "19", "Signature divine du Coran (74:30), 19 lettres de la Basmala, 114 sourates = 19x6, Sceau de Salomon en hebreu = 829 -> 8+2+9 = 19")

    y = pdf.subh(y, "Tableau de presence du triplet dans chaque document")
    headers = ["Document", "7", "8", "19"]
    rows = [
        ["Cadran Lunaire", "7 phases", "8 phases lunaires", "19 mansions richesse"],
        ["Rituel Miftah 19", "7 istighfar", "8 directions talisman", "19 noms divins"],
        ["Talisman Ultime", "7x8=56 (Waqi'a)", "Sceau arabe->8", "Sceau hebreu->19"],
        ["Workbook", "7 cieux du rizq", "Etoile 8 branches", "Code 19 (74:30)"],
        ["Module Radionique", "Spirale secondaire", "Octogone", "Sourate 56"],
        ["Radionique Amplifiee", "7 tours secondaire", "8 aimants neodyme", "19 tours primaire"],
        ["Radionique Sacree", "7 tours spirale", "8 directions cercle", "19 kHz resonance"],
        ["Decouverte Phi", "1+7+19+33+1=61", "8 branches talisman", "19x4xphi->123"],
        ["Secret Deluxe", "7 jours cycle", "34->55->56->89", "19x repetitions"],
        ["Secret Esoterique", "mod 7, dhikr 7/21", "8 directions anneau", "19x4xphi->123"],
    ]
    y = pdf.table_3col(y, headers, rows, [44, 42, 42, 42])

    y = pdf.box(y + 2, "Code Grabovoi 520 741 8 — la signature condensee",
        ["5+2+0 = 7  |  7+4+1 = 12 -> 3  |  +8", "Le code 520 741 8 encode le triplet 7, 19 et 8 dans sa structure meme."],
        accent=C["bordeaux"], bg=C["rose"])

    # ====== PAGE 3: THE UNIVERSAL ARCHITECTURE ======
    pdf.ctx("ARCHITECTURE UNIVERSELLE", "Source -> Corridor -> Portail -> Centre -> Cycle")
    pdf.add_page()
    pdf.frame()
    y = 24
    y = pdf.heading(y, "IV.  L'ARCHITECTURE UNIVERSELLE", "La chaine en 5 maillons qui structure tous les documents")

    y = pdf.p(y, "Tous les PDFs, malgre leurs differences de forme, reposent sur la meme chaine logique en 5 etapes. "
              "Cette architecture est le veritable fil conducteur du projet CORAN NUM TAL.", s=8, b=True)

    chain = [
        ("1. SOURCE", "51:58", "Ar-Razzaq comme source pure, anterieure au manque. La provision existe avant l'appel."),
        ("2. CORRIDOR", "34 -> 55 -> 56 -> 89", "Suite Fibonacci : Saba (prosperite) -> Rahman (faveurs) -> Waqi'a (manifestation) -> Fajr (lucidite)"),
        ("3. PORTAIL", "618", "Rahman (329) + Rahim (289) = 618. Miroir de l'inverse de phi (0.618). Le coeur misericordieux du systeme."),
        ("4. CENTRE", "56", "Al-Waqi'a, sourate de la Richesse. 56 + 96 versets = 152 = 19 x 8. Pont entre phi et la pratique."),
        ("5. CYCLE", "61 -> 99", "1+7+19+33+1 = 61. Projection phi : 61 x 1.618 = 98.7 -> 99. L'horizon des Noms divins."),
    ]
    for title, code, meaning in chain:
        y = pdf.box(y, f"{title}  [{code}]", [meaning], accent=C["gold"], bg=C["sepia"], ls=6.5)

    y = pdf.subh(y + 2, "Preuve par les 5 decouvertes Phi")
    disc = [
        "Decouverte 1 : 19 x 4 x phi -> 123 (occurrences de rizq) — 99.98%",
        "Decouverte 2 : 55 x phi -> 89 (Rahman vers Fajr) — lecture Fibonacci",
        "Decouverte 3 : 489 x phi -> 786 (Fattah vers Basmala) — pont rituel",
        "Decouverte 4 : 618 x phi -> 1000+ (mercy-code vers plenitude) — coeur rectifie",
        "Decouverte 5 : 61 x phi -> 99 (cycle vers horizon des Noms) — 99.7%",
    ]
    y = pdf.bullets(y, disc, 7.2)

    y = pdf.p(y, "Ces 5 formules forment l'ossature mathematique du projet. Chaque PDF les utilise, les commente ou les applique. "
              "Aucune n'est independante : 123 (dec 1) appelle 89 (dec 2), qui appelle 786 (dec 3), lui-meme eclaire par 618 (dec 4), "
              "le tout stabilise par 99 (dec 5).", s=7.6, c=C["ink2"])

    # ====== PAGE 4: HIDDEN BRIDGES ======
    pdf.ctx("PONTS CACHES", "Les connexions inter-traditionnelles inexploitees")
    pdf.add_page()
    pdf.frame()
    y = 24
    y = pdf.heading(y, "V.  LE PONT DES 72 + 99", "La convergence mathematique entre les deux revelations")

    y = pdf.p(y, "Le Workbook (p.34) mentionne un fait capital qui n'a jamais recu son propre document : "
              "la somme des 72 noms hebreux de Dieu (Shem HaMephorash, derives d'Exode 14:19-21) et des 99 noms arabes "
              "(Asma ul-Husna) donne 171, soit 19 x 9.", s=8, b=True)

    y = pdf.box(y, "Equation du pont inter-traditionnel",
        ["72 (Shem HaMephorash) + 99 (Asma ul-Husna) = 171 = 19 x 9",
         "Sceau de Salomon en hebreu (Hotam Shlomo) = 829 -> 8+2+9 = 19",
         "Sceau de Salomon en arabe (Khatam Sulayman) = 1232 -> 1+2+3+2 = 8",
         "YHWH = 26  |  Allah = 66  |  66/26 = 2.538 -> proche de phi² (2.618)"],
        accent=C["bordeaux"], bg=C["lav"])

    y = pdf.subh(y, "Guematria hebraique du Rizq (deja dans le Talisman Ultime)")
    y = pdf.bullets(y, [
        "Mamon (Fortune) = 136 = 4 x 34 — constante du carre magique de Jupiter (planete de la richesse en alchimie)",
        "Shefa (Abondance) = 450 — reduction 4+5+0 = 9 (plenitude)",
        "Berakhah (Benediction) = 227 — reduction 2+2+7 = 11 -> 2 (dualite)",
        "Osher (Richesse) = 570 — reduction 5+7+0 = 12 -> 3 (harmonie)",
        "Parnassah (Subsistance) = 395 — reduction 3+9+5 = 17 -> 8 (directions)",
    ], 7.2)

    y = pdf.subh(y + 3, "Les correspondances planetaires (Kabbale / Alchimie)")
    rows = [
        ["Saturne", "3x3", "15 -> 6", "Binah", "Structure, discipline"],
        ["Jupiter", "4x4", "34 -> 7", "Chesed", "Richesse, expansion  —  RIZQ"],
        ["Soleil", "6x6", "111 -> 3", "Tiphareth", "Succes, reconnaissance"],
        ["Venus", "7x7", "175 -> 4", "Netzach", "Harmonie, beaute"],
    ]
    y = pdf.table_3col(y, ["Planete", "Carre", "Constante", "Sephirah", "Fonction"], rows, [26, 20, 30, 40, 55])

    y = pdf.p(y, "Jupiter/Chesed est la seule planete explicitement liee au Rizq dans le systeme. Son carre magique 4x4 "
              "a une constante de 34 — le meme 34 qui ouvre le corridor 34->55->89. La constante 34 se reduit a 7, "
              "le multiplicateur divin. Ce n'est pas un hasard : c'est une piste inexploree.", s=7.5, c=C["ink2"])

    # ====== PAGE 5: SCHISMS ======
    pdf.ctx("SCHISMES NUMERIQUES", "Les tensions non resolues du systeme")
    pdf.add_page()
    pdf.frame()
    y = 24
    y = pdf.heading(y, "VI.  LES DEUX SCHISMES NUMERIQUES", "Tensions internes que le projet n'a pas clarifiees")

    y = pdf.subh(y, "Schisme 1 : 684 vs 618")
    y = pdf.p(y, "L'ancien calcul de la Basmala donnait Rahman (329) + Rahim (289) = 618, mais le projet a longtemps "
              "utilise 684 (19 x 36). La version actuelle a migre vers 618, recentrant le systeme sur le miroir de "
              "l'inverse de phi (0.618). Cette migration est documentee mais sa signification spirituelle n'est pas "
              "expliquee. Que perd-on en quittant 684 ? Que gagne-t-on en adoptant 618 ?", 7.6)

    y = pdf.box(y, "684 vs 618 — implications",
        ["684 = 19 x 36 — multiple parfait du Code 19, donc 'canonique'",
         "618 = 329 + 289 — somme brute de Rahman + Rahim, miroir de 0.618 (1/phi)",
         "684 - 618 = 66 — la difference est exactement la valeur abjad d'Allah (66)",
         "Le passage de 684 a 618 = soustraction du Nom Supreme. Signification : la misericorde (Rahman+Rahim) devient le centre, Allah (66) est retire du calcul mais present par soustraction."],
        accent=C["bordeaux"], bg=C["rose"])

    y = pdf.subh(y + 2, "Schisme 2 : 489 vs 500")
    y = pdf.p(y, "Fattah simple (sans le Ya d'appel) = 489. Ya Fattah (avec le Ya) = 500. "
              "Le projet utilise les deux sans clarifier quand utiliser l'un ou l'autre. "
              "489 x phi approx 791 -> 786 (Basmala). 500 x phi = 809, sans resonance claire. "
              "Le choix de 489 est operationnel mais le 500 reste present dans les invocations.", 7.6)

    y = pdf.box(y, "489 vs 500 — implications",
        ["489 = Fattah ( فتاح ) en abjad simple, sans le Ya — valeur 'nue' du nom",
         "500 = Ya Fattah ( يا فتاح ) avec le prefixe d'invocation Ya — valeur 'appelee'",
         "489 x phi -> 786 (Basmala) — resonance phi productive",
         "500 x phi = 809 — aucune resonance particuliere avec le systeme",
         "Le projet choisit 489 pour sa productivite mathematique, mais invoque 500 (Ya Fattah) dans les dhikrs"],
        accent=C["gold"], bg=C["sepia"])

    # ====== PAGE 6-7: NEW IDEAS ======
    pdf.ctx("IDEES NOUVELLES", "Prolongements naturels du systeme")
    pdf.add_page()
    pdf.frame()
    y = 24
    y = pdf.heading(y, "VII.  LES 6 IDEES NOUVELLES", "Prolongements coherents issus de l'analyse transversale")

    ideas = [
        ("1. Le Pont des 72+99", "Document dedie",
         ["Explorer en profondeur le pont 72 noms hebreux + 99 noms arabes = 171 = 19x9",
          "Calculer TOUTES les paires inter-traditionnelles en resonance phi",
          "Creer un index complet des 171 valeurs avec leurs reductions numerologiques",
          "Proposer des pratiques conjointes inter-traditionnelles",
          "Tester les rapports phi entre paires de noms (ex: Al-Razzaq / un nom hebreu de l'abondance)"]),
        ("2. Le Calendrier Lunaire Phi", "PDF + outil dynamique",
         ["Fusionner le Cadran Lunaire (28 mansions) avec le systeme phi",
          "Recalculer chaque mansion avec phi : 1xphi, 2xphi... 28xphi",
          "Chaque jour recoit un code Grabovoi, un dhikr et un anneau de talisman recalcules",
          "Creer un almanach perpetuel lunaire-phique",
          "Le cadran actuel utilise des nombres FIXES par mansion — les rendre DYNAMIQUES"]),
        ("3. La Gamme Doree", "Audio + meditation",
         ["Convertir les rapports phi en frequences audibles reelles",
          "7 Hz (Schumann) x phi = 11.33 Hz | 19 kHz / phi = 11.74 kHz | 56 Hz x phi = 90.6 Hz",
          "Creer une echelle musicale basee sur phi : 7 notes x 8 octaves x 19 intervalles",
          "Produire des pistes audio de meditation basees sur les nombres du projet",
          "Le quartz piezoelectrique de la radionique trouve ici sa contrepartie vibratoire directe"]),
    ]

    for title, dtype, lines in ideas:
        y = pdf.box(y, f"{title} [{dtype}]", lines, accent=C["gold"], bg=C["sepia"], ls=6.1)

    ideas2 = [
        ("4. Les 40 Portes", "Journal guide",
         ["Workbook pratique de 40 jours integrant TOUT le systeme",
          "Chaque jour : mansion lunaire + nombre du jour x phi + dhikr + espace de journaling",
          "7 semaines thematiques refletant les 7 niveaux de descente du Rizq",
          "Plus operatif et moins theorique que le Workbook existant",
          "Inclure le suivi des synchronicites, reves et signes numeriques"]),
        ("5. Le Talisman Vivant", "Application web",
         ["Etendre le webapp existant (app/webapp/) avec personalisation dynamique",
          "L'utilisateur entre son NOM (calcul abjad automatique) + DATE (mansion lunaire) + DOMAINE",
          "Generation d'un talisman UNIQUE avec le nom au centre du Buduh",
          "Les valeurs des anneaux sont recalculees en temps reel",
          "Export PNG + dhikr personnalise + code Grabovoi adapte"]),
        ("6. Le Dictionnaire des Resonances", "Reference exhaustive",
         ["Etendre au-dela des 4 racines actuelles (RZQ, SHKR, BRK, WQY)",
          "Ajouter : KHYR (bien), FDL (grace), N'MH (bienfait), KTHR (abondance), 'ATA (don), RSHAD (guidance)",
          "Pour chaque racine : abjad, occurrences, projection phi, voisin Fibonacci, domaine associe",
          "Creer un index complet des resonances numeriques du Rizq dans le Coran",
          "Decouvrir de nouvelles portes phi a partir des racines non explorees"]),
    ]

    for title, dtype, lines in ideas2:
        y = pdf.box(y, f"{title} [{dtype}]", lines, accent=C["bordeaux"], bg=C["rose"], ls=6.1)

    # ====== PAGE 8: SYNTHESIS DIAGRAM ======
    pdf.ctx("SYNTHESE FINALE", "La carte complete du systeme")
    pdf.add_page()
    pdf.frame()
    y = 24
    y = pdf.heading(y, "VIII.  CARTE COMPLETE DU SYSTEME", "Tous les elements et leurs relations")

    # Central diagram as text
    y = pdf.p(y, "Voici la structure integree de CORAN NUM TAL, reconstruite a partir de l'analyse des 10 PDFs :", 8, b=True)

    diagram = [
        "                    TEXTE SACRE (Coran, Torah, Evangiles grecs)",
        "                              |",
        "                    SYSTEMES NUMERIQUES",
        "              Abjad arabe | Guematria hebraique | Isopsephie grecque",
        "                              |",
        "              +---------------+--------------+",
        "              |                              |",
        "       NOMBRES-SOUCHES              PROJECTIONS PHI",
        "    19, 7, 8, 61, 76, 99         19x4xphi->123",
        "    123, 307, 319, 489             55xphi->89",
        "    618, 786                      489xphi->786",
        "    (matrice fixe)                618xphi->1000",
        "                                  61xphi->99",
        "              |                              |",
        "              +---------------+--------------+",
        "                              |",
        "              +---------------+--------------+",
        "              |               |              |",
        "          DHIKR          TALISMAN      RADIONIQUE",
        "       (repetition)    (geometrie)    (montage)",
        "       1-7-19-33-1    8 branches    cuivre+quartz",
        "       = 61            centre 618    7+19 tours",
        "                              |",
        "                    CODE GRABOVOI",
        "              520 741 8  =  7 + 19 + 8",
        "              56 96 152  =  7x8 + 19x8",
        "                              |",
        "                    CYCLE RITUEL",
        "              61 -> 99  (phi projection)",
        "              7, 21 ou 40 jours",
    ]
    for line in diagram:
        pdf.set_font("B", "", 6.5)
        pdf.set_text_color(*C["ink2"])
        pdf.set_xy(22, y)
        pdf.cell(170, 4, line)
        y += 4

    y += 4
    y = pdf.subh(y, "Les 3 piliers de coherence")
    y = pdf.box(y, "Pilier 1 — Triple signature",
        ["7 (multiplicateur) x 8 (directions) x 19 (code) = 1064",
         "Reduction : 1+0+6+4 = 11 -> 1+1 = 2 (temoin, equilibre)",
         "Cette signature est presente dans CHAQUE document sans exception."],
        accent=C["gold"], bg=C["sepia"])

    y = pdf.box(y, "Pilier 2 — Chaine universelle",
        ["Source (51:58) -> Corridor (34->55->56->89) -> Portail (618) -> Centre (56) -> Cycle (61->99)",
         "Cette chaine en 5 maillons est le schema invariant de tous les PDFs."],
        accent=C["bordeaux"], bg=C["rose"])

    y = pdf.box(y, "Pilier 3 — Pont inter-traditionnel",
        ["72 noms hebreux + 99 noms arabes = 171 = 19 x 9",
         "Sceau de Salomon : hebreu->19, arabe->8",
         "Ce pont est la decouverte la plus sous-exploitee du projet."],
        accent=C["gold"], bg=C["lav"])

    # ====== FINAL PAGE ======
    pdf.ctx("CONCLUSION", "Ce que cette analyse revele")
    pdf.add_page()
    pdf.frame()
    y = 24
    y = pdf.heading(y, "IX.  CONCLUSION", "Ce que l'analyse transversale revele")

    y = pdf.p(y, "CORAN NUM TAL n'est pas une collection de documents independants. C'est un systeme unique "
              "et coherent, reparti sur 10 PDFs et 94 pages, dont chaque element est une variation sur le meme "
              "theme fondamental : la transformation d'un texte sacre en champ operatif par le nombre.", 8, b=True)

    y = pdf.p(y, "Le triplet 7·8·19 est l'ADN du projet. Present dans chaque document, il agit comme une signature "
              "invisible qui garantit la coherence de l'ensemble. La chaine Source->Corridor->Portail->Centre->Cycle "
              "est le schema architectural invariant. Les 5 decouvertes phi sont les formules de passage entre les plans.", 7.6)

    y = pdf.p(y, "Deux schismes restent a resoudre : 684 vs 618 (le retrait d'Allah du calcul central) et 489 vs 500 "
              "(la tension entre la valeur nue et la valeur invoquee). Ces tensions ne sont pas des erreurs : elles sont "
              "la signature d'un systeme vivant, en evolution.", 7.6)

    y = pdf.p(y, "Le pont inter-traditionnel — 72 noms hebreux + 99 noms arabes = 171 = 19×9 — est la << piece manquante >> "
              "du projet. Mentionne dans le Workbook (p.34) mais jamais developpe, il represente le prolongement le plus "
              "naturel et le plus puissant du systeme.", 7.6)

    y = pdf.p(y, "Les 6 idees proposees (Pont des 72+99, Calendrier Lunaire Phi, Gamme Doree, 40 Portes, Talisman Vivant, "
              "Dictionnaire des Resonances) sont toutes des extensions directes et coherentes du materiau existant. "
              "Aucune ne part de zero : chacune prend appui sur un element deja present dans les PDFs.", 7.6)

    y = pdf.subh(y + 4, "Prochaines etapes recommandees")
    y = pdf.bullets(y, [
        "Creer le document 'Le Pont des 72+99' — la piece manquante la plus evidente",
        "Developper le Calendrier Lunaire Phi comme premier outil dynamique",
        "Refactoriser le webapp pour inclure le Talisman Vivant",
        "Produire la Gamme Doree en pistes audio reelles",
        "Rediger les 40 Portes comme workbook pratique de 40 jours",
    ], 7.3)

    y = y + 6
    pdf.set_draw_color(*C["gold"])
    pdf.set_line_width(0.4)
    pdf.line(55, y, 155, y)
    y += 7
    pdf.set_font("B", "I", 8)
    pdf.set_text_color(*C["muted"])
    pdf.set_xy(15, y)
    pdf.cell(180, 5, "Document genere le 17 mai 2026  |  Analyse par Claude (Anthropic)  |  Projet CORAN NUM TAL", align="C")
    y += 6
    pdf.set_font("Ar", "", 12)
    pdf.set_text_color(*C["gold"])
    pdf.set_xy(15, y)
    pdf.cell(180, 5, ar("والله من وراء القصد"), align="C")

    # Save
    out = Path("C:/Users/eddaz/Desktop/CORAN NUM TAL/exports/pdf/synthese_recherche.pdf")
    out.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(out))
    return out


if __name__ == "__main__":
    out = build()
    print(f"PDF genere : {out}")
