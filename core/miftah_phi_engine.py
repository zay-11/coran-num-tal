#!/usr/bin/env python3
"""
Miftah Phi Engine

Moteur esoterique pour analyser une sourate, un verset ou un texte arabe,
en extraire une signature numerique et proposer des sorties operatives :
- code mathematique
- talisman
- dhikr
- rituel
- module radionique

Le moteur assume une lecture symbolique, numerologique et experimentale.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

try:
    from .project_paths import QURAN_DATA_DIR
except ImportError:
    ROOT_DIR = Path(__file__).resolve().parents[1]
    if str(ROOT_DIR) not in sys.path:
        sys.path.insert(0, str(ROOT_DIR))
    from core.project_paths import QURAN_DATA_DIR


PHI = (1 + math.sqrt(5)) / 2
INV_PHI = 1 / PHI
SACRED_COUNTS = [1, 3, 7, 8, 11, 19, 21, 33, 34, 55, 61, 76, 89, 99, 114, 123]
DATA_DIR = QURAN_DATA_DIR

TEXT_URLS = {
    "simple": "https://tanzil.net/pub/download/index.php?quranType=simple-clean&outType=txt-2&agree=true",
    "uthmani": "https://tanzil.net/pub/download/index.php?quranType=uthmani-min&outType=txt-2&agree=true",
    "metadata": "http://tanzil.net/res/text/metadata/quran-data.xml",
}

FILES = {
    "simple": DATA_DIR / "quran-simple-clean.txt",
    "uthmani": DATA_DIR / "quran-uthmani-min.txt",
    "metadata": DATA_DIR / "quran-data.xml",
}

ARABIC_LETTER_RE = re.compile(r"[\u0621-\u063A\u0641-\u064A]")
NON_ARABIC_RE = re.compile(r"[^\u0621-\u063A\u0641-\u064A\s]")

ABJAD = {
    "ا": 1,
    "أ": 1,
    "إ": 1,
    "آ": 1,
    "ٱ": 1,
    "ء": 1,
    "ؤ": 6,
    "ئ": 10,
    "ب": 2,
    "ج": 3,
    "د": 4,
    "ه": 5,
    "ة": 5,
    "و": 6,
    "ز": 7,
    "ح": 8,
    "ط": 9,
    "ي": 10,
    "ى": 10,
    "ك": 20,
    "ل": 30,
    "م": 40,
    "ن": 50,
    "س": 60,
    "ع": 70,
    "ف": 80,
    "ص": 90,
    "ق": 100,
    "ر": 200,
    "ش": 300,
    "ت": 400,
    "ث": 500,
    "خ": 600,
    "ذ": 700,
    "ض": 800,
    "ظ": 900,
    "غ": 1000,
}


@dataclass
class SuraMeta:
    index: int
    ayas: int
    start: int
    name: str
    tname: str
    ename: str
    place: str
    order: int
    rukus: int


@dataclass
class VerseRecord:
    sura: int
    ayah: int
    text_simple: str
    text_uthmani: str


@dataclass
class TextMetrics:
    word_count: int
    letter_count: int
    unique_letters: int
    abjad_total: int
    abjad_reduced: int
    mod_19: int
    mod_8: int
    mod_7: int
    golden_abjad: int
    golden_letters: int
    golden_words: int
    fib_word: int
    fib_letter: int
    fib_abjad: int
    fib_word_ratio: float
    fib_letter_ratio: float
    fib_abjad_ratio: float


@dataclass
class DomainProfile:
    key: str
    label: str
    intent: str
    color: str
    geometry: str
    references: list[str]
    divine_names: list[dict[str, Any]]
    grabovoi_seed: list[str]
    anchor_numbers: list[int]


def ensure_data() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for key, path in FILES.items():
        if path.exists() and path.stat().st_size > 512:
            continue
        with urllib.request.urlopen(TEXT_URLS[key]) as response:
            data = response.read()
        path.write_bytes(data)


def normalize_arabic(text: str, keep_spaces: bool = True) -> str:
    substitutions = {
        "أ": "ا",
        "إ": "ا",
        "آ": "ا",
        "ٱ": "ا",
        "ؤ": "و",
        "ئ": "ي",
        "ى": "ي",
        "ة": "ه",
    }
    text = "".join(substitutions.get(ch, ch) for ch in text)
    text = NON_ARABIC_RE.sub(" " if keep_spaces else "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def arabic_letters(text: str) -> list[str]:
    return ARABIC_LETTER_RE.findall(normalize_arabic(text))


def abjad_sum(text: str) -> int:
    return sum(ABJAD.get(ch, 0) for ch in arabic_letters(text))


def digital_root(value: int) -> int:
    if value == 0:
        return 0
    while value > 9:
        value = sum(int(d) for d in str(value))
    return value


def fibonacci_up_to(limit: int) -> list[int]:
    fib = [1, 1]
    while fib[-1] < max(2, limit):
        fib.append(fib[-1] + fib[-2])
    return fib


def nearest_fibonacci(value: int) -> tuple[int, float]:
    if value <= 1:
        return 1, 1.0
    fibs = fibonacci_up_to(value * 2)
    nearest = min(fibs, key=lambda x: abs(x - value))
    ratio = value / nearest if nearest else 0.0
    return nearest, ratio


def nearest_sacred_count(value: float) -> int:
    return min(SACRED_COUNTS, key=lambda x: abs(x - value))


def divine_name(label: str, arabic: str, translit: str) -> dict[str, Any]:
    return {
        "label": label,
        "arabic": arabic,
        "transliteration": translit,
        "abjad": abjad_sum(arabic),
    }


def build_domain_profiles() -> dict[str, DomainProfile]:
    profiles = {
        "richesse": DomainProfile(
            key="richesse",
            label="Rizq / Richesse / Abondance",
            intent="Ouverture des causes, fluidite materielle, baraka et expansion du rizq.",
            color="gold",
            geometry="etoile a 8 branches avec centre phi",
            references=["51:58", "65:2-3", "71:10-12", "62:10", "34:39"],
            divine_names=[
                divine_name("Razzaq", "يا رزاق", "Ya Razzaq"),
                divine_name("Fattah", "يا فتاح", "Ya Fattah"),
                divine_name("Ghani", "يا غني", "Ya Ghani"),
                divine_name("Mughni", "يا مغني", "Ya Mughni"),
            ],
            grabovoi_seed=["123 55 89", "786 489 618", "6119 078"],
            anchor_numbers=[19, 55, 56, 61, 76, 89, 99, 123, 319, 489, 618, 786],
        ),
        "sante": DomainProfile(
            key="sante",
            label="Sante / Guerison / Regeneration",
            intent="Apaisement, restauration, discipline du souffle et regeneration symbolique.",
            color="emerald",
            geometry="hexagone central avec anneau 7-19",
            references=["17:82", "26:80", "10:57", "41:44"],
            divine_names=[
                divine_name("Shafi", "يا شافي", "Ya Shafi"),
                divine_name("Salam", "يا سلام", "Ya Salam"),
                divine_name("Latif", "يا لطيف", "Ya Latif"),
                divine_name("Hayy", "يا حي", "Ya Hayy"),
            ],
            grabovoi_seed=["918 794 818", "519 714 819", "786 391 131"],
            anchor_numbers=[7, 17, 19, 41, 57, 82, 99, 131, 391],
        ),
        "savoir": DomainProfile(
            key="savoir",
            label="Savoir / Science / Fath intellectuel",
            intent="Ouverture du sens, memoire, comprehension et penetration symbolique.",
            color="blue",
            geometry="triangle + cercle de 9 points",
            references=["20:114", "2:269", "58:11", "96:1-5"],
            divine_names=[
                divine_name("Alim", "يا عليم", "Ya Alim"),
                divine_name("Hakim", "يا حكيم", "Ya Hakim"),
                divine_name("Fattah", "يا فتاح", "Ya Fattah"),
                divine_name("Nur", "يا نور", "Ya Nur"),
            ],
            grabovoi_seed=["114 269 5811", "489 150 186", "96 20 114"],
            anchor_numbers=[2, 20, 58, 96, 114, 150, 186, 489],
        ),
        "protection": DomainProfile(
            key="protection",
            label="Protection / Bouclier / Fermeture des fuites",
            intent="Consolidation du champ, fermeture des portes de dispersion et garde symbolique.",
            color="violet",
            geometry="cercle double + huit sceaux",
            references=["2:255", "113:1-5", "114:1-6", "3:173"],
            divine_names=[
                divine_name("Hafiz", "يا حفيظ", "Ya Hafiz"),
                divine_name("Qahhar", "يا قهار", "Ya Qahhar"),
                divine_name("Wakil", "يا وكيل", "Ya Wakil"),
                divine_name("Nur", "يا نور", "Ya Nur"),
            ],
            grabovoi_seed=["255 113 114", "917 418 619", "4812412"],
            anchor_numbers=[2, 3, 6, 19, 113, 114, 173, 255],
        ),
        "occultes": DomainProfile(
            key="occultes",
            label="Asrar / Voiles / Perception du cache",
            intent="Travail sur le sens voile, l'intuition, les synchronicites et le discernement invisible.",
            color="midnight",
            geometry="octogone noir + centre lunaire",
            references=["18:65", "27:40", "72:26-27", "20:114"],
            divine_names=[
                divine_name("Batin", "يا باطن", "Ya Batin"),
                divine_name("Latif", "يا لطيف", "Ya Latif"),
                divine_name("Hakim", "يا حكيم", "Ya Hakim"),
                divine_name("Nur", "يا نور", "Ya Nur"),
            ],
            grabovoi_seed=["1840 7227", "2740 651", "786 129 186"],
            anchor_numbers=[18, 20, 27, 40, 65, 72, 114, 129, 186],
        ),
    }
    return profiles


class QuranCorpus:
    def __init__(self, base_dir: Path | None = None) -> None:
        self.base_dir = base_dir or DATA_DIR
        ensure_data()
        self.suras: dict[int, SuraMeta] = {}
        self.verses_simple: dict[tuple[int, int], str] = {}
        self.verses_uthmani: dict[tuple[int, int], str] = {}
        self._load_metadata()
        self._load_texts()

    def _load_metadata(self) -> None:
        text = FILES["metadata"].read_text(encoding="utf-8", errors="ignore")
        pattern = re.compile(
            r'<sura index="(?P<index>\d+)" ayas="(?P<ayas>\d+)" start="(?P<start>\d+)" '
            r'name="(?P<name>[^"]+)" tname="(?P<tname>[^"]+)" ename="(?P<ename>[^"]+)" '
            r'type="(?P<place>[^"]+)" order="(?P<order>\d+)" rukus="(?P<rukus>\d+)"'
        )
        for match in pattern.finditer(text):
            groups = match.groupdict()
            meta = SuraMeta(
                index=int(groups["index"]),
                ayas=int(groups["ayas"]),
                start=int(groups["start"]),
                name=groups["name"],
                tname=groups["tname"],
                ename=groups["ename"],
                place=groups["place"],
                order=int(groups["order"]),
                rukus=int(groups["rukus"]),
            )
            self.suras[meta.index] = meta

    def _load_text_file(self, path: Path) -> dict[tuple[int, int], str]:
        records: dict[tuple[int, int], str] = {}
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            parts = line.split("|", 2)
            if len(parts) != 3:
                continue
            sura, ayah, text = int(parts[0]), int(parts[1]), parts[2].strip()
            records[(sura, ayah)] = text
        return records

    def _load_texts(self) -> None:
        self.verses_simple = self._load_text_file(FILES["simple"])
        self.verses_uthmani = self._load_text_file(FILES["uthmani"])

    def get_verse(self, sura: int, ayah: int) -> VerseRecord:
        key = (sura, ayah)
        return VerseRecord(
            sura=sura,
            ayah=ayah,
            text_simple=self.verses_simple[key],
            text_uthmani=self.verses_uthmani.get(key, self.verses_simple[key]),
        )

    def get_surah_verses(self, sura: int, start: int | None = None, end: int | None = None) -> list[VerseRecord]:
        meta = self.suras[sura]
        start = start or 1
        end = end or meta.ayas
        return [self.get_verse(sura, ayah) for ayah in range(start, end + 1)]

    def render_reference(self, sura: int, ayah: int | None = None, end: int | None = None) -> str:
        if ayah is None:
            return f"{sura}"
        if end and end != ayah:
            return f"{sura}:{ayah}-{end}"
        return f"{sura}:{ayah}"


def compute_metrics(text: str) -> TextMetrics:
    normalized = normalize_arabic(text)
    letters = arabic_letters(text)
    words = [w for w in normalized.split(" ") if w]
    total = abjad_sum(text)
    fib_word, ratio_word = nearest_fibonacci(len(words))
    fib_letter, ratio_letter = nearest_fibonacci(len(letters))
    fib_abjad, ratio_abjad = nearest_fibonacci(total)
    return TextMetrics(
        word_count=len(words),
        letter_count=len(letters),
        unique_letters=len(set(letters)),
        abjad_total=total,
        abjad_reduced=digital_root(total),
        mod_19=(total % 19) or 19,
        mod_8=(len(letters) % 8) or 8,
        mod_7=(len(words) % 7) or 7,
        golden_abjad=round(total * INV_PHI),
        golden_letters=round(len(letters) * PHI),
        golden_words=round(len(words) * PHI),
        fib_word=fib_word,
        fib_letter=fib_letter,
        fib_abjad=fib_abjad,
        fib_word_ratio=ratio_word,
        fib_letter_ratio=ratio_letter,
        fib_abjad_ratio=ratio_abjad,
    )


def build_signature_numbers(metrics: TextMetrics, sura: int | None, ayah_start: int | None,
                            ayah_end: int | None, domain: DomainProfile) -> dict[str, Any]:
    reference_number = sura or metrics.mod_19
    ayah_number = ayah_start or metrics.mod_7
    range_number = ayah_end or metrics.word_count
    if sura and ayah_start and ayah_end == ayah_start:
        center = ayah_start
    elif sura:
        center = sura
    else:
        center = nearest_sacred_count(metrics.abjad_reduced * metrics.mod_19)
    ring_inner = [
        reference_number,
        ayah_number,
        metrics.word_count,
        metrics.letter_count,
        metrics.abjad_reduced,
        metrics.mod_19,
        metrics.mod_7,
        metrics.mod_8,
    ]
    ring_outer = [
        metrics.golden_words,
        metrics.golden_letters,
        metrics.golden_abjad,
        metrics.fib_word,
        metrics.fib_letter,
        metrics.fib_abjad,
        domain.anchor_numbers[0],
        domain.anchor_numbers[-1],
    ]
    return {
        "center": center,
        "ring_inner": ring_inner,
        "ring_outer": ring_outer,
        "reference_number": reference_number,
        "ayah_number": ayah_number,
        "range_number": range_number,
        "golden_bridge": [metrics.golden_words, metrics.golden_letters, metrics.golden_abjad],
    }


def build_grabovoi_bridge(metrics: TextMetrics, domain: DomainProfile, sura: int | None,
                          ayah_start: int | None) -> list[str]:
    pieces = [
        f"{metrics.abjad_reduced}{metrics.mod_19}{metrics.mod_7}",
        f"{metrics.golden_words} {metrics.golden_letters} {metrics.mod_8}",
        f"{sura or metrics.mod_19}{ayah_start or metrics.mod_7} {metrics.fib_word}",
    ]
    return domain.grabovoi_seed + pieces


def build_dhikr_plan(metrics: TextMetrics, domain: DomainProfile) -> list[dict[str, Any]]:
    names = domain.divine_names
    primary = nearest_sacred_count(metrics.word_count * PHI)
    secondary = nearest_sacred_count(metrics.letter_count * INV_PHI)
    tertiary = nearest_sacred_count(metrics.mod_19 + metrics.mod_7 + metrics.mod_8)
    plan = [
        {
            "phase": "ouverture",
            "formula": "Bismillah ir-Rahman ir-Rahim",
            "count": 1,
            "note": "Stabilise l'intention et ouvre la porte numerique.",
        }
    ]
    for idx, name in enumerate(names):
        count = [primary, secondary, tertiary, metrics.mod_19][idx % 4]
        plan.append(
            {
                "phase": name["label"].lower(),
                "formula": name["transliteration"],
                "arabic": name["arabic"],
                "abjad": name["abjad"],
                "count": count,
                "note": f"Ancre le domaine {domain.key} dans la matrice du texte.",
            }
        )
    plan.append(
        {
            "phase": "sceau",
            "formula": "Hasbunallahu wa ni'ma al-wakil",
            "count": nearest_sacred_count(metrics.abjad_reduced + metrics.mod_7),
            "note": "Ferme le circuit et renvoie le travail a la Source.",
        }
    )
    return plan


def build_talisman(signature: dict[str, Any], domain: DomainProfile, metrics: TextMetrics) -> dict[str, Any]:
    return {
        "geometry": domain.geometry,
        "color": domain.color,
        "center": signature["center"],
        "inner_ring": signature["ring_inner"],
        "outer_ring": signature["ring_outer"],
        "inscriptions": [
            domain.divine_names[0]["arabic"],
            domain.divine_names[1]["arabic"],
            domain.divine_names[2]["arabic"],
            domain.divine_names[3]["arabic"],
            f"phi={PHI:.6f}",
            f"abjad={metrics.abjad_total}",
        ],
        "instructions": [
            "Tracer le centre puis les 8 directions.",
            "Placer le nombre central au coeur du sceau.",
            "Placer l'anneau interne dans le sens horaire a partir de l'Est.",
            "Placer l'anneau externe dans le sens antihoraire pour creer la tension symbolique.",
            "Reciter le dhikr associe devant le talisman pendant 7, 14 ou 21 jours.",
        ],
    }


def build_radionic_module(metrics: TextMetrics, domain: DomainProfile, signature: dict[str, Any]) -> dict[str, Any]:
    primary_turns = min(19, max(7, metrics.mod_19))
    secondary_turns = min(11, max(3, metrics.mod_7))
    copper_length = round((metrics.golden_words + metrics.mod_19) * INV_PHI, 1)
    return {
        "copper_length_cm": copper_length,
        "primary_turns": primary_turns,
        "secondary_turns": secondary_turns,
        "center_code": f"{signature['center']} {metrics.golden_abjad} {metrics.abjad_reduced}",
        "ring_code": f"{metrics.golden_words} {metrics.golden_letters} {metrics.fib_word} {metrics.fib_letter}",
        "grabovoi_bridge": build_grabovoi_bridge(metrics, domain, signature["reference_number"], signature["ayah_number"])[:4],
        "activation": [
            "Ecrire le code central au centre du montage.",
            "Placer le talisman derive du texte sous la spirale ou sous le quartz.",
            "Activer avec 1 ouverture, 1 cycle du dhikr et 3 lectures du code pont.",
            "Maintenir le travail sur 7, 14 ou 21 jours selon l'intensite recherchee.",
        ],
    }


def build_ritual(metrics: TextMetrics, domain: DomainProfile, talisman: dict[str, Any]) -> dict[str, Any]:
    return {
        "duration_days": 7 if metrics.mod_7 <= 3 else 21,
        "best_windows": [
            "avant Fajr",
            "entre Dhuhr et Asr",
            "apres Maghrib",
        ],
        "protocol": [
            "Purifier l'intention en une phrase simple.",
            "Lire ou contempler le verset ou la sourate support.",
            "Reciter le dhikr calcule avec souffle stable.",
            "Fixer le regard sur le centre du talisman 3 a 8 minutes.",
            "Terminer par gratitude, tawakkul et un geste concret dans le monde.",
        ],
        "talisman_focus": talisman["center"],
        "warning": "Lecture symbolique et experimentale ; ne pas substituer ce travail a une action reelle necessaire.",
    }


def infer_domain(domain_key: str | None) -> DomainProfile:
    profiles = build_domain_profiles()
    if not domain_key:
        return profiles["richesse"]
    key = domain_key.strip().lower()
    if key not in profiles:
        raise KeyError(f"Unknown domain '{domain_key}'. Domains: {', '.join(sorted(profiles))}")
    return profiles[key]


def analyze_text(text: str, domain_key: str | None = None, source_ref: str | None = None,
                 sura: int | None = None, ayah_start: int | None = None, ayah_end: int | None = None) -> dict[str, Any]:
    domain = infer_domain(domain_key)
    metrics = compute_metrics(text)
    signature = build_signature_numbers(metrics, sura, ayah_start, ayah_end, domain)
    talisman = build_talisman(signature, domain, metrics)
    dhikr = build_dhikr_plan(metrics, domain)
    ritual = build_ritual(metrics, domain, talisman)
    radionics = build_radionic_module(metrics, domain, signature)
    result = {
        "source": source_ref or "custom-text",
        "domain": asdict(domain),
        "metrics": asdict(metrics),
        "signature": signature,
        "grabovoi_bridge": build_grabovoi_bridge(metrics, domain, sura, ayah_start),
        "talisman": talisman,
        "dhikr": dhikr,
        "ritual": ritual,
        "radionics": radionics,
        "phi": PHI,
        "inverse_phi": INV_PHI,
    }
    return result


def analyze_reference(corpus: QuranCorpus, sura: int, ayah: int | None = None,
                      end: int | None = None, domain_key: str | None = None) -> dict[str, Any]:
    verses = corpus.get_surah_verses(sura, ayah, end)
    text_simple = " ".join(v.text_simple for v in verses)
    text_uthmani = " ".join(v.text_uthmani for v in verses)
    result = analyze_text(
        text=text_simple,
        domain_key=domain_key,
        source_ref=corpus.render_reference(sura, ayah, end),
        sura=sura,
        ayah_start=ayah or 1,
        ayah_end=end or (ayah or corpus.suras[sura].ayas),
    )
    result["text"] = {
        "simple": text_simple,
        "uthmani": text_uthmani,
        "sura_name_ar": corpus.suras[sura].name,
        "sura_name_en": corpus.suras[sura].ename,
        "sura_translit": corpus.suras[sura].tname,
        "revelation_place": corpus.suras[sura].place,
    }
    return result


def pretty_summary(result: dict[str, Any]) -> str:
    m = result["metrics"]
    s = result["signature"]
    domain = result["domain"]["label"]
    lines = [
        f"Source: {result['source']}",
        f"Domain: {domain}",
        f"Abjad total: {m['abjad_total']}",
        f"Words / letters: {m['word_count']} / {m['letter_count']}",
        f"Golden bridge: {s['golden_bridge']}",
        f"Talisman center: {result['talisman']['center']}",
        f"Grabovoi bridge: {', '.join(result['grabovoi_bridge'][:3])}",
        "Dhikr phases:",
    ]
    for phase in result["dhikr"]:
        lines.append(f"  - {phase['phase']}: {phase['count']}x {phase['formula']}")
    return "\n".join(lines)


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Miftah Phi Engine")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_ref = sub.add_parser("analyze-ref", help="Analyze a Quran reference")
    p_ref.add_argument("--sura", type=int, required=True)
    p_ref.add_argument("--ayah", type=int)
    p_ref.add_argument("--end", type=int)
    p_ref.add_argument("--domain", default="richesse")
    p_ref.add_argument("--json-out")
    p_ref.add_argument("--pretty", action="store_true")

    p_text = sub.add_parser("analyze-text", help="Analyze custom Arabic text")
    p_text.add_argument("--text", required=True)
    p_text.add_argument("--domain", default="richesse")
    p_text.add_argument("--json-out")
    p_text.add_argument("--pretty", action="store_true")

    p_domains = sub.add_parser("domains", help="List supported domains")

    args = parser.parse_args()

    if args.cmd == "domains":
        print(json.dumps({k: asdict(v) for k, v in build_domain_profiles().items()}, ensure_ascii=False, indent=2))
        return

    if args.cmd == "analyze-text":
        result = analyze_text(args.text, args.domain)
    else:
        corpus = QuranCorpus()
        result = analyze_reference(corpus, args.sura, args.ayah, args.end, args.domain)

    if getattr(args, "json_out", None):
        Path(args.json_out).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    if getattr(args, "pretty", False):
        print(pretty_summary(result))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
