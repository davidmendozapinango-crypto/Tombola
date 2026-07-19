"""
Ayudantes para I/O binario seguro (no-OOP).

Descripción:
  Utilidades pequeñas para crear un escritor seguro de archivos binarios en un
  directorio de datos, escribir/leer bytes y comprobar existencia. Estas
  funciones encapsulan patrones de apertura en modo append/lectura.
"""

from pathlib import Path
from typing import Any, BinaryIO, Callable, Dict


def make_safe_writer(data_dir: str = "data") -> Dict[str, Any]:
    """Crear un escritor seguro que asegura la existencia del directorio.

    Args:
        data_dir: Ruta del directorio de datos (se crea si no existe).

    Returns:
        Dict[str, Any]: Objeto simple con clave 'data_dir' apuntando a Path.
    """
    path = Path(data_dir)
    path.mkdir(parents=True, exist_ok=True)
    return {"data_dir": path}


def writer_path(writer: Dict[str, Any], filename: str) -> Path:
    """Construye la ruta completa para un archivo dentro del directorio del writer."""
    return writer["data_dir"] / filename


def append_bytes(writer: Dict[str, Any], filename: str, data: bytes) -> None:
    """Añade bytes a un archivo en modo append, creando el archivo si no existe."""
    file_path = writer_path(writer, filename)
    with open(file_path, "ab") as f:
        f.write(data)


def read_bytes(writer: Dict[str, Any], filename: str) -> bytes:
    """Lee y devuelve todos los bytes de un archivo; devuelve b'' si falta."""
    file_path = writer_path(writer, filename)
    if not file_path.exists():
        return b""
    with open(file_path, "rb") as f:
        return f.read()


def file_exists(writer: Dict[str, Any], filename: str) -> bool:
    """Indica si un archivo existe en el directorio manejado por el writer."""
    return writer_path(writer, filename).exists()


def with_locked_write(file_path: Path, writer: Callable[[BinaryIO], Any]) -> None:
    """Abre un archivo en modo append y ejecuta la función `writer` pasándole
    el descriptor abierto. Esta utilidad permite agrupar operaciones seguras
    de escritura binaria.
    """
    with open(file_path, "ab") as f:
        writer(f)
