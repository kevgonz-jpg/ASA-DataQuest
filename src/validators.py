"""
validators.py — Funciones de validación y control de calidad.

Cada función valida un aspecto del dataset y retorna un reporte
o levanta una advertencia si encuentra problemas.
"""
import pandas as pd
import json
from pathlib import Path


def audit_missing_values(df: pd.DataFrame, name: str = "dataset") -> pd.DataFrame:
    """Auditoría completa de valores faltantes.

    Args:
        df: DataFrame a auditar.
        name: Nombre descriptivo del dataset.

    Returns:
        DataFrame con columnas: [column, n_missing, pct_missing, dtype].
    """
    total = len(df)
    missing = df.isnull().sum()
    report = pd.DataFrame({
        "column": df.columns,
        "n_missing": missing.values,
        "pct_missing": (missing.values / total * 100).round(2),
        "dtype": [str(t) for t in df.dtypes.values]
    })
    report = report[report["n_missing"] > 0].sort_values("n_missing", ascending=False).reset_index(drop=True)
    return report


def validate_births_consistency(df: pd.DataFrame, tol: float = 0.01) -> pd.DataFrame:
    """Valida que BirthsMale + BirthsFemale ≈ Births (control de calidad).

    Args:
        df: DataFrame con columnas 'Births', 'BirthsMale', 'BirthsFemale'.
        tol: Tolerancia relativa permitida.

    Returns:
        DataFrame con filas donde la consistencia falla.
    """
    required = {"Births", "BirthsMale", "BirthsFemale"}
    if not required.issubset(df.columns):
        raise ValueError(f"El DataFrame debe contener las columnas: {required}")
    
    calc_sum = df["BirthsMale"] + df["BirthsFemale"]
    diff = (calc_sum - df["Births"]).abs()
    rel_diff = diff / (df["Births"].abs() + 1e-9)
    inconsistent = df[rel_diff > tol].copy()
    inconsistent["diff_births"] = diff[rel_diff > tol]
    inconsistent["rel_diff_births"] = rel_diff[rel_diff > tol]
    return inconsistent


def check_bronze_files_exist(bronze_path: Path = None) -> dict:
    """Verifica que los archivos bronze esperados existan.

    Args:
        bronze_path: Path a data/bronze/ (opcional, usa src.config.BRONZE por defecto).

    Returns:
        Dict con {filename: {'exists': bool, 'size_mb': float, 'path': str}} indicando existencia.
    """
    if bronze_path is None:
        from src.config import BRONZE, DOCS
        bronze_path = BRONZE
        docs_path = DOCS
    else:
        bronze_path = Path(bronze_path)
        docs_path = bronze_path.parent.parent / "docs"

    files_to_check = {
        "Medium": bronze_path / "WPP2024_Demographic_Indicators_Medium_csv.gz",
        "OtherVariants": bronze_path / "WPP2024_Demographic_Indicators_OtherVariants_csv.gz",
        "Supplement": bronze_path / "WPP2024_Supplement_Births_and_LE60.csv",
        "Notes": docs_path / "WPP2024_Demographic_Indicators_notes.csv",
    }

    results = {}
    for name, p in files_to_check.items():
        exists = p.exists()
        size_mb = round(p.stat().st_size / (1024 * 1024), 2) if exists else 0.0
        results[name] = {
            "exists": exists,
            "size_mb": size_mb,
            "path": str(p)
        }
    return results


def generate_quality_report(df: pd.DataFrame, output_path: Path = None) -> dict:
    """Genera un reporte de calidad en JSON y opcionalmente lo guarda.

    Incluye: shape, dtypes, missings, duplicados, memoria en MB.

    Args:
        df: DataFrame a reportar.
        output_path: Path donde guardar el JSON (opcional).

    Returns:
        Dict con el reporte.
    """
    report = {
        "n_rows": int(len(df)),
        "n_cols": int(df.shape[1]),
        "memory_mb": round(float(df.memory_usage(deep=True).sum() / (1024 * 1024)), 2),
        "n_duplicates": int(df.duplicated().sum()),
        "columns_with_na": int((df.isnull().sum() > 0).sum()),
        "total_na_cells": int(df.isnull().sum().sum()),
        "na_pct": round(float(df.isnull().sum().sum()) / (df.shape[0] * df.shape[1]) * 100, 2),
    }
    if output_path is not None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
    return report

