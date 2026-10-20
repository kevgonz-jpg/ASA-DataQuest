"""
transforms.py — Funciones de limpieza y transformacion (Bronze -> Silver).
"""
import pandas as pd
from src.config import COUNTRY_LOCTYPEID, ESTIMATION_CUTOFF


def filter_countries(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["LocTypeID"] == COUNTRY_LOCTYPEID].copy()


def split_estimates_projections(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    estimates = df[df["Time"] <= ESTIMATION_CUTOFF].copy()
    projections = df[df["Time"] > ESTIMATION_CUTOFF].copy()
    return estimates, projections


def create_derived_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "LExFemale" in out.columns and "LExMale" in out.columns:
        out["GenderGapLE"] = out["LExFemale"] - out["LExMale"]
    if "Time" in out.columns:
        out["IsEstimate"] = out["Time"] <= ESTIMATION_CUTOFF
        bins = [-float("inf"), 1979, 1999, 2023, 2049, float("inf")]
        labels = ["1950-1979", "1980-1999", "2000-2023", "2024-2049", "2050-2100"]
        out["Epoch"] = pd.cut(out["Time"], bins=bins, labels=labels)
    if "CBR" in out.columns and "CDR" in out.columns:
        out["NaturalGrowth"] = out["CBR"] - out["CDR"]
    return out


def merge_supplement(medium_df: pd.DataFrame, supplement_df: pd.DataFrame) -> pd.DataFrame:
    suppl_cols = [c for c in ["LocID", "Time", "BirthsMale", "BirthsFemale", "LE60", "LE60Male", "LE60Female"] if c in supplement_df.columns]
    return medium_df.merge(supplement_df[suppl_cols], on=["LocID", "Time"], how="left")
