# ASA DataQuest 2026 -- World Population Prospects 2024

> Investigacion cuantitativa sobre la divergencia en la transicion demografica global, el Indice de Madurez Demografica (ICD) y el modelado predictivo de transicion de regimen al 2050.

---

## Categorias Objetivo del Concurso

| Categoria | Enfoque Metodologico |
|---|---|
| Best Statistical Insight | Indice de Madurez Demografica (ICD), clustering de regimenes K=4 y modelado predictivo supervisado (Random Forest, SVM, Multinomial Logistic) de transicion al 2050. |
| Best Consideration of Ethics | Checklist formal ASA Ethical Guidelines (10 principios), auditoria de limitaciones, mitigacion de sesgos en etiquetado demografico y reporte ejecutivo. |
| Data Quality & Pipeline | Arquitectura Medallion (Bronze -> Silver -> Gold), validacion de schema, reproducibilidad integral (SEED = 42) y registro auditable de decisiones. |

---

## Flujo de Trabajo y Notebooks

El proyecto sigue una secuencia metodologica modular:

1. **`notebooks/00_setup_and_validation.ipynb`**: Verificacion del entorno, dependencias de software y comprobacion de integridad de datos Bronze.
2. **`notebooks/01_bronze_to_silver.ipynb`**: Limpieza, tipado Parquet, filtrado estricto por `LocTypeID == 4`, separacion entre estimaciones (<=2023) y proyecciones (>=2024) y creacion de variables derivadas (`GenderGapLE`, `NaturalGrowth`, `Epoch`).
3. **`notebooks/02_eda_univariate.ipynb`**: Diagnostico de asimetria y no normalidad (Shapiro-Wilk), retencion de atipicos historicos y evaluacion de transformaciones robustas.
4. **`notebooks/03_eda_bivariate.ipynb`**: Embudo de colinealidad de Spearman, seleccion de pilares ortogonales y analisis del espacio de fase demografico.
5. **`notebooks/04_eda_multivariate.ipynb`**: Transformacion logaritmica, PCA sobre matriz de correlaciones, construccion del **Indice de Madurez Demografica (ICD)** con Winsorizacion robusta P2.5 - P97.5 y clasificacion en 4 regimenes demograficos estructurales ($K=4$).
6. **`notebooks/05_statistical_insight.ipynb`**: Formulacion del modelo predictivo supervisado de transicion de regimen al 2050 ($P(\text{Regimen}_{2050} \mid \text{ICD}_{2023}, \mathbf{x}_{2023})$), benchmarking de 5 familias algoritmicas, explicabilidad con Random Forest (ICD lidera con 18.9% de importancia), umbral critico en $\text{ICD} = 52.0$ y cuantificacion de riesgo de estancamiento pre-transicional.
7. **`notebooks/07_ethics_and_report.ipynb`**: Checklist formal de directrices eticas ASA, auditoria de limitaciones tecnicas y dilemas de etiquetado demografico, consolidacion del log de decisiones y generacion automatizada del reporte ejecutivo final (`outputs/reports/final_demographic_report.md`).

---

## Estructura del Repositorio (Medallion Architecture)

```
├── data/
│   ├── bronze/      <- Datos crudos UN WPP2024 (inmutables, no versionados en git)
│   ├── silver/      <- Datos limpios, filtrados y tipados en Parquet
│   └── gold/        <- Tablas analiticas finales, indices y predicciones
├── notebooks/       <- Notebooks reproducibles paso a paso (00 a 05, y 07)
├── src/             <- Modulos reutilizables de configuracion, carga, transformacion y visualizacion
├── outputs/         <- Figuras a 300 DPI, tablas Parquet y reportes consolidados
├── decisions/       <- Registro formal de decisiones analiticas (decision_log.md)
└── docs/            <- Documentacion metodologica de la competencia
```

---

## Reproducibilidad

- **Semilla fija global**: `SEED = 42` (configurada en `src/config.py`).
- **Trazabilidad**: Cada eleccion metodologica se encuentra justificada en `decisions/decision_log.md`.
- **Ejecucion secuencial**: Ejecutar los notebooks en orden estricto del 00 al 05, y finalmente el 07.

---

## Autores

Pregrado en Estadistica -- Universidad Nacional de Colombia, Sede Medellin.
Competencia: ASA DataQuest 2026.
