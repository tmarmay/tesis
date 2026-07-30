Otro de los objetivos de este trabajo era la implementacion de un framework que sea capaz de facilitarnos el proceso desde la generacion de instancias hasta la comparacion de resultados.  Que ademas si el dia de manana queremos agregar un solver mas tengamos que implentar una sola clase con un metodo y todo siga funcionado.

Una vez listo el framework, enfrantamos otro problema. Como vimos es una instancia muy especifica de VRP, por lo que no hay benchmarks 'conocidos' que podamos usar. Obviamente hay benchmarks conocidos de VRP y como nuestra version es mas amplias podriamos adaptar para  que corran dichos benchs, pero se decidio hacer instancias de prueba propias para este tipo de variante. Esto no es algo que no se haga, por ejemplo: en ambos ejemplos del campo que vimos anterioremente se disenaron instancias puntuales para los problemas que querian atacar.

Llegamos a implementar dos tipos de generadores de instancias. Los llame generadores porque tenemos muchas variables que podemos querer probar, por ej:
- como se comporta con precios muy grandes
- como se comporta con ventanas de tiempo amplias o mas justas
- como se comporta con muchos o pocos vehiculos
Obviamente no se podia incluir todas las variaciones, asique decidimos que parametros fijar y que otros variar.

En cuanto a los tipos de generadores hay que saber una diferencia importante:
- Generador constructivo: este generador situa a los clientes y vehiculos, luego los empareja por cercania respetando capacidad de cada vehiculo y por ultimo acomoda las ventanas de tiempo de forma que termine con una instancia que tenga solucion
	- Contras: 
		 - Contruye de una forma bastante parecida a TWNN y puede estar un poco sesgado en su favor
		- Puede no modelar instancias de la vida real (porque acomoda como si fuera ideal)
- Generador aleatorio: No contruye una solucion, y las ventanas de tiempo son generadas aleatoriamente, haciendo minimos chequeos para no generar instancias infeasibles a priori
	- Contras: 
		- no sabemos si lo que generemos tiene solucion o no, entonces no podemos saber si los solvers no encontraron solucion o no existe una solucion

Corrimos 15 instancias de cada generador para los 4 solvers, lo que nos da 120 ejecuciones para analizar