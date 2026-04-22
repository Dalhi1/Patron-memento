import tkinter as tk
import time
import sys

ANCHO_VENTANA = 600
ALTO_VENTANA = 300
VELOCIDAD_MS = 20


velocidad = 120
cinturon = False
puertas = False
ventanas = False

if len(sys.argv) >= 5:
    velocidad = int(sys.argv[1])
    cinturon = sys.argv[2] == "True"
    puertas = sys.argv[3] == "True"
    ventanas = sys.argv[4] == "True"


class CarroAnimado:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=ANCHO_VENTANA, height=ALTO_VENTANA, bg="white")
        self.canvas.pack()

        self.start_time = time.time()
        self.ha_chocado = False

        self.velocidad = velocidad
        self.cinturon = cinturon
        self.puertas = puertas

        self.carro = self.canvas.create_rectangle(50, 150, 150, 200, fill="red")

        self.animar()

    def animar(self):
        tiempo = time.time() - self.start_time

        if not self.ha_chocado:
            movimiento = max(2, int(self.velocidad / 20))
            self.canvas.move(self.carro, movimiento, 0)

            if (
                self.velocidad > 120 or
                not self.cinturon or
                not self.puertas
            ):
                if tiempo > 3:
                    self.ha_chocado = True
                    self.canvas.itemconfig(self.carro, fill="black")

                    mensaje = "¡¡CRASH!!\n"
                    if self.velocidad > 120:
                        mensaje += "Alta velocidad\n"
                    if not self.cinturon:
                        mensaje += "Sin cinturón\n"
                    if not self.puertas:
                        mensaje += "Puertas abiertas\n"

                    self.canvas.create_text(
                        300, 100,
                        text=mensaje,
                        font=("Arial", 14, "bold"),
                        fill="red"
                    )

        self.root.after(VELOCIDAD_MS, self.animar)


if __name__ == "__main__":
    root = tk.Tk()
    app = CarroAnimado(root)
    root.mainloop()
