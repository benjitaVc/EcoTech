# EcoTech

## Decisiones de Diseño (Clase 8 - CRUD Parametrizado)

- **¿Se borra de verdad?**: DELETE real (para mantener simplicidad en las consultas de lectura).
- **¿Que pasa con los hijos?**: Impedir el borrado (para resguardar la integridad del historial de tiempos).
- **¿Quien asigna el ID?**: El programa / usuario (utilizando el RUT como clave primaria).