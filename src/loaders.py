"""
loaders.py — Funciones de carga de datos desde la capa Bronze.

Cada función carga un dataset específico y retorna un DataFrame sin modificar.
La limpieza y transformación se hace en transforms.py.
"""
import pandas as pd
from src.config import MEDIUM_FILE, OTHERVARIANTS_FILE, SUPPLEMENT_FILE, NOTES_FILE


def load_medium(nrows: int = None) -> pd.DataFrame:
    """Carga el dataset principal (Medium variant).

    Args:
        nrows: Número opcional de filas a leer (útil para sampling o pruebas).

    Returns:
        DataFrame con ~84,360 filas × 67 columnas.
        Incluye TODOS los tipos de localización (países + agregados).
    """
    return pd.read_csv(
        MEDIUM_FILE,
        compression="gzip",
        encoding="utf-8-sig",
        low_memory=False,
        nrows=nrows,
    )


def load_other_variants(nrows: int = None) -> pd.DataFrame:
    """Carga variantes alternativas y bandas probabilísticas (2024–2100).

    Args:
        nrows: Número opcional de filas a leer.

    Returns:
        DataFrame con variantes High, Low, PI80, PI95, etc.
    """
    return pd.read_csv(
        OTHERVARIANTS_FILE,
        compression="gzip",
        encoding="utf-8-sig",
        low_memory=False,
        nrows=nrows,
    )


def load_supplement(nrows: int = None) -> pd.DataFrame:
    """Carga el suplemento de nacimientos por sexo y LE60.

    Args:
        nrows: Número opcional de filas a leer.

    Returns:
        DataFrame con ~35,638 filas × 9 columnas.
    """
    return pd.read_csv(
        SUPPLEMENT_FILE,
        encoding="utf-8-sig",
        low_memory=False,
        nrows=nrows,
    )


def load_notes() -> pd.DataFrame:
    """Carga el diccionario de indicadores (codebook).

    Returns:
        DataFrame con ~59 filas describiendo cada indicador y sus unidades.
    """
    return pd.read_csv(NOTES_FILE, encoding="utf-8-sig")

