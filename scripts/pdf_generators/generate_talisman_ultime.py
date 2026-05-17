#!/usr/bin/env python3
"""Talisman Ultime Miftah 19 — Synthese Coran + Kabbale + Grabovoi"""

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

# ── PALETTE ──
CREAM = (255, 250, 240)
MIDNIGHT = (12, 12, 42)
DARK_VIOLET = (75, 0, 130)
BRIGHT_VIOLET = (138, 43, 226)
GOLD = (218, 165, 32)
GOLD_LIGHT = (240, 210, 100)
DARK_BG = (40, 20, 60)
BLACK = (20, 20, 20)
GRAY = (100, 100, 100)


class TalismanPDF(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.add_font("L", "", LATIN, uni=True)
        self.add_font("L", "B", LATIN_B, uni=True)
        self.add_font("A", "", ARIAL, uni=True)
        self.set_auto_page_break(False)

    def txt_at(self, x, y, text, size=8, color=BLACK, align="C"):
        self.set_font("L", "", size)
        self.set_text_color(*color)
        self.set_xy(x, y)
        self.cell(0, 0, text, align=align)

    def txt_bold_at(self, x, y, text, size=8, color=BLACK, align="C"):
        self.set_font("L", "B", size)
        self.set_text_color(*color)
        self.set_xy(x, y)
        self.cell(0, 0, text, align=align)

    def txt_ar_at(self, x, y, text, size=9, color=BLACK, align="C"):
        self.set_font("A", "", size)
        self.set_text_color(*color)
        self.set_xy(x, y)
        self.cell(0, 0, ar(text), align=align)

    def txt_hb_at(self, x, y, text, size=9, color=BLACK, align="C"):
        self.set_font("A", "", size)
        self.set_text_color(*color)
        self.set_xy(x, y)
        self.cell(0, 0, hb(text), align=align)


def draw_talisman():
    pdf = TalismanPDF()
    pdf.add_page()

    pdf.set_fill_color(*CREAM)
    pdf.rect(0, 0, 210, 297, 'F')

    cx, cy = 105.0, 148.0

    # ═══════════════════ CERCLES CONCENTRIQUES ═══════════════════
    rings = [
        (90, GOLD, 0.7),
        (78, BRIGHT_VIOLET, 0.4),
        (66, GOLD, 0.4),
        (54, DARK_VIOLET, 0.5),
        (42, GOLD, 0.35),
        (28, BRIGHT_VIOLET, 0.35),
        (16, GOLD, 0.5),
    ]
    for r, col, lw in rings:
        pdf.set_draw_color(*col)
        pdf.set_line_width(lw)
        pdf.circle(cx, cy, r, 'D')

    # ═══════════════════ ETOILE A 8 BRANCHES ═══════════════════
    R_star = 50
    def px(deg):
        return cx + R_star * math.cos(math.radians(deg))
    def py(deg):
        return cy - R_star * math.sin(math.radians(deg))

    star_seq = [0, 135, 270, 45, 180, 315, 90, 225, 0]
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(1.0)
    for i in range(len(star_seq) - 1):
        pdf.line(px(star_seq[i]), py(star_seq[i]),
                 px(star_seq[i+1]), py(star_seq[i+1]))

    # Points aux 8 sommets
    for deg in range(0, 360, 45):
        pdf.set_fill_color(*DARK_VIOLET)
        pdf.set_draw_color(*GOLD)
        pdf.set_line_width(0.3)
        pdf.circle(px(deg), py(deg), 1.8, 'DF')

    # ═══════════════════ CENTRE : CARRE BUDUH ═══════════════════
    buduh = [["4", "9", "2"], ["3", "5", "7"], ["8", "1", "6"]]
    cw, ch = 8, 8
    bx0, by0 = cx - 12, cy - 12
    pdf.set_line_width(0.5)
    for i in range(3):
        for j in range(3):
            x, y = bx0 + j * cw, by0 + i * ch
            pdf.set_fill_color(*DARK_BG)
            pdf.set_draw_color(*GOLD)
            pdf.rect(x, y, cw, ch, 'DF')
            pdf.set_font("L", "B", 9)
            pdf.set_text_color(*GOLD)
            pdf.set_xy(x, y + 0.5)
            pdf.cell(cw, ch - 1, buduh[i][j], align="C")

    pdf.set_font("L", "B", 6)
    pdf.set_text_color(*GOLD)
    pdf.set_xy(bx0, by0 + 25)
    pdf.cell(24, 4, "BUDUH 3x3", align="C")

    # ═══════════════════ ANNEAU 1 : NOMS DIVINS (r=35) ══════════
    R1 = 35
    names = [
        (270, "\u064a\u0627 \u0631\u0632\u0627\u0642", "Razzaq", "319", "Le Pourvoyeur"),
        (0,   "\u064a\u0627 \u0641\u062a\u0627\u062d", "Fattah", "489", "L'Ouvreur"),
        (90,  "\u064a\u0627 \u063a\u0646\u064a",   "Ghani",  "1060", "Le Riche"),
        (180, "\u064a\u0627 \u0645\u063a\u0646\u064a", "Mughni", "1100", "L'Enrichisseur"),
    ]
    for deg, ar_text, latin, val, mean in names:
        r = math.radians(deg)
        x = cx + R1 * math.cos(r)
        y = cy - R1 * math.sin(r)
        off_x = -12 if deg == 180 else (-22 if deg == 270 else (8 if deg == 0 else 0))
        off_y = -22 if deg == 270 else (5 if deg == 90 else (0 if deg == 180 else -9))
        tx, ty = x + off_x, y + off_y

        pdf.set_fill_color(*MIDNIGHT)
        pdf.set_draw_color(*GOLD)
        pdf.set_line_width(0.3)
        pdf.rect(tx - 15, ty - 5, 32, 10, 'DF')

        pdf.set_font("A", "", 9)
        pdf.set_text_color(*GOLD)
        pdf.set_xy(tx - 14, ty - 4)
        pdf.cell(30, 5, ar(ar_text), align="C" if deg != 0 else "L")

        pdf.set_font("L", "", 5.5)
        pdf.set_text_color(*GOLD_LIGHT)
        pdf.set_xy(tx - 14, ty + 1.5)
        pdf.cell(30, 3, f"{latin} | Abjad {val}", align="C" if deg != 0 else "L")

    # ═══════════════════ ANNEAU 2 : GRABOVOI (r=48) ═════════════
    R2 = 48
    grab_data = [
        (315, "520 741 8",  "Argent inattendu (7+19+8)"),
        (45,  "318 798",    "Abondance (7, 36)"),
        (135, "318 612 518 714", "Cash-flow abondance"),
        (225, "9798733714615", "Manifester largent (33,61,97)"),
    ]
    for deg, code, label in grab_data:
        r = math.radians(deg)
        x = cx + R2 * math.cos(r)
        y = cy - R2 * math.sin(r)
        dx = [-20, 3, -20, -80][[315, 45, 135, 225].index(deg)]
        dy = [-8, -9, 7, 2][[315, 45, 135, 225].index(deg)]

        pdf.set_font("L", "B", 6.5)
        pdf.set_text_color(*DARK_VIOLET)
        pdf.set_xy(x + dx, y + dy)
        pdf.cell(0, 0, code, align="L")
        pdf.set_font("L", "", 5)
        pdf.set_text_color(*GRAY)
        pdf.set_xy(x + dx, y + dy + 4)
        pdf.cell(0, 0, label, align="L")

    # ═══════════════════ ANNEAU 3 : HEBREU (r=61) ═══════════════
    R3 = 61
    heb_data = [
        (270, "\u05e2\u05e9\u05e8",  "Osher", "570", "Richesse"),
        (315, "\u05e9\u05e4\u05e2",  "Shefa", "450", "Abondance"),
        (0,   "\u05de\u05de\u05d5\u05df","Mamon", "136", "Fortune"),
        (45,  "\u05e2\u05e9\u05d9\u05e8","Ashir", "580", "Riche"),
        (90,  "\u05d1\u05e8\u05db\u05d4","Berakhah","227","Benediction"),
        (135, "\u05e4\u05e8\u05e0\u05e1\u05d4","Parnassah","395","Subsistance"),
        (180, "\u05d7\u05d5\u05ea\u05dd \u05e9\u05dc\u05de\u05d4", "Hotam Shlomo","829","Sceau Salomon"),
        (225, "\u05d9\u05d4\u05d5\u05d4","YHWH", "26", "Tetragramme"),
    ]
    for deg, htext, latin, val, label in heb_data:
        r = math.radians(deg)
        x = cx + R3 * math.cos(r)
        y = cy - R3 * math.sin(r)
        offsets = {
            270: (-3, -10), 315: (3, -7), 0: (3, -2), 45: (3, 3),
            90: (-3, 6), 135: (-50, 3), 180: (-60, -2), 225: (-47, -7),
        }
        dx, dy = offsets[deg]
        pdf.set_font("A", "", 7.5)
        pdf.set_text_color(*DARK_VIOLET)
        pdf.set_xy(x + dx, y + dy)
        pdf.cell(0, 0, hb(htext), align="L")
        pdf.set_font("L", "", 5)
        pdf.set_text_color(*GRAY)
        pdf.set_xy(x + dx, y + dy + 4)
        pdf.cell(0, 0, f"{latin} {val}", align="L")

    # ═══════════════════ ANNEAU 4 : ARABE (r=73) ════════════════
    R4 = 73
    arab_segs = [
        (350, "\u0644\u0627 \u0625\u0644\u0647 \u0625\u0644\u0627 \u0627\u0644\u0644\u0647"),
        (320, "\u0627\u0644\u0645\u0644\u0643"),
        (290, "\u0627\u0644\u062d\u0642"),
        (260, "\u0627\u0644\u0645\u0628\u064a\u0646"),
        (230, "\u062e\u0627\u062a\u0645 \u0633\u0644\u064a\u0645\u0627\u0646"),
        (200, "\u0644\u0627 \u0625\u0644\u0647 \u0625\u0644\u0627 \u0627\u0644\u0644\u0647"),
        (170, "\u0627\u0644\u0645\u0644\u0643 \u0627\u0644\u062d\u0642"),
        (140, "\u0627\u0644\u0645\u0628\u064a\u0646"),
        (110, "\u062e\u0627\u062a\u0645 \u0633\u0644\u064a\u0645\u0627\u0646"),
        (80,  "\u0644\u0627 \u0625\u0644\u0647 \u0625\u0644\u0627 \u0627\u0644\u0644\u0647"),
        (50,  "\u0627\u0644\u0645\u0644\u0643"),
        (20,  "\u0627\u0644\u062d\u0642 \u0627\u0644\u0645\u0628\u064a\u0646"),
    ]
    for deg, seg in arab_segs:
        r = math.radians(deg)
        x = cx + R4 * math.cos(r)
        y = cy - R4 * math.sin(r)
        dx, dy = -10, -3
        if 300 < deg or deg < 60:
            dy = -8
        elif 60 <= deg <= 120:
            dx = 2
        elif 120 < deg < 240:
            dy = 4
        elif 240 <= deg <= 300:
            dx = -25

        pdf.set_font("A", "", 8)
        pdf.set_text_color(*BRIGHT_VIOLET)
        pdf.set_xy(x + dx, y + dy)
        pdf.cell(0, 0, ar(seg), align="C")

    # ═══════════════════ ANNEAU EXTERNE (r=86) ══════════════════
    R5 = 86
    outer_boxes = [
        (270, "56 96 152 = 19 x 8\nCODE AL-WAQI'A", True),
        (90,  "7 x 8 = 56  |  19 x 8 = 152\nTALISMAN ULTIUME MIFTAH 19", True),
        (0,   "520 741 8  =  7 + 19 + 8\nGRABOVOI - ARGENT INATTENDU", True),
        (180, "72 + 99 = 171 = 19 x 9\n72 NOMS HEBREUX + 99 NOMS ARABES", True),
    ]

    # Outer ring values between boxes
    outer_small = [
        (45,  "Hotam Shlomo"),
        (135, "Khatam Sulayman"),
        (225, "7  Rizq"),
        (315, "8  Directions"),
    ]
    for deg, txt in outer_small:
        r = math.radians(deg)
        x = cx + (R5 - 1) * math.cos(r)
        y = cy - (R5 - 1) * math.sin(r)
        pdf.set_font("L", "", 6)
        pdf.set_text_color(*GOLD)
        pdf.set_xy(x - 15, y - 2)
        pdf.cell(30, 0, txt, align="C")

    for deg, txt, is_main in outer_boxes:
        r = math.radians(deg)
        x = cx + R5 * math.cos(r)
        y = cy - R5 * math.sin(r)

        bw, bh = 60, 10
        bx, by_box = x - bw/2, y - bh/2

        pdf.set_fill_color(*MIDNIGHT)
        pdf.set_draw_color(*GOLD)
        pdf.set_line_width(0.3)
        pdf.rect(bx, by_box, bw, bh, 'DF')

        lines = txt.split("\n")
        for li, line in enumerate(lines):
            pdf.set_font("L", "B" if is_main else "", 6.5 if li == 0 else 5)
            pdf.set_text_color(*GOLD if li == 0 else GOLD_LIGHT)
            pdf.set_xy(bx, by_box + 0.5 + li * 5)
            pdf.cell(bw, 0, line, align="C")

    # ═══════════════════ TITRE ═══════════════════
    pdf.set_font("L", "B", 16)
    pdf.set_text_color(*DARK_VIOLET)
    pdf.set_xy(0, 18)
    pdf.cell(210, 8, "T A L I S M A N   U L T I M E   M I F T A H   1 9", align="C")

    pdf.set_font("L", "", 7.5)
    pdf.set_text_color(*GRAY)
    pdf.set_xy(0, 27)
    pdf.cell(210, 5, "Numerologie Coranique  |  Guematria Hebraique  |  Codes Grabovoi  |  Sceau de Salomon", align="C")

    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.3)
    pdf.line(30, 33, 180, 33)

    # ═══════════════════ LEGENDE ═══════════════════
    y_leg = 274
    leg_items = [
        ("Centre Buduh 3x3", DARK_VIOLET),
        ("Noms Divins (Razzaq, Fattah, Ghani, Mughni)", DARK_VIOLET),
        ("Codes Grabovoi (520 741 8...)", DARK_VIOLET),
        ("Etoile 8 branches", DARK_VIOLET),
        ("Guematria Hebraique (Osher, Shefa...)", DARK_VIOLET),
        ("Inscription Sceau Salomon (Arabe)", BRIGHT_VIOLET),
        ("Code Al-Waqi'a / 72+99 / Grabovoi", DARK_VIOLET),
        ("7  Rizq  |  8  Directions  |  19  Code", GOLD),
    ]
    pdf.set_xy(15, y_leg)
    col_widths = [95, 95]
    for idx, (text, col) in enumerate(leg_items):
        col_idx = idx // 4
        row_idx = idx % 4
        lx = 15 + col_idx * 100
        ly = y_leg + row_idx * 7
        pdf.set_fill_color(*col)
        pdf.set_xy(lx, ly)
        pdf.cell(3, 3, "", fill=True)
        pdf.set_font("L", "", 5.5)
        pdf.set_text_color(*BLACK)
        pdf.set_xy(lx + 4, ly - 0.5)
        pdf.cell(90, 3, text, align="L")

    # ═══════════════════ SAVE ═══════════════════
    output = PDF_OUTPUTS["talisman_ultime"]
    pdf.output(str(output))
    print(f"Talisman Ultime genere : {output}")
    print("Couches : 7 cercles | 8 branches | Buduh 3x3 | 4 traditions")


if __name__ == "__main__":
    draw_talisman()
