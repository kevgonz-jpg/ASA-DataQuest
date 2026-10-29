"""
pca_trajectories.py — Espacio factorial PCA animado (1950–2023)

Una sola figura Plotly con slider/Play temporal y 4 vistas intercambiables:
  1. 2D: PC1 vs PC2   2. 2D: PC1 vs PC3   3. 2D: PC2 vs PC3   4. 3D: PC1, PC2, PC3
En cada año se muestran los países (puntos por continente) y el centroide
continental (mediana) con su estela histórica acumulada hasta ese año.
Un desplegable permite filtrar por continente (compatible con las 4 vistas).
"""

from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go

CONTINENT_COLORS = {
    'Africa': '#E69F00', 'Asia': '#56B4E9', 'Europe': '#009E73',
    'Latin America & Caribbean': '#D55E0D',
    'Northern America': '#0072B2', 'Oceania': '#CC79A7',
}
CONTINENT_ORDER = list(CONTINENT_COLORS)

PC_LABELS = {
    'PC1': 'PC1 · Transición demográfica (54.6%) — (+) fecundidad/mortalidad, (−) longevidad/envejecimiento',
    'PC2': 'PC2 · Migración y crecimiento (25.1%)',
    'PC3': 'PC3 · Brecha de género en longevidad (10.6%)',
}
# (nombre vista, ejes). 3 vistas 2D + 1 vista 3D
VIEWS = [
    ('2D · PC1 vs PC2', ('PC1', 'PC2')),
    ('2D · PC1 vs PC3', ('PC1', 'PC3')),
    ('2D · PC2 vs PC3', ('PC2', 'PC3')),
    ('3D · PC1, PC2, PC3', ('PC1', 'PC2', 'PC3')),
]
N_C = len(CONTINENT_ORDER)
TRACES_PER_VIEW = 2 * N_C  # 6 nubes de países + 6 centroides con estela


def load_profiles_data(parquet_path=None) -> pd.DataFrame:
    if parquet_path is None:
        base_dir = Path(__file__).resolve().parent.parent
        parquet_path = base_dir / 'data' / 'gold' / 'demographic_profiles.parquet'
    df = pd.read_parquet(parquet_path)
    if 'LocTypeID' in df.columns:
        df = df[df['LocTypeID'] == 4]
    return df[df['Time'] <= 2023].copy()


def create_pca_trajectories_figure(df: pd.DataFrame = None, output_html_path=None) -> go.Figure:
    if df is None:
        df = load_profiles_data()
    df = df.sort_values(['Time', 'Location'])
    years = sorted(df['Time'].unique())

    # Precómputos
    pts = {(y, c): g for (y, c), g in df.groupby(['Time', 'Continent'])}
    cent = df.groupby(['Continent', 'Time'])[['PC1', 'PC2', 'PC3']].median()
    rng = {}
    for pc in ('PC1', 'PC2', 'PC3'):
        lo, hi = df[pc].min(), df[pc].max()
        pad = 0.06 * (hi - lo)
        rng[pc] = [round(lo - pad, 2), round(hi + pad, 2)]

    def hover_tpl(axes):
        t = "<b>%{text}</b><br>" + "<br>".join(
            f"{a}: %{{{k}:.2f}}" for a, k in zip(axes, 'xyz'))
        return t + "<extra></extra>"

    def build_traces(year_idx, base=False):
        y = years[year_idx]
        traces = []
        for vname, axes in VIEWS:
            is3d = len(axes) == 3
            Sc = go.Scatter3d if is3d else go.Scatter
            for c in CONTINENT_ORDER:  # nubes de países en el año y
                g = pts.get((y, c))
                kw = {}
                if g is not None:
                    kw['x'] = np.round(g[axes[0]].values, 3)
                    kw['y'] = np.round(g[axes[1]].values, 3)
                    if is3d:
                        kw['z'] = np.round(g[axes[2]].values, 3)
                    kw['text'] = g['Location'].values
                else:
                    kw.update(x=[], y=[], text=[])
                    if is3d:
                        kw['z'] = []
                traces.append(Sc(
                    mode='markers', name=c,
                    marker=dict(size=4 if is3d else 8, color=CONTINENT_COLORS[c],
                                opacity=0.75, line=dict(width=0)),
                    hovertemplate=hover_tpl(axes), showlegend=False, **kw))
            for c in CONTINENT_ORDER:  # centroide + estela hasta el año y
                tr = cent.loc[c].loc[:y]
                kw = dict(x=np.round(tr[axes[0]].values, 3), y=np.round(tr[axes[1]].values, 3))
                if is3d:
                    kw['z'] = np.round(tr[axes[2]].values, 3)
                n = len(tr)
                sizes = [2] * (n - 1) + [13 if not is3d else 9]
                traces.append(Sc(
                    mode='lines+markers', name=f"Centroide {c}",
                    line=dict(color=CONTINENT_COLORS[c], width=5 if not is3d else 6),
                    marker=dict(size=sizes, color=CONTINENT_COLORS[c], symbol='diamond',
                                line=dict(width=1.5, color='#111827')),
                    text=[f"Centroide {c}"] * n,
                    hovertemplate=hover_tpl(axes), showlegend=False, **kw))
        if base:
            for i, t in enumerate(traces):
                t.visible = i < TRACES_PER_VIEW
        return traces

    # Leyenda (solo colores): trazas ficticias fuera de rango, siempre visibles
    legend_traces = [go.Scatter(x=[None], y=[None], mode='markers', name=c,
                                marker=dict(size=11, color=CONTINENT_COLORS[c]),
                                hoverinfo='skip') for c in CONTINENT_ORDER]

    base_traces = build_traces(0, base=True)
    n_main = len(base_traces)
    frames = [go.Frame(data=build_traces(i), name=str(y), traces=list(range(n_main)))
              for i, y in enumerate(years)]
    fig = go.Figure(data=base_traces + legend_traces, frames=frames)

    # ---------- vistas ----------
    def vis_for(v):
        return [(v * TRACES_PER_VIEW <= i < (v + 1) * TRACES_PER_VIEW) for i in range(n_main)] \
               + [True] * N_C

    view_buttons = []
    for v, (vname, axes) in enumerate(VIEWS):
        if len(axes) == 2:
            layout = {
                'xaxis.visible': True, 'yaxis.visible': True,
                'xaxis.range': rng[axes[0]], 'yaxis.range': rng[axes[1]],
                'xaxis.title.text': f"<b>{PC_LABELS[axes[0]]}</b>",
                'yaxis.title.text': f"<b>{PC_LABELS[axes[1]]}</b>",
                'scene.xaxis.visible': False, 'scene.yaxis.visible': False,
                'scene.zaxis.visible': False,
            }
        else:
            layout = {
                'xaxis.visible': False, 'yaxis.visible': False,
                'scene.xaxis.visible': True, 'scene.yaxis.visible': True,
                'scene.zaxis.visible': True,
            }
        view_buttons.append(dict(label=vname, method='update',
                                 args=[{'visible': vis_for(v)}, layout]))

    # ---------- filtro por continente (vía opacidad: compatible con las vistas) ----------
    idx_all = list(range(n_main))
    def cont_of(i):
        return CONTINENT_ORDER[(i % TRACES_PER_VIEW) % N_C]
    filter_buttons = [dict(label='Todos los continentes', method='restyle',
                           args=[{'opacity': [1.0] * n_main}, idx_all])]
    for c in CONTINENT_ORDER:
        filter_buttons.append(dict(
            label=c, method='restyle',
            args=[{'opacity': [1.0 if cont_of(i) == c else 0.0 for i in idx_all]}, idx_all]))

    # ---------- animación ----------
    # Se usa redraw=True (necesario para Scatter3d); cada frame es ligero.
    anim = dict(frame=dict(duration=140, redraw=True),
                transition=dict(duration=0), mode='immediate')
    steps = [dict(method='animate', label=str(y), args=[[str(y)], anim]) for y in years]
    sliders = [dict(active=0, steps=steps, x=0.04, y=-0.02, len=0.92,
                    pad=dict(t=40, b=10),
                    currentvalue=dict(prefix='<b>Año: </b>', font=dict(size=16)))]
    play = dict(type='buttons', showactive=False, direction='left',
                x=0.04, y=-0.12, xanchor='left', yanchor='top',
                buttons=[
                    dict(label='▶ Reproducir', method='animate',
                         args=[None, dict(frame=dict(duration=140, redraw=True),
                                          transition=dict(duration=0),
                                          fromcurrent=True, mode='immediate')]),
                    dict(label='⏸ Pausa', method='animate',
                         args=[[None], dict(frame=dict(duration=0, redraw=False),
                                            mode='immediate')])])

    fig.update_layout(
        title=dict(
            text="<b>Trayectorias demográficas en el espacio factorial PCA (1950–2023)</b><br>"
                 "<span style='font-size:12px;color:#64748b'>Puntos = países en el año seleccionado · "
                 "◆ = centroide continental (mediana) con su estela histórica · PC1+PC2+PC3 = 90.3% de la varianza</span>",
            x=0.04, xanchor='left'),
        template='plotly_white', width=1250, height=860,
        margin=dict(l=70, r=40, t=170, b=150),
        xaxis=dict(visible=True, range=rng['PC1'], title=f"<b>{PC_LABELS['PC1']}</b>",
                   zeroline=True, gridcolor='#e2e8f0'),
        yaxis=dict(visible=True, range=rng['PC2'], title=f"<b>{PC_LABELS['PC2']}</b>",
                   zeroline=True, gridcolor='#e2e8f0'),
        scene=dict(
            xaxis=dict(visible=False, range=rng['PC1'], title=PC_LABELS['PC1'].split(' (')[0]),
            yaxis=dict(visible=False, range=rng['PC2'], title=PC_LABELS['PC2'].split(' (')[0]),
            zaxis=dict(visible=False, range=rng['PC3'], title=PC_LABELS['PC3'].split(' (')[0]),
            camera=dict(eye=dict(x=1.7, y=1.7, z=1.2)),
            aspectmode='cube'),
        legend=dict(title=dict(text='<b>Continente</b>'), x=1.01, y=0.8,
                    itemclick=False, itemdoubleclick=False),
        updatemenus=[
            dict(type='buttons', direction='left', buttons=view_buttons, active=0,
                 x=0.04, y=1.12, xanchor='left', yanchor='top'),
            dict(type='dropdown', direction='down', buttons=filter_buttons,
                 x=0.04, y=1.03, xanchor='left', yanchor='top'),
            play,
        ],
        sliders=sliders,
    )

    if output_html_path:
        out_p = Path(output_html_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        fig.write_html(str(out_p), include_plotlyjs='cdn')
        print(f"  [OK] Gráfico HTML guardado: {out_p}")
    return fig


if __name__ == "__main__":
    import sys
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    base_dir = Path(__file__).resolve().parent.parent
    figures_dir = base_dir / "outputs" / "figures"
    final_dir = figures_dir / "final"
    final_dir.mkdir(parents=True, exist_ok=True)
    print(">>> Generando Grafico 2: PCA animado (3 vistas 2D + 3D)...")
    fig = create_pca_trajectories_figure(output_html_path=figures_dir / "02_pca_trajectories_2d_3d.html")
    fig.write_html(str(final_dir / "02_pca_trajectories_2d_3d.html"), include_plotlyjs="cdn")
    print("[OK] Grafico 2 generado.")
