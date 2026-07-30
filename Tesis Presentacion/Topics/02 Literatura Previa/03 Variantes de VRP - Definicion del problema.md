
Hasta ahora ya vimos:
- El problema que queremos resolver [[01 Como se resuelve hoy]]
- Sabemos como modelarlo [[01 VRP]]
- Entendemos que hay muchas variantes de [[03 Variantes de VRP - Definicion del problema]]
- Y sabemos que no tenemos un trabajo previo del cual partir [[02 VRP en el agro]] 

Entonces ahora definamos cuales son nuestras resticciones y con ello fijamos una variante especifica de VRP. Esta claro que un VRP basico no es suficiente para modelar el problema, nos faltan mas restricciones

- Comenzamos con VRP basico
- Como los dadores de carga necesitan las maquinas para una cierta fecha (por ejemplo para empezar a cosechar), nos pasamos  a VRP-TW
- Como tenemos multiples transportistas, que parten de distintas ubicaciones, podemos considera que cada uno de ellos es como un deposito y pasamos a la variante MD-VRP-TW
- Como hay varios tipos de transportes, cada uno con disintas capacidades, caemos en la variante Fleet Size and Mix
- Como hay disintos vehiculos y cada transportista puede tener disintos costos fijos tenemos que agregar Varible Cost
- Y como eventualmente el transportista tiene que terminar su recorrido, y este puede ser distinto del punto de partida, agregamos la version de Open VRP

En resumen si convinamos las siglas de todas las restricciones tenemos un: HFV-MD-O-VRP-TW (Heterogeneous Fixed Plus Variable Cost Multi-Depot Open VRP with Time Windows), aunque no existe un nombre universalmente establecido para esta variante específica.
- Chiste con la fldsmrk 

A continuacion en [[01 Formulacion del modelo matematico]] damos la variante que modela nuestro problema