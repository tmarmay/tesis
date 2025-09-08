## Tesis: Asignación Óptima de Viajes para Transporte de Maquinaria Agrícola con Restricciones Temporales y Operativas

#### Tomas Marmay ~ Famaf 2025

### Estructura
Tesis/
│
├── solvers/                      # Algoritmos, cada uno en su módulo
│   ├── __init__.py
│   ├── nnp.py                    # NNP para MD-VRP-TW
│   ├── milp.py                   # MILP solver con HiGHS u otro
│   ├── aco.py                    # Ant Colony Optimization
│   └── utils_vrp.py              # Funciones comunes (distancias, factibilidad, TW)
|
├── models/                       # Representación de entidades del problema
│   ├── __init__.py
│   ├── user.py                   # Clase Usuario
│   ├── transportista.py          # Clase Transportista
│   ├── pedido.py                 # Clase Pedido / Orden de transporte
│   └── vehicle.py                # Clase Vehículo (si no está en transportista)
│
├── data/
│   ├── raw/                      # Datos originales o simulados crudos
│   ├── processed/                # Datos listos para correr experimentos
│   └── generators.py             # Script para crear datasets sintéticos
│
├── notebooks/
│   ├── 01_exploracion.ipynb       # Exploración de datos y definición del problema
│   ├── 02_corridas_nnp.ipynb      # Corridas del solver NNP
│   ├── 03_corridas_milp.ipynb     # Corridas del solver MILP
│   ├── 04_corridas_aco.ipynb      # Corridas del solver ACO
│   └── 05_comparacion_resultados.ipynb
│
├── results/
│   ├── logs/                      # Logs de ejecución
│   ├── rutas/                     # Rutas obtenidas en JSON/CSV
│   └── metricas/                  # Resultados agregados
│
├── config/
│   └── parametros.yaml            # Parámetros globales de ejecución
│
├── requirements.txt
├── README.md
└── main.py                        # Script para ejecutar experimentos completos
