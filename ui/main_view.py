import tkinter as tk
from tkinter import messagebox, ttk
from servicios.restaurante_servicio import RestauranteServicio


class MainView(tk.Frame):
    codigo_var: tk.StringVar
    nombre_var: tk.StringVar
    categoria_var: tk.StringVar
    precio_var: tk.StringVar
    stock_var: tk.StringVar
    tabla_productos: ttk.Treeview

    def __init__(self, master, restaurante_servicio: RestauranteServicio, on_logout):
        super().__init__(master)
        self.master = master
        self.servicio = restaurante_servicio
        self.on_logout = on_logout
        self.codigo_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.categoria_var = tk.StringVar()
        self.precio_var = tk.StringVar()
        self.stock_var = tk.StringVar()

        self.pack(padx=20, pady=20, fill="both", expand=True)
        self._crear_widgets()

    def _crear_widgets(self):
        ttk.Label(
            self,
            text="Panel Principal - Restaurante",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        self.frame_productos = ttk.Frame(notebook, padding=10)
        notebook.add(
            self.frame_productos,
            text=f"Productos ({self.servicio.cantidad_productos()})"
        )
        self._crear_seccion_productos()

        frame_usuarios = ttk.Frame(notebook, padding=10)
        notebook.add(
            frame_usuarios,
            text=f"Usuarios ({self.servicio.cantidad_usuarios()})"
        )
        self._crear_seccion_usuarios(frame_usuarios)

        ttk.Button(self, text="Cerrar Sesión", command=self.on_logout).pack(pady=10)

    def _crear_seccion_productos(self):
        formulario = ttk.LabelFrame(
            self.frame_productos,
            text="Datos del producto",
            padding=10
        )
        formulario.pack(fill="x", pady=(0, 10))

        campos = (
            ("Código", self.codigo_var),
            ("Nombre", self.nombre_var),
            ("Categoría", self.categoria_var),
            ("Precio", self.precio_var),
            ("Stock", self.stock_var),
        )

        for columna, (texto, variable) in enumerate(campos):
            ttk.Label(formulario, text=texto).grid(
                row=0, column=columna, padx=4, pady=(0, 4), sticky="w"
            )
            ttk.Entry(formulario, textvariable=variable, width=18).grid(
                row=1, column=columna, padx=4, sticky="ew"
            )

        for columna in range(len(campos)):
            formulario.columnconfigure(columna, weight=1)

        botones = ttk.Frame(self.frame_productos)
        botones.pack(fill="x", pady=(0, 10))
        ttk.Button(
            botones,
            text="Registrar",
            command=self._registrar_producto
        ).pack(side="left", padx=(0, 5))
        ttk.Button(
            botones,
            text="Actualizar",
            command=self._actualizar_producto
        ).pack(side="left", padx=5)
        ttk.Button(
            botones,
            text="Eliminar",
            command=self._eliminar_producto
        ).pack(side="left", padx=5)
        ttk.Button(
            botones,
            text="Refrescar",
            command=self._refrescar_productos
        ).pack(side="left", padx=5)

        tabla_frame = ttk.Frame(self.frame_productos)
        tabla_frame.pack(fill="both", expand=True)

        columnas = ("codigo", "nombre", "categoria", "precio", "stock")
        self.tabla_productos = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            height=10
        )
        encabezados = {
            "codigo": "Código",
            "nombre": "Nombre",
            "categoria": "Categoría",
            "precio": "Precio",
            "stock": "Stock",
        }
        for columna in columnas:
            self.tabla_productos.heading(columna, text=encabezados[columna])
            self.tabla_productos.column(columna, width=120, anchor="center")

        scrollbar = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=self.tabla_productos.yview
        )
        self.tabla_productos.configure(yscrollcommand=scrollbar.set)
        self.tabla_productos.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self._refrescar_productos()

    def _crear_seccion_usuarios(self, frame_usuarios):
        columnas = ("identificacion", "nombre", "correo")
        tabla_usuarios = ttk.Treeview(
            frame_usuarios,
            columns=columnas,
            show="headings",
            height=12
        )
        encabezados = {
            "identificacion": "Identificación",
            "nombre": "Nombre",
            "correo": "Correo",
        }
        for columna in columnas:
            tabla_usuarios.heading(columna, text=encabezados[columna])
            tabla_usuarios.column(columna, width=180, anchor="center")

        tabla_usuarios.pack(fill="both", expand=True)
        for usuario in self.servicio.listar_usuarios():
            tabla_usuarios.insert(
                "",
                "end",
                values=(usuario.identificacion, usuario.nombre, usuario.correo)
            )

    def _refrescar_productos(self):
        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)

        for producto in self.servicio.listar_productos():
            self.tabla_productos.insert(
                "",
                "end",
                values=(
                    producto.codigo,
                    producto.nombre,
                    producto.categoria,
                    f"{producto.precio:.2f}",
                    producto.stock
                )
            )

    def _registrar_producto(self):
        try:
            precio = float(self.precio_var.get())
            stock = int(self.stock_var.get())
        except ValueError:
            messagebox.showerror(
                "Error",
                "El precio debe ser decimal y el stock debe ser entero."
            )
            return

        resultado, mensaje = self.servicio.registrar_producto(
            self.codigo_var.get(),
            self.nombre_var.get(),
            self.categoria_var.get(),
            precio,
            stock
        )
        self._mostrar_resultado(resultado, mensaje)
        if resultado:
            self._refrescar_productos()
            self._limpiar_formulario()

    def _actualizar_producto(self):
        try:
            precio = float(self.precio_var.get())
            stock = int(self.stock_var.get())
        except ValueError:
            messagebox.showerror(
                "Error",
                "El precio debe ser decimal y el stock debe ser entero."
            )
            return

        resultado, mensaje = self.servicio.actualizar_producto(
            self.codigo_var.get(),
            self.nombre_var.get(),
            self.categoria_var.get(),
            precio,
            stock
        )
        self._mostrar_resultado(resultado, mensaje)
        if resultado:
            self._refrescar_productos()

    def _eliminar_producto(self):
        codigo = self.codigo_var.get().strip()
        resultado, mensaje = self.servicio.eliminar_producto(codigo)
        self._mostrar_resultado(resultado, mensaje)
        if resultado:
            self._refrescar_productos()
            self._limpiar_formulario()

    def _mostrar_resultado(self, resultado, mensaje):
        if resultado:
            messagebox.showinfo("Operación exitosa", mensaje)
        else:
            messagebox.showerror("Error", mensaje)

    def _limpiar_formulario(self):
        for variable in (
            self.codigo_var,
            self.nombre_var,
            self.categoria_var,
            self.precio_var,
            self.stock_var,
        ):
            variable.set("")
