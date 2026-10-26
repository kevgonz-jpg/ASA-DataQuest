# 🌍 ASA DataQuest 2026 — World Population Prospects 2024

> *¿Converge realmente la transición demográfica global, o emergen trayectorias divergentes?*

---

## 🏆 Categorías objetivo

| Categoría | Enfoque |
|---|---|
| 🎨 Best Data Visualization | Mapas, ridgeline, small multiples, Sankey |
| 🧠 Best Statistical Insight | Convergencia/divergencia, DTW clustering, change-points |
| ⚖️ Best Consideration of Ethics | ASA Guidelines integradas en cada fase |

## 📁 Estructura del proyecto (Medallion Architecture)

```
├── data/bronze/     → Datos crudos UN WPP2024 (inmutables)
├── data/silver/     → Datos limpios, filtrados, tipados
├── data/gold/       → Datasets analíticos listos para consumo
├── notebooks/       → Análisis paso a paso (00–07)
├── src/             → Código reutilizable (config, loaders, transforms, viz)
├── outputs/         → Figuras, tablas y reportes generados
├── docs/            → Documentación del concurso y metodología
└── decisions/       → Registro de decisiones analíticas
```

## 🚀 Quickstart

```bash
# 1. Clonar
git clone <repo-url>
cd "2026 ASA DataQuest"

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Descargar datos bronze (ver instrucciones abajo)

# 4. Ejecutar notebooks en orden (00 → 07)
```

## 📦 Datos

Los archivos `.gz` de bronze NO están en el repo (son pesados). Descárgalos de:
- [UN Population Division — WPP2024](https://population.un.org/wpp/Download/)

Colócalos en `data/bronze/`.

## 🔧 Requisitos

- Python 3.11+
- Ver `requirements.txt` para paquetes

## 📝 Reproducibilidad

- Seed fijo: `SEED = 42` (en `src/config.py`)
- Todas las decisiones analíticas documentadas en `decisions/decision_log.md`
- Separación explícita estimaciones (≤2023) vs proyecciones (≥2024)

## 📄 Licencia

MIT — Ver `LICENSE`

## 👤 Autor

Andres Pinto, Yuliana Guzman, Kevin Gonzalez— Universidad Nacional de Colombia, Sede Medellín
