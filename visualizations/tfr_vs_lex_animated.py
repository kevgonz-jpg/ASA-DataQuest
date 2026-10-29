"""
tfr_vs_lex_animated.py — Curva de Transición Demográfica Animada (1950–2023)

Genera una visualización interactiva en Plotly con slider temporal (1950–2023)
y controles para alternar entre:
  1. Nube de Países (Scatter por Continente con tamaño según población).
  2. Mapa de Calor / Nube Térmica Fluida (Densidad Kernel Gaussiana 2D renderizada
     mediante halos térmicos aditivos vectoriales con interpolación continua a 60 FPS
     y sin parpadeos ni destellos mediante redraw=False).
  3. Vista Superpuesta (Halos y núcleos térmicos continuos + burbujas de países).

Muestra empíricamente el cruce del umbral de reemplazo generacional (TFR = 2.1)
y el desplazamiento global en esperanza de vida (LEx).
"""

from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde
import plotly.graph_objects as go

# Paleta oficial colorblind-friendly para continentes
CONTINENT_COLORS = {
    'Africa': '#E69F00',                     # Naranja cálido
    'Asia': '#56B4E9',                       # Azul cielo
    'Europe': '#009E73',                     # Verde azulado
    'Latin America & Caribbean': '#D55E0D', # Bermellón
    'Northern America': '#0072B2',           # Azul marino
    'Oceania': '#CC79A7'                     # Púrpura rojizo
}

CONTINENT_ORDER = [
    'Africa', 'Asia', 'Europe',
    'Latin America & Caribbean',
    'Northern America', 'Oceania'
]


def load_demographic_data(parquet_path: Path | str = None) -> pd.DataFrame:
    """Carga los perfiles demográficos desde la capa Gold o Silver."""
    if parquet_path is None:
        base_dir = Path(__file__).resolve().parent.parent
        parquet_path = base_dir / 'data' / 'gold' / 'demographic_profiles.parquet'
        if not parquet_path.exists():
            parquet_path = base_dir / 'data' / 'silver' / 'wpp2024_countries_estimates.parquet'

    df = pd.read_parquet(parquet_path)
    if 'LocTypeID' in df.columns:
        df = df[df['LocTypeID'] == 4].copy()
    if 'Time' in df.columns:
        df = df[df['Time'] <= 2023].copy()
    return df


def _build_year_traces(year_df: pd.DataFrame, is_base: bool = False):
    """
    Construye las trazas para un año específico usando un modelo vectorial
    de capas térmicas (Glow) que Plotly interpola suavemente entre frames
    sin reconstruir el lienzo ni parpadear.
    """
    traces = []

    # Cálculo de densidad local con Kernel Gaussiano (KDE)
    tfr_vals = year_df['TFR'].values
    lex_vals = year_df['LEx'].values

    kde = gaussian_kde([tfr_vals, lex_vals], bw_method=0.35)
    densities = kde([tfr_vals, lex_vals])
    d_min, d_max = densities.min(), densities.max()
    densities_norm = (densities - d_min) / (d_max - d_min + 1e-9)

    # -------------------------------------------------------------
    # Traza 0: Halo Térmico Ambiental (difuso, amplio, aditivo)
    # En zonas densas, los círculos translúcidos se suman creando
    # una masa luminosa térmica que se desplaza fluidamente a 60 FPS.
    # -------------------------------------------------------------
    traces.append(go.Scatter(
        x=tfr_vals,
        y=lex_vals,
        mode='markers',
        name='Halo Térmico',
        marker=dict(
            size=52,
            color='rgba(225, 29, 72, 0.13)',  # Carmesí translúcido aditivo
            line=dict(width=0)
        ),
        hoverinfo='skip',
        showlegend=False,
        visible=True if is_base else None
    ))

    # -------------------------------------------------------------
    # Traza 1: Núcleo Térmico de Densidad (coloreado en escala Plasma)
    # Refleja con precisión la intensidad local de concentración.
    # -------------------------------------------------------------
    traces.append(go.Scatter(
        x=tfr_vals,
        y=lex_vals,
        mode='markers',
        name='Núcleo de Densidad',
        marker=dict(
            size=22,
            color=densities_norm,
            colorscale='Plasma',
            cmin=0.0,
            cmax=1.0,
            opacity=0.80,
            line=dict(width=0.5, color='rgba(255,255,255,0.7)')
        ),
        hoverinfo='skip',
        showlegend=False,
        visible=True if is_base else None
    ))

    # -------------------------------------------------------------
    # Trazas 2 a 7: Burbujas por Continente
    # -------------------------------------------------------------
    for cont in CONTINENT_ORDER:
        c_df = year_df[year_df['Continent'] == cont]
        if c_df.empty:
            traces.append(go.Scatter(
                x=[], y=[], mode='markers', name=cont,
                marker=dict(color=CONTINENT_COLORS[cont]),
                visible=True if is_base else None
            ))
            continue

        pop_m = c_df['TPopulation1July'] / 1000.0  # Millones
        sizes = np.clip(np.sqrt(pop_m) * 2.6 + 6.0, 6.0, 42.0)

        hover_text = [
            f"<b>{loc}</b> ({iso})<br>"
            f"Continente: {cont}<br>"
            f"Año: {int(row.Time)}<br>"
            f"TFR: <b>{row.TFR:.2f}</b> hijos/mujer<br>"
            f"LEx: <b>{row.LEx:.1f}</b> años<br>"
            f"Población: <b>{pop_m.iloc[i]:,.1f} M</b>"
            for i, (loc, iso, row) in enumerate(zip(c_df['Location'], c_df['ISO3_code'], c_df.itertuples()))
        ]

        scatter_trace = go.Scatter(
            x=c_df['TFR'],
            y=c_df['LEx'],
            mode='markers',
            name=cont,
            marker=dict(
                size=sizes,
                color=CONTINENT_COLORS[cont],
                opacity=0.84,
                line=dict(width=0.9, color='rgba(255,255,255,0.85)')
            ),
            text=hover_text,
            hoverinfo='text',
            visible=True if is_base else None
        )
        traces.append(scatter_trace)

    return traces


def create_tfr_vs_lex_animation(
    df: pd.DataFrame = None,
    output_html_path: Path | str = None
) -> go.Figure:
    """
    Construye la figura animada fluida de la Transición Demográfica (TFR vs LEx).
    """
    if df is None:
        df = load_demographic_data()

    years = sorted(df['Time'].unique())
    initial_year = years[0]

    # Trazas iniciales (1950)
    initial_df = df[df['Time'] == initial_year]
    initial_traces = _build_year_traces(initial_df, is_base=True)

    # Construcción de frames (1950..2023)
    frames = []
    for y in years:
        y_df = df[df['Time'] == y]
        y_traces = _build_year_traces(y_df, is_base=False)
        frames.append(go.Frame(data=y_traces, name=str(y)))

    # Control de Slider con transición suave sin redraw
    slider_steps = []
    for y in years:
        step = dict(
            method="animate",
            args=[
                [str(y)],
                dict(
                    mode="immediate",
                    frame=dict(duration=110, redraw=False),
                    transition=dict(duration=75, easing="linear")
                )
            ],
            label=str(y)
        )
        slider_steps.append(step)

    sliders = [dict(
        active=0,
        currentvalue=dict(
            prefix="<b>Año: </b>",
            font=dict(size=16, color="#1e293b"),
            visible=True,
            xanchor="center"
        ),
        pad=dict(t=50, b=10),
        len=0.92,
        x=0.04,
        y=-0.08,
        steps=slider_steps
    )]

    # Botones de Reproducción / Pausa (redraw=False para fluidez pura de 60fps)
    play_buttons = [dict(
        type="buttons",
        showactive=False,
        x=0.04,
        y=-0.17,
        xanchor="left",
        yanchor="top",
        direction="left",
        buttons=[
            dict(
                label="▶ Reproducir Transición Fluida (1950–2023)",
                method="animate",
                args=[
                    None,
                    dict(
                        frame=dict(duration=110, redraw=False),
                        transition=dict(duration=75, easing="linear"),
                        fromcurrent=True,
                        mode="immediate"
                    )
                ]
            ),
            dict(
                label="⏸ Pausa",
                method="animate",
                args=[
                    [None],
                    dict(
                        frame=dict(duration=0, redraw=False),
                        mode="immediate"
                    )
                ]
            )
        ]
    )]

    # Botones de Modo de Vista
    # Traces 0 y 1 = Capas Térmicas (Halo + Núcleo)
    # Traces 2 a 7 = Continentes (6 trazas)
    # Total = 8 trazas
    view_buttons = dict(
        type="buttons",
        direction="left",
        x=0.55,
        y=1.14,
        xanchor="center",
        yanchor="top",
        buttons=[
            dict(
                label="🔵 Puntos por Continente",
                method="update",
                args=[{"visible": [False, False, True, True, True, True, True, True]}]
            ),
            dict(
                label="🌋 Mapa de Calor / Nube Térmica",
                method="update",
                args=[{"visible": [True, True, False, False, False, False, False, False]}]
            ),
            dict(
                label="🔄 Ambos Superpuestos",
                method="update",
                args=[{"visible": [True, True, True, True, True, True, True, True]}]
            )
        ]
    )

    fig = go.Figure(data=initial_traces, frames=frames)

    # Configuración de diseño y layout
    fig.update_layout(
        title=dict(
            text="<b>Curva de Transición Demográfica Global: Fecundidad vs. Esperanza de Vida (1950–2023)</b><br>"
                 "<span style='font-size:12px; color:#64748b;'>"
                 "Evolución anual de 237 países y áreas. Alterna entre puntos, mapa de calor térmico o ambos con movimiento 100% fluido."
                 "</span>",
            x=0.04,
            y=0.96,
            xanchor="left"
        ),
        xaxis=dict(
            title="<b>Tasa Global de Fecundidad (TFR, hijos por mujer)</b>",
            range=[0.5, 9.2],
            dtick=1.0,
            showgrid=True,
            gridcolor="#e2e8f0",
            zeroline=False
        ),
        yaxis=dict(
            title="<b>Esperanza de Vida al Nacer (LEx, años)</b>",
            range=[15.0, 92.0],
            dtick=10.0,
            showgrid=True,
            gridcolor="#e2e8f0",
            zeroline=False
        ),
        template="plotly_white",
        width=1200,
        height=820,
        margin=dict(l=70, r=40, t=130, b=150),
        legend=dict(
            title=dict(text="<b>Continente</b>"),
            orientation="v",
            x=1.01,
            y=0.85,
            xanchor="left",
            bgcolor="rgba(255,255,255,0.85)",
            bordercolor="#cbd5e1",
            borderwidth=1
        ),
        updatemenus=[play_buttons[0], view_buttons],
        sliders=sliders
    )

    # Línea vertical fija: Umbral de Reemplazo Generacional (TFR = 2.1)
    fig.add_vline(
        x=2.1,
        line_width=1.8,
        line_dash="dash",
        line_color="#dc2626",
        annotation_text="<b>Nivel de Reemplazo (TFR = 2.1)</b>",
        annotation_position="top left",
        annotation_font=dict(size=11, color="#b91c1c")
    )

    # Línea horizontal de referencia: Longevidad 70 años
    fig.add_hline(
        y=70.0,
        line_width=1.2,
        line_dash="dot",
        line_color="#0284c7",
        annotation_text="LEx = 70 años",
        annotation_position="bottom right",
        annotation_font=dict(size=10, color="#0369a1")
    )

    # Anotaciones de cuadrante contextual
    fig.add_annotation(
        x=1.3, y=86.0,
        text="<b>Zona de Sub-reemplazo / Envejecimiento Avanzado</b><br>(TFR < 2.1 | LEx > 75 años)",
        showarrow=False,
        font=dict(size=10, color="#475569"),
        align="left",
        bgcolor="rgba(241,245,249,0.75)",
        bordercolor="#cbd5e1",
        borderwidth=1,
        borderpad=4
    )
    fig.add_annotation(
        x=7.5, y=28.0,
        text="<b>Régimen Pre-transición</b><br>(Alta Fecundidad | Alta Mortalidad)",
        showarrow=False,
        font=dict(size=10, color="#475569"),
        align="right",
        bgcolor="rgba(241,245,249,0.75)",
        bordercolor="#cbd5e1",
        borderwidth=1,
        borderpad=4
    )

    if output_html_path:
        out_p = Path(output_html_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        fig.write_html(str(out_p), include_plotlyjs="cdn")
        print(f"  [OK] Gráfico HTML guardado: {out_p}")

    return fig


if __name__ == "__main__":
    import sys
    if sys.stdout.encoding.lower() != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    base_dir = Path(__file__).resolve().parent.parent
    figures_dir = base_dir / "outputs" / "figures"
    final_dir = figures_dir / "final"

    print(">>> Regenerando Grafico 1 con Capas Térmicas Fluidas (Glow Vectorial + redraw=False)...")
    fig = create_tfr_vs_lex_animation(
        output_html_path=figures_dir / "01_tfr_vs_lex_animated.html"
    )
    fig.write_html(str(final_dir / "01_tfr_vs_lex_animated.html"), include_plotlyjs="cdn")
    print(f"  [OK] Copia guardada en final/: {final_dir / '01_tfr_vs_lex_animated.html'}")
    print("[OK] Grafico 1 100% fluido generado con exito.")
