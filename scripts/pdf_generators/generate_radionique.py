#!/usr/bin/env python3
"""Fiche Pratique Radionique Miftah 19 — Schema de Montage Spirale Cuivre + Quartz"""

import math
from pathlib import Path
import sys
from fpdf import FPDF

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.project_paths import PDF_OUTPUTS, ensure_layout

ensure_layout()

LATIN = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
LATIN_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

CREAM = (255, 250, 240)
MIDNIGHT = (12, 12, 42)
DARK_VIOLET = (75, 0, 130)
GOLD = (218, 165, 32)
GOLD_LIGHT = (240, 210, 100)
BRIGHT_VIOLET = (138, 43, 226)
DARK_BG = (40, 20, 60)
BLACK = (20, 20, 20)
GRAY = (100, 100, 100)
COPPER = (184, 115, 51)
LIGHT_COPPER = (220, 160, 80)


class RadioniquePDF(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.add_font("L", "", LATIN, uni=True)
        self.add_font("L", "B", LATIN_B, uni=True)
        self.set_auto_page_break(False)


def draw_radionique():
    pdf = RadioniquePDF()

    # ═══════════════════ PAGE 1 : SCHEMA DE MONTAGE ═══════════════════
    pdf.add_page()
    pdf.set_fill_color(*CREAM)
    pdf.rect(0, 0, 210, 297, 'F')

    cx, cy = 105.0, 130.0

    # ── TITRE ──
    pdf.set_font("L", "B", 14)
    pdf.set_text_color(*DARK_VIOLET)
    pdf.set_xy(0, 14)
    pdf.cell(210, 7, "R A D I O N I Q U E   S A C R E E   M I F T A H   1 9", align="C")
    pdf.set_font("L", "", 7)
    pdf.set_text_color(*GRAY)
    pdf.set_xy(0, 22)
    pdf.cell(210, 4, "Methode de materialisation des codes numeriques  |  Spirale de Cuivre  |  Quartz Piezoelectrique", align="C")

    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.3)
    pdf.line(35, 27, 175, 27)

    # ── CERCLES DE LA FEUILLE DE CODES ──
    # Outer circle (paper edge)
    pdf.set_draw_color(*DARK_VIOLET)
    pdf.set_line_width(0.6)
    pdf.set_fill_color(*CREAM)
    pdf.circle(cx, cy, 75, 'D')

    # Concentric guide circles
    for r, col, lw, dash in [
        (70, GOLD, 0.3, True),
        (55, BRIGHT_VIOLET, 0.25, True),
        (42, DARK_VIOLET, 0.25, True),
        (28, GOLD, 0.3, True),
    ]:
        pdf.set_draw_color(*col)
        pdf.set_line_width(lw)
        pdf.circle(cx, cy, r, 'D')

    # ── CODES DANS LES ANNEAUX ──
    # Ring 1 (outer): Grabovoi codes at 4 directions
    codes_grab = [
        (270, "520 741 8", "Argent Inattendu"),
        (0, "318 798", "Abondance"),
        (90, "318 612 518 714", "Cash-Flow"),
        (180, "9798733714615", "Manifester"),
    ]
    for deg, code, label in codes_grab:
        rad = math.radians(deg)
        x = cx + 62 * math.cos(rad)
        y = cy - 62 * math.sin(rad)
        pdf.set_font("L", "B", 7)
        pdf.set_text_color(*DARK_VIOLET)
        offx = -15 if deg == 180 else (2 if deg == 0 else -18)
        offy = -14 if deg == 270 else (4 if deg == 90 else -3)
        pdf.set_xy(x + offx, y + offy)
        pdf.cell(36, 4, code, align="C")
        pdf.set_font("L", "", 5)
        pdf.set_text_color(*GRAY)
        pdf.set_xy(x + offx, y + offy + 4)
        pdf.cell(36, 3, label, align="C")

    # Ring 2: Sacred numbers
    sacred_nums = [
        (315, "56", "Al-Waqi'a"),
        (45, "19", "Code Sacre"),
        (135, "7", "Multiplicateur"),
        (225, "152", "19x8"),
    ]
    for deg, num, label in sacred_nums:
        rad = math.radians(deg)
        x = cx + 48 * math.cos(rad)
        y = cy - 48 * math.sin(rad)
        pdf.set_fill_color(*DARK_BG)
        pdf.set_draw_color(*GOLD)
        pdf.set_line_width(0.3)
        pdf.rect(x - 8, y - 7, 16, 14, 'DF')
        pdf.set_font("L", "B", 9)
        pdf.set_text_color(*GOLD)
        pdf.set_xy(x - 7, y - 5)
        pdf.cell(14, 5, num, align="C")
        pdf.set_font("L", "", 4.5)
        pdf.set_text_color(*GOLD_LIGHT)
        pdf.set_xy(x - 7, y + 1)
        pdf.cell(14, 3, label, align="C")

    # Ring 3: 4 Divine Names
    div_names = [
        (270, "Ya Razzaq", "319"),
        (0, "Ya Fattah", "489"),
        (90, "Ya Ghani", "1060"),
        (180, "Ya Mughni", "1100"),
    ]
    for deg, name, val in div_names:
        rad = math.radians(deg)
        x = cx + 35 * math.cos(rad)
        y = cy - 35 * math.sin(rad)
        offx = -10 if deg == 180 else (3 if deg == 270 else (0 if deg == 90 else 5))
        offy = -10 if deg == 270 else (5 if deg == 90 else (-2 if deg == 0 else -1))
        pdf.set_font("L", "B", 7)
        pdf.set_text_color(*BRIGHT_VIOLET)
        pdf.set_xy(x + offx, y + offy)
        pdf.cell(20, 4, name, align="C")
        pdf.set_font("L", "", 5)
        pdf.set_text_color(*GRAY)
        pdf.set_xy(x + offx, y + offy + 4)
        pdf.cell(20, 3, val, align="C")

    # ── ZONE PHOTO (centre) ──
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.6)
    pdf.set_fill_color(245, 240, 235)
    pdf.rect(cx - 22, cy - 28, 44, 56, 'DF')
    pdf.set_font("L", "B", 8)
    pdf.set_text_color(*DARK_VIOLET)
    pdf.set_xy(cx - 21, cy - 14)
    pdf.cell(42, 5, "PLACEZ", align="C")
    pdf.set_xy(cx - 21, cy - 8)
    pdf.cell(42, 5, "VOTRE", align="C")
    pdf.set_xy(cx - 21, cy - 2)
    pdf.cell(42, 5, "PHOTO", align="C")
    pdf.set_xy(cx - 21, cy + 4)
    pdf.cell(42, 5, "ICI", align="C")
    pdf.set_font("L", "", 6)
    pdf.set_text_color(*GRAY)
    pdf.set_xy(cx - 21, cy + 12)
    pdf.cell(42, 4, "(face vers le bas)", align="C")
    pdf.set_xy(cx - 21, cy + 17)
    pdf.cell(42, 4, "contre les codes", align="C")

    # ── SPIRALE DE CUIVRE ──
    pdf.set_draw_color(*COPPER)
    # Draw spiral using Bezier-like segments
    spiral_turns = 7
    max_r = 60
    points = []
    for i in range(0, 360 * spiral_turns, 8):
        theta = math.radians(i)
        r = max_r * (1 - i / (360 * spiral_turns) * 0.7)
        if r < 3:
            r = 3
        px = cx + r * math.cos(theta)
        py = cy - r * math.sin(theta)
        points.append((px, py))

    pdf.set_line_width(1.2)
    for i in range(len(points) - 1):
        pdf.set_draw_color(*COPPER)
        pdf.line(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1])

    # Légende spirale
    pdf.set_font("L", "", 6)
    pdf.set_text_color(*COPPER)
    pdf.set_xy(cx - 65, cy - 72)
    pdf.cell(40, 4, "SPIRALE CUIVRE", align="L")
    pdf.set_text_color(*GRAY)
    pdf.set_xy(cx - 65, cy - 68)
    pdf.cell(40, 3, "7 tours | fil 1mm | 56cm", align="L")

    # ── CRISTAL DE QUARTZ ──
    # Draw crystal at center (pointing up)
    crystal_x, crystal_y = cx, cy - 2
    pdf.set_fill_color(230, 230, 255)
    pdf.set_draw_color(*GRAY)
    pdf.set_line_width(0.5)
    # Pyramid/point shape
    pdf.polygon([
        (crystal_x, crystal_y - 12),
        (crystal_x - 5, crystal_y),
        (crystal_x + 5, crystal_y),
    ], 'DF')
    pdf.set_fill_color(240, 240, 255)
    pdf.set_draw_color(*GRAY)
    pdf.polygon([
        (crystal_x, crystal_y + 10),
        (crystal_x - 4, crystal_y),
        (crystal_x + 4, crystal_y),
    ], 'DF')

    # Ley lines from crystal
    for a in range(0, 360, 45):
        rad = math.radians(a)
        pdf.set_draw_color(*COPPER)
        pdf.set_line_width(0.2)
        pdf.dashed_line(crystal_x, crystal_y,
                        crystal_x + 15 * math.cos(rad),
                        crystal_y - 15 * math.sin(rad), 2, 1.5)

    pdf.set_font("L", "", 6)
    pdf.set_text_color(*GRAY)
    pdf.set_xy(cx - 65, cy - 60)
    pdf.cell(40, 4, "CRISTAL DE QUARTZ", align="L")
    pdf.set_xy(cx - 65, cy - 56)
    pdf.cell(40, 3, "Pointe vers le haut", align="L")
    pdf.set_xy(cx - 65, cy - 52)
    pdf.cell(40, 3, "Amplifie la frequence", align="L")

    # ── EVENTAIL D'INFORMATION ──
    # Bottom section
    y_info = 220
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.3)
    pdf.line(30, y_info - 4, 180, y_info - 4)

    pdf.set_font("L", "B", 9)
    pdf.set_text_color(*DARK_VIOLET)
    pdf.set_xy(15, y_info)
    pdf.cell(0, 5, "PROTOCOLE DE MONTAGE RADIONIQUE", align="C")

    # Instructions
    steps = [
        "1. Sur une feuille blanche A4, recopiez les codes ci-dessus en respectant les positions circulaires",
        "2. Placez votre photo (portrait, visage centre) FACE VERS LE BAS sur la zone centrale",
        "3. Prenez un fil de cuivre (1mm diametre, 56cm de long) et formez une spirale de 7 tours",
        "4. Posez la spirale de cuivre PAR-DESSUS la photo, au centre des cercles de codes",
        "5. Placez un cristal de quartz pointe en haut, au CENTRE de la spirale",
        "6. Laissez le montage en place 7, 19 ou 40 jours consecutifs",
        "7. Chaque matin, posez votre main droite au-dessus du quartz et visualisez la lumiere doree",
    ]

    y_step = y_info + 8
    for step in steps:
        pdf.set_font("L", "", 6.5)
        pdf.set_text_color(*BLACK)
        pdf.set_x(25)
        pdf.set_xy(25, y_step)
        pdf.multi_cell(165, 4, step)
        y_step += 5

    # ═══════════════════ PAGE 2 : THEORIE + CORRESPONDANCES ═══════════════════
    pdf.add_page()
    pdf.set_fill_color(*CREAM)
    pdf.rect(0, 0, 210, 297, 'F')

    pdf.set_font("L", "B", 12)
    pdf.set_text_color(*DARK_VIOLET)
    pdf.set_xy(0, 14)
    pdf.cell(210, 6, "THEORIE RADIONIQUE ET CORRESPONDANCES NUMERIQUES", align="C")

    pdf.set_draw_color(*GOLD)
    pdf.line(30, 22, 180, 22)

    # ── SECTION 1: POURQUOI CA MARCHE ──
    pdf.set_font("L", "B", 10)
    pdf.set_text_color(*DARK_VIOLET)
    pdf.set_xy(18, 28)
    pdf.cell(0, 5, "I. PRINCIPES FONDAMENTAUX", align="L")

    principles = [
        ("CODES = FREQUENCES", "Chaque nombre est une vibration. En ecrivant les codes sur un support physique, vous imprimez une frequence dans la matiere. Le papier devient un oscillateur passif."),
        ("PHOTO = LIAISON SYMPATHIQUE", "La photo agit comme temoin (witness en radionique). Elle cree un pont energetique entre les codes et votre champ biophotonique."),
        ("CUIVRE = ANTENNE", "Le cuivre est le meilleur conducteur energetique apres l'argent. La spirale de 7 tours cree une cavite resonnante qui amplifie la frequence des codes par induction. La longueur de 56cm correspond a la Sourate Al-Waqi'a."),
        ("QUARTZ = AMPLIFICATEUR", "Le quartz est piezoelectrique : il convertit la pression mecanique en charge electrique et vice-versa. La pointe focalise l'energie comme un laser. Le quartz programme et stocke l'information vibratoire."),
        ("GEOMETRIE SACREE", "Les cercles concentriques + la spirale + le rectangle de la photo forment une antenne fractale. Les 8 directions + les 7 tours de spire = 56 = Al-Waqi'a = 7x8."),
    ]
    y = 35
    for title, desc in principles:
        pdf.set_font("L", "B", 7.5)
        pdf.set_text_color(*GOLD)
        pdf.set_xy(22, y)
        pdf.cell(0, 4, title, align="L")
        pdf.set_font("L", "", 6.5)
        pdf.set_text_color(*BLACK)
        pdf.set_xy(22, y + 4)
        pdf.multi_cell(170, 3.5, desc)
        y += 16

    # ── SECTION 2: CORRESPONDANCES ──
    y = 125
    pdf.set_font("L", "B", 10)
    pdf.set_text_color(*DARK_VIOLET)
    pdf.set_xy(18, y)
    pdf.cell(0, 5, "II. TABLEAU DES CORRESPONDANCES RADIONIQUES", align="L")
    y += 8

    pdf.set_fill_color(*DARK_BG)
    pdf.set_text_color(*GOLD)
    pdf.set_font("L", "B", 6)
    pdf.set_xy(18, y)
    headers = [("Element physique", 35), ("Nombre sacre", 22), ("Frequence equivalente", 35), ("Effet radionique", 82)]
    for h, w in headers:
        pdf.cell(w, 5, h, border=1, fill=True, align="C")
    pdf.ln()

    correspondances = [
        ("Feuille blanche A4", "1 (Tawhid)", "Support neutre, receptif", "Matrice vierge pret a recevoir le programme"),
        ("4 codes Grabovoi", "7, 8, 19", "520 Hz, 318 Hz, etc.", "Encodage des frequences de richesse dans le papier"),
        ("Photo personnelle", "33 (Paradis)", "Signature biophotonique", "Lie le code a votre ADN energetique"),
        ("Fil de cuivre 56cm", "56 (Waqi'a)", "Resonance 56 Hz", "Antenne spiralee amplifiant la frequence 7x8"),
        ("7 tours de spire", "7 (Rizq)", "Harmonique 7", "Multiplicateur divin de la provision"),
        ("8 directions cercle", "8 (Talisman)", "Octave superieure", "Distribution multi-directionnelle de l'energie"),
        ("Quartz pointe", "19 (Code)", "Piezoelectrique 19kHz", "Amplificateur et stabilisateur du signal"),
        ("Montage complet", "152 (19x8)", "Synergie totale", "Oscillateur Rizq autonome actif 24/7"),
    ]
    for i, (elem, num, freq, effect) in enumerate(correspondances):
        pdf.set_font("L", "", 6)
        pdf.set_text_color(*BLACK)
        pdf.set_xy(18, pdf.get_y())
        pdf.cell(35, 5, elem, border=1, align="C")
        pdf.set_text_color(*GOLD)
        pdf.set_font("L", "B", 7)
        pdf.cell(22, 5, num, border=1, align="C")
        pdf.set_font("L", "", 6)
        pdf.set_text_color(*GRAY)
        pdf.cell(35, 5, freq, border=1, align="C")
        pdf.set_text_color(*BLACK)
        pdf.set_font("L", "", 5.5)
        pdf.cell(82, 5, effect, border=1, align="L")
        pdf.ln()

    # ── SECTION 3: PROTOCOLE D'ACTIVATION ──
    y = pdf.get_y() + 6
    pdf.set_font("L", "B", 10)
    pdf.set_text_color(*DARK_VIOLET)
    pdf.set_xy(18, y)
    pdf.cell(0, 5, "III. PROTOCOLE D'ACTIVATION JOURNALIER", align="L")
    y += 8

    protocols = [
        ("MATIN (Fajr)", "Posez la main droite au-dessus du quartz. Recitez la Basmala (786) 1x. Visualisez une lumiere doree descendant du ciel, traversant le quartz, la spirale, et entrant dans votre photo. Durée : 3 minutes."),
        ("MIDI (Duha)", "Recitez les 4 Noms Divins (Ya Razzaq, Ya Fattah, Ya Ghani, Ya Mughni) 1x chacun. Visualisez 4 rayons de lumiere (rouge, vert, bleu, or) convergeant vers le quartz."),
        ("SOIR (Maghrib)", "Recitez Sourate Al-Waqi'a (56) ou son code 56-96-152. Passez votre main gauche en cercle autour du montage 7 fois dans le sens horaire."),
        ("AVANT SOMMEIL", "Placez vos deux mains en triangle au-dessus du quartz. Visualisez le code 56 96 152 s'inscrire en lettres dorees dans le cristal. Remerciez. Dormez."),
    ]
    for title, desc in protocols:
        pdf.set_font("L", "B", 7)
        pdf.set_text_color(*GOLD)
        pdf.set_xy(22, y)
        pdf.cell(0, 4, title, align="L")
        pdf.set_font("L", "", 6)
        pdf.set_text_color(*BLACK)
        pdf.set_xy(22, y + 4)
        pdf.multi_cell(170, 3.5, desc)
        y += 16

    # ── SECTION 4: RECOMMANDATIONS ──
    y += 4
    pdf.set_font("L", "B", 10)
    pdf.set_text_color(*DARK_VIOLET)
    pdf.set_xy(18, y)
    pdf.cell(0, 5, "IV. RECOMMANDATIONS ET PRECAUTIONS", align="L")
    y += 8

    recos = [
        "Utilisez du cuivre pur (fil electrique denude ou fil de bijouterie 1mm)",
        "Quartz : cristal de roche transparent, pointe naturelle, environ 3-5cm de long",
        "Ne deplacez pas le montage pendant la periode active (7/19/40 jours)",
        "Apres la periode, demontez en remerciant. Purifiez le quartz a l'eau claire + soleil 1h",
        "Vous pouvez reutiliser le quartz pour un autre montage apres purification",
        "Conservez la feuille de codes dans votre portefeuille ou sous votre oreiller apres demontage",
        "Le montage fonctionne 24h/24. Plus vous le maintenez, plus l'effet est profond",
        "N'utilisez PAS ce montage pour nuire a autrui. La loi du retour est absolue",
    ]
    for rec in recos:
        pdf.set_font("L", "", 6)
        pdf.set_text_color(*BLACK)
        pdf.set_xy(22, y)
        pdf.cell(4, 4, "\u2022", align="C")
        pdf.multi_cell(170, 4, rec)
        y += 5.5

    # ── SIGNATURE ──
    y += 5
    pdf.set_draw_color(*GOLD)
    pdf.line(60, y, 150, y)
    y += 4
    pdf.set_font("L", "", 6)
    pdf.set_text_color(*GRAY)
    pdf.set_xy(0, y)
    pdf.cell(210, 4, "Radionique Sacree Miftah 19  |  Edition 2026  |  Base sur les decouvertes de R. Khalifa, G. Grabovoi, et la tradition hermetico-islamique", align="C")

    # ═══════════════════ SAVE ═══════════════════
    output = PDF_OUTPUTS["radionique_sacree"]
    pdf.output(str(output))
    print(f"Fiche Radionique generee : {output}")
    print("Page 1: Schema de montage  |  Page 2: Theorie + Protocole")


if __name__ == "__main__":
    draw_radionique()
