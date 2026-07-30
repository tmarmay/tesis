Big-M es una técnica estándar de linealización que se usa en programación lineal entera mixta para modelar lógica condicional o eliminar productos entre variables, algo que un solver
MILP no puede resolver directamente porque rompe la linealidad. La idea es introducir una constante $M$ suficientemente grande de modo que una restricción quede "desactivada"(siempre satisfecha, sin importar el resto de las variables) cuando cierta condición binaria no se cumple, y quede "activa" (imponiendo la restricción real) cuando sí se cumple.

Formalmente, si querés expresar la lógica "si $z=1$ entonces $f(x) \le 0$, si no, sin restricción", la reescribís como $f(x) \le M(1-z)$: cuando $z=1$, el lado derecho es 0 y recuperás la restricción real $f(x)\le 0$; cuando $z=0$, el lado derecho es $M$ (un número enorme), volviendo la restricción trivialmente cierta para cualquier valor factible de $x$.

La elección de $M$ es delicada: tiene que ser lo suficientemente grande para cubrir el peor caso posible de $f(x)$, pero no demasiado grande, porque un $M$ innecesariamente holgado
debilita las cotas del relajado lineal y empeora el desempeño del branch-and-bound (esto es justo lo que discutís en tu análisis de complejidad del modelo, Sección 3.3.3).

En tu tesis lo aplicás exactamente en la restricción (2.7), que en su forma original es no lineal porque multiplica la variable binaria $x_{ij}^k$ por una expresión continua:
$x_{ij}^k(s_i^k + t_{ij} - s_j^k) \le 0$. Siguiendo la técnica, la reescribís (implícitamente, según el texto de la pág. 6-7) como:

$$s_i^k + t_{ij} - s_j^k \le M_{ij}(1 - x_{ij}^k)$$

Cuando $x_{ij}^k = 1$ (el vehículo $k$ efectivamente viaja de $i$ a $j$), el lado derecho se anula y queda $s_j^k \ge s_i^k + t_{ij}$: el tiempo de inicio en $j$ debe ser al menos el tiempo de inicio en $i$ más el viaje, que es la propagación temporal real que querés forzar. Cuando $x_{ij}^k=0$ (ese arco no se usa), necesitás que la restricción no imponga nada, y ahí es donde entra $M_{ij} = l_i + t_{ij} - e_j$: es el valor más grande que puede tomar $s_i^k + t_{ij} - s_j^k$ dado que $s_i^k$ está acotado por $l_i$ (restricción 2.8, el cierre de ventana en $i$) y $s_j^k$ está acotado inferiormente por $e_j$ (la apertura de ventana en $j$). Al fijar $M_{ij}$ exactamente en esa cota — ni más ni menos — garantizás que la restricción quede inactiva cuando corresponde, sin aflojar de más el relajado lineal del modelo