#!/usr/bin/env python3
"""
LE SECRET DU RIZQ
Version esoterique et experimentale — Edition Premium Luxe Orientale.

Ce document assume une lecture symbolique, numerologique et operative.
Il ne pretend pas etablir une preuve scientifique ni une exegese classique.
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

from core.project_paths import PDF_OUTPUTS, ensure_layout

ensure_layout()


def pick_font(*candidates: str) -> str:
    for raw in candidates:
        path = Path(raw)
        if path.exists():
            return str(path)
    raise FileNotFoundError(f"Font not found in candidates: {candidates}")


# Premium typography: Garamond for Latin, Arial fallback for Arabic
FONT_HEADING = pick_font(
    "C:/Windows/Fonts/GARABD.TTF",        # Garamond Bold
    "C:/Windows/Fonts/georgiab.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
)
FONT_BODY = pick_font(
    "C:/Windows/Fonts/GARA.TTF",           # Garamond Regular
    "C:/Windows/Fonts/georgia.ttf",
    "C:/Windows/Fonts/arial.ttf",
)
FONT_ITALIC = pick_font(
    "C:/Windows/Fonts/GARAIT.TTF",         # Garamond Italic
    "C:/Windows/Fonts/georgiai.ttf",
    "C:/Windows/Fonts/ariali.ttf",
)
FONT_ARABIC = pick_font(
    "C:/Windows/Fonts/arial.ttf",
)

# Premium Oriental Color Palette
C = {
    "parchment": (249, 244, 235),     # fond parchemin chaud
    "ivory":     (253, 250, 242),     # ivoire tres clair
    "cream":     (246, 240, 228),     # creme tiede
    "ink":       (44, 34, 28),        # encre brune profonde
    "ink_soft":  (88, 72, 60),        # encre adoucie
    "muted":     (140, 126, 110),     # texte tertiaire
    "gold":      (184, 142, 40),      # or riche
    "gold_light":(212, 178, 88),      # or clair
    "gold_pale": (235, 220, 175),     # or pale
    "gold_deep": (138, 98, 20),       # or profond
    "burgundy":  (98, 32, 48),        # bordeaux accent
    "burgundy_soft": (168, 82, 98),   # bordeaux adouci
    "rose":      (230, 195, 190),     # rose poudre pastel
    "rose_soft": (242, 220, 216),     # rose pastel clair
    "sage":      (195, 210, 190),     # vert sauge pastel
    "sage_soft": (218, 228, 214),     # vert sauge clair
    "sky":       (195, 210, 228),     # bleu ciel pastel
    "sky_soft":  (218, 228, 240),     # bleu ciel clair
    "lavender":  (212, 198, 222),     # lavande pastel
    "lavender_soft": (228, 218, 235), # lavande claire
    "dark_bg":   (26, 22, 18),        # fond sombre chaud
    "copper":    (172, 112, 58),      # cuivre
    "wine":      (72, 24, 36),        # lie de vin
}


RESHAPER = arabic_reshaper.ArabicReshaper(configuration={"support_ligatures": False})


def ar(text: str) -> str:
    return get_display(RESHAPER.reshape(text))


class Doc(FPDF):
    def __init__(self) -> None:
        super().__init__("P", "mm", "A4")
        self.add_font("H", "", FONT_HEADING)
        self.add_font("B", "", FONT_BODY)
        self.add_font("B", "B", FONT_HEADING)
        self.add_font("B", "I", FONT_ITALIC)
        self.add_font("Ar", "", FONT_ARABIC)
        self.set_auto_page_break(True, 18)
        self.header_title = ""
        self.header_subtitle = ""
        self.skip_header = False
        self.set_title("Le Secret du Rizq — Edition Premium")
        self.set_author("Codex")
        self.set_creator("CORAN NUM TAL")
        self._ornament_y = 0

    def header(self) -> None:
        if self.skip_header:
            return
        # Gold decorative line at top
        self.set_draw_color(*C["gold_light"])
        self.set_line_width(0.6)
        self.line(12, 12, 198, 12)
        self.set_draw_color(*C["gold"])
        self.set_line_width(0.3)
        self.line(12, 13.5, 198, 13.5)
        # Title
        self.set_font("B", "B", 8.5)
        self.set_text_color(*C["gold_deep"])
        self.set_xy(14, 15.5)
        self.cell(182, 5, self.header_title, align="C")
        if self.header_subtitle:
            self.set_font("B", "I", 6.5)
            self.set_text_color(*C["muted"])
            self.set_xy(14, 20.5)
            self.cell(182, 4, self.header_subtitle, align="C")
        self.ln(18)

    def footer(self) -> None:
        if self.skip_header:
            return
        self.set_y(-14)
        self.set_draw_color(*C["gold_light"])
        self.set_line_width(0.4)
        self.line(12, self.get_y(), 198, self.get_y())
        self.set_y(-10)
        self.set_font("B", "I", 6)
        self.set_text_color(*C["muted"])
        self.cell(0, 4, f"Le Secret du Rizq  |  Edition Premium Luxe  |  p. {self.page_no()}", align="C")

    def set_context(self, title: str, subtitle: str = "") -> None:
        self.header_title = title
        self.header_subtitle = subtitle

    # --- Decorative drawing helpers ---

    def ornament_divider(self, y: float) -> float:
        """Elegant gold divider with center diamond."""
        self.set_draw_color(*C["gold_light"])
        self.set_line_width(0.3)
        self.line(24, y, 88, y)
        self.line(122, y, 186, y)
        # Center diamond
        cx, cy_ = 105, y
        d = 2.5
        self.set_fill_color(*C["gold"])
        self.set_draw_color(*C["gold"])
        self.set_line_width(0.3)
        diamond = [(cx, cy_ - d), (cx + d, cy_), (cx, cy_ + d), (cx - d, cy_)]
        self.polygon(diamond, "DF")
        return y + 5

    def page_border(self) -> None:
        """Delicate gold frame around the page."""
        self.set_draw_color(*C["gold_light"])
        self.set_line_width(0.25)
        self.rect(10, 10, 190, 277, "D")
        self.set_draw_color(*C["gold_pale"])
        self.set_line_width(0.15)
        self.rect(11.5, 11.5, 187, 274, "D")

    def corner_ornament(self, x: float, y: float, size: float = 4) -> None:
        """Small decorative square at corners."""
        self.set_fill_color(*C["gold"])
        self.set_draw_color(*C["gold"])
        self.set_line_width(0.2)
        self.rect(x - size/2, y - size/2, size, size, "DF")

    def heading_block(self, y: float, title: str, subtitle: str = "") -> float:
        """Premium section heading with ornamental frame."""
        # Top gold bar
        self.set_fill_color(*C["gold"])
        self.set_draw_color(*C["gold"])
        self.rect(18, y, 174, 1.2, "F")
        self.set_fill_color(*C["gold_light"])
        self.rect(18, y + 1.2, 174, 10.5, "F")
        # Title
        self.set_font("B", "B", 10)
        self.set_text_color(*C["ink"])
        self.set_xy(22, y + 1.5)
        self.cell(166, 6, title)
        if subtitle:
            self.set_font("B", "I", 7)
            self.set_text_color(*C["gold_deep"])
            self.set_xy(22, y + 7)
            self.cell(166, 4, subtitle)
        # Bottom accent
        self.set_draw_color(*C["gold"])
        self.set_line_width(0.25)
        self.line(18, y + 12, 192, y + 12)
        return y + 16

    def sub_heading(self, y: float, title: str) -> float:
        """Refined sub-heading with gold accent."""
        self.set_fill_color(*C["gold"])
        self.rect(22, y + 2.5, 3, 3.5, "F")
        self.set_font("B", "B", 8.5)
        self.set_text_color(*C["burgundy"])
        self.set_xy(29, y + 1)
        self.cell(160, 6, title)
        return y + 9

    # --- Basic text methods ---

    def t(self, x: float, y: float, txt: str, size: float = 8, bold: bool = False,
          color=C["ink"], align: str = "L", w: float = 50) -> None:
        self.set_font("B", "B" if bold else "", size)
        self.set_text_color(*color)
        self.set_xy(x, y)
        self.cell(w, 5, txt, align=align)

    def t_ar(self, x: float, y: float, txt: str, size: float = 13,
             color=C["gold"], align: str = "C", w: float = 50) -> None:
        self.set_font("Ar", "", size)
        self.set_text_color(*color)
        self.set_xy(x, y)
        self.cell(w, 6, ar(txt), align=align)

    def p(self, y: float, txt: str, size: float = 8.2, color=C["ink"],
          bold: bool = False, x: float = 22, w: float = 168,
          align: str = "L", lh: float | None = None) -> float:
        if lh is None:
            lh = size * 0.78 + 1.5
        self.set_font("B", "B" if bold else "", size)
        self.set_text_color(*color)
        self.set_xy(x, y)
        self.multi_cell(w, lh, txt, align=align)
        return self.get_y()

    def bullets(self, y: float, items: list[str], size: float = 7.5,
                color=C["ink"]) -> float:
        for item in items:
            y = self.p(y, f"+  {item}", size=size, color=color)
            y += 0.8
        return y

    def ornate_box(self, y: float, title: str, lines: list[str],
                   accent_color=C["gold"], bg_color=C["ivory"],
                   line_size: float = 6.2) -> float:
        """Premium framed box with gold border and pastel interior."""
        h = 9 + len(lines) * 5.5 + 2
        # Shadow / outer glow
        self.set_fill_color(*bg_color)
        self.set_draw_color(*accent_color)
        self.set_line_width(0.4)
        self.rect(18, y, 174, h, "DF")
        # Left gold accent bar
        self.set_fill_color(*C["gold"])
        self.rect(18, y, 1.8, h, "F")
        # Title
        self.t(24, y + 1.5, title, 8, True, C["burgundy"], "L", 160)
        ty = y + 7.5
        for line in lines:
            self.t(24, ty, line, line_size, False, C["ink_soft"], "L", 164)
            ty += 5.5
        return y + h + 4

    def insight_box(self, y: float, number: str, title: str, formula: str,
                    reading: str, bg=C["rose_soft"]) -> float:
        """Premium insight portal with numbered gate."""
        h = 24
        self.set_fill_color(*bg)
        self.set_draw_color(*C["gold_light"])
        self.set_line_width(0.35)
        self.rect(18, y, 174, h, "DF")
        # Number badge
        self.set_fill_color(*C["gold"])
        badge_x, badge_y = 22, y + 1.5
        self.rect(badge_x, badge_y, 8, 7, "F")
        self.t(badge_x, badge_y + 0.5, number, 7, True, C["ivory"], "C", 8)
        # Title
        self.t(33, y + 1.5, title, 8, True, C["burgundy"], "L", 152)
        # Formula
        self.t(33, y + 7.5, formula, 6.5, False, C["gold_deep"], "L", 152)
        # Reading
        self.p(y + 12, reading, 6.3, C["ink_soft"], False, 33, 154)
        return max(y + h + 3, self.get_y() + 3)

    # --- Mandala / geometric drawing ---

    def draw_8point_star(self, cx: float, cy: float, r1: float, r2: float,
                          color1=None, color2=None, lw1: float = 0.6, lw2: float = 0.4) -> None:
        """Elegant 8-pointed star mandala."""
        c1 = color1 or C["gold"]
        c2 = color2 or C["gold_light"]
        for r, c, lw in [(r1, c1, lw1), (r2, c2, lw2)]:
            self.set_draw_color(*c)
            self.set_line_width(lw)
            for i in range(8):
                a1 = math.radians(45 * i - 90)
                a2 = math.radians(45 * i + 45 - 90)
                x1 = cx + r * math.cos(a1)
                y1 = cy - r * math.sin(a1)
                x2 = cx + r * math.cos(a2)
                y2 = cy - r * math.sin(a2)
                self.line(x1, y1, x2, y2)

    def draw_ornament_circle(self, cx: float, cy: float, r: float, n: int = 12) -> None:
        """Circle of small gold dots."""
        for i in range(n):
            ang = math.radians(360 / n * i)
            dx = cx + r * math.cos(ang)
            dy = cy - r * math.sin(ang)
            self.set_fill_color(*C["gold"])
            self.circle(dx, dy, 0.6, "F")

    def draw_mandala_bg(self, cx: float, cy: float, max_r: float) -> None:
        """Complex geometric mandala for cover/title pages."""
        # Outer rings
        for r, lw, c in [(max_r, 0.5, C["gold"]), (max_r * 0.82, 0.3, C["gold_light"]),
                          (max_r * 0.64, 0.25, C["gold"]), (max_r * 0.46, 0.2, C["gold_light"])]:
            self.set_draw_color(*c)
            self.set_line_width(lw)
            self.circle(cx, cy, r, "D")
        # 8-pointed stars
        self.draw_8point_star(cx, cy, max_r * 0.72, max_r * 0.54, lw1=0.5, lw2=0.3)
        # Connecting rays
        self.set_draw_color(*C["gold_light"])
        self.set_line_width(0.2)
        for i in range(16):
            ang = math.radians(22.5 * i - 90)
            x = cx + max_r * math.cos(ang)
            y = cy - max_r * math.sin(ang)
            self.line(cx, cy, x, y)
        # Dot circles
        self.draw_ornament_circle(cx, cy, max_r * 0.9, 16)


# ============================================================
# CONTENT DATA (unchanged)
# ============================================================

ROOTS = [
    ("RZQ", "123", "champ lexical du rizq, de la provision et de la subsistance"),
    ("SHKR", "75", "gratitude, reconnaissance, activation de l'augmentation"),
    ("BRK", "32", "baraka, stabilisation et benediction du flux"),
    ("WQY", "258", "taqwa, protection vibratoire et garde interieure"),
]


PHI_PORTS = [
    {
        "number": "1",
        "title": "Le corridor Saba -> Rahman",
        "formula": f"34 x phi = {34 * PHI:.4f} -> 55",
        "reading": (
            "Saba (34) parle de prosperite et de gratitude. Al-Rahman (55) deverse les faveurs. "
            "34 et 55 sont deux marches consecutives du corridor de Fibonacci."
        ),
    },
    {
        "number": "2",
        "title": "Le corridor Rahman -> Fajr",
        "formula": f"55 x phi = {55 * PHI:.4f} -> 89",
        "reading": (
            "Al-Rahman (55) et Al-Fajr (89) prolongent le meme axe. Le secret n'est pas seulement "
            "d'obtenir la richesse, mais de voir clair sur ce qu'elle signifie."
        ),
    },
    {
        "number": "3",
        "title": "La matrice des 4 noms",
        "formula": f"19 x 4 = 76 ; 76 x phi = {76 * PHI:.4f} -> 123",
        "reading": (
            "Le code 19 applique a 4 noms du rizq produit 76. Multiplie par phi, il touche la racine "
            "du rizq comptee a 123 occurrences dans la lecture numerologique du corpus."
        ),
    },
    {
        "number": "4",
        "title": "Le cycle operatif",
        "formula": f"61 x phi = {61 * PHI:.4f} -> 99",
        "reading": (
            "Le cycle 1 + 7 + 19 + 33 + 1 = 61 devient par phi une porte vers 99, nombre total "
            "des Noms divins utilises comme horizon vibratoire."
        ),
    },
    {
        "number": "5",
        "title": "Le coeur cache de la misericorde",
        "formula": f"329 + 289 = 618 ; 618 x phi = {618 * PHI:.4f} -> 1000",
        "reading": (
            "Le couple Al-Rahman + Al-Rahim donne 618, echo direct du nombre d'or inverse 0.618. "
            "Cette porte est la plus forte du systeme reconstruit."
        ),
    },
    {
        "number": "6",
        "title": "Basmala et Fattah",
        "formula": f"786 / phi = {786 / PHI:.4f} approx 489",
        "reading": (
            "La Basmala ouvre le champ. Fattah, pris en abjad simple sans le ya d'appel, vaut 489. "
            "Le rapport n'est pas exact, mais il forme une resonance operatoire utile."
        ),
    },
]


GRABOVOI_CODES = [
    (
        "123 55 89",
        "Corridor phi du rizq",
        "123 = rizq ; 55 = Rahman ; 89 = Fajr",
        "A utiliser quand tu veux ouvrir, recevoir, puis clarifier l'intention.",
    ),
    (
        "786 489 618",
        "Porte d'ouverture misericordieuse",
        "786 = Basmala ; 489 = Fattah ; 618 = Rahman + Rahim",
        "Code d'entree avant dhikr, talisman ou montage radionique.",
    ),
    (
        "6119 078",
        "Cycle operatif complet",
        "61 = rituel ; 19 = code ; 07 = multiplication ; 8 = directions",
        "Code de stabilisation pour les pratiques sur 7 ou 21 jours.",
    ),
    (
        "319 489 618 786",
        "Echelle integrale du flux",
        "Ya Razzaq -> Fattah -> Rahman/Rahim -> Basmala",
        "Code de montee progressive : appel, ouverture, effusion, sceau.",
    ),
    (
        "307 123 786",
        "Racine -> manifestation -> porte",
        "307 = abjad de rizq ; 123 = occurrences ; 786 = ouverture",
        "Code de concretisation materielle et mentale.",
    ),
]


DHIKRS = [
    (
        "Dhikr A  |  Matrice 76",
        "19x Ya Razzaq + 19x Ya Fattah + 19x Ya Ghani + 19x Ya Mughni",
        "Structure minimale pour appeler les 4 piliers du flux.",
    ),
    (
        "Dhikr B  |  Cycle 61",
        "1 Basmala + 7 Istighfar + 19 Ya Razzaq + 33 Salawat + 1 Sceau",
        "Cycle rituel complet ; excellent avant le sommeil ou avant un travail important.",
    ),
    (
        "Dhikr C  |  Corridor 34-55-89",
        "34x gratitude + 55x Ya Rahman + 89 respirations conscientes",
        "Travail sur la conscience de l'abondance avant sa manifestation externe.",
    ),
    (
        "Dhikr D  |  Porte 618",
        "61x Ya Rahman + 8x Ya Rahim ou 34x/55x selon ton ressenti",
        "Utilise quand le coeur est ferme et que le flux materiel est bloque.",
    ),
]


RADIONIC = [
    "Spirale primaire : 7 tours en cuivre.",
    "Longueur conseillee : 61.8 cm pour signer la porte 618.",
    "Centre : ecrire 786 489 618 en triangle ou en spirale.",
    "Anneau externe : 8 directions avec 55, 89, 123, 319, 489, 618, 786, 99.",
    "Quartz ou pierre claire au centre si tu travailles en montage physique.",
    "Activation : 1 cycle Dhikr B par jour sur 7, 14 ou 21 jours.",
]


SOURCES = [
    "Quranic Arabic Corpus — root rizq : corpus.quran.com/qurandictionary.jsp?root=rzq",
    "Quranic Arabic Corpus — root baraka : corpus.quran.com/qurandictionary.jsp?q=brk",
    "Study Quran Arabic — root shukr : studyquranarabic.com",
    "Quranic Arabic Corpus — root waqa : corpus.quran.com/qurandictionary.jsp?q=wqy",
    "Verses portes : 2:261, 7:96, 14:7, 34:15, 51:58, 62:10, 65:2-3, 71:10-12, 89:15-20",
]


# ============================================================
# PAGES
# ============================================================

def add_cover(pdf: Doc) -> None:
    pdf.skip_header = True
    pdf.add_page()
    # Full dark background
    pdf.set_fill_color(*C["dark_bg"])
    pdf.rect(0, 0, 210, 297, "F")

    # Mandala background
    pdf.draw_mandala_bg(105, 145, 82)

    # Central emblem circle
    pdf.set_fill_color(*C["dark_bg"])
    pdf.set_draw_color(*C["gold"])
    pdf.set_line_width(0.6)
    pdf.circle(105, 145, 32, "DF")

    # Inner design
    pdf.draw_8point_star(105, 145, 28, 20, lw1=0.5, lw2=0.35)
    pdf.set_fill_color(*C["gold"])
    pdf.set_draw_color(*C["gold"])
    pdf.circle(105, 145, 5, "DF")

    # Title block
    y = 190
    pdf.set_fill_color(*C["gold"])
    pdf.set_draw_color(*C["gold"])
    pdf.rect(30, y, 150, 1.8, "F")
    y += 8
    pdf.set_font("B", "B", 26)
    pdf.set_text_color(*C["gold"])
    pdf.set_xy(15, y)
    pdf.cell(180, 9, "LE SECRET DU RIZQ", align="C")
    y += 13
    pdf.set_font("B", "I", 10.5)
    pdf.set_text_color(*C["gold_light"])
    pdf.set_xy(15, y)
    pdf.cell(180, 6, "Phi  ·  Abjad  ·  Grabovoi  ·  Radionique Sacree", align="C")
    y += 10
    pdf.set_font("Ar", "", 18)
    pdf.set_text_color(*C["gold"])
    pdf.set_xy(15, y)
    pdf.cell(180, 8, ar("بسم الله الرحمن الرحيم"), align="C")
    y += 13
    pdf.set_draw_color(*C["gold_light"])
    pdf.set_line_width(0.3)
    pdf.line(60, y, 150, y)
    y += 7
    pdf.set_font("B", "I", 8)
    pdf.set_text_color(*C["muted"])
    pdf.set_xy(15, y)
    pdf.cell(180, 5, "Edition Premium Luxe Orientale", align="C")
    y += 12

    # Key numbers
    keys = ["19 x 4 x phi -> 123", "329 + 289 = 618", "786 / phi approx 489", "34 -> 55 -> 89", "61 x phi -> 99"]
    for key in keys:
        pdf.set_font("B", "", 7.2)
        pdf.set_text_color(*C["gold_light"])
        pdf.set_xy(50, y)
        pdf.cell(130, 4.5, "+  " + key)
        y += 5.5

    y += 6
    pdf.set_font("B", "I", 7)
    pdf.set_text_color(*C["muted"])
    pdf.set_xy(15, y)
    pdf.cell(180, 5, "CORAN NUM TAL  ·  " + "2026", align="C")

    # Corner ornaments
    pdf.corner_ornament(16, 16, 5)
    pdf.corner_ornament(194, 16, 5)
    pdf.corner_ornament(16, 281, 5)
    pdf.corner_ornament(194, 281, 5)

    pdf.skip_header = False


def page_prelim(pdf: Doc) -> None:
    pdf.set_context("PREAMBULE", "Lecture mystique, operative et hors materialisme scientifique")
    pdf.add_page()
    pdf.page_border()
    y = 24
    y = pdf.heading_block(y, "I.  LE FIL CONDUCTEUR DU SECRET", "Fondements et methode de lecture")
    y = pdf.p(
        y,
        "Dans cette reconstruction, la richesse n'est pas seulement monetaire. Elle est comprise comme "
        "flux de rizq, ouverture des causes, intensification de la baraka et descente d'une permission "
        "subtile. Le nombre d'or n'est pas traite ici comme demonstration academique, mais comme cle "
        "de passage entre des nombres coraniques, des valeurs abjad, des sequences Fibonacci et des "
        "codes de travail operatif.",
        8.2,
    )
    y = pdf.p(
        y,
        "Le projet repose sur trois plans : 1) le texte sacre et ses nombres, 2) les resonances "
        "abjad et gematriques, 3) l'application pratique par le dhikr, le talisman et la radionique.",
        7.8,
    )
    y = pdf.ornate_box(
        y + 2,
        "Avertissement de methode",
        [
            "Mode de lecture : esoterique et experimental.",
            "But : construire une architecture interieure coherente, pas un papier scientifique.",
            "Les nombres exacts sont gardes quand ils sont simples ; les resonances sont assumees comme symboliques.",
            "Le montage final doit servir la conscience, l'intention et la pratique.",
        ],
        accent_color=C["burgundy"],
        bg_color=C["rose_soft"],
    )
    y = pdf.heading_block(y + 2, "II.  LES PORTES TEXTUELLES DU RIZQ", "Ancrages scripturaires du flux")
    y = pdf.bullets(
        y,
        [
            "51:58 — Ar-Razzaq, la source pure du rizq.",
            "65:2-3 — taqwa + tawakkul = ouverture d'une issue et provision inattendue.",
            "71:10-12 — istighfar = pluie, biens et renforcement du champ familial.",
            "14:7 — gratitude = augmentation.",
            "2:261 et 34:39 — depense juste = multiplication et remplacement du flux.",
            "89:15-20 — la richesse n'est pas une preuve automatique d'honneur.",
        ],
        7.5,
    )


def page_matrix(pdf: Doc) -> None:
    pdf.set_context("MATRICE DU RIZQ", "Racines, abjad et architecture numerique")
    pdf.add_page()
    pdf.page_border()
    y = 24
    y = pdf.heading_block(y, "III.  LES NOMBRES-SOUCHES", "Le noyau dur du systeme numerique")
    y = pdf.ornate_box(
        y,
        "Noyau du systeme",
        [
            "19  = code coranique",
            "7   = multiplication, croissance, expansion",
            "8   = directions, diffusion, etoile operatoire",
            "61  = cycle complet du rituel",
            "76  = 19 x 4, matrice des 4 noms",
            "99  = horizon complet des Noms divins",
            "123 = root rizq",
            "307 = abjad de rizq",
            "319 = abjad de Ya Razzaq",
            "489 = abjad simple de Fattah",
            "618 = Al-Rahman + Al-Rahim",
            "786 = Basmala",
        ],
        accent_color=C["gold"],
        bg_color=C["sage_soft"],
        line_size=6.2,
    )
    y = pdf.ornate_box(
        y,
        "Formes arabes-souches (transliteration)",
        [
            "Rizq       — al-rizq",
            "Ya Razzaq  — invocation de l'Ouvreur",
            "Fattah     — al-Fattah",
            "Rahman     — al-Rahman",
            "Rahim      — al-Rahim",
        ],
        accent_color=C["burgundy"],
        bg_color=C["rose_soft"],
        line_size=6.2,
    )
    # Arabic rendering below
    y_offset = y
    pdf.set_font("Ar", "", 11)
    pdf.set_text_color(*C["gold"])
    for label in ["رزق", "يا رزاق", "فتاح", "الرحمن", "الرحيم"]:
        pdf.set_xy(24, y_offset)
        pdf.cell(164, 6, ar(label), align="R")
        y_offset += 5.5
    y = y_offset + 3
    y = pdf.sub_heading(y, "Racines textuelles activees dans le champ")
    root_lines = [f"{root}  ->  {count} occurrences  |  {meaning}" for root, count, meaning in ROOTS]
    y = pdf.ornate_box(y, "Index de travail", root_lines, accent_color=C["gold"], bg_color=C["sky_soft"], line_size=6.2)
    y = pdf.sub_heading(y, "Lecture centrale")
    y = pdf.p(
        y,
        "Le pivot le plus fort n'est pas 684 mais 618. Le couple Al-Rahman + Al-Rahim ouvre une porte "
        "nettement plus pure vers phi que l'ancienne version du projet. Cela recentre l'abondance "
        "sur la misericorde avant la capture materielle.",
        7.8,
    )


def page_phi(pdf: Doc) -> None:
    pdf.set_context("PORTES PHI", "Les resonances dorees du systeme reconstruit")
    pdf.add_page()
    pdf.page_border()
    y = 24
    y = pdf.heading_block(y, "IV.  LES 6 PORTES DU NOMBRE D'OR", "Architecture phi du systeme")
    for port in PHI_PORTS:
        bg = [C["rose_soft"], C["sage_soft"], C["sky_soft"], C["lavender_soft"], C["rose_soft"], C["sage_soft"]][int(port["number"]) - 1]
        y = pdf.insight_box(y, port["number"], port["title"], port["formula"], port["reading"], bg=bg)


def page_fib(pdf: Doc) -> None:
    pdf.set_context("CORRIDOR FIBONACCI", "De Saba a Rahman, puis de Rahman a Fajr")
    pdf.add_page()
    pdf.page_border()
    y = 24
    y = pdf.heading_block(y, "V.  LE FIL 34 → 55 → 89", "Le corridor dore de l'abondance")
    y = pdf.ornate_box(
        y,
        "Lecture numerique",
        [
            f"34 / 21 = {34/21:.6f}  |  seuil de preparation",
            f"55 / 34 = {55/34:.6f}  |  phi montant",
            f"89 / 55 = {89/55:.6f}  |  phi montant",
            "144 = 55 + 89  |  fermeture du corridor",
            "56 = 55 + 1     |  Waqi'a comme bascule dans le plan manifeste",
        ],
        accent_color=C["gold"],
        bg_color=C["sky_soft"],
    )
    y = pdf.sub_heading(y, "Lecture mystique du corridor")
    y = pdf.bullets(
        y,
        [
            "Saba 34 : le peuple prospere, puis perd la baraka quand la gratitude se brise.",
            "Al-Rahman 55 : les faveurs se multiplient et deviennent visibles.",
            "Al-Waqi'a 56 : la misericorde entre dans le champ des destinees et des parts.",
            "Al-Fajr 89 : le voile tombe ; richesse et restriction sont des epreuves.",
        ],
        7.5,
    )
    y = pdf.p(
        y,
        "Le corridor ne dit pas seulement comment attirer. Il dit aussi comment ne pas se perdre "
        "dans l'attraction. Sans gratitude, le flux se fissure. Sans lucidite, la richesse devient test.",
        7.8,
    )


def page_grabovoi(pdf: Doc) -> None:
    pdf.set_context("CODES DE RECHERCHE", "Grabovoi coranique et sequences de passage")
    pdf.add_page()
    pdf.page_border()
    y = 24
    y = pdf.heading_block(y, "VI.  CODES GRABOVOI RECONSTRUITS", "Sequences de passage et d'activation")
    pastels = [C["sage_soft"], C["rose_soft"], C["sky_soft"], C["lavender_soft"], C["rose_soft"]]
    for i, (code, title, comp, use) in enumerate(GRABOVOI_CODES):
        y = pdf.ornate_box(
            y,
            f"Code : {code}  |  {title}",
            [
                f"Composition : {comp}",
                f"Usage : {use}",
            ],
            accent_color=C["gold"],
            bg_color=pastels[i],
            line_size=6.2,
        )
    y = pdf.p(
        y,
        "Conseil operatif : lis le code lentement, chiffre par chiffre, puis laisse-le se compacter "
        "dans le coeur ou entre les sourcils. Le code ne remplace pas le dhikr ; il sert d'adresse.",
        7.5,
    )


def page_dhikr(pdf: Doc) -> None:
    pdf.set_context("DHIKR OPERATIF", "Cycles de repetition, ouverture et fixation du flux")
    pdf.add_page()
    pdf.page_border()
    y = 24
    y = pdf.heading_block(y, "VII.  DHIKR, NOMBRE ET INTENTION", "Cycles pratiques de travail vibratoire")
    pastels = [C["sage_soft"], C["rose_soft"], C["sky_soft"], C["lavender_soft"]]
    for i, (title, structure, sense) in enumerate(DHIKRS):
        y = pdf.ornate_box(
            y,
            title,
            [
                f"Structure : {structure}",
                f"Fonction : {sense}",
            ],
            accent_color=C["burgundy"],
            bg_color=pastels[i],
            line_size=6.2,
        )
    y = pdf.sub_heading(y, "Sceau verbal conseille")
    y = pdf.p(
        y,
        "Finir chaque session par : Bismillah, tawakkaltu 'ala Allah, wa ma bika min ni'matin fa-min Allah. "
        "L'objectif est de relier l'appel du flux a sa Source, pour eviter l'avidite brute.",
        7.5,
    )


def page_talisman(pdf: Doc) -> None:
    pdf.set_context("TALISMAN PHI", "Sceau contemplatif du rizq et des 8 directions")
    pdf.add_page()
    pdf.page_border()
    y = 24
    y = pdf.heading_block(y, "VIII.  TALISMAN ESOTERIQUE DU RIZQ", "Carte contemplative et condensateur symbolique")
    y = pdf.p(
        y,
        "Le talisman ci-dessous est propose comme carte contemplative et support de focalisation. "
        "Il n'est pas presente comme objet dogmatique mais comme condensateur symbolique du projet.",
        7.8,
    )
    cx, cy = 105, 135

    # Background mandala for talisman
    pdf.draw_mandala_bg(cx, cy, 62)

    # Center
    pdf.set_fill_color(*C["ivory"])
    pdf.set_draw_color(*C["gold"])
    pdf.set_line_width(0.5)
    pdf.circle(cx, cy, 18, "DF")
    pdf.set_font("B", "B", 15)
    pdf.set_text_color(*C["burgundy"])
    pdf.set_xy(cx - 20, cy - 7)
    pdf.cell(40, 7, "618", align="C")
    pdf.set_font("B", "I", 6.5)
    pdf.set_text_color(*C["gold_deep"])
    pdf.set_xy(cx - 40, cy + 3)
    pdf.cell(80, 5, "Rahman + Rahim", align="C")

    # Ring of 8 values
    ring = [
        (90, "55"),
        (45, "89"),
        (0, "123"),
        (315, "319"),
        (270, "489"),
        (225, "61"),
        (180, "99"),
        (135, "786"),
    ]
    for deg, value in ring:
        rad = math.radians(deg)
        x = cx + 48 * math.cos(rad)
        yv = cy - 48 * math.sin(rad)
        pdf.set_fill_color(*C["ivory"])
        pdf.set_draw_color(*C["gold_light"])
        pdf.set_line_width(0.3)
        pdf.rect(x - 10, yv - 5, 20, 10, "DF")
        pdf.set_font("B", "B", 7.5)
        pdf.set_text_color(*C["ink"])
        pdf.set_xy(x - 10, yv - 3)
        pdf.cell(20, 5, value, align="C")

    y = 210
    y = pdf.ornate_box(
        y,
        "Usage du talisman",
        [
            "Centre 618 : misericorde source du flux.",
            "Est 123 : materialisation du rizq.   Sud 489 : ouverture des portes.",
            "Ouest 99 : completude du champ divin.   Nord 55 : rappel de Rahman.",
            "Porter, poser sous un carnet de travail ou utiliser comme support de visualisation.",
        ],
        accent_color=C["gold"],
        bg_color=C["sage_soft"],
        line_size=6,
    )


def page_radionics(pdf: Doc) -> None:
    pdf.set_context("RADIONIQUE SACREE", "Montage experimental hors materialisme")
    pdf.add_page()
    pdf.page_border()
    y = 24
    y = pdf.heading_block(y, "IX.  MONTAGE RADIONIQUE PHI", "Schema et protocole de montage")
    y = pdf.ornate_box(
        y,
        "Schema recommande",
        RADIONIC,
        accent_color=C["copper"],
        bg_color=C["rose_soft"],
        line_size=6.2,
    )
    y = pdf.sub_heading(y, "Activation")
    y = pdf.bullets(
        y,
        [
            "Jour 1 a 7 : 1 cycle Dhikr B devant le montage.",
            "Jour 8 a 14 : ajouter le code 786 489 618 en lecture lente 3 fois.",
            "Jour 15 a 21 : travail avec le talisman 8 minutes matin et soir.",
            "Toujours relier la demande a une action concrete dans la vie reelle.",
        ],
        7.5,
    )
    y = pdf.p(
        y,
        "Le montage n'est pas un substitut a l'effort. Il sert a aligner intention, langage, nombre, "
        "matiere et repetition. La densite du champ depend de la coherence entre ces cinq niveaux.",
        7.8,
    )


def page_protocol(pdf: Doc) -> None:
    pdf.set_context("PROTOCOLE", "Cycle pratique de 21 jours")
    pdf.add_page()
    pdf.page_border()
    y = 24
    y = pdf.heading_block(y, "X.  ROUTINE DE MANIFESTATION", "Protocole journalier structure")
    y = pdf.ornate_box(
        y,
        "Matin — Fajr",
        [
            "Basmala 1x",
            "Dhikr A ou lecture du code 123 55 89",
            "Intention ecrite en une phrase precise",
        ],
        accent_color=C["gold"],
        bg_color=C["rose_soft"],
    )
    y = pdf.ornate_box(
        y,
        "Milieu de journee — Dhuhr / Asr",
        [
            "Rappel 51:58 ou 65:2-3",
            "Action concrete : appel, travail, vente, creation, demande, service",
            "1 mini lecture du code 319 489 618 786",
        ],
        accent_color=C["gold"],
        bg_color=C["sky_soft"],
    )
    y = pdf.ornate_box(
        y,
        "Soir — Maghrib / Isha",
        [
            "Dhikr B",
            "3 lectures lentes de 786 489 618",
            "Journal : signe, synchronicite, blocage, ouverture observee",
        ],
        accent_color=C["gold"],
        bg_color=C["sage_soft"],
    )
    y = pdf.sub_heading(y, "Cle du protocole")
    y = pdf.p(
        y,
        "Le secret n'est pas le nombre seul. Le secret est la boucle complete : nom -> nombre -> souffle "
        "-> intention -> geste -> gratitude. Quand cette boucle se ferme, le code devient vivant.",
        7.8,
    )


def page_sources(pdf: Doc) -> None:
    pdf.set_context("NOTES ET SOURCES", "Ancrages textuels du laboratoire")
    pdf.add_page()
    pdf.page_border()
    y = 24
    y = pdf.heading_block(y, "XI.  SOURCES, RECTIFICATIONS ET CLES", "Fondations et notes de laboratoire")
    y = pdf.p(
        y,
        "Cette version conserve l'ame esoterique du projet mais renforce sa coherence numerique. "
        "Deux rectifications structurantes ont ete adoptees : 1) Al-Rahman + Al-Rahim = 618, non 684 ; "
        "2) Fattah = 489 en abjad simple, tandis que Ya Fattah = 500.",
        8,
    )
    y = pdf.ornate_box(
        y + 2,
        "Sources de base",
        SOURCES,
        accent_color=C["gold"],
        bg_color=C["lavender_soft"],
        line_size=6,
    )
    y = pdf.sub_heading(y, "Conclusion esoterique")
    y = pdf.p(
        y,
        "Le secret du rizq, dans cette lecture, est que la misericorde precalcule le flux avant la "
        "matiere. Le code 618 place Rahman et Rahim au centre. Phi sert alors de passerelle entre "
        "le coeur, le nom, la proportion, la parole et l'effet. Le talisman, le dhikr et le montage "
        "radionique ne sont que trois facons de fermer ce circuit.",
        7.8,
    )
    y = pdf.p(
        y + 2,
        "Wa-Allahu min wara'i al-qasd.",
        9,
        C["burgundy"],
        False,
        22,
        166,
        "C",
    )


def build() -> Path:
    pdf = Doc()
    add_cover(pdf)
    page_prelim(pdf)
    page_matrix(pdf)
    page_phi(pdf)
    page_fib(pdf)
    page_grabovoi(pdf)
    page_dhikr(pdf)
    page_talisman(pdf)
    page_radionics(pdf)
    page_protocol(pdf)
    page_sources(pdf)
    output = PDF_OUTPUTS["secret_rizq_esoterique"]
    pdf.output(str(output))
    return output


if __name__ == "__main__":
    out = build()
    print(f"PDF generated: {out}")
