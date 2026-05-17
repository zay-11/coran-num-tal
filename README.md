# CORAN NUM TAL

Structure principale du projet apres rangement :

- `app/` : application locale et interface web.
- `core/` : moteurs de calcul, chemins projet, generation de talismans.
- `scripts/pdf_generators/` : scripts qui generent les PDF.
- `scripts/maintenance/` : scripts batch et maintenance.
- `corpus/` : textes sources, Coran local et corpus importes.
- `exports/` : tous les PDF, PNG, JSON et bibliotheques generes.
- `docs/` : documentation d'utilisation.
- `assets/` : images et ressources visuelles.
- `config/` : fichiers de configuration.
- `archive/` : anciens doublons et caches conserves.

## Commandes rapides

Lancer l'application :

```powershell
& "C:\Users\eddaz\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" .\app\miftah_phi_app.py
```

Analyser une sourate :

```powershell
& "C:\Users\eddaz\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" .\core\miftah_phi_engine.py analyze-ref --sura 56 --domain richesse --pretty
```

Les PDF classes par theme sont dans `exports/pdf/`.
