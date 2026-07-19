# Plan de Pruebas Manual - Lista de Chequeo

**Proyecto:** Tombola ODS  
**Objetivo:** Validar de forma manual todos los aspectos críticos de la aplicación y los ítems de `docs/checklist.md`.

---

## Preparación previa

- [X] Abrir una terminal en la raíz del proyecto.
- [X] Activar el entorno virtual.
- [X] Ejecutar `python -m pytest tests/` y confirmar que todas las pruebas pasan.
- [X] Eliminar o renombrar temporalmente `data/JUGADORES.bin` y `data/JUEGOS.bin` para probar con datos limpios.
- [X] Ejecutar `python src/main.py`.

---

## 1. Entorno y arranque

- [X] **E1** Ejecutar `python src/main.py` y verificar que aparece ventana de 1024×768 con pantalla de login.
- [X] **E2** Jugar una ronda completa y verificar que las animaciones son fluidas.
- [X] **E3** Presionar `Esc` en login o hacer clic en "Salir" y verificar cierre limpio.

---

## 2. Autenticación y registro

### Registro

- [X] **A1** En login, clic en "Registrarse" y verificar que aparece pantalla de registro.
- [X] **A2** Escribir `"abc"` en "Clave de acceso" y verificar retroalimentación de criterios en tiempo real.
- [X] **A3** Intentar registrar con clave `"A1="` (3 caracteres) y verificar mensaje de longitud inválida.
- [X] **A4** Intentar registrar con clave `"hola1="` y verificar mensaje de falta de mayúscula.
- [X] **A5** Intentar registrar con clave `"HOLA1="` y verificar mensaje de falta de minúscula.
- [X] **A6** Intentar registrar con clave `"Hola="` y verificar mensaje de falta de número.
- [X] **A7** Intentar registrar con clave `"Hola12"` y verificar mensaje de falta de carácter especial.
- [X] **A8** Intentar registrar con clave `"Hola1111="` y verificar mensaje de run mayor a 3.
- [X] **A9** Ingresar clave `"Hola1="` y confirmar `"Hola2="`, verificar mensaje de claves no coincidentes.
- [X] **A10** Registrar dos veces la misma cédula y verificar mensaje de jugador existente.
- [X] **A11** Ingresar estado `"XYZ"` y verificar mensaje de código de estado inválido.
- [X] **A12** Completar formulario válido y verificar regreso a login con mensaje de éxito.
- [X] **A13** Navegar con `Tab` en registro y verificar foco visible en cada campo y botón.
- [X] **A14** Presionar `Esc` en registro y verificar regreso a login.

### Login

- [X] **A15** Clic en "Ingresar" sin llenar campos y verificar mensaje de campos vacíos.
- [X] **A16** Ingresar cédula inexistente y verificar mensaje de jugador no registrado.
- [X] **A17** Ingresar cédula válida con clave errónea y verificar mensaje de clave incorrecta.
- [x] **A18** Ingresar cédula y clave válidas y verificar ingreso al menú principal.
- [X] **A19** Presionar `Tab` en login y verificar foco visible.
- [X] **A20** Pasar mouse sobre botones y mantener clic, verificar hover y efecto de presión.
- [X] **A21** Presionar `Esc` en login y verificar cierre de aplicación.

---

## 3. Menú principal

- [ ] **M1** Abrir menú y verificar panel derecho con dimension, ODS y vista previa.
- [ ] **M2** Usar flechas de dimension y verificar cambio entre 5, 7, 9, 11, 13 y 15.
- [ ] **M3** Usar flechas de ODS y verificar cambio de nombre, color y vista previa.
- [ ] **M4** Clic en "Iniciar Partida de Tombola" con configuracion valida y verificar pantalla de juego.
- [ ] **M5** Clic en "Iniciar Partida de Tombola" sin configuracion y verificar mensaje de error.
- [ ] **M6** Clic en "Cerrar sesion" y verificar regreso a login.
- [ ] **M7** Presionar `Esc` en menú y verificar cierre de sesión y regreso a login.
- [ ] **M8** Clic en "Reportes" y verificar apertura de reportes.
- [ ] **M9** Clic en "Salir" y verificar cierre de aplicación.

---

## 4. Configuración de cartón

- [ ] **C1** Cambiar dimension u ODS en el panel derecho y verificar vista previa actualizada.
- [ ] **C2** Verificar que las figuras principal y complemento muestran patrones distintos en la vista previa.

---

## 5. Pantalla de juego

- [ ] **J1** Clic en "Iniciar sorteo" y verificar que aparece primer número y se marcan coincidencias.
- [ ] **J2** Esperar varios sorteos y verificar marcado automático en ambos cartones.
- [ ] **J3** Jugar hasta completar cartón y verificar que ningún número se repite.
- [ ] **J4** Completar la figura del cartón principal y verificar etiqueta "GANADOR".
- [ ] **J5** Al ganar, verificar que se muestra la suma de todas las celdas del cartón ganador.
- [ ] **J6** Usar botón de pausa si existe y verificar detención y reanudación.
- [ ] **J7** Clic en "Jugar de nuevo" y verificar nueva partida sin pedir login.
- [ ] **J8** Clic en "Simular completo" y verificar que el juego sortea hasta encontrar ganador.
- [ ] **J9** Después de simular, verificar que aparece "GANADOR" y botón "Ver resultado".
- [ ] **J10** Presionar `Esc` en juego y verificar regreso al menú o resultados.
- [ ] **J11** Observar durante el juego y verificar mensajes/slogans ODS en pantalla.

---

## 6. Persistencia

- [ ] **P1** Registrar un jugador, cerrar app y verificar que `data/JUGADORES.bin` aumentó de tamaño.
- [ ] **P2** Jugar una ronda, cerrar app y verificar que `data/JUEGOS.bin` aumentó de tamaño.
- [ ] **P3** Registrar 3 jugadores y jugar 2 partidas, reiniciar app y verificar que todos los datos persisten.
- [ ] **P4** Corromper o renombrar `data/JUEGOS.bin`, reiniciar app y verificar manejo sin errores graves.
- [ ] **P5** Inspeccionar un registro de `JUEGOS.bin` y verificar que no contiene campos calculados (`main_points`, `complement_points`, `winning_card`).

---

## 7. Reportes

- [ ] **R1** Abrir reportes y verificar botones: "Jugadores y partidas", "TOP 5", "Numeros mas frecuentes", "Historial".
- [ ] **R2** Abrir reportes y verificar que el reporte por defecto es "Jugadores y partidas".
- [ ] **R3** Clic en "Jugadores y partidas" y verificar lista con cantidad de partidas.
- [ ] **R4** Clic en "TOP 5 jugadores" y verificar ranking por puntos acumulados.
- [ ] **R5** Clic en "Numeros mas frecuentes" y verificar TOP 10 ordenado.
- [ ] **R6** Clic en "Historial de partidas" y verificar fecha, hora, jugador, ODS, ganador y puntos.
- [ ] **R7** Ingresar rango de fechas válido y verificar filtrado correcto.
- [ ] **R8** Ingresar fecha inválida y verificar mensaje de error en español.
- [ ] **R9** Seleccionar una sección, clic en "Exportar .txt" y verificar archivo individual en `reports/`.
- [ ] **R10** Presionar `Esc` en reportes y verificar regreso al menú.

---

## 8. Accesibilidad e idioma

- [ ] **I1** Revisar todas las pantallas y verificar que todos los textos visibles están en español.
- [ ] **I2** Provocar errores en cada pantalla y verificar mensajes claros en español.
- [ ] **I3** Navegar con `Tab` en login, registro, menú, config y reportes, verificar foco visible.
- [ ] **I4** Pasar mouse sobre botones y verificar cambio de color (hover).
- [ ] **I5** Mantener clic en un botón y verificar efecto de presión.
- [ ] **I6** Enfocar un botón y presionar `Enter` o `Espacio`, verificar activación.
- [ ] **I7** Presionar `Esc` en cada pantalla principal y verificar regreso o salida.

---

## 9. Integración ODS

- [ ] **O1** Revisar fondos, botones y paneles y verificar paleta de colores alineada con ODS.
- [ ] **O2** Elegir varios ODS en configuración y verificar imagen correspondiente.
- [ ] **O3** Elegir ODS distintos y verificar slogan correspondiente.
- [ ] **O4** Jugar partidas y verificar mensajes educativos relacionados con ODS.
- [ ] **O5** Verificar que cartón principal y complemento se identifican con el nombre del ODS.

---

## 10. Cálculo y lógica

- [ ] **L1** Al ganar, verificar que la suma del cartón coincide con `N² × (N² + 1) / 2`.
- [ ] **L2** Comparar puntos mostrados con la suma de las celdas marcadas.
- [ ] **L3** Completar solo la figura asignada y verificar que se declara ganador sin llenar todo el cartón.
- [ ] **L4** Ganar una partida, revisar historial y verificar que ganador y puntos coinciden.

---

## 11. Casos límite

- [ ] **X1** Jugar con dimensión 5 y verificar funcionamiento correcto.
- [ ] **X2** Jugar con dimensión 15 y verificar figura escalada y cartón visibles.
- [ ] **X3** Sortear pocos números y salir, verificar que no se declara ganador pero se guarda la partida.
- [ ] **X4** Borrar `JUEGOS.bin` y abrir reportes, verificar mensaje de datos vacíos.
- [ ] **X5** Registrar jugador y ver reportes, verificar contador de partidas igual a 0.

---

## 12. Panel de mensajes ODS

- [ ] **PM1** Abrir login y verificar panel inferior con mensaje ODS visible.
- [ ] **PM2** Ir a registro y verificar mensaje ODS en panel inferior.
- [ ] **PM3** Iniciar sesión y verificar que el panel muestra mensaje del ODS seleccionado.
- [ ] **PM4** Iniciar partida y verificar mensajes del ODS activo sin solapamiento.
- [ ] **PM5** Completar partida y verificar panel en pantalla de resultados.
- [ ] **PM6** Abrir reportes y verificar panel inferior sin tapar botones.
- [ ] **PM7** Observar panel ~15 segundos y verificar cambio de mensaje cada 5 segundos.
- [ ] **PM8** Revisar todas las pantallas y verificar que nada queda detrás del panel.

---

## Criterios de aceptación final

- [ ] Todas las pruebas automáticas (`pytest`) pasan.
- [ ] Al menos el 90% de los casos de prueba manual arrojan el resultado esperado.
- [ ] No hay defectos de severidad Alta o Crítica sin plan de corrección.
- [ ] Todos los textos de la interfaz están en español.
- [ ] Los archivos `JUGADORES.bin` y `JUEGOS.bin` crecen correctamente sin sobrescribir datos.
- [ ] Los reportes exportados son legibles y contienen la información esperada.

---

## Registro de defectos

| ID | Caso | Descripción | Pasos para reproducir | Resultado esperado | Resultado obtenido | Severidad | Evidencia |
|----|------|-------------|----------------------|--------------------|--------------------|-----------|-----------|
|    |      |             |                      |                    |                    |           |           |
|    |      |             |                      |                    |                    |           |           |
|    |      |             |                      |                    |                    |           |           |

---

*Lista de chequeo generada como parte de la entrega final del proyecto.*
