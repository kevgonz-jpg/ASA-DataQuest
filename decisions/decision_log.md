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

*Agrega nuevas decisiones al final, manteniendo el formato.*