#!/usr/bin/env python3
"""
RAG — CORAN NUM TAL
Systeme de recherche semantique sur le corpus complet.
Interrogeable en ligne de commande ou via API.
"""

from __future__ import annotations
import json, math, re, sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

PHI = (1 + math.sqrt(5)) / 2


def load_corpus() -> list[dict]:
    """Load all knowledge from the project corpus."""
    docs = []

    # 1. All surah analysis files
    analyses_dir = ROOT / "documents/library/analyses"
    if analyses_dir.exists():
        for f in sorted(analyses_dir.glob("*.json")):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                sura = data.get("source", "")
                domain = data.get("domain", {}).get("key", "")
                text = data.get("text", {}).get("simple", "")
                abjad = data.get("metrics", {}).get("abjad_total", 0)
                docs.append({
                    "id": f.name.replace(".json", ""),
                    "type": "surah_analysis",
                    "sura": sura,
                    "domain": domain,
                    "text": text[:200],
                    "abjad": abjad,
                    "content": json.dumps(data, ensure_ascii=False),
                    "keywords": extract_keywords(data),
                })
            except Exception:
                pass

    # 2. Quranic roots dictionary (from dictionnaire data)
    roots_data = [
        ("رزق", "RZQ", "Subsistance, provision, rizq", 123, 307),
        ("شكر", "ShKR", "Gratitude, reconnaissance", 75, 520),
        ("برك", "BRK", "Baraka, benediction", 32, 222),
        ("فتح", "FTH", "Ouverture, conquete", 38, 488),
        ("غنى", "GhNY", "Richesse, autosuffisance", 73, 1060),
        ("رحم", "RHM", "Misericorde, compassion", 339, 248),
        ("نور", "NWR", "Lumiere, illumination", 43, 256),
        ("حفظ", "HFZ", "Garde, preservation", 44, 988),
        ("علم", "'ALM", "Science, connaissance", 854, 130),
        ("وهب", "WHB", "Don, donation", 25, 14),
        ("كرم", "KRM", "Generosite, noblesse", 47, 260),
        ("بسط", "BST", "Extension, dilation", 25, 71),
        ("كفى", "KFY", "Suffisance, contentement", 33, 100),
    ]
    for arabic, translit, meaning, occ, abjad_val in roots_data:
        docs.append({
            "id": f"root_{translit}",
            "type": "quranic_root",
            "arabic": arabic,
            "translit": translit,
            "meaning": meaning,
            "occurrences": occ,
            "abjad": abjad_val,
            "content": f"Racine {arabic} ({translit}): {meaning}. {occ} occurrences. Abjad: {abjad_val}.",
            "keywords": [translit.lower(), meaning.lower(), arabic],
        })

    # 3. Sacred numbers
    sacred = [
        (1, "Tawhid, Unicite divine"),
        (7, "Multiplicateur divin du Rizq (2:261), 7 cieux, completion"),
        (8, "Directions du talisman, octogone, infini"),
        (19, "Code 19, signature coranique (74:30), 19 lettres Basmala"),
        (34, "Saba, prosperite, point de depart du corridor Fibonacci"),
        (55, "Al-Rahman, deversement de faveurs"),
        (56, "Al-Waqi'a, sourate de la richesse, 7x8=56"),
        (61, "Cycle rituel complet: 1+7+19+33+1"),
        (76, "Matrice des 4 noms: 19x4"),
        (89, "Al-Fajr, aube et revelation"),
        (99, "Horizon des Noms divins, completude"),
        (123, "Occurrences du mot Rizq dans le Coran"),
        (319, "Abjad de Ya Razzaq"),
        (489, "Abjad de Fattah"),
        (618, "Rahman+Rahim, coeur misericordieux, miroir de 1/phi"),
        (786, "Basmala, porte d'ouverture"),
    ]
    for num, meaning in sacred:
        phi_val = round(num * PHI, 1)
        docs.append({
            "id": f"sacred_{num}",
            "type": "sacred_number",
            "number": num,
            "meaning": meaning,
            "phi_projection": phi_val,
            "content": f"Nombre sacre {num}: {meaning}. Projection phi: {phi_val}.",
            "keywords": [str(num), meaning.lower(), f"phi_{phi_val}"],
        })

    # 4. Phi discoveries
    discoveries = [
        ("19x4xphi->123", "Matrice fondamentale du rizq: le code 19 applique aux 4 noms produit le seuil 123"),
        ("55xphi->89", "Corridor Rahman->Fajr: la sourate 55 projette vers 89 par phi"),
        ("489xphi->786", "Ouverture: Fattah (489) projete vers Basmala (786)"),
        ("618xphi->1000", "Coeur misericordieux: Rahman+Rahim (618) projete vers 1000+"),
        ("61xphi->99", "Cycle rituel: le cycle 61 projete vers l'horizon des 99 Noms"),
    ]
    for title, desc in discoveries:
        docs.append({
            "id": f"discovery_{title.replace(' ', '_')}",
            "type": "phi_discovery",
            "title": title,
            "description": desc,
            "content": f"Decouverte phi: {title}. {desc}",
            "keywords": title.lower().replace("->", " ").replace("x", " ").split(),
        })

    return docs


def extract_keywords(data: dict) -> list[str]:
    """Extract searchable keywords from analysis data."""
    kw = []
    domain = data.get("domain", {})
    if isinstance(domain, dict):
        kw.extend([domain.get("key", ""), domain.get("label", "")])
    text = data.get("text", {})
    if isinstance(text, dict):
        kw.append(text.get("sura_name_en", ""))
        kw.append(text.get("sura_translit", ""))
    metrics = data.get("metrics", {})
    if isinstance(metrics, dict):
        kw.append(str(metrics.get("abjad_total", "")))
        kw.append(str(metrics.get("word_count", "")))
    return [k.lower() for k in kw if k]


def search(query: str, docs: list[dict], top_k: int = 10) -> list[dict]:
    """Simple keyword + semantic search over the corpus."""
    q_terms = query.lower().split()
    scored = []
    for doc in docs:
        score = 0
        content_lower = doc.get("content", "").lower()
        keywords = doc.get("keywords", [])
        # Keyword matching
        for term in q_terms:
            if term in content_lower:
                score += 3
            for kw in keywords:
                if term in str(kw).lower():
                    score += 2
        # Exact number matching
        if re.search(r"\d+", query):
            nums = re.findall(r"\d+", query)
            for n in nums:
                if n in content_lower:
                    score += 5
        if score > 0:
            scored.append((score, doc))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]


def rag_query(query: str) -> str:
    """Full RAG pipeline: retrieve + augment + generate."""
    docs = load_corpus()
    results = search(query, docs, top_k=8)

    context_parts = []
    for r in results:
        ctx = r.get("content", "")[:300]
        context_parts.append(f"[{r['type']}] {ctx}")

    context = "\n".join(context_parts)

    # Generate response from context
    response_parts = [f"=== Recherche RAG CORAN NUM TAL ==="]
    response_parts.append(f"Requete: {query}")
    response_parts.append(f"Documents trouves: {len(results)}")
    response_parts.append(f"\nContexte extrait:\n{context}")

    # Extract key numbers from results
    numbers = set()
    for r in results:
        if r["type"] == "sacred_number":
            numbers.add(r["number"])
        elif r["type"] == "quranic_root":
            numbers.add(r["abjad"])

    if numbers:
        response_parts.append(f"\nNombres cles associes: {sorted(numbers)}")

    # Compute phi projection of query-relevant numbers
    for num in list(numbers)[:5]:
        response_parts.append(f"  {num} x phi = {round(num * PHI, 1)}")

    return "\n".join(response_parts)


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/rag_query.py '<votre question>'")
        print("\nExemples:")
        print("  python scripts/rag_query.py 'quelle est la valeur abjad de rizq'")
        print("  python scripts/rag_query.py 'quels sont les nombres sacres du projet'")
        print("  python scripts/rag_query.py 'explique le corridor fibonacci 34 55 89'")
        return

    query = " ".join(sys.argv[1:])
    response = rag_query(query)
    print(response)

    # Save to file
    out = ROOT / "exports/rag/query_result.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(response, encoding="utf-8")


if __name__ == "__main__":
    main()
