#!/usr/bin/env python3
"""
LES 40 PORTES — Journal guide de 40 jours
Integre mansion lunaire, phi, dhikr personnalise et journaling.
"""

from __future__ import annotations
import math, sys
from pathlib import Path

from fpdf import FPDF
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

PHI = (1 + math.sqrt(5)) / 2

def pf(*c):
    for r in c:
        p = Path(r)
        if p.exists():
            return str(p)
    raise FileNotFoundError(str(c))

FH = pf("C:/Windows/Fonts/GARABD.TTF", "C:/Windows/Fonts/georgiab.ttf", "C:/Windows/Fonts/arialbd.ttf")
FB = pf("C:/Windows/Fonts/GARA.TTF", "C:/Windows/Fonts/georgia.ttf", "C:/Windows/Fonts/arial.ttf")
FI = pf("C:/Windows/Fonts/GARAIT.TTF", "C:/Windows/Fonts/georgiai.ttf", "C:/Windows/Fonts/ariali.ttf")

C = {
    "bg": (249, 245, 238), "w": (255, 254, 250), "ink": (42, 34, 28),
    "ink2": (84, 70, 56), "muted": (140, 124, 108),
    "gold": (184, 142, 40), "gold_l": (214, 180, 88), "gold_p": (238, 222, 178),
    "bordeaux": (88, 30, 42), "rose": (240, 218, 214), "sage": (210, 222, 205),
    "sky": (210, 218, 232), "sepia": (235, 228, 215),
}

# 7 weekly themes (7 levels of Rizq descent)
WEEKS = [
    ("Semaine 1", "L'INTENTION — Poser la demande", "Travail sur la clarte de l'intention. Quelle est ta demande reelle ?", 1),
    ("Semaine 2", "LA SOURCE — Se relier au Pourvoyeur", "Contemplation de 51:58. La provision existe avant le manque.", 51),
    ("Semaine 3", "L'OUVERTURE — Debloquer les portes", "Travail sur les blocages internes. Istighfar et liberation.", 65),
    ("Semaine 4", "LA PLUIE — Faire descendre le flux", "Activation de 71:10-12. Descente de l'abondance dans le manifeste.", 71),
    ("Semaine 5", "LE CORRIDOR — Traverser Fibonacci", "Parcours 34->55->56->89. De la prosperite a la lucidite.", 34),
    ("Semaine 6", "LE PORTAL — Le Coeur Misericordieux", "Fixation sur le centre 618. La misericorde comme moteur.", 618),
    ("Semaine 7", "LE CYCLE — Integrer et sceller", "Fermeture du cycle 61->99. Gratitude et tawakkul.", 61),
]

SAINT_NAMES = ["Ya Razzaq", "Ya Fattah", "Ya Ghani", "Ya Mughni", "Ya Rahman", "Ya Rahim", "Ya Nur"]
GRABOVOI = ["123 55 89", "786 489 618", "6119 078", "319 489 618 786", "307 123 786", "56 96 152", "520 741 8"]


def build():
    pdf = FPDF("P", "mm", "A4")
    for n, f, s in [("B", FB, ""), ("B", FH, "B"), ("B", FI, "I")]:
        pdf.add_font(n, s, f)
    pdf.set_auto_page_break(True, 14)
    pdf.set_title("Les 40 Portes")

    # Cover
    pdf.add_page()
    pdf.set_fill_color(*C["bg"])
    pdf.rect(0, 0, 210, 297, "F")
    pdf.set_fill_color(*C["gold"])
    pdf.rect(34, 100, 142, 1.6, "F")
    pdf.set_font("B", "B", 22)
    pdf.set_text_color(*C["bordeaux"])
    pdf.set_xy(15, 110)
    pdf.cell(180, 8, "LES 40 PORTES", align="C")
    pdf.set_font("B", "I", 11)
    pdf.set_text_color(*C["gold"])
    pdf.set_xy(15, 122)
    pdf.cell(180, 6, "Journal Guide de 40 Jours", align="C")
    pdf.set_font("B", "I", 8)
    pdf.set_text_color(*C["muted"])
    pdf.set_xy(15, 135)
    pdf.cell(180, 5, "Mansion Lunaire  ·  Phi  ·  Dhikr  ·  Synchronicites  ·  Reves", align="C")
    pdf.set_xy(15, 143)
    pdf.cell(180, 5, "CORAN NUM TAL  |  Edition Premium  |  2026", align="C")

    # Week intro pages + day pages
    for week_idx, (week_title, theme, desc, anchor) in enumerate(WEEKS):
        # Week intro
        pdf.add_page()
        pdf.set_fill_color(*C["gold"])
        pdf.rect(18, 30, 174, 1.2, "F")
        pdf.set_font("B", "B", 16)
        pdf.set_text_color(*C["bordeaux"])
        pdf.set_xy(20, 36)
        pdf.cell(170, 7, f"{week_title} — {theme}", align="C")
        pdf.set_font("B", "I", 9)
        pdf.set_text_color(*C["ink2"])
        pdf.set_xy(22, 48)
        pdf.cell(166, 12, desc, align="C")
        pdf.set_font("B", "", 7.5)
        pdf.set_text_color(*C["muted"])
        pdf.set_xy(22, 63)
        pdf.cell(166, 5, f"Ancre numerique: {anchor}  |  Nom: {SAINT_NAMES[week_idx]}  |  Code: {GRABOVOI[week_idx]}", align="C")

        # Daily pages
        for day in range(1, 6 if week_idx < 6 else 6):  # Last week has 5 days
            global_day = week_idx * 6 + day
            if global_day > 40:
                break
            mansion = ((global_day - 1) % 28) + 1
            phi_day = round(mansion * PHI, 1)
            dhikr_n = (global_day % 7) or 7

            pdf.add_page()
            y = 22
            pdf.set_fill_color(*C["gold_p"])
            pdf.rect(14, y, 182, 14, "F")
            pdf.set_font("B", "B", 11)
            pdf.set_text_color(*C["bordeaux"])
            pdf.set_xy(18, y + 2)
            pdf.cell(170, 5, f"JOUR {global_day}/40")
            pdf.set_font("B", "I", 7)
            pdf.set_text_color(*C["gold"])
            pdf.set_xy(18, y + 8)
            pc = round(global_day / 40 * 100)
            pdf.cell(170, 4, f"{week_title} — {theme}  |  Progression: {pc}%  |  Mansion {mansion}  |  Phi: {phi_day}")
            y += 18

            # Morning
            pdf.set_fill_color(*C["bordeaux"])
            pdf.rect(18, y, 174, 6, "F")
            pdf.set_font("B", "B", 7)
            pdf.set_text_color(*C["w"])
            pdf.set_xy(22, y + 0.5)
            pdf.cell(166, 5, "MATIN (Fajr)")
            y += 8
            pdf.set_font("B", "I", 7)
            pdf.set_text_color(*C["ink2"])
            pdf.set_xy(22, y)
            pdf.cell(166, 4, f"Dhikr: {SAINT_NAMES[week_idx]} {dhikr_n}x  |  Code du jour: {GRABOVOI[week_idx]}")
            y += 6
            pdf.set_draw_color(*C["gold_l"])
            pdf.set_line_width(0.15)
            for i in range(4):
                pdf.line(24, y + i * 14, 186, y + i * 14)
            pdf.set_font("B", "", 6.5)
            pdf.set_text_color(*C["muted"])
            pdf.set_xy(24, y)
            pdf.cell(160, 4, "Intention du jour :")
            y += 14
            pdf.set_xy(24, y)
            pdf.cell(160, 4, "Signe / synchronicite observee :")
            y += 14
            pdf.set_xy(24, y)
            pdf.cell(160, 4, "Action concrete realisee :")
            y += 14
            pdf.set_xy(24, y)
            pdf.cell(160, 4, "Ressenti / blocage / ouverture :")
            y += 18

            # Evening
            pdf.set_fill_color(*C["gold"])
            pdf.rect(18, y, 174, 6, "F")
            pdf.set_font("B", "B", 7)
            pdf.set_text_color(*C["w"])
            pdf.set_xy(22, y + 0.5)
            pdf.cell(166, 5, "SOIR (Maghrib/Isha)")
            y += 8
            pdf.set_font("B", "I", 7)
            pdf.set_text_color(*C["ink2"])
            pdf.set_xy(22, y)
            pdf.cell(166, 4, f"Dhikr de cloture: Ya Rahim 8x  |  Code pont: 786 489 618")
            y += 6
            pdf.set_draw_color(*C["gold_l"])
            pdf.set_line_width(0.15)
            for i in range(3):
                pdf.line(24, y + i * 14, 186, y + i * 14)
            pdf.set_font("B", "", 6.5)
            pdf.set_text_color(*C["muted"])
            pdf.set_xy(24, y)
            pdf.cell(160, 4, "Gratitude du jour (3 choses) :")
            y += 14
            pdf.set_xy(24, y)
            pdf.cell(160, 4, "Reve / message nocturne (a remplir le lendemain) :")
            y += 14
            pdf.set_xy(24, y)
            pdf.cell(160, 4, "Nombre(s) remarquable(s) vu(s) aujourd'hui :")

    # Final page
    pdf.add_page()
    pdf.set_fill_color(*C["gold"])
    pdf.rect(30, 120, 150, 1.8, "F")
    pdf.set_font("B", "B", 18)
    pdf.set_text_color(*C["bordeaux"])
    pdf.set_xy(15, 130)
    pdf.cell(180, 8, "LES 40 PORTES SONT OUVERTES", align="C")
    pdf.set_font("B", "I", 9)
    pdf.set_text_color(*C["ink2"])
    pdf.set_xy(15, 143)
    pdf.cell(180, 6, "Que le Rizq descende par toutes les directions. 7 · 8 · 19.", align="C")

    out = ROOT / "exports/pdf/40_portes_journal.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(out))
    return out


if __name__ == "__main__":
    out = build()
    print(f"PDF genere: {out}")
