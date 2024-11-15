# Gestor de Alumnos y Profesores

Un **CRUD (Crear, Leer, Actualizar, Eliminar)** diseñado para gestionar alumnos, profesores y materias, desarrollado en **Python** usando **PyQt6** para la interfaz gráfica e integrado con **MySQL** como base de datos.

---

## 🛠️ Características

- **Gestión de Alumnos**: 
  - Registro de alumnos con nombre, apellido, materia y calificaciones.
  - Visualización, actualización y eliminación de registros.

- **Gestión de Profesores**:
  - Registro de profesores con asignación de materias.
  - Listado de los alumnos inscritos en la materia asignada.

- **Materias y Calificaciones**:
  - Inscripción de alumnos a materias.
  - Visualización de calificaciones.

- **Roles de Usuario**:
  - Diferenciación entre roles de `admin`, `profesor` y `alumno`, con funcionalidades específicas para cada uno.

---

## 🚀 Tecnologías Utilizadas

- **Lenguaje**: Python
- **Interfaz Gráfica**: PyQt6
- **Base de Datos**: MySQL
- **Estilos**: CSS (para personalizar la apariencia de PyQt6)
- **Módulos adicionales**:
  - `PyQt6`
  - `mysql-connector-python` (o similar para conectar con MySQL)

---
🌟 Uso de la Aplicación
Inicio de sesión:

Los usuarios deben ingresar sus credenciales y rol (admin, profesor, alumno).
El sistema muestra la ventana correspondiente según el rol.
Funcionalidades principales:

Admin:
Gestión completa de alumnos, profesores y materias.
Profesor:
Visualización de los alumnos inscritos en su materia.
Alumno:
Inscripción a materias y visualización de calificaciones.

📝 Próximas Mejoras

Agregar soporte para reportes PDF de calificaciones.
Mejoras en la seguridad del sistema (cifrado de contraseñas).
Optimización de consultas SQL.

📌 Notas Adicionales

Este proyecto fue desarrollado como parte de proyecto final de la Materia de Programacion II, para aprender a gestionar bases de datos y crear aplicaciones con Python.
Sugerencias y contribuciones son bienvenidas.

👨‍💻 Autor

Cristian "Andrés" Escudero

Venado Tuerto, 2024
