# Manual de Usuario - Tombola ODS

## 1. Descripción General

**Tombola ODS** es una aplicación de escritorio desarrollada en Python con Pygame que combina el juego de tombola (bingo) con la promoción de los Objetivos de Desarrollo Sostenible (ODS) de las Naciones Unidas. Los jugadores se registran, generan cartones temáticos y participan en sorteos automáticos mientras aprenden sobre los ODS.

## 2. Requisitos del Sistema

- Python 3.8 o superior.
- Dependencias listadas en `requirements.txt` (principalmente `pygame`).
- Sistema operativo Windows, Linux o macOS.
- Resolución de pantalla mínima recomendada: 1024x768.

## 3. Instalación

1. Clonar o descargar el proyecto en la carpeta deseada.
2. Abrir una terminal en la carpeta raíz del proyecto.
3. Crear y activar un entorno virtual (recomendado):
   - Windows: `python -m venv venv && venv\Scripts\activate`
   - Linux/macOS: `python3 -m venv venv && source venv/bin/activate`
4. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
5. Ejecutar la aplicación:
   ```bash
   python src/main.py
   ```

## 4. Pantallas de la Aplicación

### 4.1 Inicio de Sesión

- Ingrese su número de cédula en el campo "Cedula".
- Ingrese su clave de acceso en el campo "Clave".
- Seleccione **Ingresar** para acceder al menú principal.
- Seleccione **Registrarse** si aún no tiene una cuenta.
- Seleccione **Salir** para cerrar la aplicación.

> Nota: existe un jugador demo con cédula `12345678` y clave `Hola1=`.

### 4.2 Registro de Jugador

Complete todos los campos del formulario:

- **Cedula:** identificador único del jugador.
- **Nombre completo:** nombre y apellido.
- **Sexo:** ingrese `m` o `f`.
- **Fecha de nacimiento:** formato `YYYY-MM-DD`.
- **Codigo estado:** código de tres letras (por ejemplo, `CCS`, `BOL`, `ZUL`).
- **Clave de acceso:** debe cumplir las siguientes reglas:
  - Tener entre 6 y 10 caracteres.
  - Contener al menos una letra mayúscula.
  - Contener al menos una letra minúscula.
  - Contener al menos un número.
  - Contener al menos un carácter especial (`*`, `=`, `%`, `_`).
  - No tener más de 3 caracteres iguales consecutivos.
- **Confirmar clave:** debe coincidir exactamente con la clave.

Seleccione **Registrar** para guardar el jugador. Seleccione **Volver** para regresar al inicio de sesión.

### 4.3 Menú Principal

Después de iniciar sesión, el menú principal ofrece las siguientes opciones:

- **Jugar:** configurar una nueva partida.
- **Reportes:** ver estadísticas y exportar reportes.
- **Demo calculadora:** demostración del módulo de comandos internos.
- **Cerrar sesion:** regresar a la pantalla de inicio de sesión.
- **Salir:** cerrar la aplicación.

### 4.4 Configuración de Cartones

- Use las flechas `<` y `>` para seleccionar la **dimensión** del cartón (5, 7, 9, 11, 13 o 15).
- Use las flechas `<` y `>` para seleccionar el **tema ODS**.
- Seleccione **Continuar** para generar los cartones principal y complemento.
- Seleccione **Volver** para regresar al menú principal.

### 4.5 Pantalla de Juego

- Se muestran dos cartones: **Carton principal** (izquierda) y **Carton complemento** (derecha).
- Seleccione **Sacar numero** para sortear el siguiente número.
- Los números coincidentes se marcan automáticamente con el color del ODS seleccionado.
- En la parte inferior se muestra el eslogan educativo del ODS.
- El juego termina cuando un cartón queda completamente marcado.
- Seleccione **Menu** para salir al menú principal en cualquier momento.

### 4.6 Pantalla de Resultado

Cuando un cartón gana:

- Se muestra la palabra **GANADOR**.
- Se indica cuál cartón ganó (`PRINCIPAL` o `COMPLEMENTO`).
- Se muestra la **suma de todas las celdas** del cartón ganador.
- Se muestra el tema ODS de la partida.
- Seleccione **Jugar de nuevo** para iniciar una nueva partida con el mismo jugador.
- Seleccione **Menu** para regresar al menú principal.

### 4.7 Reportes

La pantalla de reportes muestra:

- **Jugadores y partidas:** lista de jugadores con cantidad de partidas jugadas.
- **TOP 5 jugadores:** ranking por puntos acumulados.
- **Números más frecuentes:** los 10 números más sorteados.
- **Últimas partidas:** historial reciente con fecha, jugador, ODS, ganador y puntos.

Seleccione **Exportar .txt** para guardar todos los reportes en un archivo de texto dentro de la carpeta `reports/`. Seleccione **Volver** para regresar al menú principal.

## 5. Navegación con Teclado

- **Tab:** mover el foco entre controles.
- **Shift + Tab:** mover el foco hacia atrás.
- **Enter / Espacio:** activar el control seleccionado.
- **Escape:** volver o salir (donde aplique).

En campos de texto, use el teclado para escribir y **Retroceso** para borrar.

## 6. Archivos Generados

- `data/JUGADORES.bin`: jugadores registrados (persistencia binaria).
- `data/JUEGOS.bin`: partidas jugadas (persistencia binaria).
- `reports/reporte_tombola_YYYYMMDD_HHMMSS.txt`: reportes exportados.

## 7. Solución de Problemas

| Problema | Solución |
|---|---|
| No se puede iniciar sesión | Verifique la cédula y la clave. Use el jugador demo `12345678` / `Hola1=`. |
| Error al registrar | Revise que todos los campos sean válidos y que la clave cumpla las reglas. |
| La aplicación no abre | Verifique que Python y `pygame` estén instalados correctamente. |
| Los binarios parecen corruptos | Los archivos se manejan con manejo de excepciones; si están vacíos o dañados, la aplicación los trata como listas vacías. |

## 8. Créditos

Proyecto desarrollado para la asignatura Algoritmos y Programación. Promueve los 17 Objetivos de Desarrollo Sostenible de las Naciones Unidas.
