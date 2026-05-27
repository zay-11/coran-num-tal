# MIFTAH AL-GHAIB (مفتاح الغيب) — Moteur de Prédiction Unifié

## Architecture Complète — v1.0

---

## I. VISION

Un moteur unique capable de prédire dans **3 domaines** en interconnectant **2 traditions ésotériques complètes** :

```
┌─────────────────────────────────────────────┐
│         MIFTAH AL-GHAIB (مفتاح الغيب)        │
│         Le Moteur de Prédiction Unifié        │
├───────────────┬──────────────┬──────────────┤
│   🏇 SPORT    │  📈 FINANCE  │  👤 PERSONNEL │
│   Courses     │  Marchés     │  Vie / Destin │
│   Matchs      │  Crypto      │  Domaines x5  │
├───────────────┴──────────────┴──────────────┤
│          2 TRADITIONS INTERCONNECTÉES        │
├──────────────────────┬──────────────────────┤
│  🔭 RAG ASTRO        │  📿 CORAN NUM TAL    │
│  Astrologie Tropicale│  Abjad / Phi / 19    │
│  Védique / Jyotish   │  99 Noms Divins      │
│  Horary / Shestopalov│  Nombres Sacrés       │
│  Géomancie / Tajika  │  Géométrie Sacrée    │
│  47 techniques       │  Manazil / Grabovoi  │
├──────────────────────┴──────────────────────┤
│         9 COUCHES UNIVERSELLES PARTAGÉES     │
└─────────────────────────────────────────────┘
```

---

## II. FONDATION MATHÉMATIQUE

### La Preuve du Pont

```
TOTAL_ABJAD(Coran) / NOMBRE_SECRET(Al-Muhaymin) = φ × 10⁵
23,476,120 / 145 = 161,904.28 ≈ φ × 100,000 (161,803.40)
Écart : 0.0623%
```

Ce n'est pas un hasard. C'est le fondement qui autorise l'interconnexion des deux systèmes :
- Le Coran encode φ (Nombre d'Or)
- L'astrologie repose sur les cycles (temples du temps)
- φ est le pont mathématique entre le Texte sacré et le Cosmos

### La Méthode d'Agrégation Additive

Validée par le `sports_engine.py` existant (16 couches A→O) :
```
SCORE_TOTAL = Σ(couche_i × pondération_i)
PROBABILITÉ = score / Σ(scores)
```

Cette méthode est :
- **Déterministe** (SHA-256 + dates)
- **Additive** (chaque couche indépendante renforce ou affaiblit)
- **Normalisable** (conversion score → probabilité)
- **Cross-domain** (même logique pour sport, finance, personnel)

---

## III. LES 9 COUCHES UNIVERSELLES

Chaque couche produit un **delta** (±) pour le domaine cible. Toutes les couches sont disponibles pour tous les domaines — le paramétrage détermine lesquelles sont actives et leur poids.

### Couche 1 — HORLOGE COSMIQUE (Coranic + Astro)

| Sous-couche | Source | Calcul |
|-------------|--------|--------|
| Manazil Al-Qamar (28) | Coran Num Tal | `(jours_depuis_2024-01-11 % 29.53059) / (29.53059/28) % 28 + 1` |
| Nakshatras (27) | RAG ASTRO | `int(lon_lune / 13.3333) % 27`, seigneur + Tara Bala |
| Heures Planétaires | RAG ASTRO | Ordre Chaldéen, calcul jour/nuit par déclinaison solaire |
| Phase Lunaire | RAG ASTRO | `phase_angle = (lune - soleil) % 360`, 8 phases |
| Jour de la Semaine | Coran Num Tal | Planète régente + métal + pierre + parfum |
| Heure de Prière | Coran Num Tal | `digital_root(mansion × 145) % 7` → Fajr/Isha/etc |
| Éclipses | RAG ASTRO | `abs(NM_lon - Rahu_lon) ≤ 18.42°` (solaire), `≤ 11.63°` (lunaire) |

**Poids** : 1.0 (normalisé)

---

### Couche 2 — SIGNATURE NUMÉROLOGIQUE (Coranic)

| Sous-couche | Calcul |
|-------------|--------|
| Abjad du Nom | Σ valeurs des lettres arabes du nom de l'entité (cheval, action, personne) |
| Racine Digitale | `digital_root(abjad)` itératif jusqu'à 1 chiffre |
| Pont Secret | `round(145 × (abjad % 100 + 1) × INV_PHI)` |
| Alignement Phi | `0.3×dr_match + 0.35×mansion_power + 0.35×name_145_resonance` (0-100) |
| Fibonaccisation | `nearest_fibonacci(abjad)`, ratio d'approche de φ |
| Noms Divins Affins | Abjad des 99 Noms → résonance φ la plus proche |
| Code Grabovoi | Séquences générées par combinaison abjad × mansion × 145 |

**Poids** : 1.5 (renforcé, car spécifique à l'entité)

---

### Couche 3 — SEIGNEURS DU TEMPS (Time-Lords)

| Sous-couche | Source | Durée | Calcul |
|-------------|--------|-------|--------|
| Dasha Coranique | Nouveau | 120 ans | 9 Noms Divins au lieu de 9 planètes. Périodes ∝ Abjad du Nom. Départ = mansion natale. |
| Vimshottari Dasha | RAG ASTRO | 120 ans | Ketu(7)→Ven(20)→Sol(6)→Lune(10)→Mars(7)→Rahu(18)→Jup(16)→Sat(19)→Mer(17) |
| Firdaria | RAG ASTRO | 75 ans | Sol(10),Ven(8),Mer(13),Lune(9),Sat(11),Jup(12),Mars(7),Rahu(3),Ketu(2) |
| Profections Annuelles | RAG ASTRO | 12 ans | `ASC + age × 30°`, Seigneur de l'Année |
| Atacires | RAG ASTRO | Variable | C-12, C-25, C-60, C-72, C-144, C-360, mort(13,45,96,156) |
| Char Dasha (Jaimini) | RAG ASTRO | 96 ans | Durées variables par signe |

**Règle d'activation** : Une période est active si la date cible tombe dans sa fenêtre. Le score est multiplié par la force du Seigneur de la période.

**Poids** : 1.0 (normalisé)

---

### Couche 4 — PARTS / LOTS (Arabes + Coraniques)

| Sous-couche | Source | Nombre | Formule |
|-------------|--------|--------|---------|
| Parts Arabes Traditionnelles | RAG ASTRO | 34 | `ASC + P2 − P1` (jour), `ASC + P1 − P2` (nuit) |
| Parts Coraniques | Nouveau | 34 | `NOM_ABJAD + NOM_DIVIN_ABJAD − RACINE_DIGITALE` |
| Lots des 5 Piliers (Valens) | RAG ASTRO | 5 | Fortune, Esprit, Base, Acquisition, Exaltation |
| Parts par Domaine | Mixte | 5 | Une part calculée pour chaque domaine de vie |

**Placement** : Chaque Part est positionnée dans un domaine/maison. Parts en maisons favorables → score positif.

**Poids** : 1.0 (normalisé)

---

### Couche 5 — DIGNITÉS / FORCES

| Sous-couche | Source | Type |
|-------------|--------|------|
| Dignités Essentielles | RAG ASTRO | Domicile(+5), Exaltation(+4/+5), Triplicité(+3), Termes(+2), Décans(+1), Exil(-5), Chute(-4), Pérégrin(-5) |
| Dignités Accidentelles | RAG ASTRO | Angulaire(+4), Succédent(+2), Cadent(-2), Joie(+2), Rétro(-3), Cazimi(+5), Combustion(-5) |
| Shadbala Védique | RAG ASTRO | Sthana+Dig+Kala+Chesta+Naisargika+Drik (en Rupas) |
| Shadbala Coranique | Nouveau | Stahna(position/99 Noms)+Dig(qibla)+Kala(heure prière)+Naisargika(Abjad)+Drik(liens φ)+Chesta(variation uthmani) |
| Ashtakavarga | RAG ASTRO | 0-8 bindus par signe, Sarva par signe |
| Ashtakavarga Coranique | Nouveau | 7 Noms Divins → 0-1 bindu par groupe de sourates (0-7 par groupe) |

**Poids** : 0.8 (légèrement réduit car très sensible aux variations)

---

### Couche 6 — YOGAS / MOTIFS

| Sous-couche | Source | Détection |
|-------------|--------|-----------|
| Yogas Védiques (30+) | RAG ASTRO | Pancha Mahapurusha, Raja, Dhana, Gajakesari, Kala Sarpa, Neecha Bhanga, Viparita Raja, Shakata, Lunaires |
| Yogas Coraniques | Nouveau | Mahapurusha(num sacré en Kendra=+2.5), Raja(angulaires+trinaux=+2), Dhana(2+5+9+11=+2) |
| Résonances Phi | Coran Num Tal | `abs(r − φ) / φ × 100`, seuil < 5% = résonance |
| Paires Miroirs (Antisces Abjad) | Nouveau | `1000 − ABJAD` → détection de paires complémentaires |
| Chaînes Phi | Coran Num Tal | `A×φ≈B`, `B×φ≈C` → chaîne de 3+ noms divins liés par φ |

**Poids** : 1.2 (renforcé, car motifs rares = haute signification)

---

### Couche 7 — FORMULES D'ÉVÉNEMENTS

| Sous-couche | Source | Nombre |
|-------------|--------|--------|
| Shestopalov Traditionnel | RAG ASTRO | 11 formules (Danger, Accident, Maladie, Hospitalisation, Richesse, Perte, Immobilier, Mariage, Divorce, Carrière, Accident Voiture) |
| Shestopalov Coranique | Nouveau | 5 formules par domaine (min 3 indications harmonieuses pour activer) |

**Mécanisme** : Paires de domaines évaluées. Chaque paire produit une indication favorable/défavorable. Min 3 indications pour activer la formule.

**Poids** : 1.5 (très renforcé — prédiction binaire)

---

### Couche 8 — DIVINATION / ORACLE

| Sous-couche | Source | Méthode |
|-------------|--------|---------|
| Géomancie Classique | RAG ASTRO | 16 figures (Mères→Filles→Nièces→Témoin→Juge), points pair/impair |
| Géomancie Coranique | Nouveau | Comptage pair/impair des lettres d'un verset → figures |
| Oracle Quotidien | Coran Num Tal | `compute_daily_oracle()` : résonance secrète + guidance par domaine + synchronicités |
| SHA-256 Seed | Coran Num Tal | `sha256(date + str(TOTAL_ABJAD))[:8]` → seed déterministe |
| Istikhara Numérique | Nouveau | Tirage de verset + Abjad pair/impair + figure + interprétation |

**Poids** : 0.7 (réduit — oracle = guide, pas certitude)

---

### Couche 9 — AGRÉGATION & DÉCISION

**Score Domainal** :
```
S_domaine = Σ(couche_i × poids_i × activation_i)
```
Où `activation_i` = 1 si la couche est pertinente pour ce domaine, 0 sinon.

**Probabilité** :
```
P_domaine = S_domaine / Σ(S_tous_domaines) × 100
```

**Seuils de décision** :
```
P ≥ 65% → TRÈS FAVORABLE (action recommandée)
P ≥ 55% → FAVORABLE (action possible)
P ≥ 45% → NEUTRE (attendre)
P < 45% → DÉFAVORABLE (éviter)
```

**Value Grace (Finance/Sport)** :
```
edge = (P/100 × odds) − 1.0
edge > 0.15 AND P > 55% → Value Grace détectée
```

---

## IV. ARCHITECTURE DES FICHIERS

```
CORAN NUM TAL/
├── core/
│   ├── existing engines (miftah_phi_engine.py, predictive_oracle.py, person_engine.py, etc.)
│   │
│   ├── unified/
│   │   ├── __init__.py
│   │   │
│   │   ├── cosmic_clock.py          # Couche 1 — Horloge Cosmique
│   │   │   ├── ManazilAlQamar       # 28 mansions lunaires coraniques
│   │   │   ├── NakshatraEngine      # 27 nakshatras védiques
│   │   │   ├── PlanetaryHourEngine  # Heures planétaires + jour/nuit
│   │   │   ├── LunarPhaseEngine     # 8 phases + éclipses
│   │   │   └── PrayerTimeMapper     # Mapping heure → prière islamique
│   │   │
│   │   ├── numeric_signature.py     # Couche 2 — Signature Numérologique
│   │   │   ├── AbjadEngine          # Σ lettres arabes
│   │   │   ├── PhiBridgeEngine      # Pont secret, alignement phi
│   │   │   ├── DivineNameMatcher    # Affinité avec 99 Noms
│   │   │   ├── SacredNumberEngine   # Nombres sacrés + fibonaccisation
│   │   │   └── GrabovoiGenerator    # Séquences Grabovoi personnalisées
│   │   │
│   │   ├── time_lords.py            # Couche 3 — Seigneurs du Temps
│   │   │   ├── CoranicDashaEngine   # 9 Noms Divins, 120 ans
│   │   │   ├── VimshottariEngine    # Dasha védique (import RAG ASTRO)
│   │   │   ├── FirdariaEngine       # Périodes persanes (import RAG ASTRO)
│   │   │   ├── ProtectionEngine     # Profections annuelles
│   │   │   ├── AtacirEngine         # Directions uniformes
│   │   │   └── CharDashaEngine      # Dasha Jaimini
│   │   │
│   │   ├── sacred_parts.py          # Couche 4 — Parts Sacrées
│   │   │   ├── ArabicPartsEngine    # 34 Parts Arabes (import RAG ASTRO)
│   │   │   ├── CoranicPartsEngine   # 34 Parts Coraniques (Abjad)
│   │   │   ├── FivePillarsEngine    # 5 Piliers de Valens
│   │   │   └── DomainPartsEngine    # Parts par domaine de vie
│   │   │
│   │   ├── dignities.py             # Couche 5 — Dignités / Forces
│   │   │   ├── EssentialDignityEngine   # Domicile, exaltation, etc.
│   │   │   ├── AccidentalDignityEngine  # Angulaire, cazimi, etc.
│   │   │   ├── ShadbalaEngine           # 6 forces védiques
│   │   │   ├── CoranicShadbalaEngine    # 6 forces coraniques
│   │   │   ├── AshtakavargaEngine       # Bindus védiques
│   │   │   └── CoranicAshtakavargaEngine # Bindus coraniques
│   │   │
│   │   ├── patterns.py              # Couche 6 — Yogas / Motifs
│   │   │   ├── VedicYogaEngine      # 30+ yogas védiques
│   │   │   ├── CoranicYogaEngine    # Yogas numérologiques
│   │   │   ├── PhiResonanceEngine   # Détection résonances φ
│   │   │   ├── MirrorPairsEngine    # Antisces Abjad
│   │   │   └── PhiChainEngine       # Chaînes de noms divins liés par φ
│   │   │
│   │   ├── event_formulas.py        # Couche 7 — Formules d'Événements
│   │   │   ├── ShestopalovEngine    # 11 formules (import RAG ASTRO)
│   │   │   └── CoranicShestopalovEngine # Formules par domaine
│   │   │
│   │   ├── oracle_layer.py          # Couche 8 — Divination / Oracle
│   │   │   ├── GeomancyEngine       # 16 figures géomantiques
│   │   │   ├── CoranicGeomancyEngine # Géomancie par versets
│   │   │   ├── DailyOracleEngine    # Oracle quotidien (import)
│   │   │   └── IstikharaEngine      # Istikhara numérique
│   │   │
│   │   ├── aggregator.py            # Couche 9 — Agrégation & Décision
│   │   │   ├── ScoreAggregator      # Σ(couche × poids × activation)
│   │   │   ├── ProbabilityNormalizer # score → probabilité
│   │   │   ├── ValueGraceDetector   # edge > 15% && P > 55%
│   │   │   └── DecisionThresholds   # Seuils TRES FAVORABLE → DÉFAVORABLE
│   │   │
│   │   └── cross_domain.py          # Corrélations inter-domaines
│   │       ├── CrossCorrelationMatrix # Corrélations sport↔finance↔personnel
│   │       └── MetaPredictionEngine   # Prédiction de second ordre
│   │
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── sports_adapter.py        # Configure couches pour sport
│   │   │   ├── TeamMatchPredictor   # A vs B (16+ couches)
│   │   │   └── HorseRacePredictor   # N chevaux (5 couches enrichies)
│   │   │
│   │   ├── finance_adapter.py       # Configure couches pour finance
│   │   │   ├── MarketDirectionPredictor # UP vs DOWN
│   │   │   ├── AssetRanker          # Classement multi-actifs
│   │   │   ├── VolatilityEstimator  # Estim. volatilité par cycles
│   │   │   └── NatalChartFinance    # Thème astral d'un actif
│   │   │
│   │   └── personal_adapter.py      # Configure couches pour personnel
│   │       ├── LifeDomainPredictor  # 5-12 domaines de vie
│   │       ├── DailyOracleEnriched  # Oracle quotidien × couches astro
│   │       ├── GrimoirePredictif    # Grimoire avec prédictions
│   │       └── EventTimeline        # Chronologie des événements
│   │
│   └── bridge/
│       ├── __init__.py
│       └── astro_coranic_bridge.py  # Pont d'import RAG ASTRO → CORAN NUM TAL
│           ├── AstroEngineProxy     # Proxy vers engines RAG ASTRO
│           ├── CalculatorImporter   # Import sélectif des calculs astro
│           └── SchemaConverter      # Conversion formats RAG ASTRO ↔ Coran Num Tal
│
├── app/
│   ├── miftah_phi_app.py (modifié)  # Ajout endpoints prédiction unifiée
│   └── webapp/
│       ├── predict.html             # Interface prédiction unifiée
│       ├── predict.js               # JS frontend prédiction
│       └── predict.css              # Styles dashboard prédictif
│
├── corpus/
│   └── computed/
│       └── unified_prediction_config.json  # Configuration des poids/couches
│
└── tests/
    └── test_unified_prediction.py   # Tests unitaires + intégration
```

---

## V. ADAPTATEURS PAR DOMAINE

### 5.1 Adaptateur SPORT (TeamMatchPredictor + HorseRacePredictor)

**Entrée** :
```json
{
  "sport": "Football | Tennis | Hippisme",
  "team_a": {"name": "Équipe A"},
  "team_b": {"name": "Équipe B"},
  "horse_list": [{"number": 5, "name": "Al-Buraq", "birth": "2020-03-15"}],
  "date": "2026-06-15",
  "time": "20:45",
  "latitude": 48.8566,
  "longitude": 2.3522,
  "odds_a": 2.10,
  "odds_b": 3.50
}
```

**Couches actives** : Toutes les 9 couches

**Couches spécifiques héritées du sports_engine.py (16 couches A→O)** :
| Couche | Poids | Description |
|--------|-------|-------------|
| A | ±2.0 | Force des régents (H1 vs H7) |
| B | ±2.0 | Force des seigneurs de victoire (H10 vs H4) |
| C | ±1.5 | Occupants des maisons I et VII |
| D | +1.5/part | Parts Arabes en maisons favorables |
| E | +2.5/1.0 | Lune Ithasala/Eshrapha |
| F | +2.0 | Tajika H1-H10 / H7-H4 |
| G | +1.5 | Heure planétaire + régents |
| H | +1.5/hit | Antisces (Frawley) |
| I | +2.0/hit | Tara Bala védique |
| J | +3.0/hit | Axe nodal Rahu/Ketu |
| K | min(dig×0.3, 1.5) | Dignités étendues |
| L | +weight | Étoiles fixes |
| M | +varga_bonus | Vargottama D9 |
| N | yoga×0.4 | Yogas védiques |
| O | ±0.5 | Phase lunaire |

**Nouvelles couches Coranic ajoutées** :
| Couche | Poids | Description |
|--------|-------|-------------|
| C1 | +2.0 | Signature Abjad des noms d'équipe |
| C2 | +1.5 | Affinité Nom Divin du jour avec régents |
| C3 | +1.0 | Parts Coraniques en maisons favorables |
| C4 | +1.5 | Dasha Coranique active |
| C5 | +1.0 | Géomancie Coranique (tirage verset) |
| C6 | +0.5 | Résonance Phi entre noms d'équipe |

**Sortie Match** :
```json
{
  "verdict": "Équipe A gagnante",
  "prob_a": 62.4,
  "prob_b": 37.6,
  "total_layers_active": 22,
  "value_bet": "Value Bet sur Équipe A (edge: 18.3%)",
  "indicators_a": ["Régent H1 en domicile (+5)", "Jupiter en H1 (+1.5)", ...],
  "indicators_b": ["Saturne en H7 (+1.5 pour A)", ...],
  "coranic_indicators_a": ["Abjad équipe=786 (Basmala)", "Nom Divin du jour=Ya Fattah(489)"],
  "confidence": "ÉLEVÉE"
}
```

**Sortie Hippisme** :
```json
{
  "hour_lord": "Jupiter",
  "predictions": [
    {"rank": 1, "horse": 5, "name": "Al-Buraq", "score": 24.7, "type": "Favori Cosmique",
     "details": ["Vibration directe heure (+8.0)", "Abjad=94 résonne avec Ya Razzaq(319)", "Tara Bala=Sampat (+3.5)"]},
    ...
  ],
  "game_master": "Mars en trigone depuis cuspide V",
  "nakshatra_context": "Lune en Rohini (créativité, abondance)",
  "coranic_bridge": "Mansion 17 (Al-Iklil) sous le Nom Al-Wahhab (Le Donateur)"
}
```

---

### 5.2 Adaptateur FINANCE (MarketPredictor)

**Principe** : Chaque actif financier a un "thème astral" basé sur sa date de première cotation / création. Les cycles planétaires sont corrélés aux cycles de marché.

**Entrée** :
```json
{
  "asset": {
    "symbol": "BTC-USD",
    "name": "Bitcoin",
    "incorporation_date": "2009-01-03",
    "incorporation_time": "18:15",
    "latitude": 51.5074,
    "longitude": -0.1278
  },
  "target_date": "2026-06-15",
  "market_context": {
    "trend": "bullish",
    "volatility_index": 22.5,
    "sector": "crypto"
  }
}
```

**Couches actives** :
| Couche | Poids | Adaptation Finance |
|--------|-------|--------------------|
| Horloge Cosmique | 1.0 | Cycles lunaires × volatilité, éclipses = points de rupture |
| Signature Numérologique | 1.5 | Abjad du ticker + nom, pont secret, phi resonance |
| Time-Lords | 1.2 | Dashas de l'actif (périodes haussières/baissières) |
| Parts/Lots | 0.8 | Parts de Richesse, Commerce, Crédit, Fortune, Perte |
| Dignités | 0.8 | Force de Jupiter (expansion), Saturne (contraction) |
| Yogas | 1.2 | Dhana Yogas (richesse), Shakata (perte), Raja (succès) |
| Formules | 1.5 | Shestopalov Richesse (II+V/VIII/XI), Perte (II-VIII/XII) |
| Oracle | 0.5 | Géomancie, SHA-256 seed, guidance quotidienne |
| Agrégation | 1.0 | Score → Probabilité UP/DOWN + magnitude |

**Sortie** :
```json
{
  "direction": "UP",
  "confidence": 0.72,
  "magnitude_estimate": "modérée (+3% à +8%)",
  "key_dates": ["2026-06-18 (Jupiter trigone Fortune)", "2026-06-22 (Pleine Lune en H2)"],
  "risk_level": "MODÉRÉ",
  "active_dasha": "Jupiter (favorable, expansion)",
  "abjad_resonance": "BTC(2+20+3)=25, digital_root=7, phi_alignment=72%",
  "divine_name_day": "Ya Razzaq (319) — jour de subsistance",
  "indicators": [
    "Jupiter en H2 (+1.5)",
    "Part de Richesse en H1 favorable (+1.5)",
    "Dasha Jupiter actif (+2.0)",
    "Ashtakavarga Sarva H2 = 28 (très bon)",
    "Shestopalov Richesse: 4/5 indications → ACTIF"
  ]
}
```

---

### 5.3 Adaptateur PERSONNEL (LifePredictor)

**Entrée** :
```json
{
  "person": {
    "first_name": "Aziz",
    "last_name": "Eddaghouch",
    "birth_date": "1990-06-15",
    "birth_time": "08:30",
    "birth_lat": 33.5731,
    "birth_lon": -7.5898
  },
  "target_date": "2026-06-15",
  "domains_of_interest": ["richesse", "sante", "amour", "carriere", "spiritualite"]
}
```

**Couches actives** :
| Couche | Poids | Adaptation Personnel |
|--------|-------|---------------------|
| Horloge Cosmique | 1.0 | Manazil natale vs jour, Tara Bala |
| Signature Numérologique | 2.0 | Abjad complet, pont secret, alignement phi |
| Time-Lords | 1.5 | TOUS les dashas actifs simultanément |
| Parts/Lots | 1.0 | Parts Arabes + Coraniques dans maisons natales |
| Dignités | 0.8 | Shadbala complet + Coranic Shadbala |
| Yogas | 1.5 | Yogas védiques + coraniques dans thème natal |
| Formules | 1.5 | Shestopalov tous domaines |
| Oracle | 1.0 | Oracle quotidien + géomancie + istikhara |
| Agrégation | 1.0 | Score par domaine de vie |

**Sortie** :
```json
{
  "date": "2026-06-15",
  "age": 36.0,
  "personal_signature": {
    "abjad": 94,
    "digital_root": 4,
    "secret_bridge": 8768,
    "phi_alignment": 72.5
  },
  "active_time_lords": {
    "vimshottari": "Jupiter (16 ans, début 2024)",
    "coranic_dasha": "Al-Razzaq (319, période de subsistance)",
    "firdaria": "Jupiter/mercure",
    "profection": "Maison 1 (nouveau cycle de 12 ans)"
  },
  "domains": {
    "richesse": {
      "score": 72,
      "probability": 72,
      "verdict": "TRÈS FAVORABLE",
      "indicators": ["Jupiter en H2", "Part de Fortune angulaire", "Dasha Jupiter+Razzaq", "Lune croissante"],
      "recommendation": "Période idéale pour investissements et nouveaux projets financiers. Code : 786 319 145"
    },
    "sante": {
      "score": 58,
      "probability": 58,
      "verdict": "FAVORABLE",
      "indicators": ["Soleil en H1", "Pas de planète en H6", "Lune en mansion favorable"],
      "recommendation": "Énergie stable. Maintenir les bonnes habitudes. Dhikr Ya Shafi (401)"
    },
    "amour": {
      "score": 45,
      "probability": 45,
      "verdict": "NEUTRE",
      "indicators": ["Vénus rétrograde", "H7 vide", "Profection en H1"],
      "recommendation": "Période d'introspection. Éviter les grandes décisions relationnelles."
    },
    "carriere": {
      "score": 81,
      "probability": 81,
      "verdict": "TRÈS FAVORABLE",
      "indicators": ["MC en domicile", "Jupiter en H10", "Raja Yoga actif"],
      "recommendation": "Promotion ou reconnaissance probable. Sourate 56 (Al-Waqi'a) à réciter."
    },
    "spiritualite": {
      "score": 65,
      "probability": 65,
      "verdict": "FAVORABLE",
      "indicators": ["Mansion 17 (Al-Iklil)", "Nœud Nord en H9", "Al-Muhaymin(145) actif"],
      "recommendation": "Méditation phi à Maghrib. Rituel 7 jours avec sourate personnelle (abjad%114=94 → S94 Al-Inshirah)."
    }
  },
  "global_phi_index": 0.865,
  "power_hour": "Maghrib (couchant)",
  "daily_codes": ["145 17 213 786", "8768 786 56", "94 17 145"]
}
```

---

## VI. MOTEUR DE CORRÉLATIONS INTER-DOMAINES

### `cross_domain.py` — Matrice de Corrélation

```
┌──────────┬──────────┬──────────┬──────────┐
│          │  SPORT   │ FINANCE  │PERSONNEL │
├──────────┼──────────┼──────────┼──────────┤
│  SPORT   │    1.0   │  0.45    │  0.30    │
│ FINANCE  │  0.45    │   1.0    │  0.55    │
│PERSONNEL │  0.30    │  0.55    │   1.0    │
└──────────┴──────────┴──────────┴──────────┘
```

**Règles de corrélation** :
- Sport↔Finance : si plusieurs Value Bets sont détectés le même jour, période de volatilité → prudence sur les marchés
- Finance↔Personnel : si Dasha Jupiter+Razzaq actif pour la personne, les investissements ce jour-là sont doublement favorables
- Sport↔Personnel : si Profection en H1 (nouveau cycle), les compétitions ce jour-là ont une probabilité accrue de surprise (outsider)

**Meta-Prédiction** :
```python
meta_score = sport_score × 0.25 + finance_score × 0.35 + personal_score × 0.40
```
Le meta-score révèle la "qualité cosmique" globale d'un jour donné, toutes dimensions confondues.

---

## VII. PLAN D'IMPLÉMENTATION

### Phase 1 — Fondations (Semaine 1-2)
1. **`bridge/astro_coranic_bridge.py`** — Importer les engines RAG ASTRO comme modules
2. **`unified/cosmic_clock.py`** — Unifier Manazil + Nakshatras + Heures Planétaires + Prières
3. **`unified/numeric_signature.py`** — Extraire du code existant
4. **`unified/aggregator.py`** — ScoreAggregator + ProbabilityNormalizer + ValueGraceDetector

### Phase 2 — Couches (Semaine 3-4)
5. **`unified/time_lords.py`** — CoranicDashaEngine + import Vimshottari/Firdaria/Profections/Atacires
6. **`unified/sacred_parts.py`** — CoranicPartsEngine (34 Parts) + import ArabicPartsEngine
7. **`unified/dignities.py`** — CoranicShadbalaEngine + CoranicAshtakavargaEngine
8. **`unified/patterns.py`** — CoranicYogaEngine + PhiResonanceEngine + MirrorPairsEngine

### Phase 3 — Domaines (Semaine 5-6)
9. **`unified/event_formulas.py`** — CoranicShestopalovEngine
10. **`unified/oracle_layer.py`** — CoranicGeomancyEngine + IstikharaEngine
11. **`adapters/sports_adapter.py`** — TeamMatchPredictor + HorseRacePredictor enrichis
12. **`adapters/finance_adapter.py`** — MarketPredictor complet

### Phase 4 — Personnel + API (Semaine 7-8)
13. **`adapters/personal_adapter.py`** — LifeDomainPredictor + DailyOracleEnriched + GrimoirePredictif
14. **`unified/cross_domain.py`** — Corrélations inter-domaines
15. **`app/miftah_phi_app.py`** — Nouveaux endpoints API
16. **`app/webapp/predict.html`** — Interface dashboard prédictif

---

## VIII. ENDPOINTS API

| Méthode | Route | Description |
|---------|-------|-------------|
| POST | `/api/unified/sport` | Prédiction sportive enrichie (match + hippisme) |
| POST | `/api/unified/finance` | Prédiction financière (direction + magnitude) |
| POST | `/api/unified/personal` | Prédiction personnelle multi-domaine |
| POST | `/api/unified/all` | Les trois prédictions + corrélations |
| GET | `/api/unified/day-quality?date=` | Score méta quotidien (qualité cosmique du jour) |
| GET | `/api/unified/config` | Configuration active (couches, poids, seuils) |
| POST | `/api/unified/config` | Mettre à jour la configuration |

---

## IX. CONCLUSION

Ce moteur unifié repose sur **3 piliers** :

1. **φ (Nombre d'Or)** — le pont mathématique entre le Coran et le Cosmos, validé par TOTAL_ABJAD/145 ≈ φ×10⁵
2. **L'agrégation additive** — validée par 16 couches opérationnelles dans le sports_engine.py
3. **L'interconnexion** — chaque couche nourrit les 3 domaines simultanément, créant un écosystème prédictif cohérent

Le résultat est un système où :
- Un **cheval** est analysé par son Abjad, sa mansion lunaire, et les transits astraux du jour
- Un **actif financier** est évalué par son thème astral natal, ses dashas, et les Parts de Richesse
- Une **personne** reçoit une prédiction complète sur 5 domaines de vie, synchronisant astrologie et Abjad

La même date, la même heure, le même lieu → **une seule cohérence cosmique**, lue à travers 3 lentilles différentes.
