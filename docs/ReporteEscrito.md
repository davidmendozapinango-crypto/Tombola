# Reporte Escrito - Proyecto Tombola ODS

**Asignatura:** Algoritmos y Programación  
**Proyecto:** Tombola con temática de Objetivos de Desarrollo Sostenible (ODS)  
**Fecha de entrega:** [COMPLETAR]  
**Equipo:** [COMPLETAR]

---

## 1. Introducción

### 1.1 Planteamiento del problema
El proyecto nace como evaluación académica integradora de los contenidos de Algoritmos y Programación. Se solicita construir una aplicación de tombola digital que no solo cumpla con reglas de juego clásicas, sino que incorpore de manera visible la temática de los Objetivos de Desarrollo Sostenible (ODS). La solución debe demostrar competencias en estructuras de datos, algoritmos recursivos, persistencia binaria, interfaces gráficas con Pygame y trabajo modular en equipo.

### 1.2 Objetivos
- **Objetivo general:** Desarrollar una aplicación funcional en Python + Pygame que implemente las cinco fases del proyecto: gestión segura de jugadores, creación dinámica de cartones, lógica de juego, reportes y ambientación ODS.
- **Objetivos específicos:**
  - Implementar registro seguro de jugadores con validación recursiva de claves.
  - Generar cartones dinámicos con dimensiones impares entre 5 y 15.
  - Simular el sorteo de tombola con detección de figuras SDG.
  - Persistir jugadores y partidas en archivos binarios sin sobrescribir registros previos.
  - Generar reportes de frecuencia, historial y ranking.
  - Integrar elementos visuales de los ODS en toda la experiencia de usuario.

### 1.3 Alcance
Se entrega una aplicación ejecutable localmente que permite registrar jugadores, iniciar sesión, configurar cartones, jugar rondas de tombola, visualizar resultados y consultar reportes. Los reportes se exportan a archivos de texto. El alcance no incluye multi-jugador en red, persistencia en base de datos relacional ni despliegue en servidor.

---

## 2. Descomposición Modular

El código fuente se organiza bajo `src/` siguiendo responsabilidades claras:

```text
src/
  auth/          # Validación de jugadores y sesiones
  core/          # Cartones, figuras SDG, lógica de juego, motor de cálculo
  ods/           # Datos de los ODS (nombres, colores, slogans)
  persistence/   # Persistencia binaria de jugadores y partidas
  ui/            # Pantallas Pygame y componentes visuales
```

| Módulo | Responsabilidad | Interacciones |
|--------|-----------------|---------------|
| `src/auth/` | Validar datos de registro, gestionar sesión activa. | Es llamado por `login_screen.py`, `register_screen.py` y `menu_screen.py`. |
| `src/core/` | Generar cartones, detectar figuras, ejecutar sorteos, calcular puntos y reportes del motor de cálculo. | Consume catálogos de `src/ods/`; es usado por `src/ui/screens/game_screen.py` y `src/persistence/games.py`. |
| `src/ods/` | Centralizar nombres, colores y slogans de los 17 ODS. | Es consumido por pantallas de configuración, juego y resultados. |
| `src/persistence/` | Leer y escribir `JUGADORES.bin` y `JUEGOS.bin` de forma binaria y append-only. | Es usado por pantallas de autenticación, juego y reportes. |
| `src/ui/` | Renderizar pantallas, capturar eventos y coordinar navegación. | Depende de todos los módulos anteriores. |

---

## 3. Diseño de Algoritmos

### 3.1 Validación recursiva de clave
La clave de acceso se valida mediante dos funciones recursivas ubicadas en `src/auth/validator.py`:
- `_has_type(key, index, predicate)` recorre la clave buscando al menos un carácter que satisfaga un predicado (mayúscula, minúscula, dígito o especial).
- `_no_long_run(key, index, current_char, count)` verifica que no existan más de tres caracteres idénticos consecutivos.

Ambas funciones se invocan desde `check_password_criteria`, permitiendo mostrar retroalimentación en tiempo real durante el registro.

### 3.2 Generación de cartones
`src/core/card.py` implementa `generate_card(dimension)`:
1. Crea una lista con los números del `1` al `N*N`.
2. La mezcla aleatoriamente con `random.shuffle`.
3. Recorre la lista llenando una matriz `N×N`.

Esto garantiza números únicos dentro del rango permitido.

### 3.3 Detección de figuras SDG
`src/core/card_figures.py` define ocho familias de figuras (`A` a `H`), cada una con una figura principal y una complementaria sobre una cuadrícula de referencia de 5×5. Para dimensiones mayores, `_scale_pattern` escala proporcionalmente las coordenadas.

Durante el juego, `src/core/game.py::check_winner` obtiene el patrón correspondiente al tipo de cartón y verifica que todas las celdas del patrón estén marcadas mediante `is_figure_complete`.

### 3.4 Persistencia binaria append-only
Los módulos `src/persistence/players.py` y `src/persistence/games.py` abren los archivos `.bin` en modo `"ab"` y usan `pickle.dump` para agregar un registro a la vez. La carga recorre el archivo con lecturas secuenciales hasta `EOFError`. Los formatos de registro se documentan en las funciones `make_game_record` y en los diccionarios de jugador.

### 3.5 Reportes
Los reportes se derivan de los datos crudos almacenados:
- **Jugadores y partidas jugadas:** conteo directo sobre `JUEGOS.bin`.
- **Frecuencia de números:** `Counter` sobre los `drawn_numbers` filtrados por rango de fecha.
- **Historial:** `calculate_game_summary` recalcula puntos y ganador sin campos calculados persistidos.
- **TOP 5:** acumulación de puntos por jugador ordenada descendentemente.

---

## 4. Código Fuente Relevante

### Validación de clave (`src/auth/validator.py`)
```python
def _has_type(key: str, index: int, predicate) -> bool:
    if index >= len(key):
        return False
    if predicate(key[index]):
        return True
    return _has_type(key, index + 1, predicate)

def _no_long_run(key: str, index: int, current_char: str, count: int) -> bool:
    if index >= len(key):
        return True
    if key[index] == current_char:
        new_count = count + 1
        if new_count > 3:
            return False
    else:
        new_count = 1
        current_char = key[index]
    return _no_long_run(key, index + 1, current_char, new_count)
```

### Generación de cartones (`src/core/card.py`)
```python
def generate_card(dimension: int) -> List[List[int]]:
    numbers = list(range(1, dimension * dimension + 1))
    random.shuffle(numbers)
    card = []
    index = 0
    for _ in range(dimension):
        row = []
        for _ in range(dimension):
            row.append(numbers[index])
            index += 1
        card.append(row)
    return card
```

### Detección de figuras (`src/core/card_figures.py` y `src/core/game.py`)
```python
def check_winner(main_card, marked_main, complement_card, marked_complement, card_type):
    dimension = len(main_card)
    main_pattern = get_figure_pattern(card_type, True, dimension)
    complement_pattern = get_figure_pattern(card_type, False, dimension)
    if is_figure_complete(main_card, marked_main, main_pattern):
        return "main"
    if is_figure_complete(complement_card, marked_complement, complement_pattern):
        return "complement"
    return None
```

### Persistencia append-only (`src/persistence/games.py`)
```python
def _append_game_record(file_path: str, game: Dict[str, Any]) -> None:
    with open(file_path, "ab") as file:
        pickle.dump(game, file)

def make_game_record(player_id, sdg_id, dimension, main_card, complement_card, drawn_numbers):
    return {
        "player_id": player_id,
        "played_at": datetime.now(),
        "sdg_id": sdg_id,
        "dimension": dimension,
        "main_card": main_card,
        "complement_card": complement_card,
        "drawn_numbers": drawn_numbers,
    }
```

### Pantalla principal (`src/main.py`)
Registra todas las pantallas y ejecuta el bucle principal de Pygame, delegando eventos y renderizado a cada módulo de pantalla.

---

## 5. Pruebas y Resultados

La suite de pruebas se ejecuta con:

```bash
python -m pytest tests/
```

Resultado esperado: todas las pruebas pasan.

Tipos de pruebas realizadas:
- **Unitarias de cartones y lógica de juego:** `tests/test_card.py`, `tests/test_game.py`.
- **De autenticación y registro:** `tests/test_auth.py`.
- **De persistencia binaria:** `tests/test_persistence.py`.
- **De contratos e integración del motor de cálculo:** `tests/contract/` y `tests/integration/calculation/`.
- **De accesibilidad por teclado:** `tests/integration/calculation/test_keyboard_accessibility.py`.

---

## 6. Conclusiones

El proyecto logró integrar los requisitos académicos con una experiencia de usuario coherente. La validación recursiva de claves, la persistencia binaria append-only y la detección de figuras SDG constituyen los algoritmos centrales de la solución. Las principales dificultades fueron la interpretación visual de las figuras SDG y el mantenimiento de la coherencia entre la lógica de juego y los reportes. Como lección aprendida, separar los datos crudos de sus cálculos derivados facilitó las pruebas y la generación de reportes consistentes.

---

## 7. Referencias

- Enunciado del proyecto: `docs/Proyecto AyP2026-25.pdf`
- Objetivos de Desarrollo Sostenible: https://www.un.org/sustainabledevelopment/
- Documentación de Pygame: https://www.pygame.org/docs/
