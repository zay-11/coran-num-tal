#!/usr/bin/env python3
"""GUIDE VISUEL — Construction du Système Radionique Amplifié Miftah 19
   Schémas étape par étape avec vues de dessus, coupes et perspectives
   Généré entièrement en vectoriel via fpdf (sans dépendance externe)
"""

import math
from pathlib import Path
import sys
from fpdf import FPDF

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.project_paths import PDF_OUTPUTS, ensure_layout

ensure_layout()

# ── FONTS ──
LATIN  = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
LATIN_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# ── PALETTE ──
BG_CREAM    = (250, 245, 235)
BG_DARK     = (20, 15, 35)
GOLD        = (218, 165, 32)
GOLD_LIGHT  = (235, 195, 70)
VIOLET      = (80, 20, 130)
VIOLET_LIGHT= (140, 80, 200)
DARK_VIOLET = (50, 10, 90)
COPPER      = (184, 115, 51)
COPPER_LIGHT= (210, 155, 80)
RED_MAG     = (210, 60, 60)
BLUE_MAG    = (60, 60, 220)
QUARTZ_COL  = (200, 210, 240)
SILVER      = (180, 180, 180)
BLACK       = (25, 25, 25)
GRAY        = (100, 100, 100)
WHITE       = (255, 255, 255)
GREEN_OK    = (40, 180, 60)
ORANGE_STEP = (220, 140, 30)
BROWN_WOOD  = (140, 100, 60)
PAPER_COL   = (245, 242, 235)
PHOTO_COL   = (230, 210, 200)


class GuideVisuel(FPDF):
    """Generate visual step-by-step guide with schematics."""

    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.add_font("L", "", LATIN, uni=True)
        self.add_font("L", "B", LATIN_B, uni=True)
        self.set_auto_page_break(False)

    # ================================================================
    # DRAWING PRIMITIVES
    # ================================================================

    def _circle(self, x, y, r, style='D', color=GOLD, lw=0.4):
        self.set_draw_color(*color)
        self.set_line_width(lw)
        self.circle(x, y, r, style)

    def _fill_rect(self, x, y, w, h, color, border_color=None, lw=0.2):
        self.set_fill_color(*color)
        if border_color:
            self.set_draw_color(*border_color)
            self.set_line_width(lw)
        else:
            self.set_draw_color(*color)
        self.rect(x, y, w, h, 'DF' if border_color else 'F')

    def _line(self, x1, y1, x2, y2, color=GOLD, lw=0.3):
        self.set_draw_color(*color)
        self.set_line_width(lw)
        self.line(x1, y1, x2, y2)

    def _text(self, x, y, txt, size=6, color=BLACK, bold=False, align='L', w=40):
        style = "B" if bold else ""
        self.set_font("L", style, size)
        self.set_text_color(*color)
        self.set_xy(x, y)
        self.cell(w, 4, txt, align=align)

    def _arrow(self, x1, y1, x2, y2, color=GOLD, lw=0.4):
        """Draw arrow from (x1,y1) to (x2,y2)."""
        self.set_draw_color(*color)
        self.set_line_width(lw)
        self.line(x1, y1, x2, y2)
        ang = math.atan2(y2 - y1, x2 - x1)
        hs = 2.5
        self.line(x2, y2, x2 - hs * math.cos(ang - 0.45), y2 - hs * math.sin(ang - 0.45))
        self.line(x2, y2, x2 - hs * math.cos(ang + 0.45), y2 - hs * math.sin(ang + 0.45))

    def _dashed_rect(self, x, y, w, h, color=SILVER, lw=0.3):
        """Approximate dashed rectangle using short line segments."""
        self.set_draw_color(*color)
        self.set_line_width(lw)
        dash_len = 3
        gap_len = 2
        # Top
        cx = x
        while cx < x + w:
            end = min(cx + dash_len, x + w)
            self.line(cx, y, end, y)
            cx = end + gap_len
        # Bottom
        cx = x
        while cx < x + w:
            end = min(cx + dash_len, x + w)
            self.line(cx, y + h, end, y + h)
            cx = end + gap_len
        # Left
        cy = y
        while cy < y + h:
            end = min(cy + dash_len, y + h)
            self.line(x, cy, x, end)
            cy = end + gap_len
        # Right
        cy = y
        while cy < y + h:
            end = min(cy + dash_len, y + h)
            self.line(x + w, cy, x + w, end)
            cy = end + gap_len

    def _magnet_symbol(self, cx, cy, size=4, is_north=True):
        """Draw a small magnet symbol with N/S label."""
        col = RED_MAG if is_north else BLUE_MAG
        self._fill_rect(cx - size/2, cy - size/2, size, size, col, SILVER, 0.3)
        self._text(cx - size/2, cy - size/4 + 0.5, "N" if is_north else "S", 5, WHITE, True, 'C', size)

    def _crystal_symbol(self, cx, cy, h=10, w=4, color=QUARTZ_COL, label=""):
        """Draw a crystal symbol (pyramid + prism)."""
        self.set_fill_color(*color)
        self.set_draw_color(*SILVER)
        self.set_line_width(0.3)
        tip = (cx, cy - h)
        base_l = (cx - w, cy - h * 0.3)
        base_r = (cx + w, cy - h * 0.3)
        bot = (cx, cy + h * 0.3)
        self.polygon([tip, base_l, base_r], 'DF')
        self.polygon([base_l, base_r, bot], 'DF')
        # Center line (glow)
        self.set_draw_color(*GOLD_LIGHT)
        self.set_line_width(0.2)
        self.line(cx, cy - h, cx, cy + h * 0.3)
        if label:
            self._text(cx - 5, cy + h * 0.3 + 1, label, 4, GRAY, False, 'C', 10)

    def _spiral_draw(self, cx, cy, turns, max_r, min_r=2, color=COPPER, lw=0.6, step=8):
        """Draw a spiral."""
        self.set_draw_color(*color)
        self.set_line_width(lw)
        total_deg = turns * 360
        prev = None
        for deg in range(0, total_deg + step, step):
            theta = math.radians(deg)
            r = max_r - (max_r - min_r) * (deg / total_deg)
            x = cx + r * math.cos(theta)
            y = cy - r * math.sin(theta)
            if prev:
                self.line(prev[0], prev[1], x, y)
            prev = (x, y)

    def _star_8pt(self, cx, cy, R, color=GOLD, lw=0.4):
        """8-pointed star (two squares)."""
        pts = [(cx + R * math.cos(math.radians(i*45)), cy - R * math.sin(math.radians(i*45)))
               for i in range(8)]
        self.set_draw_color(*color)
        self.set_line_width(lw)
        for i in range(0, 8, 2):
            self.line(pts[i][0], pts[i][1], pts[(i+2) % 8][0], pts[(i+2) % 8][1])
        for i in range(1, 8, 2):
            self.line(pts[i][0], pts[i][1], pts[(i+2) % 8][0], pts[(i+2) % 8][1])

    def _buduh_square(self, cx, cy, size=18):
        """Draw the Buduh 3×3 magic square."""
        self.set_draw_color(*GOLD)
        self.set_line_width(0.3)
        # Grid
        cell = size / 3
        ox = cx - size/2
        oy = cy - size/2
        for i in range(4):
            self.line(ox + i*cell, oy, ox + i*cell, oy + size)
            self.line(ox, oy + i*cell, ox + size, oy + i*cell)
        # Numbers
        nums = [
            (1, 0, 0), (2, 1, 0), (3, 2, 0),
            (4, 0, 1), (5, 1, 1), (6, 2, 1),
            (7, 0, 2), (8, 1, 2), (9, 2, 2),
        ]
        # Actually Buduh is: 4 9 2 / 3 5 7 / 8 1 6
        buduh = [[4, 9, 2], [3, 5, 7], [8, 1, 6]]
        for row in range(3):
            for col in range(3):
                n = str(buduh[row][col])
                self._text(ox + col*cell + 1, oy + row*cell + 1, n, 6, GOLD, True, 'C', cell)

    def _compass_rose(self, cx, cy, R, labels=True):
        """Draw compass rose with 8 directions."""
        self.set_draw_color(*GRAY)
        self.set_line_width(0.15)
        for deg in range(0, 360, 45):
            rad = math.radians(deg)
            x1 = cx + (R - 3) * math.cos(rad)
            y1 = cy - (R - 3) * math.sin(rad)
            x2 = cx + R * 1.1 * math.cos(rad)
            y2 = cy - R * 1.1 * math.sin(rad)
            self.line(x1, y1, x2, y2)
            if labels:
                dirs = {0: "N", 45: "NE", 90: "E", 135: "SE", 180: "S", 225: "SO", 270: "O", 315: "NO"}
                if deg in dirs:
                    lx = cx + (R + 6) * math.cos(rad)
                    ly = cy - (R + 6) * math.sin(rad) - 2
                    self._text(lx - 3, ly, dirs[deg], 4, GRAY, True, 'C', 6)

    def _step_header(self, step_num, title, y):
        """Draw a step header banner."""
        self._fill_rect(10, y - 2, 190, 8, DARK_VIOLET, GOLD, 0.5)
        self._text(14, y + 0.5, f"ÉTAPE {step_num}", 7, GOLD, True, 'L', 30)
        self._text(50, y + 0.5, title, 7, WHITE, True, 'L', 150)

    def _material_badge(self, x, y, text, color=COPPER):
        """Small colored badge for materials."""
        self._fill_rect(x, y, 45, 4.5, color, SILVER, 0.2)
        self._text(x + 1, y + 0.3, text, 4.5, WHITE, True, 'L', 43)

    def _step_number_box(self, num, cx, y, R=6):
        """Draw a circled step number."""
        self._circle(cx, y, R, 'D', GOLD, 0.5)
        self._fill_rect(cx - R, y - R, 2*R, 2*R, DARK_VIOLET, GOLD, 0.3)
        self._text(cx - 3, y - 2.5, str(num), 7, GOLD, True, 'C', 6)

    def _legend_item(self, x, y, w, h, color, label):
        """Draw a legend color swatch + label."""
        self._fill_rect(x, y, w, h, color, GRAY, 0.2)
        self._text(x + w + 2, y - 0.5, label, 4.5, BLACK, False, 'L', 50)

    def _section_title(self, y, title, subtitle=""):
        """Draw a section title."""
        self._fill_rect(10, y, 190, 7, DARK_VIOLET, GOLD, 0.4)
        self._text(14, y + 1.5, title, 8, GOLD, True, 'L', 186)
        if subtitle:
            self._text(14, y + 7.5, subtitle, 4.5, GRAY, False, 'L', 186)
        return y + 11


# ════════════════════════════════════════════════════════════════════
# PAGE LAYOUT: STEP SCHEMATIC + INSTRUCTIONS
# ════════════════════════════════════════════════════════════════════

def _draw_step_legend(g, y_start):
    """Draw a compact legend for schematic symbols."""
    y = y_start
    g._fill_rect(10, y, 190, 18, BG_CREAM, GOLD, 0.3)
    g._text(14, y + 1, "LÉGENDE DES SCHÉMAS :", 5, DARK_VIOLET, True, 'L', 50)
    items = [
        (COPPER, "Cuivre / Fil"), (RED_MAG, "Aimant N"), (BLUE_MAG, "Aimant S"),
        (QUARTZ_COL, "Quartz"), (PHOTO_COL, "Photo"), (BROWN_WOOD, "Base bois"),
        (PAPER_COL, "Papier codes"), (GOLD, "Traits géométriques"),
    ]
    for i, (c, lbl) in enumerate(items):
        col = i % 4
        row = i // 4
        g._legend_item(14 + col * 48, y + 5 + row * 6, 4, 4, c, lbl)


def _draw_title_block(g, page_title):
    """Draw page title."""
    g._fill_rect(0, 0, 210, 22, BG_DARK)
    g._text(105, 5, "GUIDE VISUEL — CONSTRUCTION DU SYSTÈME RADIONIQUE AMPLIFIÉ", 9, GOLD, True, 'C', 200)
    g._text(105, 14, page_title, 6, GOLD_LIGHT, False, 'C', 200)
    g._line(20, 21, 190, 21, GOLD, 0.3)


# ════════════════════════════════════════════════════════════════════
# PAGE 1: ÉTAPE 1 — BASE + GÉOMÉTRIE
# ════════════════════════════════════════════════════════════════════

def page1_base(g):
    _draw_title_block(g, "ÉTAPE 1 : PRÉPARATION DE LA BASE")

    # LEFT: TOP VIEW schematic
    cx, cy = 50, 80
    # Base plate (wood)
    g._fill_rect(cx - 35, cy - 35, 70, 70, BROWN_WOOD, SILVER, 0.5)
    g._text(cx - 15, cy + 31, "Base bois 150×150mm", 4, WHITE, False, 'C', 30)

    # Main circle
    g._circle(cx, cy, 32, 'D', GOLD, 0.5)
    g._circle(cx, cy, 30, 'D', VIOLET, 0.3)

    # Compass rose
    g._compass_rose(cx, cy, 28)

    # Mark 8 direction holes
    for deg in range(0, 360, 45):
        rad = math.radians(deg)
        hx = cx + 28 * math.cos(rad)
        hy = cy - 28 * math.sin(rad)
        g._circle(hx, hy, 2.5, 'D', GOLD, 0.4)
        g._fill_rect(hx - 1, hy - 1, 2, 2, GOLD)

    # Center mark
    g._circle(cx, cy, 3, 'D', GOLD, 0.5)
    g._fill_rect(cx - 1, cy - 1, 2, 2, VIOLET)

    # Labels
    g._text(cx - 32, cy - 42, "VUE DE DESSUS", 5, DARK_VIOLET, True, 'C', 64)
    g._text(cx - 30, cy - 38, "Base carrée avec cercle R=65mm et 8 directions", 3.5, GRAY, False, 'C', 60)

    # RIGHT: Perspective view
    px, py = 148, 85
    # 3D box (simple parallelogram)
    g.set_fill_color(*BROWN_WOOD)
    g.set_draw_color(*SILVER)
    g.set_line_width(0.3)
    # Front face
    g.rect(px - 25, py - 20, 50, 40, 'DF')
    # Top face (tilted)
    g.polygon([
        (px - 25, py - 20),
        (px - 15, py - 30),
        (px + 35, py - 30),
        (px + 25, py - 20),
    ], 'DF')
    # Right face
    g.polygon([
        (px + 25, py - 20),
        (px + 35, py - 30),
        (px + 35, py + 10),
        (px + 25, py + 20),
    ], 'DF')
    g._text(px - 10, py + 22, "VUE 3D", 5, DARK_VIOLET, True, 'C', 30)

    # Material badge
    g._material_badge(12, 50, "📦 Carton boisé 3-5mm", BROWN_WOOD)
    g._material_badge(12, 56, "✏️ Compas + règle + crayon", GRAY)
    g._material_badge(12, 62, "🎨 Peinture noire/violet foncé", DARK_VIOLET)

    # INSTRUCTIONS BOX (bottom)
    y_inst = 150
    g._fill_rect(12, y_inst, 186, 60, BG_DARK, GOLD, 0.3)
    g._text(16, y_inst + 2, "✦ INSTRUCTIONS DÉTAILLÉES", 7, GOLD, True, 'L', 100)

    instructions = [
        "1. Découpez un carré de carton boisé ou de bois de 150×150mm (épaisseur 3-5mm)",
        "2. Poncez les bords au papier de verre grain 120, puis 240",
        "3. Peignez en noir mat ou violet foncé — 2 couches, séchage 2h entre chaque",
        "4. Au compas, tracez un cercle de 65mm de rayon exactement au centre",
        "5. Marquez les 8 directions (N, NE, E, SE, S, SO, O, NO) à 45° d'intervalle",
        "6. Percez un petit trou de 1mm à chaque marque (pour l'alignement des aimants)",
        "7. Vérifiez avec une équerre que la base est bien droite — la précision est cruciale",
    ]
    for i, inst in enumerate(instructions):
        g._text(16, y_inst + 10 + i * 6.5, inst, 5, WHITE, False, 'L', 180)

    # Legend
    _draw_step_legend(g, 215)
    g._text(105, 287, "Guide Visuel Radionique Miftah 19  |  Page 1/9", 5, GRAY, False, 'C', 200)


# ════════════════════════════════════════════════════════════════════
# PAGE 2: ÉTAPE 2 — GÉOMÉTRIE SACRÉE
# ════════════════════════════════════════════════════════════════════

def page2_geometrie(g):
    _draw_title_block(g, "ÉTAPE 2 : DESSIN DE LA GÉOMÉTRIE SACRÉE")

    # MAIN SCHEMATIC
    cx, cy = 60, 85
    # Base outline
    g._fill_rect(cx - 32, cy - 32, 64, 64, BROWN_WOOD, SILVER, 0.3)
    g._circle(cx, cy, 30, 'D', GOLD, 0.4)

    # 8-pointed star
    g._star_8pt(cx, cy, 26, GOLD, 0.4)

    # Concentric circles
    for r, col, lw in [(20, VIOLET, 0.3), (12, GOLD, 0.3), (6, VIOLET, 0.3)]:
        g._circle(cx, cy, r, 'D', col, lw)

    # Buduh square at center
    g._buduh_square(cx, cy, 22)

    # Compass
    g._compass_rose(cx, cy, 29)

    # Labels
    g._text(cx - 30, cy - 38, "ÉTOILE 8 BRANCHES + CARRÉ BUDUH", 4.5, DARK_VIOLET, True, 'C', 60)

    # DETAIL: Buduh close-up
    bx, by = 148, 70
    g._text(bx, by - 28, "✦ CARRÉ BUDUH (DÉTAIL)", 5, DARK_VIOLET, True, 'L', 50)
    g._buduh_square(bx, by, 24)
    g._text(bx - 12, by + 16, "4  9  2     → 15", 4, GOLD, False, 'L', 35)
    g._text(bx - 12, by + 21, "3  5  7     → 15", 4, GOLD, False, 'L', 35)
    g._text(bx - 12, by + 26, "8  1  6     → 15", 4, GOLD, False, 'L', 35)
    g._text(bx - 12, by + 31, "↓  ↓  ↓  ↗  ↘", 4, GRAY, False, 'L', 35)
    g._text(bx - 12, by + 35, "15 15 15 15 15", 4, GOLD, False, 'L', 35)
    g._text(bx - 12, by + 39, "Magique ! 3² = 9 cellules", 3.5, GRAY, False, 'L', 35)

    # MATERIALS
    g._material_badge(12, 48, "✏️ Compas à pointe sèche", GOLD)
    g._material_badge(12, 54, "📐 Règle métallique 15cm", SILVER)
    g._material_badge(12, 60, "🖊️ Stylo gel doré (0.5mm)", GOLD_LIGHT)

    # INSTRUCTIONS
    y_inst = 120
    g._fill_rect(12, y_inst, 186, 85, BG_DARK, GOLD, 0.3)
    g._text(16, y_inst + 2, "✦ INSTRUCTIONS DÉTAILLÉES", 7, GOLD, True, 'L', 100)

    instructions = [
        "1. Avec le compas, tracez les cercles concentriques: R=30, R=20, R=12, R=6mm",
        "2. L'étoile à 8 branches: 2 carrés superposés à 45° — reliez les 8 marques directionnelles",
        "3. Au centre exact, construisez le carré Buduh (30×30mm):",
        "   • Ligne 1: 4 | 9 | 2    (somme = 15)", "   • Ligne 2: 3 | 5 | 7    (somme = 15)",
        "   • Ligne 3: 8 | 1 | 6    (somme = 15)", "   • Toutes les colonnes et diagonales = 15 aussi !",
        "4. Le chiffre 15 (1+5=6) est le nombre de l'harmonie — 15 est aussi 5+5+5",
        "5. Utilisez un stylo gel doré pour les traits — il conduit mieux l'énergie",
        "6. Laissez sécher 30 min avant de passer à l'étape suivante",
    ]
    for i, inst in enumerate(instructions):
        clr = GOLD if i in [3, 4, 5, 6] else WHITE
        sz = 4.5 if i in [3, 4, 5, 6] else 5
        g._text(16, y_inst + 10 + i * 6.5, inst, sz, clr, False, 'L', 180)

    # Legend
    _draw_step_legend(g, 210)
    g._text(105, 287, "Guide Visuel Radionique Miftah 19  |  Page 2/9", 5, GRAY, False, 'C', 200)


# ════════════════════════════════════════════════════════════════════
# PAGE 3: ÉTAPE 3 — PAPIER DE CODES
# ════════════════════════════════════════════════════════════════════

def page3_codes(g):
    _draw_title_block(g, "ÉTAPE 3 : PRÉPARATION DU PAPIER DE CODES")

    cx, cy = 55, 80
    # Paper
    g._fill_rect(cx - 30, cy - 30, 60, 60, PAPER_COL, SILVER, 0.5)
    g._dashed_rect(cx - 30, cy - 30, 60, 60, GRAY, 0.2)
    g._text(cx - 20, cy - 35, "FEUILLE DE CODES (140×140mm)", 5, DARK_VIOLET, True, 'C', 40)

    # Outer circle
    g._circle(cx, cy, 28, 'D', GOLD, 0.4)

    # 8 code positions
    codes = {
        0:    ("520 741 8", "N"),
        45:   ("318 798", "NE"),
        90:   ("56 96 152", "E"),
        135:  ("318 612 518 714", "SE"),
        180:  ("9798733714615", "S"),
        225:  ("4812412", "SO"),
        270:  ("917 418 619", "O"),
        315:  ("888 888 888", "NO"),
    }
    for deg, (code, lbl) in codes.items():
        rad = math.radians(deg)
        tx = cx + 22 * math.cos(rad)
        ty = cy - 22 * math.sin(rad)
        # Code box
        g._fill_rect(tx - 14, ty - 4, 28, 8, WHITE, GOLD, 0.3)
        g._text(tx - 13, ty - 2.5, code, 3.5, VIOLET, True, 'C', 26)
        g._text(tx - 13, ty + 2, lbl, 3, GRAY, False, 'C', 26)

    # Divine Names at 4 corners
    names = [("Ya Razzaq", -24, -24), ("Ya Fattah", 24, -24),
             ("Ya Ghani", -24, 24), ("Ya Mughni", 24, 24)]
    for name, dx, dy in names:
        nx = cx + dx
        ny = cy + dy
        g._fill_rect(nx - 8, ny - 3.5, 16, 7, DARK_VIOLET, GOLD, 0.3)
        g._text(nx - 7, ny - 2, name, 3.5, GOLD, True, 'C', 14)

    # Center cross
    g._fill_rect(cx - 5, cy - 0.5, 10, 1, GOLD)
    g._fill_rect(cx - 0.5, cy - 5, 1, 10, GOLD)

    # DETAIL BOX — Code breakdown
    dx, dy = 130, 62
    g._fill_rect(dx - 20, dy - 15, 80, 65, BG_DARK, GOLD, 0.3)
    g._text(dx - 18, dy - 12, "📋 CODES GRABOVOI COMPLETS", 5, GOLD, True, 'L', 76)

    code_details = [
        "N  = 520 741 8      → Argent inattendu",
        "NE = 318 798        → Abondance",
        "E  = 56 96 152      → Al-Waqi'a (MAÎTRE)",
        "SE = 318 612 518 714→ Cash-flow",
        "S  = 9798733714615  → Manifester",
        "SO = 4812412        → Protection",
        "O  = 917 418 619    → Bouclier psychique",
        "NO = 888 888 888    → Santé optimale",
    ]
    for i, cd in enumerate(code_details):
        g._text(dx - 17, dy - 5 + i * 6.5, cd, 4.5, WHITE, False, 'L', 76)

    # MATERIALS
    g._material_badge(12, 48, "📄 Papier blanc A5 ou 15×15cm", PAPER_COL)
    g._material_badge(12, 54, "🖨️ Imprimante laser + cartouche or", GOLD_LIGHT)
    g._material_badge(12, 60, "🖊️ Stylo gel doré et violet", VIOLET)

    # INSTRUCTIONS
    y_inst = 140
    g._fill_rect(12, y_inst, 186, 72, BG_DARK, GOLD, 0.3)
    g._text(16, y_inst + 2, "✦ INSTRUCTIONS DÉTAILLÉES", 7, GOLD, True, 'L', 100)

    instructions = [
        "1. Imprimez ou recopiez les codes sur une feuille blanche 140×140mm",
        "2. Tracez le cercle au centre, puis placez chaque code à sa direction exacte",
        "3. Encadrez chaque code d'un rectangle doré de 28×8mm",
        "4. Ajoutez les 4 Noms Divins aux 4 coins en lettres violettes",
        "5. Le code MAÎTRE 56 96 152 (Al-Waqi'a) est à l'EST — direction du soleil levant",
        "6. Vérifiez que les codes sont lisibles et bien centrés dans leurs rectangles",
        "7. La précision de l'écriture est importante — chaque chiffre est une fréquence",
    ]
    for i, inst in enumerate(instructions):
        g._text(16, y_inst + 10 + i * 7.5, inst, 5, WHITE, False, 'L', 180)

    _draw_step_legend(g, 216)
    g._text(105, 287, "Guide Visuel Radionique Miftah 19  |  Page 3/9", 5, GRAY, False, 'C', 200)


# ════════════════════════════════════════════════════════════════════
# PAGE 4: ÉTAPE 4 — AIMANTS
# ════════════════════════════════════════════════════════════════════

def page4_aimants(g):
    _draw_title_block(g, "ÉTAPE 4 : PLACEMENT DES 8 AIMANTS NÉODYME")

    # MAIN SCHEMATIC — Top view with magnets
    cx, cy = 50, 80
    g._circle(cx, cy, 30, 'D', GOLD, 0.4)
    g._circle(cx, cy, 25, 'D', VIOLET, 0.3)

    # 8 magnets in ring (on the 28mm radius circle)
    for i in range(8):
        deg = i * 45
        rad = math.radians(deg)
        mx = cx + 26 * math.cos(rad)
        my = cy - 26 * math.sin(rad)
        is_north = (i % 2 == 0)
        g._magnet_symbol(mx, my, 6, is_north)

    # Center mark
    g._circle(cx, cy, 3, 'D', GOLD, 0.3)

    # Field lines (symbolic)
    g.set_draw_color(*VIOLET_LIGHT)
    g.set_line_width(0.08)
    for a in range(0, 360, 30):
        rad = math.radians(a)
        g.curve(
            cx + 6 * math.cos(rad), cy - 6 * math.sin(rad),
            cx + 18 * math.cos(rad), cy - 18 * math.sin(rad),
            cx + 28 * math.cos(rad), cy - 28 * math.sin(rad),
        )

    g._text(cx - 28, cy - 36, "8 AIMANTS EN RING — ALTERNANCE N/S", 4.5, DARK_VIOLET, True, 'C', 56)

    # POLARITY DIAGRAM
    px, py = 138, 55
    g._fill_rect(px - 25, py - 15, 50, 35, BG_DARK, GOLD, 0.3)
    g._text(px - 22, py - 12, "🌀 POLARITÉ (vue de dessus)", 5, GOLD, True, 'L', 46)

    pola = [
        ("N → NORD (0°)", "N", RED_MAG),
        ("S → NE (45°)", "S", BLUE_MAG),
        ("N → EST (90°)", "N", RED_MAG),
        ("S → SE (135°)", "S", BLUE_MAG),
        ("N → SUD (180°)", "N", RED_MAG),
        ("S → SO (225°)", "S", BLUE_MAG),
        ("N → OUEST (270°)", "N", RED_MAG),
        ("S → NO (315°)", "S", BLUE_MAG),
    ]
    for i, (dir_txt, pol, col) in enumerate(pola):
        row = i // 2
        col2 = i % 2
        g._fill_rect(px - 22 + col2 * 23, py - 5 + row * 4.5, 4, 3.5, col, SILVER, 0.2)
        g._text(px - 17 + col2 * 23, py - 5 + row * 4.5, pol, 4, WHITE, True, 'C', 4)
        g._text(px - 12 + col2 * 23, py - 5 + row * 4.5, dir_txt, 3.5, WHITE, False, 'L', 22)

    # FIELD ANIMATION — toroidal field cross-section
    fx, fy = 138, 115
    g._text(fx, fy - 28, "🌀 CHAMP TOROÏDAL (coupe)", 5, DARK_VIOLET, True, 'L', 50)
    # Torus cross-section
    g._circle(fx, fy - 5, 12, 'D', VIOLET, 0.3)
    g._circle(fx, fy - 5, 8, 'D', GOLD, 0.2)
    # Field lines
    for a in [0, 45, 90, 135]:
        rad = math.radians(a)
        g.set_draw_color(*VIOLET_LIGHT)
        g.set_line_width(0.1)
        g.curve(
            fx + 3 * math.cos(rad), fy - 5 + 3 * math.sin(rad),
            fx + 10 * math.cos(rad), fy - 5 + 10 * math.sin(rad),
            fx + 14 * math.cos(rad), fy - 5 + 14 * math.sin(rad),
        )
    g._text(fx - 15, fy + 14, "L'énergie circule en tore (donut)", 3.5, GRAY, False, 'C', 34)
    g._text(fx - 15, fy + 18, "N = rouge, S = bleu", 3.5, GRAY, False, 'C', 34)

    # MATERIALS
    g._material_badge(12, 48, "🧲 8× Aimants NdFeB N52 5×5×5mm", RED_MAG)
    g._material_badge(12, 54, "🧲 Boussole pour vérifier polarité", SILVER)
    g._material_badge(12, 60, "💧 Colle cyanoacrylate (gel)", GOLD)

    # INSTRUCTIONS
    y_inst = 150
    g._fill_rect(12, y_inst, 186, 72, BG_DARK, GOLD, 0.3)
    g._text(16, y_inst + 2, "✦ INSTRUCTIONS DÉTAILLÉES", 7, GOLD, True, 'L', 100)

    instructions = [
        "1. Identifiez la polarité des aimants avec la boussole (le côté N attire le sud de la boussole)",
        "2. Placez les aimants en cercle (R=28mm) en ALTERNANT N/S comme indiqué au-dessus",
        "3. N au NORD (0°), S au NE (45°), N à l'EST (90°), etc. — respectez l'ordre !",
        "4. Appliquez une micro-goutte de colle cyanoacrylate sous chaque aimant",
        "5. Utilisez une pince en laiton (non magnétique) pour positionner les aimants",
        "6. Vérifiez avec la boussole que le champ tourne bien en cercle",
        "7. Le champ toroïdal créé est la 'pompe magnétique' du système",
        "8. Laissez la colle polymériser 10 minutes avant l'étape suivante",
    ]
    for i, inst in enumerate(instructions):
        clr = GOLD if i in [1, 2] else WHITE
        g._text(16, y_inst + 10 + i * 7.5, inst, 5, clr, False, 'L', 180)

    _draw_step_legend(g, 226)
    g._text(105, 287, "Guide Visuel Radionique Miftah 19  |  Page 4/9", 5, GRAY, False, 'C', 200)


# ════════════════════════════════════════════════════════════════════
# PAGE 5: ÉTAPE 5 — PHOTO
# ════════════════════════════════════════════════════════════════════

def page5_photo(g):
    _draw_title_block(g, "ÉTAPE 5 : PLACEMENT DE LA PHOTO (WITNESS)")

    # SCHEMATIC — Top view
    cx, cy = 50, 75
    g._circle(cx, cy, 32, 'D', GOLD, 0.3)
    g._circle(cx, cy, 28, 'D', VIOLET, 0.3)

    # Photo in center
    ph_w, ph_h = 22, 28
    ph_x, ph_y = cx - ph_w/2, cy - ph_h/2
    g._fill_rect(ph_x, ph_y, ph_w, ph_h, PHOTO_COL, GOLD, 0.5)
    g._text(cx - 8, ph_y + 6, "📸", 8, BLACK, False, 'C', 17)
    g._text(cx - 8, ph_y + 15, "PHOTO", 4, DARK_VIOLET, True, 'C', 17)
    g._text(cx - 8, ph_y + 20, "(face bas)", 3.5, GRAY, False, 'C', 17)

    # Arrows showing face-down
    for ang in [0, 90, 180, 270]:
        rad = math.radians(ang)
        ax = cx + 16 * math.cos(rad)
        ay = cy - 16 * math.sin(rad)
        g._arrow(ax, ay, cx + 12 * math.cos(rad), cy - 12 * math.sin(rad), GOLD, 0.3)

    # Magnets still visible around
    for i in range(8):
        deg = i * 45
        rad = math.radians(deg)
        mx = cx + 27 * math.cos(rad)
        my = cy - 27 * math.sin(rad)
        is_north = (i % 2 == 0)
        g._magnet_symbol(mx, my, 4.5, is_north)

    g._text(cx - 25, cy - 42, "PHOTO AU CENTRE — FACE VERS LE BAS", 4.5, DARK_VIOLET, True, 'C', 50)

    # CROSS-SECTION VIEW
    sx, sy = 135, 72
    g._text(sx - 20, sy - 35, "✂️ COUPE TRANSVERSALE", 5, DARK_VIOLET, True, 'L', 50)

    # Cross-section: wood base, paper, photo, magnets
    # Wood base
    g._fill_rect(sx - 30, sy, 60, 6, BROWN_WOOD, SILVER, 0.3)
    # Paper layer
    g._fill_rect(sx - 28, sy - 1, 56, 2, PAPER_COL, GRAY, 0.2)
    # Photo
    g._fill_rect(sx - 9, sy - 3, 18, 2, PHOTO_COL, GOLD, 0.3)
    # Magnet (side)
    g._fill_rect(sx + 22, sy - 3, 5, 6, RED_MAG, SILVER, 0.3)
    g._text(sx + 21, sy + 4, "Aimant", 3, GRAY, False, 'L', 10)
    g._text(sx - 28, sy + 5, "Base bois", 3, GRAY, False, 'L', 15)
    g._text(sx - 10, sy - 5, "Photo (face bas)", 3, GRAY, False, 'C', 20)
    g._arrow(sx + 27, sy - 2, sx + 27, sy - 10, VIOLET, 0.2)
    g._text(sx + 22, sy - 14, "Les codes traversent la photo", 3.5, GRAY, False, 'L', 20)

    # STACK ORDER
    g._fill_rect(sx - 30, sy + 22, 60, 30, BG_DARK, GOLD, 0.3)
    g._text(sx - 27, sy + 24, "📚 ORDRE DE LA PILE (bas→haut)", 5, GOLD, True, 'L', 54)
    stack = [
        "[1] Base bois (support)",
        "[2] Papier codes (fréquences)",
        "[3] Photo (witness) FACE BAS",
        "[4] Spirales cuivre + quartz",
    ]
    for i, s in enumerate(stack):
        g._text(sx - 25, sy + 30 + i * 6, s, 4.5, WHITE if i < 2 else (GOLD if i == 2 else WHITE), False, 'L', 54)

    # INSTRUCTIONS
    y_inst = 130
    g._fill_rect(12, y_inst, 186, 72, BG_DARK, GOLD, 0.3)
    g._text(16, y_inst + 2, "✦ INSTRUCTIONS DÉTAILLÉES", 7, GOLD, True, 'L', 100)

    instructions = [
        "1. Prenez une photo portrait standard (4×5cm) — de préférence récente, visage clair",
        "2. Placez la photo au CENTRE EXACT du carré Buduh (utilisez les lignes comme guide)",
        "3. La photo doit être FACE VERS LE BAS — l'image contre les codes, le dos visible",
        "4. Le centre de la photo doit coïncider avec le centre du système (précision 1mm)",
        "5. NE COLLEZ PAS la photo — elle doit pouvoir être retirée pour le rituel nocturne",
        "6. Un petit poids en laiton peut maintenir la photo en place temporairement",
        "7. La photo est le 'témoin' — elle connecte le système à votre champ biologique",
    ]
    for i, inst in enumerate(instructions):
        clr = GOLD if i in [2, 3] else WHITE
        g._text(16, y_inst + 10 + i * 7.5, inst, 5, clr, False, 'L', 180)

    _draw_step_legend(g, 206)
    g._text(105, 287, "Guide Visuel Radionique Miftah 19  |  Page 5/9", 5, GRAY, False, 'C', 200)


# ════════════════════════════════════════════════════════════════════
# PAGE 6: ÉTAPE 6 — SPIRALE PRIMAIRE 19 TOURS
# ════════════════════════════════════════════════════════════════════

def page6_spirale_19(g):
    _draw_title_block(g, "ÉTAPE 6 : BOBINAGE DE LA SPIRALE PRIMAIRE (19 tours)")

    # MAIN — Spiral top view
    cx, cy = 55, 78
    g._circle(cx, cy, 32, 'D', GOLD, 0.3)
    g._circle(cx, cy, 28, 'D', VIOLET, 0.3)

    # Draw spiral 19 turns
    g._spiral_draw(cx, cy, 19, 24, 3, COPPER, 1.0, 6)

    # Center mark
    g._circle(cx, cy, 4, 'D', GOLD, 0.5)

    # Start/end markers
    g._fill_rect(cx - 1, cy - 1, 2, 2, GOLD)
    # End of spiral
    end_deg = 19 * 360
    end_r = 24 - (24 - 3) * (end_deg / (19 * 360))
    ex = cx + end_r * math.cos(math.radians(end_deg))
    ey = cy - end_r * math.sin(math.radians(end_deg))
    g._circle(ex, ey, 2, 'D', GOLD, 0.4)

    # Labels
    g._text(cx - 5, cy - 30, "DÉPART (centre)", 3.5, GRAY, False, 'C', 20)
    g._text(ex - 8, ey - 8, "ARRIVÉE (R=30mm)", 3.5, GRAY, False, 'C', 20)

    # WINDING DIRECTION
    dx, dy = 130, 55
    g._fill_rect(dx - 15, dy - 10, 70, 38, BG_DARK, GOLD, 0.3)
    g._text(dx - 12, dy - 7, "🔄 SENS DE BOBINAGE", 5, GOLD, True, 'L', 64)
    g._text(dx - 10, dy, "HORAIRE (CLOCKWISE)", 5, GOLD_LIGHT, True, 'L', 60)

    # Draw an arrow in a circle
    g._circle(dx + 20, dy + 16, 8, 'D', GOLD, 0.3)
    # Clockwise arrow
    for a_deg in [0, 45, 90, 135, 180, 225, 270, 315]:
        a_rad = math.radians(a_deg)
        g._arrow(
            dx + 20 + 5 * math.cos(a_rad),
            dy + 16 - 5 * math.sin(a_rad),
            dx + 20 + 8 * math.cos(a_rad),
            dy + 16 - 8 * math.sin(a_rad),
            GOLD_LIGHT, 0.2
        )

    # CALCULATIONS
    g._fill_rect(dx - 15, dy + 35, 70, 35, BG_DARK, GOLD, 0.3)
    g._text(dx - 12, dy + 37, "📐 CALCULS", 5, GOLD, True, 'L', 64)
    calcs = [
        "Fil: ~95cm de long",
        "Diamètre: 0.8mm émaillé",
        "Inductance: ~9.5 µH",
        "R=3→30mm, pas 1.5mm",
        "Fréq. résonance: ~23 kHz",
    ]
    for i, c in enumerate(calcs):
        g._text(dx - 10, dy + 43 + i * 5.5, c, 4, WHITE, False, 'L', 60)

    # INSTRUCTIONS
    y_inst = 135
    g._fill_rect(12, y_inst, 186, 78, BG_DARK, GOLD, 0.3)
    g._text(16, y_inst + 2, "✦ INSTRUCTIONS DÉTAILLÉES", 7, GOLD, True, 'L', 100)

    instructions = [
        "1. Prenez ~1m de fil de cuivre émaillé 0.8mm — coupez 5mm de plus pour les extrémités",
        "2. Commencez à côté du centre (à 3mm du point central, côté NORD du carré Buduh)",
        "3. Enroulez 19 tours en spirale HORAIRE en élargissant progressivement jusqu'à R=30mm",
        "4. L'espacement entre chaque tour doit être d'environ 1.5mm — constant !",
        "5. Utilisez une pince fine pour maintenir le début du fil pendant les premiers tours",
        "6. Appliquez 3 points de colle chaude (à 120°, 240°, 360°) pour maintenir la spirale",
        "7. Les 19 tours = Code 19 (74:30) — le fil devient une antenne accordée",
        "8. L'extrémité extérieure doit dépasser de 5mm — elle servira plus tard",
        "9. Vérifiez que les spires ne se touchent pas (l'émail isole, mais l'espacement est important)",
    ]
    for i, inst in enumerate(instructions):
        clr = GOLD if i in [2, 6] else WHITE
        g._text(16, y_inst + 10 + i * 7.2, inst, 5, clr, False, 'L', 180)

    _draw_step_legend(g, 218)
    g._text(105, 287, "Guide Visuel Radionique Miftah 19  |  Page 6/9", 5, GRAY, False, 'C', 200)


# ════════════════════════════════════════════════════════════════════
# PAGE 7: ÉTAPE 7 — SPIRALE SECONDAIRE 7 TOURS
# ════════════════════════════════════════════════════════════════════

def page7_spirale_7(g):
    _draw_title_block(g, "ÉTAPE 7 : BOBINAGE DE LA SPIRALE SECONDAIRE (7 tours)")

    # MAIN — Both spirals
    cx, cy = 55, 78
    g._circle(cx, cy, 32, 'D', GOLD, 0.3)
    g._circle(cx, cy, 28, 'D', VIOLET, 0.3)

    # Primary (faint, behind)
    g._spiral_draw(cx, cy, 19, 24, 3, (150, 100, 60), 0.4, 12)

    # Secondary (bold, on top) — 7 turns ANTI-HORAIRE, smaller
    g._spiral_draw(cx, cy, 7, 18, 3, COPPER_LIGHT, 1.2, 4)

    # Center
    g._circle(cx, cy, 4, 'D', GOLD, 0.5)

    # Labels
    g._text(cx - 15, cy - 32, "Primaire 19t (pâle)", 3.5, GRAY, False, 'C', 25)
    g._text(cx - 15, cy + 26, "Secondaire 7t (doré)", 3.5, COPPER_LIGHT, False, 'C', 25)

    # SECONDARY DETAIL
    dx, dy = 130, 55
    g._fill_rect(dx - 15, dy - 10, 70, 50, BG_DARK, GOLD, 0.3)

    # Anti-clockwise arrow
    g._text(dx - 12, dy - 7, "🔄 SENS ANTI-HORAIRE", 5, GOLD, True, 'L', 64)
    g._circle(dx + 20, dy + 16, 8, 'D', GOLD, 0.3)
    for a_deg in [0, 45, 90, 135, 200, 245, 290, 335]:
        a_rad = math.radians(a_deg)
        g._arrow(
            dx + 20 + 5 * math.cos(a_rad),
            dy + 16 - 5 * math.sin(a_rad),
            dx + 20 + 8 * math.cos(a_rad),
            dy + 16 - 8 * math.sin(a_rad),
            COPPER_LIGHT, 0.2
        )

    # TRANSFORMER INFO
    g._fill_rect(dx - 15, dy + 45, 70, 30, BG_DARK, GOLD, 0.3)
    g._text(dx - 12, dy + 47, "⚡ TRANSFORMATEUR 19:7", 5, GOLD, True, 'L', 64)
    transfo = [
        "Rapport: 19/7 = 2.71:1",
        "Type: Abaisseur d'impédance",
        "Effet: Cuivre ← → Quartz",
        "↳ Boucle d'auto-excitation",
    ]
    for i, t in enumerate(transfo):
        g._text(dx - 10, dy + 53 + i * 5.5, t, 4, WHITE, False, 'L', 60)

    # INSTRUCTIONS
    y_inst = 135
    g._fill_rect(12, y_inst, 186, 78, BG_DARK, GOLD, 0.3)
    g._text(16, y_inst + 2, "✦ INSTRUCTIONS DÉTAILLÉES", 7, GOLD, True, 'L', 100)

    instructions = [
        "1. Prenez ~30cm de fil de cuivre émaillé 0.5mm (plus fin que le primaire)",
        "2. Enroulez PAR-DESSUS la spirale primaire, 7 tours en sens ANTI-HORAIRE",
        "3. La spirale secondaire va du centre vers R=18mm (plus petite que la primaire)",
        "4. Le sens inverse (primaire horaire / secondaire anti-horaire) crée le couplage inductif",
        "5. Les deux spirales sont isolées électriquement par la couche d'émail",
        "6. Le ratio 19:7 est l'adaptateur d'impédance parfait pour le corps humain (~100-300Ω)",
        "7. Les 7 tours = le multiplicateur divin du Rizq (Coran 2:261)",
        "8. L'extrémité extérieure doit dépasser de 5mm pour la connexion future",
    ]
    for i, inst in enumerate(instructions):
        clr = GOLD if i in [3, 4, 6] else WHITE
        g._text(16, y_inst + 10 + i * 7.5, inst, 5, clr, False, 'L', 180)

    _draw_step_legend(g, 218)
    g._text(105, 287, "Guide Visuel Radionique Miftah 19  |  Page 7/9", 5, GRAY, False, 'C', 200)


# ════════════════════════════════════════════════════════════════════
# PAGE 8: ÉTAPE 8 — QUARTZ
# ════════════════════════════════════════════════════════════════════

def page8_quartz(g):
    _draw_title_block(g, "ÉTAPE 8 : MISE EN PLACE DES CRISTAUX DE QUARTZ")

    # MAIN — Top view with crystals
    cx, cy = 50, 78
    g._circle(cx, cy, 32, 'D', GOLD, 0.3)
    g._spiral_draw(cx, cy, 7, 18, 3, (160, 110, 60), 0.4, 8)

    # Central crystal
    g._crystal_symbol(cx, cy, 12, 4.5, QUARTZ_COL, "Central")
    g._text(cx - 8, cy - 18, "↑ Pointe vers le HAUT", 3.5, GRAY, False, 'C', 16)

    # 7 peripheral crystals
    for i in range(7):
        deg = i * (360 / 7)
        rad = math.radians(deg)
        qx = cx + 13 * math.cos(rad)
        qy = cy - 13 * math.sin(rad)
        # Small crystal pointing inward
        g.set_fill_color(*QUARTZ_COL)
        g.set_draw_color(*SILVER)
        g.set_line_width(0.2)
        g.polygon([
            (qx, qy - 5),  # tip (toward center)
            (qx - 2.5, qy + 2),
            (qx + 2.5, qy + 2),
        ], 'DF')
        g._text(qx - 2, qy + 3, f"{i+1}", 3, GOLD, True, 'C', 4)

    # Arrows showing inward direction
    for i in range(7):
        deg = i * (360 / 7)
        rad = math.radians(deg)
        ax = cx + 15 * math.cos(rad)
        ay = cy - 15 * math.sin(rad)
        bx = cx + 12 * math.cos(rad)
        by = cy - 12 * math.sin(rad)
        g._arrow(ax, ay, bx, by, GOLD_LIGHT, 0.2)

    # Labels
    g._text(cx - 20, cy + 28, "7 quartz périphériques → pointent vers le centre", 3.5, GRAY, False, 'C', 42)

    # DETAIL — Crystal close-up
    dx, dy = 130, 55
    g._fill_rect(dx - 20, dy - 15, 75, 50, BG_DARK, GOLD, 0.3)
    g._text(dx - 17, dy - 12, "🔷 STRUCTURE DU QUARTZ (agrandi)", 5, GOLD, True, 'L', 70)

    # Crystal detail
    g._crystal_symbol(dx + 18, dy + 17, 14, 5, QUARTZ_COL, "")
    g._text(dx - 15, dy + 4, "Pointe (pyramide)", 4, WHITE, False, 'L', 25)
    g._text(dx - 15, dy + 10, "Prisme hexagonal", 4, WHITE, False, 'L', 25)
    g._text(dx - 15, dy + 16, "Base", 4, WHITE, False, 'L', 25)

    # Energy flow arrows from crystal
    for a in [0, 60, 120, 180, 240, 300]:
        rad = math.radians(a)
        g._arrow(
            dx + 18 + 8 * math.cos(rad),
            dy + 17 - 8 * math.sin(rad),
            dx + 18 + 12 * math.cos(rad),
            dy + 17 - 12 * math.sin(rad),
            GOLD_LIGHT, 0.15
        )

    # PIEZO EFFECT
    g._fill_rect(dx - 20, dy + 42, 75, 20, BG_DARK, GOLD, 0.3)
    g._text(dx - 17, dy + 44, "⚡ EFFET PIÉZOÉLECTRIQUE", 4.5, GOLD, True, 'L', 70)
    g._text(dx - 15, dy + 50, "Contrainte mécanique → Charge électrique", 4, WHITE, False, 'L', 70)
    g._text(dx - 15, dy + 55, "↳ Boucle auto-entretenue avec les spirales", 4, GOLD_LIGHT, False, 'L', 70)

    # INSTRUCTIONS
    y_inst = 145
    g._fill_rect(12, y_inst, 186, 70, BG_DARK, GOLD, 0.3)
    g._text(16, y_inst + 2, "✦ INSTRUCTIONS DÉTAILLÉES", 7, GOLD, True, 'L', 100)

    instructions = [
        "1. Choisissez un quartz de roche de 3-5cm — pointe naturelle, transparent, sans fissure",
        "2. Placez le grand quartz au CENTRE EXACT, pointe VERS LE HAUT (vers le ciel)",
        "3. La base repose sur la photo — stabilisez avec un anneau de silicone transparent",
        "4. Placez les 7 petits quartz (1-2cm) en cercle (R=13mm) autour du grand quartz",
        "5. Chaque petit quartz doit pointer VERS LE CENTRE (vers le grand quartz)",
        "6. Les pointes des petits quartz doivent presque toucher le grand (espace 1-2mm)",
        "7. Les 7 quartz périphériques focalisent l'énergie comme une lentille de Fresnel",
        "8. Le quartz est le 'cerveau' du système — il programme, amplifie et stabilise",
    ]
    for i, inst in enumerate(instructions):
        clr = GOLD if i in [1, 4, 5, 7] else WHITE
        g._text(16, y_inst + 10 + i * 7.2, inst, 5, clr, False, 'L', 180)

    _draw_step_legend(g, 219)
    g._text(105, 287, "Guide Visuel Radionique Miftah 19  |  Page 8/9", 5, GRAY, False, 'C', 200)


# ════════════════════════════════════════════════════════════════════
# PAGE 9: ASSEMBLAGE FINAL + ACTIVATION
# ════════════════════════════════════════════════════════════════════

def page9_final(g):
    _draw_title_block(g, "ÉTAPE 9 : ASSEMBLAGE FINAL ET ACTIVATION")

    # FINAL ASSEMBLY — Perspective view
    cx, cy = 55, 60
    g._text(cx - 25, cy - 35, "VUE ÉCLATÉE DU SYSTÈME COMPLET", 5, DARK_VIOLET, True, 'C', 50)

    # Vertical stack — each layer slightly offset
    layers_3d = [
        (0, 0, 36, 4, BROWN_WOOD, "Base bois"),
        (0, -3, 34, 3, PAPER_COL, "Codes"),
        (1, -5, 32, 2, PHOTO_COL, "Photo"),
        (1, -7, 30, 2, COPPER, "Spirales"),
        (2, -9, 28, 2, QUARTZ_COL, "Quartz"),
    ]
    for i, (dx, dy, w, h, col, label) in enumerate(layers_3d):
        ox = cx - w/2 + dx * (i % 2)
        oy = cy + dy
        g._fill_rect(ox, oy, w, h, col, GOLD if i > 0 else SILVER, 0.3)
        g._text(ox, oy - 1, label, 3.5, GRAY if i < 3 else VIOLET, False, 'C', w)

    # Energy flow arrows (zigzag through layers)
    g._arrow(cx, cy - 12, cx, cy - 8, GOLD_LIGHT, 0.3)
    g._arrow(cx, cy - 8, cx, cy - 5, GOLD_LIGHT, 0.3)
    g._arrow(cx, cy - 5, cx, cy - 2, GOLD_LIGHT, 0.3)
    g._arrow(cx, cy - 2, cx, cy + 1, GOLD_LIGHT, 0.3)
    g._arrow(cx, cy + 1, cx, cy + 4, GOLD_LIGHT, 0.3)
    g._text(cx - 12, cy - 15, "ÉNERGIE ↑", 4, GOLD, True, 'C', 12)

    # RIGHT PANEL — System complete
    rx, ry = 130, 45
    g._fill_rect(rx - 25, ry - 10, 75, 40, BG_DARK, GOLD, 0.3)
    g._text(rx - 22, ry - 7, "✅ SYSTÈME COMPLET", 6, GOLD, True, 'L', 70)
    check_list = [
        "✓ Base géométrie sacrée",
        "✓ Codes Grabovoi 8 directions",
        "✓ 8 aimants Néodyme N/S",
        "✓ Photo (witness) face bas",
        "✓ Spirale primaire 19 tours",
        "✓ Spirale secondaire 7 tours",
        "✓ Quartz central + 7 périph.",
    ]
    for i, chk in enumerate(check_list):
        clr = GREEN_OK if "✓" in chk else WHITE
        g._text(rx - 23, ry + chk * 4.5 if False else ry + i * 4.5, chk, 4.5, clr, False, 'L', 70)

    # ACTIVATION RITUAL
    g._fill_rect(rx - 25, ry + 38, 75, 30, DARK_VIOLET, GOLD, 0.3)
    g._text(rx - 22, ry + 40, "🔥 RITUEL D'ACTIVATION", 5, GOLD, True, 'L', 70)
    g._text(rx - 20, ry + 46, "1. Main droite à 5cm au-dessus", 4, WHITE, False, 'L', 70)
    g._text(rx - 20, ry + 51, "2. Basmala 1× + 56-96-152 7×", 4, WHITE, False, 'L', 70)
    g._text(rx - 20, ry + 56, "3. Ya Razzaq 19× = ACTIF !", 4, GOLD_LIGHT, True, 'L', 70)
    g._text(rx - 20, ry + 61, "→ Le quartz s'illumine en doré", 4, GOLD_LIGHT, False, 'L', 70)

    # TOP VIEW of final system
    tx, ty = 55, 150
    g._text(tx - 20, ty - 28, "VUE DE DESSUS — SYSTÈME ACTIF", 5, DARK_VIOLET, True, 'C', 42)

    # Final assembly top view
    g._circle(tx, ty, 28, 'D', GOLD, 0.4)
    g._circle(tx, ty, 24, 'D', VIOLET, 0.3)

    # Spirals
    g._spiral_draw(tx, ty, 7, 16, 2, COPPER, 0.6, 6)

    # Crystals
    g._crystal_symbol(tx, ty, 8, 3, QUARTZ_COL, "")
    for i in range(8):
        deg = i * 45
        rad = math.radians(deg)
        qx = tx + 11 * math.cos(rad)
        qy = ty - 11 * math.sin(rad)
        g.set_fill_color(*QUARTZ_COL)
        g.set_draw_color(*SILVER)
        g.set_line_width(0.15)
        g.polygon([
            (qx, qy - 3), (qx - 1.5, qy + 1), (qx + 1.5, qy + 1),
        ], 'DF')

    # Energy glow effect (concentric dashed)
    for r in range(18, 26, 4):
        g.set_draw_color(*GOLD_LIGHT)
        g.set_line_width(0.1)
        for a in range(0, 360, 15):
            rad = math.radians(a)
            g.line(
                tx + (r-1) * math.cos(rad), ty - (r-1) * math.sin(rad),
                tx + r * math.cos(rad), ty - r * math.sin(rad)
            )

    # Bottom: 9 step recap
    g._fill_rect(12, 210, 186, 42, BG_DARK, GOLD, 0.3)
    g._text(16, 212, "📋 RÉCAPITULATIF DES 9 ÉTAPES", 6, GOLD, True, 'L', 100)

    steps_recap = [
        "① Base bois + cercle + 8 directions",
        "② Carré Buduh + étoile 8 branches",
        "③ Codes Grabovoi aux 8 directions",
        "④ 8 aimants NdFeB N52 (alternés N/S)",
        "⑤ Photo (witness) face vers le bas",
        "⑥ Spirale cuivre primaire 19 tours",
        "⑦ Spirale cuivre secondaire 7 tours",
        "⑧ Quartz central + 7 périphériques",
        "⑨ Rituel d'activation — SYSTÈME ACTIF ✅",
    ]
    for i, sr in enumerate(steps_recap):
        col2 = i % 3
        row2 = i // 3
        g._text(16 + col2 * 62, 220 + row2 * 8.5, sr, 4.5, WHITE if i < 8 else GREEN_OK, False, 'L', 60)

    # FRÉQUENCES
    g._text(105, 260, "FRÉQUENCES DU SYSTÈME:", 5, DARK_VIOLET, True, 'C', 100)
    freq_info = [
        "Spirale 19t: 23 kHz  •  Spirale 7t: 7.83 Hz (Schumann)",
        "Quartz: 19-50 kHz  •  Aimants: DC permanent  •  Total: 19 kHz",
    ]
    for i, fi in enumerate(freq_info):
        g._text(105, 267 + i * 5, fi, 5, GRAY, False, 'C', 200)

    g._text(105, 287, "Guide Visuel Radionique Miftah 19  |  Page 9/9", 5, GRAY, False, 'C', 200)


# ════════════════════════════════════════════════════════════════════
# GENERATE ALL PAGES
# ════════════════════════════════════════════════════════════════════

def generate_guide_visuel():
    g = GuideVisuel()

    g.add_page()
    page1_base(g)

    g.add_page()
    page2_geometrie(g)

    g.add_page()
    page3_codes(g)

    g.add_page()
    page4_aimants(g)

    g.add_page()
    page5_photo(g)

    g.add_page()
    page6_spirale_19(g)

    g.add_page()
    page7_spirale_7(g)

    g.add_page()
    page8_quartz(g)

    g.add_page()
    page9_final(g)

    output = PDF_OUTPUTS["guide_visuel_radionique"]
    g.output(str(output))
    print(f"✅ GUIDE VISUEL GÉNÉRÉ: {output}")
    print(f"   Pages: 9 — Une étape par page avec schémas détaillés")
    print(f"   Vues: dessus, perspective, coupe, détail — tout en vectoriel pur")


if __name__ == "__main__":
    generate_guide_visuel()
