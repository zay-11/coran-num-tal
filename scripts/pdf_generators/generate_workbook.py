import os, random
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

# ── FONTS ──
LATIN = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
LATIN_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
ARABIC = "/mnt/c/Windows/Fonts/arial.ttf"

def ar(text):
    return get_display(arabic_reshaper.reshape(text))

# ── PALETTE MYSTIQUE ──
DARK_VIOLET = (75, 0, 130)
NIGHT_BLUE = (25, 25, 112)
BRIGHT_VIOLET = (138, 43, 226)
SKY_BLUE = (135, 206, 250)
GOLD = (255, 215, 0)
CREAM = (255, 250, 240)
LIGHT_VIOLET = (230, 230, 250)
MIDNIGHT = (15, 15, 45)
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (100, 100, 100)

# ── CITATIONS CORAN (bas de page) ──
CITATIONS = [
    ("Et Nous avons certes facilite le Coran pour le rappel. Y a-t-il donc quelqu'un pour se rappeler?", "54:17"),
    ("Dis: C'est mon Seigneur qui m'etend Ses faveurs.", "27:40"),
    ("Quiconque craint [Allah], Il lui ouvre une issue, et lui accorde Ses ressources par voies insoupconnees.", "65:2-3"),
    ("Allah dilate et restreint la subsistance a qui Il veut.", "13:26"),
    ("En verite, en cela il y a des signes pour ceux qui reflechissent.", "13:3"),
    ("Et certes, Nous avons facilite le Coran pour le rappel. Y a-t-il donc quelqu'un pour se rappeler?", "54:22"),
    ("Quiconque craint [Allah], Il lui ouvre une issue, et lui accorde Ses ressources par voies insoupconnees.", "65:2-3"),
    ("Allah dilate et restreint la subsistance a qui Il veut.", "13:26"),
    ("C'est Lui qui fait descendre la pluie du ciel.", "30:48"),
    ("Qu'Il accorde la science a qui Il veut.", "2:269"),
    ("Quiconque fait le bien, qu'il soit male ou femelle, etant croyant, Nous lui ferons vivre une vie heureuse.", "16:97"),
    ("Car avec les difficultes, il y a facilite.", "94:5"),
    ("Certes mon Seigneur etend Ses provisions a qui Il veut.", "11:6"),
    ("Et demeurez dans vos demeures et ne vous montrez pas comme les infideles d'autrefois.", "33:33"),
    ("O vous qui croyez! Cherchez secours dans l'endurance et la Salat.", "2:153"),
    ("Car c'est Allah qui est le Meilleur des pourvoyeurs.", "62:11"),
    ("Et Il trouvera Ses ressources la ou il ne s'y attend pas.", "65:3"),
    ("Quiconque craint [Allah], Il lui ouvre une issue.", "65:2"),
    ("Dis: Seul Allah detient la maitrise absolue.", "6:57"),
    ("Certes, avec la difficulte vient la facilite.", "94:6"),
    ("Et Nous avons certes facilite le Coran pour le rappel.", "54:32"),
    ("Lui appartient tout ce qui est dans les cieux et sur la terre.", "2:284"),
    ("Allah accorde Ses faveurs a qui Il veut.", "2:212"),
    ("Quiconque craint [Allah], Il lui ouvre une issue.", "65:2"),
    ("Et Nous avons certes facilite le Coran pour le rappel.", "54:40"),
    ("Car c'est Allah qui est le Meilleur des pourvoyeurs.", "62:11"),
    ("Lui appartient tout ce qui est dans les cieux et sur la terre.", "2:284"),
    ("Et Il trouvera Ses ressources la ou il ne s'y attend pas.", "65:3"),
    ("Quiconque craint [Allah], Il lui ouvre une issue.", "65:2"),
    ("Certes, avec la difficulte vient la facilite.", "94:6"),
]

class Workbook(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.add_font("L", "", LATIN, uni=True)
        self.add_font("L", "B", LATIN_B, uni=True)
        self.add_font("A", "", ARABIC, uni=True)
        self.set_auto_page_break(True, 18)
        self.page_count = 0

    def header(self):
        if self.page_count > 0:
            self.set_font("L", "", 7)
            self.set_text_color(150, 150, 180)
            self.cell(0, 4, "Workbook Miftah 19  |  Numerologie Sacree du Coran", align="R")
            self.ln(2)
            self.set_draw_color(GOLD[0], GOLD[1], GOLD[2])
            self.set_line_width(0.2)
            self.line(15, self.get_y(), self.w - 15, self.get_y())
            self.ln(2)

    def footer(self):
        self.set_y(-16)
        # Gold line
        self.set_draw_color(GOLD[0], GOLD[1], GOLD[2])
        self.set_line_width(0.2)
        self.line(15, self.get_y(), self.w - 15, self.get_y())
        self.ln(1.5)
        # Citation
        idx = min(self.page_count - 1, len(CITATIONS) - 1) if self.page_count > 0 else 0
        text, ref = CITATIONS[idx]
        self.set_font("L", "", 7)
        self.set_text_color(120, 120, 150)
        self.cell(0, 3.5, f"\"{text}\"  |  {ref}", align="C")
        self.ln(3.5)
        # Page number
        self.set_font("L", "", 7)
        self.set_text_color(100, 100, 130)
        self.cell(0, 3, f"Page {self.page_no()}", align="C")

    def new_page(self):
        self.add_page()
        self.page_count += 1

    def bg_dark(self):
        self.set_fill_color(MIDNIGHT[0], MIDNIGHT[1], MIDNIGHT[2])
        self.rect(0, 0, 210, 297, "F")

    def bg_violet(self):
        self.set_fill_color(40, 20, 60)
        self.rect(0, 0, 210, 297, "F")

    def bg_light(self):
        self.set_fill_color(CREAM[0], CREAM[1], CREAM[2])
        self.rect(0, 0, 210, 297, "F")

    def title_cover(self, text, size=28, color=GOLD):
        self.set_font("L", "B", size)
        self.set_text_color(color[0], color[1], color[2])
        self.cell(0, 14, text, align="C")
        self.ln()

    def subtitle_cover(self, text, size=13):
        self.set_font("L", "", size)
        self.set_text_color(200, 200, 220)
        self.cell(0, 7, text, align="C")
        self.ln()

    def section_title(self, text):
        self.set_font("L", "B", 16)
        self.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
        self.cell(0, 10, text, align="L")
        self.ln(2)
        self.set_draw_color(GOLD[0], GOLD[1], GOLD[2])
        self.set_line_width(0.4)
        self.line(15, self.get_y(), 60, self.get_y())
        self.ln(5)

    def sub_title(self, text):
        self.set_font("L", "B", 12)
        self.set_text_color(NIGHT_BLUE[0], NIGHT_BLUE[1], NIGHT_BLUE[2])
        self.cell(0, 8, text, align="L")
        self.ln(2)

    def body_text(self, text, size=10, color=(40,40,40)):
        self.set_font("L", "", size)
        self.set_text_color(color[0], color[1], color[2])
        self.multi_cell(0, 5.2, text)
        self.ln(1)

    def body_ar(self, text, size=11):
        self.set_font("A", "", size)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 6, ar(text), align="R")
        self.ln(1)

    def quote_box(self, text):
        self.set_fill_color(LIGHT_VIOLET[0], LIGHT_VIOLET[1], LIGHT_VIOLET[2])
        self.set_draw_color(BRIGHT_VIOLET[0], BRIGHT_VIOLET[1], BRIGHT_VIOLET[2])
        self.set_text_color(NIGHT_BLUE[0], NIGHT_BLUE[1], NIGHT_BLUE[2])
        self.set_font("L", "B", 9)
        self.set_x(20)
        self.multi_cell(self.w - 40, 5, text, border=1, fill=True)
        self.ln(3)

    def number_box(self, num, label):
        self.set_fill_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
        self.set_text_color(GOLD[0], GOLD[1], GOLD[2])
        self.set_font("L", "B", 14)
        self.cell(22, 12, str(num), border=1, fill=True, align="C")
        self.set_text_color(40, 40, 40)
        self.set_font("L", "", 9)
        self.cell(0, 12, f"  {label}", align="L")
        self.ln()

    def two_col(self, left, right):
        self.set_font("L", "", 9)
        self.set_text_color(40, 40, 40)
        y = self.get_y()
        self.set_xy(15, y)
        self.multi_cell(85, 5, left)
        self.set_xy(110, y)
        self.multi_cell(85, 5, right)
        self.set_xy(15, max(self.get_y(), y + 20))


def build_workbook():
    pdf = Workbook()

    # ═══════════════════════════════════════════════════
    # PAGE 1 — COVER
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_violet()
    pdf.set_y(40)
    pdf.set_font("L", "B", 10)
    pdf.set_text_color(GOLD[0], GOLD[1], GOLD[2])
    pdf.cell(0, 8, "O U V R A G E   P R E M I U M", align="C")
    pdf.ln(18)

    pdf.set_font("L", "B", 36)
    pdf.set_text_color(GOLD[0], GOLD[1], GOLD[2])
    pdf.cell(0, 16, "M I F T A H   1 9", align="C")
    pdf.ln(12)

    pdf.set_font("L", "", 14)
    pdf.set_text_color(200, 180, 220)
    pdf.cell(0, 8, "La Numerologie Sacree du Coran", align="C")
    pdf.ln(6)
    pdf.set_font("L", "", 11)
    pdf.set_text_color(180, 160, 200)
    pdf.cell(0, 6, "Divine Names  |  Ritual  |  Talisman", align="C")
    pdf.ln(20)

    pdf.set_draw_color(GOLD[0], GOLD[1], GOLD[2])
    pdf.set_line_width(0.5)
    pdf.line(50, pdf.get_y(), 160, pdf.get_y())
    pdf.ln(12)

    pdf.set_font("L", "", 9)
    pdf.set_text_color(160, 140, 180)
    pdf.cell(0, 5, "Architecture basee sur le Code 19  |  Abjad 786  |  Structure Waqiah 56", align="C")
    pdf.ln(4)
    pdf.cell(0, 5, "Base sur les decouvertes de Rashad Khalifa (1974) et les traditions esoteriques islamiques", align="C")
    pdf.ln(40)

    pdf.set_font("L", "", 8)
    pdf.set_text_color(140, 120, 160)
    pdf.cell(0, 5, "Workbook de 35 pages  |  Edition Mystique  |  2026", align="C")

    # ═══════════════════════════════════════════════════
    # PAGE 2 — TABLE OF CONTENTS
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_light()
    pdf.section_title("T A B L E   D E S   M A T I E R E S")

    toc = [
        ("I.  Introduction a la Numerologie Sacree", 3),
        ("II. Le Code 19 : Signature Divine", 4),
        ("III. La Basmala : Cle d'Ouverture (786)", 5),
        ("IV. Sourate Ya-Sin : Cœur du Coran (36)", 6),
        ("V. Sourate Al-Waqiah : Source du Rizq (56)", 7),
        ("V-bis. Le Code Numerique d'Al-Waqi'a", 8),
        ("VI. Le Mot Rizq : 123 Occurrences", 10),
        ("VII. Gematria et Systeme Abjad", 11),
        ("VIII. Les 4 Noms Divins de la Richesse", 12),
        ("IX. Les 99 Noms Divins : Grille", 13),
        ("X. Architecture du Rituel Miftah 19", 14),
        ("XI. Etape 1 : Ouverture (1x)", 15),
        ("XII. Etape 2 : Istighfar (7x)", 16),
        ("XIII. Etape 3 : Les Noms Divins (19x)", 17),
        ("XIV. Etape 4 : Salawat (33x)", 18),
        ("XV. Etape 5 : Sceau (1x)", 19),
        ("XVI. Planning Quotidien", 20),
        ("XVII. Version Express (60 secondes)", 21),
        ("XVIII. Le Talisman : Vue d'Ensemble", 22),
        ("XIX. Construction du Talisman", 23),
        ("XX. Le Carre Magique du Rizq", 24),
        ("XXI. L'Etoile a 8 Branches", 25),
        ("XXII. Grille de Protection", 26),
        ("XXIII. Advanced Techniques", 27),
        ("XXIV. Les 7 Cieux et le Rizq", 28),
        ("XXV. Synchronicites Numeriques", 29),
        ("XXVI. Meditation et Visualisation", 30),
        ("XXVII. FAQ & Debutants", 31),
        ("XXVIII. Glossaire", 32),
        ("XXIX. Pages de Notes", 33),
        ("XXX. Le Talisman Ultime Miftah 19", 34),
        ("XXXI. Radionique Sacree", 36),
        ("XXXII. Conclusion & Benediction", 37),
    ]

    for title, page in toc:
        pdf.set_font("L", "B", 10)
        pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
        pdf.cell(150, 6, title, align="L")
        pdf.set_font("L", "", 10)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 6, str(page), align="R")
        pdf.ln()

    # ═══════════════════════════════════════════════════
    # PAGE 3 — INTRODUCTION
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_light()
    pdf.section_title("I.  I N T R O D U C T I O N")
    pdf.body_text("Le Coran n'est pas un simple recueil de textes sacres. C'est une architecture mathematique vivante, un reseau de codes caches que l'humanite n'a commence a decoder qu'avec l'avenement de l'informatique.")
    pdf.ln(2)
    pdf.body_text("En 1974, le biochimiste egyptien Rashad Khalifa decouvrit, a l'aide d'ordinateurs IBM, que le Coran renferme une structure mathematique centree sur le nombre 19. Ce chiffre, mentionne dans la Sourate 74, verset 30 ('Ils sont dix-neuf a y veiller'), est la signature numerique de l'Univers.")
    pdf.ln(2)
    pdf.body_text("Ce workbook est le fruit de cette revelation. Il combine la science du Code 19, la gematria arabe (Abjad), les noms divins du Rizq, un rituel structure et un talisman dessinable. Chaque element est ancre dans les textes et les nombres.")
    pdf.ln(4)

    pdf.quote_box("Ce workbook est une cle. Il n'ouvre pas les portes du hasard, mais les portes de la Providence.")
    pdf.ln(3)

    pdf.sub_title("Comment utiliser ce workbook")
    pdf.body_text("1. Lisez d'abord les fondements (pages 3-11) pour comprendre l'architecture.\n"
                  "2. Apprenez le rituel par cœur (pages 12-19).\n"
                  "3. Construisez votre talisman (pages 20-24).\n"
                  "4. Pratiquez 3 a 5 fois par jour pendant 40 jours.\n"
                  "5. Tenez un journal de vos synchronicites.")

    # ═══════════════════════════════════════════════════
    # PAGE 4 — CODE 19
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_light()
    pdf.section_title("II.  L E   C O D E   1 9")
    pdf.body_text("Le nombre 19 est la pierre angulaire de l'architecture mathematique du Coran. Il apparait dans chaque couche du texte : sourates, versets, lettres, mots.")
    pdf.ln(2)

    pdf.sub_title("Preuves du Code 19")
    data = [
        ("114 sourates", "114 = 19 x 6", "Structure globale"),
        ("Basmala (lettres)", "19 lettres", "Ouverture de chaque sourate"),
        ("Basmala (Abjad)", "684 = 19 x 36", "Noms divins centraux"),
        ("YaSeen (initiales)", "237 + 48 = 285 = 19 x 15", "Sourate 36"),
        ("Sourate 74:30", "'Ils sont dix-neuf'", "Mention explicite"),
        ("H.M. initiales", "2147 = 19 x 113", "Sourates 40-46"),
    ]
    for label, value, source in data:
        pdf.set_font("L", "B", 9)
        pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
        pdf.cell(50, 5.5, label, align="L")
        pdf.set_font("L", "B", 9)
        pdf.set_text_color(GOLD[0], GOLD[1], GOLD[2])
        pdf.set_fill_color(40, 20, 60)
        pdf.cell(55, 5.5, value, align="C", fill=True)
        pdf.set_font("L", "", 9)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0, 5.5, source, align="R")
        pdf.ln()

    pdf.ln(4)
    pdf.body_text("La probabilite statistique que tous ces multiples de 19 se produisent par coincidence est estimee a moins de un sur plusieurs trillions. Le Dr Gary Miller, mathematicien, s'est converti a l'Islam apres avoir etudie ces modeles.")

    # ═══════════════════════════════════════════════════
    # PAGE 5 — BASMALA 786
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_light()
    pdf.section_title("III.  L A   B A S M A L A  :  7 8 6")
    pdf.body_text("La Basmala est la formule d'ouverture de presque toutes les sourates du Coran. Elle contient 19 lettres et une valeur numerique totale de 786.")
    pdf.ln(2)

    pdf.body_ar("بسم الله الرحمن الرحيم")
    pdf.ln(2)

    pdf.sub_title("Decomposition Gematrique (Abjad)")
    basmala_data = [
        ("بسم (Bism)", "ب2 + س60 + م40", "102"),
        ("الله (Allah)", "ا1 + ل30 + ل30 + ه5", "66"),
        ("الرحمن (Al-Rahman)", "ا1 + ل30 + ر200 + ح8 + م40 + ن50", "329"),
        ("الرحيم (Al-Rahim)", "ا1 + ل30 + ر200 + ح8 + ي10 + م40", "289"),
    ]
    for name, calc, total in basmala_data:
        pdf.set_font("L", "B", 9)
        pdf.set_text_color(NIGHT_BLUE[0], NIGHT_BLUE[1], NIGHT_BLUE[2])
        pdf.cell(45, 5.5, name, align="L")
        pdf.set_font("L", "", 9)
        pdf.set_text_color(60, 60, 60)
        pdf.cell(95, 5.5, calc, align="L")
        pdf.set_font("L", "B", 10)
        pdf.set_text_color(GOLD[0], GOLD[1], GOLD[2])
        pdf.set_fill_color(40, 20, 60)
        pdf.cell(25, 5.5, total, align="C", fill=True)
        pdf.ln()

    pdf.ln(2)
    pdf.set_font("L", "B", 11)
    pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
    pdf.cell(0, 7, "Total : 102 + 66 + 329 + 289 = 786", align="C")
    pdf.ln()
    pdf.set_font("L", "", 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 6, "Noms divins : 66 + 329 + 289 = 684 = 19 x 36", align="C")

    pdf.ln(6)
    pdf.quote_box("La Basmala est la porte. 786 est le code d'acces. Chaque recitation active la signature divine du Coran.")

    # ═══════════════════════════════════════════════════
    # PAGE 6 — SURATE YASIN
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_light()
    pdf.section_title("IV.  S O U R A T E   Y A - S I N  (36)")
    pdf.body_text("Sourate Ya-Sin est appelee le 'Cœur du Coran'. Elle contient 83 versets, 730 mots, et 2988 lettres. Son nombre (36) se reduit a 9, le chiffre du Roi.")
    pdf.ln(2)

    pdf.sub_title("Architecture Numerique")
    yasin_data = [
        ("N° Sourate", "36", "3 + 6 = 9"),
        ("Versets", "83", "—"),
        ("Mots", "730", "—"),
        ("Lettres", "2988", "36 x 83 = 2988"),
        ("Lettres initiales ي", "237", "—"),
        ("Lettres initiales س", "48", "—"),
        ("Total initiales", "285", "19 x 15"),
    ]
    for label, val, note in yasin_data:
        pdf.set_font("L", "B", 9)
        pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
        pdf.cell(50, 5.5, label, align="L")
        pdf.set_font("L", "B", 10)
        pdf.set_text_color(GOLD[0], GOLD[1], GOLD[2])
        pdf.set_fill_color(40, 20, 60)
        pdf.cell(30, 5.5, val, align="C", fill=True)
        pdf.set_font("L", "", 9)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0, 5.5, note, align="R")
        pdf.ln()

    pdf.ln(4)
    pdf.body_text("Le Prophete (paix sur lui) a dit : 'Toute chose a un cœur, et le cœur du Coran est Ya-Sin.' (Tirmidhi). Cette sourate est traditionnellement recitee pour les defunts et comme protection.")
    pdf.ln(2)
    pdf.quote_box("36 x 83 = 2988 lettres. Ce n'est pas une coincidence. C'est une preuve.")

    # ═══════════════════════════════════════════════════
    # PAGE 7 — SURATE WAQIAH
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_light()
    pdf.section_title("V.  S O U R A T E   A L - W A Q I A H  (56)")
    pdf.body_text("Sourate Al-Waqiah est connue comme la 'Sourate de la Richesse'. Elle protege contre la pauvrete et ouvre les portes du Rizq.")
    pdf.ln(2)

    waqiah_data = [
        ("N° Sourate", "56", "5 + 6 = 11 = reflet divin"),
        ("Versets", "96", "—"),
        ("56 + 96", "152", "Miroir numerique"),
        ("Hadith cle", "—", "Reciter chaque nuit = pas de pauvrete"),
        ("Multiplicateur", "1 grain -> 7 epis x 100", "Sourate 2:261"),
    ]
    for label, val, note in waqiah_data:
        pdf.set_font("L", "B", 9)
        pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
        pdf.cell(50, 5.5, label, align="L")
        pdf.set_font("L", "B", 10)
        pdf.set_text_color(GOLD[0], GOLD[1], GOLD[2])
        pdf.set_fill_color(40, 20, 60)
        pdf.cell(30, 5.5, val, align="C", fill=True)
        pdf.set_font("L", "", 9)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0, 5.5, note, align="R")
        pdf.ln()

    pdf.ln(4)
    pdf.body_text("La sourate presente trois categories d'etres : les Sabiqun (les premiers), les gens de la droite, et les gens de la gauche. Ce triptyque reflete les trois etats de l'ame face a la Providence.")
    pdf.ln(2)
    pdf.quote_box("La Sourate Waqiah n'est pas seulement un texte. C'est un programme d'abondance.")

    # ═══════════════════════════════════════════════════
    # PAGE 8 — CODE NUMERIQUE AL-WAQI'A (1/2)
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_light()
    pdf.section_title("V-bis.  L E   C O D E   N U M E R I Q U E   D ' A L - W A Q I ' A")
    pdf.body_text("La Sourate Al-Waqi'a renferme un code mathematique unique. Son numero, son nombre de versets et son architecture interne forment une signature vibratoire qui se connecte au Code 19, a la gematria Abjad, et aux codes universels de manifestation.")
    pdf.ln(4)

    # ── ARCHITECTURE SACREE ──
    pdf.sub_title("Architecture Sacree")
    pdf.set_font("L", "B", 8)
    pdf.set_text_color(GOLD[0], GOLD[1], GOLD[2])
    pdf.set_fill_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
    headers = ["Propriete", "Valeur", "Signature"]
    col_w = [55, 35, 85]
    for h, w in zip(headers, col_w):
        pdf.cell(w, 7, h, border=1, fill=True, align="C")
    pdf.ln()
    for label, val, note in [
        ("N Sourate", "56", "5 + 6 = 11 -> 2"),
        ("Versets", "96", "9 + 6 = 15 -> 6"),
        ("Mots", "379", "3 + 7 + 9 = 19"),
        ("Lettres", "1 756", "1 + 7 + 5 + 6 = 19"),
        ("Abjad", "213", "2 + 1 + 3 = 6"),
    ]:
        pdf.set_font("L", "B", 9)
        pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
        pdf.cell(55, 6.5, label, border=1, align="L")
        pdf.set_font("L", "B", 10)
        pdf.set_text_color(GOLD[0], GOLD[1], GOLD[2])
        pdf.set_fill_color(40, 20, 60)
        pdf.cell(35, 6.5, val, border=1, fill=True, align="C")
        pdf.set_font("L", "", 9)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(85, 6.5, note, border=1, align="L")
        pdf.ln()
    pdf.ln(5)

    # ── CODE 19 ──
    pdf.sub_title("Le Code 19 dans Al-Waqi'a")
    pdf.quote_box("56 + 96 = 152  =  19 x 8")
    pdf.ln(3)
    pdf.body_text("Les reductions convergent : mots (379 -> 3+7+9 = 19), lettres (1756 -> 1+7+5+6 = 19), et le total global (2287 -> 2+2+8+7 = 19). Quatre preuves mathematiques convergentes.")
    pdf.ln(5)

    # ── MIROIR 56↔96 ──
    pdf.sub_title("Le Miroir Unique : 56  96")
    pdf.body_text("Aucune autre sourate du Coran ne possede cette propriete : son numero et son nombre de versets sont les chiffres inverses l'un de l'autre.")
    pdf.ln(3)

    y_box = pdf.get_y()
    # Encadre gauche
    pdf.set_xy(15, y_box)
    pdf.set_fill_color(LIGHT_VIOLET[0], LIGHT_VIOLET[1], LIGHT_VIOLET[2])
    pdf.set_draw_color(BRIGHT_VIOLET[0], BRIGHT_VIOLET[1], BRIGHT_VIOLET[2])
    pdf.set_font("L", "B", 12)
    pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
    pdf.cell(85, 10, "56 = 7 x 8", border=1, fill=True, align="C")
    pdf.set_xy(15, y_box + 10)
    pdf.set_font("L", "", 8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(85, 5, "7 cieux x 8 directions du talisman", align="C")
    # Encadre droite
    pdf.set_xy(110, y_box)
    pdf.set_fill_color(LIGHT_VIOLET[0], LIGHT_VIOLET[1], LIGHT_VIOLET[2])
    pdf.set_draw_color(BRIGHT_VIOLET[0], BRIGHT_VIOLET[1], BRIGHT_VIOLET[2])
    pdf.set_font("L", "B", 12)
    pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
    pdf.cell(85, 10, "96 = 8 x 12", border=1, fill=True, align="C")
    pdf.set_xy(110, y_box + 10)
    pdf.set_font("L", "", 8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(85, 5, "8 x les 12 noms divins du Rizq", align="C")

    pdf.set_xy(15, y_box + 20)
    pdf.ln(4)
    pdf.body_text("96 est aussi le numero de la Sourate Al-Alaq (Iqra), premiere revelation. Al-Waqi'a unit le Rizq (56) et la Connaissance (96) en une seule sourate.")

    # ═══════════════════════════════════════════════════
    # PAGE 9 — CODE NUMERIQUE AL-WAQI'A (2/2)
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_light()

    # ── ABJAD ──
    pdf.sub_title("Gematria Abjad")
    pdf.set_font("A", "", 14)
    pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
    pdf.cell(0, 8, ar("الواقعة"), align="R")
    pdf.ln()
    pdf.set_font("L", "", 9)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 5, "Alif(1) + Lam(30) + Waw(6) + Alif(1) + Qaf(100) + Ayn(70) + Ta(5) = 213", align="R")
    pdf.ln()
    pdf.cell(0, 5, "Reduction : 2 + 1 + 3 = 6  (harmonie, equilibre)", align="R")
    pdf.ln(4)
    pdf.set_font("A", "", 12)
    pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
    pdf.cell(0, 7, ar("سورة الواقعة"), align="R")
    pdf.ln()
    pdf.set_font("L", "", 9)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 5, "271 + 213 = 484  ->  4 + 8 + 4 = 16  ->  1 + 6 = 7", align="R")
    pdf.ln(6)

    # ── CODE VIBRATOIRE ──
    pdf.sub_title("Le Code Vibratoire")
    pdf.set_fill_color(MIDNIGHT[0], MIDNIGHT[1], MIDNIGHT[2])
    pdf.set_draw_color(GOLD[0], GOLD[1], GOLD[2])
    pdf.set_text_color(GOLD[0], GOLD[1], GOLD[2])
    pdf.set_font("L", "B", 22)
    pdf.set_x(30)
    pdf.set_line_width(0.5)
    pdf.cell(150, 16, "56    96    152", border=1, fill=True, align="C")
    pdf.set_line_width(0.2)
    pdf.ln()
    pdf.set_x(30)
    pdf.set_font("L", "", 9)
    pdf.set_text_color(160, 160, 180)
    pdf.cell(150, 6, "56 + 96 = 152 = 19 x 8        Reduction : 34 -> 7", align="C")
    pdf.ln(8)
    pdf.set_text_color(40, 40, 40)
    pdf.set_font("L", "", 10)
    pdf.body_text("Ce code combine les trois nombres sacres du systeme Miftah 19 :")
    pdf.body_text("  7  — le multiplicateur divin du Rizq (2:261)")
    pdf.body_text("  8  — les directions du talisman")
    pdf.body_text("  19 — la signature divine du Coran")
    pdf.ln(6)

    # ── PONT GRABOVOI ──
    pdf.sub_title("Pont Universel : Coran & Codes Grabovoi")
    pdf.body_text("Les memes trois nombres apparaissent dans les deux systemes vibratoires :")
    pdf.ln(3)
    pdf.set_x(20)
    pdf.set_font("L", "B", 8)
    pdf.set_fill_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
    pdf.set_text_color(GOLD[0], GOLD[1], GOLD[2])
    pdf.cell(45, 7, "Systeme", border=1, fill=True, align="C")
    pdf.cell(65, 7, "Sequence", border=1, fill=True, align="C")
    pdf.cell(60, 7, "Nombres cles", border=1, fill=True, align="C")
    pdf.ln()
    for sys, seq, keys in [
        ("Grabovoi", "520 741 8", "7 + 19 + 8"),
        ("Coran", "56 96 152", "7x8 + 19x8"),
    ]:
        pdf.set_x(20)
        pdf.set_font("L", "B", 9)
        pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
        pdf.cell(45, 7, sys, border=1, align="C")
        pdf.set_font("L", "B", 10)
        pdf.set_text_color(GOLD[0], GOLD[1], GOLD[2])
        pdf.set_fill_color(40, 20, 60)
        pdf.cell(65, 7, seq, border=1, fill=True, align="C")
        pdf.set_font("L", "", 9)
        pdf.set_text_color(60, 60, 60)
        pdf.cell(60, 7, keys, border=1, align="C")
        pdf.ln()
    pdf.ln(6)
    pdf.quote_box("Al-Waqi'a est le pont entre la numerologie coranique et les codes vibratoires universels. 56 96 152 : la cle numerique de la sourate de la richesse.")

    # ═══════════════════════════════════════════════════
    # PAGE 10 — LE MOT RIZQ
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_light()
    pdf.section_title("VI.  L E   M O T   R I Z Q  :  1 2 3")
    pdf.body_text("Le mot 'Rizq' (رزق) apparait 123 fois dans le Coran. Il designe toute forme de subsistance, pas seulement l'argent : la sante, le temps, la famille, la paix interieure.")
    pdf.ln(2)

    pdf.sub_title("Gematria du Rizq")
    rizq_data = [
        ("ر (Ra)", "200", "—"),
        ("ز (Zay)", "7", "—"),
        ("ق (Qaf)", "100", "—"),
        ("Total", "307", "3 + 0 + 7 = 10 = 1"),
    ]
    for label, val, note in rizq_data:
        pdf.set_font("L", "B", 9)
        pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
        pdf.cell(30, 5.5, label, align="L")
        pdf.set_font("L", "B", 10)
        pdf.set_text_color(GOLD[0], GOLD[1], GOLD[2])
        pdf.set_fill_color(40, 20, 60)
        pdf.cell(25, 5.5, val, align="C", fill=True)
        pdf.set_font("L", "", 9)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0, 5.5, note, align="R")
        pdf.ln()

    pdf.ln(4)
    pdf.body_text("123 est un nombre triangulaire (1+2+3=6). Dans la tradition mystique, 6 est le nombre de l'harmonie et de l'equilibre. Les 123 occurrences de Rizq forment un reseau invisible qui traverse tout le Coran.")
    pdf.ln(2)
    pdf.quote_box("Rizq n'est pas ce que tu gagnes. C'est ce qui t'est destine avant ta naissance.")

    # ═══════════════════════════════════════════════════
    # PAGE 9 — GEMATRIA ABJAD
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_light()
    pdf.section_title("VII.  G E M A T R I A   A B J A D")
    pdf.body_text("Le systeme Abjad attribue une valeur numerique a chaque lettre de l'alphabet arabe. Cette science, appelee Hisab al-Jummal, permet de decoder les couches cachees des mots sacres.")
    pdf.ln(3)

    abjad = [
        ("ا Alif", "1", "ب Ba", "2"),
        ("ج Jim", "3", "د Dal", "4"),
        ("ه Ha", "5", "و Waw", "6"),
        ("ز Zay", "7", "ح Ha", "8"),
        ("ط Ta", "9", "ي Ya", "10"),
        ("ك Kaf", "20", "ل Lam", "30"),
        ("م Mim", "40", "ن Nun", "50"),
        ("س Sin", "60", "ع Ayn", "70"),
        ("ف Fa", "80", "ص Sad", "90"),
        ("ق Qaf", "100", "ر Ra", "200"),
        ("ش Shin", "300", "ت Ta", "400"),
        ("ث Tha", "500", "خ Kha", "600"),
        ("ذ Dhal", "700", "ض Dad", "800"),
        ("ظ Za", "900", "غ Ghayn", "1000"),
    ]

    for l1, v1, l2, v2 in abjad:
        pdf.set_font("L", "B", 9)
        pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
        pdf.cell(25, 5, l1, align="L")
        pdf.set_font("L", "", 9)
        pdf.set_text_color(60, 60, 60)
        pdf.cell(20, 5, v1, align="L")
        pdf.set_font("L", "B", 9)
        pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
        pdf.cell(25, 5, l2, align="L")
        pdf.set_font("L", "", 9)
        pdf.set_text_color(60, 60, 60)
        pdf.cell(0, 5, v2, align="L")
        pdf.ln()

    pdf.ln(2)
    pdf.quote_box("Chaque lettre est un nombre. Chaque nombre est un signe. Chaque signe est un chemin vers la Lumiere.")

    # ═══════════════════════════════════════════════════
    # PAGE 10 — 4 NOMS DIVINS
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_light()
    pdf.section_title("VIII.  L E S   4   N O M S   D I V I N S   D U   R I Z Q")
    pdf.body_text("Ces quatre noms invoques dans le rituel Miftah 19 representent les quatre aspects de l'abondance divine : provision, ouverture, richesse interieure, et enrichissement.")
    pdf.ln(3)

    names = [
        ("يا رزاق", "Ya Razzaq", "Le Pourvoyeur Supreme", "319", "Celui qui pourvoit sans compter"),
        ("يا فتاح", "Ya Fattah", "L'Ouvreur des Portes", "489", "Celui qui ouvre les voies bloquees"),
        ("يا غني", "Ya Ghani", "Le Riche Absolu", "1060", "Celui dont la richesse est infinie"),
        ("يا مغني", "Ya Mughni", "L'Enrichisseur", "1100", "Celui qui enrichit Ses serviteurs"),
    ]

    for ar_name, trans, meaning, abjad, desc in names:
        pdf.set_fill_color(LIGHT_VIOLET[0], LIGHT_VIOLET[1], LIGHT_VIOLET[2])
        pdf.set_draw_color(BRIGHT_VIOLET[0], BRIGHT_VIOLET[1], BRIGHT_VIOLET[2])
        pdf.set_font("A", "", 13)
        pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
        pdf.cell(35, 8, ar(ar_name), border=1, fill=True, align="R")
        pdf.set_font("L", "B", 10)
        pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
        pdf.cell(40, 8, trans, border=1, fill=True, align="L")
        pdf.set_font("L", "", 9)
        pdf.set_text_color(60, 60, 60)
        pdf.cell(0, 8, f"{meaning}  |  Abjad: {abjad}", border=1, fill=True, align="L")
        pdf.ln()
        pdf.set_font("L", "", 8)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 4, desc, align="R")
        pdf.ln(5)

    pdf.ln(2)
    total = 319 + 489 + 1060 + 1100
    pdf.set_font("L", "B", 10)
    pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
    pdf.cell(0, 6, f"Somme Abjad : 319 + 489 + 1060 + 1100 = {total}  |  Reduction : 2+9+6+8 = 25 -> 2+5 = 7", align="C")

    # ═══════════════════════════════════════════════════
    # PAGE 11 — 99 NOMS GRILLE
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_light()
    pdf.section_title("IX.  L E S   9 9   N O M S   D I V I N S")
    pdf.body_text("Allah possede 99 noms. Chacun est une porte vers un attribut divin. Les pratiquants invoquent ces noms pour attirer les qualites correspondantes dans leur vie.")
    pdf.ln(2)

    # Key names related to wealth
    wealth_names = [
        ("Ar-Razzaq", "Le Pourvoyeur"),
        ("Al-Ghani", "Le Riche"),
        ("Al-Mughni", "L'Enrichisseur"),
        ("Al-Fattah", "L'Ouvreur"),
        ("Al-Wahhab", "Le Donateur"),
        ("Al-Karim", "Le Genereux"),
        ("Al-Basit", "Celui qui etend"),
        ("Al-Latif", "Le Doux"),
        ("Al-Mujib", "Celui qui repond"),
        ("Al-Wasi'", "L'Immense"),
        ("Al-Malik", "Le Roi"),
        ("Al-Qadir", "Le Tout-Puissant"),
    ]

    pdf.sub_title("Les 12 Noms du Rizq")
    for i, (name, meaning) in enumerate(wealth_names):
        pdf.set_font("L", "B", 9)
        pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
        pdf.cell(50, 5.5, name, align="L")
        pdf.set_font("L", "", 9)
        pdf.set_text_color(60, 60, 60)
        pdf.cell(0, 5.5, meaning, align="L")
        pdf.ln()

    pdf.ln(2)
    pdf.quote_box("Invoquer les 99 Noms, c'est tourner les 99 cles du Royaume.")

    # ═══════════════════════════════════════════════════
    # PAGE 12 — ARCHITECTURE RITUEL
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_light()
    pdf.section_title("X.  A R C H I T E C T U R E   D U   R I T U E L")
    pdf.body_text("Le rituel Miftah 19 est une structure mathematique vivante. Chaque etape est ponderee par un nombre sacre. Le cycle total forme une signature energetique.")
    pdf.ln(2)

    pdf.sub_title("Schema Numerique")
    arch = [
        ("1. Ouverture", "1x", "Basmala (19 lettres, Abjad 786)"),
        ("2. Istighfar", "7x", "Purification multiplicateur (2:261)"),
        ("3. Noms Divins", "19x", "Signature divine du Coran (74:30)"),
        ("4. Salawat", "33x", "Age du Paradis, Tasbih"),
        ("5. Sceau", "1x", "Tawakkul absolu"),
    ]

    for step, count, desc in arch:
        pdf.set_font("L", "B", 9)
        pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
        pdf.cell(50, 5.5, step, align="L")
        pdf.set_font("L", "B", 10)
        pdf.set_text_color(GOLD[0], GOLD[1], GOLD[2])
        pdf.set_fill_color(40, 20, 60)
        pdf.cell(20, 5.5, count, align="C", fill=True)
        pdf.set_font("L", "", 9)
        pdf.set_text_color(60, 60, 60)
        pdf.cell(0, 5.5, desc, align="L")
        pdf.ln()

    pdf.ln(4)
    pdf.set_font("L", "B", 12)
    pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
    pdf.cell(0, 8, "Total du cycle : 1 + 7 + 19 + 33 + 1 = 61", align="C")
    pdf.ln(5)
    pdf.set_font("L", "", 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 6, "Reduction : 6 + 1 = 7 (completion divine)", align="C")
    pdf.ln(6)
    pdf.quote_box("61 est le nombre de l'Architecte. 7 est le nombre de l'Oeuvre achevee.")

    # ═══════════════════════════════════════════════════
    # PAGE 13 — ETAPE 1 OUVERTURE
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_light()
    pdf.section_title("XI.  E T A P E   1  :  O U V E R T U R E  (1x)")
    pdf.body_text("La Basmala est la porte vibratoire. Elle aligne la conscience du pratiquant avec la frequence du Coran. Ne la recitez jamais machinalement.")
    pdf.ln(3)

    pdf.set_fill_color(LIGHT_VIOLET[0], LIGHT_VIOLET[1], LIGHT_VIOLET[2])
    pdf.set_draw_color(BRIGHT_VIOLET[0], BRIGHT_VIOLET[1], BRIGHT_VIOLET[2])
    pdf.set_font("A", "", 16)
    pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
    pdf.cell(0, 12, ar("بسم الله الرحمن الرحيم"), border=1, fill=True, align="C")
    pdf.ln(3)

    pdf.set_font("L", "", 10)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 6, "Bismillah ir-Rahman ir-Rahim", align="C")
    pdf.ln(8)

    pdf.body_text("Intention silencieuse : 'Par le code de Ta parole, ouvre les portes du Rizq.'")
    pdf.ln(2)

    pdf.sub_title("Visualisation")
    pdf.body_text("Visualisez une porte doree qui s'ouvre devant vous. Derriere cette porte, un courant lumineux de couleur violette et doree coule vers vous. C'est le Rizq qui descend.")
    pdf.ln(2)

    pdf.quote_box("1 = Tawhid. Un seul Dieu. Une seule porte. Un seul chemin vers l'abondance.")

    # ═══════════════════════════════════════════════════
    # PAGE 14 — ETAPE 2 ISTIGHFAR
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_light()
    pdf.section_title("XII.  E T A P E   2  :  I S T I G H F A R  (7x)")
    pdf.body_text("L'istighfar nettoie les blocages energetiques. Le chiffre 7 est le multiplicateur celeste (2:261) et la cle des pluies d'abondance (71:10-12).")
    pdf.ln(3)

    pdf.set_fill_color(LIGHT_VIOLET[0], LIGHT_VIOLET[1], LIGHT_VIOLET[2])
    pdf.set_draw_color(BRIGHT_VIOLET[0], BRIGHT_VIOLET[1], BRIGHT_VIOLET[2])
    pdf.set_font("A", "", 14)
    pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
    pdf.cell(0, 10, ar("استغفر الله العظيم واتوب اليه"), border=1, fill=True, align="C")
    pdf.ln(3)

    pdf.set_font("L", "", 10)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 6, "Astaghfirullah al-Azim wa atubu ilayh", align="C")
    pdf.ln(8)

    pdf.sub_title("Pourquoi 7 fois ?")
    pdf.body_text("Les 7 cieux (67:3) correspondent aux 7 niveaux de purification. Chaque repetition efface une couche de blocage financier : culpabilite, peur, avidite, orgueil, paresse, desespoir, attachement.")
    pdf.ln(2)
    pdf.quote_box("7 = 19 - 12. L'istighfar est le pont entre l'humain (12) et le divin (19).")

    # ═══════════════════════════════════════════════════
    # PAGE 15 — ETAPE 3 NOMS DIVINS
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_light()
    pdf.section_title("XIII.  E T A P E   3  :  N O M S   D I V I N S  (19x)")
    pdf.body_text("19 est le nombre-signature du Coran (74:30). Invoquer les noms divins 19 fois active la frequence mathematique du Livre.")
    pdf.ln(3)

    pdf.sub_title("Sequence des 4 Noms (4 cycles complets + 3 = 19)")

    names_seq = [
        ("1-4", "يا رزاق  |  يا فتاح  |  يا غني  |  يا مغني", "Cycle 1"),
        ("5-8", "يا رزاق  |  يا فتاح  |  يا غني  |  يا مغني", "Cycle 2"),
        ("9-12", "يا رزاق  |  يا فتاح  |  يا غني  |  يا مغني", "Cycle 3"),
        ("13-16", "يا رزاق  |  يا فتاح  |  يا غني  |  يا مغني", "Cycle 4"),
        ("17-19", "يا رزاق  |  يا فتاح  |  يا مغني", "Cycle 5 (3 noms)"),
    ]

    for nums, seq, label in names_seq:
        pdf.set_font("L", "B", 9)
        pdf.set_text_color(GOLD[0], GOLD[1], GOLD[2])
        pdf.set_fill_color(40, 20, 60)
        pdf.cell(18, 5.5, nums, align="C", fill=True)
        pdf.set_font("L", "", 9)
        pdf.set_text_color(60, 60, 60)
        pdf.cell(0, 5.5, f"  {seq}  |  {label}", align="L")
        pdf.ln()

    pdf.ln(4)
    pdf.body_text("Au 5e cycle, on omet 'Ya Ghani' pour atteindre exactement 19 invocations. Ce 'sacrifice' symbolique renforce l'intention.")
    pdf.ln(2)
    pdf.quote_box("19 = 19 x 1. La plus pure des signatures. Une seule repetition de 19 vaut mille repetitions sans nombre.")

    # ═══════════════════════════════════════════════════
    # PAGE 16 — ETAPE 4 SALAWAT
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_light()
    pdf.section_title("XIV.  E T A P E   4  :  S A L A W A T  (33x)")
    pdf.body_text("33 est le nombre sacre du Tasbih post-priere et l'age des gens du Paradis (Waqiah 56). Les Salawat connectent le pratiquant a la source prophetique.")
    pdf.ln(3)

    pdf.set_fill_color(LIGHT_VIOLET[0], LIGHT_VIOLET[1], LIGHT_VIOLET[2])
    pdf.set_draw_color(BRIGHT_VIOLET[0], BRIGHT_VIOLET[1], BRIGHT_VIOLET[2])
    pdf.set_font("A", "", 13)
    pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
    pdf.cell(0, 10, ar("اللهم صل على سيدنا محمد وعلى ال سيدنا محمد"), border=1, fill=True, align="C")
    pdf.ln(3)

    pdf.set_font("L", "", 9)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 5, "Allahumma salli 'ala Sayyidina Muhammad wa 'ala ali Sayyidina Muhammad", align="C")
    pdf.ln(8)

    pdf.sub_title("Technique de comptage")
    pdf.body_text("Divisez les 33 en 3 groupes de 11. Chaque groupe correspond a un aspect de la benediction :\n"
                  "- 1-11 : Benediction sur le corps\n"
                  "- 12-22 : Benediction sur le cœur\n"
                  "- 23-33 : Benediction sur l'ame")
    pdf.ln(2)
    pdf.quote_box("33 = 3 + 3 = 6. Le sceau prophetique scelle les 6 directions de l'espace.")

    # ═══════════════════════════════════════════════════
    # PAGE 17 — ETAPE 5 SCEAU
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_light()
    pdf.section_title("XV.  E T A P E   5  :  S C E A U  (1x)")
    pdf.body_text("Le sceau final scelle l'energie du rituel. Il affirme le Tawakkul (confiance absolue) et protege contre les doutes.")
    pdf.ln(3)

    pdf.set_fill_color(LIGHT_VIOLET[0], LIGHT_VIOLET[1], LIGHT_VIOLET[2])
    pdf.set_draw_color(BRIGHT_VIOLET[0], BRIGHT_VIOLET[1], BRIGHT_VIOLET[2])
    pdf.set_font("A", "", 13)
    pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
    pdf.cell(0, 10, ar("حسبنا الله ونعم الوكيل نعم المولى ونعم النصير"), border=1, fill=True, align="C")
    pdf.ln(3)

    pdf.set_font("L", "", 9)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 5, "Hasbunallahu wa ni'mal wakeel, ni'mal mawla wa ni'man naseer", align="C")
    pdf.ln(8)

    pdf.sub_title("Geste de scellement")
    pdf.body_text("Apres la recitation, soufflez doucement sur vos paumes. Passez-les sur votre visage, votre poitrine, et votre front. Ce geste scelle l'energie dans votre champ aurique.")
    pdf.ln(2)
    pdf.quote_box("1 = retour a l'Unite. Apres le cycle complet (61), on revient au point de depart, mais transforme.")

    # ═══════════════════════════════════════════════════
    # PAGE 18 — PLANNING
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_light()
    pdf.section_title("XVI.  P L A N N I N G   Q U O T I D I E N")
    pdf.body_text("Le rituel se pratique 3 a 5 fois par jour. Chaque session correspond a un moment energetique specifique du jour islamique.")
    pdf.ln(3)

    plan = [
        ("1", "Fajr (aube)", "Active le flux de la journee"),
        ("2", "Duha (10h-11h)", "Amplifie le Rizq en cours"),
        ("3", "Asr / Maghrib", "Scelle la journee"),
        ("4*", "Isha (nuit)", "Barakah profonde"),
        ("5*", "Avant sommeil", "Programme le subconscient"),
    ]

    for num, time, effect in plan:
        pdf.set_font("L", "B", 10)
        pdf.set_text_color(GOLD[0], GOLD[1], GOLD[2])
        pdf.set_fill_color(40, 20, 60)
        pdf.cell(15, 7, num, align="C", fill=True)
        pdf.set_font("L", "B", 10)
        pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
        pdf.cell(50, 7, time, align="L")
        pdf.set_font("L", "", 9)
        pdf.set_text_color(60, 60, 60)
        pdf.cell(0, 7, effect, align="L")
        pdf.ln()

    pdf.ln(4)
    pdf.sub_title("Calendrier des 40 jours")
    pdf.body_text("La tradition mystique recommande 40 jours de pratique ininterrompue. C'est le temps necessaire pour creer un nouveau circuit neuronal et energetique.\n\n"
                  "Jours 1-10 : Installation du rituel (adaptation)\n"
                  "Jours 11-20 : Amplification (les premiers signes apparaissent)\n"
                  "Jours 21-30 : Stabilisation (le rituel devient naturel)\n"
                  "Jours 31-40 : Transmutation (integration profonde)")
    pdf.ln(2)
    pdf.quote_box("40 = nombre de l'epreuve et de la transformation. Moise sur le mont Sinai. Jesus au desert. Muhammad a la Hira.")

    # ═══════════════════════════════════════════════════
    # PAGE 19 — VERSION EXPRESS
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_light()
    pdf.section_title("XVII.  V E R S I O N   E X P R E S S  (60s)")
    pdf.body_text("Pour les moments ou le temps manque, cette version preserve l'architecture sacree en moins d'une minute.")
    pdf.ln(3)

    express = [
        ("Ouverture", "Bismillah ir-Rahman ir-Rahim", "1x", "~3s"),
        ("Istighfar", "Astaghfirullah al-Azim", "3x", "~12s"),
        ("Nom Divin", "Ya Razzaq", "7x", "~15s"),
        ("Salawat", "Allahumma salli 'ala Muhammad", "3x", "~10s"),
        ("Sceau", "Hasbunallahu wa ni'mal wakeel", "1x", "~5s"),
    ]

    for step, formule, count, duree in express:
        pdf.set_font("L", "B", 9)
        pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
        pdf.cell(40, 5.5, step, align="L")
        pdf.set_font("L", "", 9)
        pdf.set_text_color(60, 60, 60)
        pdf.cell(85, 5.5, formule, align="L")
        pdf.set_font("L", "B", 9)
        pdf.set_text_color(GOLD[0], GOLD[1], GOLD[2])
        pdf.cell(20, 5.5, count, align="C")
        pdf.set_font("L", "", 9)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0, 5.5, duree, align="R")
        pdf.ln()

    pdf.ln(4)
    pdf.set_font("L", "B", 11)
    pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
    pdf.cell(0, 7, "Architecture : 1 + 3 + 7 + 3 + 1 = 15 = 19 - 4", align="C")
    pdf.ln(5)
    pdf.body_text("La reduction 15 conserve le schema mathematique. Meme en 60 secondes, vous activez la grille. C'est mieux que zero.")
    pdf.ln(2)
    pdf.quote_box("La baraka n'est pas dans la duree, mais dans la presence.")

    # ═══════════════════════════════════════════════════
    # PAGE 20 — TALISMAN OVERVIEW
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_violet()
    pdf.set_text_color(GOLD[0], GOLD[1], GOLD[2])
    pdf.set_y(30)
    pdf.title_cover("L E   T A L I S M A N", size=26)
    pdf.subtitle_cover("Schema geometrique de protection et d'attraction du Rizq")
    pdf.ln(10)

    pdf.set_font("L", "", 10)
    pdf.set_text_color(200, 180, 220)
    pdf.cell(0, 6, "Le talisman est un condensateur energetique. Il concentre les codes du rituel", align="C")
    pdf.ln(5)
    pdf.cell(0, 6, "dans une forme geometrique dessinable. Conservez-le sur vous ou dans votre espace.", align="C")
    pdf.ln(20)

    pdf.set_font("L", "B", 12)
    pdf.set_text_color(GOLD[0], GOLD[1], GOLD[2])
    pdf.cell(0, 8, "3 ANNEAUX  |  8 DIRECTIONS  |  1 CENTRE", align="C")
    pdf.ln(8)

    pdf.set_font("L", "", 10)
    pdf.set_text_color(180, 160, 200)
    pdf.cell(0, 6, "A reproduire sur papier de 15x15 cm", align="C")
    pdf.ln(4)
    pdf.cell(0, 6, "Encre doree ou violette sur fond blanc ou bleu nuit", align="C")

    # ═══════════════════════════════════════════════════
    # PAGE 21 — CONSTRUCTION TALISMAN
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_light()
    pdf.section_title("XIX.  C O N S T R U C T I O N   D U   T A L I S M A N")
    pdf.body_text("Suivez ces etapes pour construire votre talisman personnel.")
    pdf.ln(3)

    steps = [
        ("1. Preparation", "Prenez un papier blanc de 15x15 cm. Allumez une bougie blanche ou violette. Faites vos ablutions."),
        ("2. Cercle exterieur", "Tracez un cercle de 55 mm de rayon. C'est l'anneau de protection."),
        ("3. Cercle median", "Tracez un cercle de 43 mm. C'est l'anneau des noms divins."),
        ("4. Cercle interieur", "Tracez un cercle de 30 mm. C'est l'anneau du cœur."),
        ("5. Etoile", "Tracez deux carres decales de 45 degres pour former l'etoile a 8 branches."),
        ("6. Inscription", "Ecrivez les nombres et les noms aux positions indiquees."),
        ("7. Activation", "Recitez le rituel Miftah 19 complet devant le talisman."),
        ("8. Conservation", "Gardez-le sur vous (portefeuille) ou placez-le dans votre espace de travail."),
    ]

    for title, desc in steps:
        pdf.set_font("L", "B", 10)
        pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
        pdf.cell(0, 6, title, align="L")
        pdf.ln()
        pdf.set_font("L", "", 9)
        pdf.set_text_color(60, 60, 60)
        pdf.multi_cell(0, 4.5, desc)
        pdf.ln(2)

    pdf.quote_box("Nettoyage energetique : exposez le talisman au premier soleil du vendredi (apres Fajr).")

    # ═══════════════════════════════════════════════════
    # PAGE 22 — CARRE MAGIQUE
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_light()
    pdf.section_title("XX.  L E   C A R R E   M A G I Q U E   D U   R I Z Q")
    pdf.body_text("Ce carre 3x3 concentre les 9 nombres sacres du projet. Placez-le au centre de votre talisman ou conservez-le separement.")
    pdf.ln(5)

    # Draw magic square
    sq_size = 22
    sx, sy_base = 72, pdf.get_y() + 5
    magic = [
        ["786", "19", "1"],
        ["7", "61", "33"],
        ["123", "56", "96"],
    ]
    for r in range(3):
        for c in range(3):
            x = sx + c * sq_size
            y = sy_base + r * sq_size
            fill = (r == 1 and c == 1)
            if fill:
                pdf.set_fill_color(GOLD[0], GOLD[1], GOLD[2])
                pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
            else:
                pdf.set_fill_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
                pdf.set_text_color(GOLD[0], GOLD[1], GOLD[2])
            pdf.set_font("L", "B", 14)
            pdf.set_xy(x, y)
            pdf.cell(sq_size, sq_size, magic[r][c], border=1, fill=True, align="C")

    pdf.set_y(sy_base + 3 * sq_size + 10)
    pdf.set_font("L", "B", 10)
    pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
    pdf.cell(0, 6, "Centre : 61  |  Reduction : 6 + 1 = 7", align="C")
    pdf.ln(6)

    pdf.sub_title("Signification des 9 nombres")
    nums = [
        ("786", "Basmala — ouverture"),
        ("19", "Signature divine"),
        ("1", "Tawhid — unicite"),
        ("7", "Multiplicateur celeste"),
        ("61", "Total du cycle"),
        ("33", "Age du Paradis"),
        ("123", "Occurrences Rizq"),
        ("56", "Sourate Waqiah"),
        ("96", "Versets de Waqiah"),
    ]
    for n, desc in nums:
        pdf.set_font("L", "B", 9)
        pdf.set_text_color(GOLD[0], GOLD[1], GOLD[2])
        pdf.set_fill_color(40, 20, 60)
        pdf.cell(20, 5.5, n, align="C", fill=True)
        pdf.set_font("L", "", 9)
        pdf.set_text_color(60, 60, 60)
        pdf.cell(0, 5.5, desc, align="L")
        pdf.ln()

    pdf.ln(2)
    pdf.set_font("L", "", 9)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 5, "Somme totale : 786+19+1+7+61+33+123+56+96 = 1182  |  Reduction : 1+1+8+2 = 12 -> 1+2 = 3", align="C")

    # ═══════════════════════════════════════════════════
    # PAGE 23 — ETOILE 8 BRANCHES
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_light()
    pdf.section_title("XXI.  L ' E T O I L E   A   8   B R A N C H E S")
    pdf.body_text("L'etoile a 8 branches represente les 8 directions de l'abondance. Elle est formee par deux carres decales de 45 degres.")
    pdf.ln(3)

    pdf.sub_title("Les 8 Noms aux 8 Directions")
    directions = [
        ("Nord", "يا فتاح", "L'Ouvreur"),
        ("Nord-Est", "يا غني", "Le Riche"),
        ("Est", "يا رزاق", "Le Pourvoyeur"),
        ("Sud-Est", "يا مغني", "L'Enrichisseur"),
        ("Sud", "يا وهاب", "Le Donateur"),
        ("Sud-Ouest", "يا كريم", "Le Genereux"),
        ("Ouest", "يا باسط", "Celui qui etend"),
        ("Nord-Ouest", "يا لطيف", "Le Doux"),
    ]

    for dir, name, meaning in directions:
        pdf.set_font("L", "B", 9)
        pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
        pdf.cell(30, 5.5, dir, align="L")
        pdf.set_font("A", "", 10)
        pdf.set_text_color(NIGHT_BLUE[0], NIGHT_BLUE[1], NIGHT_BLUE[2])
        pdf.cell(35, 5.5, ar(name), align="R")
        pdf.set_font("L", "", 9)
        pdf.set_text_color(60, 60, 60)
        pdf.cell(0, 5.5, meaning, align="L")
        pdf.ln()

    pdf.ln(4)
    pdf.body_text("Cette etoile scelle les 8 directions contre la fuite du Rizq. Aucune energie negative ne peut penetrer par ces voies une fois scellees.")
    pdf.ln(2)
    pdf.quote_box("8 = 2 x 2 x 2. La triade du manifeste. Corps, cœur, ame — chacun scelle dans les 8 directions.")

    # ═══════════════════════════════════════════════════
    # PAGE 24 — GRILLE PROTECTION
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_light()
    pdf.section_title("XXII.  G R I L L E   D E   P R O T E C T I O N")
    pdf.body_text("Cette grille textuelle est une version simplifiee du talisman. Ecrivez-la en calligraphie dans un cercle.")
    pdf.ln(5)

    # Draw box
    pdf.set_fill_color(40, 20, 60)
    pdf.set_draw_color(GOLD[0], GOLD[1], GOLD[2])
    pdf.set_line_width(0.5)
    pdf.rect(40, pdf.get_y(), 130, 70, "DF")

    pdf.set_xy(40, pdf.get_y() + 3)
    pdf.set_font("A", "", 11)
    pdf.set_text_color(GOLD[0], GOLD[1], GOLD[2])
    pdf.cell(130, 8, ar("بسم الله الرحمن الرحيم"), align="C")
    pdf.ln()
    pdf.set_font("A", "", 10)
    pdf.set_text_color(SKY_BLUE[0], SKY_BLUE[1], SKY_BLUE[2])
    pdf.cell(130, 7, ar("يا رزاق    يا فتاح    يا غني    يا مغني"), align="C")
    pdf.ln()
    pdf.set_font("L", "B", 12)
    pdf.set_text_color(GOLD[0], GOLD[1], GOLD[2])
    pdf.cell(130, 10, "1 — 19 — 7", align="C")
    pdf.ln()
    pdf.cell(130, 10, "786 — 33", align="C")
    pdf.ln()
    pdf.set_font("A", "", 9)
    pdf.set_text_color(SKY_BLUE[0], SKY_BLUE[1], SKY_BLUE[2])
    pdf.cell(130, 6, ar("استغفر الله العظيم"), align="C")
    pdf.ln()
    pdf.cell(130, 6, ar("حسبنا الله ونعم الوكيل"), align="C")

    pdf.set_y(pdf.get_y() + 15)
    pdf.body_text("Cette grille textuelle peut etre ecrite sur un papier, pliee, et portee dans le portefeuille ou sous l'oreiller.")
    pdf.ln(2)
    pdf.quote_box("Le talisman ne fonctionne que s'il est active par la pratique. Sans le rituel, c'est du papier.")

    # ═══════════════════════════════════════════════════
    # PAGE 25 — ADVANCED TECHNIQUES
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_light()
    pdf.section_title("XXIII.  T E C H N I Q U E S   A V A N C E E S")
    pdf.body_text("Pour ceux qui souhaitent approfondir la pratique, voici des techniques avancees.")
    pdf.ln(3)

    techniques = [
        ("Meditation sur le 19", "Visualisez le chiffre 19 en or au centre de votre front. Maintenez cette image pendant 19 secondes."),
        ("Respiration 7-1-9", "Inspirez sur 7 battements, retenez sur 1, expirez sur 9. Repetez 19 cycles."),
        ("Ecriture automatique", "Apres le rituel, ecrivez sans reflechir pendant 3 minutes. Les reponses viennent du subconscient."),
        ("Eau programmee", "Placez un verre d'eau sur le talisman pendant 7 minutes. Buvez-la apres le rituel."),
        ("Synchronicite", "Notez chaque synchronicite numerique dans un journal (11:11, 19:19, etc.)."),
        ("Zakat rituelle", "Donnez 1/40 de vos revenus (2.5%) chaque mois. Le flux circule."),
    ]

    for title, desc in techniques:
        pdf.set_font("L", "B", 10)
        pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
        pdf.cell(0, 6, title, align="L")
        pdf.ln()
        pdf.set_font("L", "", 9)
        pdf.set_text_color(60, 60, 60)
        pdf.multi_cell(0, 4.5, desc)
        pdf.ln(2)

    # ═══════════════════════════════════════════════════
    # PAGE 26 — 7 CIEUX
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_light()
    pdf.section_title("XXIV.  L E S   7   C I E U X   E T   L E   R I Z Q")
    pdf.body_text("Dans la cosmologie islamique, les 7 cieux correspondent aux 7 niveaux de descente du Rizq. Chaque ciel filtre et purifie la subsistance avant qu'elle n'atteigne la terre.")
    pdf.ln(3)

    cieux = [
        ("1er Ciel", "Sphere materielle", "Argent, nourriture, biens physiques"),
        ("2e Ciel", "Sphere emotionnelle", "Paix, amour, relations"),
        ("3e Ciel", "Sphere intellectuelle", "Idees, solutions, strategies"),
        ("4e Ciel", "Sphere du cœur", "Intuition, guidance interieure"),
        ("5e Ciel", "Sphere de l'ame", "Purpose, mission de vie"),
        ("6e Ciel", "Sphere spirituelle", "Connexion divine directe"),
        ("7e Ciel", "L'Arsh", "Source absolue du Rizq"),
    ]

    for ciel, sphere, desc in cieux:
        pdf.set_font("L", "B", 9)
        pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
        pdf.cell(35, 5.5, ciel, align="L")
        pdf.set_font("L", "B", 9)
        pdf.set_text_color(NIGHT_BLUE[0], NIGHT_BLUE[1], NIGHT_BLUE[2])
        pdf.cell(50, 5.5, sphere, align="L")
        pdf.set_font("L", "", 9)
        pdf.set_text_color(60, 60, 60)
        pdf.cell(0, 5.5, desc, align="L")
        pdf.ln()

    pdf.ln(4)
    pdf.body_text("Le rituel Miftah 19 traverse ces 7 niveaux : 7 repetitions de l'istighfar purifient chaque ciel successivement, permettant au Rizq de descendre purifie.")
    pdf.ln(2)
    pdf.quote_box("Le Rizq ne vient pas de la terre. Il descend des cieux. Le rituel est l'echelle.")

    # ═══════════════════════════════════════════════════
    # PAGE 27 — SYNCHRONICITES
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_light()
    pdf.section_title("XXV.  S Y N C H R O N I C I T E S   N U M E R I Q U E S")
    pdf.body_text("Apres avoir commence le rituel, vous remarquerez des synchronicites numeriques. Ce sont des confirmations.")
    pdf.ln(3)

    syncs = [
        ("19:19", "Heure miroir — signature active. Le code travaille."),
        ("11:11", "Portail ouvert — faites un vœu, dites Ya Razzaq."),
        ("7:07", "Multiplicateur actif — attendez-vous a une surprise."),
        ("3:33", "Age du Paradis — les anges sont proches."),
        ("1:11", "Tawhid renforce — unifiez votre intention."),
        ("22:22", "Miroir double — equilibre demande."),
        ("12:34", "Sequence ascendante — progression confirme."),
    ]

    for num, meaning in syncs:
        pdf.set_font("L", "B", 10)
        pdf.set_text_color(GOLD[0], GOLD[1], GOLD[2])
        pdf.set_fill_color(40, 20, 60)
        pdf.cell(25, 6, num, align="C", fill=True)
        pdf.set_font("L", "", 9)
        pdf.set_text_color(60, 60, 60)
        pdf.cell(0, 6, meaning, align="L")
        pdf.ln()

    pdf.ln(4)
    pdf.body_text("Tenez un journal de ces synchronicites. Apres 40 jours, vous aurez une preuve concrete du fonctionnement du code.")
    pdf.ln(2)
    pdf.quote_box("Les nombres ne mentent pas. Ils sont le langage de Dieu. (Galilee)")

    # ═══════════════════════════════════════════════════
    # PAGE 28 — MEDITATION
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_light()
    pdf.section_title("XXVI.  M E D I T A T I O N   E T   V I S U A L I S A T I O N")
    pdf.body_text("La meditation amplifie le rituel par un facteur de 10. Voici une technique specifique.")
    pdf.ln(3)

    pdf.sub_title("Meditation du Courant Violet-Dore")
    pdf.body_text("1. Asseyez-vous dans le silence. Fermez les yeux.\n"
                  "2. Visualisez un point lumineux au centre de votre poitrine.\n"
                  "3. Ce point s'elargit en un courant de couleur violette et doree.\n"
                  "4. Le courant monte par la colonne vertebrale jusqu'au sommet du crane.\n"
                  "5. Il redescend par les epaules, les bras, les mains.\n"
                  "6. Il remplit tout votre corps d'une lumiere chaude et douce.\n"
                  "7. Restez dans cette lumiere pendant 7 minutes.\n"
                  "8. Ouvrez lentement les yeux.")
    pdf.ln(3)

    pdf.sub_title("Visualisation du Rizq")
    pdf.body_text("Pendant le rituel, visualisez-vous en train de recevoir ce que vous desirez. Ne visualisez pas le manque. Visualisez l'abondance. L'univers repond a l'image mentale, pas aux mots.")
    pdf.ln(2)
    pdf.quote_box("Ce que l'esprit peut concevoir et croire, il peut l'atteindre. (Napoleon Hill)")

    # ═══════════════════════════════════════════════════
    # PAGE 29 — FAQ
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_light()
    pdf.section_title("XXVII.  F A Q   &   D E B U T A N T S")
    pdf.ln(2)

    faqs = [
        ("Dois-je comprendre l'arabe ?", "Non. L'intention et la presence suffisent. Mais apprendre la signification renforce l'effet."),
        ("Combien de temps avant de voir des resultats ?", "Certains voient des signes en 7 jours. La transformation profonde demande 40 jours."),
        ("Puis-je modifier le rituel ?", "Non. L'architecture mathematique est precise. Chaque nombre a une fonction."),
        ("Que faire si je manque une session ?", "Ne culpabilisez pas. Reprenez a la prochaine session. La baraka n'est pas dans la perfection."),
        ("Le talisman peut-il etre numerique ?", "Oui, mais le dessin manuel est plus puissant car il engage votre energie."),
        ("Puis-je partager ce workbook ?", "Oui. La transmission est une forme de Sadaqah."),
        ("Est-ce que cela remplace le travail ?", "Non. Le rituel ouvre les portes. Vous devez marcher a travers."),
    ]

    for q, a in faqs:
        pdf.set_x(15)
        pdf.set_font("L", "B", 9)
        pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
        pdf.multi_cell(180, 5, f"Q: {q}")
        pdf.set_x(15)
        pdf.set_font("L", "", 9)
        pdf.set_text_color(60, 60, 60)
        pdf.multi_cell(180, 4.5, f"R: {a}")
        pdf.ln(2)

    # ═══════════════════════════════════════════════════
    # PAGE 30 — GLOSSAIRE
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_light()
    pdf.section_title("XXVIII.  G L O S S A I R E")
    pdf.ln(2)

    glossary = [
        ("Abjad", "Systeme numerique attribuant une valeur a chaque lettre arabe."),
        ("Basmala", "Formule d'ouverture : Bismillah ir-Rahman ir-Rahim."),
        ("Baraka", "Benediction divine, grace qui multiplie."),
        ("Buduh", "Carre magique 3x3 utilise dans les talismans islamiques."),
        ("Code 19", "Structure mathematique du Coran centree sur le nombre 19."),
        ("Gematria", "Science des valeurs numeriques des mots (hebreu, grec, arabe)."),
        ("Grabovoi", "Codes numeriques vibratoires de manifestation (Grigori Grabovoi)."),
        ("Guematria Hebraique", "Systeme de correspondance lettres hebraiques / nombres."),
        ("Istighfar", "Demande de pardon a Allah."),
        ("Miftah", "Cle, ouverture."),
        ("Muqatta'at", "Lettres detachees au debut de certaines sourates."),
        ("Rizq", "Subsistence, provision, abondance divine."),
        ("Salawat", "Invocations de benediction sur le Prophete."),
        ("Radionique", "Science de la materialisation des frequences numeriques dans la matiere."),
        ("Sceau de Salomon", "Anneau legendaire de Salomon, symbole d'autorite cosmique."),
        ("Talisman Ultime", "Synthese des 3 traditions : Coran, Kabbale, Grabovoi."),
        ("Tasbih", "Glorification d'Allah par repetition."),
        ("Tawakkul", "Confiance absolue en Allah."),
        ("Tawhid", "Unicite divine."),
        ("Waqiah", "L'Inevitable, sourate 56."),
    ]

    for term, defn in glossary:
        pdf.set_font("L", "B", 9)
        pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
        pdf.cell(35, 5.5, term, align="L")
        pdf.set_font("L", "", 9)
        pdf.set_text_color(60, 60, 60)
        pdf.cell(0, 5.5, defn, align="L")
        pdf.ln()

    # ═══════════════════════════════════════════════════
    # PAGE 31 — NOTES
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_light()
    pdf.section_title("XXIX.  P A G E S   D E   N O T E S")
    pdf.ln(2)

    for i in range(12):
        pdf.set_draw_color(200, 200, 220)
        pdf.set_line_width(0.2)
        y = pdf.get_y()
        pdf.line(15, y, 195, y)
        pdf.ln(6)

    pdf.set_y(250)
    pdf.set_font("L", "", 8)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 5, "Utilisez ces lignes pour noter vos synchronicites, reves, et ressentis.", align="C")

    # ═══════════════════════════════════════════════════
    # PAGE 34 — TALISMAN ULTIUME (1/2)
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_light()
    pdf.section_title("XXX.  L E   T A L I S M A N   U L T I M E   M I F T A H   1 9")
    pdf.body_text("Ce chapitre est la synthese de trois traditions numerologiques millenaires : la numerologie coranique (Code 19, Abjad), la guematria hebraique (Kabbale), et les codes vibratoires modernes (Grabovoi). Leur point de convergence : le Sceau de Salomon.")
    pdf.ln(3)

    # ── DECOUVERTE CENTRALE ──
    pdf.sub_title("La Decouverte : Le Sceau de Salomon encode le Code 19")
    pdf.set_fill_color(LIGHT_VIOLET[0], LIGHT_VIOLET[1], LIGHT_VIOLET[2])
    pdf.set_draw_color(GOLD[0], GOLD[1], GOLD[2])
    pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
    pdf.set_font("L", "B", 9)
    pdf.set_x(20)
    pdf.cell(50, 6, "Langue", border=1, fill=True, align="C")
    pdf.cell(40, 6, "Sceau de Salomon", border=1, fill=True, align="C")
    pdf.cell(30, 6, "Valeur", border=1, fill=True, align="C")
    pdf.cell(30, 6, "Reduction", border=1, fill=True, align="C")
    pdf.ln()
    for lang, text, val, red in [
        ("Hebreu", "\u05d7\u05d5\u05ea\u05dd \u05e9\u05dc\u05de\u05d4", "829", "8+2+9 = 19"),
        ("Arabe", "\u202b\u062e\u0627\u062a\u0645 \u0633\u0644\u064a\u0645\u0627\u0646\u202c", "1232", "1+2+3+2 = 8"),
    ]:
        pdf.set_x(20)
        pdf.set_font("L", "B", 9)
        pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
        pdf.cell(50, 6, lang, border=1, align="C")
        pdf.set_font("A", "", 9)
        pdf.cell(40, 6, ar(text), border=1, align="C")
        pdf.set_font("L", "B", 10)
        pdf.set_text_color(GOLD[0], GOLD[1], GOLD[2])
        pdf.set_fill_color(40, 20, 60)
        pdf.cell(30, 6, val, border=1, fill=True, align="C")
        pdf.set_font("L", "", 9)
        pdf.set_text_color(60, 60, 60)
        pdf.cell(30, 6, red, border=1, align="C")
        pdf.ln()
    pdf.ln(4)
    pdf.body_text("Hotam Shlomo (\u05d7\u05d5\u05ea\u05dd \u05e9\u05dc\u05de\u05d4) en hebreu = 829 -> 8+2+9 = 19, le Code Sacre du Coran. Khatam Sulayman (\u202b\u062e\u0627\u062a\u0645 \u0633\u0644\u064a\u0645\u0627\u0646\u202c) en arabe = 1232 -> 1+2+3+2 = 8, les 8 directions du talisman Miftah. Le Sceau de Salomon est le point de convergence.")
    pdf.ln(3)

    # ── PONT 72 NOMS ↔ 99 NOMS ──
    pdf.sub_title("Le Pont des Noms Divins : 72 + 99 = 19 x 9")
    pdf.set_fill_color(MIDNIGHT[0], MIDNIGHT[1], MIDNIGHT[2])
    pdf.set_draw_color(GOLD[0], GOLD[1], GOLD[2])
    pdf.set_text_color(GOLD[0], GOLD[1], GOLD[2])
    pdf.set_font("L", "B", 10)
    pdf.set_x(25)
    pdf.cell(160, 8, "72 (Shem HaMephorash)  +  99 (Asma ul-Husna)  =  171  =  19 x 9", border=1, fill=True, align="C")
    pdf.ln(6)
    pdf.body_text("Les 72 noms hebreux de Dieu (derives d'Exode 14:19-21) et les 99 noms arabes d'Allah forment un total de 171, parfait multiple de 19. Le Code 19 est le pont mathematique entre les deux revelations.")
    pdf.ln(3)

    # ── GUEMATRIA HEBREU DES MOTS DU RIZQ ──
    pdf.sub_title("Guematria Hebraique du Rizq")
    for word, letters, val, note in [
        ("Osher (Richesse)", "\u05e2\u05e9\u05e8", "570", "12 -> 3 (harmonie)"),
        ("Mamon (Fortune)", "\u05de\u05de\u05d5\u05df", "136", "= 4 x 34 (constante Jupiter)"),
        ("Shefa (Abondance)", "\u05e9\u05e4\u05e2", "450", "4+5+0 = 9 (plenitude)"),
        ("Berakhah (Benediction)", "\u05d1\u05e8\u05db\u05d4", "227", "11 -> 2 (dualite)"),
    ]:
        pdf.set_font("L", "B", 9)
        pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
        pdf.cell(40, 5.5, word, align="L")
        pdf.set_font("A", "", 10)
        pdf.cell(15, 5.5, ar(letters), align="C")
        pdf.set_font("L", "B", 10)
        pdf.set_text_color(GOLD[0], GOLD[1], GOLD[2])
        pdf.set_fill_color(40, 20, 60)
        pdf.cell(20, 5.5, val, border=0, fill=True, align="C")
        pdf.set_font("L", "", 9)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0, 5.5, note, align="L")
        pdf.ln()
    pdf.ln(2)
    pdf.body_text("Mamon = 136 = 4 x 34. Or 34 est la constante du carre magique de Jupiter, la planete de la richesse en alchimie. Et 3+4 = 7, le multiplicateur divin du Rizq.")
    pdf.ln(2)

    # ── CARRE MAGIQUE BUDUH ──
    pdf.sub_title("Le Carre Magique Buduh (Tradition Islamique)")
    buduh = [["4", "9", "2"], ["3", "5", "7"], ["8", "1", "6"]]
    y0 = pdf.get_y()
    for i, row in enumerate(buduh):
        pdf.set_xy(70, y0 + i * 7)
        for j, cell in enumerate(row):
            pdf.set_fill_color(40, 20, 60)
            pdf.set_text_color(GOLD[0], GOLD[1], GOLD[2])
            pdf.set_font("L", "B", 11)
            pdf.cell(12, 7, cell, border=1, fill=True, align="C")
    pdf.set_xy(70, y0 + 22)
    pdf.set_font("L", "", 9)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(36, 5, "Constante: 15", align="C")
    pdf.ln(8)
    pdf.body_text("Le Buduh (3x3) est le carre magique le plus utilise dans les talismans islamiques. La somme de chaque rangee, colonne et diagonale = 15. Le 5 central represente l'equilibre, entoure des 8 autres nombres formant l'octogone energetique.")
    pdf.ln(2)

    # ═══════════════════════════════════════════════════
    # PAGE 35 — TALISMAN ULTIUME (2/2)
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_light()

    # ── ANNEAU DE SALOMON ──
    pdf.sub_title("L'Anneau de Salomon")
    pdf.body_text("Selon la tradition, l'anneau du roi Salomon portait le Nom Divin grave. Dans la tradition juive, le Tetragramme YHWH (\u05d9\u05d4\u05d5\u05d4) = 26. Dans la tradition islamique, l'inscription 'La ilaha illa Allah Al-Malik Al-Haqq Al-Mubin' = 558.")
    pdf.ln(2)
    pdf.body_text("Cet anneau donnait a Salomon le pouvoir de commander les vents, les animaux et les jinns. Il symbolise la maitrise des forces cosmiques par l'invocation du Nom Divin et la connaissance des nombres sacres.")
    pdf.ln(3)

    # ── CORRESPONDANCES PLANETAIRES ──
    pdf.sub_title("Correspondances Planetaires (Kabbale / Alchimie)")
    pdf.set_font("L", "B", 8)
    pdf.set_text_color(GOLD[0], GOLD[1], GOLD[2])
    pdf.set_fill_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
    pdf.set_x(15)
    for h in ["Planete", "Ordre", "Constante", "Sephirah", "Rizq"]:
        pdf.cell([25, 25, 25, 25, 70][["Planete", "Ordre", "Constante", "Sephirah", "Rizq"].index(h)], 6, h, border=1, fill=True, align="C")
    pdf.ln()
    for name, order, const, seph, rizq in [
        ("Saturne", "3x3", "15 -> 6", "Binah", "Structure, discipline"),
        ("Jupiter", "4x4", "34 -> 7", "Chesed", "Richesse, expansion Rizq"),
        ("Soleil", "6x6", "111 -> 3", "Tiphareth", "Succes, reconnaissance"),
        ("Venus", "7x7", "175 -> 4", "Netzach", "Harmonie, beaute"),
    ]:
        pdf.set_x(15)
        for val, w in [(name, 25), (order, 25), (const, 25), (seph, 25), (rizq, 70)]:
            pdf.set_font("L", "B" if val in [name, "Jupiter"] else "", 8)
            pdf.set_text_color(DARK_VIOLET[0] if val != "Jupiter" else GOLD[0],
                               DARK_VIOLET[1] if val != "Jupiter" else GOLD[1],
                               DARK_VIOLET[2] if val != "Jupiter" else GOLD[2])
            if val == "Jupiter":
                pdf.set_fill_color(40, 20, 60)
                pdf.cell(w, 5.5, val, border=1, fill=True, align="C")
            else:
                pdf.cell(w, 5.5, val, border=1, align="C")
        pdf.ln()
    pdf.ln(4)

    # ── ARCHITECTURE DU TALISMAN ULTIUME ──
    pdf.sub_title("Architecture du Talisman Ultime (7 Couches)")
    layers = [
        ("1. Centre", "Carre magique Buduh 3x3 (constante 15)", "Equilibre cosmique"),
        ("2. Anneau 1", "4 Noms Divins du Rizq (319+489+1060+1100=2968->7)", "Les 4 piliers de l'abondance"),
        ("3. Anneau 2", "4 Codes Grabovoi (520 741 8, 318 798...)", "Pont vibratoire moderne"),
        ("4. Anneau 3", "Etoile a 8 branches (Miftah 19)", "Directions du Rizq"),
        ("5. Anneau 4", "Guematria Hebraique (Osher, Shefa, Berakhah...)", "Sagesse de la Kabbale"),
        ("6. Anneau 5", "Inscription Sceau de Salomon (Arabe + Hebreu)", "Autorite cosmique"),
        ("7. Anneau ext.", "Code Al-Waqi'a : 56 96 152 = 19 x 8", "Signature finale"),
    ]
    for name, desc, note in layers:
        pdf.set_font("L", "B", 8)
        pdf.set_text_color(DARK_VIOLET[0], DARK_VIOLET[1], DARK_VIOLET[2])
        pdf.cell(25, 5, name, align="L")
        pdf.set_font("L", "", 8)
        pdf.set_text_color(60, 60, 60)
        pdf.cell(90, 5, desc, align="L")
        pdf.set_font("L", "", 7.5)
        pdf.set_text_color(120, 120, 140)
        pdf.cell(0, 5, note, align="R")
        pdf.ln()
    pdf.ln(4)

    # ── PONT FINAL ──
    pdf.sub_title("La Triple Signature : 7 / 8 / 19")
    pdf.set_fill_color(MIDNIGHT[0], MIDNIGHT[1], MIDNIGHT[2])
    pdf.set_draw_color(GOLD[0], GOLD[1], GOLD[2])
    pdf.set_text_color(GOLD[0], GOLD[1], GOLD[2])
    pdf.set_font("L", "B", 11)
    pdf.set_x(25)
    pdf.cell(160, 8, "7 (Rizq)  x  8 (Directions)  x  19 (Code)  =  Le Talisman Ultime", border=1, fill=True, align="C")
    pdf.ln(6)
    pdf.body_text("Le 7 est le multiplicateur divin du Rizq (2:261). Le 8 est le nombre de directions du talisman et la reduction arabe du Sceau de Salomon. Le 19 est le Code Sacre du Coran et la reduction hebraique du Sceau de Salomon.")
    pdf.ln(2)
    pdf.body_text("Ces trois nombres apparaissent dans le code Grabovoi 520 741 8, dans la sourate Al-Waqi'a (56=7x8, 152=19x8), et maintenant dans le Sceau de Salomon lui-meme. La boucle est bouclee.")
    pdf.ln(3)
    pdf.quote_box("Le Talisman Ultime n'est pas un objet. C'est une carte de l'univers numerique que Dieu a tisse dans les textes sacres de l'humanite. 7, 8, 19 : les trois piliers du Rizq eternel.")

    # ═══════════════════════════════════════════════════
    # PAGE 36 — RADIONIQUE SACREE
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_light()
    pdf.section_title("XXXI.  R A D I O N I Q U E   S A C R E E")
    pdf.body_text("La radionique est l'art de materialiser les frequences numeriques dans la matiere. Les codes ne sont pas que des symboles : ce sont des vibrations. Voici comment les ancrer physiquement pour qu'ils agissent 24h/24.")
    pdf.ln(3)

    # ── PRINCIPE ──
    pdf.sub_title("Le Principe")
    pdf.body_text("Tout nombre emet une frequence. Quand vous ecrivez un code sur du papier, vous imprimez cette frequence dans la matiere. Le papier devient un oscillateur passif. La photo cree une liaison sympathique avec votre champ biophotonique. Le cuivre amplifie le signal. Le quartz le stabilise et le programme.")
    pdf.ln(3)

    # ── LES 4 ELEMENTS ──
    pdf.sub_title("Les 4 Elements du Montage")
    elements = [
        ("1. Feuille + Codes", "Papier blanc A4. Recopiez les 4 codes Grabovoi (520 741 8, 318 798, 318 612 518 714, 9798733714615) en cercle. Ajoutez les nombres sacres (56, 19, 7, 152) aux interstices et les 4 Noms Divins (Razzaq, Fattah, Ghani, Mughni)."),
        ("2. Photo personnelle", "Photo portrait, visage centre, format 4x6cm environ. Placez-la FACE VERS LE BAS au centre des cercles de codes, contre le papier. C'est le witness : il lie les codes a vous."),
        ("3. Spirale de cuivre", "Fil de cuivre pur, 1mm de diametre, 56cm de long (56 = Al-Waqi'a = 7x8). Formez 7 tours de spirale a la main. Posez-la PAR-DESSUS la photo, au centre. La spirale est l'antenne amplificatrice."),
        ("4. Cristal de quartz", "Quartz pointe naturelle, 3-5cm. Placez-le pointe VERS LE HAUT, au centre de la spirale. Le quartz est piezoelectrique : il convertit, stocke et amplifie la frequence des codes."),
    ]
    for title, desc in elements:
        pdf.set_font("L", "B", 8)
        pdf.set_text_color(*DARK_VIOLET)
        pdf.set_x(15)
        pdf.cell(0, 4.5, title, align="L")
        pdf.set_font("L", "", 7)
        pdf.set_text_color(*BLACK)
        pdf.set_x(18)
        pdf.multi_cell(172, 3.8, desc)
        pdf.ln(1.5)
    pdf.ln(2)

    # ── CORRESPONDANCES ──
    pdf.sub_title("Correspondances Elements / Nombres Sacres")
    pdf.set_fill_color(*DARK_BG)
    pdf.set_text_color(*GOLD)
    pdf.set_font("L", "B", 6.5)
    pdf.set_x(15)
    for h, w in [("Element", 40), ("Nombre", 18), ("Effet", 65), ("Lien Miftah 19", 47)]:
        pdf.cell(w, 5, h, border=1, fill=True, align="C")
    pdf.ln()
    for elem, num, effect, lien in [
        ("Papier + 4 codes Grabovoi", "7, 8, 19", "Encodage vibratoire", "520 741 8 = 7+19+8"),
        ("Photo", "33", "Liaison biophotonique", "Age du Paradis, lien personnel"),
        ("56cm cuivre, 7 tours", "56, 7", "Antenne resonnante", "Al-Waqi'a = 56 = 7x8"),
        ("8 directions cercle", "8", "Distribution energetique", "Talisman Miftah 19"),
        ("Quartz pointe", "19", "Amplificateur", "Code 19, signature divine"),
        ("Montage complet", "152", "Synergie active 24/7", "19 x 8 = 152"),
    ]:
        pdf.set_font("L", "", 6)
        pdf.set_text_color(*BLACK)
        pdf.set_x(15)
        pdf.cell(40, 4.5, elem, border=1, align="L")
        pdf.set_font("L", "B", 7)
        pdf.set_text_color(*GOLD)
        pdf.cell(18, 4.5, num, border=1, align="C")
        pdf.set_font("L", "", 6)
        pdf.set_text_color(*GRAY)
        pdf.cell(65, 4.5, effect, border=1, align="L")
        pdf.set_text_color(*BLACK)
        pdf.cell(47, 4.5, lien, border=1, align="L")
        pdf.ln()
    pdf.ln(4)

    # ── PROTOCOLE ──
    pdf.sub_title("Protocole d'Activation Quotidien")
    times = [
        ("Matin (Fajr)", "Main droite sur quartz. Basmala 1x. Visualiser lumiere doree. 3 min."),
        ("Midi (Duha)", "4 Noms Divins 1x chacun. Visualiser 4 rayons colores vers le quartz."),
        ("Soir (Maghrib)", "Sourate Al-Waqi'a ou code 56-96-152. Main gauche en cercle 7x."),
        ("Nuit", "Mains en triangle sur quartz. Visualiser 56 96 152 en or dans le cristal."),
    ]
    for time, action in times:
        pdf.set_font("L", "B", 8)
        pdf.set_text_color(*DARK_VIOLET)
        pdf.cell(30, 4.5, time, align="L")
        pdf.set_font("L", "", 7)
        pdf.set_text_color(*BLACK)
        pdf.cell(0, 4.5, action, align="L")
        pdf.ln()
    pdf.ln(3)

    pdf.body_text("Duree recommandee : 40 jours consecutifs. Apres demontage, conservez la feuille de codes dans votre portefeuille. Purifiez le quartz a l'eau claire + soleil 1h avant reutilisation.")
    pdf.ln(2)
    pdf.quote_box("Les nombres ecrits deviennent des antennes. La spirale les amplifie. Le quartz les programme dans votre realite.")

    # ═══════════════════════════════════════════════════
    # PAGE 37 — CONCLUSION
    # ═══════════════════════════════════════════════════
    pdf.new_page()
    pdf.bg_violet()
    pdf.set_y(50)
    pdf.set_font("L", "B", 10)
    pdf.set_text_color(GOLD[0], GOLD[1], GOLD[2])
    pdf.cell(0, 8, "C O N C L U S I O N", align="C")
    pdf.ln(15)

    pdf.set_font("L", "", 11)
    pdf.set_text_color(200, 180, 220)
    pdf.multi_cell(0, 7, "Ce workbook n'est pas une fin. C'est un debut.\n\n"
                           "Les codes que vous avez decouverts ne sont pas des superstitions. Ce sont des structures mathematiques qui traversent le Coran depuis 1400 ans, invisibles aux yeux de ceux qui ne cherchent pas.\n\n"
                           "Le rituel Miftah 19 est votre cle. Le talisman est votre boussole. La pratique est votre chemin.\n\n"
                           "Que les portes du Rizq s'ouvrent devant vous.\n"
                           "Que la Providence vous guide.\n"
                           "Que la baraka descende sur chaque pas.", align="C")
    pdf.ln(20)

    pdf.set_font("A", "", 14)
    pdf.set_text_color(GOLD[0], GOLD[1], GOLD[2])
    pdf.cell(0, 10, ar("والله من وراء القصد"), align="C")
    pdf.ln(6)
    pdf.set_font("L", "", 9)
    pdf.set_text_color(180, 160, 200)
    pdf.cell(0, 5, "Wa-Allahu min wara'i al-qasd — Et Allah est derriere l'intention", align="C")
    pdf.ln(30)

    pdf.set_font("L", "", 8)
    pdf.set_text_color(140, 120, 160)
    pdf.cell(0, 5, "Workbook Miftah 19  |  Edition Mystique  |  2026  |  Tous droits reserves", align="C")

    # ── SAVE ──
    output = PDF_OUTPUTS["workbook_miftah"]
    pdf.output(str(output))
    print(f"PDF Premium genere : {output}")
    print(f"Pages : {pdf.page_count}")


if __name__ == "__main__":
    build_workbook()
