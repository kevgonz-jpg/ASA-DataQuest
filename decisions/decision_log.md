# Decision Log — ASA DataQuest 2026

> Registro de decisiones analiticas del proyecto.  
> Cada entrada documenta QUE se decidio, POR QUE y su justificacion estadistica y metodologica, vinculada a su notebook correspondiente.

---

## Formato de entrada

```
### [Notebook] — [Titulo de la decision]
- **Notebook**: [nombre_del_notebook.ipynb](ruta)
- **Contexto**: ¿Que problema o pregunta motivo esta decision?
- **Decision**: ¿Que se decidio hacer?
- **Justificacion**: ¿Por que? (estadistica, metodologica, practica)
- **Alternativas descartadas**: ¿Que otras opciones se consideraron?
```

---

## Decisiones

### Notebook 01 — Filtrar por LocTypeID == 4 para analisis de paises

- **Notebook**: [01_bronze_to_silver.ipynb](../notebooks/01_bronze_to_silver.ipynb)
- **Contexto**: El dataset incluye 9 tipos de localizacion (paises, regiones, grupos de ingreso, etc.). Agregar sin filtrar produce doble conteo de poblacion.
- **Decision**: Filtrar `LocTypeID == 4` (Country/Area) como base principal del analisis.
- **Justificacion**: Evitar doble conteo es un requisito de integridad de datos. Las agregaciones regionales se usaran solo para comparacion contextual.
- **Alternativas descartadas**: Usar todas las localizaciones (descartado por doble conteo).

### Notebook 01 — Distincion politica y conceptual: Paises soberanos vs Localidades/Territorios dependientes

- **Notebook**: [01_bronze_to_silver.ipynb](../notebooks/01_bronze_to_silver.ipynb)
- **Contexto**: El filtrado por `LocTypeID == 4` (`Country/Area`) arroja 237 entidades territoriales, pero internacionalmente solo existen 195 Estados soberanos (193 miembros ONU + 2 observadores: Santa Sede y Palestina). Tratar indiscriminadamente a todas como "paises" introduce inexactitudes geopoliticas.
- **Decision**:
    1. Identificar y auditar formalmente las 42 entidades que corresponden a dependencias, territorios de ultramar o regiones administrativas especiales (ej. Puerto Rico, Groenlandia, Hong Kong, Guayana Francesa, Bermudas).
    2. Adoptar a lo largo del proyecto y los reportes la terminologia oficial de la ONU: **"Paises y Areas"** (o **"Localidades"**), evitando referirse a las 237 unidades como "paises soberanos".
    3. Conservar las 42 entidades en la capa Silver por su valor demografico autonomo, previendo que en fases posteriores (EDA e Indice Compuesto) podran filtrarse por soberania o por umbral de tamano poblacional para evitar distorsiones causadas por microterritorios.
- **Justificacion**: Preserva el rigor conceptual y academico del informe ante los evaluadores, previene afirmaciones erroneas sobre el numero de paises en el mundo y transparenta el alcance del dataset.
- **Alternativas descartadas**: Tratar todas las entidades como paises sin distincion; eliminar de forma precipitada las 42 dependencias en la capa Silver sin evaluar antes su relevancia demografica.

### Notebook 01 — Separar estimaciones (<=2023) de proyecciones (>=2024)

- **Notebook**: [01_bronze_to_silver.ipynb](../notebooks/01_bronze_to_silver.ipynb)
- **Contexto**: El dataset mezcla datos estimados a partir de censos con proyecciones basadas en modelos estadisticos. Tienen niveles de incertidumbre radicalmente distintos.
- **Decision**: Crear una columna `IsEstimate` y marcar explicitamente la separacion en todos los analisis y visualizaciones.
- **Justificacion**: Transparencia sobre la naturaleza de los datos. Presentar proyecciones como datos observados seria engañoso.
- **Alternativas descartadas**: Tratar todo como "datos" sin distincion.

### Notebook 01 — Auditoria de completitud, tratamiento de nulos y exclusion de DoublingTime

- **Notebook**: [01_bronze_to_silver.ipynb](../notebooks/01_bronze_to_silver.ipynb)
- **Contexto**: La auditoria de calidad sobre las 17.538 observaciones historicas (1950–2023) identifico que 68 de 76 variables tienen 100% de completitud. Los unicos valores nulos detectados se concentran en: `Notes` (campo textual no numerico), `DoublingTime` (3.601 nulos = 20.53%), `ISO2_code` (74 nulos = 0.42%) y las variables del suplemento (`BirthsMale`, `BirthsFemale`, `LE60`, 74 nulos = 0.42%).
- **Decision**:
    1. **Excluir `DoublingTime` del indice compuesto**: No responde a un error sino a una indeterminacion matematica ($T_d = \ln(2)/r$ solo existe si $r > 0$). En poblaciones con decrecimiento o estancamiento, la poblacion no se duplica y la ONU asigna `NaN`. Para evitar perder artificialmente el 20% de los paises/anos (especialmente en Europa y Asia oriental), se adopta **`PopGrowthRate`** como metrica continua y completa (0% nulos).
    2. **Imputar `"NA"` en `ISO2_code`**: Corregir el falso nulo de Namibia (`LocID == 516`), originado por la conversion automatica de la cadena `"NA"` a valor faltante por los lectores de datos.
    3. **Documentar exclusion de la Santa Sede (`LocID == 336`) en el indice**: Es el unico estado sin registros en el suplemento debido a su demografia clerical sin nacimientos locales. Se delimita su exclusion en el calculo multivariado para evitar sesgos por microestados atipicos.
- **Justificacion**: Garantiza maxima integridad muestral sin imputaciones estadisticamente invalidas, preserva identificadores estandar y sustenta la exclusion de variables y casos extremos con rigor demografico.
- **Alternativas descartadas**: Eliminar filas con `DoublingTime` nulo (sesga la muestra al excluir paises en declive); imputar valores sinteticos a `DoublingTime` o a la natalidad del Vaticano; dejar a Namibia sin codigo ISO2.

### Notebook 01 — Creacion de variables derivadas (GenderGapLE, IsEstimate, Epoch, NaturalGrowth)

- **Notebook**: [01_bronze_to_silver.ipynb](../notebooks/01_bronze_to_silver.ipynb)
- **Contexto**: El dataset crudo contiene indicadores brutos aislados y una variable de tiempo anual continua, pero carece de metricas sinteticas para evaluar brechas de equidad en supervivencia, dinamica vegetativa pura y agregacion por etapas historicas.
- **Decision**: Incorporar en la capa Silver cuatro variables derivadas clave:
    1. `GenderGapLE` ($\text{LExFemale} - \text{LExMale}$): Metrica directa de brecha de genero en longevidad. Permite evaluar equidad en salud, sobremortalidad masculina adulta o desatencion sanitaria materna.
    2. `NaturalGrowth` ($\text{CBR} - \text{CDR}$): Tasa de crecimiento natural por 1.000 habitantes. Separa el componente reproductivo interno de las fluctuaciones migratorias (`CNMR`).
    3. `IsEstimate`: Booleano explicito que distingue estimaciones historicas con base empirica ($\le 2023$) de modelos y proyecciones matematicas ($\ge 2024$).
    4. `Epoch`: Agrupamiento ordinal en periodos historicos y futuros (`1950-1979`, `1980-1999`, `2000-2023`, `2024-2049`, `2050-2100`) para analizar trayectorias de transicion demografica sin fragmentar el analisis ano a ano.
- **Justificacion**: Dota al proyecto de dimensiones directamente aplicables a la construccion del indice compuesto, reduce la necesidad de recalcular variables en cada notebook y salvaguarda la transparencia metodologica al diferenciar datos retrospectivos de escenarios simulados.
- **Alternativas descartadas**: Calcular features de manera dispersa y redundante en cada notebook de analisis; omitir la marcacion explicita de datos observados frente a proyecciones.

### Notebook 01 — Usar formato Parquet para Silver/Gold

- **Notebook**: [01_bronze_to_silver.ipynb](../notebooks/01_bronze_to_silver.ipynb)
- **Contexto**: CSV es legible pero ineficiente para datasets de >30K filas con tipos mixtos.
- **Decision**: Silver y Gold se guardan en `.parquet` (con pyarrow).
- **Justificacion**: Preserva tipos de datos (int vs float vs string), compresion eficiente, lectura ~10x mas rapida.
- **Alternativas descartadas**: CSV (pierde tipos), Feather (menos portable).

### Notebook 01 / EDA — Pregunta central y filtro de seleccion de variables para el Indice Compuesto

- **Notebook**: [01_bronze_to_silver.ipynb](../notebooks/01_bronze_to_silver.ipynb) (conexion hacia [02_eda_univariate.ipynb](../notebooks/02_eda_univariate.ipynb) a [05_statistical_insight.ipynb](../notebooks/05_statistical_insight.ipynb))
- **Contexto**: Se adopta formalmente la pregunta central: "Indice compuesto: ¿Como podria sintetizar multiples indicadores demograficos en una metrica unica del perfil demografico de un pais, y que elecciones metodologicas exige justificar?". El dataset Bronze contiene 67 variables, incluyendo magnitudes absolutas dependientes del tamaño poblacional y medidas redundantes.
- **Decision**: En la capa Silver se preserva el universo completo de paises (`LocTypeID == 4`) y se integran los nacimientos por sexo y sobrevida geriatrica (`LE60`). La reduccion de variables se traslada formalmente al EDA mediante un embudo metodologico: filtro conceptual de 4 pilares (tasas relativas en univariado), descarte por colinealidad extrema ($r > 0.90$ en bivariado) y validacion factorial (PCA en multivariado).
- **Justificacion**: Prevenir el descarte prematuro o arbitrario de variables en la capa de datos. Cada exclusion debe sustentarse en evidencia empirica y quedar registrada como decision metodologica justificable.
- **Alternativas descartadas**: Filtrar columnas a priori en la capa Silver sin sustento cuantitativo previo.

### Notebook 02 / EDA — Normalizacion robusta y retencion de valores atipicos historicos

- **Notebook**: [02_eda_univariate.ipynb](../notebooks/02_eda_univariate.ipynb)
- **Contexto**: Las variables candidatas rechazan la normalidad estadistica (Shapiro-Wilk $p < 0.001$) y presentan asimetrias severas (ej. `IMR` asimetria > +2.0, `TFR` > +1.0). Asimismo, existen eventos de mortalidad extrema (Camboya 1977-1979, Ruanda 1994) y fecundidades ultrabajas (Corea del Sur 2023).
- **Decision**: Descartar estandarizacion clasica Z-score (media y desviacion estandar). Retener los outliers historicos por tratarse de fenomenos veridicos y aplicar metodos de escalamiento robustos (transformacion logaritmica en `IMR`/`TFR` o normalizacion Min-Max sobre percentiles 1-99).
- **Justificacion**: El Z-score clasico distorsiona variables asimetricas con colas pesadas. Preservar los eventos historicos mantiene la validez del storytelling sin deformar la escala del indice.
- **Alternativas descartadas**: Eliminar paises con valores atipicos; asumir distribuciones normales.

### Notebook 03 / EDA — Filtro de colinealidad bivariada y seleccion de pilares

- **Notebook**: [03_eda_bivariate.ipynb](../notebooks/03_eda_bivariate.ipynb)
- **Contexto**: Varios indicadores demograficos presentan redundancia severa ($|\rho| > 0.90$), lo que sobredimensionaria ciertos pilares dentro del indice compuesto.
- **Decision**: Reducir dimensionalidad aplicando un filtro de colinealidad de Spearman:
    1. **Fecundidad**: Conservar `TFR` y excluir `CBR` ($\rho = 0.98$). `TFR` es independiente de la piramide de edades.
    2. **Mortalidad Temprana**: Conservar `IMR` y excluir `Q5` ($\rho = 1.00$). `IMR` es la metrica canonica internacional.
    3. **Longevidad y Vejez**: Conservar `LEx` y evaluar `LE60` para capturar supervivencia global frente a vejez.
    4. **Estructura y Migracion**: Conservar `MedianAgePop` (divergencia regional clave, $\rho = 0.78$ con `LEx`) y `CNMR` (dimension migratoria ortogonal, $|\rho| < 0.20$).
    5. **Equidad**: Conservar `GenderGapLE` como dimension directa de brecha de genero en supervivencia.
- **Justificacion**: Elimina el doble conteo de varianza en el PCA/indice y asegura interpretabilidad de cada dimension del perfil demografico.
- **Alternativas descartadas**: Incluir todos los indicadores en el PCA sin descarte previo; utilizar filtros lineales de Pearson sobre datos con relaciones no lineales.

### Notebook 04 / EDA Multivariado -- Escalamiento robusto con transformacion logaritmica

- **Notebook**: [04_eda_multivariate.ipynb](../notebooks/04_eda_multivariate.ipynb)
- **Contexto**: Las variables `IMR` (asimetria > +2.0) y `TFR` (asimetria > +1.0) presentan distribuciones severamente asimétricas en el corte 2023 y ninguna variable pasa el test de normalidad (Shapiro-Wilk $p < 0.001$).
- **Decision**: Aplicar transformacion logaritmica a `IMR` (`log(IMR+1)`) y `TFR` (`log(TFR)`) previo al escalamiento. Usar `RobustScaler` (mediana y rango intercuartilico) en lugar de `StandardScaler`.
- **Justificacion**: La transformacion log reduce la asimetria sin eliminar la varianza informativa. `RobustScaler` no distorsiona la posicion de los outliers historicos retenidos en el Notebook 02.
- **Alternativas descartadas**: `StandardScaler` (asume normalidad); Min-Max sin transformacion (sensible a extremos); no transformar (sesga PC1).

### Notebook 04 / EDA Multivariado -- Ponderacion endogena del Indice Compuesto Demografico (ICD)

- **Notebook**: [04_eda_multivariate.ipynb](../notebooks/04_eda_multivariate.ipynb)
- **Contexto**: La construccion de un indice compuesto requiere asignar pesos a los indicadores. Las opciones incluyen pesos iguales (arbitrario), pesos de experto (subjetivo) o pesos derivados de PCA (endogeno/basado en datos).
- **Decision**: Ponderar las componentes principales retenidas (>= 80% varianza acumulada) por su proporcion de varianza explicada y normalizar el indice a escala 0-100.
- **Justificacion**: La ponderacion endogena elimina decisiones subjetivas sobre la importancia relativa de cada pilar. El PCA asigna mayor peso a las dimensiones con mayor dispersion real entre paises, lo que maximiza el poder discriminante del indice.
- **Alternativas descartadas**: Pesos iguales (ignora la estructura de covarianza); pesos de experto (no reproducibles).

### Notebook 04 / EDA Multivariado -- Sustitucion de Min-Max ingenuo por Estandarizacion Robusta de Percentiles (Winsorizacion P2.5 - P97.5) en el ICD

- **Notebook**: [04_eda_multivariate.ipynb](../notebooks/04_eda_multivariate.ipynb)
- **Contexto**: El calculo inicial del ICD acotaba el indice crudo (`raw_index`) a escala $[0, 100]$ mediante reescalamiento Min-Max clasico ($\frac{x - x_{\min}}{x_{\max} - x_{\min}}$). La auditoria de distribucion revelo que `raw_index` rechaza categoricamente la normalidad (Jarque-Bera $p < 10^{-100}$), presentando una distribucion leptocurtica con colas pesadas (curtosis $> 9.4$) y asimetria pronunciada causada por choques migratorios y microterritorios insulares. El Min-Max ingenuo basa su denominador exclusivamente en los estadisticos de orden extremos $X_{(1)}$ y $X_{(n)}$, colapsando la varianza util del 95% central de los paises en una franja artificialmente estrecha y anulando el poder discriminante del indice.
- **Decision**:
    1. Sustituir el Min-Max ingenuo por una **Estandarizacion Robusta con Winsorizacion de percentiles ($P_{2.5} - P_{97.5}$)** siguiendo las directrices de la OCDE/JRC (*Handbook on Constructing Composite Indicators*):
       $$\text{ICD}_i = 100 \times \operatorname{clip}\left(\frac{\text{raw}_i - P_{2.5}}{P_{97.5} - P_{2.5}}, 0, 1\right)$$
    2. Alinear la orientacion de cada componente principal retenida con el vector de longevidad (`LEx`), asegurando validez de constructo en la agregacion lineal ponderada.
- **Justificacion**: 
    1. *Preservacion de la metrica cardinal*: A diferencia de transformaciones sigmoides no lineales o rangos percentiles (ECDF), la Winsorizacion lineal mantiene inalterada la distancia proporcional entre naciones a lo largo del 95% central del espectro demografico (una diferencia de 1 punto refleja exactamente la misma magnitud relativa).
    2. *Inmunidad ante atipicos de cola*: Acota el impacto de anomalias extremas transitorias o de microestados en los extremos absolutos (0 y 100), impidiendo que distorsionen el benchmark global.
    3. *Estandar internacional*: Cumple rigurosamente las pautas metodologicas recomendadas por la OCDE y Naciones Unidas para indices sinteticos con variables asimetricas.
- **Alternativas descartadas**:
    - *Min-Max ingenuo global*: Descartado por hiper-sensibilidad a outliers y perdida masiva de resolucion analitica en el cuerpo central de la distribucion.
    - *Transformacion Sigmoide Robusta*: Descartada porque introduce no-linealidad en la escala, alterando la interpretacion de distancias fijas en los extremos.
    - *Percentile Rank / ECDF*: Descartado porque fuerza una distribucion uniforme artificial, destruyendo las distancias cuantitativas reales entre paises contiguos.

### Notebook 04 / EDA Multivariado -- Determinacion de regimenes demograficos por clustering

- **Notebook**: [04_eda_multivariate.ipynb](../notebooks/04_eda_multivariate.ipynb)
- **Contexto**: Identificar regimenes demograficos estructuralmente distintos permite segmentar los analisis del Notebook 05 y validar la coherencia del ICD.
- **Decision**: Aplicar K-Means sobre los scores de PCA retenidos, seleccionando K por maximo coeficiente de silueta en el rango [2, 8].
- **Justificacion**: K-Means es interpretable, escalable y adecuado para clusters de forma convexa. El coeficiente de silueta cuantifica la separabilidad y cohesion de los grupos sin requerir supuestos distribucionales.
- **Alternativas descartadas**: Clustering jerarquico (mas costoso, menos interpretable para n > 200); DBSCAN (sensible a parametros epsilon/min_samples en dimensiones altas).

### Notebook 05 / Statistical Insight -- Evaluacion morfologica de trayectorias con DTW bivariado

- **Notebook**: [05_statistical_insight.ipynb](../notebooks/05_statistical_insight.ipynb)
- **Contexto**: Evaluar si todos los paises recorren la misma trayectoria en el espacio de fase $(TFR, LEx)$ requiere comparar series temporales sin penalizar desfasajes cronologicos.
- **Decision**: Implementar Dynamic Time Warping (DTW) bivariado sobre trayectorias quinquenales normalizadas en escala $[0, 1]$, seguido de clustering jerarquico con metodo `complete linkage`.
- **Justificacion**: DTW mide la disimilaridad morfologica independientemente del anio de inicio de la transicion. El muestreo quinquenal reduce el costo computacional de 500s a 24s para las 27,966 parejas sin perder fidelidad analitica. Complete linkage evita el efecto de encadenamiento espurio (*chaining*) propio de single linkage.
- **Alternativas descartadas**: Distancia euclidiana directa (penaliza calendarios distintos como si fueran trayectorias distintas); correlacion cruzada simple (asume retardos lineales uniformes).

### Notebook 05 / Statistical Insight -- Deteccion de quiebres estructurales por regresion segmentada

- **Notebook**: [05_statistical_insight.ipynb](../notebooks/05_statistical_insight.ipynb)
- **Contexto**: Determinar si las transiciones son suaves o estan pautadas por perturbaciones no lineales y aceleraciones exogenas.
- **Decision**: Implementar regresion lineal segmentada en dos tramos (metodologia Chow / Bai-Perron con barrido exhaustivo de puntos de corte con segmento minimo $h=8$) para identificar el anio de maxima reduccion de varianza residual en $TFR$ y $LEx$.
- **Justificacion**: Permite datar formalmente las discontinuidades macroestructurales (reformas de politicas de poblacion, shocks epidemicos, guerras o colapsos geopoliticos) con fundamento estadistico basado en el estadistico $F$.
- **Alternativas descartadas**: CUSUM recursivo generico sin fechado puntual optimo; deteccion puramente heuristica o visual.

### Notebook 05 / Statistical Insight -- Experimento contrafactual de compensacion migratoria

- **Notebook**: [05_statistical_insight.ipynb](../notebooks/05_statistical_insight.ipynb)
- **Contexto**: Cuantificar si la migracion internacional compensa el envejecimiento poblacional en las economias avanzadas receptoras.
- **Decision**: Comparar la variante oficial `Zero migration` (fronteras netas neutras) con la variante `Medium` a los horizontes 2050 y 2100 para evaluar la variacion neta en edad mediana ($\Delta \text{MedianAge}$) y tamano de poblacion.
- **Justificacion**: Utiliza un contrafactual oficial estandarizado de Naciones Unidas que aisla exclusivamente el componente migratorio manteniendo constantes los supuestos de fertilidad y mortalidad.
- **Alternativas descartadas**: Regresion ecologica cross-section entre migracion y edad promedio (sujeta a confusion endogena y causalidad reversa); modelos ad-hoc sin base de proyeccion WPP.

### Notebook 06 / Visualizaciones Finales -- Sistema grafico bajo principios de Tufte y accesibilidad

- **Notebook**: [06_visualizations.ipynb](../notebooks/06_visualizations.ipynb)
- **Contexto**: Las figuras finales deben cumplir con estandares competitivos para concurso y rigor de publicacion cientifica.
- **Decision**: Maximizar el data-ink ratio eliminando marcos y elementos ornamentales; utilizar paletas perceptualmente uniformes y accesibles para daltonismo (`viridis`, `Blues`, `RdBu_r`); exportar estricto a 300 DPI con `bbox_inches='tight'`.
- **Justificacion**: Garantiza legibilidad universal, contraste optimizado para impresion y reproduccion digital, y foco directo en los patrones empiricos.
- **Alternativas descartadas**: Paletas por defecto no contrastadas; visualizaciones 3D con oclusion perceptiva.

### Notebook 07 / Etica y Reporte Final -- Marco etico ASA y contextualizacion no alarmista

- **Notebook**: [07_ethics_and_report.ipynb](../notebooks/07_ethics_and_report.ipynb)
- **Contexto**: Las estadisticas demograficas de fertilidad, mortalidad y migracion conllevan riesgos de instrumentalizacion politica, estigmatizacion territorial y discursos coercitivos.
- **Decision**: Adoptar explicitamente las *ASA Ethical Guidelines for Statistical Practice* como marco de control de calidad; contextualizar las proyecciones de envejecimiento y descenso de fecundidad sin apelar a retoricas de panico (\"declive poblacional\" o \"invierno demografico\"); fundamentar las recomendaciones en derechos reproductivos, salud universal y equidad distributiva.
- **Justificacion**: Garantiza que los hallazgos cientificos no sean descontextualizados y cumplan con la responsabilidad social y etica exigida en la practica estadistica profesional.
- **Alternativas descartadas**: Tratamiento puramente actuarial desprovisto de marco etico; presentacion de proyecciones como certezas deterministas sin explicitacion de incertidumbre.

---

*Agrega nuevas decisiones al final, manteniendo el formato.*