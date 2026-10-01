import tkinter as tk
from tkinter import messagebox
from servicios.restaurante_servicio import RestauranteServicio

class LoginView(tk.Frame):
    def __init__(self, master, restaurante_servicio: RestauranteServicio, on_login_success):
        super().__init__(master)
        self.master = master
        self.servicio = restaurante_servicio
        self.on_login_success = on_login_success

        self.pack(fill="both", expand=True)
        self._crear_widgets()

    def _crear_widgets(self):
        # Fondo y tarjeta central del formulario.
        azul_marino = "#10243A"
        dorado = "#C9A45C"
        blanco = "#FFFFFF"
        self.configure(bg=azul_marino)

        tarjeta = tk.Frame(self, bg=blanco, padx=34, pady=26)
        tarjeta.place(relx=0.5, rely=0.5, anchor="center")

        tk.Frame(tarjeta, bg=dorado, height=4).pack(fill="x", pady=(0, 20))

        # Encabezado del restaurante.
        tk.Label(
            tarjeta,
            text="Mi-Restaurante Jaramillo",
            font=("Arial", 19, "bold"),
            fg=azul_marino,
            bg=blanco
        ).pack(pady=(0, 5))
        tk.Label(
            tarjeta,
            text="Inicio de Sesión",
            font=("Arial", 13),
            fg="#657386",
            bg=blanco
        ).pack(pady=(0, 20))

        # Campos de acceso.
        tk.Label(
            tarjeta,
            text="Identificación",
            font=("Arial", 10, "bold"),
            fg=azul_marino,
            bg=blanco,
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        self.txt_identificacion = tk.Entry(
            tarjeta,
            font=("Arial", 12),
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground="#D8DEE6",
            highlightcolor=dorado
        )
        self.txt_identificacion.pack(fill="x", ipady=8, pady=(0, 15))

        tk.Label(
            tarjeta,
            text="Contraseña",
            font=("Arial", 10, "bold"),
            fg=azul_marino,
            bg=blanco,
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        self.txt_clave = tk.Entry(
            tarjeta,
            show="*",
            font=("Arial", 12),
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground="#D8DEE6",
            highlightcolor=dorado
        )
        self.txt_clave.pack(fill="x", ipady=8, pady=(0, 22))

        # Acción principal.
        tk.Button(
            tarjeta,
            text="Ingresar",
            command=self._validar,
            font=("Arial", 12, "bold"),
            fg=blanco,
            bg=azul_marino,
            activeforeground=blanco,
            activebackground="#1C3957",
            relief="flat",
            cursor="hand2",
            height=2
        ).pack(fill="x")

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
            messagebox.showerror("Error", "Identificación o clave incorrecta...")