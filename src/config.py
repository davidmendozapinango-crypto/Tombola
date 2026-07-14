"""Application configuration constants (non-OOP)."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"

DATA_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

PLAYERS_FILE = DATA_DIR / "JUGADORES.bin"
GAMES_FILE = DATA_DIR / "JUEGOS.bin"

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

COLOR_PINE = (56, 102, 65)
COLOR_MOSS = (167, 201, 87)
COLOR_MINT = (242, 247, 244)
COLOR_CHARCOAL = (27, 46, 30)
COLOR_WHITE = (255, 255, 255)
COLOR_SAGE_LIGHT = (215, 225, 210)
COLOR_RED_ALERT = (220, 80, 80)
COLOR_AMBER_LED = (245, 180, 50)

COLOR_SDG = {
    1: (229, 36, 59),
    2: (221, 166, 58),
    3: (76, 159, 56),
    4: (199, 33, 47),
    5: (239, 64, 43),
    6: (38, 189, 226),
    7: (252, 195, 11),
    8: (162, 25, 66),
    9: (243, 111, 33),
    10: (221, 19, 103),
    11: (249, 157, 37),
    12: (207, 141, 42),
    13: (63, 126, 68),
    14: (10, 151, 217),
    15: (86, 192, 43),
    16: (19, 106, 124),
    17: (24, 72, 116),
}

SDG_NAMES = {
    1: "Fin de la pobreza",
    2: "Hambre cero",
    3: "Salud y bienestar",
    4: "Educacion de calidad",
    5: "Igualdad de genero",
    6: "Agua limpia y saneamiento",
    7: "Energia asequible y no contaminante",
    8: "Trabajo decente y crecimiento economico",
    9: "Industria, innovacion e infraestructura",
    10: "Reduccion de las desigualdades",
    11: "Ciudades y comunidades sostenibles",
    12: "Produccion y consumo responsables",
    13: "Accion por el clima",
    14: "Vida submarina",
    15: "Vida de ecosistemas terrestres",
    16: "Paz, justicia e instituciones solidas",
    17: "Alianzas para lograr los objetivos",
}

SDG_SLOGANS = {
    1: "Erradicar la pobreza en todas sus formas.",
    2: "Poner fin al hambre, lograr seguridad alimentaria.",
    3: "Garantizar una vida sana y promover el bienestar.",
    4: "Garantizar educacion inclusiva, equitativa y de calidad.",
    5: "Lograr la igualdad entre los generos.",
    6: "Garantizar la disponibilidad de agua y su gestion sostenible.",
    7: "Garantizar el acceso a energia asequible, segura y sostenible.",
    8: "Promover el crecimiento economico sostenido e inclusivo.",
    9: "Construir infraestructuras resilientes, promover la innovacion.",
    10: "Reducir la desigualdad en y entre los paises.",
    11: "Lograr que las ciudades sean inclusivas, seguras y sostenibles.",
    12: "Garantizar modalidades de consumo y produccion sostenibles.",
    13: "Adoptar medidas urgentes para combatir el cambio climatico.",
    14: "Conservar y utilizar sosteniblemente los oceanos.",
    15: "Promover el uso sostenible de los ecosistemas terrestres.",
    16: "Promover sociedades pacificas e inclusivas.",
    17: "Fortalecer los medios de implementacion y revitalizar la Alianza Mundial.",
}

STATE_CODES = {
    "AMA": "Amazonas",
    "ANA": "Anzoategui",
    "APU": "Apure",
    "ARA": "Aragua",
    "BAR": "Barinas",
    "BOL": "Bolivar",
    "CAR": "Carabobo",
    "COJ": "Cojedes",
    "DCA": "Delta Amacuro",
    "FAL": "Falcon",
    "GUA": "Guarico",
    "LAR": "Lara",
    "MER": "Merida",
    "MIR": "Miranda",
    "MON": "Monagas",
    "NES": "Nueva Esparta",
    "POR": "Portuguesa",
    "SUC": "Sucre",
    "TAC": "Tachira",
    "TRU": "Trujillo",
    "VAR": "Vargas",
    "YAR": "Yaracuy",
    "ZUL": "Zulia",
    "CCS": "Distrito Capital",
    "VUT": "Venezuela",
}
