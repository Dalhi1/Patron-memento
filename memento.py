import tkinter as tk
import sys

# ---------------------------
# Sonidos
# ---------------------------
if sys.platform == "win32":
    import winsound
    def sonido_ok(): winsound.Beep(1000, 150)
    def sonido_restore(): winsound.Beep(600, 150)
    def sonido_error(): winsound.Beep(300, 300)
else:
    def sonido_ok(): print("\a")
    def sonido_restore(): print("\a")
    def sonido_error(): print("\a")


# ---------------------------
# memento
# ---------------------------
class Memento:
    def __init__(self, state):
        self._state = state.copy()

    def get_state(self):
        return self._state


# ---------------------------
# originador
# ---------------------------
class SeguridadInfantil:
    def __init__(self):
        self.config = {
            "ventanas": False,
            "puertas": False,
            "cinturon": False,
            "velocidad": 120
        }

    def set_config(self, ventanas, puertas, cinturon, velocidad):
        self.config = {
            "ventanas": ventanas,
            "puertas": puertas,
            "cinturon": cinturon,
            "velocidad": velocidad
        }

    def create_memento(self):
        return Memento(self.config)

    def restore(self, memento):
        self.config = memento.get_state()


# ---------------------------
# cuidador
# ---------------------------
class Historial:
    def __init__(self):
        self._historial = []

    def guardar(self, memento):
        self._historial.append(memento)

    def deshacer(self):
        if self._historial:
            return self._historial.pop()
        return None


# ---------------------------
# App
# ---------------------------
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Seguridad Infantil")
        self.root.geometry("420x550")
        self.root.configure(bg="#0b0b0b")

        self.seguridad = SeguridadInfantil()
        self.historial = Historial()
        self.modo_infantil_activo = False

        self.vars = {
            "ventanas": tk.BooleanVar(value=False),
            "puertas": tk.BooleanVar(value=False),
            "cinturon": tk.BooleanVar(value=False),
            "velocidad": tk.IntVar(value=120)
        }

        self.crear_ui()

    # ---------------------------
    # Animacion
    # ---------------------------
    def hex_to_rgb(self, h):
        h = h.lstrip("#")
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    def rgb_to_hex(self, rgb):
        return "#%02x%02x%02x" % rgb

    def animar_color(self, widget, inicio, fin, pasos=10, delay=30):
        r1, g1, b1 = self.hex_to_rgb(inicio)
        r2, g2, b2 = self.hex_to_rgb(fin)

        def step(i=0):
            if i > pasos:
                return
            r = int(r1 + (r2 - r1) * i / pasos)
            g = int(g1 + (g2 - g1) * i / pasos)
            b = int(b1 + (b2 - b1) * i / pasos)
            widget.config(fg=self.rgb_to_hex((r, g, b)))
            self.root.after(delay, lambda: step(i + 1))

        step()

    def flash(self):
        original = self.root["bg"]
        self.root.config(bg="#003300")
        self.root.after(100, lambda: self.root.config(bg=original))

    # ---------------------------
    # ui
    # ---------------------------
    def crear_switch(self, texto, var):
        frame = tk.Frame(self.root, bg="#111")
        frame.pack(fill="x", padx=20, pady=5)

        tk.Label(frame, text=texto, fg="white", bg="#111").pack(side="left")

        btn = tk.Button(
            frame,
            text="OFF",
            width=6,
            bg="#550000",
            fg="white",
            relief="flat",
            command=lambda: self.toggle(var, btn)
        )
        btn.pack(side="right")
        return btn

    def toggle(self, var, btn):
        if self.modo_infantil_activo:
            return

        estado = not var.get()
        var.set(estado)

        if estado:
            btn.config(text="ON", bg="#00aa00")
        else:
            btn.config(text="OFF", bg="#550000")

    def crear_ui(self):
        tk.Label(self.root, text="SEGURIDAD INFANTIL",
                 fg="#ff0000", bg="#0b0b0b",
                 font=("Arial", 16, "bold")).pack(pady=10)

        self.indicador = tk.Label(self.root,
                                  text="● SISTEMA NORMAL",
                                  fg="#00ff00", bg="#000")
        self.indicador.pack(fill="x", padx=10, pady=5)

        self.btns = {}
        self.btns["ventanas"] = self.crear_switch("Ventanas bloqueadas", self.vars["ventanas"])
        self.btns["puertas"] = self.crear_switch("Puertas bloqueadas", self.vars["puertas"])
        self.btns["cinturon"] = self.crear_switch("Cinturón obligatorio", self.vars["cinturon"])

        self.vel_label = tk.Label(self.root,
                                  text="120 km/h",
                                  fg="#ffaa00", bg="#000",
                                  font=("Arial", 18))
        self.vel_label.pack(pady=5)

        self.scale = tk.Scale(self.root,
                              from_=40, to=180,
                              orient="horizontal",
                              variable=self.vars["velocidad"],
                              command=self.actualizar_velocidad,
                              bg="#111", fg="white")
        self.scale.pack(fill="x", padx=20)

        tk.Button(self.root, text="ACTIVAR MODO INFANTIL",
                  command=self.activar,
                  bg="#0066cc", fg="white").pack(fill="x", padx=20, pady=5)

        tk.Button(self.root, text="RESTAURAR",
                  command=self.restaurar,
                  bg="#444", fg="white").pack(fill="x", padx=20)

        self.estado = tk.Label(self.root,
                               text="Estado: Normal",
                               fg="#aaa", bg="#0b0b0b")
        self.estado.pack(pady=10)

    # ---------------------------
    # funciones
    # ---------------------------
    def actualizar_velocidad(self, v):
        self.vel_label.config(text=f"{v} km/h")

    def bloquear_controles(self, bloquear=True):
        estado = "disabled" if bloquear else "normal"

        for btn in self.btns.values():
            btn.config(state=estado)

        self.scale.config(state=estado)

    def activar(self):
        self.historial.guardar(self.seguridad.create_memento())

        # MODELO primero
        self.seguridad.set_config(True, True, True, 60)

        # UI sincronizada
        self.cargar_ui()

        self.modo_infantil_activo = True
        self.bloquear_controles(True)

        self.indicador.config(text="● MODO INFANTIL ACTIVO")
        self.animar_color(self.indicador, "#004400", "#00ff00")

        self.estado.config(text="Modo infantil activado (60 km/h)", fg="#00ff00")

        self.flash()
        sonido_ok()

    def restaurar(self):
        memento = self.historial.deshacer()

        if memento:
            self.seguridad.restore(memento)
            self.cargar_ui()

            self.modo_infantil_activo = False
            self.bloquear_controles(False)

            self.indicador.config(text="● SISTEMA NORMAL")
            self.animar_color(self.indicador, "#333300", "#00ff00")

            self.estado.config(text="Restaurado", fg="#ffaa00")
            sonido_restore()
        else:
            self.indicador.config(text="● ERROR")
            self.animar_color(self.indicador, "#440000", "#ff0000")

            self.estado.config(text="Sin historial", fg="#ff4444")
            sonido_error()

    def cargar_ui(self):
        config = self.seguridad.config

        for key in ["ventanas", "puertas", "cinturon"]:
            valor = config[key]
            self.vars[key].set(valor)

            btn = self.btns[key]

            if valor:
                btn.config(text="ON", bg="#00aa00")
            else:
                btn.config(text="OFF", bg="#550000")

        self.vars["velocidad"].set(config["velocidad"])
        self.scale.set(config["velocidad"])

        self.actualizar_velocidad(config["velocidad"])


# ---------------------------
# main
# ---------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()