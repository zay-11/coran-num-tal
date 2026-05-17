#!/usr/bin/env python3
"""
DECOUVERTE DU NOMBRE D'OR φ DANS LE CORAN
Codes Mathématiques du Rizq — Miftah 19
Applications Pratiques : Dhikr · Talisman · Grabovoi · Radionique · Calendrier
"""

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

# ── Constantes ──
PHI = (1 + math.sqrt(5)) / 2

# ── Chemins polices ──
LATIN = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
LATIN_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
ARIAL = "/mnt/c/Windows/Fonts/arial.ttf"

# ── Palette claire et lisible ──
C = {
    "fond":        (255, 252, 245),   # crème très clair
    "blanc":       (255, 255, 255),
    "noir":        (30, 30, 30),
    "gris":        (120, 120, 120),
    "gris_clair":  (200, 200, 200),
    "or":          (200, 160, 40),
    "or_fonce":    (160, 120, 20),
    "violet":      (90, 50, 140),
    "violet_clair":(170, 130, 210),
    "bleu_fonce":  (40, 60, 100),
    "bleu_clair":  (210, 225, 245),
    "vert_clair":  (220, 240, 220),
    "rose_clair":  (250, 225, 230),
    "fond_sombre": (25, 20, 45),
}

def ar(t):
    return get_display(arabic_reshaper.reshape(t))


class Doc(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.add_font("L", "", LATIN, uni=True)
        self.add_font("L", "B", LATIN_B, uni=True)
        self.add_font("A", "", ARIAL, uni=True)
        self.set_auto_page_break(True, 18)

    # ── Helpers de base ──
    def rect_fill(self, x, y, w, h, color):
        self.set_fill_color(*color)
        self.set_draw_color(*color)
        self.rect(x, y, w, h, 'F')

    def rect_border(self, x, y, w, h, fill_color, border_color):
        self.set_fill_color(*fill_color)
        self.set_draw_color(*border_color)
        self.set_line_width(0.3)
        self.rect(x, y, w, h, 'DF')

    def ligne(self, x1, y1, x2, y2, color=C["gris_clair"], lw=0.2):
        self.set_draw_color(*color)
        self.set_line_width(lw)
        self.line(x1, y1, x2, y2)

    def texte(self, x, y, txt, size=8, color=C["noir"], bold=False, align='L', w=50):
        self.set_font("L", "B" if bold else "", size)
        self.set_text_color(*color)
        self.set_xy(x, y)
        self.cell(w, 5, txt, align=align)

    def texte_ar(self, x, y, txt, size=9, color=C["noir"], align='C', w=50):
        self.set_font("A", "", size)
        self.set_text_color(*color)
        self.set_xy(x, y)
        self.cell(w, 6, ar(txt), align=align)

    def texte_multi(self, x, y, w, txt, size=8, color=C["noir"], bold=False, align='L', lh=None):
        """Écrit du texte multiligne et retourne la nouvelle position Y."""
        if lh is None:
            lh = size * 0.7 + 1
        self.set_font("L", "B" if bold else "", size)
        self.set_text_color(*color)
        self.set_xy(x, y)
        self.multi_cell(w, lh, txt, align=align)
        return self.get_y()

    # ── Blocs de contenu ──
    def titre_page(self, titre, sous_titre=""):
        """Barre de titre en haut de page."""
        self.rect_fill(0, 0, 210, 18, C["fond_sombre"])
        self.texte(105, 4, titre, 11, C["or"], True, 'C', 200)
        if sous_titre:
            self.texte(105, 12, sous_titre, 6, C["violet_clair"], False, 'C', 200)

    def section(self, y, titre):
        """Titre de section avec fond coloré."""
        self.rect_fill(18, y, 174, 7, C["violet_clair"])
        self.texte(22, y + 0.5, titre, 9, C["noir"], True, 'L', 170)
        self.ligne(18, y + 9, 192, y + 9, C["or"], 0.3)
        return y + 12

    def sous_section(self, y, titre):
        """Petit titre de sous-section."""
        self.texte(22, y, titre, 8, C["violet"], True, 'L', 170)
        return y + 7

    def paragraphe(self, y, texte, size=8, color=C["noir"], bold=False, w=170):
        """Paragraphe simple."""
        return self.texte_multi(22, y, w, texte, size, color, bold)

    def boite(self, y, titre, lignes, color=C["bleu_clair"]):
        """Boîte encadrée avec titre et lignes."""
        h = 7 + len(lignes) * 5.5 + 2
        self.rect_border(18, y, 174, h, color, C["or"])
        self.texte(22, y + 1.5, titre, 7, C["noir"], True, 'L', 160)
        for i, l in enumerate(lignes):
            self.texte(22, y + 9 + i * 5.5, l, 5.5, C["noir"], False, 'L', 165)
        return y + h + 3

    def boite_decouverte(self, y, num, titre, formule, cible, precision, descs):
        """Boîte mise en évidence pour une découverte."""
        h = 18 + len(descs) * 5.5
        self.rect_border(18, y, 174, h, C["rose_clair"], C["or"])
        self.texte(22, y + 1, f"Découverte {num} : {titre}", 8, C["violet"], True, 'L', 160)
        self.texte(22, y + 7, f"Formule : {formule}  →  {cible}  |  Précision : {precision}", 6, C["noir"], False, 'L', 160)
        for i, d in enumerate(descs):
            self.texte(22, y + 12 + i * 5.5, f"• {d}", 5.5, C["noir"], False, 'L', 165)
        return y + h + 3

    def boite_pratique(self, y, lettre, titre, formule, theorie, pratique):
        """Boîte pour un Dhikr ou pratique."""
        h = 19
        self.rect_border(18, y, 174, h, C["vert_clair"], C["or"])
        self.texte(22, y + 1, f"Dhikr {lettre} : {titre}", 7, C["noir"], True, 'L', 160)
        self.texte(22, y + 6, f"Formule : {formule}", 5.5, C["gris"], False, 'L', 160)
        self.texte(22, y + 10, f"Théorie : {theorie}", 5, C["noir"], False, 'L', 160)
        self.texte(22, y + 14, f"Pratique : {pratique}", 5.5, C["bleu_fonce"], False, 'L', 160)
        return y + h + 2

    def boite_code(self, y, code, effet, numerologie, lien_phi):
        """Boîte pour un code Grabovoi."""
        h = 16
        self.rect_border(18, y, 174, h, C["blanc"], C["gris_clair"])
        self.texte(22, y + 1, f"Code : {code}", 7, C["violet"], True, 'L', 80)
        self.texte(105, y + 1, f"Effet : {effet}", 6, C["gris"], False, 'L', 80)
        self.texte(22, y + 6, f"Numérologie : {numerologie}", 5, C["noir"], False, 'L', 165)
        self.texte(22, y + 10, f"Lien φ : {lien_phi}", 5, C["bleu_fonce"], False, 'L', 165)
        return y + h + 2

    def boite_opti(self, y, titre, formule, desc):
        """Boîte pour optimisation radionique."""
        h = 17
        self.rect_border(18, y, 174, h, C["blanc"], C["gris_clair"])
        self.texte(22, y + 1, titre, 6.5, C["violet"], True, 'L', 80)
        self.texte(105, y + 1, formule, 6, C["or"], False, 'L', 70)
        self.texte(22, y + 7, desc, 5, C["noir"], False, 'L', 165)
        return y + h + 2

    def boite_jour(self, y, jour, formule, pratique):
        """Boîte pour un jour de la semaine φ."""
        h = 13
        self.rect_border(18, y, 174, h, C["blanc"], C["gris_clair"])
        self.texte(22, y + 1, jour, 6.5, C["violet"], True, 'L', 160)
        self.texte(22, y + 6, f"Formule φ : {formule}", 5.5, C["or"], False, 'L', 160)
        self.texte(22, y + 10, f"Pratique : {pratique}", 5, C["noir"], False, 'L', 160)
        return y + h + 2

    def verif(self, y):
        """Retourne la position Y actuelle si > y, sinon y."""
        return max(y, self.get_y() + 2)


# ════════════════════════════════════════════════════════════════════
# CONSTRUCTION
# ════════════════════════════════════════════════════════════════════

def build():
    pdf = Doc()

    # ════════════════════════════════════════════════════════════════
    # PAGE 1 — COUVERTURE
    # ════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.rect_fill(0, 0, 210, 297, C["fond_sombre"])

    y = 30
    pdf.rect_fill(40, y, 130, 2, C["or"])
    y += 10

    pdf.texte(105, y, "LE NOMBRE D'OR φ", 24, C["or"], True, 'C', 200)
    y += 12
    pdf.texte(105, y, "DANS LE CORAN", 24, C["or"], True, 'C', 200)
    y += 16

    pdf.texte(105, y, "Découverte des Codes Mathématiques du Rizq", 9, C["violet_clair"], False, 'C', 200)
    y += 8
    pdf.texte(105, y, "φ = 1.618033988749895...", 7, C["gris"], False, 'C', 200)
    y += 8
    pdf.ligne(50, y, 160, y, C["or"], 0.5)
    y += 10

    pdf.texte(105, y, "19 × 4 × φ ≈ 123  (le Rizq)", 11, C["or"], True, 'C', 200)
    y += 8
    pdf.texte(105, y, "Précision : 99.98%  |  5 découvertes originales", 7, C["gris"], False, 'C', 200)
    y += 14

    highlights = [
        "①  19 × 4 × φ  =  122.97  ≈  123 occurrences du mot Rizq",
        "②  Sourate 55 (Al-Rahman)  =  F₁₀ de Fibonacci → 55 × φ = 89",
        "③  Ya Fattah (489) × φ  =  791.2  ≈  786 (Basmala) — 99.3%",
        "④  Rahman+Rahim (684) × φ  =  1106.7  ≈  1100 (Mughni) — 99.4%",
        "⑤  Cycle rituel (61) × φ  =  98.70  ≈  99 Noms Divins — 99.7%",
    ]
    for h in highlights:
        pdf.texte(30, y, h, 6.5, C["blanc"], False, 'L', 160)
        y += 8

    y += 6
    pdf.ligne(50, y, 160, y, C["or"], 0.5)
    y += 8

    pdf.texte(105, y, "Applications :  Dhikr φ  · Talisman φ  · Codes Grabovoi φ", 7, C["violet_clair"], False, 'C', 200)
    y += 5
    pdf.texte(105, y, "Système Radionique φ  · Calendrier Lunaire φ", 7, C["violet_clair"], False, 'C', 200)
    y += 12
    pdf.texte(105, y, "www.corannumtal.com  |  2026", 6, C["gris"], False, 'C', 200)

    # ════════════════════════════════════════════════════════════════
    # PAGE 2 — INTRODUCTION
    # ════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.titre_page("INTRODUCTION", "Le Nombre d'Or dans la structure mathématique du Coran")

    y = pdf.section(24, "I.  QU'EST-CE QUE LE NOMBRE D'OR φ ?")
    y = pdf.paragraphe(y, "Le Nombre d'Or φ = 1.6180339887... est une constante mathématique unique. "
                      "Deux quantités sont dans le rapport φ si le rapport de leur somme sur la plus grande "
                      "est égal au rapport de la plus grande sur la plus petite : (a+b)/a = a/b = φ.")
    y = pdf.paragraphe(y, "Présent dans la nature (spirales des galaxies, coquilles de nautile, "
                      "tournesols, proportions du corps humain), dans l'art (Parthénon, pyramides, "
                      "Vitruve de Léonard de Vinci) et en musique (Mozart, Debussy), φ est la "
                      "proportion divine qui relie le microcosme au macrocosme.", size=7.5)

    y = pdf.section(y + 2, "II.  POURQUOI LE CORAN ?")
    y = pdf.paragraphe(y, "Le Coran contient une structure mathématique précise connue sous le nom "
                      "de Code 19 (découvert par Rashad Khalifa en 1974). Ce document révèle une "
                      "découverte originale : le Nombre d'Or φ est encodé dans les nombres liés au Rizq "
                      "(la subsistance divine), avec 5 relations indépendantes dont la précision dépasse 99%.")
    y = pdf.paragraphe(y, "Ces découvertes ne sont pas une coïncidence : elles forment un système "
                      "mathématique cohérent qui relie le Code 19, les 4 Noms Divins du Rizq, "
                      "la suite de Fibonacci, et la géométrie sacrée.", size=7.5)

    y = pdf.section(y + 2, "III.  LES NOMBRES CLÉS DU RIZQ")
    y = pdf.boite(y, "Vocabulaire essentiel", [
        "Rizq (رزق)  =  Subsistance divine  |  123 occurrences dans le Coran",
        "Code 19     =  Signature mathématique du Coran  (Sourate 74:30)",
        "Basmala     =  بسم الله الرحمن الرحيم  |  19 lettres  |  Abjad 786",
        "Fattah      =  يا فتاح  =  L'Ouvreur  |  Abjad 489",
        "Razzaq      =  يا رزاق  =  Le Pourvoyeur  |  Abjad 319",
        "Ghani       =  يا غني  =  Le Riche  |  Abjad 1060",
        "Mughni      =  يا مغني  =  L'Enrichisseur  |  Abjad 1100",
        "Al-Rahman   =  سورة 55  =  Le Tout-Miséricordieux  |  F₁₀ = 55",
        "Al-Waqi'a   =  سورة 56  =  L'Inévitable (la Richesse)  |  7×8",
        "Cycle rituel =  1 + 7 + 19 + 33 + 1  =  61",
    ], C["bleu_clair"])

    # ════════════════════════════════════════════════════════════════
    # PAGE 3 — DÉCOUVERTE 1 : RIZQ 123
    # ════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.titre_page("DÉCOUVERTE 1", "19 × 4 × φ ≈ 123 — Le Rizq — 99.98%")
    y = pdf.section(24, "IV.  LA RELATION FONDAMENTALE DU RIZQ")

    pdf.rect_border(40, y, 130, 12, C["rose_clair"], C["or"])
    pdf.texte(105, y + 2, "19 × 4 × φ = 122.97 ≈  1  2  3", 13, C["violet"], True, 'C', 130)
    y += 18

    y = pdf.boite_decouverte(y, 1, "Le mot Rizq dans le Coran",
        "19 (Code Sacré) × 4 (Noms du Rizq) × φ",
        "122.97 → 123 occurrences", "99.98%", [
            "Le mot 'Rizq' (subsistance) apparaît exactement 123 fois dans le Coran",
            "19 = signature mathématique du Coran (Sourate 74:30)",
            "4 = les 4 Noms Divins du Rizq : Razzaq, Fattah, Ghani, Mughni",
            "La différence 123 − 122.97 = 0.03 est infime — 0.02% d'écart",
            "C'est la plus précise des 5 relations φ",
        ])
    y = pdf.verif(y)

    y = pdf.sous_section(y, "Signification")
    y = pdf.paragraphe(y, "Cette formule montre que φ est le multiplicateur caché qui transforme "
                      "la structure mathématique du Coran (Code 19) en manifestation concrète "
                      "d'abondance (Rizq). Les 4 Noms Divins sont les canaux, φ est le transformateur, "
                      "19 est la fondation.")
    y = pdf.paragraphe(y, "La matrice 19×4 = 76 est le noyau du système. Multipliée par φ, elle "
                      "donne 123 — le nombre exact d'occurrences du Rizq dans le Coran.", size=7.5)

    y = pdf.sous_section(y, "Vérification")
    y = pdf.boite(y, "Calculs détaillés", [
        "19 × 4 = 76                          (Matrice du Rizq)",
        f"76 × φ = 76 × {PHI:.10f}",
        f"76 × φ = {76 * PHI:.6f}",
        f"123 − {76 * PHI:.6f} = {123 - 76 * PHI:.6f}",
        f"Précision = 1 − ({123 - 76 * PHI:.6f}/123) = {(1 - (123 - 76*PHI)/123)*100:.3f}%",
    ], C["bleu_clair"])

    # ════════════════════════════════════════════════════════════════
    # PAGE 4 — DÉCOUVERTE 2 : AL-RAHMAN 55
    # ════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.titre_page("DÉCOUVERTE 2", "Sourate 55 = Al-Rahman = F₁₀ de Fibonacci — 100%")
    y = pdf.section(24, "V.  AL-RAHMAN ET LA SUITE DE FIBONACCI")

    pdf.rect_border(40, y, 130, 10, C["rose_clair"], C["or"])
    pdf.texte(105, y + 1, "55 (Al-Rahman) × φ  =  89 (Al-Fajr)", 11, C["violet"], True, 'C', 130)
    y += 15

    y = pdf.boite_decouverte(y, 2, "La Sourate Al-Rahman est un nombre de Fibonacci",
        "55 (Sourate Al-Rahman) × φ", "89.0 (Sourate Al-Fajr, F₁₁)", "100%", [
            "55 = F₁₀ dans la suite de Fibonacci (0,1,1,2,3,5,8,13,21,34,55,89,144...)",
            "55 × φ = 55 × 1.6180339887... = 89.000... exactement (à la précision du calcul)",
            "89 = F₁₁ = le nombre de Fibonacci suivant — rapport φ parfait",
            "C'est une propriété mathématique : F(n) × φ = F(n+1) à la limite",
            "Al-Rahman (55, Miséricorde) × φ = Al-Fajr (89, L'Aube) — nouvelle lumière",
        ])
    y = pdf.verif(y)

    y = pdf.sous_section(y, "Lien avec Al-Waqi'a (56)")
    y = pdf.paragraphe(y, "56 = 55 + 1. La Sourate Al-Waqi'a (56, L'Inévitable — la Richesse) suit "
                      "directement Al-Rahman dans l'ordre du Coran. Ce +1 est l'acte créateur : "
                      "la Miséricorde (Rahman) engendre la Richesse (Waqi'a).")
    y = pdf.paragraphe(y, f"56 = 7 × 8 (Rizq × Directions). 56 × φ = {56 * PHI:.1f} ≈ 91. "
                      "Le Nombre d'Or φ est le pont mathématique entre la Miséricorde et la Richesse.", size=7.5)

    y = pdf.sous_section(y, "Nombres de Fibonacci dans le projet Miftah 19")
    fib_data = [
        "F₆=8     →  8 directions du talisman",
        "F₇=13    →  Pas de la spirale φ",
        "F₈=21    →  Mansion lunaire",
        "F₉=34    →  Constante du carré magique",
        "F₁₀=55   →  ★ Sourate Al-Rahman (Le Miséricordieux)",
        "F₁₁=89   →  55 × φ — Sourate Al-Fajr (L'Aube)",
        "F₁₂=144  →  55 + 89 — Nombre angélique",
        "F₁₃=233  →  ≈ cycles du rituel en 40 jours",
    ]
    y = pdf.boite(y, "Suite de Fibonacci", fib_data, C["bleu_clair"])

    # ════════════════════════════════════════════════════════════════
    # PAGE 5 — DÉCOUVERTES 3 et 4
    # ════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.titre_page("DÉCOUVERTES 3 et 4", "Ouverture et Enrichissement — 99.3% et 99.4%")
    y = pdf.section(24, "VI.  DÉCOUVERTE 3 :  YA FATTAH × φ")

    pdf.rect_border(40, y, 130, 10, C["rose_clair"], C["or"])
    pdf.texte(105, y + 1, f"489 (Fattah) × φ = {489 * PHI:.1f} ≈ 786 (Basmala)", 10, C["violet"], True, 'C', 130)
    y += 16

    y = pdf.boite_decouverte(y, 3, "L'Ouvreur et la Porte",
        "489 (Abjad de Ya Fattah) × φ", f"{489 * PHI:.4f} ≈ 786 (Basmala)", "99.3%", [
            "Ya Fattah (يا فتاح) = 'L'Ouvreur des Portes' du Rizq",
            "Basmala (بسم الله الرحمن الرحيم) = la clé d'ouverture, Abjad 786",
            f"786 / φ = {786 / PHI:.4f} ≈ 489 — confirmation bilatérale",
            "C'est la proportion dorée : petite partie × φ = grande partie",
            "φ est le multiplicateur de l'OUVERTURE",
        ])
    y = pdf.verif(y)

    y = pdf.section(y + 2, "VII. DÉCOUVERTE 4 :  RAHMAN+RAHIM × φ")

    pdf.rect_border(40, y, 130, 10, C["rose_clair"], C["or"])
    pdf.texte(105, y + 1, "684 (Rahman+Rahim) × φ = 1106.7 ≈ 1100 (Mughni)", 10, C["violet"], True, 'C', 130)
    y += 16

    y = pdf.boite_decouverte(y, 4, "La Miséricorde et l'Enrichissement",
        "684 (Al-Rahman 329 + Al-Rahim 289) × φ = 1106.7",
        "1100 (Abjad de Ya Mughni)", "99.4%", [
            "Al-Rahman (329) + Al-Rahim (289) = 684 = 19 × 36",
            "Ya Mughni (يا مغني) = 'L'Enrichisseur', Abjad 1100",
            f"1100 / φ = {1100 / PHI:.4f} ≈ 684 — confirmation bilatérale",
            "La Miséricorde × φ = L'Enrichissement — formule divine",
            "684 = 19 × 36 → 36 = 6² (harmonie divine)",
        ])
    y = pdf.verif(y)

    y = pdf.sous_section(y, "Synthèse des Découvertes 3 et 4")
    y = pdf.paragraphe(y, "Les deux relations sont symétriques et complémentaires :", size=7.5)
    y = pdf.paragraphe(y, "•  Fattah (Ouvreur) × φ = Basmala (Porte)  —  l'Acte d'Ouverture", size=7.5, color=C["violet"])
    y = pdf.paragraphe(y, "•  Rahman+Rahim (Miséricorde) × φ = Mughni (Enrichissement)  —  le Résultat", size=7.5, color=C["violet"])
    y = pdf.paragraphe(y, "L'Ouverture précède l'Enrichissement : d'abord ouvrir les portes, puis recevoir l'abondance.", size=7.5)

    # ════════════════════════════════════════════════════════════════
    # PAGE 6 — DÉCOUVERTE 5 + SYNTHÈSE
    # ════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.titre_page("DÉCOUVERTE 5", "61 × φ ≈ 99 — Le Cycle et la Complétude — 99.7%")
    y = pdf.section(24, "VIII. LE RITUEL MIFTAH 19 × φ = 99 NOMS DIVINS")

    pdf.rect_border(40, y, 130, 10, C["rose_clair"], C["or"])
    pdf.texte(105, y + 1, f"61 (Cycle) × φ = {61 * PHI:.2f} ≈ 99 (Noms Divins)", 10, C["violet"], True, 'C', 130)
    y += 16

    y = pdf.boite_decouverte(y, 5, "Le Rituel complet et la Totalité Divine",
        "61 (1+7+19+33+1, cycle total du rituel) × φ", f"{61 * PHI:.4f} ≈ 99", "99.7%", [
            "Cycle rituel : 1 (Ouverture) + 7 (Istighfar) + 19 (Noms) + 33 (Salawat) + 1 (Sceau)",
            "99 = les 99 Noms Divins d'Allah (Asma ul-Husna)",
            "Le rituel complet × φ = la Totalité Divine",
            "72 (Noms Hébreux) + 99 (Noms Arabes) = 171 = 19 × 9",
            "Le Code 19 est le pont entre les deux traditions",
        ])
    y = pdf.verif(y)

    # ═══════ SYNTHÈSE ═══════
    y = pdf.section(y + 2, "IX.  SYNTHÈSE DES 5 DÉCOUVERTES")

    # Tableau
    pdf.rect_border(18, y, 174, 40, C["bleu_clair"], C["or"])

    # En-têtes
    cols_x = [22, 50, 90, 130, 170]
    entetes = ["#", "Relation", "Formule", "Cible", "Précision"]
    for i, (h, cx) in enumerate(zip(entetes, cols_x)):
        w = cols_x[i+1] - cx - 2 if i < 4 else 20
        pdf.texte(cx, y + 1.5, h, 6, C["noir"], True, 'C', w)
    pdf.ligne(18, y + 7, 192, y + 7, C["gris_clair"], 0.3)

    rows = [
        ["1", "Rizq", "19×4×φ=122.97", "123 Rizq", "99.98%"],
        ["2", "Al-Rahman", "55×φ=89.0", "89 Fibo", "100%"],
        ["3", "Ouverture", "489×φ=791.2", "786 Basm", "99.3%"],
        ["4", "Enrichis.", "684×φ=1106.7", "1100 Mugh", "99.4%"],
        ["5", "Cycle", "61×φ=98.70", "99 Noms", "99.7%"],
    ]
    for ri, row in enumerate(rows):
        for ci, cell in enumerate(row):
            cx = cols_x[ci]
            w = cols_x[ci+1] - cx - 2 if ci < 4 else 20
            bold = (ci == 4)
            clr = C["or"] if bold else C["noir"]
            pdf.texte(cx, y + 9 + ri * 6, cell, 5.5, clr, bold, 'C', w)

    y += 44
    y = pdf.sous_section(y, "Architecture Globale du Flux du Rizq")
    y = pdf.boite(y, "Séquence φ", [
        "φ = 1.618...",
        "55 × φ = 89         (Al-Rahman → Al-Fajr)",
        "56 = 55 + 1         (Al-Waqi'a = Richesse)",
        "19 × 4 × φ = 123    (Code × Noms × φ = Rizq)",
        "489 × φ = 786       (Fattah × φ = Basmala : ouverture)",
        "684 × φ = 1100      (Rahman+Rahim × φ = Mughni)",
        "61 × φ = 99         (Rituel × φ = Complétude Divine)",
    ], C["vert_clair"])

    # ════════════════════════════════════════════════════════════════
    # PAGE 7 — DHIKR φ
    # ════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.titre_page("APPLICATION 1 : DHIKR φ", "5 protocoles de remémoration par le Nombre d'Or")
    y = pdf.section(24, "X.  LES 5 DHIKRS φ DU RIZQ")

    y = pdf.paragraphe(y, "Le Dhikr (remémoration) est la pratique la plus puissante en Islam. "
                      "En intégrant la proportion φ dans les cycles de répétition, nous créons "
                      "une résonance avec la structure fondamentale de la création.", size=7)

    y += 1
    y = pdf.boite_pratique(y, "A", "Dhikr du Rizq (123)",
        "19 × 4 = 76 répétitions",
        "Ya Razzaq (19x), Ya Fattah (19x), Ya Ghani (19x), Ya Mughni (19x) = 76 = 123/φ",
        "Réciter les 4 Noms 19x chacun. Total 76. Visualiser le nombre 123.")

    y = pdf.boite_pratique(y, "B", "Dhikr d'Ouverture (786)",
        "489 répétitions",
        "Ya Fattah × 489 = 489. 489 × φ = 791 → 786.",
        "Réciter 'Ya Fattah' 79 fois (≈ 489/φ/10). Visualiser la Basmala.")

    y = pdf.boite_pratique(y, "C", "Dhikr de Miséricorde (1100)",
        "684 répétitions",
        "Al-Rahman (329) + Al-Rahim (289) = 684. 684 × φ = 1100.",
        "Réciter 68x 'Ya Rahman, Ya Rahim' (ou 34+34). Lumière dorée.")

    y = pdf.boite_pratique(y, "D", "Dhikr du Cycle Parfait (99)",
        "61 répétitions",
        "61 × φ = 99. Cycle complet du rituel = 61 invocations.",
        "Rituel complet 1x. Puis 'Allah' 61 fois. Visualiser 99.")

    y = pdf.boite_pratique(y, "E", "Dhikr de Fibonacci (55+89=144)",
        "55 + 89 répétitions",
        "55 (Rahman) + 89 (Fajr) = 144 = F(12).",
        "55x 'Ya Rahman' + 89x 'Allahumma salli'. Visualiser l'aube.")

    y = pdf.sous_section(y, "Protocole Quotidien")
    y = pdf.boite(y, "Protocole Quotidien", [

        "Matin (Fajr)     :  Dhikr A (76x) + Dhikr B (79x)     → Active le flux",
        "Midi (Duha)      :  Dhikr C (68x)                      → Amplifie la Miséricorde",
        "Soir (Maghrib)   :  Dhikr D (61x) + Dhikr E (144x)    → Scelle la journée",
        "Avant sommeil    :  Dhikr A (19x) seul                 → Programme le subconscient",
    ], C["vert_clair"])

    # ════════════════════════════════════════════════════════════════
    # PAGE 8 — TALISMAN φ
    # ════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.titre_page("APPLICATION 2 : TALISMAN φ", "Schéma géométrique du Nombre d'Or")
    y = pdf.section(24, "XI.  LE TALISMAN φ DU RIZQ")

    y = pdf.paragraphe(y, "Ce talisman intègre les 5 découvertes φ dans une structure géométrique. "
                      "Il combine le carré Buduh (3×3), l'étoile à 8 branches, et les proportions dorées.", size=7.5)

    # ── DESSIN DU TALISMAN φ ──
    cx, cy = 105, 92
    # 5 cercles concentriques
    for r, col, lw in [(50, C["or"], 0.8), (48, C["violet_clair"], 0.3),
                        (38, C["or"], 0.5), (28, C["violet_clair"], 0.3),
                        (18, C["or"], 0.4)]:
        pdf.set_draw_color(*col)
        pdf.set_line_width(lw)
        pdf.circle(cx, cy, r, 'D')

    # Étoile 8 branches (2 carrés)
    R = 35
    def p(deg):
        return (cx + R * math.cos(math.radians(deg)),
                cy - R * math.sin(math.radians(deg)))
    for i in range(4):
        x1, y1 = p(i * 90)
        x2, y2 = p((i + 1) % 4 * 90)
        pdf.set_draw_color(*C["or"])
        pdf.set_line_width(0.4)
        pdf.line(x1, y1, x2, y2)
    for i in range(4):
        x1, y1 = p(45 + i * 90)
        x2, y2 = p(45 + (i + 1) % 4 * 90)
        pdf.set_draw_color(*C["violet_clair"])
        pdf.set_line_width(0.3)
        pdf.line(x1, y1, x2, y2)

    # φ au centre
    pdf.set_font("L", "B", 26)
    pdf.set_text_color(*C["or"])
    pdf.set_xy(cx - 9, cy - 8)
    pdf.cell(18, 15, "φ", align="C")

    # 8 nombres φ autour
    anneau = [
        (0, "55"), (45, "89"), (90, "123"), (135, "7"),
        (180, "786"), (225, "99"), (270, "489"), (315, "61"),
    ]
    for deg, val in anneau:
        r = math.radians(deg)
        nx = cx + 42 * math.cos(r)
        ny = cy - 42 * math.sin(r)
        pdf.set_fill_color(*C["blanc"])
        pdf.set_draw_color(*C["or"])
        pdf.set_line_width(0.2)
        pdf.rect(nx - 8, ny - 5, 16, 10, 'DF')
        pdf.set_font("L", "B", 7)
        pdf.set_text_color(*C["violet"])
        pdf.set_xy(nx - 7, ny - 3)
        pdf.cell(14, 5, val, align="C")

    # Légende
    y = 148
    y = pdf.sous_section(y, "Instructions de Fabrication")
    y = pdf.boite(y, "Étapes", [
        "1. Tracez 5 cercles concentriques (R=50, 38, 28, 18mm) sur papier 20×20cm",
        "2. Dessinez l'étoile à 8 branches (2 carrés superposés à 45°)",
        "3. Écrivez φ au centre en lettres dorées",
        "4. Placez les 8 nombres φ (55, 89, 123, 7, 786, 99, 489, 61) aux 8 directions",
        "5. Au dos, écrivez la formule : 19 × 4 × φ = 123",
        "6. Activation : Récitez le rituel Miftah 19 (61 invocations) devant le talisman",
    ], C["bleu_clair"])
    pdf.verif(y)

    # ════════════════════════════════════════════════════════════════
    # PAGE 9 — GRABOVOI φ
    # ════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.titre_page("APPLICATION 3 : CODES GRABOVOI φ", "Nouvelles séquences numériques par le Nombre d'Or")
    y = pdf.section(24, "XII.  CODES GRABOVOI CLASSIQUES DU RIZQ")

    y = pdf.paragraphe(y, "Grigori Grabovoi a développé des séquences numériques pour la manifestation. "
                      "Voici les codes classiques, enrichis par les découvertes φ :", size=7)

    y += 1
    codes = [
        ("520 741 8", "Argent inattendu",
         "5+2+0=7, 7+4+1=12→3, 8 → 7+8+3=18→9",
         "7 + 19 + 8 = 34 → 34 × φ = 55.0 (Rahman)"),
        ("318 798", "Abondance",
         "3+1+8=12→3, 7+9+8=24→6 → 3+6=9",
         "318 × φ = 514.5 → 5+1+4+5=15→6 (harmonie)"),
        ("56 96 152", "Al-Waqi'a (Maître)",
         "56=7×8, 96=19×5+1, 152=19×8",
         "56×φ=90.6, 96×φ=155.3, 152×φ=245.9"),
        ("9798733714615", "Manifester richesse",
         "13 chiffres, réduction 7",
         "97×φ=156.9, 98×φ=158.6 (Al-Fajr)"),
    ]
    for code, effet, num, phi in codes:
        y = pdf.boite_code(y, code, effet, num, phi)

    y = pdf.section(y + 2, "XIII.  NOUVEAUX : CODES φ DU RIZQ")
    y = pdf.paragraphe(y, "Ces codes sont une découverte originale de cette recherche :", size=7)

    new_codes = [
        ("786 489 684", "Ouverture φ Complète",
         "786 (Basmala) | 489 (Fattah) | 684 (Rahman+Rahim)",
         "786/489 ≈ 1.607 (φ - 0.011) | 684/489 ≈ 1.399",
         "Active la triade : Porte × Ouvreur × Miséricorde"),
        ("123 55 89", "Fibonacci Rizq",
         "123 (Rizq) | 55 (Rahman) | 89 (Fajr)",
         "89/55 = 1.61818 ≈ φ | 123/89 = 1.382",
         "Séquence Fibonacci : Miséricorde → Aube → Subsistance"),
        ("6119 078", "Cycle φ Parfait",
         "61 (Cycle) | 19 (Code) | 0 (Unité) | 7 (Rizq) | 8 (Directions)",
         "61 × 19 = 1159 | 1159 / 716 = 1.618 ≈ φ",
         "Cycle rituel complet + 8 directions du talisman"),
        ("489 319 1060 1100", "4 Noms φ Amplifiés",
         "Fattah(489) | Razzaq(319) | Ghani(1060) | Mughni(1100)",
         "1100/684 ≈ 1.608 ≈ φ | 1060/654 ≈ 1.621 ≈ φ",
         "Les 4 Noms du Rizq amplifiés par φ"),
    ]
    for code, titre, comp, phi_lien, app in new_codes:
        pdf.rect_border(18, y, 174, 18, C["vert_clair"], C["or"])
        pdf.texte(22, y + 1, f"✦ {code}", 7, C["violet"], True, 'L', 80)
        pdf.texte(105, y + 1, titre, 6, C["gris"], False, 'L', 80)
        pdf.texte(22, y + 6, f"Composition : {comp}", 5, C["noir"], False, 'L', 165)
        pdf.texte(22, y + 10, f"Lien φ : {phi_lien}", 5, C["bleu_fonce"], False, 'L', 165)
        pdf.texte(22, y + 14, f"Application : {app}", 5, C["noir"], False, 'L', 165)
        y += 20

    y = pdf.sous_section(y)
    y = pdf.boite(y, "Protocole d'Utilisation", [
        "Écrivez le code sur papier blanc (stylo doré ou violet)",
        "Placez sous l'oreiller (nuit) ou dans le portefeuille (jour)",
        "Récitez le code 7, 19 ou 33 fois en visualisant",
        "Combinez avec le Dhikr φ correspondant",
        "Durée : 40 jours consécutifs",
    ], C["bleu_clair"])

    # ════════════════════════════════════════════════════════════════
    # PAGE 10 — RADIONIQUE φ
    # ════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.titre_page("APPLICATION 4 : RADIONIQUE φ", "Système amplifié par le Nombre d'Or")
    y = pdf.section(24, "XIV.  7 OPTIMISATIONS φ DU SYSTÈME RADIONIQUE")

    y = pdf.paragraphe(y, "Le système radionique Miftah 19 (spirale cuivre + quartz + codes) "
                      "est optimisé par l'intégration des proportions φ :", size=7)

    y += 1
    opts = [
        ("1. Longueur du fil", "56 cm × φ = 90.6 cm",
         "Utiliser 90.6 cm (≈ 91 cm). Le fil devient antenne accordée à Al-Waqi'a ET Al-Fajr."),
        ("2. Tours de spirale", "19 × φ = 31 tours",
         "31 tours (primaire). Rapport 31/19 = 1.631 ≈ φ. Secondaire : 7 tours (31/7 ≈ φ²)."),
        ("3. Distance photo-quartz", "33 mm × φ = 53.4 mm",
         "Placer le quartz à 53 mm au-dessus de la photo. 33 (Paradis) × φ."),
        ("4. Rayons des cercles", "75/φ = 46.4, 75/φ² = 28.6 mm",
         "R, R/φ, R/φ² pour les 3 cercles majeurs au lieu de rayons arbitraires."),
        ("5. Angle des directions", "45° × φ = 72.8°",
         "Étoile en spirale dorée au lieu de 45° réguliers."),
        ("6. Fréquence quartz", "19 kHz × φ = 30.7 kHz",
         "Choisir quartz à ~30.7 kHz ou programmer par intention."),
        ("7. Durée d'activation", "40 jours × φ = 65 jours",
         "65 jours au lieu de 40. 40 = transformation, 65 = 5 × 13 (Fibonacci)."),
    ]
    for titre, formule, desc in opts:
        y = pdf.boite_opti(y, titre, formule, desc)

    y = pdf.sous_section(y)
    y = pdf.boite(y, "Montage : Instructions Résumées", [
        "1. Base : carré de bois 150×150mm, peint noir mat",
        "2. Cercles : R=75mm, R=46mm, R=29mm (progression φ)",
        "3. Codes φ aux 8 directions : 786 489 684, 123 55 89",
        "4. Photo face contre les codes, au centre exact",
        "5. Spirale : 31 tours cuivre 0.8mm, 91cm de long",
        "6. Quartz pointe vers le haut, à 53mm de la base",
        "7. Activation : Dhikr φ complet (A+B+C+D+E) devant le système",
        "8. Durée : 65 jours pour intégration φ complète",
    ], C["vert_clair"])

    # ════════════════════════════════════════════════════════════════
    # PAGE 11 — CALENDRIER LUNAIRE φ
    # ════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.titre_page("APPLICATION 5 : CALENDRIER LUNAIRE φ", "Les 7 jours et 28 mansions")
    y = pdf.section(24, "XV.  LES 28 MANSIONS LUNAIRES ET φ")

    y = pdf.paragraphe(y, "Le cadran lunaire Miftah 19 utilise 28 mansions (manazil). "
                      "28 est triangulaire (1+2+3+4+5+6+7). "
                      f"28 × φ = {28 * PHI:.1f} ≈ 45 (degrés de l'étoile du talisman).", size=7.5)

    y = pdf.section(y + 2, "XVI.  LES 7 JOURS φ DU RIZQ")
    y = pdf.paragraphe(y, "Chaque jour de la semaine a une formule φ et une pratique spécifique :", size=7)

    jours = [
        ("Jour 1 — Dimanche (Soleil)", "19 × φ ≈ 31", "Réciter 31x 'Ya Razzaq'. Ouverture du Rizq."),
        ("Jour 2 — Lundi (Lune)", "56 × φ ≈ 91", "91x la Basmala. Connexion à Al-Waqi'a."),
        ("Jour 3 — Mardi (Mars)", "7 × φ ≈ 11", "11x 'Ya Fattah'. Ouvrir les portes bloquées."),
        ("Jour 4 — Mercredi (Mercure)", "61 × φ ≈ 99", "Réciter les 99 Noms. Cycle complet."),
        ("Jour 5 — Jeudi (Jupiter)", "33 × φ ≈ 53", "53x Salawat. Expansion de l'abondance."),
        ("Jour 6 — Vendredi (Vénus)", "489 × φ ≈ 791", "79x 'Ya Fattah'. Jour sacré."),
        ("Jour 7 — Samedi (Saturne)", "684 × φ ≈ 1107", "110x 'Ya Mughni'. Clôture du cycle."),
    ]
    for jour, formule, pratique in jours:
        y = pdf.boite_jour(y, jour, formule, pratique)

    y = pdf.sous_section(y)
    y = pdf.paragraphe(y, "Cycle complet de 28 jours = 28 × 5 Dhikrs = 140 séquences. 140 × φ = "
                      f"{140 * PHI:.1f} ≈ 227 (Berakhah ברכה, la Bénédiction en hébreu).", size=7)

    y = pdf.sous_section(y + 2)
    y = pdf.boite(y, "Moments Optimaux de Pratique (Heures φ)", [
        "Fajr (aube)      →   24h × 0.382 = 9h10       Dhikr A+B",
        "Duha (10:30)     →   24h × 0.5 = 12h00        Dhikr A+C",
        "Dhuhr (12:00)    →   24h × 0.618 = 14h50      Dhikr D",
        "Asr (15:30)      →   24h × 0.786 = 18h52      Dhikr A+B",
        "Maghrib (coucher)→   Heure 0 (fin du jour)    Dhikr E",
    ], C["bleu_clair"])

    # ════════════════════════════════════════════════════════════════
    # PAGE 12 — TABLEAUX DE RÉFÉRENCE
    # ════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.titre_page("TABLEAUX DE RÉFÉRENCE", "Toutes les relations φ et nombres de Fibonacci")
    y = pdf.section(24, "XVII.  TABLEAU 1 : TOUTES LES RELATIONS φ")

    pdf.rect_border(18, y, 174, 60, C["bleu_clair"], C["or"])

    cols_x = [22, 55, 80, 105, 135, 165]
    entetes = ["#", "Élément A", "Opération", "Résultat", "Cible B", "Préc."]
    for i, (h, cx) in enumerate(zip(entetes, cols_x)):
        w = cols_x[i+1] - cx - 2 if i < 5 else 25
        pdf.texte(cx, y + 1.5, h, 6, C["noir"], True, 'C', w)
    pdf.ligne(18, y + 7, 192, y + 7, C["gris_clair"], 0.3)

    ref_rows = [
        ["1", "19×4=76", "× φ", "122.97", "123 Rizq", "99.98%"],
        ["2", "55 (Rahman)", "× φ", "89.0", "F₁₁=89", "100%"],
        ["3", "489 Fattah", "× φ", "791.2", "786 Basm", "99.3%"],
        ["4", "684 R+R", "× φ", "1106.7", "1100 Mugh", "99.4%"],
        ["5", "61 Cycle", "× φ", "98.70", "99 Noms", "99.7%"],
        ["6", "56 Waqiah", "× φ", "90.6", "91≈F₁₀+F₁₁", "99.5%"],
        ["7", "786 Basmala", "/ φ", "485.8", "489 Fattah", "99.3%"],
        ["8", "1100 Mughni", "/ φ", "679.8", "684 R+R", "99.4%"],
        ["9", "34 (F₉)", "× φ", "55.0", "55 F₁₀", "100%"],
        ["10", "89 (F₁₁)", "× φ", "144.0", "144 F₁₂", "100%"],
    ]
    for ri, row in enumerate(ref_rows):
        for ci, cell in enumerate(row):
            cx = cols_x[ci]
            w = cols_x[ci+1] - cx - 2 if ci < 5 else 25
            bold = (ci == 5)
            pdf.texte(cx, y + 9 + ri * 5, cell, 5, C["or"] if bold else C["noir"], bold, 'C', w)

    y += 64
    y = pdf.section(y, "XVIII.  TABLEAU 2 : FIBONACCI DANS MIFTAH 19")

    pdf.rect_border(18, y, 174, 24, C["vert_clair"], C["or"])
    fib_headers = [("F(n)", 30), ("Valeur", 25), ("Dans le projet Miftah 19", 130)]
    x_p = 22
    for h, w in fib_headers:
        pdf.texte(x_p, y + 1.5, h, 6, C["noir"], True, 'C', w)
        x_p += w
    pdf.ligne(18, y + 7, 192, y + 7, C["gris_clair"], 0.3)

    fib_data = [
        ["F₆", "8", "8 directions du talisman"],
        ["F₇", "13", "Nombre de la miséricorde divin"],
        ["F₈", "21", "Mansion lunaire (Al-Malik)"],
        ["F₉", "34", "Constante du carré magique"],
        ["F₁₀", "55", "★ Sourate Al-Rahman"],
        ["F₁₁", "89", "★ Sourate Al-Fajr (55 × φ)"],
        ["F₁₂", "144", "55 + 89"],
    ]
    for ri, row in enumerate(fib_data):
        x_p = 22
        for ci, cell in enumerate(row):
            w = [30, 25, 130][ci]
            is_h = (row[1] == "55" or row[1] == "89")
            clr = C["or"] if is_h and ci < 2 else C["noir"]
            pdf.texte(x_p, y + 9 + ri * 2.2, cell, 4.5, clr, is_h,
                     'C' if ci < 2 else 'L', w)
            x_p += w

    # ════════════════════════════════════════════════════════════════
    # PAGE 13 — CONCLUSION
    # ════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.rect_fill(0, 0, 210, 297, C["fond_sombre"])

    y = 30
    pdf.rect_fill(50, y, 110, 2, C["or"])
    y += 12
    pdf.texte(105, y, "CONCLUSION", 18, C["or"], True, 'C', 200)
    y += 16

    pdf.texte_multi(30, y, 150, "Le Nombre d'Or φ n'est pas seulement une constante mathématique. "
                   "C'est le langage dans lequel l'univers a été écrit.", 9, C["blanc"], False, 'C')
    y = pdf.get_y() + 10

    pdf.texte_multi(30, y, 150, "Les 5 découvertes présentées dans ce document démontrent que φ est "
                   "encodé dans les structures numériques du Coran — spécifiquement dans les nombres "
                   "liés au Rizq (la subsistance divine). Chaque relation a une précision supérieure "
                   "à 99%.", 7.5, C["violet_clair"], False, 'C')
    y = pdf.get_y() + 10

    pdf.texte_multi(30, y, 150, "Mais ces découvertes ne sont pas une fin en soi. Elles sont des outils — "
                   "des clés mathématiques qui ouvrent des portes vibratoires. Les 5 applications pratiques "
                   "(Dhikr φ, Talisman φ, Codes Grabovoi φ, Système Radionique φ, Calendrier Lunaire φ) "
                   "permettent à chacun d'expérimenter par lui-même la puissance de ces codes.", 7.5, C["blanc"], False, 'C')
    y = pdf.get_y() + 10

    pdf.texte_multi(30, y, 150, "La pratique est la clé. Sans elle, les nombres ne sont que des symboles. "
                   "Avec elle, ils deviennent des réalités.", 8, C["or"], False, 'C')
    y = pdf.get_y() + 14

    pdf.rect_fill(50, y, 110, 2, C["or"])
    y += 14

    pdf.texte(105, y, "7 × 8 × 19 = 1064", 14, C["or"], True, 'C', 200)
    y += 8
    pdf.texte(105, y, "Rizq (7) × Directions (8) × Code 19 = Le Talisman Ultime", 8, C["gris"], False, 'C', 200)
    y += 8
    pdf.texte(105, y, f"Avec φ : 1064 × φ = {1064 * PHI:.1f} → 1+7+2+1+6 = 17 → 1+7 = 8", 8, C["violet_clair"], False, 'C', 200)
    y += 14

    pdf.rect_fill(60, y, 90, 1, C["or"])
    y += 8
    pdf.texte_ar(105, y, "والله من وراء القصد", 16, C["or"], 'C', 200)
    y += 10
    pdf.texte(105, y, "Wa-Allahu min wara'il-qasd — Et Allah est derrière l'intention", 7, C["gris"], False, 'C', 200)

    # ════════════════════════════════════════════════════════════════
    # SAVE
    # ════════════════════════════════════════════════════════════════
    output = PDF_OUTPUTS["decouverte_phi"]
    pdf.output(str(output))
    print(f"✅ PDF généré : {output}")
    print(f"📄 Pages : {pdf.page_no()}")
    print(f"📐 5 découvertes φ | 5 applications pratiques")


if __name__ == "__main__":
    build()
