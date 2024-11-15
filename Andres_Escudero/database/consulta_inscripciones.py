import sqlite3
import os
base_dir = os.path.dirname(os.path.abspath(__file__))
bdd = os.path.abspath("c:/Users/Emula/Desktop/Python-CRUD-QT/mi_base_de_datos.db")

class inscripciones:
    def __init__(self, db_path=bdd):
        self.db_path = db_path
        self.cnn = sqlite3.connect(self.db_path)
        print(f"Conectando a la base de datos en: {self.db_path}")

    
    def consulta_inscripciones(self, id_alumno):
            try:
                cur = self.cnn.cursor()
                sql = """
                    SELECT m.nombre, m.id_profesor, i.fecha_inscripcion
                    FROM inscripcion i
                    JOIN materia m ON i.id_materia = m.id
                    WHERE i.id_alumno = ?
                """
                cur.execute(sql, (id_alumno,))
                datos = cur.fetchall()
                cur.close()
                return datos
            except sqlite3.Error as e:
                print(f"Error al consultar inscripciones: {e}")
                return []