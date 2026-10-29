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

---

### Notebook 03 — Filtro de colinealidad extrema (Spearman |rho| > 0.90) para el Indice Compuesto

- **Notebook**: [03_eda_bivariate.ipynb](../notebooks/03_eda_bivariate.ipynb)
- **Contexto**: El calculo de un indice multivariado mediante PCA o ponderaciones objetivas se distorsiona ante redundancias severas de variables que miden el mismo fenomeno demografico subyacente.
- **Decision**: 
    1. **Conservar `TFR` y descartar `CBR`** ($\rho = +0.98$): `TFR` es la medida canonica independiente de la estructura etaria, mientras que `CBR` esta sesgada por la juventud o envejecimiento de la poblacion.
    2. **Conservar `IMR` y descartar `Q5`** ($\rho = +1.00$): La mortalidad en menores de 1 ano y menores de 5 anos tienen correlacion casi perfecta. Se conserva `IMR` por ser el indicador prioritario de salud publica en los ODS.
    3. **Preservar `CNMR` como dimension autonoma**: Se evidencio que la tasa neta de migracion tiene correlaciones minimas con las variables vegetativas ($|\rho| < 0.20$), confirmando su papel como vector independiente y amortiguador demografico.
- **Justificacion**: Garantiza parsimonia y estabilidad numerica en la descomposicion factorial (Notebook 04), previniendo sobreponderacion artificial del pilar reproductivo o de mortalidad infantil.
- **Alternativas descartadas**: Conservar todas las variables candidatas sin filtrado (infla la varianza del primer componente con redundancias); usar correlacion de Pearson (invalida por la asimetria y colas pesadas de las tasas).

---

### Notebook 04 — Construccion del Indice de Transicion Demografica (DTI) via PCA y Min-Max [0, 100]

- **Notebook**: [04_eda_multivariate.ipynb](../notebooks/04_eda_multivariate.ipynb)
- **Contexto**: Responder a la Pregunta Guia #5 requeria sintetizar los indicadores depurados en una metrica unica, objetiva y reproducible, evitando ponderaciones ad hoc o arbitrarias.
- **Decision**: 
    1. **Extraer ponderaciones mediante PCA**: El primer componente ($PC1$) explica el **54.58% de la varianza total** de los 7 indicadores seleccionados. Sus cargas agrupan naturalmente el eje clásico de supervivencia (`LEx`, `MedianAgePop`) frente a mortalidad y fecundidad pre-transición (`IMR`, `TFR`).
    2. **Inversion de signo y normalizacion Min-Max [0, 100]**: Se invirtio el signo de $PC1$ ($\text{DTI}^* = -PC1$) para que mayores puntuaciones reflejen mayor madurez en salud y supervivencia, escalando el rango a $[0, 100]$.
    3. **Preservar $PC2$ (25.12% de varianza)**: Se mantuvo como eje ortogonal de Dinámica Externa / Migración (`CNMR`, `PopGrowthRate`) para construir el espacio bidimensional de regímenes demográficos.
- **Justificacion**: Garantiza total fundamentación matemática (79.7% de varianza acumulada en 2 componentes) y máxima interpretabilidad para los evaluadores y formuladores de políticas.
- **Alternativas descartadas**: Promedio aritmético no ponderado (asume varianzas iguales); fijación subjetiva de pesos (sesgo ético).

### Notebook 04 — Segmentacion de Regimenes Demograficos con K-Means (K = 4)

- **Notebook**: [04_eda_multivariate.ipynb](../notebooks/04_eda_multivariate.ipynb)
- **Contexto**: Responder a la Pregunta Guia #6 requeria agrupar a los paises en perfiles demograficos distintivos segun como interactuan sus dimensiones conjuntas.
- **Decision**: Seleccionar $K=4$ regímenes globales mediante análisis conjunto de inercia (codo) y coeficiente de silueta:
    - *Regimen 1: Transicion Incipiente* (África subsahariana: $TFR > 4.2$, edad mediana $<20$ años).
    - *Regimen 2: Transicion Media / Emergente* (América Latina y Asia emergente: fertilidad cercana a reemplazo, longevidad moderada).
    - *Regimen 3: Alta Inmigracion / Expansion Externa* (Economías del Golfo y receptores netos con $CNMR > 10$).
    - *Regimen 4: Post-Transicion Avanzada / Envejecida* (Europa y Asia oriental: $LEx > 80$ años, $TFR < 1.4$, edad mediana $>42$ años).
- **Justificacion**: $K=4$ ofrece la mejor separabilidad cualitativa y cuantitativa, capturando tanto los estadios de transición clásica como la anomalía contemporánea de flujos migratorios externos.
- **Alternativas descartadas**: $K=2$ (excesivamente simplista, borra a las economías emergentes); $K \ge 6$ (fragmenta micro-variaciones sin sustento macroeconómico).

---

### Notebook 05 — Agrupamiento Morfologico de Trayectorias con Dynamic Time Warping (DTW) y Ward Linkage

- **Notebook**: [05_statistical_insight.ipynb](../notebooks/05_statistical_insight.ipynb)
- **Contexto**: Evaluar la hipótesis de convergencia requería comparar cómo evolucionan las series demográficas en el tiempo, considerando que las naciones no inician su transición simultáneamente.
- **Decision**: 
    1. **Adoptar DTW sobre la distancia Euclidiana**: Emplear alineamiento elástico temporal ($L_1$-norm) sobre la trayectoria longitudinal del $DTI$ (1950–2023) para agrupar países por la *forma y aceleración* de su transición demográfica, independientemente del rezago cronológico.
    2. **Identificar 4 Macro-Arquetipos**: Transición Precoz y Madura (Europa/Norteamérica), Despegue Intermedio (Latinoamérica/Norte de África), Transición Acelerada/Salto del Este Asiático (Corea/China/Singapur) y Transición Tardía/Inercial (África Subsahariana).
- **Justificacion**: La distancia euclidiana distorsiona la similitud al penalizar desfases de décadas. DTW demuestra que el Este Asiático replicó la transición europea pero a una velocidad 3 veces superior.
- **Alternativas descartadas**: Distancia euclidiana año a año (sesga por timing); comparar únicamente los años extremos 1950 y 2023 (omite la dinámica intra-periodo).

### Notebook 05 — Deteccion de Quiebres Estructurales (Change-Point Detection con PELT)

- **Notebook**: [05_statistical_insight.ipynb](../notebooks/05_statistical_insight.ipynb)
- **Contexto**: Determinar si la transición es un proceso determinista suave o si está expuesta a quiebres estructurales provocados por shocks exógenos.
- **Decision**: Aplicar el algoritmo PELT (Pruned Exact Linear Time) con costo kernel $L_2$ sobre series de países con eventos críticos documentados (Ruanda 1994, colapso soviético 1991, China 1979).
- **Justificacion**: Proporciona evidencia formal de que los shocks geopolíticos y sanitarios provocan desviaciones no estacionarias que reconfiguran permanentemente las sendas de transición demográfica.
- **Alternativas descartadas**: Inspección visual ad hoc; filtros lineales estándar tipo Hodrick-Prescott (suavizan artificialmente quiebres reales).

### Notebook 05 — Evaluacion Econometrica: La Falacia de la Reversion Migratoria

- **Notebook**: [05_statistical_insight.ipynb](../notebooks/05_statistical_insight.ipynb)
- **Contexto**: Abordar la Pregunta Guía #4 sobre si los flujos migratorios netos pueden revertir o solucionar el envejecimiento poblacional en regímenes sub-reemplazo ($TFR < 2.1$).
- **Decision**: Estimar un modelo de regresión de panel con errores estándar robustos a heterocedasticidad (HC1) del cambio anual en edad mediana ($\Delta \text{MedianAgePop}$) en función de $\text{CNMR}$.
- **Justificacion**: Se comprobó un efecto de amortiguación estadísticamente significativo ($\beta = -0.0053$, $p < 0.001$), pero de magnitud insuficiente: el envejecimiento intrínseco ($+0.53$ años/año) supera con creces el efecto compensador de la migración practicable.
- **Alternativas descartadas**: Afirmar cualitativamente que la migración "rejuvenece" a las poblaciones sin sustento paramétrico.

---

*Agrega nuevas decisiones al final, manteniendo el formato.*