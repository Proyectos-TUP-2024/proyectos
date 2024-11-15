import sqlite3
import os
from db import Database

class Alumnos:
    def __init__(self, database):
        self.cnn = database.cnn  # Usa la conexión proporcionada por Database

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
            cur = self.cnn.cursor()
            query = "SELECT * FROM Alumnos WHERE nombre LIKE ? OR apellido LIKE ?"
            cur.execute(query, (f'%{texto_busqueda}%', f'%{texto_busqueda}%'))
            resultados = cur.fetchall()
            cur.close()
            return resultados if resultados else []
        except sqlite3.Error as e:
            print(f"Error al buscar alumno: {e}")
            return []

    def inserta_alumno(self, nombre, apellido, nota):
        try:
            cur = self.cnn.cursor()
            sql = "INSERT INTO Alumnos (nombre, apellido, nota) VALUES (?, ?, ?)"
            cur.execute(sql, (nombre, apellido, nota))
            self.cnn.commit()
            n = cur.rowcount
            cur.close()
            return n
        except sqlite3.Error as e:
            print(f"Error al insertar alumno: {e}")
            return 0

    def elimina_alumno(self, id):
        try:
            cur = self.cnn.cursor()
            sql = "DELETE FROM Alumnos WHERE id = ?"
            cur.execute(sql, (id,))
            self.cnn.commit()
            n = cur.rowcount
            cur.close()
            return n
        except sqlite3.Error as e:
            print(f"Error al eliminar alumno: {e}")
            return 0

    def modifica_alumno(self, id, nombre, apellido, nota):
        try:
            cur = self.cnn.cursor()
            sql = "UPDATE Alumnos SET nombre = ?, apellido = ?, nota = ? WHERE id = ?"
            cur.execute(sql, (nombre, apellido, nota, id))
            self.cnn.commit()
            n = cur.rowcount
            cur.close()
            return n
        except sqlite3.Error as e:
            print(f"Error al modificar alumno: {e}")
            return 0
