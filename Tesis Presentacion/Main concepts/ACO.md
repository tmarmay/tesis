
## Fase 1

### Funcion de Probabiliad

$$P(c \to v) = \frac{(\tau_{vc}^{asig})^\alpha \cdot (\eta_{vc})^\beta}{\sum_{v' \in V} (\tau_{v'c}^{asig})^\alpha \cdot (\eta_{v'c})^\beta}$$Es una selección por ruleta: para un cliente $c$ dado, cada hormiga calcula esta probabilidad para cada vehículo $v$ candidato, y elige uno al azar ponderado por esos valores (no determinísticamente el máximo).

  Los dos ingredientes

  - $\tau_{vc}^{asig}$ (feromona): cuánto "se acuerda" el sistema de que asignar el cliente $c$ al vehículo $v$ dio buenos resultados en iteraciones anteriores. Es la componente de aprendizaje/memoria.
  - $\eta_{vc} = \dfrac{1}{d[\text{Depot}_v][c]}$ (atractivo heurístico): mientras más cerca esté el depósito del vehículo $v$ del cliente $c$, mayor este valor. Es la componente miope/greedy — el mismo tipo de criterio que usa TWNN, pero acá solo mirando distancia depósito–cliente, no toda la ruta.

  Los exponentes

  $\alpha$ y $\beta$ son los pesos relativos de cada componente:
  - $\alpha$ alto → el agente confía más en lo que "aprendió" la colonia en iteraciones pasadas.
  - $\beta$ alto → el agente confía más en el criterio heurístico inmediato (cercanía al depósito).

  El denominador

  Es solo la normalización: sumás $(\tau_{v'c}^{asig})^\alpha \cdot (\eta_{v'c})^\beta$ sobre todos los vehículos candidatos $v'$, para que las probabilidades de todos los vehículossumen 1 y sea una distribución válida.

  En una frase: la Fase 1 no decide "el mejor vehículo" de forma determinística, sino que le da a cada vehículo una probabilidad de ser elegido proporcional a una combinación pesada de
  "qué tan bien le fue históricamente a ese cliente con ese vehículo" (feromona) y "qué tan cerca está ese vehículo del cliente ahora" (heurística) — y el resultado de esta fase es la
  asignación cliente→vehículo con la que luego arranca la Fase 2 (construcción de la ruta en sí).

Se llama selección por ruleta (roulette wheel selection), y de hecho tu propio texto ya usa ese término — está en la Fase 2 (pág. 11): "de lo contrario, se realiza una selección probabilística por ruleta (exploración)". Es el mismo mecanismo que en algoritmos genéticos se conoce también como fitness-proportionate selection.

  Cómo funciona en términos generales

  1. Tenés un conjunto de opciones, cada una con una probabilidad $P_i$ (que suman 1, como tu $P(c \to v)$).
  2. Armás la función de distribución acumulada (CDF): ordenás las opciones y vas sumando las probabilidades una tras otra, como si fueran "porciones" de una ruleta.
  3. Tirás un número aleatorio uniforme $r \sim U(0,1)$.
  4. Elegís la opción en cuyo "intervalo acumulado" cae $r$.

  La opción con mayor probabilidad ocupa una porción más grande de la ruleta, así que tiene más chances de ser elegida — pero cualquier opción con probabilidad $>0$ puede salir. Eso es
  justo lo que buscás en Fase 1: no siempre el vehículo/nodo "mejor" según feromona+heurística, pero sí el más probable.

## Fase 2

### Sistema de score
  $$\text{score}(i,j) = (\tau_{ij}^{ruta})^\alpha \cdot \eta_{ij}^\beta \cdot \mu_{ij}^\gamma$$

  Es una combinación multiplicativa de tres señales independientes, cada una capturando un aspecto distinto de "qué tan buena idea es ir de $i$ a $j$ ahora":

  1. $\tau_{ij}^{ruta}$ — memoria: cuánto reforzaron las iteraciones anteriores el hecho de visitar $j$ inmediatamente después de $i$.
  2. $\eta_{ij} = \dfrac{1}{t_{ij} + W_u \cdot s_j}$ — urgencia + cercanía: penaliza tanto la distancia/tiempo de viaje como lo pronto que cierra la ventana de $j$ (a través de $s_j$, su tiempo de inicio de servicio). Un cliente cercano y urgente puntúa alto.
  3. $\mu_{ij}$ — el ahorro de Clarke-Wright, que es tu duda.

  Al ser multiplicativo, cada término actúa como un "filtro": si cualquiera de los tres es muy bajo, el score total cae, sin importar que los otros sean altos. Los exponentes $\alpha, \beta, \gamma$ regulan cuánto peso relativo tiene cada señal.
### Ahorro de Clarke-Wright

  Qué significa esto en tu escenario real (sin regreso al depósito)

  Un NN/greedy puro elegiría simplemente el candidato con menor $d_{ij}$ o $d_{ik}$ (el más cercano a $i$, punto). El término $\mu$ le agrega un sesgo extra: preferí al candidato que, 
  además de estar cerca, esté lejos del depósito — aunque sea un poquito menos cercano que la otra opción.

  ¿Por qué querés ese sesgo si nunca volvés al depósito? Porque corrige exactamente el problema clásico de NN que ya charlamos antes: dejar un cliente lejano aislado para el final. Si $k$ está cerca de $i$ pero también cerca del depósito, y $j$ está un poco más lejos de $i$ pero mucho más lejos del depósito, un NN puro se iría por $k$ (más cerca) y dejaría a $j$ colgado — y como $j$ está lejos del depósito, atenderlo tarde en la ruta (o en otra ruta) sale caro. $\mu$ empuja a "aprovechar que estoy cerca de $j$ ahora" antes de que se vuelva un problema más adelante, mientras que a $k$ (cerca del depósito) lo podés "dejar para después" sin mucho costo adicional, porque siempre va a ser relativamente barato llegar a él.

Quiere  mitigar el caso en el que estoy al pedio entre un cliente cerca del return y otro un poco mas lejos. NN caeria en el que esta cerca del return y despues deja el mas aisalado para el final. Pero esta metrica incentiva a atender primero al mas lejano, porque eventualmente tengo que volver el return y puedo atander al cliente de pasada.

Lo que realmente compara $\mu$ entre dos candidatos.Tenés:

$$\mu_{ij} = \max(0,\ d_{i,dep} + d_{dep,j} - d_{ij}) + 1$$
$$\mu_{ik} = \max(0,\ d_{i,dep} + d_{dep,k} - d_{ik}) + 1$$

Como $i$ es el mismo nodo en ambos casos, el término $d_{i,dep}$ es común y se cancela al comparar (asumiendo que ambos ahorros son positivos, caso típico):

$$\mu_{ij} - \mu_{ik} = \underbrace{(d_{dep,j} - d_{dep,k})}{\text{qué tan más lejos del depósito está } j \text{ vs } k} - \underbrace{(d{ij} - d_{ik})}_{\text{qué tan más lejos de
} i \text{ está } j \text{ vs } k}$$

Es decir: no está comparando "conviene volver al depósito o no" (esa opción no está en juego para nada, y de hecho el término $d_{i,dep}$ desaparece de la comparación). Lo que está
comparando es algo mucho más simple: entre $j$ y $k$, ¿cuál es el que está más lejos del depósito relativo a lo cerca que está de $i$?
