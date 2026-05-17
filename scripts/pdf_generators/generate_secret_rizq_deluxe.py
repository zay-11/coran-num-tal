#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.esoteric_pdf_base import C, EsotericDoc
from core.miftah_phi_engine import PHI, QuranCorpus, analyze_reference
from core.project_paths import PDF_OUTPUTS, ensure_layout


ensure_layout()


def compact_lines(result: dict) -> list[str]:
    m = result["metrics"]
    s = result["signature"]
    return [
        f"Reference : {result['source']}  |  Centre : {result['talisman']['center']}",
        f"Abjad : {m['abjad_total']}  |  Mots : {m['word_count']}  |  Lettres : {m['letter_count']}",
        f"Pont phi : {s['golden_bridge'][0]} / {s['golden_bridge'][1]} / {s['golden_bridge'][2]}",
        f"Anneau interne : {' - '.join(str(x) for x in s['ring_inner'])}",
        f"Code pont : {result['grabovoi_bridge'][0]}  |  {result['grabovoi_bridge'][1]}",
    ]


def add_cover(pdf: EsotericDoc) -> None:
    pdf.skip_header = True
    pdf.add_page()
    pdf.set_fill_color(*C["night"])
    pdf.rect(0, 0, 210, 297, "F")
    y = 24
    pdf.set_fill_color(*C["gold"])
    pdf.rect(32, y, 146, 2, "F")
    y += 10
    pdf.text(105, y, "LE SECRET DU RIZQ", 25, True, C["gold"], "C", 200)
    y += 12
    pdf.text(105, y, "DELUXE", 11, True, C["violet_soft"], "C", 200)
    y += 10
    pdf.text(105, y, "Phi • Abjad • Couloir Fibonacci • Grabovoi • Talisman • Radionique", 8.5, False, C["white"], "C", 200)
    y += 11
    pdf.text_ar(105, y, "بسم الله الرحمن الرحيم", 17, C["gold"], "C", 200)
    y += 13
    for line in [
        "34 -> 55 -> 56 -> 89  |  couloir de l'abondance",
        "319 -> 489 -> 618 -> 786  |  echelle d'ouverture et de misericorde",
        "51:58 + 65:2-3 + 71:10-12  |  source, issue et pluie du rizq",
        "Le coeur du systeme : misericorde -> ouverture -> descente -> fixation",
    ]:
        pdf.text(27, y, line, 7.1, False, C["white"], "L", 165)
        y += 8
    y += 10
    pdf.hline(y, C["gold"], 0.45)
    y += 8
    pdf.text(105, y, "Version operatoire : lecture esoterique et experimentale.", 7.2, False, C["gold"], "C", 200)
    y += 8
    pdf.text(105, y, "Corpus arabe : Tanzil Quran Text (source attribuee en fin d'ouvrage).", 6.4, False, C["muted"], "C", 200)
    pdf.skip_header = False


def add_portal_page(pdf: EsotericDoc, title: str, subtitle: str, result: dict, doctrine: list[str]) -> None:
    pdf.set_context(title, subtitle)
    pdf.add_page()
    y = 24
    y = pdf.section(y, f"PORTE ACTIVE  |  {result['source']}")
    y = pdf.paragraph(y, result["text"]["uthmani"], 8.2, C["gold_dark"], False)
    y = pdf.box(y + 1, "Code extrait par le moteur", compact_lines(result), C["blue_soft"], line_size=5.8)
    y = pdf.sub(y, "Lecture operative")
    y = pdf.bullets(y, doctrine, 7.1)
    dhikr_preview = []
    for phase in result["dhikr"][:4]:
        dhikr_preview.append(f"{phase['count']}x {phase['formula']}")
    y = pdf.box(y, "Dhikr issu de cette porte", dhikr_preview, C["green_soft"], line_size=6.0)


def add_talisman_page(pdf: EsotericDoc, result: dict) -> None:
    pdf.set_context("TALISMAN DELUXE", "Sceau du rizq derive de la sourate-maitre")
    pdf.add_page()
    y = 24
    y = pdf.section(y, "SCHEMA TALISMANIQUE DE LA SOURATE 56")
    y = pdf.paragraph(
        y,
        "Ce sceau est derive directement du moteur a partir de la sourate 56 en domaine richesse. "
        "Le centre reprend la reference-source ; l'anneau interne fixe la charpente textuelle ; "
        "l'anneau externe porte les projections phi et Fibonacci.",
        7.3,
    )
    cx, cy = 105, 118
    pdf.draw_star_8(cx, cy, 43, 31)
    pdf.circle(cx, cy, 17, "D")
    pdf.text(105, 112, str(result["talisman"]["center"]), 14, True, C["violet"], "C", 20)
    pdf.text(105, 121, "Sourate-maitre", 6, False, C["gold_dark"], "C", 40)

    for idx, value in enumerate(result["talisman"]["inner_ring"]):
        angle = 90 - idx * 45
        import math
        rad = math.radians(angle)
        x = cx + 42 * math.cos(rad)
        yy = cy - 42 * math.sin(rad)
        pdf.set_fill_color(*C["cream"])
        pdf.set_draw_color(*C["gold"])
        pdf.rect(x - 7, yy - 4, 14, 8, "DF")
        pdf.text(x, yy - 1.5, str(value), 6.2, True, C["blue"], "C", 14)

    for idx, value in enumerate(result["talisman"]["outer_ring"]):
        angle = 67.5 - idx * 45
        import math
        rad = math.radians(angle)
        x = cx + 61 * math.cos(rad)
        yy = cy - 61 * math.sin(rad)
        pdf.set_fill_color(*C["white"])
        pdf.set_draw_color(*C["violet_soft"])
        pdf.rect(x - 8.5, yy - 4, 17, 8, "DF")
        pdf.text(x, yy - 1.5, str(value), 6.0, False, C["violet"], "C", 17)

    y = 186
    y = pdf.box(y, "Inscriptions", [str(x) for x in result["talisman"]["inscriptions"]], C["rose_soft"], line_size=6.0)
    y = pdf.box(y, "Activation", result["talisman"]["instructions"], C["green_soft"], line_size=5.8)


def add_domains_page(pdf: EsotericDoc, health: dict, knowledge: dict, occult: dict) -> None:
    pdf.set_context("EXTENSIONS", "Le moteur sur d'autres domaines")
    pdf.add_page()
    y = 24
    y = pdf.section(y, "APERÇU MULTI-DOMAINE")
    y = pdf.paragraph(
        y,
        "Le meme moteur ne sert pas uniquement a la richesse. Il peut lire un verset, calculer une "
        "signature numerique, puis proposer une sortie operative adaptee au domaine choisi.",
        7.4,
    )
    y = pdf.box(
        y,
        "Sante  |  17:82",
        compact_lines(health)[:4],
        C["green_soft"],
        line_size=5.8,
    )
    y = pdf.box(
        y,
        "Savoir  |  20:114",
        compact_lines(knowledge)[:4],
        C["blue_soft"],
        line_size=5.8,
    )
    y = pdf.box(
        y,
        "Asrar / Voiles  |  27:40",
        compact_lines(occult)[:4],
        C["rose_soft"],
        line_size=5.8,
    )
    y = pdf.paragraph(
        y,
        "Dans cette logique, le texte coranique devient une matrice d'extraction numerique : "
        "reference, abjad, nombre de mots, seuils phi, voisins Fibonacci, anneaux du talisman, "
        "comptage du dhikr et geometie du module radionique.",
        7.3,
    )


def add_protocol_page(pdf: EsotericDoc, wealth: dict) -> None:
    pdf.set_context("PROTOCOLE DELUXE", "Cycle complet sur 21 jours")
    pdf.add_page()
    y = 24
    y = pdf.section(y, "CYCLE RITUEL")
    y = pdf.box(
        y,
        "Matin",
        [
            "Lecture de 51:58 ou contemplation de son sceau.",
            f"{wealth['dhikr'][1]['count']}x {wealth['dhikr'][1]['formula']}",
            "Inscrire l'intention du jour en une phrase.",
        ],
        C["blue_soft"],
    )
    y = pdf.box(
        y,
        "Midi / Action",
        [
            "Une action concrete liee au rizq : creation, vente, appel, demande, service.",
            f"{wealth['dhikr'][2]['count']}x {wealth['dhikr'][2]['formula']}",
            "Visualiser le couloir 34 -> 55 -> 56 -> 89.",
        ],
        C["green_soft"],
    )
    y = pdf.box(
        y,
        "Soir",
        [
            "Lecture ou ecoute de la sourate 56.",
            f"{wealth['dhikr'][3]['count']}x {wealth['dhikr'][3]['formula']}",
            "3 lectures lentes du code 786 489 618 puis sceau final.",
        ],
        C["rose_soft"],
    )
    y = pdf.sub(y, "Axiome du deluxe")
    y = pdf.paragraph(
        y,
        "La richesse ne se fixe que si les trois etages restent relies : la Source (51:58), "
        "l'issue (65:2-3) et la pluie d'ouverture (71:10-12). Le nombre sert de serrure ; "
        "la pratique sert de cle ; l'action sert de preuve.",
        7.5,
    )


def add_notes_page(pdf: EsotericDoc) -> None:
    pdf.set_context("NOTES FINALES", "Sources et rectifications")
    pdf.add_page()
    y = 24
    y = pdf.section(y, "SOURCES")
    y = pdf.bullets(
        y,
        [
            "Corpus arabe : Tanzil Quran Text, format simple-clean et uthmani-min.",
            "Metadonnees de sourates : Tanzil Quran Metadata.",
            "Le moteur conserve une lecture symbolique et experimentale.",
            "Rectification numerique centrale : Al-Rahman + Al-Rahim = 618.",
            "Le couloir 34 -> 55 -> 56 -> 89 est interprete comme fil conducteur, non comme preuve scientifique.",
        ],
        7.1,
    )
    y = pdf.section(y + 2, "FORMULE FINALE")
    y = pdf.paragraph(
        y,
        "Le secret du rizq, dans cette version deluxe, est que la misericorde precalcule la forme "
        "de l'abondance avant sa manifestation materielle. Phi relie les seuils, l'abjad densifie "
        "les noms, le talisman fixe la carte, le dhikr anime la carte, et la radionique tente de "
        "maintenir le circuit ouvert dans la duree.",
        7.4,
    )
    y = pdf.paragraph(y + 2, "Wa-Allahu min wara'i al-qasd.", 8, C["gold_dark"], False, 22, 166, "C")


def build() -> Path:
    corpus = QuranCorpus()
    rizq_master = analyze_reference(corpus, 56, domain_key="richesse")
    razzaq_gate = analyze_reference(corpus, 51, 58, domain_key="richesse")
    issue_gate = analyze_reference(corpus, 65, 2, 3, domain_key="richesse")
    rain_gate = analyze_reference(corpus, 71, 10, 12, domain_key="richesse")
    health = analyze_reference(corpus, 17, 82, domain_key="sante")
    knowledge = analyze_reference(corpus, 20, 114, domain_key="savoir")
    occult = analyze_reference(corpus, 27, 40, domain_key="occultes")

    pdf = EsotericDoc("Le Secret du Rizq Deluxe", "Phi, Abjad, Talisman et Radionique")
    add_cover(pdf)

    pdf.set_context("DOCTRINE", "Architecture generale du secret")
    pdf.add_page()
    y = 24
    y = pdf.section(y, "THESE DU DELUXE")
    y = pdf.paragraph(
        y,
        "Le fil directeur du deluxe est simple : 51:58 pose la Source pure du rizq, 65:2-3 ouvre "
        "l'issue, 71:10-12 appelle la pluie, puis le couloir 34 -> 55 -> 56 -> 89 organise la "
        "descente du flux de l'invisible vers le manifeste.",
        7.5,
    )
    y = pdf.box(
        y,
        "Equation du systeme",
        [
            "Source : 51:58  ->  la provision vient d'Allah",
            "Cle : 65:2-3    ->  taqwa et tawakkul ouvrent une issue",
            "Pluie : 71:10-12 -> istighfar, biens, enfants, jardins, rivieres",
            "Couloir : 34 -> 55 -> 56 -> 89",
            f"Phi = {PHI:.6f}  |  passerelle de resonance entre les seuils",
        ],
        C["blue_soft"],
    )
    y = pdf.box(
        y,
        "Rectification fondatrice",
        [
            "Le coeur mercy-code n'est pas 684 mais 618.",
            "329 + 289 = 618  ->  Al-Rahman + Al-Rahim",
            "618 x phi ~ 1000  ->  seuil de dilatation symbolique",
            "Cette correction rend la charpente plus propre que l'ancienne version du projet.",
        ],
        C["rose_soft"],
    )

    add_portal_page(
        pdf,
        "PORTE-SOURCE",
        "51:58  |  Ar-Razzaq",
        razzaq_gate,
        [
            "Le verset sert de noyau-source : la provision existe avant la demande.",
            "Le centre 58 devient un nombre d'appel, pas seulement une reference.",
            "Le moteur propose ici une sortie courte, ideale pour le matin ou avant une action.",
        ],
    )
    add_portal_page(
        pdf,
        "PORTE-ISSUE",
        "65:2-3  |  Taqwa et voies inattendues",
        issue_gate,
        [
            "Cette porte sert a casser le blocage et a provoquer un deplacement des causes.",
            "Elle travaille mieux avec une demande precise et un geste concret immediat.",
            "Dans le deluxe, c'est la charniere entre l'appel et la manifestation.",
        ],
    )
    add_portal_page(
        pdf,
        "PORTE-PLUIE",
        "71:10-12  |  Istighfar et descente du flux",
        rain_gate,
        [
            "Le texte construit une image de pluie, de biens, de jardins et de rivieres.",
            "Cette porte est ideale pour les cycles de 7 ou 21 jours.",
            "Elle sert a faire descendre, non seulement a ouvrir.",
        ],
    )

    pdf.set_context("COULOIR", "34 -> 55 -> 56 -> 89")
    pdf.add_page()
    y = 24
    y = pdf.section(y, "LE COULOIR DE L'ABONDANCE")
    y = pdf.box(
        y,
        "Lecture numerique",
        [
            "34 = Saba : prosperite puis rupture de gratitude",
            "55 = Rahman : deversement des faveurs",
            "56 = Waqi'a : bascule vers le plan manifeste",
            "89 = Fajr : revelation, tri, epreuve de la richesse",
            "55 / 34 et 89 / 55 ouvrent le corridor Fibonacci de l'ouvrage",
        ],
        C["green_soft"],
    )
    y = pdf.paragraph(
        y,
        "Le deluxe lit ce couloir comme une sequence : une civilisation recoit, oublie, chute, puis "
        "la conscience est reorientee vers une abondance plus lucide. La richesse n'est donc pas le "
        "but final ; elle est un test de densite et de clarte.",
        7.4,
    )
    y = pdf.box(y, "Matrice-mere : Sourate 56", compact_lines(rizq_master), C["blue_soft"], line_size=5.8)

    add_talisman_page(pdf, rizq_master)
    add_protocol_page(pdf, rizq_master)
    add_domains_page(pdf, health, knowledge, occult)
    add_notes_page(pdf)

    output = PDF_OUTPUTS["secret_rizq_deluxe"]
    pdf.output(str(output))
    return output


if __name__ == "__main__":
    out = build()
    print(f"PDF generated: {out}")
