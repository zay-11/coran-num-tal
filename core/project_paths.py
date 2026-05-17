from __future__ import annotations

from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]

APP_DIR = ROOT_DIR / "app"
WEBAPP_DIR = APP_DIR / "webapp"

CORE_DIR = ROOT_DIR / "core"
SCRIPTS_DIR = ROOT_DIR / "scripts"
PDF_GENERATORS_DIR = SCRIPTS_DIR / "pdf_generators"
MAINTENANCE_DIR = SCRIPTS_DIR / "maintenance"

CORPUS_DIR = ROOT_DIR / "corpus"
QURAN_DATA_DIR = CORPUS_DIR / "quran"
IMPORTED_CORPORA_DIR = CORPUS_DIR / "imported"

EXPORTS_DIR = ROOT_DIR / "exports"
GENERATED_DIR = EXPORTS_DIR / "generated"
GENERATED_TALISMANS_DIR = GENERATED_DIR / "talismans"
LIBRARY_DIR = EXPORTS_DIR / "library"
LIBRARY_ANALYSES_DIR = LIBRARY_DIR / "analyses"
LIBRARY_TALISMANS_DIR = LIBRARY_DIR / "talismans"
PDF_DIR = EXPORTS_DIR / "pdf"
PDF_RICHESSE_DIR = PDF_DIR / "richesse_abondance"
PDF_RADIONIQUE_DIR = PDF_DIR / "radionique"
PDF_MIFTAH_DIR = PDF_DIR / "miftah_19"
PDF_MIFTAH_CADRANS_DIR = PDF_MIFTAH_DIR / "cadrans"
PDF_MIFTAH_RITUELS_DIR = PDF_MIFTAH_DIR / "rituels"
PDF_MIFTAH_TALISMANS_DIR = PDF_MIFTAH_DIR / "talismans"
PDF_MIFTAH_WORKBOOKS_DIR = PDF_MIFTAH_DIR / "workbooks"
HTML_DIR = EXPORTS_DIR / "html"
HTML_CADRANS_DIR = HTML_DIR / "cadrans"
PREVIEW_DIR = EXPORTS_DIR / "preview"

DOCS_DIR = ROOT_DIR / "docs"
ASSETS_DIR = ROOT_DIR / "assets"
ASSETS_IMAGES_DIR = ASSETS_DIR / "images"
CONFIG_DIR = ROOT_DIR / "config"
ARCHIVE_DIR = ROOT_DIR / "archive"

PDF_OUTPUTS = {
    "decouverte_phi": PDF_RICHESSE_DIR / "Decouverte_Phi_Coran_Rizq.pdf",
    "secret_rizq_esoterique": PDF_RICHESSE_DIR / "Secret_Rizq_Phi_Grabovoi_Esoterique.pdf",
    "secret_rizq_deluxe": PDF_RICHESSE_DIR / "Secret_Rizq_Phi_Deluxe.pdf",
    "module_radionique_rizq": PDF_RADIONIQUE_DIR / "Module_Radionique_Rizq_Phi.pdf",
    "radionique_sacree": PDF_RADIONIQUE_DIR / "Radionique_Sacree_Miftah_19.pdf",
    "radionique_amplifiee": PDF_RADIONIQUE_DIR / "Radionique_Amplifiee_Miftah_19.pdf",
    "guide_visuel_radionique": PDF_RADIONIQUE_DIR / "Guide_Visuel_Radionique_Miftah_19.pdf",
    "cadran_lunaire_pdf": PDF_MIFTAH_CADRANS_DIR / "Cadran_Lunaire_Miftah_19.pdf",
    "cadran_lunaire_html": HTML_CADRANS_DIR / "Cadran_Lunaire_Miftah19.html",
    "rituel_miftah": PDF_MIFTAH_RITUELS_DIR / "Rituel_Miftah_19.pdf",
    "talisman_ultime": PDF_MIFTAH_TALISMANS_DIR / "Talisman_Ultime_Miftah_19.pdf",
    "workbook_miftah": PDF_MIFTAH_WORKBOOKS_DIR / "Workbook_Miftah_19_Premium.pdf",
}


def ensure_layout() -> None:
    for path in [
        APP_DIR,
        WEBAPP_DIR,
        CORE_DIR,
        SCRIPTS_DIR,
        PDF_GENERATORS_DIR,
        MAINTENANCE_DIR,
        CORPUS_DIR,
        QURAN_DATA_DIR,
        IMPORTED_CORPORA_DIR,
        EXPORTS_DIR,
        GENERATED_DIR,
        GENERATED_TALISMANS_DIR,
        LIBRARY_DIR,
        LIBRARY_ANALYSES_DIR,
        LIBRARY_TALISMANS_DIR,
        PDF_DIR,
        PDF_RICHESSE_DIR,
        PDF_RADIONIQUE_DIR,
        PDF_MIFTAH_DIR,
        PDF_MIFTAH_CADRANS_DIR,
        PDF_MIFTAH_RITUELS_DIR,
        PDF_MIFTAH_TALISMANS_DIR,
        PDF_MIFTAH_WORKBOOKS_DIR,
        HTML_DIR,
        HTML_CADRANS_DIR,
        PREVIEW_DIR,
        DOCS_DIR,
        ASSETS_IMAGES_DIR,
        CONFIG_DIR,
        ARCHIVE_DIR,
    ]:
        path.mkdir(parents=True, exist_ok=True)
