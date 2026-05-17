#!/usr/bin/env python3
"""
CALENDRIER LUNAIRE PHI — Almanach perpetuel
Fusion du Cadran Lunaire Miftah 19 avec le systeme phi.
Chaque mansion lunaire recoit ses projections phi personnalisees.
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
INV_PHI = 1 / PHI


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
    "bg": (249, 244, 236), "w": (255, 254, 250), "ink": (42, 34, 26),
    "ink2": (84, 68, 52), "muted": (140, 124, 108),
    "gold": (184, 142, 40), "gold_l": (214, 180, 88), "gold_p": (238, 222, 178),
    "bordeaux": (88, 30, 42), "rose": (240, 218, 214),
    "sage": (210, 222, 205), "sky": (210, 218, 232), "lav": (222, 212, 232),
    "sepia": (235, 228, 215), "copper": (170, 108, 56),
}

# 28 Mansions Lunaires — from Cadran Lunaire
MANSIONS = [
    (1, "Al-Sharatain", "Nouveau depart", "Nouvelle Lune", 1, "2017133"),
    (2, "Al-Butayn", "Chance, reconquete", "Nouvelle Lune", 1, "2017133"),
    (3, "Al-Thurayya", "PROFIT, TOUT BIEN", "Nouvelle Lune", 1, "2017133"),
    (4, "Al-Dabaran", "Investissement", "Nouvelle Lune", 1, "2017133"),
    (5, "Al-Haqa", "Etude, construction", "Croissant Croissant", 7, "520 741 8"),
    (6, "Al-Hana", "Justice, chasse", "Croissant Croissant", 7, "520 741 8"),
    (7, "Al-Dhira", "PROFIT, BIENS", "Croissant Croissant", 7, "520 741 8"),
    (8, "Al-Nathrah", "Amitie, amour", "Croissant Croissant", 7, "520 741 8"),
    (9, "Al-Tarf", "Ennemis, protection", "Premier Quartier", 8, "87467894"),
    (10, "Al-Jabhah", "Amour, guerison", "Premier Quartier", 8, "87467894"),
    (11, "Al-Zubrah", "COMMERCE, RICHESSE", "Premier Quartier", 8, "87467894"),
    (12, "Al-Sarfah", "Recolte, elevation", "Premier Quartier", 8, "87467894"),
    (13, "Al-Awwa", "COMMERCE, VOYAGE", "Gibbeuse Croissante", 19, "318 798"),
    (14, "Al-Simak", "Guerison, moissons", "Gibbeuse Croissante", 19, "318 798"),
    (15, "Al-Ghafr", "TRESORS CACHES", "Gibbeuse Croissante", 19, "318 798"),
    (16, "Al-Zubana", "ARGENT, GAINS", "Gibbeuse Croissante", 19, "318 798"),
    (17, "Al-Iklil", "FORTUNE, MARIAGE", "Pleine Lune", 15, "9798733714615"),
    (18, "Al-Qalb", "Protection", "Pleine Lune", 15, "9798733714615"),
    (19, "Al-Shaulah", "CHANCE GENERALE", "Pleine Lune", 15, "9798733714615"),
    (20, "Al-Naaim", "Chasse, batiment", "Pleine Lune", 15, "9798733714615"),
    (21, "Al-Baldah", "GAINS, VOYAGE", "Gibbeuse Decroissante", 33, "3657745"),
    (22, "Sa'd al-Dhabih", "Liberation, soins", "Gibbeuse Decroissante", 33, "3657745"),
    (23, "Sa'd Bula", "Amitie, medecine", "Gibbeuse Decroissante", 33, "3657745"),
    (24, "Sa'd al-Su'ud", "Mariage, victoire", "Gibbeuse Decroissante", 33, "3657745"),
    (25, "Sa'd al-Akhbiyah", "Protection", "Dernier Quartier", 61, "9213140"),
    (26, "Al-Fargh al-Mukdim", "GAINS, EMPLOI", "Dernier Quartier", 61, "9213140"),
    (27, "Al-Fargh al-Thani", "GAINS, RECOLTE", "Dernier Quartier", 61, "9213140"),
    (28, "Batn al-Hut", "COMMERCE, ABONDANCE", "Dernier Quartier", 61, "9213140"),
]


def fibonacci_up_to(limit):
    fib = [1, 1]
    while fib[-1] < limit:
        fib.append(fib[-1] + fib[-2])
    return fib


def nearest_fib(value):
    if value <= 1:
        return 1, 1.0
    fibs = fibonacci_up_to(value * 2)
    nearest = min(fibs, key=lambda x: abs(x - value))
    return nearest, value / nearest if nearest else 0


def digital_root(n):
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n


def compute_mansion_phi(m):
    idx, name, prop, phase, sacre, grabovoi = m
    phi_val = round(idx * PHI, 2)
    inv_phi_val = round(idx * INV_PHI, 2)
    fib, ratio = nearest_fib(idx)
    lucky = (idx * 7 + digital_root(idx)) % 49
    if lucky == 0:
        lucky = 49
    dhikr = digital_root(round(idx * PHI))
    return {
        "index": idx, "name": name, "property": prop, "phase": phase,
        "sacred_number": sacre, "grabovoi_code": grabovoi,
        "phi_projection": phi_val, "inv_phi_projection": inv_phi_val,
        "nearest_fibonacci": fib, "fib_ratio": round(ratio, 4),
        "lucky_number": lucky, "dhikr_repetition": dhikr if dhikr > 0 else 7,
        "golden_code": f"{idx} {round(idx*PHI)} {fib}",
    }


def build():
    mansions_phi = [compute_mansion_phi(m) for m in MANSIONS]

    pdf = FPDF("P", "mm", "A4")
    pdf.add_font("H", "", FONT_H)
    pdf.add_font("B", "", FONT_B)
    pdf.add_font("B", "B", FONT_H)
    pdf.add_font("B", "I", FONT_I)
    pdf.add_font("Ar", "", FONT_AR)
    pdf.set_auto_page_break(True, 14)
    pdf.set_title("Calendrier Lunaire Phi")

    # Cover
    pdf.add_page()
    pdf.set_fill_color(*C["bg"])
    pdf.rect(0, 0, 210, 297, "F")

    # Lunar wheel on cover
    cx, cy = 105, 130
    for r, lw, clr in [(80, 0.4, C["gold"]), (65, 0.3, C["gold_l"]), (50, 0.25, C["copper"]), (35, 0.2, C["gold_l"])]:
        pdf.set_draw_color(*clr)
        pdf.set_line_width(lw)
        pdf.circle(cx, cy, r, "D")
    # 28 rays
    for i in range(28):
        ang = math.radians(360 / 28 * i - 90)
        x = cx + 55 * math.cos(ang)
        yc = cy - 55 * math.sin(ang)
        pdf.set_fill_color(*C["gold"])
        pdf.circle(x, yc, 1.2, "F")

    y = 190
    pdf.set_fill_color(*C["gold"])
    pdf.rect(32, y, 146, 1.6, "F")
    y += 8
    pdf.set_font("B", "B", 19)
    pdf.set_text_color(*C["bordeaux"])
    pdf.set_xy(15, y)
    pdf.cell(180, 7, "CALENDRIER LUNAIRE PHI", align="C")
    y += 10
    pdf.set_font("B", "I", 9)
    pdf.set_text_color(*C["gold"])
    pdf.set_xy(15, y)
    pdf.cell(180, 5, "28 Mansions  ·  Projections Phi  ·  Codes Grabovoi  ·  Almanach Perpetuel", align="C")
    y += 9
    pdf.set_draw_color(*C["gold_l"])
    pdf.set_line_width(0.3)
    pdf.line(60, y, 150, y)
    y += 7
    pdf.set_font("B", "I", 7)
    pdf.set_text_color(*C["muted"])
    pdf.set_xy(15, y)
    pdf.cell(180, 4, "CORAN NUM TAL  |  Edition Premium  |  2026", align="C")

    # Mansion pages (4 per page = 7 pages)
    for page_start in range(0, 28, 4):
        pdf.add_page()
        y = 20
        pdf.set_font("B", "B", 9)
        pdf.set_text_color(*C["bordeaux"])
        pdf.set_xy(20, y)
        pdf.cell(170, 5, f"MANSIONS {page_start+1} - {min(page_start+4, 28)}", align="C")
        y += 8

        for i in range(4):
            idx = page_start + i
            if idx >= 28:
                break
            m = mansions_phi[idx]

            # Mansion card
            h = 58
            bg_col = C["sepia"] if i % 2 == 0 else C["w"]
            pdf.set_fill_color(*bg_col)
            pdf.set_draw_color(*C["gold_l"])
            pdf.set_line_width(0.3)
            pdf.rect(16, y, 178, h, "DF")
            # Left gold bar
            pdf.set_fill_color(*C["gold"])
            pdf.rect(16, y, 2.5, h, "F")
            # Number
            pdf.set_font("B", "B", 18)
            pdf.set_text_color(*C["bordeaux"])
            pdf.set_xy(24, y + 2)
            pdf.cell(12, 8, str(m["index"]), align="C")
            # Name
            pdf.set_font("B", "B", 8.5)
            pdf.set_text_color(*C["ink"])
            pdf.set_xy(40, y + 2)
            pdf.cell(140, 5, m["name"])
            # Property
            pdf.set_font("B", "I", 6.5)
            pdf.set_text_color(*C["gold"])
            pdf.set_xy(40, y + 7)
            pdf.cell(140, 4, m["property"])
            # Phase
            pdf.set_font("B", "", 6)
            pdf.set_text_color(*C["muted"])
            pdf.set_xy(40, y + 12)
            pdf.cell(140, 4, m["phase"])
            # Values row 1
            row_y = y + 19
            pdf.set_font("B", "B", 5.8)
            pdf.set_text_color(*C["bordeaux"])
            cols = [("Phi", str(m["phi_projection"])), ("1/Phi", str(m["inv_phi_projection"])),
                    ("Fibonacci", str(m["nearest_fibonacci"])), ("Lucky#", str(m["lucky_number"])),
                    ("Dhikr", f"{m['dhikr_repetition']}x"), ("N Sacre", str(m["sacred_number"]))]
            cx = 28
            for label, val in cols:
                pdf.set_xy(cx, row_y)
                pdf.cell(24, 3, label, align="C")
                pdf.set_font("B", "", 6.5)
                pdf.set_text_color(*C["ink2"])
                pdf.set_xy(cx, row_y + 3.5)
                pdf.cell(24, 4, val, align="C")
                pdf.set_font("B", "B", 5.8)
                pdf.set_text_color(*C["bordeaux"])
                cx += 27
            # Code
            code_y = row_y + 9
            pdf.set_font("B", "B", 5.5)
            pdf.set_text_color(*C["muted"])
            pdf.set_xy(28, code_y)
            pdf.cell(20, 3, "Code:")
            pdf.set_font("B", "", 6.5)
            pdf.set_text_color(*C["ink2"])
            pdf.set_xy(45, code_y)
            pdf.cell(90, 3, m["grabovoi_code"])
            pdf.set_font("B", "I", 5.8)
            pdf.set_text_color(*C["gold"])
            pdf.set_xy(28, code_y + 4.5)
            pdf.cell(140, 3, f"Code phi: {m['golden_code']}")

            y += h + 4

    # Summary page
    pdf.add_page()
    y = 20
    pdf.set_font("B", "B", 10)
    pdf.set_text_color(*C["bordeaux"])
    pdf.set_xy(20, y)
    pdf.cell(170, 5, "RESUME — LES 8 MEILLEURES MANSIONS POUR LE RIZQ", align="C")
    y += 10
    rich_mansions = [m for m in mansions_phi if any(w in m["property"].upper() for w in ["PROFIT", "GAIN", "ARGENT", "FORTUNE", "CHANCE", "COMMERCE", "TRESOR", "RICHESSE"])]
    for m in rich_mansions:
        pdf.set_font("B", "B", 7.5)
        pdf.set_text_color(*C["ink"])
        pdf.set_xy(24, y)
        pdf.cell(10, 4, str(m["index"]))
        pdf.set_text_color(*C["bordeaux"])
        pdf.set_xy(32, y)
        pdf.cell(40, 4, m["name"])
        pdf.set_font("B", "", 6.5)
        pdf.set_text_color(*C["gold"])
        pdf.set_xy(72, y)
        pdf.cell(50, 4, f"Phi: {m['phi_projection']}")
        pdf.set_text_color(*C["ink2"])
        pdf.set_xy(120, y)
        pdf.cell(50, 4, f"Lucky#: {m['lucky_number']}  |  Code: {m['grabovoi_code']}")
        y += 5

    y += 6
    pdf.set_font("B", "I", 7)
    pdf.set_text_color(*C["muted"])
    pdf.set_xy(24, y)
    pdf.cell(160, 4, "Formule du Lucky Number : (Mansion# x 7 + digital_root(Mansion#)) mod 49. Si 0, prendre 49.")

    out = ROOT / "exports/pdf/calendrier_lunaire_phi.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(out))
    return out


if __name__ == "__main__":
    out = build()
    print(f"PDF genere: {out}")
