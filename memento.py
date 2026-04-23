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
    
    def sonido_choque_sintetico():
            # 1. El impacto inicial (un golpe grave y seco)
        winsound.Beep(300, 150) 
        
        # 2. El "crujido" del metal (secuencia descendente rápida)
        winsound.Beep(250, 100)
        winsound.Beep(200, 100)
        winsound.Beep(150, 150)
        
        # 3. El sonido final de restos/metal (un tono muy grave)
        winsound.Beep(100, 250)
else:
    def sonido_ok(): print("\a")
    def sonido_restore(): print("\a")
    def sonido_error(): print("\a")
    def sonido_choque_sintetico(): print("\a")


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
        ##test
        self.animacion_id = None

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
        
        self.perfiles = tk.Label(self.root,
                               text="Elige un perfil",
                               fg="#aaa", bg="#0b0b0b")
        self.perfiles.pack(pady=10)
        
        tk.Button(self.root, text="Seguro",
                  command=self.cambioperfil("Seguro"),
                  bg="green", fg="black").pack(fill="x", padx=5, pady=3)
        
        tk.Button(self.root, text="Normal",
                  command=self.cambioperfil("Normal"),
                  bg="yellow", fg="black").pack(fill="x", padx=1, pady=1)
        
        tk.Button(self.root, text="MUERTE",
                  command=self.cambioperfil("MUERTE"),
                  bg="red", fg="black").pack(fill="x", padx=1, pady=1)
        
    def cambioperfil(self, perfil):
        if perfil == "Seguro":
            self.vars["velocidad"].set(40)
        elif perfil == "Normal":
            self.vars["velocidad"].set(120)
        elif perfil == "MUERTE":
            self.vars["velocidad"].set(180)
        else:
            return
        
        self.cargar_ui()


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
        self.ventana_simulacion.protocol("WM_DELETE_WINDOW", self.cerrar_simulacion)
        self.ventana_simulacion.title("Simulación")
        self.ventana_simulacion.geometry("1000x900")

       
        velocidad = self.vars["velocidad"].get()
        ventana = self.vars["ventanas"].get()
        puertas = self.vars["puertas"].get()
        cinturon = self.vars["cinturon"].get()
        #variables


        tamaño_letra = 10

        tk.Label(self.ventana_simulacion, text=f"Velocidad: {velocidad} km/h ,Ventanas bloqueadas: {'Sí' if ventana else 'No'}, Puertas bloqueadas: {'Sí' if puertas else 'No'}, Cinturón obligatorio: {'Sí' if cinturon else 'No'}", fg="#fff", bg="#222", font=("Arial",tamaño_letra)).pack(side="top", fill="x")


        self.canvas = tk.Canvas(self.ventana_simulacion, width=900, height=250, bg="#0b0b0b")
        self.canvas.pack(padx=10, pady=10)
        
        # Dibujar el obstáculo (un bloque rojo al final del canvas)
        self.obstaculo = self.canvas.create_rectangle(750, 150, 780, 220, fill="gray", outline="black")
        
        self.partes_carro = []

        # Chasis (Cuerpo principal - rectángulo azul)
        chasis = self.canvas.create_rectangle(50, 150, 200, 200, fill="blue", outline="black")
        self.partes_carro.append(chasis)

        # Techo (Parte superior - rectángulo azul más pequeño)
        techo = self.canvas.create_rectangle(80, 110, 170, 150, fill="blue", outline="black")
        self.partes_carro.append(techo)

        # Ventanas (dos rectángulos celestes)
        ventana1 = self.canvas.create_rectangle(90, 120, 120, 145, fill="lightcyan", outline="black")
        ventana2 = self.canvas.create_rectangle(130, 120, 160, 145, fill="lightcyan", outline="black")
        self.partes_carro.append(ventana1)
        self.partes_carro.append(ventana2)

        # Llantas (dos círculos negros con centro gris)
        llanta_trasera = self.canvas.create_oval(70, 180, 110, 220, fill="black", outline="black")
        llanta_delantera = self.canvas.create_oval(140, 180, 180, 220, fill="black", outline="black")
        centro_trasero = self.canvas.create_oval(85, 195, 95, 205, fill="gray", outline="black")
        centro_delantero = self.canvas.create_oval(155, 195, 165, 205, fill="gray", outline="black")
        self.partes_carro.extend([llanta_trasera, llanta_delantera, centro_trasero, centro_delantero])
        
        
        
        self.animar()    
    
    def animar(self):
        
        kmh = self.vars["velocidad"].get()
        paso_pixeles = self.calcular_paso_pixeles(kmh)
        velocidad_animacion =20
        altura_canvas = 250
        ancho_canva= 900
        
        # 1. Obtener coordenadas actuales del chasis y del obstáculo
        coord_chasis = self.canvas.coords(self.partes_carro[0]) # [x1, y1, x2, y2]
        coord_obs = self.canvas.coords(self.obstaculo)          # [ox1, oy1, ox2, oy2]
        
        # 2. DETECCIÓN DE COLISIÓN
        # Si el borde derecho del chasis (coord_chasis[2]) toca el izquierdo del obstáculo (coord_obs[0])
        if coord_chasis[2] >= coord_obs[0]:
            print("¡COLISIÓN!")
            sonido_choque_sintetico()
            # Aquí termina la función y NO llamamos a after(), por lo que se detiene.
            return
            
        for parte in self.partes_carro:
            self.canvas.move(parte, paso_pixeles, 0)

        # Verificar si el carro salió de la pantalla para reiniciarlo
        # Obtenemos las coordenadas del chasis (la primera parte) [x1, y1, x2, y2]
        coord_chasis = self.canvas.coords(self.partes_carro[0])
        
        # Si el borde izquierdo del chasis supera el ancho de la ventana
        if coord_chasis[0] > ancho_canva:
            ancho_carro = 150
            distancia_reinicio = -(ancho_canva + ancho_carro)
            for parte in self.partes_carro:
                self.canvas.move(parte, distancia_reinicio, 0)

        # Volver a llamar a esta función después de VELOCIDAD_MS
        self.animacion_id = self.root.after(velocidad_animacion, self.animar)
        
    def detener_animacion(self):
        if self.animacion_id:
            self.root.after_cancel(self.animacion_id)
            self.animacion_id = None
            
    def cerrar_simulacion(self):
        self.detener_animacion()
        self.ventana_simulacion.destroy()
        
    def calcular_paso_pixeles(self, kmh):
        v_min, v_max = 40, 180
        dest_min, dest_max = 1, 20
        
        # Aplicamos la fórmula
        velocidadF = ((kmh - v_min) * (dest_max - dest_min) / (v_max - v_min)) + dest_min
        
        # Retornamos el valor como entero, ya que los píxeles no tienen decimales
        return int(velocidadF)
            

# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
