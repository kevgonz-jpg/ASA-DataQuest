"""
config.py — Constantes centralizadas del proyecto ASA DataQuest 2026.

Todas las rutas, seeds y columnas clave se definen aquí para garantizar
consistencia y reproducibilidad en todo el pipeline.
"""
from pathlib import Path

# ============================================================
# PATHS — Arquitectura Medallion
# ============================================================
ROOT = Path(__file__).resolve().parent.parent

# Data layers
BRONZE = ROOT / "data" / "bronze"
SILVER = ROOT / "data" / "silver"
GOLD   = ROOT / "data" / "gold"

# Outputs
FIGURES_EDA   = ROOT / "outputs" / "figures" / "eda"
FIGURES_FINAL = ROOT / "outputs" / "figures" / "final"
TABLES        = ROOT / "outputs" / "tables"
REPORTS       = ROOT / "outputs" / "reports"

# Docs
DOCS = ROOT / "docs"

# ============================================================
# BRONZE FILE NAMES
# ============================================================
MEDIUM_FILE       = BRONZE / "WPP2024_Demographic_Indicators_Medium_csv.gz"
OTHERVARIANTS_FILE = BRONZE / "WPP2024_Demographic_Indicators_OtherVariants_csv.gz"
SUPPLEMENT_FILE   = BRONZE / "WPP2024_Supplement_Births_and_LE60.csv"
NOTES_FILE        = DOCS / "WPP2024_Demographic_Indicators_notes.csv"

# ============================================================
# REPRODUCIBILITY
# ============================================================
SEED = 42

# ============================================================
# COLUMN GROUPS
# ============================================================
ID_COLS = ["SortOrder", "LocID", "Notes", "ISO3_code", "ISO2_code",
           "SDMX_code", "LocTypeID", "LocTypeName", "ParentID",
           "Location", "VarID", "Variant", "Time"]

KEY_INDICATORS = ["TFR", "LEx", "LExMale", "LExFemale", "IMR",
                  "MedianAgePop", "PopGrowthRate", "NetMigrations",
                  "TPopulation1July", "CBR", "CDR", "NRR"]

# ============================================================
# ANALYSIS CONSTANTS
# ============================================================
ESTIMATION_CUTOFF = 2023   # <= 2023 = estimaciones, >= 2024 = proyecciones
COUNTRY_LOCTYPEID = 4      # LocTypeID para Country/Area

EPOCH_YEARS = [1950, 1980, 2000, 2024, 2050, 2100]  # Para comparaciones

# ============================================================
# VISUALIZATION
# ============================================================
FIG_DPI = 150
FIG_FORMAT = "png"         # "png", "svg", or "pdf"

# Paleta colorblind-friendly
PALETTE_NAME = "colorblind"
