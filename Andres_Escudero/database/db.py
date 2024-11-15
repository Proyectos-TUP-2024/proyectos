import sqlite3
import os

# Definir la ruta de la base de datos
base_dir = os.path.dirname(os.path.abspath(__file__))  
bdd = os.path.abspath("c:/Users/Emula/Desktop/Python-CRUD-QT/mi_base_de_datos.db")

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.cnn = None
        
        try:
            self.cnn = sqlite3.connect(self.db_path)
            print("Conexión exitosa a la base de datos")
            self.crear_bdd()  # Crear las tablas al inicializar
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            self.cnn = None

    def crear_bdd(self):  
        cursor = self.cnn.cursor()

        # Crear tabla de usuarios
        cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            edad INTEGER,
            password TEXT NOT NULL,
            rol TEXT NOT NULL CHECK(rol IN ('Alumno', 'Profesor', 'Admin'))  -- Incluir Admin
        )''')

        # Inserta un usuario admin de ejemplo
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        if cursor.fetchone()[0] == 0:  # Solo insertar si no hay usuarios
            cursor.execute("INSERT INTO usuarios (nombre, apellido, edad, password, rol) VALUES (?, ?, ?, ?, ?)",
                           ("admin", "admin", 30, "hashed_password", "Admin"))  # Reemplaza hashed_password con un hash real

        # Crear tabla de Alumnos
        cursor.execute('''CREATE TABLE Alumnos (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "nombre" TEXT NOT NULL,
            "apellido" TEXT NOT NULL,
            "fecha_nacimiento" TEXT,
            "nota" REAL,
            "rol" TEXT NOT NULL,
            "usuario_id" INTEGER,
            FOREIGN KEY (usuario_id) REFERENCES Usuarios (id) ON DELETE CASCADE
        )''')


        # Crear tabla de Materia
        cursor.execute('''CREATE TABLE IF NOT EXISTS materia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            id_profesor INTEGER NOT NULL,
            hs_ingreso TEXT NOT NULL,
            hs_fin TEXT NOT NULL,
            FOREIGN KEY (id_profesor) REFERENCES Profesor (id) ON DELETE SET NULL
        )''')

        # Crear tabla de Inscripción
        cursor.execute('''CREATE TABLE IF NOT EXISTS inscripcion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_alumno INTEGER NOT NULL,
            id_materia INTEGER NOT NULL,
            fecha_inscripcion DATE DEFAULT (date('now')),
            FOREIGN KEY (id_alumno) REFERENCES Alumnos (id) ON DELETE CASCADE,
            FOREIGN KEY (id_materia) REFERENCES Materias (id) ON DELETE CASCADE
        )''')

        # Crear tabla de Profesores
        cursor.execute('''CREATE TABLE IF NOT EXISTS profesor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            id_usuario INTEGER NOT NULL,
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
        )''')

        # Guardar los cambios
        self.cnn.commit()
        print("Base de datos y tablas creadas exitosamente.")
        
    def probar_conexion(self):
        try:
            self.cnn.execute("SELECT 1")
            print("Conexión exitosa a la base de datos.")
        except sqlite3.Error as e:
            print(f"No se pudo conectar a la base de datos: {e}")

            




