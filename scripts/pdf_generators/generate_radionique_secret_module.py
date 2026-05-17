#!/usr/bin/env python3
from __future__ import annotations

import math
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.esoteric_pdf_base import C, EsotericDoc
from core.miftah_phi_engine import QuranCorpus, analyze_reference
from core.project_paths import PDF_OUTPUTS, ensure_layout

ensure_layout()


def code_lines(result: dict) -> list[str]:
    return [
        f"{result['source']}  |  centre {result['talisman']['center']}",
        f"abjad {result['metrics']['abjad_total']}",
        f"mots {result['metrics']['word_count']}  |  lettres {result['metrics']['letter_count']}",
        f"pont {result['signature']['golden_bridge'][0]} / {result['signature']['golden_bridge'][1]} / {result['signature']['golden_bridge'][2]}",
    ]


def cover(pdf: EsotericDoc) -> None:
    pdf.skip_header = True
    pdf.add_page()
    pdf.set_fill_color(*C["dark"])
    pdf.rect(0, 0, 210, 297, "F")
    y = 28
    pdf.set_fill_color(*C["copper"])
    pdf.rect(34, y, 142, 2, "F")
    y += 10
    pdf.text(105, y, "MODULE RADIONIQUE", 22, True, C["gold"], "C", 200)
    y += 11
    pdf.text(105, y, "RIZQ • PHI • ABJAD", 12, True, C["violet_soft"], "C", 200)
    y += 11
    pdf.text(105, y, "Cuivre • Spirale • Quartz • Codes-ponts • Talisman derive", 8.2, False, C["white"], "C", 200)
    y += 12
    pdf.text_ar(105, y, "بسم الله الرحمن الرحيم", 17, C["gold"], "C", 200)
    y += 14
    for line in [
        "Noyau 1 : 51:58  |  source pure du rizq",
        "Noyau 2 : 65:2-3 |  issue et provision inattendue",
        "Noyau 3 : 71:10-12 | pluie, biens, jardins et rivieres",
        "Matrice-maitre : Sourate 56",
    ]:
        pdf.text(30, y, line, 7.1, False, C["white"], "L", 165)
        y += 8
    y += 8
    pdf.text(105, y, "Version operatoire autonome du laboratoire Miftah Phi.", 7.2, False, C["gold"], "C", 200)
    pdf.skip_header = False


def draw_module(pdf: EsotericDoc, center_result: dict, gate_a: dict, gate_b: dict, gate_c: dict) -> None:
    cx, cy = 105, 120
    pdf.set_draw_color(*C["copper"])
    pdf.set_line_width(0.7)
    pdf.circle(cx, cy, 56, "D")
    pdf.circle(cx, cy, 44, "D")
    pdf.circle(cx, cy, 31, "D")
    pdf.circle(cx, cy, 19, "D")
    pdf.draw_star_8(cx, cy, 49, 34)

    pdf.set_draw_color(*C["gold"])
    pdf.set_line_width(0.5)
    for deg in range(0, 360, 45):
        rad = math.radians(deg)
        x = cx + 56 * math.cos(rad)
        y = cy - 56 * math.sin(rad)
        pdf.line(cx, cy, x, y)

    pdf.text(cx, cy - 5, str(center_result["talisman"]["center"]), 13, True, C["violet"], "C", 20)
    pdf.text(cx, cy + 3, "56", 8, False, C["gold_dark"], "C", 20)

    outer = [
        gate_a["talisman"]["center"],
        gate_b["signature"]["reference_number"],
        gate_c["signature"]["reference_number"],
        center_result["metrics"]["abjad_reduced"],
        center_result["metrics"]["mod_19"],
        center_result["metrics"]["mod_7"],
        center_result["metrics"]["mod_8"],
        center_result["metrics"]["fib_word"],
    ]
    for idx, value in enumerate(outer):
        angle = 90 - idx * 45
        rad = math.radians(angle)
        x = cx + 61 * math.cos(rad)
        y = cy - 61 * math.sin(rad)
        pdf.set_fill_color(*C["cream"])
        pdf.set_draw_color(*C["gold"])
        pdf.rect(x - 8, y - 4, 16, 8, "DF")
        pdf.text(x, y - 1.5, str(value), 6, True, C["blue"], "C", 16)


def build() -> Path:
    corpus = QuranCorpus()
    master = analyze_reference(corpus, 56, domain_key="richesse")
    source = analyze_reference(corpus, 51, 58, domain_key="richesse")
    issue = analyze_reference(corpus, 65, 2, 3, domain_key="richesse")
    rain = analyze_reference(corpus, 71, 10, 12, domain_key="richesse")
    protection = analyze_reference(corpus, 2, 255, domain_key="protection")
    knowledge = analyze_reference(corpus, 20, 114, domain_key="savoir")

    pdf = EsotericDoc("Module Radionique Rizq", "Architecture cuivre, phi, talisman et codes-ponts")
    cover(pdf)

    pdf.set_context("DOCTRINE", "Le montage comme circuit symbolique")
    pdf.add_page()
    y = 24
    y = pdf.section(y, "AXIOME DE FONCTIONNEMENT")
    y = pdf.paragraph(
        y,
        "Le module radionique n'est pas pense ici comme machine physique au sens scientifique fort, "
        "mais comme circuit symbolique intensif : le texte fournit la cle, l'abjad la charge, phi "
        "la proportion, le cuivre la forme, le quartz le point de fixation, et la repetition le courant.",
        7.4,
    )
    y = pdf.box(
        y,
        "Les 4 noyaux du module",
        [
            "Noyau-source : 51:58",
            "Noyau-issue : 65:2-3",
            "Noyau-pluie : 71:10-12",
            "Noyau-maitre : sourate 56",
        ],
        C["blue_soft"],
    )
    y = pdf.box(
        y,
        "Sorties du moteur reutilisees",
        [
            "centre du talisman",
            "anneaux internes et externes",
            "code pont Grabovoi",
            "longueur cuivre conseillee",
            "nombre de tours primaire et secondaire",
        ],
        C["green_soft"],
    )

    pdf.set_context("NOYAUX", "Les codes-textes injectes dans le montage")
    pdf.add_page()
    y = 24
    y = pdf.section(y, "CODES ACTIFS")
    y = pdf.box(y, "Source  |  51:58", code_lines(source), C["rose_soft"], line_size=5.8)
    y = pdf.box(y, "Issue  |  65:2-3", code_lines(issue), C["blue_soft"], line_size=5.8)
    y = pdf.box(y, "Pluie  |  71:10-12", code_lines(rain), C["green_soft"], line_size=5.8)
    y = pdf.box(y, "Maitre  |  56", code_lines(master), C["rose_soft"], line_size=5.8)

    pdf.set_context("SCHEMA", "Montage concentrique")
    pdf.add_page()
    y = 24
    y = pdf.section(y, "PLAN DU MODULE")
    y = pdf.paragraph(
        y,
        "Le schema ci-dessous concentre la matrice-maitre et ses noyaux auxiliaires. "
        "Le centre 56 fixe la sourate ; l'octogone distribue ; les anneaux portent le code du moteur.",
        7.3,
    )
    draw_module(pdf, master, source, issue, rain)
    y = 196
    y = pdf.box(
        y,
        "Lecture du schema",
        [
            "Centre : reference-sceau de la sourate maitre.",
            "1er anneau : sous-structure textuelle du passage.",
            "2e anneau : projections phi et seuils Fibonacci.",
            "Rayons : diffusion par 8 directions.",
        ],
        C["blue_soft"],
        line_size=5.8,
    )

    pdf.set_context("SPECIFICATIONS", "Montage physique conseille")
    pdf.add_page()
    y = 24
    y = pdf.section(y, "FICHE TECHNIQUE")
    y = pdf.box(
        y,
        "Parametres derives de la sourate 56",
        [
            f"Longueur cuivre conseillee : {master['radionics']['copper_length_cm']} cm",
            f"Spirale primaire : {master['radionics']['primary_turns']} tours",
            f"Spirale secondaire : {master['radionics']['secondary_turns']} tours",
            f"Code central : {master['radionics']['center_code']}",
            f"Code anneau : {master['radionics']['ring_code']}",
        ],
        C["green_soft"],
        line_size=6.0,
    )
    y = pdf.box(
        y,
        "Materiaux",
        [
            "Papier blanc ou support rigide clair",
            "Fil de cuivre fin",
            "Quartz ou cristal clair",
            "Encre noire ou dorée pour le code",
            "Talisman derive du moteur place sous le centre ou sous la spirale",
        ],
        C["blue_soft"],
        line_size=6.0,
    )
    y = pdf.box(
        y,
        "Rythme",
        [
            "Cycle court : 7 jours",
            "Cycle normal : 14 jours",
            "Cycle dense : 21 jours",
            "Le matin pour ouvrir ; le soir pour fixer",
        ],
        C["rose_soft"],
        line_size=6.0,
    )

    pdf.set_context("ACTIVATION", "Dhikr et mise en tension")
    pdf.add_page()
    y = 24
    y = pdf.section(y, "SEQUENCE D'ACTIVATION")
    y = pdf.box(
        y,
        "Etape 1",
        [
            "Placer le schema du module, puis le talisman derive, puis le quartz.",
            "Lire 51:58 une fois en fixant le centre.",
            "Lire 65:2-3 une fois en fixant l'anneau interne.",
            "Lire 71:10-12 une fois en fixant l'anneau externe.",
        ],
        C["blue_soft"],
        line_size=5.9,
    )
    y = pdf.box(
        y,
        "Etape 2",
        [
            f"{master['dhikr'][1]['count']}x {master['dhikr'][1]['formula']}",
            f"{master['dhikr'][2]['count']}x {master['dhikr'][2]['formula']}",
            f"{master['dhikr'][3]['count']}x {master['dhikr'][3]['formula']}",
            f"{master['dhikr'][4]['count']}x {master['dhikr'][4]['formula']}",
        ],
        C["green_soft"],
        line_size=6.0,
    )
    y = pdf.box(
        y,
        "Etape 3",
        [
            "Lire lentement les 4 premiers codes-ponts du moteur.",
            "Placer les deux mains autour du montage pendant 3 a 8 minutes.",
            "Terminer par le sceau du dhikr et une gratitude explicite.",
        ],
        C["rose_soft"],
        line_size=6.0,
    )

    pdf.set_context("CALIBRATION", "Variantes du module")
    pdf.add_page()
    y = 24
    y = pdf.section(y, "ADAPTATIONS")
    y = pdf.box(
        y,
        "Richesse",
        [
            "Support maitre : 56",
            "Codes-ponts : 123 55 89 / 786 489 618",
            "Couleur dominante : or / cuivre / violet",
        ],
        C["green_soft"],
        line_size=5.8,
    )
    y = pdf.box(
        y,
        "Protection",
        [
            f"Support : {protection['source']}",
            f"Centre : {protection['talisman']['center']}",
            f"Code-pont : {protection['grabovoi_bridge'][0]}",
            "Couleur dominante : bleu nuit / violet",
        ],
        C["blue_soft"],
        line_size=5.8,
    )
    y = pdf.box(
        y,
        "Savoir",
        [
            f"Support : {knowledge['source']}",
            f"Centre : {knowledge['talisman']['center']}",
            f"Code-pont : {knowledge['grabovoi_bridge'][0]}",
            "Couleur dominante : bleu / or pâle",
        ],
        C["rose_soft"],
        line_size=5.8,
    )

    pdf.set_context("NOTES", "Source et limites")
    pdf.add_page()
    y = 24
    y = pdf.section(y, "NOTE FINALE")
    y = pdf.paragraph(
        y,
        "Ce module est une construction esoterique et experimentale. Le moteur ne remplace ni la lecture "
        "spirituelle, ni l'intelligence pratique, ni l'action dans le monde. Il fournit une charpente "
        "coherente pour travailler nombre, texte, souffle, geste et focalisation.",
        7.4,
    )
    y = pdf.bullets(
        y,
        [
            "Texte arabe et metadata : Tanzil Quran Text.",
            "Le moteur phi-abjad calcule les anneaux automatiquement.",
            "Le module reste modulable pour sante, savoir, protection et asrar.",
        ],
        7.1,
    )

    output = PDF_OUTPUTS["module_radionique_rizq"]
    pdf.output(str(output))
    return output


if __name__ == "__main__":
    out = build()
    print(f"PDF generated: {out}")
