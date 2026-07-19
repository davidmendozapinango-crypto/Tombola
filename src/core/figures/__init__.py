"""Utilities and families for figure masks and numbering.

Este paquete expone utilidades para construir máscaras escalables y las
implementaciones por familia. Principales API exportadas:
  - `fill_from_mask` (utility): rellenar números según una máscara y un orden.
  - módulos de familias bajo `families` (cada familia implementa
    `generate_principal` / `generate_complementary`).

Nota:
  Importar `families` trae módulos A..J; use explícitamente las funciones del
  generador cuando necesite construir matrices numeradas.
"""

from .utils import fill_from_mask
from .families import *

__all__ = ["fill_from_mask"]
