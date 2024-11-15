import sqlite3
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
bdd = os.path.abspath("c:/Users/Emula/Desktop/Python-CRUD-QT/mi_base_de_datos.db")

class Alumnos:

    def __init__(self, db_path=bdd):
        self.db_path = db_path
        self.cnn = sqlite3.connect(self.db_path)
        print(f"Conectando a la base de datos en: {self.db_path}")
        
    def consulta_alumno(self):
            try:
                cur = self.cnn.cursor()
                cur.execute("SELECT * FROM Alumnos")
                datos = cur.fetchall()
                cur.close()
                return datos
            except sqlite3.Error as e:
                print(f"Error al consultar alumnos: {e}")
                return []

    def buscar_alumno(self, texto_busqueda):
            try:
                with self.cnn.cursor() as cursor:
                    query = "SELECT * FROM Alumnos WHERE nombre LIKE ? OR apellido LIKE ?"
                    cursor.execute(query, (f'%{texto_busqueda}%', f'%{texto_busqueda}%'))
                    resultados = cursor.fetchall()
                return resultados if resultados else []
            except sqlite3.Error as e:
                print(f"Error al buscar alumno: {e}")
                return []


    def inserta_alumno(self, nombre, apellido, nota):
            print(f"Insertando alumno: {nombre}, {apellido}, {nota}")
            try:
                cur = self.cnn.cursor(bdd)
                sql = "INSERT INTO Alumnos (nombre, apellido, nota) VALUES (?, ?, ?)"
                cur.execute(sql, (nombre, apellido, nota))
                self.cnn.commit()
                n = cur.rowcount
                cur.close()
                return n
            except sqlite3.Error as e:
                print(f"Error al insertar alumno: {e}")
                return 0

    def elimina_alumno(self, Id):
            try:
                cur = self.cnn.cursor()
                sql = "DELETE FROM Alumnos WHERE id = ?"
                cur.execute(sql, (Id,))
                self.cnn.commit()
                n = cur.rowcount
                cur.close()
                return n
            except sqlite3.Error as e:
                print(f"Error al eliminar alumno: {e}")
                return 0

    def modifica_alumno(self, nombre, apellido, nota):
            try:
                cur = self.cnn.cursor()
                sql = "UPDATE Alumnos SET nombre = ?, apellido = ?, nota = ? WHERE id = ?"
                cur.execute(sql, (nombre, apellido, nota))
                self.cnn.commit()
                n = cur.rowcount
                cur.close()
                return n
            except sqlite3.Error as e:
                print(f"Error al modificar alumno: {e}")
                return 0
    def inscribir_alumno(self, id_alumno, id_materia, fecha_inscripcion):
            try:
                cur = self.cnn.cursor()
                sql = "INSERT INTO inscripcion (id_alumno, id_materia, fecha_inscripcion) VALUES (?, ?, ?)"
                cur.execute(sql, (id_alumno, id_materia, fecha_inscripcion))
                self.cnn.commit()
                n = cur.rowcount
                cur.close()
                return n
            except sqlite3.Error as e:
                print(f"Error al inscribir alumno: {e}")
                return 0