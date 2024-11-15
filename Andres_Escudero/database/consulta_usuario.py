import sqlite3
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
bdd = os.path.abspath("c:/Users/Emula/Desktop/Python-CRUD-QT/mi_base_de_datos.db")

class Usuarios:
    def __init__(self, db_path=bdd):
        self.db_path = db_path
        self.cnn = sqlite3.connect(self.db_path)
        print(f"Conectando a la base de datos en: {self.db_path}")

    def registrar_usuario(self, nombre, apellido, edad, password, rol):
        try:
            cursor = self.cnn.cursor()
            sql = "INSERT INTO usuarios (nombre, apellido, edad, password, rol) VALUES (?, ?, ?, ?, ?)"
            cursor.execute(sql, (nombre, apellido, edad, password, rol))
            self.cnn.commit()
            cursor.close()
            print("Usuario registrado exitosamente.")
            return True
        except sqlite3.Error as e:
            print(f"Error al registrar usuario: {e}")
            return False

    def verificar_usuario(self, usuario, contraseña):
        try:
            cursor = self.cnn.cursor()
            cursor.execute("SELECT password FROM usuarios WHERE nombre = ?", (usuario,))
            resultado = cursor.fetchone()
            if resultado and resultado[0] == contraseña:
                return True  # Las credenciales son válidas
            return False  # Las credenciales son inválidas
        except sqlite3.Error as e:
            print(f"Error al verificar usuario: {e}")
            return False    

    def obtener_rol_usuario(self, usuario):
        try:
            cursor = self.cnn.cursor()
            sql = "SELECT rol FROM usuarios WHERE nombre = ?"
            cursor.execute(sql, (usuario,))
            resultado = cursor.fetchone()
            cursor.close()
            if resultado:
                return resultado[0]  # Devuelve el rol del usuario
            else:
                return None  # Usuario no encontrado
        except sqlite3.Error as e:
            print(f"Error al obtener el rol del usuario: {e}")
            return None
    def get_usuario_id(self, nombre, apellido):
        conn = sqlite3.connect("c:/Users/Emula/Desktop/Python-CRUD-QT/mi_base_de_datos.db")
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM usuarios WHERE nombre = ? AND apellido = ?", (nombre, apellido))
            result = cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Error al obtener el ID del usuario: {e}")
            return None
        finally:
            conn.close()
