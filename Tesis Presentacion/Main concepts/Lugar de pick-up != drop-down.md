### Porque no  hay una restriccion que refleje el viaje entre el pick up y drop off                                                                
  
  La razón por la que no hay una restricción explícita para el tramo pickup→drop-off está en la Sección 2.3, justo después de presentar la formulación
  matemática (2.1)–(2.13), y es una decisión de alcance deliberada, no un descuido.

  El argumento central: el modelo no necesita una restricción nueva porque el viaje cargado (origen→destino) no se modela como una decisión de ruteo — se modela como una redefinición 
  de los datos de entrada. Concretamente:

  $$c_{ij} = c_{\text{destination}_i, \text{origin}j} + c{\text{origin}j, \text{destination}j}$$
  $$t{ij} = t{\text{destination}_i, \text{origin}_j}$$

  y el tramo cargado propio de cada cliente, $t_{\text{origin}_i, \text{destination}_i}$, se incorpora como tiempo de servicio del cliente $i$ (el término $s_i^k$ que ya está en la formulación, ecuación 2.7). Es decir: en vez de agregar un nodo "pickup" y un nodo "drop-off" por cliente con una restricción de precedencia entre ellos, colapso ambos en un único nodo cliente $i$, y el costo/tiempo de "moverme dentro de ese cliente" queda absorbido en los pesos de las aristas y en el tiempo de servicio que el modelo ya contempla.

  Por qué esto es válido y no una trampa matemática: funciona porque asumo que el vehículo siempre completa el ciclo $origin_i \to destination_i$ antes de dirigirse al próximo cliente — nunca lleva simultáneamente la carga de dos clientes distintos. Bajo ese supuesto, el grafo de decisión no cambia de forma respecto al VRP base: seguís decidiendo un orden de visita sobre un conjunto de "clientes", solo que ahora cada "cliente" empaqueta un origen y un destino en vez de ser un punto único. La precedencia (recoger antes de entregar) y el acoplamiento (que sea el mismo vehículo el que hace ambas partes) no necesitan restricción explícita porque están garantizados por construcción, no por una ecuación adicional.

  Por qué no fui al PDP completo: un PDP general sí necesitaría esas restricciones explícitas de precedencia y acoplamiento, porque en el caso general un vehículo puede llevar simultáneamente la carga de varios clientes intercaladas (recoger a A, recoger a B, entregar a A, entregar a B), y ahí sí el orden entre pickup y drop-off deja de ser trivial y hay
  que forzarlo con restricciones. Pero en mi dominio — transporte de maquinaria agrícola — ese escenario no ocurre: la entrega es secuencial, no hay ventanas de tiempo en el destino, y no se contempla transportar pedidos de múltiples clientes de forma simultánea (una máquina agrícola ocupa el camión entero). Agregar la maquinaria de restricciones de un PDP general para un caso donde esas restricciones son estructuralmente redundantes hubiera sido complejidad innecesaria — y de hecho, extender el modelo al caso general con múltiples cargas simultáneas queda explícitamente como línea de trabajo futuro en la Sección 2.3.

### Y como se resuelve el tema de cambio de ubicacion ?

El "cambio de ubicación" es justamente el problema físico que resuelve la redefinición de $c_{ij}$ y $t_{ij}$ que mencioné antes — no es un tema aparte, es la razón de ser de esa redefinición. Se lo explico con más detalle porque es el punto fino que hace que el truco funcione.

El problema concreto: en el VRP base, cada nodo $i$ tiene una sola ubicación física, y $d_{ij}$ es simplemente la distancia entre dos puntos. Pero acá cada "cliente" en realidad son dos puntos distintos: $origin_i$ (donde el vehículo recoge la maquinaria) y $destination_i$ (donde la entrega). Eso significa que cuando el vehículo termina de atender al cliente $i$, no está parado en el mismo lugar donde empezó — arrancó en $origin_i$ pero al momento de partir hacia el próximo cliente está físicamente en $destination_i$. Si uno ingenuamente usara $t_{ij}$ o $c_{ij}$ como si $i$ fuera un punto único, el modelo estaría calculando mal el próximo tramo: asumiría que el vehículo viaja desde $origin_i$ (o algún punto ambiguo) hacia $j$, cuando en realidad viaja desde $destination_i$.

Cómo se resuelve: la redefinición ataca exactamente eso, referenciando el punto físico correcto en cada extremo del arco:

$$t_{ij} = t_{destination_i,\ origin_j}$$

Es decir, el tiempo de viaje "de $i$ a $j$" en el grafo comprimido no es una distancia abstracta entre dos nodos-cliente, sino literalmente el tiempo real de manejar desde el punto  de entrega de $i$ hasta el punto de recogida de $j$ — el tramo que el camión efectivamente recorre vacío. El cambio de ubicación queda resuelto porque el dato de entrada ya "sabe" dónde termina físicamente el vehículo después de $i$.

El tramo cargado propio de $i$ ($origin_i \to destination_i$) no desaparece, se reubica como tiempo de servicio $s_i^k$. Esto es válido porque la restricción de propagación temporal (2.7), $x_{ij}^k(s_i^k + t_{ij} - s_j^k) \le 0$, no le importa en qué se gasta el tiempo mientras se "atiende" al nodo $i$ — solo le importa que el reloj avance correctamente y se respete la ventana (2.8). Manejar con la carga puesta de $origin_i$ a $destination_i$ es, a efectos del modelo, indistinguible de "tiempo de servicio", así que absorberlo ahí no rompe nada.

Del lado del costo pasa algo simétrico pero con el vecino siguiente:

$$c_{ij} = c_{destination_i,\ origin_j} + c_{origin_j,\ destination_j}$$

acá se suma también el costo del tramo cargado de $j$ ($origin_j \to destination_j$) directamente en el arco de entrada a $j$. Esto garantiza que ese costo obligatorio se cuente exactamente una vez en la función objetivo (2.1), porque cada cliente tiene exactamente un arco entrante activo (restricción 2.2 + conservación de flujo 2.5).

Por qué esto alcanza y no hace falta más maquinaria: las variables de decisión $x_{ij}^k$ y $s_i^k$ nunca referencian coordenadas directamente — solo interactúan con el modelo a través de las matrices $c_{ij}$, $t_{ij}$ y el escalar $s_i^k$, que son datos de entrada, no estructura del modelo. Al redefinir esos datos para que reflejen la geometría real de dos puntos por cliente, el cambio de ubicación queda resuelto sin tocar ni una restricción de (2.2)–(2.13).
