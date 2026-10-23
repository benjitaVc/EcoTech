EcoTech - Evaluación Sumativa N°2

Proyecto desarrollado por Benjamín Vergara y Javiera Peña. Sección D-IEI-N2-P2-C1/D.
Sistema en Python para gestionar empleados y sus registros de tiempo usando SQLite.

Paso a paso para ejecutar (Windows)
Descomprimir la carpeta EcoTech y abrir una terminal (consola) dentro de ella. Si Windows no reconoce el comando python, puedes usar py como en los siguientes ejemplos:

PowerShell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.venv\Scripts\python.exe inicializar_bd.py
.venv\Scripts\python.exe main.py
.venv\Scripts\python.exe main.py --menu
No necesitas instalar librerías externas complejas porque sqlite3 ya viene integrado en Python. Si ya tienes Python configurado en tu equipo, puedes ejecutar el programa directamente con:

PowerShell
py main.py
py main.py --menu
main.py: Ejecuta una demostración automática con datos de prueba.

main.py --menu: Abre el menú interactivo para ingresar, buscar, actualizar y borrar datos de forma manual. Si las tablas no existen en la base de datos, el menú las crea automáticamente sin borrar la información previa.

Configuración de la Base de Datos
Copia el archivo .env.example y renómbralo a .env. Dentro viene la configuración por defecto: DB_NOMBRE=ecotech.db.

SQLite guarda toda la información en ese archivo local dentro de la carpeta del proyecto, por lo que no requiere nombre de usuario ni contraseña para conectarse.

Pruebas y Evidencias
Para revisar que todas las funciones andan bien, puedes correr los siguientes comandos en la terminal:

PowerShell
py -m unittest discover -s tests -v
py evidencias_transaccion.py
py -O main.py
Resultado: 29 pruebas pasadas correctamente (OK). En la carpeta evidencias/ dejamos guardados los registros de texto e imágenes que demuestran que el menú, los errores de conexión, la seguridad contra inyección SQL y el control de transacciones funcionan sin fallas.

Decisiones Principales de Diseño
Separación de capas: Guardamos y buscamos información mediante repositorios (EmpleadoRepositorio y RegistroTiempoRepositorio), logrando que las clases del negocio no tengan código SQL mezclado.

Identificadores: El RUT no se modifica porque es el identificador único del empleado en la base de datos. Lo que sí se actualiza desde el menú es el sueldo base.

Seguridad en el borrado: Al eliminar un empleado, el sistema borra sus datos de las dos tablas al mismo tiempo dentro de una misma transacción. Si el empleado ya tiene registros de tiempo guardados, el sistema bloquea el borrado para no perder el historial.

Inyección SQL: Todas las consultas usan el marcador ? para pasar los datos por separado. De esta forma, la base de datos trata la entrada del usuario estrictamente como texto y no como comandos ejecutables.

Cálculo de negocio: El cálculo de horas trabajadas se realiza directamente en Python sumando los registros cargados en el objeto empleado.

Alcance del Proyecto
Aspectos clave para considerar durante la presentación:

El RUT se valida verificando que no sea un texto vacío.

El sistema funciona 100% por consola de comandos, sin interfaz gráfica ni usuarios con clave, tal como está estipulado para esta etapa del proyecto.

Archivos de Documentación
BITACORA_IA.md: Documento donde explicamos cómo usamos la IA, qué sugerencias aceptamos y qué correcciones le hicimos.

CAMBIOS_ES2.md: Resumen con las mejoras hechas al código.

docs/modelo_actual.mmd: Estructura del diagrama de clases del sistema.

Informe_EcoTech_ES2.pdf: Informe técnico en PDF que se adjunta junto al archivo ZIP en la entrega final.