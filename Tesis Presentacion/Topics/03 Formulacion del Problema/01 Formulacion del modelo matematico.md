Tener bien estudidado [[Lugar de pick-up != drop-down]]

Lo primero que tenemos que hacer, es saber que queremos minimizar. Una vez con el objetivo claro, vamos agregando las restricciones necesarias para llegar al modelo planteado.

En este trabajo, lo que se intenta es conseguir fletes al mejor precio. 

Dado que las transportistas cotizan por kilometro, buscamos minimizar los kilometros recorridos ($d_ij$) teniendo tambien en cuenta los gastos fijos de cada vehiculo. 
Recordemos que nuestro objetivo es disminuir los gastos del viaje, entonces se puede dar que tengamos 2 transportitas uno que para una orden tiene menos kilometros totales pero tiene gastos fijos muy altos por alguna razon. Entonces para ese caso vamos a querer elegir un transportista que tenga algunos km mas pero el precio final sea menor.

Esta es nuetra primera restriccion. Luego tenemos 12 restricciones mas, de las cuales 
(de 2.1 a 2.10) 10 son casi una copia de un paper de MD-VRP-TW con algunas modificaiones para que se adapte a nuestras necesidades, y las 3 restantes son propias completamente que garanzian que el modelo de soluciones validas, podemos llamarlas de integridad

Vale la pena mencionar, como mencionamos en los posibles trabajos a futuro, que podriamos modificar la funcion objetivo con el fin de atacar otras problematicas. Por ejemplo:
- Distribucion de cargas equitativas entre los transportistas para que no se haga un monopolio de viajes
- Minimizacion de tiempos de servicio: dejamos de pensar en los costos y porque ahora nos interesa atender todas las ordenes lo antes posible 