### Intro
La programación lineal (LP), introducida por George Dantzig en 1947 [4], permitió formular y resolver de manera sistemática una amplia clase de problemas de optimización bajo restricciones lineales. 
Se demostró que LP pertenece a la clase P, es decir, existe un algoritmo que lo resuelve en tiempo polinomial, lo que lo convierte en un problema tratable en la práctica.
Sin embargo, muchos problemas reales requieren decisiones discretas: si un vehículo hace o no un recorrido, si es activado o no. Al incorporar variables binarias o enteras se obtiene la Progra-mación Lineal Entera Mixta (MILP) [5], que puede representar estas decisiones con exactitud pero a un costo computacional significativamente mayor: un MILP es en general NP-Hard

### Implementacion	
Para poder realizar la implementacion, utilizamos el framework pyomo, que nos permite codificar las restricciones que vimos previamente.
Una vez codificadas las restricciones queda ver quien va a ser el solver que resuleva la instancia. Aca es donde agregamos un eje mas de comparacion al trabajo, porque hicimos los experimentos con dos solvers. 
Tenemos dos tipos de solvers: open source y comerciales. Representado a los de codigo abierto tenemos a Highs, desarollado por la universidad de edinburgo completamente gratuito y en desarollo activo. Por el otro lado tenemos al solver de referencia comercial Gurobi, que por ser estudiante pudimos sacar una licencia para utilizarlo.

Pyomo nos permite cambiando una sola linea podemos cambiar de solver 

Vale la pena mencionar que al principio se utilizaron dos solvers mas CBC y GLPK pero su rendimiento fue muy por debajo de los anteriores por lo que se desidio obviarlos

Una aclaracion importante es que en este trabajo jugamos con las distintas flags que tiene cada solver. Simpleente lo usamos como viene por defecto en pyomo y investigar distintas configuraciones para mejorar el rendimiento puede ser otra linea de trabajo futuro 

Como venimos diciendo, MILP si bien eventualmente (si tenemos los recursos) va a encontrar el optimo, no tenemos una garantia de cuanto tiempo le va a llegar. Por eso se decidio por un limite de tiempo a la ejecucion de 20min.
Aca es interesante entender como funcionan estos solvers, ya que comienzan con una solucion y en cada iteracion la van mejorando. Por lo que al usar el timeout podemos quedarnos con una solucion que es valida pero que no es optima. COMPLETAR!!!

### Complejidad
Por ultimo veamos rapidamente a que complejidad nos enfrentamos en terminos de cantidad de restricciones. 
En el trabajo podemos encontrar la forma en la que llegamos a esta ecuacion final, que sale de sumar la cantidad de ecuaciones que aporta cada restriccion . De ahi concluimos que el modelo tiene  $O(V * N^2)$ ecuaciones 
Para poner un número concreto, consideremos una instancia con |C| = 20 clientes y |V | =10 vehículos eso nos da un aproximado de 7000 términos 
Si se duplican ambos parámetros a |C| = 40 y |V | = 20, el mismo cálculo da 56.000 términos: ocho veces más para apenas el doble de clientes y vehículos


