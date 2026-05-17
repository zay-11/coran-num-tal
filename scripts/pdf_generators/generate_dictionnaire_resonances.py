#!/usr/bin/env python3
"""
DICTIONNAIRE DES RESONANCES DU RIZQ
Reference exhaustive de TOUTES les racines coraniques liees au rizq.
Abjad, occurrences, phi, Fibonacci, domaines associes.
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
    "sky": (210, 218, 232), "lav": (222, 212, 232), "sepia": (235, 228, 215),
}

ABJAD = {
    "ا": 1, "أ": 1, "إ": 1, "آ": 1, "ٱ": 1, "ء": 1, "ؤ": 6, "ئ": 10,
    "ب": 2, "ج": 3, "د": 4, "ه": 5, "ة": 5, "و": 6, "ز": 7, "ح": 8, "ط": 9,
    "ي": 10, "ى": 10, "ك": 20, "ل": 30, "م": 40, "ن": 50, "س": 60, "ع": 70,
    "ف": 80, "ص": 90, "ق": 100, "ر": 200, "ش": 300, "ت": 400, "ث": 500,
    "خ": 600, "ذ": 700, "ض": 800, "ظ": 900, "غ": 1000,
}


def abjad(t):
    return sum(ABJAD.get(c, 0) for c in t)


def droot(n):
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n


def fib_up_to(limit):
    f = [1, 1]
    while f[-1] < limit:
        f.append(f[-1] + f[-2])
    return f


def near_fib(v):
    if v <= 1:
        return 1, 1.0
    fibs = fib_up_to(max(v * 2, 10))
    n = min(fibs, key=lambda x: abs(x - v))
    return n, round(v / n, 4) if n else 0


# Comprehensive Quranic roots related to Rizq
# Format: (arabic_root, transliteration, meaning, occurrences_approx, domain)
ROOTS = [
    ("رزق", "RZQ", "Subsistance, provision, rizq", 123, "Richesse"),
    ("شكر", "ShKR", "Gratitude, reconnaissance", 75, "Richesse"),
    ("برك", "BRK", "Baraka, benediction, stabilite", 32, "Richesse"),
    ("وقي", "WQY", "Taqwa, protection, garde", 258, "Protection"),
    ("خير", "KhYR", "Bien, bonte, meilleur", 190, "Richesse"),
    ("فضل", "FDL", "Grace, faveur, surplus", 88, "Richesse"),
    ("نعم", "N'AM", "Bienfait, douceur, beatitude", 140, "Richesse"),
    ("كثر", "KThR", "Abondance, multiplication", 167, "Richesse"),
    ("عطو", "'ATW", "Don, octroi, attribution", 35, "Richesse"),
    ("فتح", "FTH", "Ouverture, conquete, victoire", 38, "Richesse"),
    ("وسع", "WS'", "Immensite, ampleur, largesse", 31, "Richesse"),
    ("غنى", "GhNY", "Richesse, autosuffisance", 73, "Richesse"),
    ("غفر", "GhFR", "Pardon, recouvrement", 234, "Protection"),
    ("رحم", "RHM", "Misericorde, compassion", 339, "Richesse"),
    ("هدي", "HDY", "Guidance, direction", 316, "Savoir"),
    ("علم", "'ALM", "Science, connaissance", 854, "Savoir"),
    ("حكم", "HKM", "Sagesse, jugement", 210, "Savoir"),
    ("نور", "NWR", "Lumiere, illumination", 43, "Savoir"),
    ("شفع", "ShF'", "Intercession, guerison", 31, "Sante"),
    ("برء", "BR'", "Guerison, innocence", 31, "Sante"),
    ("سلم", "SLM", "Paix, integrite, soumission", 140, "Protection"),
    ("أمن", "'AMN", "Securite, foi, confiance", 879, "Protection"),
    ("حفظ", "HFZ", "Garde, preservation", 44, "Protection"),
    ("نصر", "NSR", "Secours, victoire", 159, "Protection"),
    ("كفى", "KFY", "Suffisance, contentement", 33, "Richesse"),
    ("ملك", "MLK", "Royaute, possession, pouvoir", 206, "Richesse"),
    ("كرم", "KRM", "Generosite, noblesse", 47, "Richesse"),
    ("وهب", "WHB", "Don, donation", 25, "Richesse"),
    ("بسط", "BST", "Extension, dilation, joie", 25, "Richesse"),
    ("قدر", "QDR", "Puissance, mesure, destinee", 132, "Richesse"),
    ("رجع", "RJ'", "Retour, revenu, rappel", 104, "Protection"),
    ("حسب", "HSB", "Calcul, suffisance", 109, "Richesse"),
    ("جود", "JWD", "Generosite, excellence", 5, "Richesse"),
    ("سعد", "S'D", "Bonheur, felicite", 35, "Richesse"),
    ("فلح", "FLH", "Reussite, succes", 40, "Richesse"),
    ("نجح", "NJH", "Succes, accomplissement", 1, "Richesse"),
    ("ربح", "RBH", "Profit, gain commercial", 2, "Richesse"),
    ("كسى", "KSY", "Vetement, couverture, dignite", 10, "Richesse"),
    ("طعم", "T'AM", "Nourriture, subsistance", 48, "Richesse"),
    ("شرب", "ShRB", "Boisson, abreuvement", 39, "Richesse"),
    ("سكن", "SKN", "Tranquillite, residence", 69, "Protection"),
    ("قسم", "QSM", "Partage, repartition", 33, "Richesse"),
    ("عدل", "'ADL", "Justice, equilibre", 28, "Protection"),
    ("صدق", "SDQ", "Veracite, charite", 154, "Richesse"),
    ("زكى", "ZKY", "Purification, croissance", 59, "Richesse"),
    ("طيب", "TYB", "Bon, pur, agreable", 50, "Richesse"),
    ("حلل", "HLL", "Licit, permission, desengagement", 53, "Richesse"),
    ("يسر", "YSR", "Facilite, aise", 44, "Richesse"),
    ("رغب", "RGHB", "Desir, aspiration", 13, "Richesse"),
    ("طلب", "TLB", "Demande, requete, quete", 55, "Richesse"),
]


def compute_all():
    results = []
    for arabic, translit, meaning, occ, domain in ROOTS:
        a = abjad(arabic)
        dr = droot(a)
        phi_val = round(a * PHI, 1)
        inv_phi = round(a / PHI, 1)
        fib, ratio = near_fib(a)
        results.append({
            "arabic": arabic, "translit": translit, "meaning": meaning,
            "occurrences": occ, "domain": domain,
            "abjad": a, "digital_root": dr,
            "phi_projection": phi_val, "inv_phi": inv_phi,
            "fibonacci": fib, "fib_ratio": ratio,
        })
    return results


def build():
    data = compute_all()

    pdf = FPDF("P", "mm", "A4")
    pdf.add_font("B", "", FB)
    pdf.add_font("B", "B", FH)
    pdf.add_font("B", "I", FI)
    pdf.set_auto_page_break(True, 13)
    pdf.set_title("Dictionnaire des Resonances du Rizq")

    # Cover
    pdf.add_page()
    pdf.set_fill_color(*C["bg"])
    pdf.rect(0, 0, 210, 297, "F")
    pdf.set_fill_color(*C["gold"])
    pdf.rect(28, 110, 154, 1.6, "F")
    pdf.set_font("B", "B", 19)
    pdf.set_text_color(*C["bordeaux"])
    pdf.set_xy(15, 120)
    pdf.cell(180, 8, "DICTIONNAIRE", align="C")
    pdf.set_xy(15, 130)
    pdf.cell(180, 8, "DES RESONANCES DU RIZQ", align="C")
    pdf.set_font("B", "I", 10)
    pdf.set_text_color(*C["gold"])
    pdf.set_xy(15, 144)
    pdf.cell(180, 6, "50 racines coraniques  ·  Abjad  ·  Phi  ·  Fibonacci  ·  Domaines", align="C")
    pdf.set_font("B", "I", 7)
    pdf.set_text_color(*C["muted"])
    pdf.set_xy(15, 158)
    pdf.cell(180, 4, "CORAN NUM TAL  |  Edition Premium  |  2026", align="C")

    # Table pages (25 entries per page = 2 pages)
    for page_start in range(0, len(data), 25):
        pdf.add_page()
        y = 16
        pdf.set_font("B", "B", 7)
        pdf.set_text_color(*C["bordeaux"])
        headers = ["Racine", "Sens", "Occ", "Abjad", "Rac", "Phi", "1/Phi", "Fib", "Domaine"]
        widths = [18, 38, 10, 16, 10, 18, 18, 14, 28]
        cx = 18
        for i, h in enumerate(headers):
            pdf.set_xy(cx, y)
            pdf.cell(widths[i], 4.5, h, align="C")
            cx += widths[i]
        y += 5.5

        page_data = data[page_start:page_start + 25]
        for row_idx, d in enumerate(page_data):
            bg = C["sepia"] if row_idx % 2 == 0 else C["w"]
            pdf.set_fill_color(*bg)
            vals = [d["arabic"], d["meaning"], str(d["occurrences"]), str(d["abjad"]),
                    str(d["digital_root"]), str(d["phi_projection"]), str(d["inv_phi"]),
                    str(d["fibonacci"]), d["domain"]]
            cx = 18
            for i, v in enumerate(vals):
                pdf.set_font("B", "", 5.8)
                pdf.set_text_color(*C["ink2"])
                pdf.set_xy(cx, y)
                pdf.cell(widths[i], 4.5, v, fill=True, align="C")
                cx += widths[i]
            y += 4.8

    # Summary page
    pdf.add_page()
    y = 20
    pdf.set_font("B", "B", 10)
    pdf.set_text_color(*C["bordeaux"])
    pdf.set_xy(20, y)
    pdf.cell(170, 6, "ANALYSE STATISTIQUE", align="C")
    y += 10

    domains = {}
    for d in data:
        dom = d["domain"]
        if dom not in domains:
            domains[dom] = {"count": 0, "total_abjad": 0, "total_occ": 0}
        domains[dom]["count"] += 1
        domains[dom]["total_abjad"] += d["abjad"]
        domains[dom]["total_occ"] += d["occurrences"]

    for dom_name, stats in sorted(domains.items()):
        pdf.set_font("B", "B", 7.5)
        pdf.set_text_color(*C["bordeaux"])
        pdf.set_xy(24, y)
        pdf.cell(60, 5, dom_name)
        pdf.set_font("B", "", 7)
        pdf.set_text_color(*C["ink2"])
        pdf.set_xy(80, y)
        pdf.cell(100, 5, f"{stats['count']} racines  |  Total abjad: {stats['total_abjad']}  |  Total occurrences: {stats['total_occ']}")
        y += 6

    # Top phi resonances
    y += 6
    pdf.set_font("B", "B", 10)
    pdf.set_text_color(*C["bordeaux"])
    pdf.set_xy(20, y)
    pdf.cell(170, 6, "TOP 10 — PLUS HAUTES RESONANCES PHI (abjad proche de phi ou 1/phi)", align="C")
    y += 10

    # Find roots where abjad is closest to phi ratio with another abjad
    abjads = [(d["arabic"], d["translit"], d["abjad"], d["meaning"]) for d in data]
    phi_pairs = []
    for i in range(len(abjads)):
        for j in range(i + 1, len(abjads)):
            if abjads[i][2] > 0 and abjads[j][2] > 0:
                ratio = abjads[i][2] / abjads[j][2]
                d1 = abs(ratio - PHI)
                d2 = abs(ratio - (1 / PHI))
                best = min(d1, d2)
                if best < 0.1:
                    phi_pairs.append((best, abjads[i], abjads[j], ratio))
    phi_pairs.sort()

    for i, (dist, a, b, ratio) in enumerate(phi_pairs[:10]):
        pdf.set_font("B", "", 7)
        pdf.set_text_color(*C["ink2"])
        pdf.set_xy(24, y)
        pdf.cell(160, 4.5, f"#{i+1}  {a[1]} ({a[2]}) <phi> {b[1]} ({b[2]})  Ratio: {ratio:.3f}  Dist: {dist:.4f}")
        y += 5

    out = ROOT / "exports/pdf/dictionnaire_resonances.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(out))
    return out


if __name__ == "__main__":
    out = build()
    print(f"PDF genere: {out}")
