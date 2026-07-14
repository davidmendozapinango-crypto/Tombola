# Resumen de Actividades por Miembro

**Proyecto:** Tombola ODS  
**Asignatura:** Algoritmos y Programación  
**Fecha:** [COMPLETAR]

---

## Miembro 1: [Nombre]

### Áreas de responsabilidad
Autenticación, validación de jugadores y persistencia de jugadores.

### Tareas realizadas
- Diseño e implementación de `src/auth/validator.py` con validación recursiva de clave.
- Implementación de `src/auth/session.py` para gestión de sesión.
- Implementación de `src/persistence/players.py` con persistencia append-only.
- Creación de `tests/test_auth.py` y `tests/test_persistence.py`.
- Ajuste de `register_screen.py` para mostrar retroalimentación de criterios de clave.

### Entregables
- Código fuente funcional.
- Tests de autenticación y persistencia pasando.

---

## Miembro 2: [Nombre]

### Áreas de responsabilidad
Generación de cartones, figuras SDG y lógica de juego.

### Tareas realizadas
- Implementación de `src/core/card.py` para generar cartones N×N con números únicos.
- Definición de figuras SDG en `src/core/card_figures.py` con escalado para dimensiones mayores.
- Implementación de `src/core/game.py` para sorteos, marcado y detección de ganador por figura.
- Integración de imágenes ODS en `card_display_screen.py` y `game_screen.py`.
- Creación de `tests/test_card.py` y `tests/test_game.py`.

### Entregables
- Generación y detección de figuras funcionales.
- Tests de cartones y lógica de juego pasando.

---

## Miembro 3: [Nombre]

### Áreas de responsabilidad
Persistencia de partidas, flujo de juego y pantallas de resultado.

### Tareas realizadas
- Implementación de `src/persistence/games.py` con registros append-only y cálculo derivado de puntos/ganador.
- Integración de `game_screen.py` con la lógica de sorteo y detección de figuras.
- Implementación de `result_screen.py` para mostrar puntos y cartón ganador.
- Implementación de `card_display_screen.py` para la vista previa del cartón y figura.
- Ajuste de `config_screen.py` para enlazar la pantalla de vista previa.

### Entregables
- Flujo de juego completo funcional.
- Almacenamiento binario de partidas sin campos calculados.

---

## Miembro 4: [Nombre]

### Áreas de responsabilidad
Reportes, motor de cálculo y exportación.

### Tareas realizadas
- Implementación de `src/ui/screens/reports_screen.py` con filtros de fecha y exportación a `.txt`.
- Implementación del motor de cálculo (`src/core/calculation_engine.py` y módulos relacionados).
- Generación de reportes de frecuencia, historial y ranking TOP 5.
- Pruebas de integración del módulo de cálculo.
- Creación de `docs/ConstitutionCompliance.md`.

### Entregables
- Reportes funcionales con filtros y exportación.
- Documentación de cumplimiento de la constitución del proyecto.

---

## Miembro 5: [Nombre]

### Áreas de responsabilidad
Interfaz gráfica, navegación, accesibilidad y documentación de usuario.

### Tareas realizadas
- Implementación de `src/main.py` y registro de pantallas.
- Implementación de `login_screen.py`, `menu_screen.py` y `register_screen.py`.
- Mejoras de accesibilidad: foco visible, efecto de click y navegación con `Esc` en todas las pantallas principales.
- Centralización de componentes visuales en `src/ui/common.py`.
- Redacción de `docs/ManualUsuario.md`.

### Entregables
- Interfaz gráfica completa con navegación por mouse y teclado.
- Manual de usuario actualizado.

---

## Actividades conjuntas

- Revisión conjunta del enunciado y planificación de fases.
- Integración de módulos y resolución de conflictos entre lógica de juego y reportes.
- Ejecución de la suite de pruebas y corrección de errores.
- Preparación de la documentación final (`ReporteEscrito.md`, `ResumenActividades.md`, `ConstitutionCompliance.md`).
- Revisión final del `docs/checklist.md`.
