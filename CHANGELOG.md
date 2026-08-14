# Changelog

Registro de cambios relevantes sobre el documento de tesis (`thesis/Tesis-Final-Correciones.pdf`).

## 2026-08-14

Correcciones sobre `thesis/Tesis-Final-Correciones.pdf`:

- **Notación**: `\eta` renombrado a `\eta^{asig}` (Fase 1) y `\eta^{ruta}` (Fase 2). El mismo símbolo representaba dos fórmulas distintas (distancia vs. tiempo+urgencia); ahora queda simétrico con `\tau^{asig}`/`\tau^{ruta}`.
- **Pseudocódigo**: agregado el label "Fase 3 — Actualización de feromonas" al Algoritmo 1. El texto en prosa ya nombraba esa fase pero el pseudocódigo la ejecutaba sin etiquetarla, rompiendo la correspondencia texto/algoritmo.
- **Traducción**: "Universidad de Edinburgh" → "Universidad de Edimburgo". El resto del documento está en español y el nombre en inglés quedaba como anglicismo suelto.
- **Preámbulo LaTeX**: agregado `\usepackage{amssymb}`. Sin él, `\lesssim` (usado en "$|N| \lesssim 50$") se descartaba en silencio en Overleaf y el PDF mostraba "|N|50" en vez de "≲".
- **Notación (Sección 2.3)**: reorganizada en índices/parámetros/variables, y definido explícitamente `N = C ∪ Depot ∪ Ret`. La lista mezclaba tipos de objetos sin distinguirlos y dejaba ambigua la relación entre `C` y `N`.
- **Terminología**: `s_i^k` renombrado de "tiempo de servicio" a "instante de servicio". Verificado en MILP, ACO y NN que `s_i^k` siempre representa un timestamp (momento de inicio), no una duración.
