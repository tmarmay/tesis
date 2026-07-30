### Porque necesito MILP y no basta con LP
Sin embargo, muchos problemas reales requieren decisiones discretas: si un vehículo hace o no
un recorrido, si es activado o no. Al incorporar variables binarias o enteras se obtiene la Progra-
mación Lineal Entera Mixta (MILP)
### Como puede mejorarse el rendimiento
Existen estrategias para mitigar estas limitaciones. Kallehauge et al. [3] documentan, en
el contexto de métodos exactos para el VRPTW, mejoras atribuibles al preprocesamiento y la
poda de arcos infactibles según ventanas de tiempo y capacidades, a la eliminación de columnas
inactivas durante el proceso de generación de columnas, al parado temprano del subproblema
de precios en cuanto se genera una columna de costo reducido negativo, a la incorporación de
2-path cuts para reducir la brecha de integralidad, y a estrategias de branching sobre ventanas
de tiempo. Sin embargo, su implementación excede los objetivos de este trabajo.



