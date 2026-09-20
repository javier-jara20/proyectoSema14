from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:

    def __init__(
        self,
        datos_productos: list[dict],
        datos_usuarios: list[dict],
        archivo_servicio: ArchivoServicio
    ) -> None:

        self.archivo_servicio = archivo_servicio

        self.productos: list[Producto] = []
        self.usuarios: list[Usuario] = []

        self.cargar_productos(datos_productos)
        self.cargar_usuarios(datos_usuarios)

    # -------------------------------------------------
    # CARGA DE DATOS
    # -------------------------------------------------

    def cargar_productos(self, datos_productos: list[dict]) -> None:
        """Convierte los registros JSON en objetos Producto."""

        self.productos.clear()

        for registro in datos_productos:
            producto = Producto(
                codigo=str(registro.get("codigo", "")).strip(),
                nombre=str(registro.get("nombre", "")).strip(),
                categoria=str(registro.get("categoria", "")).strip(),
                precio=float(registro.get("precio", 0)),
                stock=int(registro.get("stock", 0))
            )

            self.productos.append(producto)

    def cargar_usuarios(self, datos_usuarios: list[dict]) -> None:
        """Convierte los registros JSON en objetos Usuario."""

        self.usuarios.clear()

        for registro in datos_usuarios:
            usuario = Usuario(
                identificacion=str(
                    registro.get("identificacion", "")
                ).strip(),
                nombre=str(registro.get("nombre", "")).strip(),
                correo=str(registro.get("correo", "")).strip()
            )

            self.usuarios.append(usuario)

    # -------------------------------------------------
    # LOGIN
    # -------------------------------------------------

    def validar_usuario(
        self,
        identificacion: str,
        clave: str
    ) -> Usuario | None:

        if clave != "1234":
            return None

        for usuario in self.usuarios:
            if usuario.identificacion == identificacion:
                return usuario

        return None

    # -------------------------------------------------
    # CONSULTAS
    # -------------------------------------------------

    def listar_productos(self) -> list[Producto]:
        return self.productos

    def listar_usuarios(self) -> list[Usuario]:
        return self.usuarios

    def cantidad_productos(self) -> int:
        return len(self.productos)

    def cantidad_usuarios(self) -> int:
        return len(self.usuarios)

    def buscar_producto(self, codigo: str) -> Producto | None:
        """Busca un producto mediante su código."""

        for producto in self.productos:
            if producto.codigo == codigo:
                return producto

        return None

    # -------------------------------------------------
    # PERSISTENCIA
    # -------------------------------------------------

    def guardar_productos(self) -> None:
        """Guarda los productos actuales en productos.json."""

        datos = [
            producto.to_dict()
            for producto in self.productos
        ]

        self.archivo_servicio.guardar_json(
            "datos/productos.json",
            datos
        )

    # -------------------------------------------------
    # REGISTRAR PRODUCTO
    # -------------------------------------------------

    def registrar_producto(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float,
        stock: int
    ) -> tuple[bool, str]:

        codigo = codigo.strip()
        nombre = nombre.strip()
        categoria = categoria.strip()

        if not codigo or not nombre or not categoria:
            return False, "Todos los campos son obligatorios."

        if self.buscar_producto(codigo) is not None:
            return False, "Ya existe un producto con ese código."

        try:
            nuevo_producto = Producto(
                codigo=codigo,
                nombre=nombre,
                categoria=categoria,
                precio=float(precio),
                stock=int(stock)
            )

        except ValueError as error:
            return False, str(error)

        self.productos.append(nuevo_producto)
        self.guardar_productos()

        return True, "Producto registrado correctamente."

    # -------------------------------------------------
    # ACTUALIZAR PRODUCTO
    # -------------------------------------------------

    def actualizar_producto(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float,
        stock: int
    ) -> tuple[bool, str]:

        producto_existente = self.buscar_producto(codigo.strip())

        if producto_existente is None:
            return False, "No existe un producto con ese código."

        nombre = nombre.strip()
        categoria = categoria.strip()

        if not nombre or not categoria:
            return False, "El nombre y la categoría son obligatorios."

        try:
            producto_actualizado = Producto(
                codigo=producto_existente.codigo,
                nombre=nombre,
                categoria=categoria,
                precio=float(precio),
                stock=int(stock)
            )

        except ValueError as error:
            return False, str(error)

        posicion = self.productos.index(producto_existente)
        self.productos[posicion] = producto_actualizado

        self.guardar_productos()

        return True, "Producto actualizado correctamente."

    # -------------------------------------------------
    # ELIMINAR PRODUCTO
    # -------------------------------------------------

    def eliminar_producto(self, codigo: str) -> tuple[bool, str]:

        producto = self.buscar_producto(codigo.strip())

        if producto is None:
            return False, "No existe un producto con ese código."

        self.productos.remove(producto)
        self.guardar_productos()

        return True, "Producto eliminado correctamente."