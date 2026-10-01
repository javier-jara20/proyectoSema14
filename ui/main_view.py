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

        self.master.geometry("1180x760")
        self.master.minsize(900, 620)
        self.pack(fill="both", expand=True)
        self._crear_widgets()

    def _crear_widgets(self):
        self._configurar_estilos()

        contenedor = ttk.Frame(self, style="App.TFrame")
        contenedor.pack(fill="both", expand=True)

        barra_lateral = ttk.Frame(
            contenedor,
            width=220,
            style="Sidebar.TFrame"
        )
        barra_lateral.pack(side="left", fill="y")
        barra_lateral.pack_propagate(False)

        ttk.Label(
            barra_lateral,
            text="RESTAURANTE",
            style="SidebarBrand.TLabel"
        ).pack(anchor="w", padx=22, pady=(30, 2))
        ttk.Label(
            barra_lateral,
            text="JARAMILLO",
            style="SidebarName.TLabel"
        ).pack(anchor="w", padx=22, pady=(0, 30))

        contenido = ttk.Frame(contenedor, padding=(26, 22), style="App.TFrame")
        contenido.pack(side="left", fill="both", expand=True)
        ttk.Label(
            contenido,
            text="Panel de administración",
            style="PageTitle.TLabel"
        ).pack(anchor="w", pady=(0, 16))

        self.notebook = ttk.Notebook(contenido)
        self.notebook.pack(fill="both", expand=True)

        self.frame_productos = ttk.Frame(self.notebook, padding=16)
        self.notebook.add(
            self.frame_productos,
            text=f"Productos ({self.servicio.cantidad_productos()})"
        )
        self._crear_seccion_productos()

        self.frame_usuarios = ttk.Frame(self.notebook, padding=16)
        self.notebook.add(
            self.frame_usuarios,
            text=f"Usuarios ({self.servicio.cantidad_usuarios()})"
        )
        self._crear_seccion_usuarios(self.frame_usuarios)

        opciones = (
            ("🏠 Inicio", lambda: self.notebook.select(self.frame_productos), "Nav.TButton"),
            ("👥 Usuarios", lambda: self.notebook.select(self.frame_usuarios), "Nav.TButton"),
            ("🍔 Productos", lambda: self.notebook.select(self.frame_productos), "Nav.TButton"),
            ("💰 Ventas", lambda: None, "Nav.TButton"),
        )
        for texto, comando, estilo in opciones:
            boton = ttk.Button(
                barra_lateral,
                text=texto,
                command=comando,
                style=estilo
            )
            boton.pack(fill="x", padx=12, pady=3)
            if texto == "💰 Ventas":
                boton.state(["disabled"])

        ttk.Button(
            barra_lateral,
            text="Cerrar sesión",
            command=self.on_logout,
            style="Logout.TButton"
        ).pack(side="bottom", fill="x", padx=12, pady=18)

    def _configurar_estilos(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure("App.TFrame", background="#f2f5f8")
        estilo.configure("TFrame", background="#f2f5f8")
        estilo.configure("Sidebar.TFrame", background="#102a43")
        estilo.configure(
            "SidebarBrand.TLabel",
            background="#102a43",
            foreground="#e0b84f",
            font=("Arial", 10, "bold")
        )
        estilo.configure(
            "SidebarName.TLabel",
            background="#102a43",
            foreground="#ffffff",
            font=("Arial", 17, "bold")
        )
        estilo.configure(
            "Nav.TButton",
            background="#102a43",
            foreground="#f2f5f8",
            anchor="w",
            padding=(14, 11),
            borderwidth=0,
            font=("Arial", 10, "bold")
        )
        estilo.map(
            "Nav.TButton",
            background=[("active", "#1d4666"), ("disabled", "#102a43")],
            foreground=[("disabled", "#8093a5")]
        )
        estilo.configure(
            "PageTitle.TLabel",
            background="#f2f5f8",
            foreground="#183b56",
            font=("Arial", 20, "bold")
        )
        estilo.configure(
            "Primary.TButton",
            background="#1769aa",
            foreground="#ffffff",
            padding=(11, 8),
            borderwidth=0,
            font=("Arial", 9, "bold")
        )
        estilo.map("Primary.TButton", background=[("active", "#12588f")])
        estilo.configure(
            "Gold.TButton",
            background="#c99a22",
            foreground="#ffffff",
            padding=(11, 8),
            borderwidth=0,
            font=("Arial", 9, "bold")
        )
        estilo.map("Gold.TButton", background=[("active", "#a97f19")])
        estilo.configure(
            "Danger.TButton",
            background="#c0392b",
            foreground="#ffffff",
            padding=(11, 8),
            borderwidth=0,
            font=("Arial", 9, "bold")
        )
        estilo.map("Danger.TButton", background=[("active", "#a93226")])
        estilo.configure(
            "Neutral.TButton",
            background="#dce4eb",
            foreground="#183b56",
            padding=(11, 8),
            borderwidth=0,
            font=("Arial", 9, "bold")
        )
        estilo.map("Neutral.TButton", background=[("active", "#c8d4de")])
        estilo.configure(
            "Logout.TButton",
            background="#c0392b",
            foreground="#ffffff",
            padding=(12, 10),
            borderwidth=0,
            font=("Arial", 10, "bold")
        )
        estilo.map("Logout.TButton", background=[("active", "#a93226")])
        estilo.configure("TNotebook", background="#f2f5f8", borderwidth=0)
        estilo.configure(
            "TNotebook.Tab",
            background="#dce4eb",
            foreground="#183b56",
            padding=(14, 8),
            font=("Arial", 9, "bold")
        )
        estilo.map(
            "TNotebook.Tab",
            background=[("selected", "#ffffff")],
            foreground=[("selected", "#1769aa")]
        )
        estilo.configure(
            "Treeview",
            background="#ffffff",
            fieldbackground="#ffffff",
            foreground="#263746",
            rowheight=32,
            font=("Arial", 10)
        )
        estilo.configure(
            "Treeview.Heading",
            background="#183b56",
            foreground="#ffffff",
            padding=(8, 9),
            font=("Arial", 9, "bold")
        )

    def _crear_seccion_productos(self):
        formulario = ttk.LabelFrame(
            self.frame_productos,
            text="Datos del producto",
            padding=14
        )
        formulario.pack(fill="x", pady=(0, 12))

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
            text="➕ Registrar",
            command=self._registrar_producto,
            style="Primary.TButton"
        ).pack(side="left", padx=(0, 6))
        ttk.Button(
            botones,
            text="🔍 Cargar por código",
            command=self._cargar_producto,
            style="Gold.TButton"
        ).pack(side="left", padx=6)
        ttk.Button(
            botones,
            text="✏️ Actualizar",
            command=self._actualizar_producto,
            style="Primary.TButton"
        ).pack(side="left", padx=6)
        ttk.Button(
            botones,
            text="🗑️ Eliminar",
            command=self._eliminar_producto,
            style="Danger.TButton"
        ).pack(side="left", padx=6)
        ttk.Button(
            botones,
            text="🧹 Limpiar",
            command=self._limpiar_formulario,
            style="Neutral.TButton"
        ).pack(side="left", padx=6)
        ttk.Button(
            botones,
            text="↻ Refrescar",
            command=self._refrescar_productos,
            style="Neutral.TButton"
        ).pack(side="left", padx=6)

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

    def _cargar_producto(self):
        codigo = self.codigo_var.get().strip()
        producto = self.servicio.buscar_producto(codigo)
        if producto is None:
            messagebox.showerror("Error", "No existe un producto con ese código.")
            return

        self.codigo_var.set(producto.codigo)
        self.nombre_var.set(producto.nombre)
        self.categoria_var.set(producto.categoria)
        self.precio_var.set(str(producto.precio))
        self.stock_var.set(str(producto.stock))

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
        self.notebook.tab(
            self.frame_productos,
            text=f"Productos ({self.servicio.cantidad_productos()})"
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
