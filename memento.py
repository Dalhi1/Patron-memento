import tkinter as tk
import sys
import subprocess
from tkinter import messagebox

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
# MEMENTO
# ---------------------------
class Memento:
    def __init__(self, state):
        self._state = state.copy()

    def get_state(self):
        return self._state


# ---------------------------
# ORIGINADOR
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
# CUIDADOR
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
# APP
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
        self.ventana_simulacion = None

        self.vars = {
            "ventanas": tk.BooleanVar(value=False),
            "puertas": tk.BooleanVar(value=False),
            "cinturon": tk.BooleanVar(value=False),
            "velocidad": tk.IntVar(value=120)
        }

        self.crear_ui()

    # ---------------------------
    # UI
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

        tk.Button(self.root, text="SIMULACION",
                  command=self.simulacion,
                  bg="#222", fg="white").pack(fill="x", padx=20, pady=10)

        self.estado = tk.Label(self.root,
                               text="Estado: Normal",
                               fg="#aaa", bg="#0b0b0b")
        self.estado.pack(pady=10)

    # ---------------------------
    # FUNCIONES
    # ---------------------------
    def actualizar_velocidad(self, v):
        self.vel_label.config(text=f"{v} km/h")

    def activar(self):
        self.seguridad.set_config(True, True, True, 60)
        self.cargar_ui()
        self.modo_infantil_activo = True
        self.estado.config(text="Modo infantil activado", fg="#00ff00")
        sonido_ok()

        # Bloquear botones y escala
        for btn in self.btns.values():
            btn.config(state="disabled")
        self.scale.config(state="disabled")

    def restaurar(self):
        self.seguridad.set_config(False, False, False, 120)
        self.cargar_ui()
        self.modo_infantil_activo = False
        self.estado.config(text="Restablecido", fg="#ffaa00")
        sonido_restore()

        
        for btn in self.btns.values():
            btn.config(state="normal")
        self.scale.config(state="normal")

    def cargar_ui(self):
        config = self.seguridad.config

        for key in ["ventanas", "puertas", "cinturon"]:
            valor = config[key]
            self.vars[key].set(valor)
            btn = self.btns[key]
            btn.config(text="ON" if valor else "OFF",
                       bg="#00aa00" if valor else "#550000")

        self.vars["velocidad"].set(config["velocidad"])
        self.scale.set(config["velocidad"])

        self.vel_label.config(text=f"{config['velocidad']} km/h")
        

    #  SIMULACIÓN CON DATOS
    def simulacion(self):
        # Verificar si ya hay una ventana abierta
        if self.ventana_simulacion and self.ventana_simulacion.winfo_exists():
            sonido_error()
            messagebox.showwarning("Advertencia", "Ya hay una simulación abierta.")
            return

        self.ventana_simulacion = tk.Toplevel(self.root)
        self.ventana_simulacion.title("Simulación")
        self.ventana_simulacion.geometry("600x500")

        velocidad = self.vars["velocidad"].get()
        ventana = self.vars["ventanas"].get()
        puertas = self.vars["puertas"].get()
        cinturon = self.vars["cinturon"].get()

        tk.Label(self.ventana_simulacion, text=f"Velocidad: {velocidad} km/h", fg="#fff", bg="#222", font=("Arial", 14)).pack(side="top")
        tk.Label(self.ventana_simulacion, text=f"Ventanas bloqueadas: {'Sí' if ventana else 'No'}", fg="#fff", bg="#222", font=("Arial", 14)).pack(side="top")
        tk.Label(self.ventana_simulacion, text=f"Puertas bloqueadas: {'Sí' if puertas else 'No'}", fg="#fff", bg="#222", font=("Arial", 14)).pack(side="top")
        tk.Label(self.ventana_simulacion, text=f"Cinturón obligatorio: {'Sí' if cinturon else 'No'}", fg="#fff", bg="#222", font=("Arial", 14)).pack(side="top")


# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
