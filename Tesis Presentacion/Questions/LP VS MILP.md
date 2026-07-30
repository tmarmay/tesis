LP (Programación Lineal) puro, por definición, solo admite variables continuas — cualquier valor real dentro de sus cotas, sin restricción a números enteros. Ese es
  justo el problema con el VRP: variables como $x_{ij}^k$ (¿el vehículo $k$ viaja de $i$ a $j$?) o $u^k$ (¿se usa el vehículo $k$?) son decisiones inherentemente binarias — o pasa o no
  pasa, no hay término medio. Si resolvés la versión "relajada" del modelo dejando que $x_{ij}^k \in [0,1]$ en lugar de $x_{ij}^k \in {0,1}$ (lo cual es exactamente lo que hace un
  solver LP), no hay nada en la formulación que le impida al solver devolver, por ejemplo, $x_{ij}^k = 0.4$ — matemáticamente es una solución válida y hasta puede tener menor costo que
  cualquier alternativa entera, pero físicamente no significa nada: un camión no puede "viajar 40%" por una arista.

  Un ejemplo concreto de tu propio dominio: pensá en dos clientes con maquinaria pesada, cada uno demandando una carga que ocupa el 60% de la capacidad de un camión, y un solo vehículo
  disponible. La restricción de capacidad (2.3) del LP relajado podría "resolver" el problema diciendo que el camión atiende 60% al cliente A y 40% al cliente B en un viaje, y el
  resto en otro — una combinación fraccionaria de asignaciones que en total no exceda la capacidad y minimice el costo lineal. El problema es que una maquinaria agrícola no se puede 
  partir: o el camión se lleva la máquina completa del cliente A, o no se la lleva; no existe "0.4 tractores". El LP puro no tiene manera de imponer esa indivisibilidad porque su
  definición matemática no conoce el concepto de "todo o nada" — de ahí que necesites el MILP (Programación Lineal Entera Mixta): agregás explícitamente restricciones de integralidad
  (2.9 y 2.11 en tu formulación, $x_{ij}^k \in {0,1}$, $u^k \in {0,1}$) sobre esas variables de decisión discretas, mientras dejás como continuas las que sí tiene sentido que lo sean
  (como $s_i^k$, el tiempo de inicio de servicio, restricción 2.10 — ahí sí un valor como "las 14:32.7hs" es perfectamente válido). El costo de esa integralidad es que ya no podés
  resolver el problema con los métodos eficientes de LP puro (simplex en tiempo polinomial); necesitás branch-and-bound, que explora combinaciones enteras podando ramas con la ayuda de
  la relajación LP como cota — exactamente la razón por la que MILP escala tan mal en tu experimentación (Sección 3.3.3) frente al LP relajado, que sería trivial de resolver.

> La limitacion es por sentido en las soluciones
  Sobre el "sentido" de las soluciones: exacto, la limitación de LP no es que "no pueda calcular bien" — matemáticamente resuelve el problema perfecto, encuentra el óptimo del espacio
  continuo sin drama. El problema es de correspondencia con la realidad: el LP puede devolver un óptimo matemáticamente válido que no representa ninguna decisión física ejecutable (0.4
  camiones, 60% de una máquina en un viaje). El LP no está "mal", está resolviendo un problema distinto al que en verdad te interesa — un problema relajado, más fácil, que ignora una
  restricción real del mundo (la indivisibilidad).

> La diferencia entre lp y milp son las restricciones a las varibles para que sea binarias ?
  Sobre la diferencia LP vs MILP: sí, es exactamente eso — la diferencia es la restricción de integralidad sobre las variables. Formalmente:
  - LP: todas las variables son continuas.
  - MILP: algunas variables son enteras/binarias y otras siguen siendo continuas (de ahí "mixed" — mezcla).
  - Si todas las variables fueran enteras (ninguna continua), eso ya no se llamaría MILP sino ILP (Integer Linear Programming) o, si son específicamente 0/1, BIP (Binary Integer Programming). Tu modelo es MILP propiamente dicho porque mezclás $x_{ij}^k, u^k$ (binarias) con $s_i^k$ (continua).

>En lp puedo hacer que  todas las variables sean solo enteras ?  
  Sobre "¿en LP puedo hacer que las variables sean enteras?": acá el matiz — no, y no es una limitación técnica del solver, es definicional: en el momento en que le agregás la
  restricción "esta variable debe ser entera" a un problema, ese problema deja de llamarse LP y pasa a llamarse ILP o MILP. No es que exista un LP con variables enteras; es que agregar
  esa restricción es precisamente lo que separa una clase de la otra. Y esto no es solo una cuestión de nombres: importa muchísimo porque se resuelven con algoritmos completamente 
  distintos. El LP se resuelve en tiempo polinomial (simplex o métodos de punto interior) porque su región factible es un poliedro convexo continuo — el óptimo siempre está en un
  vértice, y hay maneras eficientes de navegar hacia él. En cuanto exigís integralidad, la región factible deja de ser continua (es un conjunto discreto de puntos aislados dentro de
  ese poliedro), y ya no existe un atajo algebraico: hay que recurrir a búsqueda combinatoria (branch-and-bound), que en el peor caso explora exponencialmente muchas combinaciones — la
  misma razón, dicho sea de paso, por la que TSP y VRP son NP-Hard mientras que su relajación LP no lo es.

