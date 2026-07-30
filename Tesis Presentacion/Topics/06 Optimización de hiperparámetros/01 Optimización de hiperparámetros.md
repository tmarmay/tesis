El rendimiento de ACO depende fuertemente de sus hiperparámetros

Elegir estos valores manualmente es difícil porque interactúan entre sí de formas no lineales y su efecto varía según las características de las instancias.

La optimización de hiperparámetros puede formularse como un problema de optimización en sí mismo: dado un algoritmo parametrizado, encontrar la configuración que minimiza una métrica de rendimiento sobre un conjunto representativo de instancias. 
La dificultad radica en que cada evaluación requiere ejecutar el algoritmo completo, lo que hace prohibitivo explorar el espacio de configuraciones de forma exhaustiva. Estrategias simples como la búsqueda en grilla o la búsqueda aleatoria no escalan bien cuando el número de parámetros es alto y sus interacciones entre sí son no lineales: el valor óptimo de un parámetro depende del valor de los
demás, por lo que no es posible optimizarlos de forma independiente

La optimización bayesiana aborda este problema construyendo un modelo probabilístico del espacio de búsqueda que se actualiza con cada evaluación, permitiendo proponer configuraciones prometedoras en lugar de explorar a ciegas

El objetivo de la optimización fue minimizar el costo promedio de las soluciones encontradas por ACO sobre un conjunto de instancias representativo. La configuración resultante no solo redujo el costo promedio, sino que también disminuyó significativamente la dispersión entre ejecuciones.

Las instancias utilizadas para la calibración fueron generadas con el mismo rango de parámetros que el experimento principal (véase laSección 4.3), pero con distintas combinaciones, evitando así que el algoritmo se calibre sobre las mismas instancias que luego se evalúan

Hablamos de 10 parametros, que pueden tomar valores continuos mayores a cero y relacionarse entre si de formas no lineales.