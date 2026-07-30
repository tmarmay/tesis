El problema [[01 Como se resuelve hoy]] se da por la falta de un ente coordinador que posee el panorama completo.

Como funcionaria:
	- Pablo de Cordoba (que quiere llevar la maquina nueva a su campo) carga el en el 'Ente'
	- Tito de Buenos Aires (que quiere mover su maquina entre sus campos) carga el viaje en el 'Ente'
	- El 'Ente':
		- Ve la disponibilidad de todos los transportistas registrados 
			- Segun algun criterio calcula la mejor asignacion
				- El criterio depende del 'Ente', algunas opciones:
					- Cargas equilibradas para los transportistas = Todos tengan trabajos
					- Asignacion final mas barata
					- Asignacion que minimiza km recorridos
					- Asignacion que reduce el tiempo de atendido
			-  Para este caso decide que Maria busca la maquina de Tito en  Buenos Aires, y la lleva a Cordoba. En Cordoba busca la maquina de Pablo y la lleva  a Buenos Aires y vuelve a su casa

Este es uno solo de los escenarios que se puede dar y hay muchas matices que no estamos tocando. 
(Por lo que en la seccion de [[01 Formulacion del modelo matematico]] definimos la variante puntual del problemas que vamos a atacar)

Vehículos que salen de un depósito, visitan clientes, y vuelven, minimizando costo. Esto tiene nombre: es una variante del Vehicle Routing Problem [[01 VRP]].  Con VRP vamos a modelar este problema ya que el problema que acabamos de explicar puede ser encasillado como una variante de VRP.