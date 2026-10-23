Diagnóstico y Arreglos para la Entrega ES2
Cómo estaba el proyecto antes de los arreglos
El proyecto ya tenía un buen avance: podíamos guardar, buscar y borrar datos de forma segura, y pasaba 19 pruebas de funcionamiento. Sin embargo, al revisarlo con Gemini, nos dimos cuenta de que faltaban cosas clave que pide la pauta: no se notaba bien cómo funcionaba la herencia entre las clases, faltaba leer correctamente el archivo .env, el programa se cerraba feo si había un error al iniciar, y no teníamos un menú interactivo. Además, usábamos un comando (el assert) que podía hacer que el código fallara si se ejecutaba de cierta manera en la revisión del profe.

Cambios que hicimos y por qué (con apoyo de Gemini)
Menú para el usuario (consola.py): Armamos un menú interactivo. Si el usuario mete un dato malo, el programa te avisa y te pide ingresarlo de nuevo en lugar de caerse.

Mejoras en el inicio (main.py): Cambiamos el comando problemático (assert) por una función propia que llamamos comprobar(). Ahora la demostración funciona perfecto en cualquier computador. También agregamos ejemplos claros para que el profe vea cómo las distintas clases interactúan entre sí.

Conexión más robusta (infraestructura/conexion.py): Ajustamos la configuración para que lea la ubicación de la base de datos desde el archivo .env. Si la base de datos no está o falla, el programa lanza un mensaje amigable y no un error incomprensible.

Lógica de negocio (dominio/empleado.py): Le agregamos al empleado una función calcular_total_horas() que suma todas las horas que tiene registradas, demostrando que sabemos meter reglas de negocio en el código.

Más orden: Separamos las clases de excepciones y de informes en distintos archivos. Quedó todo mucho más limpio y fácil de leer.

Consultas SQL blindadas: Modificamos cómo se arman las consultas de búsqueda para separar aún más el código SQL de los datos que ingresa el usuario, asegurando el puntaje de seguridad.

Más pruebas automatizadas: Con ideas de Gemini, creamos 10 pruebas nuevas (llegando a 29). Pasaron todas.

Demostración de seguridad (evidencias_transaccion.py): Creamos un script cortito que simula un corte de luz o un error a la mitad de un guardado. Esto demuestra visualmente que nuestro sistema echa todo para atrás (hace un rollback) y no deja datos guardados a medias.

Todo probado y funcionando
Corrimos las 29 pruebas y el código funciona al 100%. Probamos el menú metiendo sueldos falsos, RUTs repetidos e intentando borrar empleados que no debían borrarse, y el sistema aguantó todo de forma controlada.

Lo que nos toca a nosotros (Para la defensa oral)
Tenemos súper claro que el código no hace el trabajo solo. Para la interrogación, tenemos que tener a mano nuestro diagrama UML de la Unidad 1 para compararlo con este código, y cada uno debe saber explicar en qué partes del proyecto trabajó y por qué tomamos estas decisiones de diseño.