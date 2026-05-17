#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
import sys
from typing import Any

try:
    from .miftah_phi_engine import PHI, digital_root, nearest_fibonacci, nearest_sacred_count
    from .project_paths import IMPORTED_CORPORA_DIR
except ImportError:
    ROOT_DIR = Path(__file__).resolve().parents[1]
    if str(ROOT_DIR) not in sys.path:
        sys.path.insert(0, str(ROOT_DIR))
    from core.miftah_phi_engine import PHI, digital_root, nearest_fibonacci, nearest_sacred_count
    from core.project_paths import IMPORTED_CORPORA_DIR


BASE_DIR = Path(__file__).resolve().parent
CORPORA_DIR = IMPORTED_CORPORA_DIR
CORPORA_DIR.mkdir(exist_ok=True)


ARABIC_VALUES = {
    "ا": 1, "أ": 1, "إ": 1, "آ": 1, "ٱ": 1, "ء": 1, "ؤ": 6, "ئ": 10,
    "ب": 2, "ج": 3, "د": 4, "ه": 5, "ة": 5, "و": 6, "ز": 7, "ح": 8, "ط": 9,
    "ي": 10, "ى": 10, "ك": 20, "ل": 30, "م": 40, "ن": 50, "س": 60, "ع": 70,
    "ف": 80, "ص": 90, "ق": 100, "ر": 200, "ش": 300, "ت": 400, "ث": 500,
    "خ": 600, "ذ": 700, "ض": 800, "ظ": 900, "غ": 1000,
}

HEBREW_VALUES = {
    "א": 1, "ב": 2, "ג": 3, "ד": 4, "ה": 5, "ו": 6, "ז": 7, "ח": 8, "ט": 9,
    "י": 10, "כ": 20, "ך": 20, "ל": 30, "מ": 40, "ם": 40, "נ": 50, "ן": 50,
    "ס": 60, "ע": 70, "פ": 80, "ף": 80, "צ": 90, "ץ": 90, "ק": 100, "ר": 200,
    "ש": 300, "ת": 400,
}

GREEK_VALUES = {
    "α": 1, "β": 2, "γ": 3, "δ": 4, "ε": 5, "ϛ": 6, "ζ": 7, "η": 8, "θ": 9,
    "ι": 10, "κ": 20, "λ": 30, "μ": 40, "ν": 50, "ξ": 60, "ο": 70, "π": 80,
    "ϟ": 90, "ρ": 100, "σ": 200, "ς": 200, "τ": 300, "υ": 400, "φ": 500,
    "χ": 600, "ψ": 700, "ω": 800, "ϡ": 900,
}


SCRIPT_CONFIGS = {
    "arabic_abjad": {
        "label": "Abjad arabe",
        "values": ARABIC_VALUES,
        "letters_re": re.compile(r"[\u0621-\u063A\u0641-\u064A]"),
        "cleanup_re": re.compile(r"[^\u0621-\u063A\u0641-\u064A\s]"),
    },
    "hebrew_gematria": {
        "label": "Guematrie hebraique",
        "values": HEBREW_VALUES,
        "letters_re": re.compile(r"[\u05D0-\u05EA]"),
        "cleanup_re": re.compile(r"[^\u05D0-\u05EA\s]"),
    },
    "greek_isopsephy": {
        "label": "Isopsephie grecque",
        "values": GREEK_VALUES,
        "letters_re": re.compile(r"[α-ωϛϟϡςΑ-Ω]"),
        "cleanup_re": re.compile(r"[^α-ωϛϟϡςΑ-Ω\s]"),
    },
}


GENERIC_DOMAINS = {
    "richesse": {
        "label": "Richesse / Abondance",
        "color": "gold",
        "geometry": "etoile a 8 branches",
        "spirit_words": ["ouverture", "flux", "expansion", "fixation"],
    },
    "sante": {
        "label": "Sante / Guerison",
        "color": "emerald",
        "geometry": "hexagone de regeneration",
        "spirit_words": ["apaisement", "restauration", "souffle", "coherence"],
    },
    "savoir": {
        "label": "Savoir / Intelligence sacree",
        "color": "blue",
        "geometry": "triangle de vision",
        "spirit_words": ["clarte", "ouverture", "comprehension", "penetration"],
    },
    "protection": {
        "label": "Protection / Bouclier",
        "color": "violet",
        "geometry": "double cercle de garde",
        "spirit_words": ["limite", "filtre", "retour", "fixite"],
    },
    "occultes": {
        "label": "Asrar / Voiles / Invisible",
        "color": "midnight",
        "geometry": "octogone des voiles",
        "spirit_words": ["voile", "seuil", "revelation", "discernement"],
    },
}


@dataclass
class ImportedCorpus:
    corpus_id: str
    name: str
    scheme: str
    description: str
    entries: list[dict[str, str]]


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text or "corpus"


def normalize_text(text: str, scheme: str) -> str:
    cfg = SCRIPT_CONFIGS[scheme]
    if scheme == "arabic_abjad":
        substitutions = {"أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا", "ؤ": "و", "ئ": "ي", "ى": "ي", "ة": "ه"}
        text = "".join(substitutions.get(ch, ch) for ch in text)
    elif scheme == "greek_isopsephy":
        text = text.lower()
    text = cfg["cleanup_re"].sub(" ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_letters(text: str, scheme: str) -> list[str]:
    normalized = normalize_text(text, scheme)
    return SCRIPT_CONFIGS[scheme]["letters_re"].findall(normalized)


def value_sum(text: str, scheme: str) -> int:
    values = SCRIPT_CONFIGS[scheme]["values"]
    return sum(values.get(ch.lower(), values.get(ch, 0)) for ch in extract_letters(text, scheme))


def compute_metrics(text: str, scheme: str) -> dict[str, Any]:
    normalized = normalize_text(text, scheme)
    letters = extract_letters(text, scheme)
    words = [w for w in normalized.split(" ") if w]
    total = value_sum(text, scheme)
    fib_word, ratio_word = nearest_fibonacci(len(words))
    fib_letter, ratio_letter = nearest_fibonacci(len(letters))
    fib_total, ratio_total = nearest_fibonacci(total)
    return {
        "word_count": len(words),
        "letter_count": len(letters),
        "unique_letters": len(set(letters)),
        "value_total": total,
        "value_reduced": digital_root(total),
        "mod_19": total % 19 or 19,
        "mod_8": len(letters) % 8 or 8,
        "mod_7": len(words) % 7 or 7,
        "golden_value": round(total / PHI),
        "golden_letters": round(len(letters) * PHI),
        "golden_words": round(len(words) * PHI),
        "fib_word": fib_word,
        "fib_letter": fib_letter,
        "fib_total": fib_total,
        "fib_word_ratio": ratio_word,
        "fib_letter_ratio": ratio_letter,
        "fib_total_ratio": ratio_total,
    }


def spirit_profile(metrics: dict[str, Any], domain: str) -> dict[str, Any]:
    theme = GENERIC_DOMAINS[domain]
    root = metrics["value_reduced"]
    quadrant = ((root - 1) % 4)
    spirit_word = theme["spirit_words"][quadrant]
    if root in {1, 3, 7, 9}:
        polarity = "emission"
    elif root in {2, 4, 8}:
        polarity = "construction"
    else:
        polarity = "transmutation"
    return {
        "root": root,
        "spirit_word": spirit_word,
        "polarity": polarity,
        "formula": f"{root}-{metrics['mod_19']}-{metrics['mod_7']}-{metrics['mod_8']}",
        "reading": f"Le texte porte une tonalite de {spirit_word} avec une polarite de {polarity}.",
    }


def build_signature(metrics: dict[str, Any], ref_label: str, domain: str) -> dict[str, Any]:
    ref_digits = [int(x) for x in re.findall(r"\d+", ref_label)] or [metrics["value_reduced"]]
    center = ref_digits[-1]
    inner = [
        center,
        metrics["word_count"],
        metrics["letter_count"],
        metrics["value_reduced"],
        metrics["mod_19"],
        metrics["mod_7"],
        metrics["mod_8"],
        metrics["fib_word"],
    ]
    outer = [
        metrics["golden_words"],
        metrics["golden_letters"],
        metrics["golden_value"],
        metrics["fib_letter"],
        metrics["fib_total"],
        nearest_sacred_count(metrics["golden_value"]),
        nearest_sacred_count(metrics["golden_letters"]),
        nearest_sacred_count(metrics["golden_words"]),
    ]
    return {
        "center": center,
        "inner_ring": inner,
        "outer_ring": outer,
        "reference_label": ref_label,
        "geometry": GENERIC_DOMAINS[domain]["geometry"],
    }


def build_practice(text: str, metrics: dict[str, Any], domain: str, scheme: str) -> list[dict[str, Any]]:
    words = normalize_text(text, scheme).split()
    seed = " ".join(words[: min(4, len(words))]) if words else text[:24]
    counts = [
        1,
        nearest_sacred_count(metrics["golden_words"]),
        nearest_sacred_count(metrics["value_reduced"] + metrics["mod_7"]),
        nearest_sacred_count(metrics["mod_19"] + metrics["mod_8"]),
    ]
    return [
        {"phase": "ouverture", "formula": seed, "count": counts[0], "note": "Pose le champ."},
        {"phase": "charge", "formula": seed, "count": counts[1], "note": "Charge le texte."},
        {"phase": "fixation", "formula": str(metrics["value_total"]), "count": counts[2], "note": "Fixe la valeur."},
        {"phase": "sceau", "formula": f"{metrics['golden_value']} {metrics['fib_total']}", "count": counts[3], "note": "Scelle le circuit."},
    ]


def analyze_generic_text(text: str, scheme: str, domain: str = "richesse",
                         source_ref: str = "custom-text", corpus_name: str | None = None) -> dict[str, Any]:
    if scheme not in SCRIPT_CONFIGS:
        raise KeyError(f"Unknown scheme {scheme}")
    if domain not in GENERIC_DOMAINS:
        raise KeyError(f"Unknown domain {domain}")
    metrics = compute_metrics(text, scheme)
    spirit = spirit_profile(metrics, domain)
    signature = build_signature(metrics, source_ref, domain)
    bridge = [
        f"{signature['center']} {metrics['value_reduced']} {metrics['mod_19']}",
        f"{metrics['golden_words']} {metrics['golden_letters']} {metrics['golden_value']}",
        f"{metrics['fib_word']} {metrics['fib_letter']} {metrics['fib_total']}",
    ]
    result = {
        "source": source_ref,
        "corpus_name": corpus_name or "custom",
        "scheme": scheme,
        "scheme_label": SCRIPT_CONFIGS[scheme]["label"],
        "domain": GENERIC_DOMAINS[domain],
        "text": text,
        "metrics": metrics,
        "spirit": spirit,
        "signature": signature,
        "bridge_codes": bridge,
        "practice": build_practice(text, metrics, domain, scheme),
        "talisman": {
            "center": signature["center"],
            "inner_ring": signature["inner_ring"],
            "outer_ring": signature["outer_ring"],
            "geometry": signature["geometry"],
            "color": GENERIC_DOMAINS[domain]["color"],
            "instructions": [
                "Tracer la geometrie annoncee par la signature.",
                "Placer le centre puis l'anneau interne dans le sens horaire.",
                "Placer l'anneau externe dans le sens antihoraire.",
                "Reciter la pratique en regardant le centre du sceau.",
            ],
        },
    }
    return result


def parse_entries(raw: str) -> list[dict[str, str]]:
    raw = raw.strip()
    if not raw:
        return []
    if raw.startswith("[") or raw.startswith("{"):
        data = json.loads(raw)
        if isinstance(data, dict):
            data = data.get("entries", [])
        entries = []
        for item in data:
            ref = str(item.get("ref") or item.get("reference") or item.get("id") or "")
            text = str(item.get("text") or "")
            if ref and text:
                entries.append({"ref": ref, "text": text})
        return entries
    entries = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        if "|" not in line:
            continue
        ref, text = line.split("|", 1)
        ref = ref.strip()
        text = text.strip()
        if ref and text:
            entries.append({"ref": ref, "text": text})
    return entries


def save_corpus(name: str, scheme: str, raw_entries: str, description: str = "") -> ImportedCorpus:
    entries = parse_entries(raw_entries)
    if not entries:
        raise ValueError("No valid entries found. Expected JSON entries or lines in 'ref|text' format.")
    corpus_id = slugify(name)
    path = CORPORA_DIR / f"{corpus_id}.json"
    payload = {
        "corpus_id": corpus_id,
        "name": name,
        "scheme": scheme,
        "description": description,
        "entries": entries,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return ImportedCorpus(**payload)


def list_corpora() -> list[dict[str, Any]]:
    corpora = []
    for path in sorted(CORPORA_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        corpora.append(
            {
                "corpus_id": data["corpus_id"],
                "name": data["name"],
                "scheme": data["scheme"],
                "description": data.get("description", ""),
                "entry_count": len(data.get("entries", [])),
            }
        )
    return corpora


def load_corpus(corpus_id: str) -> ImportedCorpus:
    path = CORPORA_DIR / f"{slugify(corpus_id)}.json"
    if not path.exists():
        raise FileNotFoundError(f"Corpus not found: {corpus_id}")
    data = json.loads(path.read_text(encoding="utf-8"))
    return ImportedCorpus(**data)


def analyze_corpus_entry(corpus_id: str, ref: str, domain: str = "richesse") -> dict[str, Any]:
    corpus = load_corpus(corpus_id)
    matches = [entry for entry in corpus.entries if str(entry["ref"]) == str(ref)]
    if not matches:
        raise KeyError(f"Reference not found: {ref}")
    entry = matches[0]
    return analyze_generic_text(entry["text"], corpus.scheme, domain, source_ref=entry["ref"], corpus_name=corpus.name)
