# Miftah Phi Engine

Moteur esoterique pour lire une sourate, un verset ou un texte sacre et produire :

- une signature numerique
- un talisman
- un dhikr
- un rituel
- un module radionique

## Fichiers principaux

- `core/miftah_phi_engine.py` : moteur Coran, abjad, phi, Fibonacci, domaines.
- `core/sacred_text_engine.py` : moteur multi-traditions, guematrie hebraique, isopsephie grecque, textes importes.
- `core/talisman_image_generator.py` : generation PNG des talismans.
- `app/miftah_phi_app.py` : serveur local de l'application.
- `scripts/maintenance/build_quran_library.py` : generation batch de la bibliotheque Coran.

## Donnees

- `corpus/quran/quran-simple-clean.txt`
- `corpus/quran/quran-uthmani-min.txt`
- `corpus/quran/quran-data.xml`
- `corpus/imported/*.json`

## Domaines supportes

- `richesse`
- `sante`
- `savoir`
- `protection`
- `occultes`

## Commandes utiles

Lister les domaines :

```powershell
& "C:\Users\eddaz\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" .\core\miftah_phi_engine.py domains
```

Analyser la sourate 56 en mode richesse :

```powershell
& "C:\Users\eddaz\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" .\core\miftah_phi_engine.py analyze-ref --sura 56 --domain richesse --pretty
```

Analyser le verset 51:58 :

```powershell
& "C:\Users\eddaz\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" .\core\miftah_phi_engine.py analyze-ref --sura 51 --ayah 58 --domain richesse --pretty
```

Exporter un JSON :

```powershell
& "C:\Users\eddaz\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" .\core\miftah_phi_engine.py analyze-ref --sura 56 --domain richesse --json-out .\exports\preview\analyse_s56.json
```

Generer un talisman PNG depuis une analyse :

```powershell
& "C:\Users\eddaz\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" .\core\talisman_image_generator.py --json .\exports\library\analyses\sura_056_richesse.json
```

Regenerer la bibliotheque complete :

```powershell
& "C:\Users\eddaz\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" .\scripts\maintenance\build_quran_library.py
```

## Appli locale

Lancement :

```powershell
& "C:\Users\eddaz\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" .\app\miftah_phi_app.py
```

Puis ouvrir :

```text
http://127.0.0.1:8765
```

L'application permet :

- analyse coranique par sourate, verset ou plage
- rendu automatique d'un talisman PNG
- import de corpus sacres externes en `ref|texte` ou JSON
- analyse en abjad arabe, guematrie hebraique, isopsephie grecque
- consultation de la bibliotheque batch des 114 sourates

## Sorties

- `exports/pdf/richesse_abondance/`
- `exports/pdf/radionique/`
- `exports/pdf/miftah_19/`
- `exports/generated/talismans/`
- `exports/library/quran_surah_library.json`
- `exports/library/analyses/*.json`
- `exports/library/talismans/*.png`
