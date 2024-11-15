import sqlite3

# Ruta de la base de datos
db_path = "c:/Users/Emula/Desktop/Python-CRUD-QT/mi_base_de_datos.db"

import sqlite3

# Ruta de la base de datos
db_path = "c:/Users/Emula/Desktop/Python-CRUD-QT/mi_base_de_datos.db"

def insertar_datos():
    # Conexión a la base de datos
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")  # Activar claves foráneas

    with conn:
        try:
            # Agregar un usuario
            conn.execute("INSERT INTO usuarios (nombre, apellido, rol, password) VALUES (?, ?, ?, ?)",
                         ("Juan", "Perez", "Alumno", "password123"))

            # Obtener el ID del último usuario insertado
            usuario_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

            # Agregar el usuario como alumno
            conn.execute("INSERT INTO alumnos (id, nombre, apellido) VALUES (?, ?, ?)", 
                         (usuario_id, "Juan", "Perez"))
            print("Alumno de ejemplo agregado correctamente.")
            
            # Agregar un profesor de ejemplo
            conn.execute("INSERT INTO profesor (nombre, apellido) VALUES (?, ?)", ("Carlos", "Martínez"))
            profesor_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            print("Profesor de ejemplo agregado correctamente.")
            
            # Agregar una materia de ejemplo asociada al profesor
            conn.execute("INSERT INTO materia (nombre_materia, id_profesor) VALUES (?, ?)", ("Matemáticas", profesor_id))
            print("Materia de ejemplo agregada correctamente.")
            
        except sqlite3.Error as e:
            print(f"Error al insertar datos: {e}")

    conn.close()

if __name__ == "__main__":
    insertar_datos()
