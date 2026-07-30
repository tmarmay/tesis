### Cobertura
Comenzamos el analisis con este primer grafico que muestra la cobertura de cada metodologia.  En el eje x vemos la cantidad de clientes y en el eje y el porcentaje de cada metodologia de como se desempeno para esa cantidad de clientes 

Como se puede ver a primera vista hay una dominancia de Gurobi y Aco y como Highs con el aumento de los clientes pierde cobertura.

En cuanto a TWNN de las 15 instancias generadas constructivamente resolvio 15, mostrando el sesgo del que hablabamos, pero de las 15 instancias aleatorias solo pudo resolver 3. Y en las que mejor desempeno tuvo fue en aquellas que la cantidad de vehiculos era igual a la de los clientes (porque una solucion es asignarle un vehiculo a cada cliente) y en las que sobraban vehiculos.

 Pasando los solvers MILP pareciera que partir de la bracha de los 50 clientes (70 para gurobi) comienza a perder cobertura. Los graficos a continuacion buscan explicar porque pasa esto y para los casos en los que los solvers resolvieron la misma instancias comparar dichas resoluciones

### Flujo de ejecuciones MILP y ACO
bla bla

Pasamos a ver unos graficos que nos explican el uso de recursos de cada metodologia.

### Uso de RAM
Este grafico nos hace concluir dos cosas:
1. TWNN y ACO en terminos de memoria crecer el tamano del problema no impacta significativamente el uso de la memoria
2. Que tan grande es la estructura que necesita MILP para poder resolver el problema 

Si nos enfocamos puntualmente en MILP podemos ver en el siguiente grafico como evoluciona el uso de memoria segun crece el tamano de la instancia
### Uso de RAM MILP
Este grafico refleja lo que deciamos antes, que si decidieramos evaluar sobre mas cantidad de vehiculos o clientes, los solvers MILP empeorarian, porque a partir de N = 150 todo termina por limite de memoria (OOM) sin solucion.
Algo a marcar para este grafico es que del 100% de las instancias que termina por memoria, el 62.5% es de HIGHS y el 37.5 % restante es de Gurobi. Lo que nos dice que Gurobi tiene un mejor manejo de memoria 

Ahora pasemos a ver el uso de CPUS
### Uso de CPU
Clave aclarar que TWNN Y ACO no fueron disenados para usar mas de un CPU, y hacerlo podria ser un alinea de trabajo futuro, que sin duda mejoraria el rendimiento (mas que todo en ACO).

Lo que hay que quedarse de este grafico, es que gurobi de por si ya se auto gestiona los CPU disponibles, a diferencia de HIGHS, lo que deberia implicar que reliza computo en paralelo y por ello deberia ser mas rapido que HIGHs.

AVERIGUAR SI HIHGS PUEDE USAR MAS DE UN CPU

### Escalabilidad
Este grafico, muestra dimencion del problema vs el tiempo en escala logaritmica. 
Podemos notar que apartir de N=50 aproximadamente, HIGHS y Gurobi comienzan a realizar timeouts. Y a partir de N=160 se detienen. Esto no es porque los solvers se vuelvan más eficientes para instancias grandes, sino que a partir de ese tamano comienzan a pegarle al limite de memoria y finalizando el programa. 

De los timeouts registrados, el 44% es de gurobi y el 56% de Highs. 

Ahora pasemos a ver la calidad de las soluciones. Es importante aclarar que para que las comparaciones sean justas, en cada grafico se limito al conjunto en comun que comparten los solvers graficados en cuanto a instancias resueltas

### Distribucion de costos
En este grafico se analiza el resultado de 18 instancias, que son las que los cuatro solvers resolvieron, limitados por TWNN. 
Podemos notar una gran diferencia entre TWNN y el resto, no estan ni en la misma escala por lo que de ahora en mas no vamos a tener en cuenta a TWNN porque ya quedo claro que no es competitivo, pero este grafico nos muestra cuando podriamos optimizar si pasamos a metodos con asignaciones mas inteligentes

### Gap
Como sabemos los metodos exactos van a llegar a la mejor solucion, por lo que vamos a querer comparar las soluciones que generamos contra la mejor solucion concocida. Y como ya vimos, Gurobi demostro ser mejor que Highs, por lo que nos quedamos con Gurobi como referencia y graficamos el gap contra el. 

INTERPRETAR BIEN EL GRAFICO DE CAJAS !!!

En este grafico la metodologia limitante pasa a ser HIGHS con 20/30 instancias resueltas.
Podemos observar como highs tiene mucha mas dispercion. Antes de la optimizacion de hiper-parametros ACO presentaba una dispercion parecida, y miren como la pudimos achicar, simplemente modificando los hiper-parametros. 

Para el punto en el que highs registra un gap negativo, significa que highs le gano a gurobi en costos, osea encontro una solucion mas barata.

Y ahora podriamos pensar que  un gap medio de 30% puede parecer mucho, como que estamos lejos del optimo. Pero hay que tener en cuanta que estamos comparando un algoritmo que esta corriendo solo 80segundos en un solo CPU, y no esta lejos DEL MEJOR SOLVER COMERCIAL

### Costo en el tiempo de ACO
Durante el analisis post ejecuciones, pensamos: Y si ACO corriera el mismo tiempo que MILP, que tan buena seria la solucion ? De ahi nace este grafico.

Muestra como evoluciona el costo en el tiempo si lo dejarimos correr mas de los 80 segundos, y basta con darle un cuarto del tiempo del que usa MILP para alcanzar una solucion un 10% mejor 
Despues entra en una meseta en la que no puede salir por el resto de la ejecucion, lo qu eindicaria que llegamos al limite que le podemos sacar a ACO por limitaciones estructurales. 

Uno de los trabajos futuros propuesto fue hacer que cada hormiga corra en paralelo, ya que son independientes, sale casi directo.  Esto nos permitira correr en los mismos 80segundos mas iteraciones y obtener mejores resoltados


### Uso de vehiculos
Antes de introducir algunas mejores en el algoritmo base de ACO, teniamos un gap mas grande con Gurobi. A lo que salio la pregunta: como podemos ver esa diferencia en la solucion.

Comenzamos analisando el uso de vehiculos por metodologia. Esta claro que TWNN no le queda otra que usar vehiculos por la falta de inteligencia. Y cada vehiculo agregado inecesariamente pesa porque son mas salidas del deposito y mas viajes de vuelta, mas los costos fijos.

Entonces vimos que ACO estaba usando inecesariamente mas vehiculos, por lo que decidimos agregarle un modulo al finalizar el algoritmo que hace que agarra la solucion final e intenta mejorarla eliminando vehiculos, re-ubicando los clientes a distintas rutas
El resultado es el que estan viendo, bastante simular a la cantidad de vehiculos que usa Gurobi

### Asignaciones
Por ultimo este grafico, que es un ejemplo visual de una instancia puntual, del uso de vehiculos y ruteo de cada metodologia. 