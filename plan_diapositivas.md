# Plan Maestro y Guion Narrativo (5 Minutos) — Presentación V2 (Storytelling Compacto)

> **Propósito:** Versión optimizada para un **video de 5 minutos (300 segundos)** en el **ASA DataQuest 2026**.  
> **Enfoque:** Pasar de una exposición de "estructura de notebooks" a una **historia científica de descubrimiento estadístico** (*Storytelling*): **El Mito → La Evidencia Real → La Métrica (ICD) → El Futuro (2050) → El Punto de Quiebre ($\text{ICD}=52$) → El Impacto Humano**.  
> **Versiones preservadas:** La versión técnica exhaustiva de 12 diapositivas quedó guardada intacta en `presentation_v1.html` y `presentation_v1_autocontenida.html`.

---

## ⏱️ Cronograma del Video de 5 Minutos (8 Diapositivas · ~37 s por diapositiva)

| Slide | Tiempo | Arco Narrativo (Storytelling) | Mensaje Central (1 Frase para el Jurado) | Gráfico Protagonista |
| :---: | :---: | :--- | :--- | :--- |
| **1** | `0:00 – 0:30` | **El Gancho** | El mundo no envejece al mismo ritmo: se está partiendo en dos velocidades demográficas. | Portada ejecutiva + 3 KPIs de impacto |
| **2** | `0:30 – 1:10` | **El Mito vs. La Realidad** | Durante 74 años la longevidad convergió, pero la fecundidad se polarizó (+65% en dispersión); la historia real está en los extremos. | `03_scatter_tfr_vs_lex_epochs.png` |
| **3** | `1:10 – 1:50` | **El Reto de Medir sin Sesgar** | De 67 variables colineales y asimétricas destilamos **7 pilares ortogonales** y creamos el **ICD (0–100)** con PCA (80.1% varianza) y Winsorización OCDE. | `04_pca_scree_loadings.png` |
| **4** | `1:50 – 2:30` | **Los 4 Mundos Demográficos** | El planeta hoy se divide en **4 regímenes estructurales** ($K=4$) y la prueba de $\sigma$-convergencia refuta formalmente la convergencia homogénea. | `04_cluster_regimes.png` |
| **5** | `2:30 – 3:10` | **Viaje al 2050 (Machine Learning)** | Proyectando sin *data leakage* y validando 5 familias ML (**89.1% Accuracy**), demostramos que el **ICD es el predictor #1 (18.9% Gini)** del destino al 2050. | `05_diagnostics_and_feature_importance.png` |
| **6** | `3:10 – 3:55` | **El Clímax: El Umbral $\text{ICD} = 52.0$** | Descubrimos una bifurcación no lineal en **52 puntos**: **32 países** (incluidos Colombia y Brasil) se gradúan a Post-Transición, mientras **22 naciones** quedan atrapadas en Pre-Transición. | `05_critical_icd_threshold.png` |
| **7** | `3:55 – 4:30` | **Ética ASA y Acción Pública** | Un algoritmo predice trayectorias, no destinos fatales: hoja de ruta por régimen auditada bajo los **10 principios éticos de la ASA**. | Tarjetas visuales de acción y ética |
| **8** | `4:30 – 5:00` | **Veredicto y Cierre 60 FPS** | Síntesis de los 3 premios ASA y apertura en vivo de la animación interactiva a 60 FPS (`1950–2023`). | `01_tfr_vs_lex_animated.html` |

---

## 🎙️ Guion Hablado Sugerido por Diapositiva (Listo para Grabar)

### Diapositiva 1: Portada — El Gran Dilema Demográfico (`0:00 – 0:30`)
- **Lo que se ve:** Título de alto impacto, 3 tarjetas limpias con el hallazgo central, la solidez del dato y la ética.
- **Guion (30 s):**
  > *"Durante décadas asumimos que todos los países seguirían el mismo camino demográfico hacia el envejecimiento. Analizando 74 años de historia censal en los 237 países y áreas de Naciones Unidas, demostramos que esa convergencia homogénea es un mito. Construimos el Índice de Madurez Demográfica (ICD), identificamos un umbral crítico de bifurcación en 52 puntos y predecimos con un 89.1% de precisión qué naciones darán el salto al 2050 y cuáles enfrentan una trampa estructural."*

### Diapositiva 2: El Mito de la Convergencia y la Historia en los Extremos (`0:30 – 1:10`)
- **Lo que se ve:** Gráfico de dispersión `TFR vs. LEx` (1950–2023) a la izquierda; a la derecha, 3 bloques visuales ultracompactos sobre integridad del dato (`LocTypeID == 4`, corte `IsEstimate`) y por qué los *outliers* son historia viva.
- **Guion (40 s):**
  > *"Al separar rigurosamente las 17.538 observaciones empíricas de las proyecciones y evitar el doble conteo regional, emerge una paradoja: desde 1950 el mundo se desplazó hacia una mayor esperanza de vida, pero al cruzar la línea de reemplazo de 2.1 hijos por mujer, las trayectorias se fracturaron. Además, rechazamos borrar los valores extremos: una esperanza de vida de 11 años en Camboya o Ruanda, o choques migratorios del 350 por mil en el Golfo Pérsico, no son errores de digitación; son cicatrices históricas que un modelo riguroso debe preservar."*

### Diapositiva 3: Destilando la Complejidad — Del Ruido al Índice ICD (`1:10 – 1:50`)
- **Lo que se ve:** Panel triple del PCA + Loadings + Gradiente Regional del ICD arriba; abajo, el flujo en 3 pasos cortos: Embudo de Spearman (7 pilares) $\to$ PCA en correlaciones (80.1% varianza) $\to$ Winsorización OCDE ($P_{2.5}\text{–}P_{97.5}$).
- **Guion (40 s):**
  > *"¿Cómo resumir 67 indicadores sin sesgar la estadística? Primero aplicamos un embudo de Spearman para eliminar variables redundantes y destilar 7 pilares ortogonales. Luego, mediante Componentes Principales sobre la matriz de correlaciones, capturamos el 80.1% de la información global en dos ejes: transición biológica (56.7%) y dinámica migratoria (23.4%). Finalmente, aplicamos Winsorización entre los percentiles 2.5 y 97.5 siguiendo el manual de la OCDE, creando el Índice de Madurez Demográfica de 0 a 100 sin que los microestados distorsionen la escala."*

### Diapositiva 4: Los 4 Mundos Demográficos y la Falacia de Convergencia (`1:50 – 2:30`)
- **Lo que se ve:** Biplot K-Means ($K=4$) + Curva de $\sigma$-Convergencia arriba; abajo, 4 tarjetas compactas (una por régimen con su mediana de ICD, `TFR` y `LEx`).
- **Guion (40 s):**
  > *"En este espacio factorial emergen 4 regímenes estructurales: desde el Pre-Transicional en África con ICD mediano de 17 puntos y casi 4 hijos por mujer, pasando por la Transición Media en América Latina, hasta la Post-Transición envejecida y las economías receptoras de migración. Al evaluar la sigma-convergencia entre 1950 y 2023, comprobamos formalmente nuestra tesis: el mundo convergió en supervivencia biológica, pero su dispersión relativa en fecundidad aumentó un 65%. Nos estamos polarizando."*

### Diapositiva 5: Prediciendo el 2050 — El ICD como Predictor Líder (`2:30 – 3:10`)
- **Lo que se ve:** Panel triple de ML (Benchmark de 5 modelos + Matriz de Confusión Out-of-Fold + Ranking de Importancia Gini) arriba; abajo, 3 mensajes clave concisos con los números de la transición ($2023 \to 2050$).
- **Guion (40 s):**
  > *"Para proyectar hacia dónde irá cada país en 2050 sin fuga de datos, congelamos la geometría de 2023 y entrenamos cinco familias de Machine Learning bajo validación cruzada estratificada. Todos los modelos superan el 85% de precisión, liderados por SVM y Regresión Logística con 89.1%. Y el hallazgo clave de explicabilidad: nuestro índice compuesto ICD es el predictor individual número uno del futuro demográfico con 18.9% de importancia Gini, superando a la fecundidad y la esperanza de vida por separado."*

### Diapositiva 6: El Punto de Quiebre — El Umbral Crítico $\text{ICD} = 52.0$ (`3:10 – 3:55`)
- **Lo que se ve:** Curva sigmoidal del umbral $\text{ICD} = 52.0$ a la izquierda; a la derecha, los 3 destinos al 2050 (Graduados, Escape Acelerado y Trampa Pre-Transicional) con banderas/nombres clave.
- **Guion (45 s):**
  > *"Aquí está el corazón de nuestro hallazgo estadístico: la transición hacia el 2050 no es lineal; obedece a un umbral crítico en 52 puntos del ICD. Ningún país en desarrollo por debajo de 52 logra graduarse a la Post-Transición. Quienes ya cruzaron ese umbral —32 naciones como Brasil, Colombia, México, Argentina y Turquía— tienen más de un 91% de probabilidad de envejecer rápidamente hacia la Post-Transición. En contraste, aunque 35 países como Ghana y Ruanda logran escapar a la etapa intermedia reduciendo su mortalidad infantil, 22 naciones del Sahel quedan atrapadas en la Pre-Transición con más del 98% de probabilidad."*

### Diapositiva 7: Gobernanza Ética ASA — De la Predicción a la Acción (`3:55 – 4:30`)
- **Lo que se ve:** Dos columnas muy visuales y limpias: a la izquierda, 4 garantías éticas ASA (Transparencia, Cero Fatalismo, Honestidad Out-of-Fold, Reproducibilidad); a la derecha, la receta de política pública para cada régimen.
- **Guion (35 s):**
  > *"Siguiendo los 10 principios éticos de la ASA, enfatizamos que una probabilidad del 99% no es determinismo biológico: es una alerta temprana humanitaria. Para las 22 naciones en la trampa pre-transicional, la palanca crítica es abatir la mortalidad infantil bajo 30 por mil. Para América Latina, que se gradúa hacia 2050, urge formalizar el empleo juvenil antes de que se cierre el bono demográfico. Y en la Post-Transición, debemos sustituir el alarmismo natalista por sistemas de cuidado e integración migratoria con enfoque de derechos humanos."*

### Diapositiva 8: Veredicto Final y Exploración Interactiva 60 FPS (`4:30 – 5:00`)
- **Lo que se ve:** Tres grandes tarjetas de conclusión vinculadas a los criterios del jurado + Botón de lanzamiento del gráfico animado a 60 FPS.
- **Guion (30 s):**
  > *"En conclusión: demostramos que el mundo diverge reproductivamente, construimos un índice compuesto robusto que lidera la predicción supervisada al 2050, y descubrimos el umbral crítico de 52 puntos que separa la graduación demográfica del estancamiento. Cerramos nuestro recorrido abriendo nuestra visualización interactiva a 60 cuadros por segundo para explorar 74 años de historia demográfica en tiempo real. Muchas gracias."*
