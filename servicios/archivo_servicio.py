import json
from pathlib import Path


class ArchivoServicio:

    def __init__(self) -> None:
        self.base_dir = Path(__file__).resolve().parent.parent

    def cargar_json(self, ruta: str):
        ruta_completa = self.base_dir / ruta

        with open(ruta_completa, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    def guardar_json(self, ruta: str, datos) -> None:
        ruta_completa = self.base_dir / ruta

        with open(
            ruta_completa,
            "w",
            encoding="utf-8"
        ) as archivo:
            json.dump(
                datos,
                archivo,
                ensure_ascii=False,
                indent=4
            )