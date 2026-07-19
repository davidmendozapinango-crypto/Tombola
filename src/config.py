"""Application configuration constants (non-OOP)."""
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'
ASSETS_DIR = BASE_DIR / 'assets'
DATA_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_DIR.mkdir(parents=True, exist_ok=True)
PLAYERS_FILE = DATA_DIR / 'JUGADORES.bin'
GAMES_FILE = DATA_DIR / 'JUEGOS.bin'
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

# --- PALETA DE COLORES CANVA (Estilo ODS Mundialista) ---
COLOR_FONDO_GENERAL = (247, 241, 227)
COLOR_VERDE_HEADER = (136, 84, 49)
COLOR_VERDE_PANEL = (193, 154, 107)
COLOR_BTN_ROSA = (205, 119, 95)
COLOR_BTN_NARANJA = (210, 138, 92)
COLOR_BTN_VERDE_CLARO = (173, 141, 100)
COLOR_BTN_AZUL = (161, 123, 91)
COLOR_BTN_ORO = (187, 133, 77)
COLOR_BTN_VERDE_OSCURO = (100, 76, 53)
COLOR_BTN_ROSA_CLARO = (249, 226, 214)
COLOR_BTN_NARANJA_CLARO = (255, 239, 214)
COLOR_BTN_VERDE_CLARO_CLARO = (239, 229, 213)
COLOR_BTN_AZUL_CLARO = (241, 236, 222)
COLOR_BTN_ORO_CLARO = (254, 243, 212)
COLOR_BTN_VERDE_OSCURO_CLARO = (227, 218, 201)
COLOR_BORDE_CONTENEDOR = (136, 84, 49)
COLOR_TEXTO_OSCURO = (80, 70, 60)
COLOR_BLANCO_PURO = (250, 244, 236)

# Colores base utilizados por la interfaz
COLOR_PINE = COLOR_VERDE_HEADER
COLOR_MOSS = COLOR_BTN_VERDE_CLARO
COLOR_MINT = COLOR_FONDO_GENERAL
COLOR_CHARCOAL = COLOR_TEXTO_OSCURO
COLOR_WHITE = COLOR_BLANCO_PURO
COLOR_SAGE_LIGHT = COLOR_VERDE_PANEL
COLOR_RED_ALERT = COLOR_BTN_ROSA
COLOR_AMBER_LED = COLOR_BTN_ORO

# Lista de colores para los botones ODS
COLORES_ODS = [
    COLOR_BTN_ROSA,
    COLOR_BTN_NARANJA,
    COLOR_BTN_VERDE_CLARO,
    COLOR_BTN_ROSA,
    COLOR_BTN_ORO,
    COLOR_BTN_AZUL,
    COLOR_BTN_ORO,
    COLOR_BTN_VERDE_OSCURO,
]

COLORES_ODS_CLAROS = [
    COLOR_BTN_ROSA_CLARO,
    COLOR_BTN_NARANJA_CLARO,
    COLOR_BTN_VERDE_CLARO_CLARO,
    COLOR_BTN_ROSA_CLARO,
    COLOR_BTN_ORO_CLARO,
    COLOR_BTN_AZUL_CLARO,
    COLOR_BTN_ORO_CLARO,
    COLOR_BTN_VERDE_OSCURO_CLARO,
]

COLOR_SDG = {
    sdg_id: COLORES_ODS[(sdg_id - 1) % len(COLORES_ODS)]
    for sdg_id in range(1, 18)
}

COLOR_SDG_BG = {
    sdg_id: COLORES_ODS_CLAROS[(sdg_id - 1) % len(COLORES_ODS_CLAROS)]
    for sdg_id in range(1, 18)
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

# Three allusive/educational messages per SDG.
SDG_MESSAGES = {
    1: [
        "Erradicar la pobreza extrema es un acto de justicia y potencial humano.",
        "Nadie debe quedarse atras: la dignidad comienza con las necesidades basicas cubiertas.",
        "Invertir en personas vulnerables genera comunidades mas fuertes.",
    ],
    2: [
        "Garantizar alimentos nutritivos y agricultura sostenible es cuidar la vida.",
        "El hambre cero es posible cuando reducimos el desperdicio de alimentos.",
        "Una alimentacion saludable impulsa el desarrollo de ninos y adultos.",
    ],
    3: [
        "Una vida sana promueve el progreso sostenible en todas las edades.",
        "La salud mental y fisica son pilares del bienestar colectivo.",
        "Vacunas, agua limpia y educacion sanitaria salvan millones de vidas.",
    ],
    4: [
        "La educacion equitativa y de calidad es la semilla del futuro.",
        "Aprender a aprender nos prepara para resolver los desafios del manana.",
        "Cada nino con acceso a la escuela es una oportunidad de transformacion.",
    ],
    5: [
        "La igualdad de genero es el motor indispensable para un mundo libre.",
        "Cuando las mujeres prosperan, las sociedades enteras avanzan.",
        "Eliminar la discriminacion nos acerca a comunidades mas justas.",
    ],
    6: [
        "El agua potable segura y saneada es un derecho humano fundamental.",
        "Cuidar el agua es preservar la vida en todos los ecosistemas.",
        "La gestion sostenible del agua evita enfermedades y conflictos.",
    ],
    7: [
        "La energia asequible y limpia impulsa el desarrollo sin dañar el planeta.",
        "Las renovables son la llave para un futuro con aire mas puro.",
        "Acceso universal a la energia reduce la brecha social y economica.",
    ],
    8: [
        "El trabajo decente y el crecimiento economico sostenido reducen la desigualdad.",
        "Las oportunidades dignas construyen sociedades mas resilientes.",
        "Innovacion y empleo formal son bases para el progreso compartido.",
    ],
    9: [
        "Infraestructuras resilientes e innovacion conectan comunidades y generan progreso.",
        "La tecnologia al servicio de todos acelera el desarrollo sostenible.",
        "Industria responsable crece sin dejar de cuidar el medio ambiente.",
    ],
    10: [
        "Reducir las desigualdades fortalece la cohesion social y economica.",
        "La equidad empieza con oportunidades justas para todos y todas.",
        "Erradicar la discriminacion nos hace mas humanos y mas prosperos.",
    ],
    11: [
        "Ciudades inclusivas, seguras y sostenibles mejoran la calidad de vida.",
        "El transporte publico eficiente reduce la contaminacion urbana.",
        "Espacios verdes en la ciudad benefician la salud de sus habitantes.",
    ],
    12: [
        "Producir y consumir de forma sostenible alarga la vida del planeta.",
        "Reducir, reutilizar y reciclar son actos de responsabilidad global.",
        "Cada compra consciente impulsa una economia mas verde.",
    ],
    13: [
        "Combatir el cambio climatico es proteger nuestra unica casa.",
        "Pequeñas acciones diarias suman para reducir la huella de carbono.",
        "La educacion climatica empodera a las nuevas generaciones.",
    ],
    14: [
        "Conservar los oceanos garantiza la vida marina y la seguridad alimentaria.",
        "Menos plastico en el mar es mas vida bajo el agua.",
        "La pesca sostenible protege los ecosistemas costeros.",
    ],
    15: [
        "Proteger los ecosistemas terrestres es defender la biodiversidad.",
        "Restaurar suelos, sembrar arboles y apagar el fuego salva nuestra fauna.",
        "Cada especie preservada enriquece el equilibrio natural.",
    ],
    16: [
        "Sociedades pacificas e inclusivas construyen instituciones solidas.",
        "La justicia y el acceso a la ley son derechos de todas las personas.",
        "La paz comienza con el respeto mutuo y el dialogo.",
    ],
    17: [
        "Las alianzas globales aceleran los objetivos de desarrollo sostenible.",
        "Cooperar entre paises, empresas y ciudadanos multiplica el impacto.",
        "La solidaridad internacional es clave para no dejar a nadie atras.",
    ],
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
