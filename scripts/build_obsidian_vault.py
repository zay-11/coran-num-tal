#!/usr/bin/env python3
"""
Build Obsidian vault from CORAN NUM TAL knowledge base.
Creates interlinked markdown files for Obsidian.
"""

from __future__ import annotations
import json, math, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
VAULT = ROOT / "obsidian_vault"
PHI = (1 + math.sqrt(5)) / 2


def md(text: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build():
    VAULT.mkdir(parents=True, exist_ok=True)
    links = []

    # --- HOME ---
    md(f"""# CORAN NUM TAL — Vault

Bienvenue dans le coffre de connaissance du projet CORAN NUM TAL.

## Concepts fondamentaux
- [[Triple Signature 7-8-19]]
- [[Architecture Universelle]]
- [[Code 19]]
- [[Nombres Sacres]]
- [[Nombres d'Or Phi]]
- [[Systeme Abjad]]

## Systemes
- [[Rituel Miftah 19]]
- [[Talisman]]
- [[Radionique]]
- [[Codes Grabovoi]]

## Ponts inter-traditionnels
- [[Pont des 72+99]]
- [[Sceau de Salomon]]
- [[Guematria Hebraique]]

## Ressources
- [[Dictionnaire des Racines]]
- [[Decouvertes Phi]]
- [[Corpus Coranique]]
- [[Idees Nouvelles]]
""", VAULT / "Home.md")

    # --- TRIPLE SIGNATURE ---
    md(f"""# Triple Signature 7·8·19

Les trois nombres fondamentaux du projet CORAN NUM TAL.

## 7 — Multiplicateur Divin
- Source: Coran 2:261 (1 grain -> 7 epis)
- 7 cieux, 7 terres, 7 versets de la Fatiha
- 7 niveaux de purification dans l'istighfar
- 7 tours dans la spirale secondaire de la radionique
- Reduction du Sceau: 1064 -> 1+0+6+4 = 11 -> 2

## 8 — Directions du Talisman
- 8 directions cardinales et intercardinales
- Etoile a 8 branches (2 carres superposes a 45°)
- 8 phases lunaires du Cadran Lunaire
- Sceau de Salomon en arabe: 1232 -> 1+2+3+2 = 8
- 8 aimants neodyme dans la radionique amplifiee

## 19 — Signature Divine
- Source: Coran 74:30 ("Ils sont dix-neuf a y veiller")
- 19 lettres dans la Basmala
- 114 sourates = 19 x 6
- Sceau de Salomon en hebreu: 829 -> 8+2+9 = 19
- 19 tours dans la spirale primaire de la radionique

## Formule condensee
520 741 8 = 7 + 19 + 8

## Voir aussi
- [[Code 19]]
- [[Nombres Sacres]]
""", VAULT / "Concepts/Triple Signature 7-8-19.md")

    # --- ARCHITECTURE UNIVERSELLE ---
    md(f"""# Architecture Universelle

La chaine en 5 maillons qui structure TOUS les documents du projet.

## La Chaine
1. **SOURCE** (51:58) — Ar-Razzaq comme source pure du rizq
2. **CORRIDOR** (34->55->56->89) — Suite Fibonacci de l'abondance
3. **PORTAIL** (618) — Rahman(329) + Rahim(289) = miroir de 1/phi
4. **CENTRE** (56) — Al-Waqi'a, sourate de la Richesse
5. **CYCLE** (61->99) — 1+7+19+33+1 = 61, projection phi vers 99

## Preuve par les 5 decouvertes phi
1. 19 x 4 x {PHI:.1f} -> 123 (rizq)
2. 55 x {PHI:.1f} -> 89 (Fajr)
3. 489 x {PHI:.1f} -> 786 (Basmala)
4. 618 x {PHI:.1f} -> 1000+
5. 61 x {PHI:.1f} -> 99 (Noms)

## Voir aussi
- [[Nombres d'Or Phi]]
- [[Rituel Miftah 19]]
- [[Decouvertes Phi]]
""", VAULT / "Concepts/Architecture Universelle.md")

    # --- CODE 19 ---
    md(f"""# Code 19

Le Code 19 est la pierre angulaire de l'architecture mathematique du Coran selon Rashad Khalifa (1974).

## Preuves
- 114 sourates = 19 x 6
- Basmala = 19 lettres
- 74:30 mentionne explicitement 19
- 72 noms hebreux + 99 noms arabes = 171 = 19 x 9
- Sourate 56 + 96 = 152 = 19 x 8

## Dans le projet
- Rituel: 19 invocations des noms divins
- Radionique: 19 tours dans la spirale primaire
- Talisman: 19 au centre du Buduh
- Phi: 19 x 4 x phi -> 123

## Voir aussi
- [[Triple Signature 7-8-19]]
- [[Nombres Sacres]]
""", VAULT / "Concepts/Code 19.md")

    # --- NOMBRES SACRES ---
    sacred = [
        (1, "Tawhid, Unicite divine"),
        (7, "Multiplicateur divin (2:261)"),
        (8, "Directions du talisman"),
        (19, "Signature coranique (74:30)"),
        (34, "Saba, point de depart Fibonacci"),
        (55, "Al-Rahman, deversement de faveurs"),
        (56, "Al-Waqi'a, sourate de la richesse"),
        (61, "Cycle rituel complet"),
        (76, "Matrice des 4 noms"),
        (89, "Al-Fajr, aube et revelation"),
        (99, "Horizon des Noms divins"),
        (123, "Occurrences du mot Rizq"),
        (319, "Abjad de Ya Razzaq"),
        (489, "Abjad de Fattah"),
        (618, "Rahman+Rahim, coeur misericordieux"),
        (786, "Basmala, porte d'ouverture"),
    ]
    sac_lines = [f"| {n} | {m} | {round(n * PHI, 1)} |" for n, m in sacred]
    sac_table = "\n".join(sac_lines)
    md(f"""# Nombres Sacres

| Nombre | Signification | Projection phi |
|--------|--------------|---------------|
{sac_table}

## Voir aussi
- [[Triple Signature 7-8-19]]
- [[Nombres d'Or Phi]]
- [[Code 19]]
""", VAULT / "Concepts/Nombres Sacres.md")

    # --- PHI ---
    md(f"""# Nombres d'Or Phi

φ = {PHI}
1/φ = {1/PHI}

## Les 5 decouvertes phi du projet
1. 19 x 4 x φ = {19*4*PHI:.1f} -> 123
2. 55 x φ = {55*PHI:.1f} -> 89
3. 489 x φ = {489*PHI:.1f} -> 786
4. 618 x φ = {618*PHI:.1f} -> 1000
5. 61 x φ = {61*PHI:.1f} -> 99

## Voir aussi
- [[Decouvertes Phi]]
- [[Architecture Universelle]]
""", VAULT / "Concepts/Nombres d'Or Phi.md")

    # --- SYSTEME ABJAD ---
    abjad_table = []
    for letter, val in [("ا",1),("ب",2),("ج",3),("د",4),("ه",5),("و",6),("ز",7),("ح",8),("ط",9),
                         ("ي",10),("ك",20),("ل",30),("م",40),("ن",50),("س",60),("ع",70),
                         ("ف",80),("ص",90),("ق",100),("ر",200),("ش",300),("ت",400),("ث",500),
                         ("خ",600),("ذ",700),("ض",800),("ظ",900),("غ",1000)]:
        abjad_table.append(f"| {letter} | {val} |")

    md(f"""# Systeme Abjad

L'Abjad est le systeme numerique arabe ou chaque lettre a une valeur.

| Lettre | Valeur |
|--------|--------|
{chr(10).join(abjad_table)}

## Noms divins du Rizq
- Ya Razzaq (يا رزاق) = 319
- Ya Fattah (يا فتاح) = 489
- Ya Ghani (يا غني) = 1060
- Ya Mughni (يا مغني) = 1100
- Somme = 2968 -> 2+9+6+8 = 25 -> 7

## Voir aussi
- [[Dictionnaire des Racines]]
- [[Nombres Sacres]]
""", VAULT / "Concepts/Systeme Abjad.md")

    # --- RITUEL ---
    md(f"""# Rituel Miftah 19

## Architecture
1. **Ouverture** (1x) — Basmala (19 lettres, Abjad 786)
2. **Istighfar** (7x) — Purification, multiplicateur (2:261)
3. **Noms Divins** (19x) — Ya Razzaq, Ya Fattah, Ya Ghani, Ya Mughni
4. **Salawat** (33x) — Benediction sur le Prophete
5. **Sceau** (1x) — Tawakkul (Hasbunallah)

**Total: 1 + 7 + 19 + 33 + 1 = 61**
Reduction: 6+1 = 7 (completion)

## Version Express (60 secondes)
1 + 3 + 7 + 3 + 1 = 15 = 19 - 4

## Voir aussi
- [[Architecture Universelle]]
- [[Talisman]]
- [[Nombres Sacres]]
""", VAULT / "Pratiques/Rituel Miftah 19.md")

    # --- TALISMAN ---
    md(f"""# Talisman

## Structure
- **Centre**: 618 (Rahman+Rahim) ou 19 (Code) ou 56 (Waqi'a)
- **Anneau interne**: 8 valeurs (mots, lettres, abjad reduit, mod 19, mod 7, mod 8, fib word, fib letter)
- **Anneau externe**: 8 valeurs (golden words, golden letters, golden abjad, fib word, fib letter, fib abjad, anchor[0], anchor[-1])
- **Geometrie**: Etoile a 8 branches (2 carres superposes a 45°)

## Talisman Ultime
Synthese de 3 traditions:
- Abjad arabe (4 noms divins du Rizq)
- Guematria hebraique (Osher, Shefa, Berakhah, Mamon, Parnassah)
- Codes Grabovoi (520 741 8, 318 798, 56 96 152...)

## Talisman Vivant
Personnalisation par:
- Nom -> Abjad -> Centre du talisman
- Date -> Mansion lunaire
- Domaine -> Sourate de reference

## Voir aussi
- [[Rituel Miftah 19]]
- [[Radionique]]
- [[Sceau de Salomon]]
""", VAULT / "Pratiques/Talisman.md")

    # --- RADIONIQUE ---
    md(f"""# Radionique

## Principe
Montage physique ou les codes numeriques sont imprimes dans la matiere via:
- **Cuivre**: antenne spiralee (7 ou 19 tours)
- **Quartz**: amplificateur piezoelectrique
- **Photo**: temoin biophotonique (witness)
- **Aimants**: champ magnetique toroidal
- **Geometrie sacree**: carre Buduh 3x3, etoile 8 branches

## Systeme Amplifie (7 couches)
1. Base — Geometrie sacree (Buduh)
2. Codes numeriques (papier)
3. 8 aimants neodyme N52
4. Photo (witness)
5. Spirale cuivre primaire (19 tours)
6. Spirale cuivre secondaire (7 tours)
7. Quartz central + 7 quartz peripheriques

## Frequences
- Resonance systeme: ~19 kHz
- Harmonie Schumann: 7.83 Hz
- Ondes Alpha: 8-12 Hz

## Voir aussi
- [[Talisman]]
- [[Codes Grabovoi]]
- [[Gamme Doree]]
""", VAULT / "Pratiques/Radionique.md")

    # --- CODES GRABOVOI ---
    md(f"""# Codes Grabovoi

## Codes principaux du projet
- **520 741 8**: Argent inattendu (7+19+8)
- **318 798**: Abondance generale
- **318 612 518 714**: Cash-flow continu
- **9798733714615**: Manifestation rapide
- **56 96 152**: Code Al-Waqi'a (7x8 + 19x8)
- **123 55 89**: Corridor phi du rizq
- **786 489 618**: Porte d'ouverture misericordieuse
- **6119 078**: Cycle operatif complet (61+19+7+8)
- **319 489 618 786**: Echelle integrale du flux
- **307 123 786**: Racine -> manifestation -> porte

## Usage
- Lecture lente, chiffre par chiffre
- Ecrire sur papier sous la photo en radionique
- Reciter 7x, 19x ou 33x selon protocole
- Placer sous un verre d'eau, sous l'oreiller, dans le portefeuille

## Voir aussi
- [[Radionique]]
- [[Architecture Universelle]]
""", VAULT / "Pratiques/Codes Grabovoi.md")

    # --- PONT 72+99 ---
    md(f"""# Pont des 72+99

## Equation fondatrice
72 noms hebreux (Shem HaMephorash) + 99 noms arabes (Asma ul-Husna) = 171 = 19 x 9

## Le Sceau de Salomon
- Hebreu: Hotam Shlomo = 829 -> 8+2+9 = 19
- Arabe: Khatam Sulayman = 1232 -> 1+2+3+2 = 8
- Le Sceau donne 19 (Code) en hebreu et 8 (Directions) en arabe

## Resonances phi
447 paires de noms en resonance phi (distance < 5%) sur 7128 combinaisons possibles.

## Voir aussi
- [[Guematria Hebraique]]
- [[Triple Signature 7-8-19]]
- [[Sceau de Salomon]]
""", VAULT / "Ponts/Pont des 72+99.md")

    # --- GUEMATRIA HEBRAIQUE ---
    md(f"""# Guematria Hebraique

## Valeurs principales
- YHWH (יהוה) = 26
- Mamon (Fortune) = 136 = 4 x 34 (carre Jupiter)
- Shefa (Abondance) = 450
- Berakhah (Benediction) = 227
- Osher (Richesse) = 570
- Parnassah (Subsistance) = 395
- Hotam Shlomo (Sceau de Salomon) = 829

## Correspondances planetaires
- Saturne (3x3): 15 -> 6 (Binah)
- Jupiter (4x4): 34 -> 7 (Chesed) — RIZQ
- Soleil (6x6): 111 -> 3 (Tiphareth)
- Venus (7x7): 175 -> 4 (Netzach)

## Voir aussi
- [[Pont des 72+99]]
- [[Sceau de Salomon]]
""", VAULT / "Ponts/Guematria Hebraique.md")

    # --- SCEAU DE SALOMON ---
    md(f"""# Sceau de Salomon

## Point de convergence
Le Sceau de Salomon (Khatam Sulayman / Hotam Shlomo) est le point de convergence
mathematique entre la tradition juive et islamique.

## Valeurs numeriques
- Hebreu (חותם שלמה) = 829 -> Reduction: 8+2+9 = 19
- Arabe (خاتم سليمان) = 1232 -> Reduction: 1+2+3+2 = 8

## Symbolisme
- Etoile a 6 branches (hexagramme) = union du masculin et feminin
- Etoile a 8 branches (octogramme) = 8 directions du Rizq
- Anneau de Salomon = pouvoir sur les vents, animaux, jinns
- Inscription: "La ilaha illa Allah, Al-Malik, Al-Haqq, Al-Mubin" = 558

## Voir aussi
- [[Pont des 72+99]]
- [[Talisman]]
- [[Guematria Hebraique]]
""", VAULT / "Ponts/Sceau de Salomon.md")

    # --- DICTIONNAIRE ---
    roots = [
        ("رزق","RZQ","Subsistance, provision",123,307),
        ("شكر","ShKR","Gratitude",75,520),
        ("برك","BRK","Baraka, benediction",32,222),
        ("خير","KhYR","Bien, bonte",190,810),
        ("فضل","FDL","Grace, faveur",88,800),
        ("كثر","KThR","Abondance",167,620),
        ("فتح","FTH","Ouverture",38,488),
        ("غنى","GhNY","Richesse",73,1060),
        ("وهب","WHB","Don",25,14),
        ("كرم","KRM","Generosite",47,260),
        ("بسط","BST","Extension",25,71),
        ("كفى","KFY","Suffisance",33,100),
        ("نور","NWR","Lumiere",43,256),
        ("حفظ","HFZ","Garde",44,988),
        ("سلم","SLM","Paix",140,130),
    ]
    root_lines = [f"| {a} | {t} | {m} | {o} | {abj} | {round(abj*PHI,1)} |" for a,t,m,o,abj in roots]
    root_table = "\n".join(root_lines)
    md(f"""# Dictionnaire des Racines

| Arabe | Translit | Sens | Occ | Abjad | Phi |
|--------|---------|------|-----|-------|-----|
{root_table}

## Voir aussi
- [[Systeme Abjad]]
- [[Nombres Sacres]]
""", VAULT / "Ressources/Dictionnaire des Racines.md")

    # --- DECOUVERTES PHI ---
    md(f"""# Decouvertes Phi

## Les 5 decouvertes
1. **19 x 4 x φ = {19*4*PHI:.1f} -> 123** (occurrences de rizq)
2. **55 x φ = {55*PHI:.1f} -> 89** (Rahman vers Fajr)
3. **489 x φ = {489*PHI:.1f} -> 786** (Fattah vers Basmala)
4. **618 x φ = {618*PHI:.1f} -> 1000** (mercy-code vers plenitude)
5. **61 x φ = {61*PHI:.1f} -> 99** (cycle vers horizon des Noms)

## Voir aussi
- [[Nombres d'Or Phi]]
- [[Architecture Universelle]]
""", VAULT / "Ressources/Decouvertes Phi.md")

    # --- IDEES NOUVELLES ---
    md(f"""# Idees Nouvelles

## 1. [[Pont des 72+99]]
Document explorant la convergence mathematique entre les 72 noms hebreux et 99 noms arabes.

## 2. Calendrier Lunaire Phi
Fusion du Cadran Lunaire (28 mansions) avec le systeme phi.
Recalcule chaque mansion avec phi: 1xphi, 2xphi... 28xphi.

## 3. Gamme Doree
Conversion des rapports phi en frequences audio.
13 fichiers audio generes (75.7 MB).

## 4. Les 40 Portes
Journal guide de 40 jours integrant mansion lunaire, phi, dhikr et journaling.

## 5. Talisman Vivant
Personnalisation dynamique du talisman via nom (abjad), date (mansion lunaire), domaine.

## 6. Dictionnaire des Resonances
Reference exhaustive de 50 racines coraniques liees au rizq avec abjad, phi, Fibonacci.

## Voir aussi
- [[Architecture Universelle]]
- [[Corpus Coranique]]
""", VAULT / "Ressources/Idees Nouvelles.md")

    # --- CORPUS ---
    surah_count = 114
    md(f"""# Corpus Coranique

## Structure
- {surah_count} sourates
- 5 domaines: Richesse, Sante, Savoir, Protection, Occultes
- 570 analyses JSON ({surah_count} sourates x 5 domaines)
- 114 talismans PNG

## Textes sources
- Uthmani (original arabe)
- Simple clean (arabe simplifie)
- Metadata XML (Tanzil.net)

## Corpus importes
- Torah (hebreu, guematria)
- Evangeliques grecs (isopsephie)
- Nouveaux corpus via l'API d'import

## Voir aussi
- [[Systeme Abjad]]
- [[Guematria Hebraique]]
""", VAULT / "Ressources/Corpus Coranique.md")

    # --- GAMME DOREE ---
    md(f"""# Gamme Doree

## Frequences audio generees
- Schumann 7.83 Hz (harmoniques)
- Rizq 56 Hz (Al-Waqi'a)
- Waqi'a 152 Hz
- Basmala 786 Hz
- Mercy 618 Hz
- Code 19 Hz
- Fattah 489 Hz
- Razzaq 319 Hz

## Pistes
- Frequences sacrees pures (8 pistes)
- Accord phi complet (90s)
- Sequence Fibonacci
- Gamme doree 19 notes
- Bourdon meditation Waqi'a (3 min)
- Sequence activation Rizq 7-19-8

## Voir aussi
- [[Radionique]]
- [[Nombres d'Or Phi]]
""", VAULT / "Pratiques/Gamme Doree.md")

    print(f"Obsidian vault created: {VAULT}")
    print(f"Files: {len(list(VAULT.rglob('*.md')))} markdown files")
    return VAULT


if __name__ == "__main__":
    build()
