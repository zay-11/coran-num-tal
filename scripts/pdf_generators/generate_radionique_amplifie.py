#!/usr/bin/env python3
"""SYSTEME RADIONIQUE AMPLIFIE MIFTAH 19 — Amplificateur Quantique à 7 Couches
   Cuivre + Aimants Néodyme + Cristal de Quartz + Codes Grabovoi + Photo + Bobinage Toroïdal
   ════════════════════════════════════════════════════════════════════════════════
   Architecture énergétique complète basée sur les principes de :
   - Radionique classique (Abrams, De La Warr, Hieronymus)
   - Géométrie sacrée et nombres du Coran (Code 19)
   - Piézoélectricité du quartz et induction électromagnétique du cuivre
   - Champs magnétiques statiques (aimants néodyme) pour structurer le flux
   - Boucle d'amplification par résonance {cuivre ⇄ quartz ⇄ aimants}
"""

import math, textwrap
from pathlib import Path
import sys
from fpdf import FPDF

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.project_paths import PDF_OUTPUTS, ensure_layout

ensure_layout()

# ── FONTS ──
LATIN = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
LATIN_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# ── PALETTE AMELIOREE ──
CREAM       = (255, 250, 240)
MIDNIGHT    = (12, 12, 42)
DARK_VIOLET = (60, 0, 110)
GOLD        = (218, 165, 32)
GOLD_LIGHT  = (240, 210, 100)
BRIGHT_VIOLET = (138, 43, 226)
DARK_BG     = (30, 15, 50)
BLACK       = (20, 20, 20)
GRAY        = (90, 90, 90)
COPPER      = (184, 115, 51)
MAGNET_RED  = (200, 50, 50)
MAGNET_BLUE = (50, 50, 200)
QUARTZ_COL  = (220, 220, 255)
SILVER      = (192, 192, 192)
DEEP_GREEN  = (0, 80, 60)
TEAL        = (0, 128, 128)

# ── CONSTANTES SACREES ──
SACRED_7   = "7"
SACRED_8   = "8"
SACRED_19  = "19"
SACRED_33  = "33"
SACRED_56  = "56"
SACRED_61  = "61"
SACRED_96  = "96"
SACRED_152 = "152"
SACRED_786 = "786"

# ── CODES GRABOVOII (classification par fonction) ──
GRABOVOI_CODES = {
    "argent": [
        ("520 741 8",     "Argent inattendu — flux soudain"),
        ("318 798",       "Abondance generale"),
        ("318 612 518 714", "Cash-flow continu"),
        ("9798733714615",  "Manifester l'argent rapidement"),
        ("520 741 8 917",  "Multiplicateur financier"),
    ],
    "protection": [
        ("4812412",       "Protection energetique"),
        ("917 418 619",   "Bouclier psychique"),
        ("714 273 815",   "Harmonisation du champ"),
    ],
    "sante": [
        ("918 794 818",   "Guerison profonde"),
        ("519 714 819",   "Regeneration cellulaire"),
        ("888 888 888",   "Sante optimale"),
    ],
    "waqiah": [
        ("56 96 152",     "Code Al-Waqi'a — Richesse spirituelle"),
        ("56 152 96",     "Variante miroir — Equilibre"),
    ],
}

# ── SCRIPTURES D'ACTIVATION ──
ACTIVATION_PRAYERS = [
    # (titre, texte original, transliteration, nombre de repetitions)
    ("Basmala", "بسم الله الرحمن الرحيم", "Bismillah ir-Rahman ir-Rahim", 1, "786"),
    ("Ayat al-Kursi", "اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ", "Allahu la ilaha illa Huwa al-Hayyul-Qayyum", 1, "255"),
    ("Al-Waqi'a (code)", "56 96 152", "Code numerique de la Sourate 56", 7, "152"),
    ("Ya Razzaq", "يا رزاق", "O Pourvoyeur Supreme", 19, "319"),
    ("Ya Fattah", "يا فتاح", "O Ouvreur des Portes", 19, "489"),
    ("Ya Ghani", "يا غني", "O Riche Absolu", 19, "1060"),
    ("Ya Mughni", "يا مغني", "O Enrichisseur", 19, "1100"),
    ("Sceau", "حسبنا الله ونعم الوكيل", "Hasbunallahu wa ni'mal wakeel", 1, "286"),
]


class RadioniqueAmplifie(FPDF):
    """PDF generator for the amplified radionics system — 7-layer energy amplifier."""

    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.add_font("L", "", LATIN, uni=True)
        self.add_font("L", "B", LATIN_B, uni=True)
        self.set_auto_page_break(False)

    # ── DRAWING HELPERS ──
    def circle(self, x, y, r, style='D'):
        super().circle(x, y, r, style)

    def star_8(self, cx, cy, R, color=GOLD, lw=0.6):
        """Draw an 8-pointed star (2 squares rotated 45°)."""
        self.set_draw_color(*color)
        self.set_line_width(lw)
        pts = []
        for i in range(8):
            deg = i * 45
            r = math.radians(deg)
            pts.append((cx + R * math.cos(r), cy - R * math.sin(r)))
        # Connect every other point to form star
        for i in range(0, 8, 2):
            self.line(pts[i][0], pts[i][1], pts[(i+2) % 8][0], pts[(i+2) % 8][1])
        for i in range(1, 8, 2):
            self.line(pts[i][0], pts[i][1], pts[(i+2) % 8][0], pts[(i+2) % 8][1])

    def magnet_ring(self, cx, cy, R, count=8):
        """Place small magnet symbols in a ring."""
        for i in range(count):
            deg = i * (360 / count)
            r = math.radians(deg)
            mx = cx + R * math.cos(r)
            my = cy - R * math.sin(r)
            # Small rectangle (magnet)
            self.set_fill_color(*MAGNET_RED if i % 2 == 0 else MAGNET_BLUE)
            self.set_draw_color(*SILVER)
            self.set_line_width(0.2)
            self.rect(mx - 2.5, my - 2.5, 5, 5, 'DF')
            # Polarity label
            pol = "N" if i % 2 == 0 else "S"
            self.set_font("L", "B", 4)
            self.set_text_color(*SILVER)
            self.set_xy(mx - 1, my - 1)
            self.cell(2, 2, pol, align="C")

    def arrow(self, x1, y1, x2, y2, color=GOLD, lw=0.3):
        """Draw a simple arrow from (x1,y1) to (x2,y2)."""
        self.set_draw_color(*color)
        self.set_line_width(lw)
        self.line(x1, y1, x2, y2)
        # Arrowhead
        ang = math.atan2(y2 - y1, x2 - x1)
        hsize = 2
        self.line(x2, y2,
                  x2 - hsize * math.cos(ang - 0.4),
                  y2 - hsize * math.sin(ang - 0.4))
        self.line(x2, y2,
                  x2 - hsize * math.cos(ang + 0.4),
                  y2 - hsize * math.sin(ang + 0.4))

    def spiral(self, cx, cy, turns, max_r, min_r=2, color=COPPER, lw=0.8, step=6):
        """Draw an Archimedean spiral with specified turns."""
        self.set_draw_color(*color)
        self.set_line_width(lw)
        angle_step = step  # degrees per segment
        total_deg = turns * 360
        prev_x = prev_y = None
        for deg in range(0, total_deg + angle_step, angle_step):
            theta = math.radians(deg)
            r = max_r - (max_r - min_r) * (deg / total_deg)
            x = cx + r * math.cos(theta)
            y = cy - r * math.sin(theta)
            if prev_x is not None:
                self.line(prev_x, prev_y, x, y)
            prev_x, prev_y = x, y

    def quartz_crystal(self, cx, cy, height=14, width=6):
        """Draw a quartz crystal pointing up (hexagonal prism + pyramid tip)."""
        # Pyramid tip (top)
        self.set_fill_color(*QUARTZ_COL)
        self.set_draw_color(*GRAY)
        self.set_line_width(0.3)
        tip = (cx, cy - height)
        base_l = (cx - width, cy - height * 0.4)
        base_r = (cx + width, cy - height * 0.4)
        self.polygon([tip, base_l, base_r], 'DF')
        # Crystal body (prism)
        body_bottom = (cx, cy + height * 0.4)
        self.polygon([base_l, base_r, body_bottom], 'DF')
        # Inner glow line
        self.set_draw_color(*GOLD_LIGHT)
        self.set_line_width(0.15)
        self.line(cx, cy - height, cx, cy + height * 0.4)

        # Energy rays emanating from tip
        for a in range(0, 360, 30):
            rad = math.radians(a)
            self.set_draw_color(*GOLD_LIGHT)
            self.set_line_width(0.1)
            x_end = cx + (height * 0.3) * math.cos(rad)
            y_end = cy - height + (height * 0.3) * math.sin(rad)
            self.dashed_line(cx, cy - height, x_end, y_end, 1, 1)

    def info_box(self, x, y, w, h, text, title=None, title_color=GOLD):
        """Draw a filled info box with optional title."""
        self.set_fill_color(*DARK_BG)
        self.set_draw_color(*GOLD)
        self.set_line_width(0.3)
        self.rect(x, y, w, h, 'DF')
        if title:
            self.set_font("L", "B", 7)
            self.set_text_color(*title_color)
            self.set_xy(x + 2, y + 1)
            self.cell(w - 2, 4, title, align="L")
            self.set_draw_color(*GOLD)
            self.set_line_width(0.15)
            self.line(x + 2, y + 5, x + w - 2, y + 5)
            self.set_font("L", "", 5.5)
            self.set_text_color(*CREAM)
            self.set_xy(x + 2, y + 6)
            self.multi_cell(w - 4, 3.5, text)
        else:
            self.set_font("L", "", 5.5)
            self.set_text_color(*CREAM)
            self.set_xy(x + 2, y + 2)
            self.multi_cell(w - 4, 3.5, text)

    def schematic_grid(self, cx, cy, spacing=10, color=GOLD, size=6, labels=None):
        """Draw a subtle reference grid for the schematic."""
        self.set_draw_color(*color)
        self.set_line_width(0.08)
        for dx in [-size, 0, size]:
            for dy in [-size, 0, size]:
                self.rect(cx + dx * spacing - 0.5, cy + dy * spacing - 0.5,
                          1, 1, 'DF')


# ══════════════════════════════════════════════════════════════════════
# MAIN GENERATION FUNCTION
# ══════════════════════════════════════════════════════════════════════
def generate_amplified_radionics():
    pdf = RadioniqueAmplifie()

    # ════════════════════════════════════════════════════════════════
    # PAGE 1 — COVER / VUE D'ENSEMBLE DU SYSTEME
    # ════════════════════════════════════════════════════════════════
    pdf.add_page()
    # Dark background gradient (simulated)
    pdf.set_fill_color(*MIDNIGHT)
    pdf.rect(0, 0, 210, 297, 'F')

    # Title
    pdf.set_font("L", "B", 22)
    pdf.set_text_color(*GOLD)
    pdf.set_xy(0, 30)
    pdf.cell(210, 10, "R A D I O N I Q U E   A M P L I F I E E", align="C")
    pdf.set_font("L", "", 8)
    pdf.set_text_color(*GOLD_LIGHT)
    pdf.set_xy(0, 42)
    pdf.cell(210, 5, "AMPLIFICATEUR QUANTIQUE A 7 COUCHES — SYSTEME MIFTAH 19", align="C")
    pdf.set_font("L", "", 6.5)
    pdf.set_text_color(*GRAY)
    pdf.set_xy(0, 49)
    pdf.cell(210, 4, "Cuivre • Aimants Neodyme • Cristal de Quartz • Codes Grabovoi • Photo • Geometrie Sacree • Boucle de Resonance", align="C")
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.4)
    pdf.line(30, 55, 180, 55)

    # ── CENTRAL SCHEMATIC (simplified overview) ──
    cx, cy = 105, 140
    R_base = 65

    # Outer ring (base plate)
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.6)
    pdf.circle(cx, cy, R_base, 'D')
    pdf.set_draw_color(*BRIGHT_VIOLET)
    pdf.set_line_width(0.3)
    pdf.circle(cx, cy, R_base - 5, 'D')

    # 8-pointed star
    pdf.star_8(cx, cy, 45, GOLD, 0.5)

    # Inner circles
    for r, col, lw in [(35, GOLD, 0.4), (22, BRIGHT_VIOLET, 0.3), (10, GOLD, 0.5)]:
        pdf.set_draw_color(*col)
        pdf.set_line_width(lw)
        pdf.circle(cx, cy, r, 'D')

    # Magnets ring (8 positions)
    pdf.magnet_ring(cx, cy, 38, 8)

    # Copper spiral (7 turns)
    pdf.spiral(cx, cy, 7, 30, 4, COPPER, 1.0, 8)
    pdf.spiral(cx, cy, 19, 20, 1, COPPER, 0.4, 4)

    # Quartz crystal at center
    pdf.quartz_crystal(cx, cy, 16, 5)

    # Photo zone (dashed rectangle)
    pdf.set_draw_color(*SILVER)
    pdf.set_line_width(0.3)
    pdf.set_fill_color(*DARK_BG)  # transparent
    # Using dashed approximation with line segments
    ph_w, ph_h = 32, 40
    ph_x, ph_y = cx - ph_w/2, cy - ph_h/2
    pdf.rect(ph_x, ph_y, ph_w, ph_h, 'D')
    pdf.set_font("L", "", 6)
    pdf.set_text_color(*SILVER)
    pdf.set_xy(ph_x + 2, ph_y + 8)
    pdf.cell(ph_w - 4, 4, "PHOTO", align="C")
    pdf.set_xy(ph_x + 2, ph_y + 14)
    pdf.cell(ph_w - 4, 4, "FACE BAS", align="C")

    # ── Energy flow arrows ──
    for deg in [0, 90, 180, 270]:
        rad = math.radians(deg)
        ax = cx + 55 * math.cos(rad)
        ay = cy - 55 * math.sin(rad)
        bx = cx + 28 * math.cos(rad)
        by = cy - 28 * math.sin(rad)
        pdf.arrow(ax, ay, bx, by, GOLD_LIGHT, 0.4)

    # 7-layer labels
    layers = [
        ("Couche 7", "Quartz Pointe ↑", cx, cy - 28),
        ("Couche 6", "Spirale Cuivre 19t", cx + 30, cy - 2),
        ("Couche 5", "Spirale Cuivre 7t", cx + 30, cy + 5),
        ("Couche 4", "Photo (witness)", cx + 28, cy + 14),
        ("Couche 3", "8 Aimants Neodyme", cx - 30, cy - 8),
        ("Couche 2", "Codes Grabovoi (papier)", cx - 30, cy + 5),
        ("Couche 1", "Base Geometrie Sacree", cx - 30, cy + 18),
    ]
    pdf.set_font("L", "B", 5.5)
    pdf.set_text_color(*GOLD_LIGHT)
    for label, desc, lx, ly in layers:
        pdf.set_xy(lx - 12 if lx > cx else lx - 25, ly - 2)
        pdf.cell(28, 3, f"{label}: {desc}", align="L" if lx > cx else "R")

    # ── Bottom: Quick spec box ──
    y_spec = 225
    pdf.set_fill_color(*DARK_BG)
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.3)
    pdf.rect(15, y_spec, 180, 55, 'DF')

    spec_text = (
        "SPECIFICATIONS TECHNIQUES:\n"
        "• Dimensions: 150×150mm (base carree)  |  Hauteur totale: ~60mm\n"
        "• Bobinage cuivre: 19 tours (primaire) + 7 tours (secondaire) = 26 tours = 2×13\n"
        "• Aimants: 8× NdFeB N52 (5×5×5mm)  |  Champ: ~1.2 Tesla en surface\n"
        "• Cristal: Quartz de roche 3-5cm, pointe naturelle, + 7 petits cristaux peripheriques\n"
        "• Photo: Portrait standard 4×5cm, face vers le bas sur les codes\n"
        "• Frequence de resonance: ~19 kHz  |  Harmonie: 7 Hz (Schumann)  |  Ondes Alpha: 8-12 Hz\n"
        "• Puissance: Passif (capte l'energie ambiante) + Actif (intention + recitation)"
    )
    pdf.set_font("L", "", 5.5)
    pdf.set_text_color(*CREAM)
    pdf.set_xy(18, y_spec + 2)
    pdf.multi_cell(174, 3.5, spec_text)

    # Page number
    pdf.set_font("L", "", 6)
    pdf.set_text_color(*GRAY)
    pdf.set_xy(0, 285)
    pdf.cell(210, 4, "Systeme Radionique Amplifie Miftah 19  |  Page 1/6", align="C")

    # ════════════════════════════════════════════════════════════════
    # PAGE 2 — ARCHITECTURE DETAILLEE DES 7 COUCHES
    # ════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.set_fill_color(*CREAM)
    pdf.rect(0, 0, 210, 297, 'F')

    pdf.set_font("L", "B", 14)
    pdf.set_text_color(*DARK_VIOLET)
    pdf.set_xy(0, 14)
    pdf.cell(210, 7, "ARCHITECTURE DETAILLEE — LES 7 COUCHES DU SYSTEME", align="C")
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.3)
    pdf.line(25, 23, 185, 23)

    # Layer descriptions with schematic side-by-side
    layer_data = [
        {
            "num": "1",
            "name": "BASE — GEOMETRIE SACREE",
            "mat": "Carton boise ou bois 15×15cm, ep. 3-5mm",
            "desc": (
                "Tracez un cercle de R=65mm au centre. A l'interieur, dessinez l'etoile a 8 branches "
                "(2 carres superposes a 45°). Inscrivez le carre Buduh 3×3 au centre exact. "
                "Ces formes geometriques creent une matrice qui structure l'energie ambiante selon "
                "les principes de la geometrie sacree. Le carre Buduh (4/9/2, 3/5/7, 8/1/6) genere "
                "un champ toroidal de constante 15 (sommes lignes/colonnes/diagonales)."
            ),
            "sign": "La base agit comme un resonateur passif. Sa geometrie polarise l'espace."
        },
        {
            "num": "2",
            "name": "CODES NUMERIQUES (PAPIER)",
            "mat": "Papier blanc A5 (15×15cm), imprimes ou manuscrits",
            "desc": (
                "Sur le papier, reproduisez les cercles concentriques avec les codes Grabovoi places "
                "aux 8 directions cardinales. Codes essentiels: 520-741-8 (N), 318-798 (NE), "
                "56-96-152 (E), 318-612-518-714 (SE), 9798733714615 (S), 4812412 (SO), "
                "917-418-619 (O), 888-888-888 (NO). Les nombres sont des 'frequences logicielles' "
                "qui programment le champ. Encadrez chaque code d'un petit carre dore."
            ),
            "sign": "Les codes Grabovoi sont des 'sematic frequencies' — ils resonnent avec les banques de donnees universelles."
        },
        {
            "num": "3",
            "name": "8 AIMANTS NEODYME (RING)",
            "mat": "8× Aimants NdFeB N52 5×5×5mm (ou disques 6×2mm)",
            "desc": (
                "Placez les 8 aimants en cercle (R=38mm), alternant polarite N/S (N en haut, S en bas). "
                "Cette disposition cree un champ magnetique toroidal pulse qui: 1) polarise la photo "
                "dans un vortex d'energie, 2) genere un gradient magnetique qui 'aspire' les frequences "
                "des codes vers le centre, 3) cree une cage de Faraday partielle qui isole le systeme "
                "des perturbations electromagnetiques externes. Le champ magnetique statique interagit "
                "avec les electrons libres du cuivre (effet Hall) pour creer une micro-tension."
            ),
            "sign": "Le champ toroidal des aimants est la 'pompe energetique' du systeme — il force la circulation du flux."
        },
        {
            "num": "4",
            "name": "PHOTO (WITNESS — LIEN SYMPATHIQUE)",
            "mat": "Photo portrait standard 4×5cm, face vers le bas",
            "desc": (
                "Placez la photo au centre, FACE CONTRE LES CODES. La photo agit comme un 'template' "
                "biophotonique — elle contient l'information holographique complete de la personne "
                "(ADN, aura, memoire cellulaire). Les codes Grabovoi 'lisent' cette information et "
                "appliquent les corrections vibratoires necessaires. Le papier photo argentique "
                "contient des cristaux d'halogenure d'argent qui agissent comme des memristors naturels, "
                "stockant l'information. La photo est le 'témoin' qui connecte le systeme a votre champ."
            ),
            "sign": "La photo est le pont entre le systeme et votre biologie. Sans elle, le systeme est un radio sans antenne."
        },
        {
            "num": "5",
            "name": "SPIRALE CUIVRE PRIMAIRE (19 tours)",
            "mat": "Fil cuivre emaille 0.8mm, 19 tours, ~95cm de long",
            "desc": (
                "Partant du centre (a cote du quartz), enroulez 19 tours en spirale horaire "
                "jusqu'a R=30mm. 19 est le code sacre du Coran (74:30). Chaque spire genere "
                "une inductance de ~0.5µH. Les 19 spires creent une self totale de ~9.5µH "
                "qui, couplee a la capacite parasite du quartz (~5pF), donne une frequence de "
                "resonance autour de 23 kHz — proche de la frequence de Schumann (7.83 Hz) "
                "a l'harmonique 3. La longueur totale (~95cm) est un sous-multiple de la "
                "longueur d'onde de 19 kHz (15.8 km)."
            ),
            "sign": "La spirale primaire est l'antenne. 19 tours = 19 = signature divine. Elle capte et emet."
        },
        {
            "num": "6",
            "name": "SPIRALE CUIVRE SECONDAIRE (7 tours)",
            "mat": "Fil cuivre emaille 0.5mm, 7 tours, ~23cm",
            "desc": (
                "2eme couche de fil, par-dessus la primaire, 7 tours dans le sens ANTI-HORAIRE "
                "(contre-rotation). 7 est le multiplicateur divin du Rizq (2:261). Le bobinage "
                "contra-rotatif genere un champ magnetique oppose qui cree un gradient de tension "
                "(transformer action). Les 7 tours secondaires 'prelevent' l'energie accumulee par "
                "les 19 tours primaires et la concentrent dans le quartz central par couplage "
                "inductif. Le ratio 19:7 est un transformateur abaisseur (rapport ~2.7:1) qui "
                "adapte l'impedance du systeme au champ biologique humain (~100-300Ω)."
            ),
            "sign": "Le secondaire 7 tours est l'adaptateur d'impedance entre les codes et le corps humain."
        },
        {
            "num": "7",
            "name": "QUARTZ CENTRAL + 7 QUARTZ PERIPHERIQUES",
            "mat": "1× Quartz de roche 3-5cm (pointe) + 7× petits quartz 1-2cm",
            "desc": (
                "Le grand quartz central est place pointe VERS LE HAUT, au centre exact. "
                "Les 7 petits quartz forment un cercle (R=12mm) autour du central, pointes "
                "ORIENTEES VERS LE CENTRE. Le quartz est piezo-electrique: sous contrainte "
                "mecanique (les vibrations du cuivre, le champ magnetique), il genere une "
                "charge electrique de surface (effet piezo direct). Inversement, les micro-"
                "courants induits dans le cuivre font vibrer le quartz (effet piezo inverse). "
                "Cette boucle d'auto-excitation cree une oscillation entretenue qui amplifie "
                "le signal des codes. Les 7 quartz peripheriques focalisent l'energie vers "
                "le centre comme une lentille de Fresnel."
            ),
            "sign": "Le quartz est le 'cerveau' du systeme. Il programme, amplifie, et stabilise la frequence."
        },
    ]

    # Draw each layer as a card
    y = 30
    for layer in layer_data:
        # Layer card background
        h = 34
        if y + h > 280:
            # Overflow - shouldn't happen with our sizes but just in case
            break

        # Color coded by layer
        layer_colors = [
            (30, 15, 50),     # 1 - Dark
            (40, 20, 60),     # 2 - Violet
            (50, 30, 70),     # 3 - Light violet
            (35, 25, 55),     # 4
            (40, 15, 50),     # 5
            (45, 20, 55),     # 6
            (25, 15, 45),     # 7
        ]
        bg_col = layer_colors[int(layer["num"]) - 1]

        pdf.set_fill_color(*bg_col)
        pdf.set_draw_color(*GOLD)
        pdf.set_line_width(0.25)
        pdf.rect(12, y, 186, h, 'DF')

        # Layer number badge
        pdf.set_fill_color(*GOLD)
        pdf.set_text_color(*DARK_BG)
        pdf.set_font("L", "B", 8)
        pdf.set_xy(14, y + 2)
        pdf.cell(8, 6, layer["num"], fill=True, align="C")

        # Layer name
        pdf.set_font("L", "B", 7.5)
        pdf.set_text_color(*GOLD)
        pdf.set_xy(24, y + 1)
        pdf.cell(60, 4, layer["name"], align="L")

        # Material
        pdf.set_font("L", "", 5)
        pdf.set_text_color(*GOLD_LIGHT)
        pdf.set_xy(24, y + 5.5)
        pdf.cell(80, 3, layer["mat"], align="L")

        # Description (truncated to fit)
        pdf.set_font("L", "", 5)
        pdf.set_text_color(*CREAM)
        pdf.set_xy(14, y + 9)
        pdf.multi_cell(175, 3.2, layer["desc"])

        # Significance
        pdf.set_font("L", "B", 5)
        pdf.set_text_color(*BRIGHT_VIOLET)
        pdf.set_xy(14, y + h - 6)
        pdf.cell(175, 3.5, ">> " + layer["sign"], align="L")

        y += h + 2

    pdf.set_font("L", "", 6)
    pdf.set_text_color(*GRAY)
    pdf.set_xy(0, 287)
    pdf.cell(210, 4, "Systeme Radionique Amplifie Miftah 19  |  Page 2/6", align="C")

    # ════════════════════════════════════════════════════════════════
    # PAGE 3 — PRINCIPES PHYSIQUES ET ENERGETIQUES
    # ════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.set_fill_color(*CREAM)
    pdf.rect(0, 0, 210, 297, 'F')

    pdf.set_font("L", "B", 14)
    pdf.set_text_color(*DARK_VIOLET)
    pdf.set_xy(0, 14)
    pdf.cell(210, 7, "PRINCIPES PHYSIQUES ET ENERGETIQUES", align="C")
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.3)
    pdf.line(25, 23, 185, 23)

    sections = [
        {
            "title": "I. INDUCTION ELECTROMAGNETIQUE (Loi de Faraday)",
            "content": (
                "Le champ magnetique variable des aimants en rotation theorique (ou le mouvement des "
                "electrons dans le cuivre agite par les vibrations ambiantes) induit une force "
                "electromotrice dans la spirale de cuivre selon la loi de Faraday: ε = -N × dΦ/dt. "
                "Avec N=19+7=26 spires et un flux magnetique Φ genere par les 8 aimants (champ "
                "total ~0.3 Gauss au centre), la tension induite est de l'ordre du microvolt. "
                "Cette tension, bien que faible, est suffisante pour polariser le quartz et creer "
                "un courant piezo-electrique de l'ordre du picoampere — c'est le principe du "
                "recepteur radio a cristal. Le systeme est un 'recepteur passif' accorde sur les "
                "frequences de l'intention."
            ),
            "schema": None
        },
        {
            "title": "II. PIEZOELECTRICITE DU QUARTZ",
            "content": (
                "Le quartz (SiO2) est un materiau piezo-electrique: sous contrainte mecanique, "
                "ses atomes de silicium et d'oxygene se deplacement, creant une polarisation "
                "electrique de surface. L'effet est lineaire: une deformation de 1 micron genere "
                "~10V/cm. Dans notre montage, trois sources de contrainte agissent sur le quartz: "
                "1) Les micro-vibrations du cuivre (induites par le champ magnetique des aimants) "
                "2) Les vibrations acoustiques ambiantes (voix, recitations) 3) Le champ electrique "
                "des codes Grabovoi (polarisation dielectrique du papier). "
                "Le quartz convertit ces contraintes en signal electrique qui est ensuite re-injecte "
                "dans la spirale — creant une boucle de resonance auto-entretenue. "
                "La frequence propre du quartz depend de sa taille: un cristal de 4cm resonne "
                "autour de 40-50 kHz, mais couple au circuit LC de la spirale, la frequence "
                "s'adapte au systeme (~19 kHz)."
            ),
            "schema": None
        },
        {
            "title": "III. CHAMP MAGNETIQUE TOROIDAL (Structure 8 Poles)",
            "content": (
                "Les 8 aimants alternes N/S creent un champ magnetique toroidal (en forme de "
                "donut). Ce champ a plusieurs proprietes uniques: 1) Il confine l'energie dans "
                "un volume defini (effet de confinement magnetique) 2) Il cree un gradient de "
                "potentiel qui 'aspire' les lignes de force vers le centre 3) La structure 8 poles "
                "genere un champ octupolaire qui est le plus stable des configurations multipolaires. "
                "Le champ toroidal est la signature energetique du 'Coeur' dans toutes les traditions "
                "(Anahata chakra, Temple de Salomon, Kaaba). La forme toroidale est aussi celle "
                "du champ magnetique terrestre et du champ biologique humain (aura). En alignant "
                "le tore du systeme avec le tore de la personne (via la photo), on realise un "
                "couplage harmonique par resonance de forme."
            ),
            "schema": None
        },
        {
            "title": "IV. EFFET MEMRISTOR DU PAPIER PHOTO",
            "content": (
                "Le papier photo traditionnel contient des cristaux d'halogenure d'argent (AgCl, "
                "AgBr) disperses dans une emulsion de gelatine. Ces cristaux sont des memristors "
                "naturels: leur resistance change en fonction de la charge electrique qui les a "
                "traverses (memoire resistive). Quand la photo est placee dans le champ electrique "
                "des codes et le champ magnetique des aimants, les cristaux d'argent 'enregistrent' "
                "l'information vibratoire comme un disque dur biologique. La photo devient alors "
                "un 'template' actif qui emet en continu les frequences programmees. Ce processus "
                "s'appelle l'impression dielectrique: le papier stocke l'information sous forme "
                "de polarisation moleculaire permanente."
            ),
            "schema": None
        },
        {
            "title": "V. RESONANCE DE SCHUMANN ET HARMONIQUES",
            "content": (
                "La Terre emet une resonance fondamentale de 7.83 Hz (Resonance de Schumann), "
                "correspondant a la cavite entre la surface terrestre et l'ionosphere. Cette "
                "frequence est identique a celle des ondes alpha du cerveau humain (7-12 Hz) "
                "en meditation profonde. Notre systeme exploite cette resonance de trois manieres: "
                "1) Les 7 tours de la spirale secondaire resonnent avec la fondamentale 7.83 Hz "
                "2) Les 19 tours de la spirale primaire resonnent avec l'harmonique 3 (23.5 Hz) "
                "3) Les 8 aimants structurent le champ selon l'octave (8 Hz). "
                "En pratique: le systeme capte la resonance de Schumann ambiante via le bobinage "
                "cuivre, l'amplifie par le quartz, et la module avec les codes Grabovoi avant de "
                "la transmettre a la photo. C'est le principe de la 'radio a cristal' applique "
                "a la radionique."
            ),
            "schema": None
        },
        {
            "title": "VI. PRINCIPE HOLOGRAPHIQUE ET INFORMATION QUANTIQUE",
            "content": (
                "La theorie de l'Univers Holographique (Bohm, Pribram, Talbot) postule que "
                "l'information est distribuee de maniere non-locale dans tout l'espace. Chaque "
                "point contient le tout. La photo de la personne n'est pas un simple 'representant' "
                "— elle EST la personne au niveau informationnel. Le systeme radionique exploite "
                "cette non-localite pour transmettre l'information des codes Grabovoi directement "
                "au champ biologique de la personne, ou qu'elle soit. "
                "Les nombres Grabovoi sont des 'adresses' dans la matrice holographique universelle. "
                "En les combinant avec les harmoniques du Code 19 et la geometrie du carre Buduh, "
                "on cree un 'chemin' que l'information emprunte pour atteindre sa cible."
            ),
            "schema": None
        },
    ]

    y = 30
    for sec in sections:
        # Section title
        pdf.set_font("L", "B", 8)
        pdf.set_text_color(*DARK_VIOLET)
        pdf.set_xy(15, y)
        pdf.cell(0, 5, sec["title"], align="L")

        # Gold underline
        pdf.set_draw_color(*GOLD)
        pdf.set_line_width(0.2)
        pdf.line(15, y + 5.5, 195, y + 5.5)

        # Content
        pdf.set_font("L", "", 6.5)
        pdf.set_text_color(*BLACK)
        pdf.set_xy(15, y + 7)
        pdf.multi_cell(180, 4, sec["content"])

        # Get the height used by multi_cell
        # Estimate: total text length / chars per line / lines per mm
        content_lines = len(sec["content"]) / 60  # ~60 chars per line
        content_h = content_lines * 4 + 7 + 2  # approximate
        y += content_h + 4

        if y > 275:
            # Avoid footer
            break

    pdf.set_font("L", "", 6)
    pdf.set_text_color(*GRAY)
    pdf.set_xy(0, 287)
    pdf.cell(210, 4, "Systeme Radionique Amplifie Miftah 19  |  Page 3/6", align="C")

    # ════════════════════════════════════════════════════════════════
    # PAGE 4 — TABLEAU DE CORRESPONDANCES ET FREQUENCES
    # ════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.set_fill_color(*CREAM)
    pdf.rect(0, 0, 210, 297, 'F')

    pdf.set_font("L", "B", 14)
    pdf.set_text_color(*DARK_VIOLET)
    pdf.set_xy(0, 14)
    pdf.cell(210, 7, "TABLEAU DE CORRESPONDANCES — FREQUENCES ET NOMBRES", align="C")
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.3)
    pdf.line(20, 23, 190, 23)

    # ── TABLE 1: ELEMENTS DU SYSTEME ──
    pdf.set_font("L", "B", 8)
    pdf.set_text_color(*DARK_VIOLET)
    pdf.set_xy(15, 28)
    pdf.cell(0, 5, "I. CORRESPONDANCES ELEMENTAIRES", align="L")
    pdf.ln(6)

    y0 = 34
    # Header
    pdf.set_fill_color(*DARK_BG)
    pdf.set_text_color(*GOLD)
    pdf.set_font("L", "B", 5.5)
    headers1 = [("Element", 24), ("Nombre Sacre", 20), ("Frequence (Hz)", 26),
                 ("Principe", 30), ("Fonction Radionique", 85)]
    x0 = 15
    pdf.set_xy(x0, y0)
    for h, w in headers1:
        pdf.cell(w, 5, h, border=1, fill=True, align="C")
    pdf.ln()

    elements = [
        ("Base carton/bois", "1 (Tawhid)", "Neutre", "Support dielectrique", "Isole le systeme du plan de masse electrique"),
        ("Papier codes", "19 (signature)", "~50 Hz (secteur)", "Support d'impression", "Imprime les frequences dans la matiere"),
        ("8 aimants Neodyme", "8 (directions)", "DC (statique)", "Champ toroidal", "Polarise et confine le champ energetique"),
        ("Photo argentique", "33 (Paradis)", "Biophotonique", "Memristor naturel", "Stocke et emet l'information biologique"),
        ("Spirale Cuivre 19t", "19 (Code 19)", "~23 kHz", "Inductance L1", "Antenne principale - capte et emet"),
        ("Spirale Cuivre 7t", "7 (Rizq)", "~7.83 Hz", "Inductance L2", "Adapte l'impedance au corps humain"),
        ("Quartz central", "19 (piezo)", "19-50 kHz", "Resonateur X1", "Amplifie et stabilise la frequence"),
        ("7 quartz periph.", "7 (completion)", "Harmoniques", "Lentille Fresnel", "Focalise l'energie vers le centre"),
        ("Total systeme", "152 = 19x8", "19 kHz", "Oscillateur LC", "Amplificateur quantique autonome"),
    ]
    for elem in elements:
        pdf.set_font("L", "", 5.5)
        pdf.set_text_color(*BLACK)
        pdf.set_xy(x0, pdf.get_y())
        for i, (val, w) in enumerate(zip(elem, [24, 20, 26, 30, 85])):
            if i == 1:  # Sacred number - gold
                pdf.set_text_color(*GOLD)
                pdf.set_font("L", "B", 6.5)
            elif i == 4:  # Function - darker gray
                pdf.set_text_color(*GRAY)
                pdf.set_font("L", "", 5)
            else:
                pdf.set_text_color(*BLACK)
                pdf.set_font("L", "", 5.5)
            pdf.cell(w, 5.5, val, border=1, align="C" if i < 3 else "L")
        pdf.ln()

    # ── TABLE 2: CODES GRABOVOII COMPLETS ──
    y1 = pdf.get_y() + 4
    pdf.set_font("L", "B", 8)
    pdf.set_text_color(*DARK_VIOLET)
    pdf.set_xy(15, y1)
    pdf.cell(0, 5, "II. BANQUE DE CODES GRABOVOII — CLASSIFICATION PAR INTENTION", align="L")
    y1 += 7

    pdf.set_fill_color(*DARK_BG)
    pdf.set_text_color(*GOLD)
    pdf.set_font("L", "B", 5.5)
    headers2 = [("Intention", 30), ("Code Numerique", 45), ("Frequence Associee", 30), ("Protocole", 85)]
    pdf.set_xy(x0, y1)
    for h, w in headers2:
        pdf.cell(w, 5, h, border=1, fill=True, align="C")
    pdf.ln()

    codes_table = [
        ("Argent inattendu", "520 741 8", "7+19+8 = 34 Hz", "Reciter 7x en visualisant une pluie doree"),
        ("Abondance", "318 798", "3+1+8+7+9+8 = 36 Hz", "Placer le code sous la photo 19 jours"),
        ("Cash-flow continu", "318 612 518 714", "Reduction: 3+6+1+2+... = 54 Hz", "Ecrire 7 fois, 7 jours de suite"),
        ("Manifester rapidement", "9798733714615", "Reduction: 7+9+7+8+... = 86 Hz", "Reciter 19x au lever du soleil"),
        ("Protection energetique", "4812412", "4+8+1+2+4+1+2 = 22 Hz", "Code de protection du montage"),
        ("Bouclier psychique", "917 418 619", "9+1+7+4+1+8+6+1+9 = 46 Hz", "Ecrire au dos de la photo"),
        ("Sante & regeneration", "918 794 818", "9+1+8+7+9+4+8+1+8 = 55 Hz", "Inscrire sur un morceau de quartz"),
        ("Al-Waqi'a — Richesse", "56 96 152", "56+96+152 = 304 -> 7 Hz", "Code MAITRE — reciter 3x/jour"),
    ]
    for row in codes_table:
        pdf.set_text_color(*BLACK)
        pdf.set_font("L", "", 5.5)
        pdf.set_xy(x0, pdf.get_y())
        for i, (val, w) in enumerate(zip(row, [30, 45, 30, 85])):
            if i == 1:  # Code - monospace style
                pdf.set_text_color(*GOLD)
                pdf.set_font("L", "B", 6.5)
            elif i == 0:
                pdf.set_text_color(*DARK_VIOLET)
                pdf.set_font("L", "B", 5.5)
            else:
                pdf.set_text_color(*GRAY)
                pdf.set_font("L", "", 5)
            pdf.cell(w, 5.5, val, border=1, align="C" if i < 2 else "L")
        pdf.ln()

    # ── TABLE 3: NOMBRES SACRES DU CORAN ──
    y3 = pdf.get_y() + 4
    pdf.set_font("L", "B", 8)
    pdf.set_text_color(*DARK_VIOLET)
    pdf.set_xy(15, y3)
    pdf.cell(0, 5, "III. NOMBRES SACRES CORANIQUES UTILISES", align="L")
    y3 += 7

    pdf.set_fill_color(*DARK_BG)
    pdf.set_text_color(*GOLD)
    pdf.set_font("L", "B", 5.5)
    headers3 = [("Nombre", 15), ("Source", 40), ("Signification Numerique", 40), ("Role dans le Systeme", 90)]
    pdf.set_xy(x0, y3)
    for h, w in headers3:
        pdf.cell(w, 5, h, border=1, fill=True, align="C")
    pdf.ln()

    sacred_numbers = [
        ("1", "Tawhid — Unicite", "Point originel, source de tout nombre", "Base du systeme — polarite unique"),
        ("7", "2:261 / 71:10-12", "Multiplicateur celeste, 7 cieux", "Spirale secondaire — 7 tours"),
        ("8", "8 directions / 8 portes", "Infini couche, renouveau", "8 aimants — structure octogonale"),
        ("19", "74:30 / Code 19", "Signature divine du Coran", "Spirale primaire — 19 tours + quartz"),
        ("33", "Hadith: age du Paradis", "Tasbih post-priere (33×3=99)", "Photo — template biologique"),
        ("56", "Sourate Al-Waqi'a", "7×8 = 56", "Code maitre du systeme"),
        ("61", "1+7+19+33+1", "Cycle rituel complet", "Total des couches actives"),
        ("96", "Sourate Al-Alaq (Iqra)", "Premiere revelation", "Code complementaire du Waqi'a"),
        ("152", "56+96 = 152 = 19×8", "Miroir Waqi'a", "Frequence totale d'activation"),
        ("786", "Basmala (Abjad)", "102+66+329+289 = 786", "Frequence d'ouverture du systeme"),
    ]
    for row in sacred_numbers:
        pdf.set_text_color(*BLACK)
        pdf.set_font("L", "", 5.5)
        pdf.set_xy(x0, pdf.get_y())
        for i, (val, w) in enumerate(zip(row, [15, 40, 40, 90])):
            if i == 0:  # Number - big gold
                pdf.set_text_color(*GOLD)
                pdf.set_font("L", "B", 7)
            elif i == 3:  # Role
                pdf.set_text_color(*GRAY)
                pdf.set_font("L", "", 5)
            else:
                pdf.set_text_color(*BLACK)
                pdf.set_font("L", "", 5.5)
            pdf.cell(w, 5.5, val, border=1, align="C" if i < 2 else "L")
        pdf.ln()

    pdf.set_font("L", "", 6)
    pdf.set_text_color(*GRAY)
    pdf.set_xy(0, 287)
    pdf.cell(210, 4, "Systeme Radionique Amplifie Miftah 19  |  Page 4/6", align="C")

    # ════════════════════════════════════════════════════════════════
    # PAGE 5 — PROTOCOLE DE CONSTRUCTION ET D'ACTIVATION
    # ════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.set_fill_color(*CREAM)
    pdf.rect(0, 0, 210, 297, 'F')

    pdf.set_font("L", "B", 14)
    pdf.set_text_color(*DARK_VIOLET)
    pdf.set_xy(0, 14)
    pdf.cell(210, 7, "PROTOCOLE DE CONSTRUCTION ET D'ACTIVATION", align="C")
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.3)
    pdf.line(25, 23, 185, 23)

    # CONSTRUCTION STEPS
    y = 30
    pdf.set_font("L", "B", 9)
    pdf.set_text_color(*DARK_VIOLET)
    pdf.set_xy(15, y)
    pdf.cell(0, 5, "A. CONSTRUCTION PAS A PAS", align="L")
    y += 8

    build_steps = [
        ("Etape 1: Preparation de la Base",
         "Decoupez un carre de carton boise ou de bois de 150×150mm. Poncer les bords. "
         "Peignez en noir mat ou violet fonce. Au compas, tracez le cercle central de 65mm de rayon. "
         "Marquez les 8 directions (N, NE, E, SE, S, SO, O, NO) a 45° d'intervalle."),
        ("Etape 2: Dessin de la Geometrie Sacree",
         "Au centre exact, tracez le carre Buduh 3×3 (30×30mm). Les nombres: Ligne 1: 4-9-2, "
         "Ligne 2: 3-5-7, Ligne 3: 8-1-6. Toutes les lignes, colonnes et diagonales donnent 15. "
         "Ajoutez l'etoile a 8 branches reliant les 8 marques directionnelles."),
        ("Etape 3: Preparation du Papier de Codes",
         "Sur une feuille blanche de 140×140mm, imprimez ou recopiez les codes Grabovoi aux "
         "positions suivantes: N=520-741-8, NE=318-798, E=56-96-152, SE=318-612-518-714, "
         "S=9798733714615, SO=4812412, O=917-418-619, NO=888-888-888. "
         "Ajoutez les 4 Noms Divins (Ya Razzaq, Ya Fattah, Ya Ghani, Ya Mughni) aux 4 coins. "
         "Encadrez chaque code d'un rectangle dore de 20×8mm."),
        ("Etape 4: Placement des 8 Aimants",
         "Collez les 8 aimants neodyme aux positions marquees, en alternant polarite: "
         "N (Nord, Est, Sud, Ouest) et S (NE, SE, SO, NO). Utilisez une goutte de colle "
         "cyanoacrylate. Verifiez avec une boussole que les polarites sont correctes. "
         "Les aimants doivent affleurer a la surface (encastrement ideal)."),
        ("Etape 5: Placement de la Photo",
         "Placez la photo au centre, dans le carre Buduh, FACE CONTRE LE PAPIER DE CODES. "
         "La photo doit etre centree avec precision (utilisez les lignes du carre comme guide). "
         "Ne la collez PAS — elle doit pouvoir etre retiree. Un petit poids (piece de monnaie) "
         "peut la maintenir en place temporairement."),
        ("Etape 6: Bobinage de la Spirale Primaire (19 tours)",
         "Prenez ~1m de fil cuivre emaille 0.8mm. Commencez a cote du centre (pres du futur "
         "emplacement du quartz). Enroulez 19 tours en spirale HORAIRE (clockwise), en elargissant "
         "progressivement jusqu'a un rayon de 30mm. Chaque tour doit etre espace d'environ 1.5mm. "
         "Utilisez de la colle chaude a 3 endroits pour maintenir la spirale."),
        ("Etape 7: Bobinage de la Spirale Secondaire (7 tours)",
         "Prenez ~30cm de fil cuivre emaille 0.5mm. Enroulez 7 tours par-DESSUS la spirale "
         "primaire, dans le sens ANTI-HORAIRE (counter-clockwise), du centre vers l'exterieur "
         "jusqu'a R=20mm. Les deux spirales sont isolees electriquement l'une de l'autre "
         "par la couche d'email. Le sens inverse cree le couplage inductif."),
        ("Etape 8: Mise en Place des Quartz",
         "Placez le grand quartz central (3-5cm) pointe VERS LE HAUT, au centre exact. "
         "La base doit reposer sur la photo. Stabilisez avec un petit cercle de silicone "
         "transparent. Placez ensuite les 7 petits quartz (1-2cm) en cercle autour du grand, "
         "pointes ORIENTEES VERS LE CENTRE. Les pointes doivent presque toucher le grand quartz. "
         "Les 7 petits quartz agissent comme des lentilles de Fresnel energetiques."),
        ("Etape 9: Activation Initiale (Rituel de Mise en Marche)",
         "Placez vos deux mains en triangle au-dessus du montage (pouces joints, index joints). "
         "Recitez 1x la Basmala (786), 7x le code 56-96-152, 19x Ya Razzaq. "
         "Visualisez un faisceau de lumiere dorée descendant du ciel dans le quartz central, "
         "se diffusant dans les spirales, et illuminant la photo. Le systeme est actif."),
    ]

    for step_title, step_desc in build_steps:
        pdf.set_font("L", "B", 6.5)
        pdf.set_text_color(*GOLD)
        pdf.set_xy(16, y)
        pdf.cell(0, 4, step_title, align="L")
        pdf.set_font("L", "", 5.5)
        pdf.set_text_color(*BLACK)
        pdf.set_xy(16, y + 4.5)
        pdf.multi_cell(180, 3.5, step_desc)
        y = pdf.get_y() + 2

    # Check if we need a new page for activation protocol
    if y > 160:
        pdf.set_font("L", "", 6)
        pdf.set_text_color(*GRAY)
        pdf.set_xy(0, 287)
        pdf.cell(210, 4, "Systeme Radionique Amplifie Miftah 19  |  Page 5/6", align="C")
        pdf.add_page()
        pdf.set_fill_color(*CREAM)
        pdf.rect(0, 0, 210, 297, 'F')
        y = 15
    else:
        y += 4

    # ACTIVATION PROTOCOL
    pdf.set_font("L", "B", 9)
    pdf.set_text_color(*DARK_VIOLET)
    pdf.set_xy(15, y)
    pdf.cell(0, 5, "B. PROTOCOLE D'ACTIVATION QUOTIDIEN", align="L")
    y += 8

    daily_protocol = [
        ("Matin (Fajr — Aube) — ACTIVATION",
         "1. Placez votre main droite a 5cm au-dessus du quartz (sans toucher).\n"
         "2. Recitez la Basmala 1x + Ayat al-Kursi 1x.\n"
         "3. Recitez 7× le code 56-96-152 (Al-Waqi'a).\n"
         "4. Visualisez le quartz qui s'allume comme une LED doree.\n"
         "5. Voyez cette lumiere se repandre dans les spirales et dans la photo.\n"
         "6. Recitez 3x: 'Par la puissance du Code 19, que le Rizq m'arrive par toutes les directions.'\n"
         "7. Durée: 5 minutes."),
        ("Mi-journee (Duha — 10h-11h) — AMPLIFICATION",
         "1. Placez les deux mains en triangle au-dessus du montage.\n"
         "2. Recitez les 4 Noms Divins: Ya Razzaq (7x), Ya Fattah (7x), Ya Ghani (7x), Ya Mughni (7x).\n"
         "3. Recitez 1× le code 520 741 8 (argent inattendu).\n"
         "4. Visualisez 4 rayons colores (rouge, vert, bleu, or) convergeant vers le quartz.\n"
         "5. Sentez le champ energetique du montage qui pulse en harmonie avec votre cœur.\n"
         "6. Durée: 3 minutes."),
        ("Soir (Maghrib — Coucher du soleil) — SCELLEMENT",
         "1. Passez votre main gauche en cercle autour du montage, 7× dans le sens horaire.\n"
         "2. Recitez la Sourate Al-Waqi'a (56) ou son code 56-96-152 3x.\n"
         "3. Recitez 1x le code 4812412 (protection du montage).\n"
         "4. Recitez le Sceau 1x: 'Hasbunallahu wa ni'mal wakeel — Allah nous suffit.'\n"
         "5. Visualisez une bulle de lumiere violette qui entoure tout le montage.\n"
         "6. Durée: 3 minutes."),
        ("Avant sommeil — PROGRAMMATION PROFONDE",
         "1. Placez la photo sous votre oreiller (sortez-la du montage).\n"
         "2. Allongez-vous, mains sur le plexus solaire.\n"
         "3. Recitez 33x 'Allahumma salli 'ala Muhammad' (Salawat).\n"
         "4. Visualisez le quartz qui continue a briller sous votre lit.\n"
         "5. Intention: 'Mon subconscient integre les codes pendant mon sommeil.'\n"
         "6. Le matin, remettez la photo dans le montage."),
    ]

    for time_title, time_desc in daily_protocol:
        if y > 260:
            # Auto page break
            pdf.add_page()
            pdf.set_fill_color(*CREAM)
            pdf.rect(0, 0, 210, 297, 'F')
            y = 15

        pdf.set_font("L", "B", 7)
        pdf.set_text_color(*DARK_VIOLET)
        pdf.set_xy(16, y)
        pdf.cell(0, 4, time_title, align="L")
        pdf.set_font("L", "", 5.5)
        pdf.set_text_color(*BLACK)
        pdf.set_xy(16, y + 4.5)
        pdf.multi_cell(180, 3.5, time_desc)
        y = pdf.get_y() + 3

    pdf.set_font("L", "", 6)
    pdf.set_text_color(*GRAY)
    pdf.set_xy(0, 287)
    pdf.cell(210, 4, "Systeme Radionique Amplifie Miftah 19  |  Page 5/6", align="C")

    # ════════════════════════════════════════════════════════════════
    # PAGE 6 — RECOMMANDATIONS, ENTRETIEN, VARIANTES
    # ════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.set_fill_color(*CREAM)
    pdf.rect(0, 0, 210, 297, 'F')

    pdf.set_font("L", "B", 14)
    pdf.set_text_color(*DARK_VIOLET)
    pdf.set_xy(0, 14)
    pdf.cell(210, 7, "RECOMMANDATIONS, ENTRETIEN ET VARIANTES AVANCEES", align="C")
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.3)
    pdf.line(25, 23, 185, 23)

    y = 30

    # ── RECOMMENDATIONS ──
    pdf.set_font("L", "B", 9)
    pdf.set_text_color(*DARK_VIOLET)
    pdf.set_xy(15, y)
    pdf.cell(0, 5, "I. RECOMMANDATIONS GENERALES", align="L")
    y += 8

    recs = [
        "QUALITE DES MATERIAUX: Utilisez du cuivre PUR (fil electrique denude ou fil de bijouterie). Le cuivre recouvert de vernis est acceptable — le vernis sert d'isolant entre les spires. Les aimants doivent etre en NEODIME (NdFeB) grade N52 pour un champ maximal. Evitez les aimants ferrites qui sont trop faibles.",
        "PURIFICATION PREALABLE: Avant montage, purifiez chaque composant: quartz → eau distillee + sel 24h + soleil 1h. Cuivre → vinaigre blanc 1h → rincer a l'eau claire. Aimants → les passer a l'encens (benjoin ou oliban). Photo → lavisualiser entouree de lumiere blanche 1 minute.",
        "EMPLACEMENT DU MONTAGE: Placez le systeme dans un endroit calme, a l'abri des courants d'air et des sources electromagnetiques (wifi, micro-ondes, transformateurs). Idealement dans votre chambre, sur une table en bois naturelle, orientee vers l'EST (direction de la Mecque pour les pratiquants).",
        "DUREE D'UTILISATION: Cycle minimal: 7 jours (test). Cycle ideal: 19 jours (activation complete). Cycle profond: 40 jours (transmutation). Apres 40 jours, demontez le systeme, purifiez tous les elements, et reconstruisez-le avec une nouvelle photo si desire.",
        "NE JAMAIS DEPLACER LE MONTAGE PENDANT LE CYCLE: Le systeme cree un champ stable qui s'installe progressivement. Le deplacement brise la coherence. Si vous devez absolument le deplacer, refaites le rituel d'activation initial.",
        "HYGIENE ENERGETIQUE: Avant chaque utilisation, lavez-vous les mains. Ne manipulez pas le montage en etat de colere ou de stress. L'intention est le carburant du systeme. Un utilisateur centre et reconnaissant obtiendra des resultats 10× superieurs.",
    ]

    for rec in recs:
        pdf.set_font("L", "", 5.5)
        pdf.set_text_color(*BLACK)
        pdf.set_xy(18, y)
        pdf.cell(4, 3.5, "\u2022", align="C")
        pdf.set_xy(22, y)
        pdf.multi_cell(174, 3.5, rec)
        y = pdf.get_y() + 2
        if y > 145:
            break

    y = max(y, pdf.get_y() + 4)

    # ── VARIANTS / ADVANCED ──
    if y < 260:
        pdf.set_font("L", "B", 9)
        pdf.set_text_color(*DARK_VIOLET)
        pdf.set_xy(15, y)
        pdf.cell(0, 5, "II. VARIANTES AVANCEES", align="L")
        y += 8

        variants = [
            ("VARIANTE TOROIDAL (Haute Puissance)",
             "Remplacez les 8 petits aimants par un aimant toroidal (donut) en neodyme de 40mm de diametre "
             "exterieur, 20mm interieur, 5mm d'epaisseur. Placez-le SOUS la base du montage. Ce tore "
             "genere un champ beaucoup plus coherent et puissant. Le champ toroidal s'aligne parfaitement "
             "avec le carre Buduh et les spirales. Version professionnelle recommandee pour les pratiquants "
             "experimentes."),
            ("VARIANTE PYRAMIDE (Concentration Maximale)",
             "Construisez une pyramide en cuivre (base 150×150mm, hauteur 95mm — ratio phi 1.618) "
             "que vous placerez au-dessus du montage. La pyramide concentre l'energie au centre. "
             "Fabriquez-la en fil de cuivre de 2mm soudé aux sommets. La pyramide ajoute une couche "
             "supplementaire de geometrie sacree et multiplie l'effet par resonance de forme."),
            ("VARIANTE BOBINAGE BIFILAIRE (Annulation des parasites)",
             "Au lieu de deux spirales separees, utilisez un bobinage bifilaire: deux fils de cuivre "
             "paralleles enroules simultanement (19+7 tours). Ce montage annule les parasites "
             "electromagnetiques haute frequence tout en preservant le signal basse frequence. "
             "Technique utilisee dans les resistances de precision et les bobines de filtrage audio."),
            ("VARIANTE A DISTANCE (Radionique Remote)",
             "Une fois le systeme actif (apres 7 jours), vous pouvez 'broadcaster' les codes a distance. "
             "Prenez un petit quartz programme de 1cm, placez-le sur le montage pendant 1 heure avec "
             "l'intention de le charger. Ensuite, portez ce quartz sur vous (poche, collier). "
             "Le petit quartz agit comme un 'recepteur satellite' qui maintient la connexion avec "
             "le montage maitre. Ou: placez la photo d'une autre personne sur le montage 24h pour "
             "la traiter a distance."),
        ]

        for var_title, var_desc in variants:
            if y > 255:
                break
            pdf.set_font("L", "B", 6.5)
            pdf.set_text_color(*GOLD)
            pdf.set_xy(16, y)
            pdf.cell(0, 4, var_title, align="L")
            pdf.set_font("L", "", 5.5)
            pdf.set_text_color(*BLACK)
            pdf.set_xy(16, y + 4.5)
            pdf.multi_cell(180, 3.5, var_desc)
            y = pdf.get_y() + 3

    # ── QUICK REFERENCE ──
    if y < 235:
        y = max(y, pdf.get_y() + 2)
        pdf.set_font("L", "B", 9)
        pdf.set_text_color(*DARK_VIOLET)
        pdf.set_xy(15, y)
        pdf.cell(0, 5, "III. FICHE DE SUIVI — CALENDRIER DES 40 JOURS", align="L")
        y += 8

        pdf.set_fill_color(*DARK_BG)
        pdf.set_text_color(*GOLD)
        pdf.set_font("L", "B", 5.5)
        cal_headers = [("Phase", 25), ("Jours", 16), ("Effet Attendu", 75), ("Rituel Recommande", 74)]
        px = 12
        pdf.set_xy(px, y)
        for h, w in cal_headers:
            pdf.cell(w, 5, h, border=1, fill=True, align="C")
        pdf.ln()

        cal_entries = [
            ("Installation", "1-7", "Adaptation du systeme", "3x/jour — Protocole standard"),
            ("Activation", "8-14", "Premiers signes/synchronicites", "3x/jour + Version longue le soir"),
            ("Amplification", "15-21", "Changement perceptible du flux", "5x/jour + Inclure sourate Waqiah"),
            ("Stabilisation", "22-30", "Le Rizq devient fluide et regulier", "3x/jour — Confiance et gratitude"),
            ("Transmutation", "31-40", "Transformation profonde du rapport a l'argent", "Rituel complet 5x/jour + Jefne optionnel"),
        ]
        for phase, days, effect, ritual in cal_entries:
            pdf.set_xy(px, pdf.get_y())
            pdf.set_font("L", "B", 5.5)
            pdf.set_text_color(*DARK_VIOLET)
            pdf.cell(25, 5, phase, border=1, align="C")
            pdf.set_font("L", "B", 5.5)
            pdf.set_text_color(*GOLD)
            pdf.cell(16, 5, days, border=1, align="C")
            pdf.set_font("L", "", 5)
            pdf.set_text_color(*BLACK)
            pdf.cell(75, 5, effect, border=1, align="L")
            pdf.set_font("L", "", 5)
            pdf.set_text_color(*GRAY)
            pdf.cell(74, 5, ritual, border=1, align="L")
            pdf.ln()

    # Signature footer
    pdf.set_font("L", "", 6)
    pdf.set_text_color(*GRAY)
    pdf.set_xy(0, 287)
    pdf.cell(210, 4, "Systeme Radionique Amplifie Miftah 19  |  Page 6/6", align="C")

    # ════════════════════════════════════════════════════════════════
    # SAVE
    # ════════════════════════════════════════════════════════════════
    output = PDF_OUTPUTS["radionique_amplifiee"]
    pdf.output(str(output))
    print(f"SYSTEME RADIONIQUE AMPLIFIE GENERE: {output}")
    print(f"Pages: {pdf.page_no()}/6")
    print("Couverture: 7 couches | Cuivre + Aimants + Quartz + Codes Grabovoi + Photo")
    print("Pages 1: Schema systeme  |  2: Architecture 7 couches")
    print("Pages 3: Principes physiques  |  4: Tables de correspondances")
    print("Pages 5: Construction + Activation quotidienne  |  6: Entretien + Variantes")


if __name__ == "__main__":
    generate_amplified_radionics()
