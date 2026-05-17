#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.miftah_phi_engine import QuranCorpus, analyze_reference
from core.project_paths import LIBRARY_ANALYSES_DIR, LIBRARY_DIR, LIBRARY_TALISMANS_DIR
from core.talisman_image_generator import render_talisman


BASE_DIR = ROOT_DIR
LIB_DIR = LIBRARY_DIR
ANALYSIS_DIR = LIBRARY_ANALYSES_DIR
TALISMAN_DIR = LIBRARY_TALISMANS_DIR
ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
TALISMAN_DIR.mkdir(parents=True, exist_ok=True)

DOMAINS = ["richesse", "sante", "savoir", "protection", "occultes"]


def build() -> Path:
    corpus = QuranCorpus()
    index = {
        "book": "Quran",
        "surah_count": len(corpus.suras),
        "domains": DOMAINS,
        "entries": [],
    }

    for sura in range(1, 115):
        meta = corpus.suras[sura]
        entry = {
            "sura": sura,
            "name_ar": meta.name,
            "name_en": meta.ename,
            "tname": meta.tname,
            "ayas": meta.ayas,
            "domain_files": {},
            "canonical_talisman": "",
        }

        canonical = analyze_reference(corpus, sura, domain_key="richesse")
        canonical_path = TALISMAN_DIR / f"sura_{sura:03d}_richesse.png"
        render_talisman(canonical, canonical_path, title=f"Sura {sura:03d} - {meta.tname}")
        entry["canonical_talisman"] = str(canonical_path.relative_to(BASE_DIR)).replace("\\", "/")

        for domain in DOMAINS:
            result = analyze_reference(corpus, sura, domain_key=domain)
            out_path = ANALYSIS_DIR / f"sura_{sura:03d}_{domain}.json"
            out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
            entry["domain_files"][domain] = str(out_path.relative_to(BASE_DIR)).replace("\\", "/")

        index["entries"].append(entry)

    index_path = LIB_DIR / "quran_surah_library.json"
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    return index_path


if __name__ == "__main__":
    out = build()
    print(out)
