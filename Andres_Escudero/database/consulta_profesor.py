import sqlite3
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
bdd = os.path.abspath("c:/Users/Emula/Desktop/Python-CRUD-QT/mi_base_de_datos.db")

class Profesor:
    def __init__(self, db_path=bdd):
        self.db_path = db_path
        self.cnn = sqlite3.connect(self.db_path)
        print(f"Conectando a la base de datos en: {self.db_path}")

    def obtener_nombre_profesor(self, id_profesor):
        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT nombre FROM profesor WHERE id = ?", (id_profesor,))
            resultado = cur.fetchone()
            return resultado[0] if resultado else "Desconocido"
        except sqlite3.Error as e:
            print(f"Error al obtener el nombre del profesor: {e}")
            return "Desconocido"

    def agregar_profesor(self, nombre, apellido):
        try:
            cursor = self.cnn.cursor()
            cursor.execute("INSERT INTO profesor (nombre, apellido) VALUES (?, ?)", (nombre, apellido))
            self.cnn.commit()
        except sqlite3.Error as e:
            print(f"Error al agregar profesor: {e}")

    def consultar_profesores(self):
        try:
            cursor = self.cnn.cursor()
            cursor.execute("SELECT * FROM profesor")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al consultar profesor: {e}")
            return []

    def actualizar_profesor(self, id_profesor, nuevo_nombre, nuevo_apellido):
        try:
            cursor = self.cnn.cursor()
            cursor.execute("UPDATE profesor SET nombre=?, apellido=? WHERE id=?", (nuevo_nombre, nuevo_apellido, id_profesor))
            self.cnn.commit()
        except sqlite3.Error as e:
            print(f"Error al actualizar profesor: {e}")

    def eliminar_profesor(self, id_profesor):
        try:
            cursor = self.cnn.cursor()
            cursor.execute("DELETE FROM profesor WHERE id=?", (id_profesor,))
            self.cnn.commit()
        except sqlite3.Error as e:
            print(f"Error al eliminar profesor: {e}")

    def __del__(self):
        if self.cnn:
            self.cnn.close()
