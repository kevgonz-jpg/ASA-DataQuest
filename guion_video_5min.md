# Guion de Exposición para el Video (5 Minutos) — ASA DataQuest 2026

> **Archivo de presentación asociado:** `presentation_autocontenida.html` / `presentation.html` (8 diapositivas)  
> **Duración objetivo:** `5:00` minutos (`300 segundos`)  
> **Ritmo de locución recomendado:** ~135 palabras por minuto (pausado, claro, marcando silencios breves tras cada cifra clave)

---

## 🧭 Parte 1: Estrategia de Exposición (Sentido y Objetivo según los Documentos Oficiales)

### 1. Conexión directa con las preguntas semilla del concurso (*Getting Started Guide*, Sección 6)
El video responde explícitamente tres de las preguntas propuestas por los organizadores:
1. **Índice compuesto y justificación metodológica:** *«How might you combine several indicators into a single measure of a country's demographic profile, and what choices would that require you to justify?»* $\rightarrow$ Construcción del **Índice de Madurez Demográfica (ICD)** justificando el filtro conceptual de Spearman (7 pilares complementarios), las transformaciones logarítmicas, los 2 ejes ortogonales de PCA y el acotamiento robusto ($P_{2.5}\text{–}P_{97.5}$).
2. **Grupos y trayectorias en el tiempo:** *«Do countries fall into distinct groups based on how their indicators have moved together over time, rather than where they stand in any single year?»* $\rightarrow$ Identificación de los **4 Regímenes Demográficos** ($K=4$, estabilidad $\text{ARI} = 0.91$) y demostración de la **Convergencia Asimétrica** ($1950\text{–}2023$).
3. **Un indicador vs. mirada multivariada:** *«Is there a single indicator in this dataset that tells the whole story on its own, or does the interesting story only emerge once you look at several together?»* $\rightarrow$ Ningún indicador bruto aislado captura la transición completa, pero el ICD condensa la señal conjunta de los 7 pilares.

### 2. Las 3 «pruebas de fuego» de la Guía Oficial y del Código Ético ASA (2022)
- **Prevención del doble conteo (*Getting Started*, Sección 2):** Explicar en la Diapositiva 2 que se filtraron los agregados regionales y grupos de ingreso usando `ISO3_code` y `LocTypeID == 4` para aislar entidades territoriales reales.
- **Estimaciones vs. Proyecciones (*Getting Started*, Sección 5):** Distinguir con rigor entre las **estimaciones históricas reconstruidas (`1950–2023`)** y el **escenario plausible *Medium* de la ONU (`2024–2050`)**, comparando los modelos supervisados contra la **línea base de persistencia ($57.8\%$)**.
- **Los 8 Principios Éticos de la ASA (*Ethical Guidelines*, Principios A–H):** Vincular las decisiones técnicas con los **Principios B.1 y D.10** (aptitud y procedencia del dato), **Principios B.2 y C.4** (transparencia sobre supuestos e incertidumbre fuera de muestra, destacando el $53.5\%$ de *recall* en *Dinámica Migratoria*) y **Principio D.6** (evitar narrativas fatalistas o estigmatizantes hacia poblaciones vulnerables).

---

## ⏱️ Parte 2: Cronograma Ejecutivo por Diapositiva

| Diapositiva | Tiempo | Duración | Mensaje Central para el Jurado | Visualización Protagonista |
| :---: | :---: | :---: | :--- | :--- |
| **1** | `0:00 – 0:30` | 30 s | El caso Colombia y las 3 preguntas centrales sobre convergencia e índice compuesto. | Portada + 3 KPIs ejecutivos |
| **2** | `0:30 – 1:10` | 40 s | Rigor contra el doble conteo (`ISO3` / `LocTypeID`) y preservación de shocks históricos reales (`1950–2023`). | `03_scatter_tfr_vs_lex_epochs.png` |
| **3** | `1:10 – 1:50` | 40 s | De 67 variables a 7 pilares complementarios, 2 componentes principales ortogonales ($80.1\%$ varianza) y el ICD ($0\text{–}100$). | `04_pca_scree_loadings.png` |
| **4** | `1:50 – 2:30` | 40 s | Los 4 regímenes demográficos ($K=4$) y la **Convergencia Asimétrica** (longevidad $\beta = -0.75$ vs. fecundidad $\text{CV} +65\%$). | `04_cluster_regimes.png` |
| **5** | `2:30 – 3:10` | 40 s | Evaluación hacia el escenario ONU 2050: superación del *baseline* de persistencia ($57.8\% \to 88\text{–}89\%$) y transparencia fuera de muestra. | `05_diagnostics_and_feature_importance.png` |
| **6** | `3:10 – 3:55` | 45 s | La frontera de transición ($\text{ICD} = 52.0$), la graduación de Colombia y la mortalidad infantil ($29.8\text{‰}$ vs. $48.5\text{‰}$) en el escape pre-transicional. | `05_critical_icd_threshold.png` |
| **7** | `3:55 – 4:30` | 35 s | Gobernanza bajo los **8 Principios Éticos de la ASA (A–H)** y políticas diferenciadas por régimen sin fatalismo. | Matriz de Ética ASA y Política Pública |
| **8** | `4:30 – 5:00` | 30 s | Síntesis de los 3 criterios del jurado y demostración en vivo del gráfico interactivo a 60 FPS. | `01_tfr_vs_lex_animated.html` |

---

## 🎙️ Parte 3: Guion Minuto a Minuto (Listo para Grabar)

### Diapositiva 1: Portada — El Gran Dilema Demográfico (`0:00 – 0:30` | 30 s)
* **[En pantalla]:** Portada con el título del proyecto y las 3 tarjetas de síntesis (*Hallazgo Central*, *Rigor del Dato*, *Gobernanza Ética*).
* **[Locución]:**
  > «En una sola generación, países como Colombia pasaron de casi siete hijos por mujer a 1.65, envejeciendo tres veces más rápido de lo que tardó Europa.
  >
  > Al analizar las series de *World Population Prospects 2024* de las Naciones Unidas, nos propusimos responder tres preguntas clave del concurso: ¿Cómo sintetizar múltiples indicadores demográficos en una métrica única justificando cada decisión metodológica? ¿Se agrupan los países en regímenes distintos a lo largo del tiempo? ¿Y qué condiciones actuales separan a las naciones que logran avanzar hacia 2050 de las que permanecen rezagadas?»

---

### Diapositiva 2: Divergencia en la Transición y la Historia en los Extremos (`0:30 – 1:10` | 40 s)
* **[En pantalla]:** Gráfico `TFR vs. LEx` (`1950–2023`) a la izquierda; bloques de integridad del dato y preservación de extremos históricos a la derecha.
* **[Acción con el cursor]:** Señalar primero el bloque de filtrado `LocTypeID == 4` / `ISO3` a la derecha, y luego recorrer el gráfico de izquierda a derecha hacia la zona inferior derecha (baja fecundidad, alta longevidad).
* **[Locución]:**
  > «Siguiendo la guía oficial del dataset y el **Principio B.1 de la ASA sobre aptitud de los datos**, nuestro primer paso fue evitar el doble conteo poblacional: filtramos agregados regionales mediante el código `ISO3` y `LocTypeID`, y separamos las **17.538 estimaciones históricas (1950–2023)** de las proyecciones futuras.
  >
  > Tampoco eliminamos valores extremos como si fueran errores de captura: caídas de esperanza de vida a 11 años en Camboya o Ruanda, o picos migratorios en el Golfo Pérsico, son shocks históricos reales. Al conservarlos, emerge una paradoja: el mundo avanzó hacia una mayor esperanza de vida, pero al cruzar el umbral de reemplazo de 2.1 hijos por mujer, las trayectorias reproductivas se fragmentaron.»

---

### Diapositiva 3: Destilando la Complejidad — Del Ruido al Índice ICD (`1:10 – 1:50` | 40 s)
* **[En pantalla]:** Panel triple superior (Varianza PCA, Cargas Factoriales y Gradiente Regional del ICD) y los 3 pasos metodológicos en la parte inferior.
* **[Acción con el cursor]:** Señalar el paso 1 (los 7 pilares), luego el panel central de cargas (`PC1` vs. `PC2`) y finalmente el boxplot regional a la derecha.
* **[Locución]:**
  > «¿Cómo resumir 67 variables en un índice compuesto sin arbitrariedad? Justificamos tres elecciones metodológicas:
  >
  > Primero, depuramos tasas redundantes mediante correlaciones de Spearman, seleccionando **7 pilares conceptualmente complementarios**: fecundidad total, natalidad adolescente, mortalidad infantil, esperanza de vida, brecha de género en longevidad, edad mediana y migración neta.
  >
  > Segundo, tras corregir la asimetría con transformaciones logarítmicas, proyectamos las variables en **dos componentes principales ortogonales** que capturan más del **80 % de la varianza global**: un primer eje de transición vital y envejecimiento, y un segundo eje de presión migratoria.
  >
  > Y tercero, acotamos los extremos entre los percentiles 2.5 y 97.5 para construir el **Índice de Madurez Demográfica (ICD)** de 0 a 100.»

---

### Diapositiva 4: Los 4 Mundos Demográficos y la Convergencia Asimétrica (`1:50 – 2:30` | 40 s)
* **[En pantalla]:** Biplot K-Means ($K=4$) a la izquierda, gráfico de $\sigma$-convergencia a la derecha y las 4 tarjetas de régimen abajo.
* **[Acción con el cursor]:** Señalar los 4 clústeres en el biplot izquierdo y luego las dos curvas del gráfico derecho (la línea descendente de longevidad y la ascendente de dispersión relativa en fecundidad).
* **[Locución]:**
  > «Sobre este espacio ortogonal, el agrupamiento K-Means —con una estabilidad *bootstrap* ARI de 0.91— revela que el planeta se organiza hoy en **cuatro regímenes demográficos**: **Pre-Transicional** (con mediana de ICD en 17 puntos), **Transición Media** (donde se ubica América Latina con mediana de 49), **Post-Transición** envejecida (80 puntos) y **Dinámica Migratoria**.
  >
  > En el panel derecho demostramos formalmente lo que llamamos **Convergencia Asimétrica**: entre 1950 y 2023, la dispersión en esperanza de vida cayó de forma sostenida con pendiente $\beta$ de $-0.75$, pero la **dispersión relativa en fecundidad aumentó un 65 %**. Convergimos en supervivencia, pero divergimos en reproducción.»

---

### Diapositiva 5: Evaluando las Trayectorias al 2050 (`2:30 – 3:10` | 40 s)
* **[En pantalla]:** Benchmark de 5 modelos ML, Matriz de Confusión *Out-of-Fold* e Importancia de variables arriba; 3 bloques de síntesis abajo.
* **[Acción con el cursor]:** Apuntar a la matriz de confusión central (destacando el 53.5 % en Dinámica Migratoria) y al gráfico de barras de la derecha.
* **[Locución]:**
  > «Como subraya la guía del concurso, los datos hacia 2050 representan el escenario plausible *Medium* de las Naciones Unidas, no una certeza determinista. Para evaluar qué perfiles de 2023 logran cambiar de régimen en esa proyección sin fuga de datos, congelamos los centroides de 2023 y validamos cinco familias de modelos fuera de muestra.
  >
  > Mientras que una línea base de simple persistencia acierta el **57.8 %**, nuestros clasificadores alcanzan entre **87.8 % y 89.1 % de precisión** ($\pm 4.3\%$). Además, el ICD sintetiza con alta fidelidad la señal conjunta de los 7 indicadores, y la matriz fuera de muestra revela con transparencia dónde radica la incertidumbre: los regímenes biológicos superan el 91 % de sensibilidad, pero la **Dinámica Migratoria** baja a 53.5 % por su alta volatilidad geopolítica.»

---

### Diapositiva 6: La Frontera de Transición ($\text{ICD} = 52.0$) y la Trampa Pre-Transicional (`3:10 – 3:55` | 45 s)
* **[En pantalla]:** Curva de probabilidad hacia Post-Transición con la línea en $\text{ICD} = 52.0$ a la izquierda; a la derecha, los 3 grupos de países hacia 2050 (*Graduados*, *Escape Acelerado* y *Trampa Pre-Transicional*).
* **[Acción con el cursor]:** Señalar el cruce en 52.0 en la gráfica izquierda y luego las tarjetas de *Graduación* (Colombia, Brasil) y *Trampa Pre-Transicional* a la derecha.
* **[Locución]:**
  > «Al proyectar las transiciones hacia 2050 sobre la escala del ICD, la frontera estructural entre la Transición Media y la Post-Transición se sitúa alrededor de los **52 puntos del índice**.
  >
  > Las **32 naciones** en desarrollo que en 2023 ya superaron ese nivel —incluyendo a **Colombia (56.3)**, Brasil, México y Chile— transitan de forma consistente hacia el régimen Post-Transicional en las proyecciones de 2050.
  >
  > Pero el contraste más importante ocurre en el régimen Pre-Transicional: de 57 países, **35 logran avanzar** hacia la Transición Media —como Ghana, Ruanda y Senegal—, mientras **22 naciones del Sahel y África Central permanecen estancadas**. ¿Qué diferencia a ambos grupos desde 2023? Los países que despegan ya habían reducido su mortalidad infantil a una mediana de **29.8 por mil**, frente a **48.5 por mil** en los que quedan rezagados.»

---

### Diapositiva 7: Gobernanza Ética ASA y Hoja de Ruta Pública (`3:55 – 4:30` | 35 s)
* **[En pantalla]:** Columna izquierda con el marco ético de la ASA; columna derecha con las recomendaciones de política pública para cada uno de los 4 regímenes.
* **[Acción con el cursor]:** Recorrer los bloques de ética a la izquierda y luego las 4 tarjetas de política pública a la derecha.
* **[Locución]:**
  > «Alineados con los **ocho Principios Éticos de la ASA (A al H)** —especialmente los principios **B, C y D** sobre transparencia metodológica, comunicación honesta de la incertidumbre y protección de grupos vulnerables—, enfatizamos que una proyección alta de estancamiento nunca debe leerse como fatalismo biológico, sino como un llamado urgente a la acción.
  >
  > Por eso proponemos políticas diferenciadas por régimen: en los **22 países en rezago pre-transicional**, concentrar la inversión en supervivencia materno-infantil; en las **32 economías en transición como Colombia**, formalizar el empleo antes de que se cierre la ventana del bono demográfico; y en las naciones **Post-Transicionales**, fortalecer los sistemas de cuidado y la integración ética de las personas migrantes.»

---

### Diapositiva 8: Veredicto Final y Exploración Interactiva 60 FPS (`4:30 – 5:00` | 30 s)
* **[En pantalla]:** Las 3 tarjetas finales (*Best Statistical Insight*, *Best Data Visualization*, *Best Consideration of Ethics*) y el botón que abre la animación interactiva `01_tfr_vs_lex_animated.html`.
* **[Acción en pantalla en `4:40`]:** Hacer clic en el botón **`Abrir Visualización Interactiva (60 FPS)`** para mostrar en pantalla durante los últimos 15 segundos el movimiento continuo de los países entre 1950 y 2023.
* **[Locución]:**
  > «En conclusión: demostramos que el mundo vive una convergencia asimétrica, construimos un índice compuesto transparente que clasifica el planeta en cuatro regímenes estructurales y traducimos sus transiciones al 2050 en políticas públicas éticas y diferenciadas.
  >
  > Cerramos abriendo en vivo nuestra visualización interactiva a 60 cuadros por segundo, donde pueden recorrer año por año las 74 décadas de transformación demográfica global. Muchas gracias.»
