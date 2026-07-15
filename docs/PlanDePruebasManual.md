# Plan de Pruebas Manual - Tombola ODS

**Proyecto:** Tombola con temática de Objetivos de Desarrollo Sostenible  
**Objetivo:** Validar de forma manual todos los aspectos críticos de la aplicación y los ítems de `docs/checklist.md`.  
**Herramientas:** Teclado, mouse, editor de texto (para verificar archivos `.bin` y `.txt`), terminal (para ejecutar `pytest`).

---

## Preparación previa

1. Abrir una terminal en la raíz del proyecto.
2. Activar el entorno virtual.
3. Ejecutar `python -m pytest tests/` y confirmar que **todas las pruebas pasan**.
4. Eliminar o renombrar temporalmente `data/JUGADORES.bin` y `data/JUEGOS.bin` para probar el comportamiento con datos limpios.
5. Ejecutar `python src/main.py`.

---

## 1. Pruebas de entorno y arranque

| ID | Caso | Pasos | Resultado esperado |
|----|------|-------|-------------------|
| E1 | Ventana de inicio | Ejecutar `python src/main.py`. | Aparece ventana de 1024×768 titulada "Tombola - ODS" con pantalla de login. |
| E2 | Estabilidad de FPS | Jugar una ronda completa observando el movimiento. | Animaciones fluidas, sin congelamientos visibles. |
| E3 | Cierre limpio | Presionar `Esc` en login o hacer clic en "Salir". | La ventana se cierra sin errores en terminal. |

---

## 2. Pruebas de autenticación y registro

### 2.1 Registro de jugador

| ID | Caso | Pasos | Resultado esperado |
|----|------|-------|-------------------|
| A1 | Navegación a registro | En login, clic en "Registrarse" o foco + `Enter`. | Aparece pantalla de registro. |
| A2 | Validación de clave en tiempo real | Escribir `"abc"` en "Clave de acceso". | Criterios no cumplidos muestran ✗ en rojo; criterios cumplidos muestran ✓ en verde. |
| A3 | Clave inválida por longitud | Intentar registrar con clave `"A1="` (3 caracteres). | Mensaje: "La clave debe tener entre 6 y 10 caracteres." |
| A4 | Clave sin mayúscula | Clave `"hola1="`. | Mensaje de falta de mayúscula. |
| A5 | Clave sin minúscula | Clave `"HOLA1="`. | Mensaje de falta de minúscula. |
| A6 | Clave sin número | Clave `"Hola="`. | Mensaje de falta de número. |
| A7 | Clave sin especial | Clave `"Hola12"`. | Mensaje de falta de carácter especial. |
| A8 | Clave con run mayor a 3 | Clave `"Hola1111="`. | Mensaje: "La clave no puede tener más de 3 caracteres iguales seguidos." |
| A9 | Confirmación de clave | Clave `"Hola1="` y confirmar `"Hola2="`. | Mensaje: "Las claves no coinciden." |
| A10 | Cédula duplicada | Registrar dos veces la misma cédula. | Mensaje: "Ya existe un jugador con esa cedula." |
| A11 | Estado inválido | Escribir estado `"XYZ"`. | Mensaje: "El codigo de estado no es valido." |
| A12 | Registro exitoso | Completar formulario válido y clic en "Registrar". | Vuelve a login con mensaje de éxito. |
| A13 | Navegación con teclado en registro | Usar `Tab` para recorrer campos y botones; ver borde de foco. | Foco visible cambia entre campos y botones. |
| A14 | Retroceso con Esc en registro | Presionar `Esc`. | Regresa a pantalla de login. |

### 2.2 Inicio de sesión

| ID | Caso | Pasos | Resultado esperado |
|----|------|-------|-------------------|
| A15 | Credenciales vacías | Clic en "Ingresar" sin llenar campos. | Mensaje: "Ingrese cedula y clave." |
| A16 | Jugador no registrado | Ingresar cédula inexistente. | Mensaje: "Jugador no registrado." |
| A17 | Clave incorrecta | Ingresar cédula válida con clave errónea. | Mensaje: "Clave incorrecta." |
| A18 | Login exitoso | Ingresar cédula y clave válidas. | Aparece menú principal con nombre del jugador. |
| A19 | Foco visible en login | Presionar `Tab` varias veces. | Botón/input enfocado muestra borde grueso. |
| A20 | Hover y click en botones | Pasar mouse sobre botones y mantener clic. | Color cambia al pasar; botón se "presiona" visualmente. |
| A21 | Salir con Esc en login | Presionar `Esc`. | Aplicación cierra. |

---

## 3. Pruebas del menú principal

| ID | Caso | Pasos | Resultado esperado |
|----|------|-------|-------------------|
| M1 | Navegación por teclado | `Tab` y `Enter` sobre "Jugar". | Abre pantalla de configuración. |
| M2 | Cerrar sesión | Clic en "Cerrar sesion". | Regresa a login. |
| M3 | Esc en menú | Presionar `Esc`. | Cierra sesión y regresa a login. |
| M4 | Acceso a reportes | Clic en "Reportes". | Abre pantalla de reportes. |
| M5 | Salir | Clic en "Salir". | Aplicación cierra. |

---

## 4. Pruebas de configuración de cartón

| ID | Caso | Pasos | Resultado esperado |
|----|------|-------|-------------------|
| C1 | Selección de dimensión | Elegir dimensiones 5, 7, 9, 11, 13 y 15. | Cada vez se muestra vista previa correcta. |
| C2 | Dimensión par rechazada | Intentar elegir dimensión par. | No se permite o se muestra mensaje de error. |
| C3 | Dimensión fuera de rango | Intentar 3 o 17. | No se permite o se muestra mensaje de error. |
| C4 | Selección de ODS | Elegir diferentes ODS. | Se muestra nombre, color, slogan e imagen correspondiente. |
| C5 | Vista previa del cartón | Clic en "Continuar" tras configurar. | Aparece pantalla `card_display` con secuencia de llenado y figura resaltada. |
| C6 | Figura principal vs complemento | Verificar que main y complement muestran patrones distintos. | Patrones distinguibles entre sí. |
| C7 | Esc en configuración | Presionar `Esc`. | Regresa al menú principal. |

---

## 5. Pruebas de pantalla de juego

| ID | Caso | Pasos | Resultado esperado |
|----|------|-------|-------------------|
| J1 | Inicio de sorteo | Clic en "Iniciar sorteo" o equivalente. | Aparece primer número sorteado; cartones se marcan si coincide. |
| J2 | Marcado automático | Esperar varios sorteos. | Números coincidentes aparecen marcados en ambos cartones. |
| J3 | No repetición de números | Jugar hasta completar el cartón. | Ningún número se repite en la lista de sorteados. |
| J4 | Detección de ganador por figura | Completar la figura del cartón principal. | Aparece "GANADOR" en el cartón correspondiente. |
| J5 | Suma del cartón ganador | Al ganar, verificar resultado. | Se muestra la suma de todas las celdas del cartón ganador. |
| J6 | Pausa / continuar | Usar botón de pausa si existe. | Sorteo se detiene y reanuda correctamente. |
| J7 | Jugar otra ronda | Clic en "Jugar de nuevo" o similar. | Permite nueva partida sin pedir login. |
| J8 | Simulación completa | Clic en "Simular completo". | El juego sortea números automáticamente hasta encontrar un ganador. |
| J9 | Estado tras simulación | Después de "Simular completo". | Aparece "GANADOR" y el botón "Ver resultado". |
| J10 | Esc en juego | Presionar `Esc`. | Regresa al menú principal o a resultados según corresponda. |
| J11 | Mensajes educativos ODS | Observar durante el juego. | Aparecen mensajes/slogans ODS en pantalla. |

---

## 6. Pruebas de persistencia

| ID | Caso | Pasos | Resultado esperado |
|----|------|-------|-------------------|
| P1 | Registro agregado a `JUGADORES.bin` | Registrar un jugador y cerrar app. | El archivo `data/JUGADORES.bin` aumenta de tamaño y contiene el nuevo registro. |
| P2 | Partida agregada a `JUEGOS.bin` | Jugar una ronda y cerrar app. | El archivo `data/JUEGOS.bin` aumenta de tamaño. |
| P3 | No sobrescritura de datos | Registrar 3 jugadores y jugar 2 partidas; reiniciar app. | Todos los jugadores y partidas siguen disponibles. |
| P4 | Recuperación ante archivo corrupto | Corromper parcialmente `data/JUEGOS.bin` con un editor hexadecimal o renombrar. | App inicia sin errores y maneja la corrupción (puede mostrar lista vacía o mensaje). |
| P5 | Campos calculados no persistidos | Inspeccionar un registro de `JUEGOS.bin`. | Solo contiene: `player_id`, `played_at`, `sdg_id`, `dimension`, `main_card`, `complement_card`, `drawn_numbers`. No contiene `main_points`, `complement_points`, `winning_card`. |

---

## 7. Pruebas de reportes

| ID | Caso | Pasos | Resultado esperado |
|----|------|-------|-------------------|
| R1 | Pantalla de selección de reportes | Abrir reportes. | Aparecen botones para "Jugadores y partidas", "TOP 5", "Numeros mas frecuentes" e "Historial". |
| R2 | Reporte por defecto | Abrir reportes sin seleccionar nada. | Muestra el reporte "Jugadores y partidas" por defecto. |
| R3 | Lista de jugadores | Clic en "Jugadores y partidas". | Muestra todos los jugadores con cantidad de partidas jugadas. |
| R4 | TOP 5 ranking | Clic en "TOP 5 jugadores". | Muestra los 5 jugadores con más puntos acumulados. |
| R5 | Frecuencia de números | Clic en "Numeros mas frecuentes". | Muestra los 10 números más sorteados ordenados de mayor a menor. |
| R6 | Historial de partidas | Clic en "Historial de partidas". | Muestra fecha, hora, jugador, ODS, ganador y puntos. |
| R7 | Filtro por fecha | Ingresar rango de fechas y aplicar. | Reporte seleccionado solo incluye partidas dentro del rango. |
| R8 | Fecha inválida | Ingresar texto no válido en campos de fecha. | Mensaje de error en español. |
| R9 | Exportación individual | Seleccionar una sección y clic en "Exportar .txt". | Se crea archivo en `reports/` solo con el contenido de esa sección. |
| R10 | Esc en reportes | Presionar `Esc`. | Regresa al menú principal. |

---

## 8. Pruebas de accesibilidad e idioma

| ID | Caso | Pasos | Resultado esperado |
|----|------|-------|-------------------|
| I1 | Texto en español | Revisar todas las pantallas. | Todos los textos visibles están en español. |
| I2 | Mensajes de error en español | Provocar errores en cada pantalla. | Mensajes claros y en español. |
| I3 | Foco visible | Navegar con `Tab` en login, registro, menú, config, reportes. | Elemento enfocado tiene borde destacado. |
| I4 | Retroalimentación de hover | Pasar mouse sobre botones. | Cambio de color visible. |
| I5 | Retroalimentación de click | Mantener clic en un botón. | Botón se visualiza presionado (desplazamiento/color). |
| I6 | Navegación con Enter/Espacio | Enfocar botón y presionar `Enter` o `Espacio`. | Botón se activa. |
| I7 | Esc funcional en todas las pantallas | Presionar `Esc` en cada pantalla principal. | Regresa a la pantalla anterior o sale de la aplicación. |

---

## 9. Pruebas de integración ODS

| ID | Caso | Pasos | Resultado esperado |
|----|------|-------|-------------------|
| O1 | Colores ODS | Revisar fondos, botones y paneles. | Paleta de colores alineada con los ODS. |
| O2 | Imágenes ODS | Elegir varios ODS en configuración. | Aparece la imagen correspondiente en `card_display` y/o juego. |
| O3 | Slogans ODS | Elegir ODS distintos. | Se muestra el slogan del ODS seleccionado. |
| O4 | Mensajes educativos | Jugar partidas. | Aparecen mensajes relacionados con los ODS durante el juego. |
| O5 | Cartones tematizados | Verificar que cada partida tiene un ODS asignado. | El cartón principal y complemento se identifican con el nombre del ODS. |

---

## 10. Pruebas de cálculo y lógica

| ID | Caso | Pasos | Resultado esperado |
|----|------|-------|-------------------|
| L1 | Suma de cartón | Verificar resultado al ganar. | Suma = `N² × (N² + 1) / 2` (suma de 1 a N²). |
| L2 | Puntos del cartón | Comparar puntos mostrados con celdas marcadas. | Puntos = suma de los valores marcados. |
| L3 | Ganador por figura (no cartón completo) | Marcar solo las celdas de la figura asignada. | Juego declara ganador al completar la figura, sin necesidad de llenar todo el cartón. |
| L4 | Consistencia reporte-juego | Ganar una partida y revisar historial. | El ganador y puntos en el reporte coinciden con lo mostrado en el juego. |

---

## 11. Pruebas de casos límite

| ID | Caso | Pasos | Resultado esperado |
|----|------|-------|-------------------|
| X1 | Dimensión mínima (5) | Jugar con dimensión 5. | Funciona correctamente. |
| X2 | Dimensión máxima (15) | Jugar con dimensión 15. | Figura escalada y cartón visibles sin errores. |
| X3 | Partida sin ganador | Sortear pocos números y salir. | No se declara ganador; partida se guarda igual. |
| X4 | Reporte sin datos | Borrar `JUEGOS.bin` y abrir reportes. | Pantalla muestra mensaje indicando que no hay datos. |
| X5 | Jugador sin partidas | Registrar jugador y ver reportes. | Contador de partidas = 0. |

---

## Formato de registro de defectos

Para cada falla encontrada, registrar:

| Campo | Descripción |
|-------|-------------|
| ID | Identificador único (ej: DEF-01). |
| Caso de prueba | ID del caso donde ocurrió. |
| Descripción | Qué falló. |
| Pasos para reproducir | Secuencia exacta. |
| Resultado esperado | Lo que debería pasar. |
| Resultado obtenido | Lo que pasó realmente. |
| Severidad | Baja / Media / Alta / Crítica. |
| Evidencia | Captura o nota adicional. |

---

## Criterios de aceptación final

- [ ] Todas las pruebas automáticas (`pytest`) pasan.
- [ ] Al menos el 90% de los casos de prueba manual arrojan el resultado esperado.
- [ ] No hay defectos de severidad Alta o Crítica sin plan de corrección.
- [ ] Todos los textos de la interfaz están en español.
- [ ] Los archivos `JUGADORES.bin` y `JUEGOS.bin` crecen correctamente sin sobrescribir datos.
- [ ] Los reportes exportados son legibles y contienen la información esperada.

---

*Plan de pruebas generado como parte de la entrega final del proyecto.*
