# Redundancia en la restricción de flota mínima (Ec. 2.13)

Nota para una futura revisión del modelo MILP presentado en `main-vFinal.tex`, Sección 2.3 (Notación y formulación matemática). No implica un error: la solución óptima del modelo no cambia.

## Contexto

El modelo incluye la restricción

```
sum_{k in V} u^k >= 1        (Ec. 2.13, \label{eq:minveh})
```

que exige que se active al menos un vehículo.

## Por qué es redundante

Fijado un cliente `c ∈ C`, la restricción de cobertura (Ec. 2.2, `\eqref{eq:cobertura}`) obliga a que exista exactamente un par `(k, j)` con `x_{cj}^k = 1`. Es decir, hay al menos un vehículo `k` con alguna variable `x_{ij}^k` distinta de cero.

Para ese mismo `k`, la restricción de activación (Ec. 2.12, `\eqref{eq:activacion}`)

```
sum_i sum_j x_ij^k <= |N| * u^k
```

tiene su lado izquierdo mayor que cero, lo que fuerza `u^k > 0` y, al ser `u^k` binaria, `u^k = 1`.

Por lo tanto, siempre que `C ≠ ∅` (siempre es el caso: no tiene sentido resolver una instancia sin clientes), la Ec. 2.2 + la Ec. 2.12 ya implican `sum_k u^k >= 1`. La Ec. 2.13 no agrega restricción nueva al espacio de soluciones factibles.

## Por qué no se elimina ahora

- No invalida ningún resultado ni análisis del informe: agregar restricciones redundantes no cambia el óptimo.
- El único costo posible es de rendimiento del solver: si el presolver de Gurobi/HiGHS no detecta la redundancia, el árbol de branch and bound puede terminar siendo marginalmente más grande. El orden de magnitud debería ser similar.
- La tesis ya fue defendida con esta formulación; modificarla ahora no aporta beneficio que justifique el riesgo de introducir un error al retocar el modelo matemático post-defensa.

## Mejora futura sugerida

Si se retoma el modelo MILP más adelante (por ejemplo, para las optimizaciones listadas en "Líneas de trabajo futuro" del documento), evaluar:

1. Eliminar la Ec. 2.13 y verificar empíricamente si el presolver ya la deducía (comparar tiempos de resolución con y sin ella).
2. Si se elimina, agregar una nota en el texto explicando por qué es redundante (el argumento de esta nota), para que quede documentado el razonamiento.

## Origen

Observación de corrección hecha por el director de tesis sobre el manuscrito, no incorporada al documento final por las razones arriba descriptas.
