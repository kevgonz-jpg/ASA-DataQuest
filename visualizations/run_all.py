"""
run_all.py — Generador por lotes de todas las visualizaciones interactivas de ASA DataQuest 2026.
"""

import sys
from pathlib import Path

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

base_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(base_dir))

from visualizations.tfr_vs_lex_animated import create_tfr_vs_lex_animation
from visualizations.pca_trajectories import create_pca_trajectories_figure

def generate_all():
    figures_dir = base_dir / "outputs" / "figures"
    final_dir = figures_dir / "final"
    final_dir.mkdir(parents=True, exist_ok=True)

    print("================================================================================")
    print("   ASA DataQuest 2026 — Generador de Visualizaciones Finales (Plotly HTML)")
    print("================================================================================")

    # 1. TFR vs LEx
    print("\n[1/2] Generando Curva de Transicion Demografica Animada (TFR vs LEx)...")
    fig1 = create_tfr_vs_lex_animation(
        output_html_path=figures_dir / "01_tfr_vs_lex_animated.html"
    )
    fig1.write_html(str(final_dir / "01_tfr_vs_lex_animated.html"), include_plotlyjs="cdn")
    print(f"  [OK] Guardado en: {figures_dir / '01_tfr_vs_lex_animated.html'}")

    # 2. PCA Trajectories 2D / 3D
    print("\n[2/2] Generando Trayectorias en el Espacio Factorial PCA (2D / 3D)...")
    fig2 = create_pca_trajectories_figure(
        output_html_path=figures_dir / "02_pca_trajectories_2d_3d.html"
    )
    fig2.write_html(str(final_dir / "02_pca_trajectories_2d_3d.html"), include_plotlyjs="cdn")
    print(f"  [OK] Guardado en: {figures_dir / '02_pca_trajectories_2d_3d.html'}")

    print("\n================================================================================")
    print("   [OK] Todas las figuras fueron generadas y guardadas exitosamente en:")
    print(f"        -> {figures_dir}")
    print(f"        -> {final_dir}")
    print("================================================================================")

if __name__ == "__main__":
    generate_all()
