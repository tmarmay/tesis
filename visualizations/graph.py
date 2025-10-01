import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

carriers = [1,2,3,4,5,6,7,8,9,10,11]

# ========= DATOS DE EJEMPLO =========
np.random.seed(0)

iters = 50  # número de iteraciones

# Distribuimos nodos en círculo
radius = 40
angles = np.linspace(0, 2*np.pi, len(carriers), endpoint=False)
coords = np.column_stack((radius * np.cos(angles), radius * np.sin(angles)))

# Tiempo transcurrido = eje x
time_elapsed = np.arange(iters)

# Costo simulado que va disminuyendo con algo de ruido
cost_t = np.linspace(500, 200, iters) + np.random.randn(iters) * 10

# ========= CREAR FIGURA =========
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# Panel izquierdo: Grafo VRP
ax1.set_title("Current Solution")
ax1.set_xlim(-60, 60)
ax1.set_ylim(-60, 60)

# Dibujar nodos
for i, (x, y) in enumerate(coords):
    if i == 0:
        ax1.scatter(x, y, c="black", s=250, marker="o", edgecolors="white", linewidths=2, alpha=0.8, zorder=3)
        ax1.text(x, y, str(carriers[i]), color="white", ha="center", va="center", fontsize=14, fontweight="bold", bbox=dict(facecolor='black', alpha=0.3, edgecolor='white', boxstyle='round,pad=0.3'))
    else:
        ax1.scatter(x, y, c="deepskyblue", s=250, edgecolors="dodgerblue", linewidths=2, alpha=0.7, zorder=3)
        ax1.text(x, y, str(carriers[i]), color="dodgerblue", ha="center", va="center", fontsize=14, bbox=dict(facecolor='white', alpha=0.7, edgecolor='deepskyblue', boxstyle='round,pad=0.3'))


# Panel derecho: Costo vs Iteraciones
ax2.set_title("Función costo por iteración")
ax2.set_xlabel("Tiempo")
ax2.set_ylabel("Costo")
ax2.set_xlim(0, iters)
ax2.set_ylim(0, 600)
line_cost, = ax2.plot([], [], "b-", label="Costo")
ax2.legend()

# ========= FUNCIÓN DE ACTUALIZACIÓN =========
edges_plot = []

def update(frame):
    global edges_plot
    # borrar aristas previas
    for ln in edges_plot:
        ln.remove()
    edges_plot = []

    # ruta aleatoria simulada (ejemplo)
    perm = np.random.permutation(range(1, len(carriers)))
    route = [0] + perm.tolist() + [0]

    # dibujar aristas
    for i in range(len(route) - 1):
        x = [coords[route[i], 0], coords[route[i+1], 0]]
        y = [coords[route[i], 1], coords[route[i+1], 1]]
        ln, = ax1.plot(x, y, "k-", alpha=0.7)
        edges_plot.append(ln)

    # actualizar curva de costo
    line_cost.set_data(range(frame+1), cost_t[:frame+1])

    return edges_plot + [line_cost]

# ========= CREAR ANIMACIÓN =========
anim = FuncAnimation(fig, update, frames=iters, interval=200, blit=False, repeat=False)

# Si tenés GUI (por ej. Jupyter Notebook o local con Tk/Qt):
# plt.show()

# En tu entorno (Agg, sin GUI), guardalo en GIF
anim.save("vrp_anim.mp4", writer="pillow", fps=1)
print("Animación guardada como vrp_anim.mp4")
