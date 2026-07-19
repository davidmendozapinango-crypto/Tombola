from typing import Any, List, Optional, Tuple

try:
    from src.persistence.games import list_games
    from src.persistence.players import list_players
except ImportError:
    try:
        from persistence.games import list_games
        from persistence.players import list_players
    except ImportError:
        def list_games(*args: Any, **kwargs: Any) -> List[Any]:
            return []

        def list_players(*args: Any, **kwargs: Any) -> List[Any]:
            return []


def _ordenar_intercambio_directo(cedulas: List[str], nombres: List[str], puntos: List[int]) -> None:
    """Ordena tres arreglos en paralelo de mayor a menor por puntos usando
    intercambio directo (método de burbuja)."""
    n = len(puntos)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if puntos[j] < puntos[j + 1]:
                puntos[j], puntos[j + 1] = puntos[j + 1], puntos[j]
                cedulas[j], cedulas[j + 1] = cedulas[j + 1], cedulas[j]
                nombres[j], nombres[j + 1] = nombres[j + 1], nombres[j]


def _obtener_valor(game: Any, nombre: str, default: Any = None) -> Any:
    if isinstance(game, dict):
        return game.get(nombre, default)
    return getattr(game, nombre, default)


def top_players(
    date_from: Optional[str] = None, date_to: Optional[str] = None, top: int = 5
) -> List[Tuple[str, str, int]]:
    """Devuelve el TOP 'top' de jugadores con más puntos acumulados en el
    rango de fechas, como una lista de tuplas (cedula, nombre, puntos)."""
    games = list_games(date_from=date_from, date_to=date_to)

    puntos_por_cedula: dict[str, int] = {}
    for game in games:
        player_id = str(_obtener_valor(game, "player_id", "") or "")
        winner_card = str(_obtener_valor(game, "winner_card", "") or "")

        if winner_card in ("main", "both"):
            puntos_por_cedula[player_id] = (
                puntos_por_cedula.get(player_id, 0)
                + int(_obtener_valor(game, "main_card_sum", 0) or 0)
            )

        if winner_card in ("complement", "both"):
            puntos_por_cedula[player_id] = (
                puntos_por_cedula.get(player_id, 0)
                + int(_obtener_valor(game, "complement_card_sum", 0) or 0)
            )

    nombre_por_cedula: dict[str, str] = {}
    for player in list_players():
        if isinstance(player, dict):
            cedula = player.get("player_id") or player.get("cedula")
            nombre = player.get("full_name") or player.get("name")
        else:
            cedula = getattr(player, "cedula", None) or getattr(player, "player_id", None)
            nombre = getattr(player, "full_name", None) or getattr(player, "name", None)

        if cedula is not None:
            nombre_por_cedula[str(cedula)] = str(nombre or "(desconocido)")

    cedulas: List[str] = []
    nombres: List[str] = []
    puntos: List[int] = []
    for cedula, total_puntos in puntos_por_cedula.items():
        cedulas.append(str(cedula))
        nombres.append(nombre_por_cedula.get(str(cedula), "(desconocido)"))
        puntos.append(int(total_puntos))

    _ordenar_intercambio_directo(cedulas, nombres, puntos)

    if top < 1:
        return []

    limite = min(top, len(puntos))
    return [(cedulas[i], nombres[i], puntos[i]) for i in range(limite)]
