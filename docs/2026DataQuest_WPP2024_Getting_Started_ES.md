# Guia de Inicio: Conjunto de Datos UN World Population Prospects 2024

Esta guia describe los tres archivos proporcionados para la competencia DataQuest 2026, su contenido y como cargarlos y comenzar a trabajar con ellos.

---

## 1. Contenido de los Archivos

| Archivo | Contenido | Filas | Anos cubiertos |
| :--- | :--- | :--- | :--- |
| `WPP2024_Demographic_Indicators_Medium_csv.gz` | Dataset principal: la serie de estimacion central de la ONU ("Medium"). Incluye estimaciones historicas mas la proyeccion variante media como una serie continua. | 84,360 | 1950-2100 |
| `WPP2024_Demographic_Indicators_OtherVariants_csv.gz` | Opcional. Escenarios alternativos de proyeccion (alta/baja fecundidad, mortalidad constante, migracion cero, intervalos de confianza probabilistas, etc.). Solo cubre anos proyectados. | 662,919 | 2024-2100 |
| `WPP2024_Demographic_Indicators_notes.csv` | Diccionario de indicadores (codebook): significado de cada abreviatura de columna y su unidad de medida. | 54 | - |

Ambos archivos `.gz` son archivos CSV comprimidos con gzip. Las herramientas de programacion (como `pandas` en Python o `read_csv` en R) pueden leerlos directamente sin necesidad de descomprimirlos previamente (ver Seccion 3). Sin embargo, Excel no puede abrir archivos `.gz` directamente.

Si desea usar Excel:
1. Extraiga el archivo primero (doble clic en Mac; en Windows con herramientas como 7-Zip).
2. Verifique el nombre del archivo extraido: el archivo original de la ONU se almacena sin extension `.csv` (termina en `_csv` en lugar de `.csv`), por lo que la mayoria de herramientas conservan ese nombre sin extension. Renombrelo agregando `.csv` al final antes de abrirlo; de lo contrario, Excel no lo reconocera como hoja de calculo.
3. Abra el archivo renombrado en Excel de forma habitual.

Comience con el archivo `Medium`. Es el dataset central para la mayoria de los analisis: una fila por ubicacion y por ano, con indicadores de poblacion, fecundidad, mortalidad y migracion como columnas. Utilice `OtherVariants` unicamente cuando desee evaluar la incertidumbre de las proyecciones (ver Seccion 5).

---

## 2. Columnas Clave a Comprender Antes de Cualquier Analisis

El campo `Location` no contiene unicamente paises individuales. Tambien incluye agregados regionales, agregados por nivel de ingreso y mas de 230 agrupaciones ad hoc. Si no separa los paises reales de estas agrupaciones antes de realizar comparaciones entre paises o agregaciones globales, duplicara o sobreestimara el conteo de poblacion.

| Columna | Que representa | Por que es importante |
| :--- | :--- | :--- |
| `Location` | Nombre del pais, region o agrupacion geografica/economica. | Identificador textual de la entidad demografica. |
| `ISO3_code` | Codigo de pais de 3 letras (ej. USA, KEN, COL). | Solo esta presente para paises reales; permanece en blanco para regiones y agregados. Es un filtro esencial. |
| `LocTypeName` | Tipo de entidad de la fila. | Diferencia paises individuales de agrupaciones regionales, por nivel de ingreso u organizaciones. |
| `Variant` | Escenario de proyeccion correspondiente. | En el archivo Medium siempre es "Medium". En OtherVariants adopta 18 valores distintos (ver Seccion 5). |
| `Time` | Ano calendario. | Abarca el rango 1950-2100. |

---

## 3. Carga de los Datos

### Python
```python
import pandas as pd

medium = pd.read_csv(
    "WPP2024_Demographic_Indicators_Medium_csv.gz",
    compression="gzip",
    encoding="utf-8-sig",
    low_memory=False
)
```

### R
```r
medium <- read.csv(
  "WPP2024_Demographic_Indicators_Medium_csv.gz",
  fileEncoding = "UTF-8-BOM"
)
```

---

## 4. Referencia de Indicadores (Metadatos y Codebook)

Cada columna en los archivos Medium y OtherVariants corresponde a uno de los siguientes indicadores agrupados por tematica. Utilice esta tabla de referencia en lugar de asumir el significado de las abreviaturas.

Nota: Cuando un desglose por sexo o grupo de edad comparte el mismo concepto y unidad subyacente (por ejemplo, `Deaths`, `DeathsMale`, `DeathsFemale`), las filas se combinan para facilitar la lectura. Para la redaccion exacta columna por columna, consulte `WPP2024_Demographic_Indicators_notes.csv`.

### Poblacion

| Codigo | Nombre | Unidad |
| :--- | :--- | :--- |
| `TPopulation1Jan` | Poblacion total al 1 de enero | miles |
| `TPopulation1July` | Poblacion total al 1 de julio | miles |
| `TPopulationMale1July` | Poblacion masculina al 1 de julio | miles |
| `TPopulationFemale1July` | Poblacion femenina al 1 de julio | miles |
| `PopDensity` | Densidad poblacional al 1 de julio | personas por km cuadrado |
| `PopSexRatio` | Razon de sexo de la poblacion al 1 de julio | hombres por cada 100 mujeres |
| `MedianAgePop` | Edad mediana al 1 de julio | anos |
| `NatChange` | Cambio natural (Nacimientos menos Muertes) | miles |
| `NatChangeRT` | Tasa de cambio natural | por cada 1,000 habitantes |
| `PopChange` | Cambio poblacional total | miles |
| `PopGrowthRate` | Tasa de crecimiento poblacional | porcentaje (%) |
| `DoublingTime` | Tiempo de duplicacion anual de la poblacion | anos |

### Fecundidad

| Codigo | Nombre | Unidad |
| :--- | :--- | :--- |
| `Births` | Nacimientos anuales totales | miles |
| `BirthsMale` / `BirthsFemale` | Nacimientos por sexo (en suplemento oficial) | miles |
| `Births1519` | Nacimientos de mujeres entre 15 y 19 anos | miles |
| `CBR` | Tasa bruta de natalidad (Crude Birth Rate) | nacimientos por cada 1,000 habitantes |
| `TFR` | Tasa global de fecundidad (Total Fertility Rate) | hijos nacidos vivos por mujer |
| `NRR` | Tasa neta de reproduccion (Net Reproduction Rate) | hijas sobrevivientes por mujer |
| `MAC` | Edad media a la maternidad (Mean Age Childbearing) | anos |
| `SRB` | Razon de sexo al nacer (Sex Ratio at Birth) | hombres por cada 100 nacimientos femeninos |

### Mortalidad

| Codigo | Nombre | Unidad |
| :--- | :--- | :--- |
| `Deaths` / `DeathsMale` / `DeathsFemale` | Defunciones totales y por sexo | miles |
| `CDR` | Tasa bruta de mortalidad (Crude Death Rate) | defunciones por cada 1,000 habitantes |
| `LEx` / `LExMale` / `LExFemale` | Esperanza de vida al nacer | anos |
| `LE15`, `LE60`, `LE65`, `LE80` (+ Male/Female) | Esperanza de vida a las edades 15, 60, 65 y 80 | anos |
| `InfantDeaths` | Muertes infantiles (menores de 1 ano) | miles |
| `IMR` | Tasa de mortalidad infantil | muertes infantiles por cada 1,000 nacidos vivos |
| `LBsurvivingAge1` | Nacidos vivos que sobreviven hasta el primer ano | miles |
| `Under5Deaths` | Muertes de menores de 5 anos | miles |
| `Q5` | Tasa de mortalidad en la ninez (menores de 5 anos) | muertes menores de 5 anos por cada 1,000 nacidos vivos |
| `Q0040`, `Q0060` (+ Male/Female) | Probabilidad de morir antes de los 40 y 60 anos | por cada 1,000 nacidos vivos |
| `Q1550`, `Q1560` (+ Male/Female) | Probabilidad de morir entre 15-50 y 15-60 anos | por cada 1,000 sobrevivientes a los 15 anos |

### Migracion

| Codigo | Nombre | Unidad |
| :--- | :--- | :--- |
| `NetMigrations` | Saldo neto migratorio (Inmigrantes menos Emigrantes) | miles |
| `CNMR` | Tasa neta de migracion | por cada 1,000 habitantes |

*Nota tecnica:* Una version preliminar indicaba que `LE60`, `LE60Male`, `LE60Female`, `BirthsMale` y `BirthsFemale` se encontraban en el dataset Medium. Dichas series fueron provistas en un archivo suplementario separado (`WPP2024_Supplement_Births_and_LE60.csv`). Los archivos Medium y OtherVariants contienen 54 columnas directas de indicadores.

---

## 5. Estimaciones vs. Proyecciones — y el Archivo OtherVariants (Opcional)

El archivo `Medium` conforma una serie temporal continua, pero sus periodos poseen distinta naturaleza metodologica:
- **1950-2023:** Son estimaciones basadas en registros civiles, censos de poblacion y encuestas de hogares.
- **2024-2100:** Son proyecciones de variante media calculadas por la ONU bajo supuestos explicitos de convergencia de fecundidad, mortalidad y patrones migratorios. Constituye un escenario plausible, no un pronostico exacto.

El archivo `OtherVariants` no es obligatorio, pero esta disponible para profundizar en el analisis de incertidumbre demografica. Abarca exclusivamente el periodo **2024-2100** e incluye:
- **Escenarios alternativos deterministas:** Fecundidad alta (`High`), fecundidad baja (`Low`), fecundidad constante (`Constant fertility`), mortalidad constante (`Constant mortality`), migracion nula (`Zero migration`), reemplazo instantaneo (`Instant replacement`), inercia demografica (`Momentum`), sin fecundidad antes de los 18 anos, entre otros.
- **Intervalos de prediccion probabilistas:** Intervalo inferior y superior al 80% (`Lower 80 PI`, `Upper 80 PI`), intervalo inferior y superior al 95% (`Lower 95 PI`, `Upper 95 PI`), mediana probabilista (`Median PI`) y media (`Mean`).

Una entrega competitiva y rigurosa puede desarrollarse completamente utilizando unicamente la variante `Medium`.

---

## 6. Preguntas Iniciales Sugeridas

1. **Estructura por edad:** Como diverge la estructura de edad de la poblacion (edad mediana, indicadores de esperanza de vida vinculados a dependencia economica) entre paises o regiones a lo largo del tiempo?
2. **Incertidumbre demografica (OtherVariants):** Que paises muestran la mayor dispersion entre las proyecciones de las variantes Alta y Baja, y que revela esto sobre la incertidumbre de su futuro poblacional?
3. **Sensibilidad a la fecundidad (OtherVariants):** Que tan sensible es la proyeccion de poblacion al ano 2100 de un determinado pais ante el supuesto exclusivo de fecundidad (comparando variante Media vs. Fecundidad Constante vs. Alta/Baja)?
4. **Impacto migratorio:** Cual es la relacion empírica entre los patrones de migracion neta y el crecimiento o decrecimiento poblacional en las distintas regiones del mundo?
5. **Indice compuesto:** Como podria sintetizar multiples indicadores demograficos en una metrica unica del perfil demografico de un pais, y que elecciones metodologicas exige justificar?
6. **Agrupamiento y trayectorias:** Se agrupan los paises en perfiles distintivos segun como han evolucionado conjuntamente sus indicadores en el tiempo, en lugar de considerar su posicion en un ano aislado?
7. **Interaccion de componentes demograficos:** Como interactuan la fecundidad, la mortalidad y la migracion para definir la trayectoria poblacional de un pais, y varia dicha dinamica entre niveles de ingreso o continentes?
8. **Vision holistica:** Existe un indicador individual que sintetice toda la dinamica demografica por si solo, o el patron relevante emerge unicamente cuando se evaluan varias dimensiones de manera conjunta?
