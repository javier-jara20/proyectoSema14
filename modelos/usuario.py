class Usuario:

    def __init__(
        self,
        identificacion: str,
        nombre: str,
        correo: str
    ) -> None:

        if not identificacion.strip():
            raise ValueError(
                "La identificación no puede estar vacía."
            )

        if not nombre.strip():
            raise ValueError(
                "El nombre no puede estar vacío."
            )

        if not correo.strip():
            raise ValueError(
                "El correo no puede estar vacío."
            )

        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo

    def mostrar_informacion(self) -> str:

        return (
            f"Identificación: {self.identificacion}\n"
            f"Nombre: {self.nombre}\n"
            f"Correo: {self.correo}"
        )

    def to_dict(self) -> dict:

        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo
        }
