"""Utilidades seguras para I/O binario en disco.

Proporciona funciones simples para crear un escritor seguro (asegura que el
directorio exista), escribir/leer bytes y comprobar existencia de archivos.
Las operaciones están diseñadas para uso sencillo y robusto en código que
requiere append-safe behavior.
"""

from pathlib import Path
from typing import Any, BinaryIO, Callable, Dict


def make_safe_writer(data_dir: str = "data") -> Dict[str, Any]:
    """Crea y prepara el directorio de datos; devuelve un dict con `data_dir`."""
    path = Path(data_dir)
    path.mkdir(parents=True, exist_ok=True)
    return {"data_dir": path}


def writer_path(writer: Dict[str, Any], filename: str) -> Path:
    """Devuelve la ruta completa para `filename` dentro del `writer`."""
    return writer["data_dir"] / filename


def append_bytes(writer: Dict[str, Any], filename: str, data: bytes) -> None:
    """Añade bytes al final del archivo (modo append binario)."""
    file_path = writer_path(writer, filename)
    with open(file_path, "ab") as f:
        f.write(data)


def read_bytes(writer: Dict[str, Any], filename: str) -> bytes:
    """Lee y devuelve todos los bytes del archivo; devuelve b'' si no existe."""
    file_path = writer_path(writer, filename)
    if not file_path.exists():
        return b""
    with open(file_path, "rb") as f:
        return f.read()


def file_exists(writer: Dict[str, Any], filename: str) -> bool:
    """Comprueba si el archivo existe en el directorio del `writer`."""
    return writer_path(writer, filename).exists()


def with_locked_write(file_path: Path, writer: Callable[[BinaryIO], Any]) -> None:
    """Abre el archivo en modo append y ejecuta la función `writer` proporcionada."""
    with open(file_path, "ab") as f:
        writer(f)
