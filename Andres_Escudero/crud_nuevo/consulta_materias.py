import sqlite3
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
bdd = os.path.abspath("c:/Users/Emula/Desktop/Python-CRUD-QT/mi_base_de_datos.db")

class Materias:
    def __init__(self, db_path=bdd):
        self.db_path = db_path
        self.cnn = sqlite3.connect(self.db_path)
        print(f"Conectando a la base de datos en: {self.db_path}")

    def consulta_materias(self):
        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT m.nombre, p.nombre FROM materia m JOIN profesor p ON m.id_profesor = p.id")
            datos = cur.fetchall()
            cur.close()
            return datos
        except sqlite3.Error as e:
            print(f"Error al consultar materia: {e}")
            return []

    def agregar_materia(self, nombre_materia, nombre_profesor):
        try:
            cursor = self.cnn.cursor()
            cursor.execute("INSERT INTO materia (nombre, id_profesor) VALUES (?, (SELECT id FROM profesor WHERE nombre=?))", 
                           (nombre_materia, nombre_profesor))
            self.cnn.commit()
        except sqlite3.Error as e:
            print(f"Error al agregar materia: {e}")

    def actualizar_materia(self, id_materia, nuevo_nombre, nuevo_profesor):
        try:
            cursor = self.cnn.cursor()
            cursor.execute("UPDATE materia SET nombre=?, id_profesor=(SELECT id FROM profesor WHERE nombre=?) WHERE id=?", 
                           (nuevo_nombre, nuevo_profesor, id_materia))
            self.cnn.commit()
        except sqlite3.Error as e:
            print(f"Error al actualizar materia: {e}")

    def eliminar_materia(self, id_materia):
        try:
            cursor = self.cnn.cursor()
            cursor.execute("DELETE FROM materia WHERE id=?", (id_materia,))
            self.cnn.commit()
        except sqlite3.Error as e:
            print(f"Error al eliminar materia: {e}")

    def __del__(self):
        if self.cnn:
            self.cnn.close()
