Antes de ver los resultados nos pongamos de acuerdo en algunas cosas. 
1. Las ejecuciones tienen un tiempo limite de 20 min, luego de eso se considera timeout
	- Esto fue implementado para las metologias milp
	- Por el funcionamiento de los solvers milp,  la mayoria de las veces vamos a tener una solucion cuando se realice el timeout (no la optima pero si una solucion)
2. Aregamos un limite de RAM (tambien por los solvers milp), pero en este caso si le pega al limite se corta el programa sin obtener una solucion.
Con lo anterior nos quedan estos posibles estados:
- finished: puede contener una solucion o no
- oom: sin solucion
- timeout: puede contener una solucion o no

Al finalizar la ejecucion de una instancia (en caso de que se obtenga solucion), se chequea que se cumpla todas las restricciones

