import os
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

# ── Font paths ──
ARABIC_FONT = "/mnt/c/Windows/Fonts/arial.ttf"  # Arial (full Arabic support)
LATIN_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
LATIN_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def ar(text):
    """Reshape + bidi for Arabic text"""
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

class PDF(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.add_font("Lat", "", LATIN_FONT, uni=True)
        self.add_font("Lat", "B", LATIN_BOLD, uni=True)
        self.add_font("Ar", "", ARABIC_FONT, uni=True)
        self.set_auto_page_break(True, 15)

    def header(self):
        if self.page_no() > 1:
            self.set_font("Lat", "B", 8)
            self.set_text_color(100,100,100)
            self.cell(0, 5, "RITUEL MIFTAH 19 — Clé Mathématique du Rizq", align="C")
            self.ln(8)

    def footer(self):
        self.set_y(-12)
        self.set_font("Lat", "", 7)
        self.set_text_color(150,150,150)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    # ── Helpers ──
    def title_box(self, text):
        self.set_fill_color(15, 23, 42)
        self.set_text_color(255, 215, 0)
        self.set_font("Lat", "B", 16)
        self.cell(0, 10, text, ln=True, align="C", fill=True)
        self.ln(3)

    def subtitle(self, text):
        self.set_text_color(15, 23, 42)
        self.set_font("Lat", "B", 13)
        self.cell(0, 8, text, ln=True)
        self.ln(1)

    def sub_subtitle(self, text):
        self.set_text_color(34, 68, 102)
        self.set_font("Lat", "B", 11)
        self.cell(0, 7, text, ln=True)
        self.ln(1)

    def body(self, text):
        self.set_text_color(40, 40, 40)
        self.set_font("Lat", "", 10)
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def body_ar(self, text):
        self.set_text_color(40, 40, 40)
        self.set_font("Ar", "", 12)
        self.multi_cell(0, 7, ar(text), align="R")
        self.ln(1)

    def gold_line(self):
        self.set_draw_color(255, 215, 0)
        self.set_line_width(0.3)
        x = self.get_x()
        y = self.get_y()
        self.line(x + 10, y, self.w - x - 10, y)
        self.ln(4)

    def table_header(self, cols, widths):
        self.set_fill_color(15, 23, 42)
        self.set_text_color(255, 215, 0)
        self.set_font("Lat", "B", 9)
        for i, col in enumerate(cols):
            self.cell(widths[i], 7, col, border=1, fill=True, align="C")
        self.ln()

    def table_row(self, cells, widths, bold_last=False):
        self.set_text_color(40, 40, 40)
        fill = self.page_no() % 2 == 0
        if fill:
            self.set_fill_color(245, 245, 250)
        for i, cell in enumerate(cells):
            self.set_font("Lat", "B" if bold_last and i == len(cells)-1 else "", 9)
            self.cell(widths[i], 6.5, str(cell), border=1, fill=fill, align="C")
        self.ln()

    def info_box(self, text):
        self.set_fill_color(240, 245, 250)
        self.set_text_color(34, 68, 102)
        self.set_font("Lat", "", 9)
        self.set_x(15)
        x0 = self.get_x()
        y0 = self.get_y()
        self.multi_cell(self.w - 30, 5, text, fill=True)
        self.ln(2)


def build():
    pdf = PDF()
    pdf.alias_nb_pages()

    # ═══════════════════════════════════════
    # PAGE 1 — COUVERTURE + ARCHITECTURE
    # ═══════════════════════════════════════
    pdf.add_page()

    # Fond sombre haut de couv
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(0, 0, 210, 85, "F")

    pdf.set_y(15)
    pdf.set_text_color(255, 215, 0)
    pdf.set_font("Lat", "B", 10)
    pdf.cell(0, 6, "ARCHITECTURE MATHÉMATIQUE DU CORAN", align="C")
    pdf.ln(12)

    pdf.set_font("Lat", "B", 30)
    pdf.cell(0, 12, "RITUEL MIFTAH 19", align="C")
    pdf.ln(16)

    pdf.set_font("Lat", "", 13)
    pdf.set_text_color(200, 200, 220)
    pdf.cell(0, 8, "Cle Mathematique du Rizq", align="C")
    pdf.ln(10)

    pdf.set_draw_color(255, 215, 0)
    pdf.set_line_width(0.5)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(8)

    pdf.set_font("Lat", "", 10)
    pdf.set_text_color(180, 180, 200)
    pdf.cell(0, 6, "Base : Code 19  |  Abjad 786  |  Structure Waqiah 56", align="C")
    pdf.ln(5)
    pdf.cell(0, 6, "Duree : ~2 min/session  |  Frequence : 3-5x/jour", align="C")

    # Bloc chiffres en dessous
    pdf.set_y(90)
    pdf.set_font("Lat", "B", 17)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 10, "Architecture Sacree", align="C")
    pdf.ln(8)

    pdf.set_font("Lat", "B", 14)
    pdf.set_text_color(34, 68, 102)
    pdf.cell(0, 8, "1  ->  7  ->  19  ->  33  ->  1  =  61", align="C")
    pdf.ln(3)
    pdf.set_font("Lat", "", 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, "6+1 = 7  =  Completion Divine", align="C")
    pdf.ln(10)

    # Légende des nombres
    cols = ["Etape", "Nombre", "Signification"]
    widths = [35, 25, 130]
    pdf.table_header(cols, widths)
    pdf.table_row(["1. Ouverture", "1", "Tawhid, Basmala (19 lettres, Abjad 786)"], widths)
    pdf.table_row(["2. Istighfar", "7", "Multiplicateur celeste (2:261) — pluie d'abondance (71:10-12)"], widths)
    pdf.table_row(["3. Noms Divins", "19", "Signature du Coran (74:30) — 114 sourates = 19x6"], widths)
    pdf.table_row(["4. Salawat", "33", "Age du Paradis — Waqiah 56 — Tasbih post-priere"], widths)
    pdf.table_row(["5. Fermeture", "1", "Sceau — Tawakkul absolu"], widths)
    pdf.ln(6)

    pdf.info_box("Chaque nombre est extrait directement du Coran ou de la Sunna. L'architecture 1-7-19-33-1 "
                 "replique la structure mathematique du Code 19 decouvert par Rashad Khalifa (1974). "
                 "Total du cycle : 61. Reduction numerologique : 6+1 = 7, le nombre de la completion divine "
                 "(7 cieux, 7 terres, sourate Fatiha en 7 versets).")

    # ═══════════════════════════════════════
    # PAGE 2 — LE RITUEL COMPLET
    # ═══════════════════════════════════════
    pdf.add_page()
    pdf.title_box("LE RITUEL COMPLET")

    # ── ÉTAPE 1 ──
    pdf.subtitle("ETAPE 1 — OUVERTURE (1x)")
    pdf.gold_line()
    pdf.body("Recite la Basmala une fois, en pleine conscience de son poids mathematique.")
    pdf.info_box("Basmala = 19 lettres  |  Abjad total = 786  |  Al-Rahman (329) + Al-Rahim (289) = 684 = 19 x 36")
    pdf.body_ar("بسم الله الرحمن الرحيم")
    pdf.set_text_color(100, 100, 100)
    pdf.set_font("Lat", "", 9)
    pdf.cell(0, 5, "Intention silencieuse : Par le code de Ta parole, ouvre les portes du Rizq.", align="C")
    pdf.ln(8)

    # ── ÉTAPE 2 ──
    pdf.subtitle("ETAPE 2 — ISTIGHFAR (7x)")
    pdf.gold_line()
    pdf.body("Repete 7 fois. Le chiffre 7 est le multiplicateur divin (2:261) et la cle des pluies d'abondance (71:10-12).")
    pdf.info_box("7 cieux (67:3)  |  1 grain -> 7 epis (2:261)  |  7 = 19 - 12 (lien Code 19)")
    pdf.body_ar("استغفر الله العظيم واتوب اليه")
    pdf.body("7 repetitions, en visualisant une lumiere doree qui descend et nettoie tous les blocages financiers.")

    # ── ÉTAPE 3 ──
    pdf.subtitle("ETAPE 3 — LES 4 NOMS DIVINS DE LA RICHESSE (19x)")
    pdf.gold_line()
    pdf.body("Invoque ces 4 noms en boucle. 4 noms x 4 cycles complets (16) + 3 noms du 5e cycle = 19 invocations.")
    pdf.info_box("19 = signature divine dans le Coran — 74:30 \"Ils sont dix-neuf a y veiller\"")

    cols2 = ["Arabe", "Transcription", "Sens", "Abjad"]
    widths2 = [30, 40, 55, 40]
    pdf.table_header(cols2, widths2)
    pdf.table_row(["يا رزاق", "Ya Razzaq", "Le Pourvoyeur Supreme", "319"], widths2)
    pdf.table_row(["يا فتاح", "Ya Fattah", "L'Ouvreur des portes", "489"], widths2)
    pdf.table_row(["يا غني", "Ya Ghani", "Le Riche Absolu", "1060"], widths2)
    pdf.table_row(["يا مغني", "Ya Mughni", "L'Enrichisseur", "1100"], widths2)
    pdf.ln(4)
    pdf.info_box(f"Somme Abjad des 4 noms : 319 + 489 + 1060 + 1100 = {319+489+1060+1100}. "
                 f"Reduction : 2+9+6+8 = 25 -> 2+5 = 7 (completion).")

    # ── ÉTAPE 4 ──
    pdf.subtitle("ETAPE 4 — SALAWAT (33x)")
    pdf.gold_line()
    pdf.body("33 repetitions. Le hadith rapporte que les gens du Paradis auront 33 ans. "
             "Nombre sacre du Tasbih post-priere (33 Subhanallah, 33 Alhamdulillah, 33 Allahu Akbar).")
    pdf.info_box("33  |  3+3 = 6 (sceau prophetique)  |  Waqiah 56 evoque ce nombre")
    pdf.body_ar("اللهم صل على سيدنا محمد وعلى ال سيدنا محمد")
    pdf.body("En visualisant une connexion directe avec le Prophete (paix sur lui), canal de toute benediction.")

    # ── ÉTAPE 5 ──
    pdf.subtitle("ETAPE 5 — FERMETURE (1x)")
    pdf.gold_line()
    pdf.body("Recite une fois, souffle sur les mains, et passe-les sur le visage pour sceller.")
    pdf.body_ar("حسبنا الله ونعم الوكيل نعم المولى ونعم النصير")
    pdf.set_font("Lat", "B", 10)
    pdf.set_text_color(34, 68, 102)
    pdf.cell(0, 6, "Hasbunallahu wa ni'mal wakeel, ni'mal mawla wa ni'man naseer", align="C")
    pdf.ln(3)
    pdf.set_font("Lat", "", 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, "Allah nous suffit, quel excellent Garant, quel excellent Maitre, quel excellent Secoureur (3:173)", align="C")
    pdf.ln(8)

    # ═══════════════════════════════════════
    # PAGE 3 — PLANNING + VERSION EXPRESS + FONDEMENTS
    # ═══════════════════════════════════════
    pdf.add_page()
    pdf.title_box("PLANNING QUOTIDIEN")

    pdf.body("Le rituel se pratique 3 a 5 fois par jour. Voici le planning optimal :")
    pdf.ln(1)

    cols3 = ["Session", "Moment", "Effet"]
    widths3 = [20, 45, 130]
    pdf.table_header(cols3, widths3)
    pdf.table_row(["1", "Fajr (aube)", "Active le flux de la journee — ouverture du canal"], widths3)
    pdf.table_row(["2", "Duha (matinee)", "Amplifie le rizq en cours — maintient l'elan"], widths3)
    pdf.table_row(["3", "Asr / Maghrib", "Scelle la journee — protection contre la perte"], widths3)
    pdf.table_row(["4*", "Isha (nuit)", "Rituel nocturne Waqiah — barakah profonde (optionnel)"], widths3)
    pdf.table_row(["5*", "Avant sommeil", "Programme le subconscient — semence nocturne (optionnel)"], widths3)
    pdf.ln(4)

    pdf.info_box("* Les sessions 4 et 5 sont optionnelles. Minimum recommande : 3 sessions/jour.")

    # ── VERSION EXPRESS ──
    pdf.ln(4)
    pdf.title_box("VERSION EXPRESS — 60 SECONDES")
    pdf.body("Pour les moments ou le temps manque, cette version condensee preserve l'architecture sacree.")

    pdf.set_fill_color(240, 245, 250)
    pdf.set_text_color(15, 23, 42)
    pdf.set_font("Lat", "B", 10)
    pdf.cell(0, 7, "ARCHITECTURE EXPRESS : 1 + 3 + 7 + 3 + 1 = 15 = 19 - 4", align="C", fill=True)
    pdf.ln(8)

    cols4 = ["Etape", "Formule", "Nb", "Duree"]
    widths4 = [30, 75, 20, 50]
    pdf.table_header(cols4, widths4)
    pdf.table_row(["Ouverture", "Bismillah ir-Rahman ir-Rahim", "1x", "~3s"], widths4)
    pdf.table_row(["Istighfar", "Astaghfirullah al-Azim", "3x", "~12s"], widths4)
    pdf.table_row(["Nom Divin", "Ya Razzaq", "7x", "~15s"], widths4)
    pdf.table_row(["Salawat", "Allahumma salli 'ala Muhammad", "3x", "~10s"], widths4)
    pdf.table_row(["Fermeture", "Hasbunallahu wa ni'mal wakeel", "1x", "~5s"], widths4)
    pdf.ln(4)

    pdf.info_box("Meme en 60 secondes, l'architecture 1-3-7-3-1 preserve le schema mathematique. "
                 "Le total 15 est une reduction du 19 originel (19-4, le 4 etant les noms divins reduits).")

    # ── FONDEMENTS ──
    pdf.ln(4)
    pdf.title_box("FONDEMENTS MATHEMATIQUES")
    pdf.body("Chaque element du rituel est ancre dans les codes numeriques du Coran :")

    cols5 = ["Element", "Valeur Numerique", "Source Coranique"]
    widths5 = [45, 55, 95]
    pdf.table_header(cols5, widths5)
    pdf.table_row(["Basmala", "19 lettres / Abjad 786", "Ouverture de toutes sourates sauf 9"], widths5)
    pdf.table_row(["Sourates du Coran", "114 = 19 x 6", "Structure globale"], widths5)
    pdf.table_row(["Mot 'Rizq'", "123 occurrences", "Reparti dans tout le Coran"], widths5)
    pdf.table_row(["YaSeen (S.36)", "ي237 + س48 = 285 = 19x15", "Sourate Ya-Sin"], widths5)
    pdf.table_row(["Waqiah (S.56)", "56 + 96 versets = 152", "Sourate de la Richesse"], widths5)
    pdf.table_row(["Multiplicateur", "1 -> 7 epis x 100 = 700", "Sourate 2:261"], widths5)
    pdf.table_row(["Al-Rahman + Al-Rahim", "329 + 289 = 684 = 19x36", "Gematria Basmala"], widths5)
    pdf.table_row(["Noms Allah + Al-Rahman + Al-Rahim", "66 + 329 + 289 = 684 = 19x36", "Gematria Basmala"], widths5)
    pdf.ln(6)

    # ── RECAP VISUEL ──
    pdf.title_box("RECAPITULATIF VISUEL")

    pdf.set_font("Lat", "B", 12)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 8, "CYCLE QUOTIDIEN COMPLET", align="C")
    pdf.ln(10)

    # Schéma ASCII-like des cycles
    pdf.set_font("Lat", "B", 10)
    pdf.set_text_color(34, 68, 102)
    schema = [
        "    1x BASMALA (Ouverture)",
        "          |",
        "    7x ISTIGHFAR (Purification)",
        "          |",
        "   19x NOMS DIVINS (Activation)",
        "          |",
        "   33x SALAWAT (Connexion)",
        "          |",
        "    1x TAWAKKUL (Sceau)",
    ]
    for line in schema:
        pdf.cell(0, 6.5, line, align="C")
        pdf.ln()
    pdf.ln(4)

    pdf.info_box(
        f"Total numerique du rituel complet : 1 + 7 + 19 + 33 + 1 = 61 invocations.\n"
        f"Reduction : 6 + 1 = 7 (completion).\n"
        f"En 3 sessions/jour : 61 x 3 = 183 invocations. Reduction : 1+8+3 = 12 -> 1+2 = 3 (equilibre).\n"
        f"En 5 sessions/jour : 61 x 5 = 305 invocations. Reduction : 3+0+5 = 8 (infini)."
    )

    # ═══════════════════════════════════════
    # PAGE 5 — TALISMAN MIFTAH 19
    # ═══════════════════════════════════════
    pdf.add_page()
    pdf.title_box("TALISMAN MIFTAH 19 — A DESSINER")

    pdf.body("Ce talisman concentre les codes sacres du rituel en un schema geometrique. "
             "A reproduire sur papier, a garder sur soi, ou a placer dans son espace de travail.")

    pdf.set_text_color(100, 100, 100)
    pdf.set_font("Lat", "", 8)
    pdf.cell(0, 5, "Dimensions recommandees : carre de 15x15 cm  |  Encre doree ou noire sur fond blanc", align="C")
    pdf.ln(8)

    # ── TALISMAN DRAWING ──
    cx, cy = 105, 190   # center
    pdf.set_line_width(0.3)

    # Outer ring 1 — ∞
    pdf.set_draw_color(15, 23, 42)
    r = 55
    step = 1.5 * 3.14159 / 180  # ~1.5 deg
    for i in range(360):
        angle = i * 3.14159 / 180
        ri = r + 1.5 * (i % 3)
        x = cx + ri * (i % 180) * 0.005 if i < 180 else ri
        x = cx + ri * (0.0001)

    # Outer circle
    pdf.set_draw_color(15, 23, 42)
    pdf.set_line_width(1.2)
    pdf.ellipse(cx - 55, cy - 55, 110, 110, "D")
    pdf.ellipse(cx - 57, cy - 57, 114, 114, "D")

    # Middle ring
    pdf.set_line_width(0.5)
    pdf.set_draw_color(34, 68, 102)
    pdf.ellipse(cx - 43, cy - 43, 86, 86, "D")
    pdf.set_line_width(0.3)
    pdf.ellipse(cx - 45, cy - 45, 90, 90, "D")

    # Inner ring
    pdf.set_draw_color(15, 23, 42)
    pdf.set_line_width(0.8)
    pdf.ellipse(cx - 30, cy - 30, 60, 60, "D")

    # 8-pointed star (2 squares rotated)
    pdf.set_draw_color(255, 215, 0)
    pdf.set_line_width(0.6)
    sq1 = 27
    sq2 = 27 * 0.707  # same radius, rotated 45
    pdf.line(cx, cy - sq1, cx + sq1, cy)
    pdf.line(cx + sq1, cy, cx, cy + sq1)
    pdf.line(cx, cy + sq1, cx - sq1, cy)
    pdf.line(cx - sq1, cy, cx, cy - sq1)

    pdf.set_draw_color(34, 68, 102)
    d2 = 19
    pdf.line(cx + d2, cy - d2, cx - d2, cy - d2)
    pdf.line(cx - d2, cy - d2, cx - d2, cy + d2)
    pdf.line(cx - d2, cy + d2, cx + d2, cy + d2)
    pdf.line(cx + d2, cy + d2, cx + d2, cy - d2)

    # Center number
    pdf.set_font("Lat", "B", 22)
    pdf.set_text_color(255, 215, 0)
    pdf.set_xy(cx - 10, cy - 6)
    pdf.cell(20, 10, "19", align="C")

    # Inner circle numbers (4 cardinal directions)
    pdf.set_font("Lat", "B", 11)
    pdf.set_text_color(15, 23, 42)
    ir = 22
    positions = [
        (cx, cy - ir, "1", "C"),
        (cx + ir, cy, "7", "L"),
        (cx, cy + ir, "33", "C"),
        (cx - ir, cy, "786", "R"),
    ]
    for px, py, txt, al in positions:
        w = 14 if len(txt) <= 2 else 22
        pdf.set_xy(px - w/2 if al == "C" else px - w if al == "R" else px, py - 5)
        pdf.cell(w, 8, txt, align=al if al != "R" else "R")

    # 8 names around middle ring
    pdf.set_font("Ar", "", 12)
    pdf.set_text_color(15, 23, 42)
    names = [
        (cx, cy - 37, ar("يا فتاح")),
        (cx + 26, cy - 26, ar("يا غني")),
        (cx + 37, cy, ar("يا رزاق")),
        (cx + 26, cy + 26, ar("يا مغني")),
        (cx, cy + 37, ar("يا وهّاب")),
        (cx - 26, cy + 26, ar("يا كريم")),
        (cx - 37, cy, ar("يا باسط")),
        (cx - 26, cy - 26, ar("يا لطيف")),
    ]
    for px, py, txt in names:
        pdf.set_xy(px - 14, py - 5)
        pdf.cell(28, 8, txt, align="C")

    # Outer ring text — Basmala in circle
    pdf.set_font("Ar", "", 10)
    pdf.set_text_color(34, 68, 102)
    outer_texts = [
        (cx, cy - 52, ar("بسم الله")),
        (cx + 37, cy - 37, ar("الرحمن")),
        (cx + 52, cy, ar("الرحيم")),
        (cx + 37, cy + 37, ar("ملك")),
        (cx, cy + 52, ar("القدوس")),
        (cx - 37, cy + 37, ar("السلام")),
        (cx - 52, cy, ar("المؤمن")),
        (cx - 37, cy - 37, ar("المهيمن")),
    ]
    for px, py, txt in outer_texts:
        pdf.set_xy(px - 10, py - 4)
        pdf.cell(20, 6, txt, align="C")

    # ── LEGEND BELOW TALISMAN ──
    pdf.set_y(260)
    pdf.gold_line()

    pdf.subtitle("GUIDE DE CONSTRUCTION")

    cols6 = ["Couche", "Element", "Signification"]
    widths6 = [28, 55, 112]
    pdf.table_header(cols6, widths6)
    pdf.table_row(["Anneau 1", "Noms divins (8)", "Basmala + 7 attributs de protection"], widths6)
    pdf.table_row(["Anneau 2", "4 noms de richesse", "Razzaq, Fattah, Ghani, Mughni + 4 noms de flux"], widths6)
    pdf.table_row(["Etoile", "8 branches", "8 directions du Rizq"], widths6)
    pdf.table_row(["Croix", "4 nombres cardinaux", "1 (Est) — 7 (Sud) — 33 (Ouest) — 786 (Nord)"], widths6)
    pdf.table_row(["Centre", "19", f"Signature divine du Coran — 74:30 — {19}x5 (cycles) = 95"], widths6)
    pdf.ln(4)

    pdf.info_box(
        "Dessiner ce talisman sur un papier de 15x15 cm.\n"
        "1. Tracer les 3 cercles concentriques au compas (rayons : 27, 43, 55 mm)\n"
        "2. Tracer l'etoile a 8 branches : 2 carres decales de 45 degres\n"
        "3. Inscrire les nombres et les noms aux positions indiquees\n"
        "4. Activer par recitation du rituel Miftah 19 complet\n"
        "5. Conserver sur soi (portefeuille) ou placer dans l'espace de travail\n\n"
        "Nettoyage energetique : exposer au premier soleil du vendredi (Fajr)."
    )

    # ── SIMPLIFIED VERSION (TEXT-BASED) ──
    pdf.ln(2)
    pdf.title_box("VERSION SIMPLIFIEE — TALISMAN TEXTE")

    pdf.body("Si le dessin geometrique est trop complexe, voici une version textuelle "
             "a ecrire en calligraphie dans un cercle :")

    pdf.set_fill_color(245, 245, 250)
    pdf.set_font("Lat", "", 11)
    pdf.set_text_color(15, 23, 42)

    talisman_text = [
        "",
        "                    ╔══════════════════════════════╗",
        "                    ║     بسم الله الرحمن الرحيم    ║",
        "                    ║                              ║",
        "                    ║   يا رزاق  يا فتاح  يا غني   ║",
        "                    ║           يا مغني            ║",
        "                    ║        1 — 19 — 7           ║",
        "                    ║          786 — 33           ║",
        "                    ║     استغفر الله العظيم       ║",
        "                    ║ حسبنا الله ونعم الوكيل       ║",
        "                    ╚══════════════════════════════╝",
        "",
    ]
    for line in talisman_text:
        pdf.set_font("Ar" if any('\u0600' <= c <= '\u06ff' or '\u0750' <= c <= '\u077f' for c in line) else "Lat", "", 11)
        pdf.cell(0, 6, line, align="C")
        pdf.ln()

    # ── NUMERICAL TABLE OF TALISMAN ──
    pdf.ln(3)
    pdf.subtitle("CARRE MAGIQUE DU RIZQ (3x3)")
    pdf.body("Disposer ces 9 nombres dans une grille 3x3. Toutes les lignes tendent vers le meme noyau :")

    # Magic square data
    magic = [
        ["786", "19", "1"],
        ["7", "61", "33"],
        ["123", "56", "96"],
    ]
    row_sums = [sum(int(x) for x in r) for r in magic]
    col_sums = [sum(int(magic[r][c]) for r in range(3)) for c in range(3)]

    # Draw magic square
    sq_size = 15
    sx, sy_base = 60, pdf.get_y() + 5
    pdf.set_fill_color(15, 23, 42)
    pdf.set_text_color(255, 215, 0)
    pdf.set_font("Lat", "B", 12)
    for r in range(3):
        for c in range(3):
            x = sx + c * sq_size
            y = sy_base + r * sq_size
            fill = (r == 1 and c == 1)  # center highlighted
            if fill:
                pdf.set_fill_color(255, 215, 0)
                pdf.set_text_color(15, 23, 42)
            else:
                pdf.set_fill_color(15, 23, 42)
                pdf.set_text_color(255, 215, 0)
            pdf.set_xy(x, y)
            pdf.cell(sq_size, sq_size, magic[r][c], border=1, fill=True, align="C")

    pdf.set_y(sy_base + 3 * sq_size + 5)
    pdf.set_font("Lat", "", 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, f"Sommes lignes : {row_sums}  |  Sommes colonnes : {col_sums}  |  Centre : 61  |  Reduction : 6+1 = 7", align="C")
    pdf.ln(5)

    pdf.info_box(
        "786 = Basmala (ouverture)\n"
        "19 = Signature divine (74:30)\n"
        "1 = Tawhid (unicite)\n"
        "7 = Multiplicateur (2:261)\n"
        "61 = Total du cycle (1+7+19+33+1)\n"
        "33 = Age du Paradis\n"
        "123 = Occurrences 'Rizq' dans le Coran\n"
        "56 = Sourate Waqiah (richesse)\n"
        "96 = Versets de Waqiah\n\n"
        "Ce carre est un miroir mathematique : somme des 9 nombres = 1182.\n"
        "Reduction : 1+1+8+2 = 12 -> 1+2 = 3 (Trinite du Rizq : quete + gratitude + confiance)."
    )

    # ── SAVE ──
    output = PDF_OUTPUTS["rituel_miftah"]
    pdf.output(str(output))
    print(f"PDF genere : {output}")
    print(f"Pages : {pdf.page_no()}")


if __name__ == "__main__":
    build()
