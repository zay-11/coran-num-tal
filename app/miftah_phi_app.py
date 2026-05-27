#!/usr/bin/env python3
from __future__ import annotations

import datetime
import json
import math
import mimetypes
import os
import re
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.miftah_phi_engine import QuranCorpus, analyze_reference, build_domain_profiles, abjad_sum, digital_root
from core.project_paths import GENERATED_DIR, LIBRARY_DIR, WEBAPP_DIR, PDF_DIR, AUDIO_DIR
from core.sacred_text_engine import (
    GENERIC_DOMAINS,
    SCRIPT_CONFIGS,
    analyze_corpus_entry,
    analyze_generic_text,
    list_corpora,
    load_corpus,
    save_corpus,
)
from core.talisman_image_generator import render_talisman
from core.predictive_oracle import (
    predict,
    compute_daily_oracle,
    compute_personal_signature,
    TOTAL_ABJAD,
    TOTAL_ABJAD_SOURCE,
    TOTAL_ABJAD_VERSES,
    TOTAL_ABJAD_LETTERS,
    TOTAL_ABJAD_DR,
    NOMBRE_SECRET,
    NOM_SECRET_NOM,
    WAQIA_ABJAD,
    BASMALA_ABJAD,
    SOMME_SOURATES,
    CODE_19_FACTEUR,
    PHI as ORACLE_PHI,
)

BASE_DIR = ROOT_DIR
STATIC_DIR = WEBAPP_DIR
LIB_INDEX = LIBRARY_DIR / "quran_surah_library.json"

QURAN = QuranCorpus()

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# ── Constantes astronomiques ────────────────────────────────────────────────
SYNODIC_MONTH = 29.53059  # jours (lunaire)
# Nouvelle lune de référence vérifiée : 11 janvier 2024 à 11h57 UTC
_KNOWN_NEW_MOON = datetime.date(2024, 1, 11)
PHI = (1 + math.sqrt(5)) / 2


def json_bytes(payload: object) -> bytes:
    return json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")


# ── Mansion lunaire (corrigée) ───────────────────────────────────────────────
def lunar_mansion(target_date: datetime.date) -> int:
    """Calcule la mansion lunaire (1-28) à partir d'une date.
    Utilise la période synodique exacte (29.53059 jours) et une
    nouvelle lune de référence vérifiée astronomiquement."""
    delta = (target_date - _KNOWN_NEW_MOON).days
    cycle_day = delta % SYNODIC_MONTH          # 0 = nouvelle lune
    # 28 mansions réparties sur le cycle synodique
    mansion_idx = int(cycle_day / (SYNODIC_MONTH / 28)) % 28
    return mansion_idx + 1                      # 1-28


def moon_phase_name(target_date: datetime.date) -> str:
    """Retourne la phase lunaire approximative en français (sans emoji)."""
    delta = (target_date - _KNOWN_NEW_MOON).days
    day = delta % SYNODIC_MONTH
    if day < 1.5:
        return "Nouvelle lune"
    elif day < 7.4:
        return "Premier croissant"
    elif day < 8.8:
        return "Premier quartier"
    elif day < 14.2:
        return "Lune gibbeuse croissante"
    elif day < 15.5:
        return "Pleine lune"
    elif day < 22.1:
        return "Lune gibbeuse decroissante"
    elif day < 23.5:
        return "Dernier quartier"
    else:
        return "Dernier croissant"


# ── Translittération Nom → Abjad ────────────────────────────────────────────
def _transliterate_to_arabic(name: str) -> str:
    mapping = {
        "mohamed": "محمد", "mohammed": "محمد", "muhammed": "محمد", "muhammad": "محمد",
        "ahmad": "أحمد", "ahmed": "أحمد",
        "ali": "علي", "fatima": "فاطمة", "fatma": "فاطمة",
        "hassan": "حسن", "hussein": "حسين", "hussain": "حسين",
        "omar": "عمر", "aisha": "عائشة", "aicha": "عائشة",
        "khadija": "خديجة", "khadidja": "خديجة",
        "ibrahim": "إبراهيم", "brahim": "إبراهيم",
        "mariam": "مريم", "maryam": "مريم", "miriam": "مريم",
        "youssef": "يوسف", "yusuf": "يوسف",
        "amina": "أمنة", "aminata": "أمنة",
        "zaynab": "زينب", "zeineb": "زينب",
        "nour": "نور", "noor": "نور",
        "sarah": "سارة", "sara": "سارة",
        "hakim": "حكيم", "karim": "كريم",
        "salim": "سليم",
        "jamal": "جمال", "djamal": "جمال",
        "samir": "سمير", "samira": "سميرة",
        "rachid": "رشيد", "rashid": "رشيد",
        "malik": "مالك", "malika": "مالكة",
        "sofia": "صفية", "sofiane": "سفيان",
        "bilal": "بلال", "ilyas": "إلياس",
        "adam": "آدم", "issa": "عيسى",
        "moussa": "موسى", "david": "داود",
        "souleymane": "سليمان", "sulayman": "سليمان",
        "yahya": "يحيى", "zakaria": "زكريا",
        "imane": "إيمان", "iman": "إيمان",
        "leila": "ليلى", "layla": "ليلى",
        "yasmine": "ياسمين", "jasmine": "ياسمين",
        "rania": "رانيا", "raniya": "رانيا",
        "zineb": "زينب", "wafa": "وفاء",
        "houda": "هدى", "huda": "هدى",
        "hamza": "حمزة", "hamid": "حميد",
        "tarek": "طارق", "tariq": "طارق",
        "yacine": "ياسين", "yassin": "ياسين",
        "zaid": "زيد", "zayd": "زيد",
        "idris": "إدريس", "khalid": "خالد",
        "khaled": "خالد", "said": "سعيد", "saad": "سعد",
        "ayoub": "أيوب", "ayyub": "أيوب",
        "abdallah": "عبدالله", "abdullah": "عبدالله",
        "abderrahmane": "عبدالرحمن", "abdulrahman": "عبدالرحمن",
        "abdelkader": "عبدالقادر", "abdulqadir": "عبدالقادر",
        "aboubakr": "أبوبكر", "abubakr": "أبوبكر",
        "othman": "عثمان", "uthman": "عثمان",
        "hasna": "حسنى", "hassna": "حسنى",
        "nadia": "نادية", "djamila": "جميلة", "jamila": "جميلة",
        "rachida": "رشيدة",
        "sultana": "سلطانة",
        "aicha": "عائشة",
        "boumediene": "بومدين",
        "nabil": "نبيل", "nabila": "نبيلة",
        "rachid": "رشيد",
        "selim": "سليم",
        "taha": "طه",
        "walid": "وليد",
        "omar": "عمر",
        "youssef": "يوسف",
        "Reda": "رضا", "reda": "رضا", "rida": "رضا",
        "Mahmoud": "محمود", "mahmoud": "محمود",
    }
    return mapping.get(name.strip().lower(), "")


# ── RAG intégré ─────────────────────────────────────────────────────────────
def _rag_search(query: str, top_k: int = 8) -> dict:
    """Recherche dans le corpus du projet (sacred numbers, découvertes phi, racines)."""
    sacred = [
        (1, "Tawhid, unicité divine"),
        (7, "Multiplicateur divin du Rizq (2:261), 7 cieux, complétion"),
        (8, "Directions du talisman, octogone, infini"),
        (13, "Ahad (أحد) = 13 = Fibonacci F₇, L'Unique inscrit dans la spirale"),
        (19, "Code 19, signature coranique (74:30), 19 lettres Basmala, Al-Wahid=19"),
        (28, "Lettres arabes = mansions lunaires = nombre parfait (1+2+4+7+14=28)"),
        (34, "Saba, prospérité, point du corridor Fibonacci"),
        (45, "Adam (אדם) en hébreu = 45, 28×φ=45.30"),
        (55, "Al-Mujib (55) = Fibonacci F₁₀, déversement de faveurs, Al-Rahman = sourate 55"),
        (56, "Al-Waqi'a, sourate de la richesse, 7×8=56"),
        (61, "Cycle rituel complet: 1+7+19+33+1"),
        (76, "Matrice des 4 noms: 19×4"),
        (89, "Al-Fajr, aube et révélation, Fibonacci F₁₁"),
        (99, "Horizon des Noms divins, complétude"),
        (114, "Nombre de sourates du Coran, Al-Jami=114, 114×φ=Al-Muqaddim"),
        (123, "Occurrences du mot Rizq dans le Coran"),
        (131, "Al-Salam, 131×φ=212=Malik al-Mulk, écart 0.018%"),
        (137, "Al-Wasi (الواسع)=137 = Kabbala (קבלה) = 1/alpha (constante de structure fine)"),
        (171, "72+99=171=9×19 — Pont des traditions"),
        (184, "Al-Muqaddim, 114×φ=184, 184×φ=Rahman (298)"),
        (256, "نور (Nur Lumière) = 256 = Do central C4 à A=432Hz. CORRESPONDANCE PARFAITE."),
        (302, "Al-Basir (Le Voyant), 302×φ=489=Fattah, écart 0.072%"),
        (319, "Abjad de يا رزاق (Ya Razzaq)"),
        (489, "Abjad de فتاح (Fattah — racine sans article), Fibonacci F₁₀ × 3 = 165…"),
        (618, "Rahman+Rahim=618=1000×(1/φ) — cœur miséricordieux, Fatiha verset 3"),
        (744, "Al-Muqtadir, Nit (hébreu 460)×φ=744, résonance inter-traditions 0.040%"),
        (786, "Basmala, porte d'ouverture, 786=102+66+329+289, Fatiha verset 1"),
    ]
    discoveries = [
        ("Basmala=786", "بسم الله الرحمن الرحيم = 102+66+329+289 = 786. EXACT."),
        ("Basmala 19 lettres", "La Basmala contient exactement 19 lettres arabes. Confirmé."),
        ("114=19×6", "Le Coran a 114 sourates = 19×6 exactement. Code 19 confirmé."),
        ("Rahman+Rahim=618=1000/phi", "329+289=618. 618×phi=999.94≈1000. Précision 0.01%."),
        ("489×phi≈791", "فتاح (Fattah)=489. 489×phi=791.22 (≈786, écart 0.66%). Approximatif."),
        ("55×phi≈89", "55×phi=88.99≈89 (Fib). Précision 0.01%. EXACT Fibonacci."),
        ("76×phi≈123", "76×phi=122.97≈123 (Rizq). Précision 0.02%."),
        ("61×phi≈99", "61×phi=98.70≈99 (Noms). Précision 0.30%."),
        ("171=9×19", "72 noms hébreux + 99 noms arabes = 171 = 9×19. Pont des traditions."),
        ("Al-Wahid=19", "واحد (sans article) = و(6)+ا(1)+ح(8)+د(4) = 19 = Code coranique."),
        ("digital_root Basmala=Fattah=3", "digital_root(786)=3, digital_root(489)=3. Résonance fondamentale."),
        ("Fattah+Razzaq->7", "489+319=808. digital_root(808)=7 (Schumann, 7 cieux)."),
        # ── Nouvelles découvertes (deep_exploration.py) ──────────────────────
        ("114×phi²=Al-Rahman", "114×φ=184(Al-Muqaddim, 0.248%), 184×φ=298(Al-Rahman, 0.095%). Les 114 sourates encodent Al-Rahman via deux φ."),
        ("28×phi=Adam45", "28 (lettres arabes/mansions lunaires/nombre parfait) × φ = 45.30 ≈ 45 = Adam (אדם) en hébreu. Écart 0.68%."),
        ("Fatiha1:1=786 Fatiha1:3=618", "Al-Fatiha verset 1 (Basmala) = 786 EXACT. Verset 3 (Al-Rahman Al-Rahim) = 618 = 1000/φ EXACT. La sourate mère encode φ."),
        ("Al-Wasi=137=Kabbala=alpha", "الواسع (Al-Wasi, L'Immense) abjad = 137. Kabbala (קבלה) hébreu = 137. 137 = 1/α constante de structure fine. Une constante physique unit les deux traditions."),
        ("Cumul99Noms->phi-e-pi", "Somme cumulative des 99 Noms: après nom#11 ≈ 1618 (φ×1000), après nom#12 ≈ 2718 (e×1000), après nom#13 ≈ 3141 (π×1000). Trois constantes universelles encodées."),
        ("Salam131×phi=MalikAlMulk212", "السلام (131) × φ = 212.0 ≈ Al-Malik al-Mulk (212). Écart 0.018% quasi-parfait. La Paix mène au Royaume par Phi."),
        ("Basir302×phi=Fattah489", "البصير (302) × φ = 488.6 ≈ الفتاح (489). Écart 0.072%. Le Voyant ouvre vers l'Ouverture par φ."),
        ("NitHebreu460×phi=Muqtadir744", "Nit (hébreu, valeur 460) × φ = 744.3 ≈ Al-Muqtadir arabe (744). Écart 0.040%. Résonance inter-traditions quasi-parfaite."),
        ("Mujib=55Fibonacci Ahad=13Fibonacci", "Al-Mujib (المجيب) = م(40)+ج(3)+ي(10)+ب(2) = 55 = Fibonacci F₁₀. Al-Ahad (أحد) = 1+8+4 = 13 = Fibonacci F₇. Deux noms divins sur la spirale."),
        ("Nur=256=DoC4=A432Hz", "نور (Lumière) = ن(50)+و(6)+ر(200) = 256. À A=432Hz, Do central C4 = 256 Hz EXACTEMENT. Correspondance parfaite 0.000%."),
        ("Jami114→Muqaddim184→Rahman298", "جامع (Al-Jami) = 114 = nombre de sourates. 114×φ = 184 (Al-Muqaddim). 184×φ = 298 (Al-Rahman). Chaîne phi parfaite."),
        ("MiroirPhi: Mutakabbir+Ghani=phi", "Pos11+Pos89: Mutakabbir(662)+Ghani(1060)=1722, ratio=1.601≈φ. Pos21+79 et 28+72: même structure. Symétrie miroir des 99 Noms encode φ."),
        # ── Ponts Astrologie ← Coran Num Tal ──────────────────────────────────
        ("Manazil-TaraBala: 28 mansions lunaires enrichies", "Chaque mansion lunaire reçoit un Nom Divin Seigneur et un score Tara Bala. Formule: ((manzil_jour-manzil_naissance) % 28) % 9 + 1. Sadhana(6)=+2.5, Sampat(2)=+2.0."),
        ("Dasha-NomsDivins: 9 Noms comme 9 planètes", "Vimshottari Dasha 120 ans: les 9 planètes remplacées par les 9 Noms Divins majeurs. Périodes proportionnelles à l'Abjad. Al-Razzaq(319), Al-Fattah(489), Al-Rahman(298), Al-Muhaymin(145), Al-Wasi(137), Nur(256), Al-Mujib(55), Al-Ahad(13), Basmala(786)."),
        ("Ashtakavarga-Sourates: Bindus coraniques", "7 Noms Divins = 7 planètes contribuant 1 bindu à 12 groupes de sourates. Sarva = Σ bindus par groupe (0-7). Transit quotidien via mansion lunaire. Score ≥5: sourate puissante du jour."),
        ("Antisces-Abjad: Miroirs numériques", "Formule antisces: (180-lon)%360 adaptée en MIROIR_ABJAD = 1000 - ABJAD. Fattah(489) miroir = 511. Razzaq(319) miroir = 681. Paires miroir = signatures complémentaires."),
        ("Geomancie-Quran: Istikhara par lettres", "Comptage pair/impair des lettres d'un verset génère 16 figures géomantiques coraniques. Écu Mères→Filles→Nièces→Témoin→Juge = processus divinatoire guidé par le Texte."),
        ("Yogas-Abjad: Motifs de destinée numérale", "Pancha Mahapurusha: nombre sacré en Kendra(1/4/7/10)=+2.5. Raja Yoga: angulaires+trinaux=+2. Dhana Yoga: 2+5+9+11=+2. Détection automatique de yogas dans le profil Abjad personnel."),
        ("Score-Vibratoire: Agrégation 11 couches", "Modèle additif transposé du sports_engine.py (16 couches A→O). Couches: Abjad+Phi+Mansion+Prière+NomDivin+Grabovoi+Sacré+Miroir+Yogas+TaraBala+Dignité. Probabilité = score_domaine / Σ scores."),
    ]
    roots = [
        ("رزق", "Rizq — subsistance", 123, 307),
        ("شكر", "Shukr — gratitude", 75, 520),
        ("فتح", "Fath — ouverture", 38, 488),
        ("رحم", "Rahma — miséricorde", 339, 248),
        ("نور", "Nur — lumière, 256=Do central A=432Hz", 43, 256),
        ("وهب", "Wahb — don", 25, 14),
        ("برك", "Baraka — bénédiction", 32, 222),
        ("علم", "Ilm — connaissance", 854, 130),
        ("حفظ", "Hifz — préservation", 44, 988),
        ("وسع", "Wasi — immensité, constante de structure fine 137", 33, 137),
        ("صلم", "Salam — paix, 131×φ=Malik al-Mulk 212", 40, 131),
        ("ملك", "Mulk — royaume, Malik al-Mulk=212", 167, 212),
        ("أحد", "Ahad — unicité, abjad=13=Fibonacci F7", 82, 13),
    ]
    ponts_astrologie = [
        ("Parts Coraniques (34 Lots Abjad)", "La formule ASC+P2-P1 des Parts Arabes devient NOM_ABJAD+NOM_DIVIN_ABJAD−RACINE_DIGITALE. Créer 34 Lots Coraniques pour domaines: rizq, shifa, ilm, hifz. Score vibratoire par domaine."),
        ("Dasha Coranique (Périodes de Vie)", "Adapter Vimshottari Dasha (120 ans) avec 9 noms divins au lieu des 9 planètes. Départ: mansion lunaire de naissance. Sous-périodes Antardasha. Chronocrators personnalisés par Abjad."),
        ("Tara Bala Coranique (Manazil)", "Enrichir les 28 mansions lunaires avec Seigneurs (noms divins). Tara Bala = ((manzil_jour − manzil_naissance) % 28) % 9 + 1. Score quotidien de faveur divine."),
        ("Géomancie Coranique (Istikhara)", "16 figures géomantiques générées par comptage pair/impair des lettres d'un verset coranique. Écu: Mères→Filles→Nièces→Témoin→Juge. Oracle par Abjad."),
        ("Shadbala Coranique (Force Noms Divins)", "6 forces adaptées: Sthana(position/99 Noms), Dig(qibla), Kala(5 prières), Naisargika(Abjad), Drik(liens phi), Chesta(variation uthmani). Score de puissance rituelle."),
        ("Ashtakavarga Coranique (Bindus/Sourates)", "7 noms divins contribuent 0-1 bindu à 12 groupes de sourates. Sarva par groupe (0-7). Transit quotidien: score du groupe correspondant à la mansion lunaire."),
        ("Yogas Numériques (Combinaisons Sacrées)", "Détection de motifs Abjad: Mahapurusha (nombre sacré en position de force +2.5), Raja (angulaires+trinaux +2), Dhana (2+5+9+11 +2). Score de destin additionnel."),
        ("Miroirs Abjad (Antisces)", "Miroir numérique: 1000−ABJAD ou TOTAL_VERSE−ABJAD. Paires de noms divins en miroir. Ajout dans l'anneau extérieur du talisman."),
        ("Shestopalov Coranique (11 Formules)", "Paires de domaines (I+IV/VII+X = Richesse). Min 3 indications harmonieuses pour activer une formule. Détection de périodes favorables par domaine."),
        ("Score Vibratoire Composite", "Agrégation additive multi-couche (Abjad+Phi+Mansion+Prière+NomDivin+Grabovoi+Sacré+Miroir+Yogas+TaraBala). Normalisation: score_domaine / Σ scores. Détection Value Grace."),
        ("Pont Phi-Astrologie 145", "TOTAL_ABJAD/145≈φ×10^5. 145=Al-Muhaymin connecte le Coran à φ. Les cycles lunaires (29.53j) et dashas (120 ans) partagent des structures mathématiques communes avec les périodes astrologiques."),
        ("Profections Annuelles Abjad", "Ascendant natal + 1 signe/an devient Année_Abjad = (abjad_natal + age × PHI) % 12. Seigneur de l'Année = nom divin du domaine actif. Oracle annuel personnalisé."),
    ]

    q_lower = query.lower()
    q_terms = q_lower.split()
    results = []

    for num, meaning in sacred:
        score = 0
        text = f"{num} {meaning.lower()}"
        for t in q_terms:
            if t in text:
                score += 3
            if t in str(num):
                score += 5
        if score > 0:
            results.append({
                "type": "nombre_sacré",
                "nombre": num,
                "sens": meaning,
                "phi": round(num * PHI, 2),
                "digital_root": digital_root(num),
                "score": score,
            })

    for title, desc in discoveries:
        score = 0
        text = (title + " " + desc).lower()
        for t in q_terms:
            if t in text:
                score += 4
        if score > 0:
            results.append({
                "type": "découverte_phi",
                "titre": title,
                "description": desc,
                "score": score,
            })

    for ar, meaning, occ, abjad_val in roots:
        score = 0
        text = f"{ar} {meaning.lower()}"
        for t in q_terms:
            if t in text:
                score += 3
        if score > 0:
            results.append({
                "type": "racine_coranique",
                "arabe": ar,
                "sens": meaning,
                "occurrences": occ,
                "abjad": abjad_val,
                "score": score,
            })

    for title, desc in ponts_astrologie:
        score = 0
        text = (title + " " + desc).lower()
        for t in q_terms:
            if t in text:
                score += 4
        if score > 0:
            results.append({
                "type": "pont_astrologie_coran_num",
                "titre": title,
                "description": desc,
                "score": score,
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return {
        "query": query,
        "count": len(results[:top_k]),
        "results": results[:top_k],
    }


class Handler(BaseHTTPRequestHandler):
    server_version = "MiftahPhiApp/2.0"

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        return

    def _send(self, status: int, body: bytes, content_type: str = "application/json; charset=utf-8") -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "http://127.0.0.1:8765")
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, payload: object, status: int = 200) -> None:
        self._send(status, json_bytes(payload))

    def _safe_path(self, base_dir: Path, relative: str) -> Path | None:
        try:
            resolved = (base_dir / relative).resolve()
            base = base_dir.resolve()
            if not str(resolved).startswith(str(base) + os.sep) and resolved != base:
                return None
            if not resolved.is_file():
                return None
            return resolved
        except (ValueError, OSError):
            return None

    def _send_file(self, path: Path, allowed_dir: Path | None = None) -> None:
        if allowed_dir is not None:
            resolved = path.resolve()
            base = allowed_dir.resolve()
            if not str(resolved).startswith(str(base) + os.sep) and resolved != base:
                self._send_json({"error": "Forbidden"}, status=403)
                return
        if not path.exists() or not path.is_file():
            self._send_json({"error": "File not found"}, status=404)
            return
        mime, _ = mimetypes.guess_type(str(path))
        self._send(200, path.read_bytes(), mime or "application/octet-stream")

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        return json.loads(raw.decode("utf-8"))

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        # ── Fichiers statiques ───────────────────────────────────────────
        if path in ("/", "/index.html"):
            return self._send_file(STATIC_DIR / "index.html", allowed_dir=STATIC_DIR)
        if path in ("/landing", "/landing.html"):
            return self._send_file(STATIC_DIR / "landing.html", allowed_dir=STATIC_DIR)
        if path in {"/app.js", "/styles.css"}:
            return self._send_file(STATIC_DIR / path.lstrip("/"), allowed_dir=STATIC_DIR)
        if path.startswith("/generated/"):
            safe = self._safe_path(GENERATED_DIR, path.removeprefix("/generated/"))
            if not safe:
                return self._send_json({"error": "Forbidden"}, status=403)
            return self._send_file(safe, allowed_dir=GENERATED_DIR)

        # ── API Domaines et corpus ───────────────────────────────────────
        if path == "/api/domains":
            return self._send_json({
                "quran_domains": {k: v.__dict__ for k, v in build_domain_profiles().items()},
                "generic_domains": GENERIC_DOMAINS,
                "schemes": {k: {"label": v["label"]} for k, v in SCRIPT_CONFIGS.items()},
            })
        if path == "/api/quran/suras":
            payload = [
                {
                    "index": idx,
                    "name_ar": meta.name,
                    "name_en": meta.ename,
                    "tname": meta.tname,
                    "ayas": meta.ayas,
                    "place": meta.place,
                }
                for idx, meta in QURAN.suras.items()
            ]
            return self._send_json(payload)
        if path == "/api/corpora":
            return self._send_json(list_corpora())
        if path == "/api/corpus/refs":
            corpus_id = qs.get("corpus_id", [""])[0]
            corpus = load_corpus(corpus_id)
            return self._send_json([entry["ref"] for entry in corpus.entries])
        if path == "/api/library":
            if LIB_INDEX.exists():
                return self._send_file(LIB_INDEX)
            return self._send_json({"error": "Library not built yet"}, status=404)

        # ── API Audio ────────────────────────────────────────────────────
        if path == "/api/audio":
            index_file = AUDIO_DIR / "index.json"
            if not AUDIO_DIR.exists():
                return self._send_json({"files": [], "error": "Audio directory not found"})
            files = []
            for f in sorted(AUDIO_DIR.glob("*.wav")):
                size_kb = round(f.stat().st_size / 1024)
                # Extract frequency/label from filename
                stem = f.stem  # e.g. "rizq_56hz"
                files.append({
                    "filename": f.name,
                    "label": stem.replace("_", " ").title(),
                    "size_kb": size_kb,
                    "url": f"/audio/{f.name}",
                })
            meta = {}
            if index_file.exists():
                meta = json.loads(index_file.read_text(encoding="utf-8"))
            return self._send_json({"files": files, "meta": meta})

        if path.startswith("/audio/"):
            filename = path.removeprefix("/audio/")
            safe = self._safe_path(AUDIO_DIR, filename)
            if not safe:
                return self._send_json({"error": "Audio not found"}, status=404)
            return self._send_file(safe, allowed_dir=AUDIO_DIR)

        # ── API PDFs ─────────────────────────────────────────────────────
        if path == "/api/pdfs":
            if not PDF_DIR.exists():
                return self._send_json({"files": []})
            files = []
            for f in sorted(PDF_DIR.rglob("*.pdf")):
                rel = f.relative_to(PDF_DIR).as_posix()
                size_kb = round(f.stat().st_size / 1024)
                # Build a clean label from the filename
                label = f.stem.replace("_", " ").replace("-", " ")
                files.append({
                    "filename": f.name,
                    "label": label,
                    "path": rel,
                    "size_kb": size_kb,
                    "url": f"/pdf/{rel}",
                })
            return self._send_json({"files": files, "count": len(files)})

        if path.startswith("/pdf/"):
            rel_path = path.removeprefix("/pdf/")
            safe = self._safe_path(PDF_DIR, rel_path)
            if not safe:
                return self._send_json({"error": "PDF not found"}, status=404)
            return self._send_file(safe, allowed_dir=PDF_DIR)

        # ── API Lune ─────────────────────────────────────────────────────
        if path == "/api/moon":
            date_str = qs.get("date", [""])[0]
            try:
                d = datetime.date.fromisoformat(date_str) if date_str else datetime.date.today()
            except ValueError:
                d = datetime.date.today()
            mansion = lunar_mansion(d)
            phase = moon_phase_name(d)
            delta = (d - _KNOWN_NEW_MOON).days
            cycle_day = delta % SYNODIC_MONTH
            return self._send_json({
                "date": str(d),
                "mansion": mansion,
                "mansion_of_28": f"{mansion}/28",
                "phase": phase,
                "cycle_day": round(cycle_day, 2),
                "synodic_month": SYNODIC_MONTH,
            })

        # ── API Oracle ──────────────────────────────────────────────────
        if path == "/api/oracle/daily":
            date_str = qs.get("date", [""])[0]
            try:
                d = datetime.date.fromisoformat(date_str) if date_str else datetime.date.today()
            except ValueError:
                d = datetime.date.today()
            oracle = compute_daily_oracle(d)
            return self._send_json(oracle.__dict__)

        if path == "/api/oracle/discovery":
            return self._send_json({
                "nombre_secret": NOMBRE_SECRET,
                "nom_secret": NOM_SECRET_NOM,
                "abjad_total_coran": TOTAL_ABJAD,
                "provenance": {
                    "source": TOTAL_ABJAD_SOURCE,
                    "versets": TOTAL_ABJAD_VERSES,
                    "lettres": TOTAL_ABJAD_LETTERS,
                    "digital_root": TOTAL_ABJAD_DR,
                    "reproductible": "python scripts/compute_total_abjad.py",
                },
                "formule_principale": f"ABJAD_TOTAL / {NOMBRE_SECRET} ≈ φ × 100 000",
                "verification": {
                    "total_div_145": TOTAL_ABJAD / NOMBRE_SECRET,
                    "phi_fois_100k": ORACLE_PHI * 1e5,
                    "ecart_pct": round(abs(TOTAL_ABJAD / NOMBRE_SECRET - ORACLE_PHI * 1e5) / (ORACLE_PHI * 1e5) * 100, 4),
                    "statut": "résonance approximative — opérandes sourcées (total réel + 145=مهيمن), non une identité",
                },
                "resonances": {
                    "phi": {
                        "via": NOMBRE_SECRET,
                        "via_sens": "145 = مهيمن (Al-Muhaymin, sans article)",
                        "ecart": 0.0623,
                        "fiabilite": "sourcée — diviseur principiel (99 Noms)",
                    },
                    "pi": {
                        "via": 747,
                        "ecart": 0.0359,
                        "fiabilite": "coïncidence numérique — diviseur 747 NON principiel",
                    },
                    "e": {
                        "via": 863,
                        "ecart": 0.0740,
                        "fiabilite": "coïncidence numérique — diviseur 863 NON principiel",
                    },
                },
                "code_19_rizq": {
                    "somme_sourates": SOMME_SOURATES,
                    "facteur_19": CODE_19_FACTEUR,
                    "waqia_abjad": WAQIA_ABJAD,
                    "ratio": round(CODE_19_FACTEUR / WAQIA_ABJAD, 4),
                    "statut": "EXACT : Σ(1..114)=6555=19×345 ; 345/213≈φ (écart 0.10%)",
                },
                "pont_traditions": "72 noms hébreux + 99 noms arabes = 171 = 19 × 9 (exact)",
                "basmala": BASMALA_ABJAD,
            })

        if path in ("/oracle", "/oracle.html"):
            return self._send_file(STATIC_DIR / "oracle.html", allowed_dir=STATIC_DIR)

        self._send_json({"error": "Not found"}, status=404)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        try:
            payload = self._read_json()

            if path == "/api/analyze/quran":
                sura = int(payload["sura"])
                ayah = payload.get("ayah")
                end = payload.get("end")
                result = analyze_reference(
                    QURAN,
                    sura=sura,
                    ayah=int(ayah) if ayah not in (None, "", 0) else None,
                    end=int(end) if end not in (None, "", 0) else None,
                    domain_key=payload.get("domain", "richesse"),
                )
                return self._send_json(result)

            if path == "/api/analyze/text":
                result = analyze_generic_text(
                    text=payload["text"],
                    scheme=payload["scheme"],
                    domain=payload.get("domain", "richesse"),
                    source_ref=payload.get("ref_label", "custom-text"),
                    corpus_name=payload.get("corpus_name", "custom"),
                )
                return self._send_json(result)

            if path == "/api/import/corpus":
                name = payload.get("name", "").strip()
                if not name or len(name) > 200:
                    return self._send_json({"error": "Invalid corpus name"}, status=400)
                raw_entries = payload.get("raw_entries", "")
                if len(raw_entries) > 5_000_000:
                    return self._send_json({"error": "Entries too large (max 5 MB)"}, status=400)
                corpus = save_corpus(
                    name=name,
                    scheme=payload["scheme"],
                    raw_entries=raw_entries,
                    description=payload.get("description", ""),
                )
                return self._send_json(corpus.__dict__)

            if path == "/api/analyze/corpus":
                result = analyze_corpus_entry(
                    corpus_id=payload["corpus_id"],
                    ref=payload["ref"],
                    domain=payload.get("domain", "richesse"),
                )
                return self._send_json(result)

            if path == "/api/render/talisman":
                result = payload["result"]
                title = payload.get("title")
                out = render_talisman(result, title=title)
                rel = out.relative_to(GENERATED_DIR).as_posix()
                return self._send_json({"path": f"/generated/{rel}"})

            if path == "/api/talisman/vivant":
                name = payload.get("name", "")
                domain = payload.get("domain", "richesse")
                date_str = payload.get("date", "")

                name_arabic = _transliterate_to_arabic(name)
                if name_arabic:
                    name_abjad = abjad_sum(name_arabic)
                else:
                    # Fallback Latin gematria (a=1…z=26) — approximation only
                    name_abjad = sum(ord(c.lower()) - 96 for c in name if c.isalpha())
                name_root = digital_root(name_abjad) if name_abjad > 0 else 1

                try:
                    d = datetime.date.fromisoformat(date_str) if date_str else datetime.date.today()
                    mansion = lunar_mansion(d)      # ← formule corrigée
                    phase = moon_phase_name(d)
                except Exception:
                    d = datetime.date.today()
                    mansion = 1
                    phase = "Inconnue"

                suras_by_domain = {
                    "richesse": 56, "sante": 17, "savoir": 20,
                    "protection": 113, "occultes": 18,
                }
                sura = suras_by_domain.get(domain, 56)
                result = analyze_reference(QURAN, sura=sura, domain_key=domain)
                result["talisman"]["center"] = name_root
                result["talisman"]["inner_ring"][0] = name_abjad
                result["talisman"]["inner_ring"][1] = mansion
                result["signature"]["center"] = name_root
                result["signature"]["ring_inner"][0] = name_abjad
                result["signature"]["ring_inner"][1] = mansion
                result["source"] = f"{name} (Mansion {mansion})"
                result["vivant"] = {
                    "name": name,
                    "name_arabic": name_arabic or "(translittération latine)",
                    "name_abjad": name_abjad,
                    "name_root": name_root,
                    "lunar_mansion": mansion,
                    "lunar_phase": phase,
                    "date": str(d),
                    "sura": sura,
                    "domain": domain,
                }
                return self._send_json(result)

            # ── RAG Search ────────────────────────────────────────────
            if path == "/api/rag":
                query = payload.get("query", "").strip()
                if not query:
                    return self._send_json({"error": "query manquante"}, status=400)
                result = _rag_search(query)
                return self._send_json(result)

            # ── Oracle Predictif ───────────────────────────────────────
            if path == "/api/oracle/predict":
                name = payload.get("name", "").strip()
                if not name:
                    return self._send_json({"error": "Nom requis"}, status=400)
                birth_date = payload.get("birth_date", "")
                domain = payload.get("domain", "richesse")
                target_date = payload.get("date", "")
                result = predict(name, birth_date or None, domain, target_date or None)
                return self._send_json({
                    "signature": result.signature.__dict__,
                    "oracle": result.oracle.__dict__,
                    "phi_formula_verification": result.phi_formula_verification,
                    "inter_tradition_bridges": result.inter_tradition_bridges,
                    "recommended_action": result.recommended_action,
                    "codes_to_use": result.codes_to_use,
                })

        except Exception as exc:  # noqa: BLE001
            return self._send_json({"error": str(exc)}, status=500)

        self._send_json({"error": "Not found"}, status=404)


def run(host: str = "127.0.0.1", port: int = 8765) -> None:
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Miftah Phi App v3.0 — http://{host}:{port}")
    print(f"  Oracle : http://{host}:{port}/oracle")
    print(f"  Audio  : {AUDIO_DIR}")
    print(f"  PDFs   : {PDF_DIR}")
    server.serve_forever()


if __name__ == "__main__":
    run()
