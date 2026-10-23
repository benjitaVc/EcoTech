Bitácora de uso de IA (Apoyo de Gemini)
Herramienta utilizada: Gemini.
Usamos Gemini para ayudarnos a revisar el código, armar las pruebas, encontrar errores y entender mejor cómo explicar todo para la defensa oral. La IA nos dio muy buenas ideas para el código y el informe, pero no copiamos y pegamos a ciegas. Aquí dejamos anotadas las cosas que aceptamos y las que tuvimos que cambiar nosotros mismos para que el proyecto cumpliera con lo que pide el profe.

1. main.py / Comprobaciones
Qué revisamos: Que el programa no se caiga al ejecutarlo de distintas formas.Decisión: Modificado. Gemini nos había sugerido usar un comando llamado assert para verificar si se actualizaban los datos. Nos dimos cuenta de que si ejecutamos Python en modo rápido (optimizado), ese comando se ignora y no hace nada. Lo cambiamos por una función propia comprobar() y ahora sí revisa siempre.

2. infraestructura/conexion.py / obtener_conexion
Qué revisamos: Qué pasa si falla la conexión a la base de datos.Decisión: Modificado. Al principio, si la conexión fallaba, el programa simplemente se cerraba feo. Con un poco de ayuda extra de Gemini, armamos unos bloques para atrapar el error. Ahora, si la base de datos no carga, te muestra un mensaje amigable en la consola y te devuelve al menú principal sin que el programa explote.

3. dominio/informe*.py y main.py
Qué revisamos: Orden de los archivos y POO (Programación Orientada a Objetos).Decisión: Modificado. Inicialmente, Gemini nos había puesto todas las clases de informes juntas en un solo archivo. Nosotros decidimos separarlas, dejando cada clase en su propio archivo. Quedó mucho más ordenado y nos será más fácil mostrarle al profe cómo funciona la herencia.

4. infraestructura/conexion.py / obtener_ruta_bd
Qué revisamos: La configuración de la base de datos.Decisión: Modificado. Ajustamos el código para asegurarnos de que el programa de verdad lea la ruta de la base de datos desde el archivo .env (las variables de entorno), para que funcione bien en cualquier computador y no quede la ruta pegada a la fuerza en el código.

5. Repositorios / Consultas SQL
Qué revisamos: Seguridad para que no nos hagan Inyección SQL.Decisión: Aceptado. Le hicimos caso a las buenas prácticas de Gemini y mantuvimos estrictamente el uso del signo ? (parámetros) en todas las consultas a la base de datos. Intentamos meter textos raros y comillas para "hackearlo" y el sistema no se rompió. Quedó 100% seguro.

6. consola.py / Menú de usuario
Qué revisamos: Que el usuario no rompa el programa al ingresar datos inválidos.Decisión: Aceptado. Nos quedamos con la estructura del menú interactivo que armamos con Gemini. Lo pusimos a prueba ingresando sueldos negativos, RUTs repetidos y textos vacíos, y el menú atrapa todos esos errores y te pide el dato de nuevo sin cerrarse.