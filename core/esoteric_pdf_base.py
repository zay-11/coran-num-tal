#!/usr/bin/env python3
from __future__ import annotations

import math
from pathlib import Path

from fpdf import FPDF
import arabic_reshaper
from bidi.algorithm import get_display


def pick_font(*candidates: str) -> str:
    for raw in candidates:
        path = Path(raw)
        if path.exists():
            return str(path)
    raise FileNotFoundError(f"No font found in candidates: {candidates}")


LATIN = pick_font(
    "C:/Windows/Fonts/arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
)
LATIN_B = pick_font(
    "C:/Windows/Fonts/arialbd.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "C:/Windows/Fonts/arial.ttf",
)
ARABIC = pick_font(
    "C:/Windows/Fonts/arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
)

RESHAPER = arabic_reshaper.ArabicReshaper(configuration={"support_ligatures": False})

C = {
    "cream": (250, 246, 236),
    "white": (255, 255, 255),
    "ink": (26, 24, 32),
    "muted": (116, 114, 122),
    "line": (205, 204, 212),
    "gold": (201, 156, 57),
    "gold_dark": (146, 105, 28),
    "violet": (88, 49, 132),
    "violet_soft": (186, 160, 222),
    "blue": (42, 61, 107),
    "blue_soft": (220, 229, 246),
    "green_soft": (223, 241, 225),
    "rose_soft": (249, 230, 235),
    "dark": (19, 17, 30),
    "night": (13, 14, 39),
    "copper": (181, 108, 54),
    "teal": (20, 124, 120),
}


def ar(text: str) -> str:
    return get_display(RESHAPER.reshape(text))


class EsotericDoc(FPDF):
    def __init__(self, title: str, subtitle: str = "") -> None:
        super().__init__("P", "mm", "A4")
        self.add_font("Body", "", LATIN, uni=True)
        self.add_font("Body", "B", LATIN_B, uni=True)
        self.add_font("Ar", "", ARABIC, uni=True)
        self.set_auto_page_break(True, 15)
        self.set_title(title)
        self.set_author("Codex")
        self.set_creator("Esoteric PDF Base")
        self.header_title = title
        self.header_subtitle = subtitle
        self.skip_header = False

    def set_context(self, title: str, subtitle: str = "") -> None:
        self.header_title = title
        self.header_subtitle = subtitle

    def header(self) -> None:
        if self.skip_header:
            return
        self.set_fill_color(*C["dark"])
        self.rect(0, 0, 210, 18, "F")
        self.set_font("Body", "B", 10.5)
        self.set_text_color(*C["gold"])
        self.set_xy(10, 4)
        self.cell(190, 5, self.header_title, align="C")
        if self.header_subtitle:
            self.set_font("Body", "", 6)
            self.set_text_color(*C["violet_soft"])
            self.set_xy(10, 11)
            self.cell(190, 4, self.header_subtitle, align="C")
        self.ln(18)

    def footer(self) -> None:
        if self.skip_header:
            return
        self.set_y(-11)
        self.set_font("Body", "", 6)
        self.set_text_color(*C["muted"])
        self.cell(0, 4, f"{self.header_title}  |  p. {self.page_no()}", align="C")

    def text(self, x: float, y: float, txt: str, size: float = 8, bold: bool = False,
             color=C["ink"], align: str = "L", w: float = 50) -> None:
        self.set_font("Body", "B" if bold else "", size)
        self.set_text_color(*color)
        self.set_xy(x, y)
        self.cell(w, 5, txt, align=align)

    def text_ar(self, x: float, y: float, txt: str, size: float = 12,
                color=C["gold"], align: str = "C", w: float = 50) -> None:
        self.set_font("Ar", "", size)
        self.set_text_color(*color)
        self.set_xy(x, y)
        self.cell(w, 6, ar(txt), align=align)

    def paragraph(self, y: float, txt: str, size: float = 8, color=C["ink"],
                  bold: bool = False, x: float = 22, w: float = 168,
                  align: str = "L", lh: float | None = None) -> float:
        if lh is None:
            lh = size * 0.72 + 1.2
        self.set_font("Body", "B" if bold else "", size)
        self.set_text_color(*color)
        self.set_xy(x, y)
        self.multi_cell(w, lh, txt, align=align)
        return self.get_y()

    def section(self, y: float, title: str) -> float:
        self.set_fill_color(*C["violet_soft"])
        self.rect(18, y, 174, 7, "F")
        self.text(22, y + 1, title, 9, True, C["ink"], "L", 166)
        self.hline(y + 9)
        return y + 12

    def sub(self, y: float, title: str) -> float:
        self.text(22, y, title, 8, True, C["violet"], "L", 166)
        return y + 7

    def bullets(self, y: float, items: list[str], size: float = 7.1,
                color=C["ink"]) -> float:
        for item in items:
            y = self.paragraph(y, f"• {item}", size=size, color=color)
            y += 1
        return y

    def hline(self, y: float, color=C["gold"], lw: float = 0.3) -> None:
        self.set_draw_color(*color)
        self.set_line_width(lw)
        self.line(18, y, 192, y)

    def box(self, y: float, title: str, lines: list[str], fill=C["blue_soft"],
            border=C["gold"], title_color=C["violet"], line_size: float = 6.0) -> float:
        h = 8 + len(lines) * 5.2 + 2
        self.set_fill_color(*fill)
        self.set_draw_color(*border)
        self.set_line_width(0.35)
        self.rect(18, y, 174, h, "DF")
        self.text(22, y + 1, title, 7.5, True, title_color, "L", 164)
        cy = y + 7.5
        for line in lines:
            self.text(22, cy, line, line_size, False, C["ink"], "L", 166)
            cy += 5.2
        return y + h + 3

    def quote(self, y: float, txt: str, fill=C["rose_soft"]) -> float:
        return self.paragraph(
            y + 2,
            txt,
            size=7.1,
            color=C["blue"],
            bold=False,
            x=24,
            w=162,
            align="L",
        )

    def circle(self, x: float, y: float, r: float, style: str = "D") -> None:
        self.ellipse(x - r, y - r, 2 * r, 2 * r, style)

    def draw_star_8(self, cx: float, cy: float, r1: float, r2: float) -> None:
        angles1 = [45, 135, 225, 315]
        angles2 = [0, 90, 180, 270]
        pts1 = []
        pts2 = []
        for deg in angles1:
            rad = math.radians(deg)
            pts1.append((cx + r1 * math.cos(rad), cy - r1 * math.sin(rad)))
        for deg in angles2:
            rad = math.radians(deg)
            pts2.append((cx + r2 * math.cos(rad), cy - r2 * math.sin(rad)))
        self.set_draw_color(*C["gold"])
        self.set_line_width(0.5)
        for i in range(4):
            x1, y1 = pts1[i]
            x2, y2 = pts1[(i + 1) % 4]
            self.line(x1, y1, x2, y2)
        self.set_draw_color(*C["violet_soft"])
        self.set_line_width(0.4)
        for i in range(4):
            x1, y1 = pts2[i]
            x2, y2 = pts2[(i + 1) % 4]
            self.line(x1, y1, x2, y2)
