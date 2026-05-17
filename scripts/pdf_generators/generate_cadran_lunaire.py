#!/usr/bin/env python3
"""Cadran Lunaire Divinatoire Miftah 19 — 28 Mansions + 8 Phases + Codes Sacres"""

import math
from pathlib import Path
import sys
from fpdf import FPDF
import arabic_reshaper
from bidi.algorithm import get_display

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.project_paths import PDF_OUTPUTS, ensure_layout

ensure_layout()

LATIN = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
LATIN_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
ARIAL = "/mnt/c/Windows/Fonts/arial.ttf"

def ar(text):
    return get_display(arabic_reshaper.reshape(text))

def hb(text):
    return get_display(text)

CREAM = (255, 250, 240)
MIDNIGHT = (12, 12, 42)
DARK_VIOLET = (75, 0, 130)
BRIGHT_VIOLET = (138, 43, 226)
GOLD = (218, 165, 32)
GOLD_LIGHT = (240, 210, 100)
DARK_BG = (40, 20, 60)
BLACK = (20, 20, 20)
GRAY = (100, 100, 100)
RED = (180, 40, 40)


# ══════ 28 MANSIONS LUNARES ══════
MANSIONS = [
    (1,  "Al-Sharatain",   "\u0627\u0644\u0634\u0631\u0637\u064a\u0646",   "Cornes",      "Nouveau depart",       1),
    (2,  "Al-Butayn",      "\u0627\u0644\u0628\u0637\u064a\u0646",     "Ventre",       "Chance, reconquete",   7),
    (3,  "Al-Thurayya",    "\u0627\u0644\u062b\u0631\u064a\u0627",     "Pleiades",     "PROFIT, TOUT BIEN",   19),
    (4,  "Al-Dabaran",     "\u0627\u0644\u062f\u0628\u0631\u0627\u0646",   "Suiveur",      "Investissement",       8),
    (5,  "Al-Haqa",        "\u0627\u0644\u0647\u0642\u0639\u0629",       "Tache Blanche", "Etude, construction", 15),
    (6,  "Al-Hana",        "\u0627\u0644\u0647\u0646\u0639\u0629",       "Marque",        "Justice, chasse",      3),
    (7,  "Al-Dhira",       "\u0627\u0644\u0630\u0631\u0627\u0639",       "Avant-Bras",    "PROFIT, BIENS",        7),
    (8,  "Al-Nathrah",     "\u0627\u0644\u0646\u062b\u0631\u0629",      "Creche",        "Amitie, amour",        8),
    (9,  "Al-Tarf",        "\u0627\u0644\u0637\u0631\u0641",        "Regard",        "Ennemis, protection",  9),
    (10, "Al-Jabhah",      "\u0627\u0644\u062c\u0628\u0647\u0629",       "Front",         "Amour, guerison",     10),
    (11, "Al-Zubrah",      "\u0627\u0644\u0632\u0628\u0631\u0629",       "Criniere",      "COMMERCE, RICHESSE",  11),
    (12, "Al-Sarfah",      "\u0627\u0644\u0635\u0631\u0641\u0629",       "Queue Lion",   "Recolte, elevation",  12),
    (13, "Al-Awwa",        "\u0627\u0644\u0639\u0648\u0627\u0621",        "Aboyeur",       "COMMERCE, VOYAGE",    13),
    (14, "Al-Simak",       "\u0627\u0644\u0633\u0645\u0627\u0643",       "Spica",         "Guerison, moissons",  14),
    (15, "Al-Ghafr",       "\u0627\u0644\u063a\u0641\u0631",         "Voile",         "TRESORS CACHES",      15),
    (16, "Al-Zubana",      "\u0627\u0644\u0632\u0628\u0627\u0646\u0649",   "Pinces",        "ARGENT, GAINS $$$",   16),
    (17, "Al-Iklil",       "\u0627\u0644\u0625\u0643\u0644\u064a\u0644",    "Couronne",      "FORTUNE, MARIAGE",    17),
    (18, "Al-Qalb",        "\u0627\u0644\u0642\u0644\u0628",          "C\u0153ur",       "Protection",          18),
    (19, "Al-Shaulah",     "\u0627\u0644\u0634\u0648\u0644\u0629",     "Dard",          "CHANCE GENERALE",     19),
    (20, "Al-Naaim",       "\u0627\u0644\u0646\u0639\u0627\u0626\u0645",    "Autruches",     "Chasse, batiment",    20),
    (21, "Al-Baldah",      "\u0627\u0644\u0628\u0644\u062f\u0629",       "Cite",          "GAINS, VOYAGE",       21),
    (22, "Sa'd al-Dhabih", "\u0633\u0639\u062f \u0627\u0644\u0630\u0627\u0628\u062d", "Assassin",       "Liberation, soins",   22),
    (23, "Sa'd Bula",      "\u0633\u0639\u062f \u0628\u0644\u0639",        "Aviateur",      "Amitie, medecine",    23),
    (24, "Sa'd al-Su'ud",  "\u0633\u0639\u062f \u0627\u0644\u0633\u0639\u0648\u062f", "Fortune",        "Mariage, victoire",   24),
    (25, "Sa'd al-Akhbiyah","\u0633\u0639\u062f \u0627\u0644\u0623\u062e\u0628\u064a\u0629", "Tentes",         "Protection",          25),
    (26, "Al-Fargh al-Mukdim","\u0627\u0644\u0641\u0631\u063a \u0627\u0644\u0645\u0642\u062f\u0645", "1er Spout",     "GAINS, EMPLOI",       26),
    (27, "Al-Fargh al-Thani","\u0627\u0644\u0641\u0631\u063a \u0627\u0644\u062b\u0627\u0646\u064a", "2e Spout",       "GAINS, RECOLTE",      27),
    (28, "Batn al-Hut",    "\u0628\u0637\u0646 \u0627\u0644\u062d\u0648\u062a",   "Poisson",       "COMMERCE, ABONDANCE", 28),
]

PHASES = [
    (1,  "Nouvelle Lune",       "2017133", "Attirer la Chance",       "1"),
    (2,  "Croissant Croissant", "520 741 8","Argent Inattendu",       "7"),
    (3,  "Premier Quartier",    "87467894","Confiance Financiere",    "8"),
    (4,  "Gibbeuse Croissante", "318 798", "Abondance",              "19"),
    (5,  "Pleine Lune",         "9798733714615","Manifester l'Argent","15"),
    (6,  "Gibbeuse Decroissante","3657745","Independance Financiere", "33"),
    (7,  "Dernier Quartier",    "9213140", "Revenu Stable",           "61"),
    (8,  "Croissant Decroissant","318 612 518 714","Cash-Flow Abondant","56"),
]


class Cadran(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.add_font("L", "", LATIN, uni=True)
        self.add_font("L", "B", LATIN_B, uni=True)
        self.add_font("A", "", ARIAL, uni=True)
        self.set_auto_page_break(False)


def draw_cadran():
    pdf = Cadran()
    pdf.add_page()

    pdf.set_fill_color(*CREAM)
    pdf.rect(0, 0, 210, 297, 'F')

    cx, cy = 105.0, 150.0

    # ═══════════════════ CERCLES ═══════════════════
    circle_defs = [
        (90, GOLD, 0.8),
        (81, BRIGHT_VIOLET, 0.4),
        (58, DARK_VIOLET, 0.5),
        (35, GOLD, 0.4),
        (14, DARK_BG, 0.4),
    ]
    for r, col, lw in circle_defs:
        pdf.set_draw_color(*col)
        pdf.set_line_width(lw)
        pdf.circle(cx, cy, r, 'D')

    # ═══════════════ ANNEAU EXTERNE : 28 MANSIONS ═══════════════
    R_mans = 85
    ang_step = 360.0 / 28.0  # ~12.857°

    wealth_mansions = {3, 7, 11, 13, 15, 16, 17, 19, 21, 26, 27, 28}
    for idx, (num, name, _, _, _, _) in enumerate(MANSIONS):
        deg = 270 - idx * ang_step
        rad = math.radians(deg)
        x = cx + R_mans * math.cos(rad)
        y = cy - R_mans * math.sin(rad)

        is_wealth = num in wealth_mansions
        txt_col = GOLD if is_wealth else DARK_VIOLET
        fsize = 5.5 if is_wealth else 4.5

        # Ligne radiale
        pdf.set_draw_color(*GOLD)
        pdf.set_line_width(0.15)
        xr = cx + 80.5 * math.cos(rad)
        yr = cy - 80.5 * math.sin(rad)
        pdf.line(cx + 58 * math.cos(rad), cy - 58 * math.sin(rad), xr, yr)

        # Numero
        pdf.set_font("L", "B", 6 if is_wealth else 5)
        pdf.set_text_color(*txt_col)
        pdf.set_xy(x - 8, y - 8)
        pdf.cell(16, 0, str(num), align="C")

        # Nom
        pdf.set_font("L", "B" if is_wealth else "", fsize)
        pdf.set_text_color(*txt_col)
        pdf.set_xy(x - 14, y - 2)
        pdf.cell(28, 0, name, align="C")

    # ═══════════════ ANNEAU 2 : 8 PHASES LUNAIRES ═══════════════
    R_phase = 69
    phase_angles = [270, 225, 180, 135, 90, 45, 0, 315]
    for i, (num, name, code, label, qnum) in enumerate(PHASES):
        deg = phase_angles[i]
        rad = math.radians(deg)
        x = cx + R_phase * math.cos(rad)
        y = cy - R_phase * math.sin(rad)

        # Moon phase symbol (circle)
        moon_r = 4
        pdf.set_fill_color(*MIDNIGHT if i != 4 else GOLD_LIGHT)
        pdf.set_draw_color(*GOLD)
        pdf.set_line_width(0.3)
        pdf.circle(x, y, moon_r, 'DF')

        # Phase name + code
        off_x = [0, 15, 18, 15, 0, -15, -18, -15][i]
        off_y = [-15, -10, 0, 10, 12, 10, 0, -10][i]
        pdf.set_font("L", "B", 6)
        pdf.set_text_color(*DARK_VIOLET)
        pdf.set_xy(x + off_x - 20, y + off_y - 6)
        pdf.cell(40, 0, name, align="C")
        pdf.set_font("L", "", 5)
        pdf.set_text_color(*GRAY)
        pdf.set_xy(x + off_x - 20, y + off_y)
        pdf.cell(40, 0, f"Code: {code}", align="C")
        pdf.set_font("L", "", 4.5)
        pdf.set_text_color(*BRIGHT_VIOLET)
        pdf.set_xy(x + off_x - 20, y + off_y + 4)
        pdf.cell(40, 0, f"Numero Sacre: {qnum}", align="C")

    # ═══════════════ ANNEAU 3 : NUMEROS SACRES ═══════════════
    R_sacre = 47
    sacred_angles = [270, 0, 90, 180]
    sacred = [
        ("7", "Multiplicateur\ndu Rizq"),
        ("19", "Code Sacre\ndu Coran"),
        ("8", "Directions\ndu Talisman"),
        ("56", "Al-Waqi'a\nSourate Richesse"),
    ]
    for (val, desc), deg in zip(sacred, sacred_angles):
        rad = math.radians(deg)
        x = cx + R_sacre * math.cos(rad)
        y = cy - R_sacre * math.sin(rad)

        pdf.set_fill_color(*MIDNIGHT)
        pdf.set_draw_color(*GOLD)
        pdf.set_line_width(0.3)
        pdf.rect(x - 10, y - 10, 20, 20, 'DF')

        pdf.set_font("L", "B", 10)
        pdf.set_text_color(*GOLD)
        pdf.set_xy(x - 9, y - 8)
        pdf.cell(18, 0, val, align="C")

        for li, line in enumerate(desc.split("\n")):
            pdf.set_font("L", "", 4.5)
            pdf.set_text_color(*GOLD_LIGHT)
            pdf.set_xy(x - 9, y + 2 + li * 4)
            pdf.cell(18, 0, line, align="C")

    # ═══════════════ CENTRE : CARRE BUDUH ═══════════════
    buduh = [["4", "9", "2"], ["3", "5", "7"], ["8", "1", "6"]]
    cw, ch = 8, 8
    bx0, by0 = cx - 12, cy - 12
    for i in range(3):
        for j in range(3):
            x, y = bx0 + j * cw, by0 + i * ch
            pdf.set_fill_color(*DARK_BG)
            pdf.set_draw_color(*GOLD)
            pdf.set_line_width(0.4)
            pdf.rect(x, y, cw, ch, 'DF')
            pdf.set_font("L", "B", 8)
            pdf.set_text_color(*GOLD)
            pdf.set_xy(x, y + 0.5)
            pdf.cell(cw, ch - 1, buduh[i][j], align="C")

    # ═══════════════ TITRE ═══════════════
    pdf.set_font("L", "B", 14)
    pdf.set_text_color(*DARK_VIOLET)
    pdf.set_xy(0, 16)
    pdf.cell(210, 7, "C A D R A N   L U N A I R E   D I V I N A T O I R E", align="C")
    pdf.set_font("L", "", 7)
    pdf.set_text_color(*GRAY)
    pdf.set_xy(0, 24)
    pdf.cell(210, 4, "Miftah 19  |  28 Mansions Lunaires  |  8 Phases  |  Codes Grabovoi  |  Nombres Sacres Coraniques", align="C")
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.3)
    pdf.line(25, 29, 185, 29)

    # ═══════════════ LEGENDE ═══════════════
    yl = 270
    legends = [
        ("Anneau 1: 28 Mansions Lunaires (noms arabes + proprietes)", GOLD),
        ("Anneau 2: 8 Phases Lunaires + Codes Grabovoi + Nombres Sacres", DARK_VIOLET),
        ("Anneau 3: 4 Nombres Sacres Fondamentaux (7, 19, 8, 56)", MIDNIGHT),
        ("Centre: Carre Magique Buduh 3x3 (constante 15)", GOLD),
        ("ETOILE = Mansions de Richesse (3,7,11,13,15,16,17,19,21,26,27,28)", GOLD),
        ("Comment utiliser: Trouvez la mansion lunaire actuelle, lisez les codes correspondants", BLACK),
    ]
    for idx, (txt, col) in enumerate(legends):
        col_idx = idx // 2
        row_idx = idx % 2
        lx = 15 + col_idx * 98
        ly = yl + row_idx * 7
        pdf.set_fill_color(*col)
        pdf.set_xy(lx, ly)
        pdf.cell(3, 3, "", fill=True)
        pdf.set_font("L", "", 5)
        pdf.set_text_color(*BLACK)
        pdf.set_xy(lx + 4, ly - 0.5)
        pdf.cell(92, 3, txt, align="L")

    # ═══════════════ FLECHE INDICATRICE ═══════════════
    # Arrow at top (0° / 270° in math coords)
    arrow_deg = 270
    arrow_rad = math.radians(arrow_deg)
    ax0, ay0 = cx + 70 * math.cos(arrow_rad), cy - 70 * math.sin(arrow_rad)
    ax1, ay1 = cx + 55 * math.cos(arrow_rad), cy - 55 * math.sin(arrow_rad)
    # Arrow head
    aleft_x = cx + 60 * math.cos(arrow_rad - 0.15) - cy
    aleft_y = cy - 60 * math.sin(arrow_rad - 0.15)

    pdf.set_draw_color(*RED)
    pdf.set_line_width(0.8)
    pdf.line(ax0, ay0, ax1, ay1)
    # Simple triangle pointer
    pdf.set_fill_color(*RED)
    pdf.set_draw_color(*RED)
    ax_h = cx + 68 * math.cos(arrow_rad)
    ay_h = cy - 68 * math.sin(arrow_rad)
    alx = cx + 63 * math.cos(math.radians(arrow_deg - 3))
    aly = cy - 63 * math.sin(math.radians(arrow_deg - 3))
    arx = cx + 63 * math.cos(math.radians(arrow_deg + 3))
    ary = cy - 63 * math.sin(math.radians(arrow_deg + 3))
    pdf.polygon([(ax_h, ay_h), (alx, aly), (arx, ary)], 'DF')

    # ═══════════════ SAVE ═══════════════
    output = PDF_OUTPUTS["cadran_lunaire_pdf"]
    # output called at end of function

    # ═══════════════ PAGE 2 : TABLEAU COMPLET ═══════════════
    pdf.add_page()
    pdf.set_fill_color(*CREAM)
    pdf.rect(0, 0, 210, 297, 'F')

    pdf.set_font("L", "B", 12)
    pdf.set_text_color(*DARK_VIOLET)
    pdf.set_xy(0, 14)
    pdf.cell(210, 6, "TABLEAU COMPLET DES 28 MANSIONS LUNAIRES", align="C")
    pdf.set_font("L", "", 6)
    pdf.set_text_color(*GRAY)
    pdf.set_xy(0, 21)
    pdf.cell(210, 4, "Systeme divinatoire Miftah 19 — Correspondances Numeriques pour Richesses et Jeux de Hasard", align="C")
    pdf.set_draw_color(*GOLD)
    pdf.line(15, 26, 195, 26)

    # Header
    y0 = 30
    pdf.set_fill_color(*DARK_BG)
    pdf.set_text_color(*GOLD)
    pdf.set_font("L", "B", 5.5)
    pdf.set_xy(15, y0)
    cols = [("N", 6), ("Nom Arabe", 25), ("Propriete", 30), ("Ph. Lun.", 14), ("N Sacre", 10), ("Code Grabovoi", 28), ("Lucky #", 10), ("Jeux", 50)]
    for name, w in cols:
        pdf.cell(w, 5, name, border=1, fill=True, align="C")
    pdf.ln()

    for idx, (num, name, aname, _, prop, _) in enumerate(MANSIONS):
        phase_idx = idx // 4
        phase_name = PHASES[phase_idx][1]
        qnum = PHASES[phase_idx][4]
        gcode = PHASES[phase_idx][2]

        # Lucky number derivation
        lucky = (num * 7 + idx + 1) % 49
        if lucky == 0:
            lucky = 49

        wealth = "OUI" if num in wealth_mansions else "non"
        games = "LOTO, PARIS, HIPPIQUE" if num in wealth_mansions else "A eviter"

        y = y0 + 5 + idx * 5
        pdf.set_font("L", "B" if num in wealth_mansions else "", 5)
        pdf.set_text_color(*GOLD if num in wealth_mansions else DARK_VIOLET)
        pdf.set_xy(15, y)
        pdf.cell(6, 4, str(num), border=1 if num in wealth_mansions else 0, align="C")
        pdf.set_font("A", "", 5.5)
        pdf.set_text_color(*BLACK)
        pdf.cell(25, 4, ar(aname), border=0, align="C")

        pdf.set_font("L", "", 5)
        pdf.set_text_color(*BLACK)
        pdf.cell(30, 4, prop, border=0, align="L")
        pdf.cell(14, 4, phase_name, border=0, align="C")
        pdf.set_font("L", "B", 5)
        pdf.set_text_color(*DARK_VIOLET)
        pdf.cell(10, 4, qnum, border=0, align="C")
        pdf.set_font("L", "", 4.5)
        pdf.set_text_color(*GRAY)
        pdf.cell(28, 4, gcode, border=0, align="C")
        pdf.set_font("L", "B", 6)
        pdf.set_text_color(*GOLD if num in wealth_mansions else BLACK)
        pdf.cell(10, 4, str(lucky), border=1 if num in wealth_mansions else 0, fill=num in wealth_mansions, align="C")

        pdf.set_font("L", "B" if num in wealth_mansions else "", 5)
        pdf.set_text_color(*RED if num in wealth_mansions else GRAY)
        pdf.cell(50, 4, games, border=0, align="L")
        pdf.ln()

    # ═══════════════ MODE D'EMPLOI ═══════════════
    pdf.set_y(pdf.get_y() + 6)
    pdf.set_font("L", "B", 9)
    pdf.set_text_color(*DARK_VIOLET)
    pdf.set_xy(15, pdf.get_y())
    pdf.cell(0, 5, "MODE D'EMPLOI DU CADRAN DIVINATOIRE", align="L")
    pdf.ln(7)

    instructions = [
        "1. Determinez la mansion lunaire actuelle (app mobile: 'Moon Calendar', 'Lunar Phase' ou site web d'astronomie)",
        "2. Localisez-la sur le cadran (anneau externe, mansions 1 a 28)",
        "3. Relevez le Numero Sacre et le Code Grabovoi correspondant a la phase",
        "4. Utilisez le Lucky Number pour vos jeux de hasard (loto, Keno, roulette)",
        "5. Verifiez si la mansion est marquee RICHESSE (ETOILE) — si oui, jour favorable",
        "6. Pour les paris sportifs/hippiques : utilisez le N de mansion comme numero de cheval/joueur",
        "7. Combinez toujours avec le Code Al-Waqi'a (56 96 152) en recitant la Sourate avant de jouer",
        "8. Les mansions 3, 7, 11, 16, 19, 28 sont les plus puissantes pour les gains $$$",
    ]
    for instr in instructions:
        pdf.set_font("L", "", 6.5)
        pdf.set_text_color(*BLACK)
        pdf.set_x(18)
        pdf.multi_cell(175, 4, instr)

    pdf.ln(4)
    pdf.set_font("L", "B", 7)
    pdf.set_text_color(*DARK_VIOLET)
    pdf.set_x(15)
    pdf.cell(0, 5, "FORMULE DU LUCKY NUMBER : (Mansion# x 7 + IndexJour) mod 49  |  Si resultat = 0, prendre 49", align="L")
    pdf.ln(5)
    pdf.set_font("L", "", 6)
    pdf.set_text_color(*GRAY)
    pdf.set_x(15)
    pdf.cell(0, 4, "AVERTISSEMENT : Ce systeme est un outil de guidance et de synchronicite. Le jeu comporte des risques. Jouez avec moderation et responsabilite.", align="L")

    output2 = output
    pdf.output(str(output2))
    print(f"Cadran Lunaire genere : {output}")
    print("28 Mansions | 8 Phases | 7 Cercles | Codes Grabovoi integres")
    print("Page 1: Cadran Lunaire  |  Page 2: Tableau complet + Mode d'emploi")


if __name__ == "__main__":
    draw_cadran()
