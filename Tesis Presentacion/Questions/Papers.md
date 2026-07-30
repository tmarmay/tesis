### Que diferencia seria usar ACO como Bakhtiari y VRP como Garcia ?  Porque ACO puede no ser VRP ? 
  ACO es agnóstico al problema. Ant Colony Optimization (Dorigo, 1992) nació originalmente para resolver TSP, no VRP. La idea de fondo — agentes que construyen soluciones incrementalmente, guiados por feromonas +
  heurística local, con refuerzo probabilístico de los mejores caminos — es un mecanismo de búsqueda sobre un grafo, no una técnica atada a una formulación matemática específica. Por eso se
  aplicó después a:

  - TSP (su caso original)
  - VRP y sus variantes (tu caso)
  - Job-shop scheduling
  - Quadratic Assignment Problem
  - Coloreo de grafos
  - Ruteo en redes de telecomunicaciones

  Lo único que ACO necesita es que el problema se pueda representar como un grafo donde una solución se construye paso a paso (agregando nodos/aristas), y que exista una función de costo
  para evaluar la calidad del recorrido final. Cualquier problema con esa forma es candidato a ACO — no hace falta que sea VRP.

## Evolucion de TSP a VRP en "Truck Dispatching Problem ~ Dantzig"
  Dantzig y Ramser (1959) plantean el "truck dispatching problem": una empresa tiene una terminal (depósito) central y debe abastecer con combustible a varias estaciones de servicio
  dispersas geográficamente, usando una flota de camiones homogéneos con capacidad limitada. El objetivo es determinar las rutas de los camiones que minimicen la distancia (o costo)
  total recorrida, respetando que:
  - Cada estación debe ser visitada exactamente una vez.
  - Cada camión sale y vuelve al depósito.
  - La demanda total asignada a un camión no puede exceder su capacidad.
 
En términos estructurales, el VRP nace como un "m-TSP con restricción de capacidad"

#### TSP como caso particular de VRP (a nivel de modelo)
  Si en el modelo de VRP ponés m = 1 (un solo vehículo) y capacidad Q → ∞ (o al menos Q ≥ demanda total), la restricción de partición desaparece: ya no hace falta cortar el conjunto de
  clientes en subgrupos, porque un solo vehículo puede cubrir toda la demanda en un único recorrido. Ahí el VRP colapsa exactamente al TSP. Por eso formalmente se dice que VRP ⊇ TSP:
  el TSP es el caso degenerado de VRP sin restricción de capacidad activa y con una sola ruta.

####  La estrategia algorítmica que se desprende de eso
  Tu intuición de "particionar y después correr m TSP" es precisamente el paradigma que en la literatura se conoce como cluster-first, route-second:

  1. Partición (clustering): agrupás los clientes en subconjuntos $S_1, ..., S_m$ tal que $\sum_{i \in S_k} d_i \le Q$ para cada camión $k$.
  2. Ruteo (TSP por subconjunto): una vez fija la partición, encontrar el orden óptimo de visita dentro de cada $S_k$ es literalmente resolver un TSP independiente en cada subgrupo
  (nodos = clientes del cluster + depósito).

  Esto te da el gancho formal perfecto para completar el párrafo anterior: la partición es la parte nueva que aporta el VRP, pero una vez que particionás, cada subproblema se reduce
  otra vez a un TSP — es TSP "empaquetado" m veces.

## Complejidad de TSP

### Crecimiento del espacio de soluciones (combinatoria pura)
  Dado $n$ ciudades (sin contar el depósito, o incluyéndolo como punto fijo de partida):
  - Todas las permutaciones posibles: $n!$
  - Tours distintos fijando el punto de partida (porque el ciclo es el mismo empiece donde empiece): $(n-1)!$
  - Para TSP simétrico (distancia $i\to j$ = distancia $j\to i$), además cada tour se puede recorrer en dos sentidos y da el mismo costo, entonces los tours realmente distintos son:
  $$\frac{(n-1)!}{2}$$
  Esta es la fórmula que normalmente se cita para mostrar la explosión combinatoria: con $n=10$ ya son ~181.440 tours candidatos; con $n=20$ son del orden de $10^{17}$.

### Crecimiento de la complejidad computacional
  Acá es donde entra Garey y Johnson (1990), que ya tenés en tu lista de fuentes. El resultado central es que TSP es NP-hard (la versión de decisión es NP-completa), lo que significa
  que no se conoce ningún algoritmo exacto que resuelva el problema en tiempo polinomial respecto de $n$ — en el peor caso, el tiempo de cómputo crece de forma exponencial.

  El mejor algoritmo exacto conocido no es fuerza bruta ($O(n!)$), sino programación dinámica de Held-Karp (1962), que baja la cota a:
  $$O(n^2 \cdot 2^n) \text{ en tiempo, } \quad O(n \cdot 2^n) \text{ en espacio}$$
  Sigue siendo exponencial, pero muchísimo mejor que $n!$. Esta es la fórmula que se suele citar en la literatura de VRP como referencia de "cota superior conocida para resolución
  exacta", y es el punto de partida habitual para justificar por qué se recurre a heurísticas y metaheurísticas (como tu ACO) a medida que $n$ crece.
