import sqlite3
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'mi_base_de_datos.db')

class Database:
    def __init__(self):
        self.cnn = None
        try:
            self.cnn = sqlite3.connect(db_path)
            self.cnn.execute("PRAGMA foreign_keys = ON")
            print("Conexión exitosa a la base de datos")
            self.crear_tablas()
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def crear_tablas(self):
            cursor = self.cnn.cursor()

            cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                edad INTEGER,
                password TEXT NOT NULL,
                rol TEXT NOT NULL CHECK(rol IN ('Alumno', 'Profesor', 'Admin'))
            )''')


            cursor.execute('''CREATE TABLE IF NOT EXISTS Alumnos (
                id_alumnos INTEGER PRIMARY KEY AUTOINCREMENT,
                id_usuario INTEGER,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                nota REAL,
                rol TEXT NOT NULL,
                FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario) ON DELETE CASCADE
            )''')


            cursor.execute('''CREATE TABLE IF NOT EXISTS profesor (
                id_profesor INTEGER PRIMARY KEY AUTOINCREMENT,
                id_usuario INTEGER,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario) ON DELETE CASCADE
            )''')

            

            cursor.execute('''CREATE TABLE IF NOT EXISTS materia (
                id_materia INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                id_profesor INTEGER,
                FOREIGN KEY (id_profesor) REFERENCES profesor (id_profesor) ON DELETE SET NULL
            )''')
            

            cursor.execute('''CREATE TABLE IF NOT EXISTS inscripcion (
                id_inscripcion INTEGER PRIMARY KEY AUTOINCREMENT,
                id_alumnos INTEGER NOT NULL,
                id_materia INTEGER NOT NULL,
                fecha_inscripcion DATE DEFAULT (date('now')),
                FOREIGN KEY (id_alumnos) REFERENCES Alumnos (id_alumnos) ON DELETE CASCADE,
                FOREIGN KEY (id_materia) REFERENCES materia (id_materia) ON DELETE CASCADE
            )''')
            
            

            cursor.execute('''CREATE TABLE IF NOT EXISTS notificaciones (
                id_notificacion INTEGER PRIMARY KEY AUTOINCREMENT,
                id_alumnos INTEGER NOT NULL,
                id_profesor INTEGER NOT NULL,
                mensaje TEXT NOT NULL,
                fecha DATE DEFAULT (date('now')),
                FOREIGN KEY (id_alumnos) REFERENCES Alumnos(id_alumnos) ON DELETE CASCADE,
                FOREIGN KEY (id_profesor) REFERENCES profesor(id_profesor) ON DELETE CASCADE
            )''')


            self.cnn.commit()
            print("Tablas y datos predeterminados creados correctamente.")

        
    def insertar_usuarios_por_defecto(self, cursor):
    
            cursor.execute('''INSERT OR IGNORE INTO usuarios (nombre, apellido, edad, password, rol)
                            VALUES ('AdminUser', 'AdminLastName', 30, 'admin1234', 'Admin')''')
            
    def insertar_materias_por_defecto(self):
        """Inserta un conjunto de materias predeterminadas para la carrera de programación."""
        materias = [
            ("Introducción a la Programación", None),
            ("Estructuras de Datos", None),
            ("Bases de Datos", None),
            ("Programación Orientada a Objetos", None),
            ("Desarrollo Web", None),
            ("Sistemas Operativos", None),
            ("Redes y Comunicaciones", None),
            ("Ingeniería de Software", None),
            ("Inteligencia Artificial", None),
            ("Algoritmos y Complejidad", None)
        ]
        
        cursor = self.cnn.cursor()
        for nombre, id_profesor in materias:
            cursor.execute(
                "INSERT OR IGNORE INTO materia (nombre, id_profesor) VALUES (?, ?)", (nombre, id_profesor)
            )
        
        self.cnn.commit()
        print("Materias predeterminadas insertadas correctamente.")
    
    def cerrar_conexion(self):
        if self.cnn:
            self.cnn.close()

class Usuarios:
    def __init__(self, db):
        self.cnn = db.cnn  # Usar cnn para la conexión de base de datos

    def obtener_id_alumno(self, nombre_usuario):
        """Obtiene el id_alumnos basado en el nombre de usuario del alumno"""
        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT id_alumnos FROM Alumnos WHERE nombre = ?", (nombre_usuario,))
            resultado = cur.fetchone()
            cur.close()
            return resultado[0] if resultado else None
        except sqlite3.Error as e:
            print(f"Error al obtener id_alumno para {nombre_usuario}: {e}")
            return None

    def obtener_id_profesor(self, nombre_usuario):
        """Obtiene el id_profesor basado en el nombre de usuario del profesor"""
        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT id_profesor FROM profesor WHERE nombre = ?", (nombre_usuario,))
            resultado = cur.fetchone()
            cur.close()
            return resultado[0] if resultado else None
        except sqlite3.Error as e:
            print(f"Error al obtener id_profesor para {nombre_usuario}: {e}")
            return None

    def registrar_usuario(self, nombre, apellido, edad, contraseña, rol):
        try:
            cursor = self.cnn.cursor()
            cursor.execute(
                "INSERT INTO usuarios (nombre, apellido, edad, password, rol) VALUES (?, ?, ?, ?, ?)",
                (nombre, apellido, edad, contraseña, rol)
            )
            user_id = cursor.lastrowid  # Obtiene el ID del usuario recién insertado
            self.cnn.commit()
            
            # Si el rol es "Alumno", insertar también en la tabla Alumnos
            if rol == "Alumno":
                cursor.execute(
                    "INSERT INTO Alumnos (id_usuario, nombre, apellido, nota, rol) VALUES (?, ?, ?, ?, ?)",
                    (user_id, nombre, apellido, None, rol)
                )
                self.cnn.commit()
            
            # Si el rol es "Profesor", insertar también en la tabla Profesor
            elif rol == "Profesor":
                cursor.execute(
                    "INSERT INTO profesor (id_usuario, nombre, apellido) VALUES (?, ?, ?)",
                    (user_id, nombre, apellido)
                )
                self.cnn.commit()

            cursor.close()
            return True
        except sqlite3.Error as e:
            print(f"Error al registrar usuario: {e}")
            return False

    def verificar_usuario(self, usuario, contraseña):
        try:
            cursor = self.cnn.cursor()
            cursor.execute("SELECT password FROM usuarios WHERE nombre = ?", (usuario,))
            resultado = cursor.fetchone()
            cursor.close()
            
            if resultado:
                stored_password = resultado[0]  # Obtener la contraseña almacenada en texto plano
                return contraseña == stored_password  # Comparar la contraseña ingresada con la almacenada
            else:
                return False
        except sqlite3.Error as e:
            print(f"Error al verificar usuario: {e}")
            return False

    def obtener_rol_usuario(self, usuario):
        """Obtiene el rol de un usuario específico."""
        try:
            if not usuario:
                return None
            
            cursor = self.cnn.cursor()
            cursor.execute("SELECT rol FROM usuarios WHERE nombre = ?", (usuario,))
            resultado = cursor.fetchone()
            cursor.close()
            return resultado[0] if resultado else None  # Retorna el rol o None si no existe
        except sqlite3.Error as e:
            print(f"Error al obtener el rol del usuario: {e}")
            return None

class Alumnos:
    def __init__(self, db):
        self.db = db
        self.cnn = db.cnn
        print(f"[DEBUG] Conexión de base de datos asignada a Alumnos: {self.db}")

    def modificar_nota(self, alumno_id, nueva_nota):
        
        try:
            print(f"[DEBUG] Intentando modificar nota para alumno_id={alumno_id} a nueva_nota={nueva_nota}")
            print(f"[DEBUG] Verificando conexión de base de datos en Alumnos: {self.db}")
            if not self.db or not hasattr(self.db, 'cnn'):
                print("[ERROR] La conexión a la base de datos no está disponible en la instancia de Alumnos.")
                return False
            
            cur = self.db.cnn.cursor()  
            query = "UPDATE alumnos SET nota = ? WHERE id_alumnos = ?"
            cur.execute(query, (nueva_nota, alumno_id))
            self.db.cnn.commit()  
            cur.close()
            print(f"[DEBUG] Nota actualizada para alumno ID {alumno_id}: {nueva_nota}")
            return True
        except sqlite3.Error as e:
            print(f"[ERROR] Error al actualizar la nota del alumno: {e}")
            return False

    def consulta_alumno(self,id_alumnos):
            try:
                cur = self.cnn.cursor()
                cur.execute("SELECT * FROM Alumnos WHERE id_alumnos = ?", (id_alumnos,))
                datos = cur.fetchone()  
                cur.close()
                return datos
            except sqlite3.Error as e:
                print(f"Error al consultar alumno por ID: {e}")
                return None

    def buscar_alumno(self, texto_busqueda):
        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM Alumnos WHERE nombre LIKE ? OR apellido LIKE ?", 
                        (f'%{texto_busqueda}%', f'%{texto_busqueda}%'))
            resultados = cur.fetchall()
            cur.close()
            return resultados if resultados else []
        except sqlite3.Error as e:
            print(f"Error al buscar alumno: {e}")
            return []

    def elimina_alumno(self, id_alumnos):
        try:
            cur = self.cnn.cursor()
            cur.execute("DELETE FROM Alumnos WHERE id_alumno = ?", (id_alumnos,))
            self.cnn.commit()
            cur.close()
            return True
        except sqlite3.Error as e:
            print(f"Error al eliminar alumno: {e}")
            return False

    def inserta_alumno(self, nombre, apellido, nota):
        try:
            cur = self.cnn.cursor()
            cur.execute("INSERT INTO Alumnos (nombre, apellido, nota, rol) VALUES (?, ?, ?, 'Alumno')", 
                        (nombre, apellido, nota))
            self.cnn.commit()
            cur.close()
            return True
        except sqlite3.Error as e:
            print(f"Error al insertar alumno: {e}")
            return False

    def modifica_alumno(self, id_alumnos, nombre, apellido, nota):
        try:
            cur = self.cnn.cursor()
            cur.execute("UPDATE Alumnos SET nombre = ?, apellido = ?, nota = ? WHERE id_alumnos = ?", 
                        (nombre, apellido, nota, id_alumnos))
            self.cnn.commit()
            cur.close()
            return True
        except sqlite3.Error as e:
            print(f"Error al modificar alumno: {e}")
            return False
    def enviar_mensaje_al_profesor(self, id_alumnos, id_profesor, mensaje):
        """Envía un mensaje del alumno al profesor y lo guarda en la tabla notificaciones."""
        try:
            print(f"[DEBUG] Enviando mensaje al profesor ID {id_profesor} desde alumno ID {id_alumnos}")
            print(f"[DEBUG] Mensaje a enviar: {mensaje}")

            cur = self.db.cnn.cursor()
            query = """
                INSERT INTO notificaciones (id_alumnos, id_profesor, notificacion, fecha)
                VALUES (?, ?, ?, datetime('now'))
            """
            print(f"[DEBUG] Ejecutando consulta SQL para enviar mensaje al profesor: {query}")
            cur.execute(query, (id_alumnos, id_profesor, mensaje))
            self.db.cnn.commit() 
            cur.close()
            
            print(f"[DEBUG] Mensaje enviado correctamente al profesor ID {id_profesor}")
            return True
        except sqlite3.Error as e:
            print(f"[ERROR] Error al enviar mensaje al profesor: {e}")
            return False

        
    def enviar_respuesta_al_alumno(self, id_alumno, mensaje):
        """Envía una respuesta al alumno y la guarda en la tabla notificaciones"""
        try:
            print(f"[DEBUG] Preparando para enviar respuesta al alumno ID {id_alumno}")
            print(f"[DEBUG] Contenido de la respuesta: {mensaje}")

            cur = self.db.cnn.cursor()
            query = """
                INSERT INTO notificaciones (id_profesor, id_alumnos, notificacion, fecha)
                VALUES (?, ?, ?, datetime('now'))
            """
            print(f"[DEBUG] Ejecutando consulta SQL para enviar respuesta al alumno: {query}")
            cur.execute(query, (self.id_profesor, id_alumno, mensaje))
            self.db.cnn.commit()
            cur.close()
            
            print(f"[DEBUG] Respuesta enviada correctamente al alumno ID {id_alumno}")
            return True
        except sqlite3.Error as e:
            print(f"[ERROR] Error al enviar respuesta al alumno: {e}")
            return False

        
    def obtener_id_alumno_por_nombre(self, nombre):
        """Obtiene el ID del alumno dado su nombre completo"""
        try:
            print(f"[DEBUG] Buscando ID de alumno para nombre: {nombre}")
            cur = self.db.cnn.cursor()
            query = "SELECT id_alumnos FROM alumnos WHERE nombre = ?"
            cur.execute(query, (nombre,))
            result = cur.fetchone()
            cur.close()

            if result:
                print(f"[DEBUG] ID encontrado para {nombre}: {result[0]}")
                return result[0]
            else:
                print(f"[ERROR] No se encontró un alumno con el nombre: {nombre}")
                return None
        except sqlite3.Error as e:
            print(f"[ERROR] Error al obtener el ID del alumno por nombre: {e}")
            return None
        
    def consulta_alumnos_por_materia(self, id_profesor):
        """Consulta los alumnos inscritos en las materias asignadas al profesor especificado, incluyendo el nombre de la materia y la nota."""
        try:
            print(f"[DEBUG] Ejecutando consulta_alumnos_por_materia con id_profesor: {id_profesor}")
            cur = self.cnn.cursor()
            query = """
                SELECT DISTINCT a.id_alumnos, a.nombre, a.apellido, a.nota
                FROM inscripcion i
                JOIN alumnos a ON i.id_alumnos = a.id_alumnos
                JOIN materia m ON i.id_materia = m.id_materia
                WHERE m.id_profesor = ?
            """
            print(f"[DEBUG] Consulta SQL ajustada: {query}")
            alumnos = cur.fetchall()
            print(f"[DEBUG] Resultados obtenidos: {alumnos}")
            cur.close()
            print(f"Resultado de consulta_alumnos_por_materia: {alumnos}")  # Depuración
            return alumnos
        except sqlite3.Error as e:
            print(f"Error al consultar alumnos por materia: {e}")
            return []

class Profesores:
    def __init__(self, db):
        self.cnn = db.cnn

    def consultar_profesores(self, id_profesor):
        try:
            cur = self.cnn.cursor()  
            cur.execute("SELECT nombre FROM profesor WHERE id_profesor = ?", (id_profesor,))
            resultado = cur.fetchone()
            cur.close()
            return resultado[0] if resultado else "Profesor Desconocido"
        except sqlite3.Error as e:
            print(f"Error al consultar el nombre del profesor: {e}")
            return "Profesor Desconocido"

    
    def agregar_profesor(self, nombre, apellido):
        try:
            with self.cnn:
                cur = self.cnn.cursor()
                cur.execute("INSERT INTO profesor (nombre, apellido) VALUES (?, ?)", (nombre, apellido))
                return True
        except sqlite3.Error as e:
            print(f"Error al agregar profesor: {e}")
            return False
    def leer_mensajes_alumnos(self, id_profesor):
        """Obtiene los mensajes enviados al profesor por los alumnos."""
        try:
            cur = self.cnn.cursor()
            cur.execute("""
                SELECT a.nombre, a.apellido, n.mensaje, n.fecha
                FROM notificaciones n
                JOIN alumnos a ON n.id_alumnos = a.id_alumnos
                WHERE n.id_profesor = ?
                ORDER BY n.fecha DESC
            """, (id_profesor,))
            mensajes = cur.fetchall()
            cur.close()
            return mensajes
        except sqlite3.Error as e:
            print(f"Error al leer mensajes de alumnos: {e}")
            return []

class Materias:
    def __init__(self, db):
        self.cnn = db.cnn

    def consulta_materias(self):
            try:
                cur = self.cnn.cursor()
                cur.execute("SELECT m.nombre, p.nombre FROM materia m JOIN profesor p ON m.id_profesor = p.id_profesor")
                materias = cur.fetchall()
                cur.close()
                return materias
            except sqlite3.Error as e:
                print(f"Error al consultar materias: {e}")
                return []

    def agregar_materia(self, nombre_materia, id_profesor):
        try:
            with self.cnn:
                cur = self.cnn.cursor()
                cur.execute("INSERT INTO materia (nombre, id_profesor) VALUES (?, ?)", 
                            (nombre_materia, id_profesor))
                return True
        except sqlite3.Error as e:
            print(f"Error al agregar materia: {e}")
            return False

class Inscripciones:
    def __init__(self, db):
        self.db = db
        self.cnn = db.cnn 

    def consulta_inscripciones(self, id_alumnos):
        try:
            cur = self.cnn.cursor()
            cur.execute("""
                SELECT materia.nombre, materia.id_profesor, inscripcion.fecha_inscripcion
                FROM inscripcion
                JOIN materia ON inscripcion.id_materia = materia.id_materia
                WHERE inscripcion.id_alumnos = ?
            """, (id_alumnos,))
            inscripciones = cur.fetchall()
            cur.close()
            return inscripciones
        except sqlite3.Error as e:
            print(f"Error al consultar inscripciones: {e}")
            return []

    def inscribir_alumno(self, id_alumnos, id_materia, fecha_inscripcion):
        try:
            cur = self.cnn.cursor()
            cur.execute("INSERT INTO inscripcion (id_alumnos, id_materia,fecha_inscripcion) VALUES (?, ?, ?)", (id_alumnos, id_materia, fecha_inscripcion))
            self.cnn.commit()
            cur.close()
            return True
        except sqlite3.Error as e:
            print(f"Error al inscribir alumno: {e}")
            return False

    def existe_alumno(self, id_alumnos):
        try:
            with self.cnn.cursor() as cur:
                cur.execute("SELECT 1 FROM Alumnos WHERE id_alumnos = ?", (id_alumnos,))
                return cur.fetchone() is not None
        except sqlite3.Error:
            return False

    def existe_materia(self, id_materia):
        try:
            with self.cnn.cursor() as cur:
                cur.execute("SELECT 1 FROM materia WHERE id_materia = ?", (id_materia,))
                return cur.fetchone() is not None
        except sqlite3.Error:
            return False
    def consulta_materias(self):
        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT id_materia, nombre FROM materia")
            materias = cur.fetchall()
            cur.close()
            return materias
        except sqlite3.Error as e:
            print(f"Error al consultar materias: {e}")
            return []
        
    def obtener_id_profesor_por_alumno(self, id_alumnos):
        """Obtiene el id del profesor en función del id del alumno inscrito en una materia."""
        try:
            cur = self.cnn.cursor()
            cur.execute("""
                SELECT m.id_profesor
                FROM inscripcion i
                JOIN materia m ON i.id_materia = m.id_materia
                WHERE i.id_alumnos = ?
            """, (id_alumnos,))
            resultado = cur.fetchone()
            cur.close()
            return resultado[0] if resultado else None
        except sqlite3.Error as e:
            print(f"Error al obtener id_profesor por alumno: {e}")
            return None
        
    def consulta_materias_por_alumno(self, id_alumnos):
        """Obtiene las materias inscritas por un alumno específico junto con el nombre del profesor y la nota."""
        try:
            cur = self.cnn.cursor()
            cur.execute("""
                SELECT m.nombre AS materia, p.nombre AS profesor, a.nota
                FROM inscripcion i
                JOIN materia m ON i.id_materia = m.id_materia
                JOIN profesor p ON m.id_profesor = p.id_profesor
                JOIN alumnos a ON i.id_alumnos = a.id_alumnos
                WHERE i.id_alumnos = ?
            """, (id_alumnos,))
            materias = cur.fetchall()
            cur.close()
            return materias
        except sqlite3.Error as e:
            print(f"Error al consultar materias por alumno: {e}")
            return []
    def consulta_alumnos_por_materia(self, id_profesor):
        """Consulta los alumnos inscritos en las materias asignadas al profesor especificado."""
        try:
            cur = self.cnn.cursor()
            cur.execute("""
                SELECT a.id_alumnos, a.nombre, a.apellido, a.nota
                FROM inscripcion i
                JOIN alumnos a ON i.id_alumnos = a.id_alumnos
                JOIN materia m ON i.id_materia = m.id_materia
                WHERE m.id_profesor = ?
            """, (id_profesor,))
            alumnos = cur.fetchall()
            cur.close()
            return alumnos
        except sqlite3.Error as e:
            print(f"Error al consultar alumnos por materia: {e}")
            return []
        
    def obtener_mensajes_para_alumno(self, id_alumnos):
        """Obtiene los mensajes enviados al alumno específico desde la tabla notificaciones"""
        try:
            print(f"[DEBUG] Buscando mensajes para alumno ID: {id_alumnos}")
            cur = self.db.cnn.cursor()
            query = """
                SELECT mensaje, fecha
                FROM notificaciones
                WHERE id_alumnos = ? AND id_profesor IS NOT NULL
                ORDER BY fecha DESC
            """
            cur.execute(query, (id_alumnos,))
            mensajes = cur.fetchall()
            cur.close()
            
            print(f"[DEBUG] Mensajes encontrados para alumno ID {id_alumnos}: {mensajes}")
            return mensajes
        except sqlite3.Error as e:
            print(f"[ERROR] Error al obtener mensajes para el alumno: {e}")
            return []

