"""
viz.py — Funciones de visualización reutilizables.

Todas las funciones siguen los mismos principios:
- Paleta colorblind-friendly (viridis/colorblind)
- Alta resolución (DPI configurable)
- Guardan la figura si se pasa save_path
- Retornan (fig, ax) para personalización posterior
"""
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np
import pandas as pd
from pathlib import Path
from src.config import FIG_DPI, FIG_FORMAT, PALETTE_NAME, FIGURES_EDA, FIGURES_FINAL


def setup_style():
    """Configura el estilo global de matplotlib/seaborn.

    Llamar al inicio de cada notebook.
    """
    plt.rcParams.update({
        'figure.figsize': (12, 6),
        'figure.dpi': FIG_DPI,
        'font.size': 11,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'axes.spines.top': False,
        'axes.spines.right': False,
    })
    sns.set_palette(PALETTE_NAME)


def save_figure(fig, name: str, subdir: str = "eda"):
    """Guarda una figura en el directorio correcto.

    Args:
        fig: matplotlib Figure.
        name: Nombre del archivo (sin extensión).
        subdir: "eda" o "final".
    """
    base = FIGURES_EDA if subdir == "eda" else FIGURES_FINAL
    base.mkdir(parents=True, exist_ok=True)
    path = base / f"{name}.{FIG_FORMAT}"
    fig.savefig(path, dpi=FIG_DPI, bbox_inches='tight', facecolor='white')
    print(f"  Saved: {path.relative_to(path.parents[3])}")


# TODO: Agregar funciones de visualización a medida que las necesites.
# Ejemplos:
#
# def plot_kde_by_epoch(df, variable, epochs, **kwargs):
#     """KDE plot de una variable en distintas épocas."""
#     pass
#
# def plot_correlation_matrix(df, variables, **kwargs):
#     """Heatmap de correlaciones Spearman."""
#     pass
#
# def plot_timeline(df, variable, groupby, **kwargs):
#     """Line plot de evolución temporal por grupo."""
#     pass
