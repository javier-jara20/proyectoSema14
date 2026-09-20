import tkinter as tk
from tkinter import messagebox
from servicios.restaurante_servicio import RestauranteServicio

class LoginView(tk.Frame):
    def __init__(self, master, restaurante_servicio: RestauranteServicio, on_login_success):
        super().__init__(master)
        self.master = master
        self.servicio = restaurante_servicio
        self.on_login_success = on_login_success

        self.pack(padx=20, pady=20)
        self._crear_widgets()

    def _crear_widgets(self):
        tk.Label(self, text="Inicio de Sesión", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Label(self, text="Identificación:").pack()
        self.txt_identificacion = tk.Entry(self)
        self.txt_identificacion.pack(pady=5)

        tk.Label(self, text="Clave (1234):").pack()
        self.txt_clave = tk.Entry(self, show="*")
        self.txt_clave.pack(pady=5)

        tk.Button(self, text="Ingresar", command=self._validar).pack(pady=10)

    def _validar(self):
        identificacion = self.txt_identificacion.get().strip()
        clave = self.txt_clave.get().strip()

        if not identificacion or not clave:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
            return

        # Llama a tu método validar_usuario
        usuario_valido = self.servicio.validar_usuario(identificacion, clave)

        if usuario_valido:
            self.on_login_success()
        else:
            messagebox.showerror("Error", "Identificación no registrada o clave incorrecta (use 1234).")