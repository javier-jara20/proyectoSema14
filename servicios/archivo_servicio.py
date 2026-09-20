import json
from typing import Any


class ArchivoServicio:
    """Gestiona la lectura y escritura de archivos JSON."""

    def cargar_json(self, ruta: str) -> list[dict[str, Any]]:
        """Carga una lista de registros desde un archivo JSON."""

        with open(ruta, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        return datos

    def guardar_json(
        self,
        ruta: str,
        datos: list[dict[str, Any]]
    ) -> None:
        """Guarda una lista de registros en un archivo JSON."""

        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)
