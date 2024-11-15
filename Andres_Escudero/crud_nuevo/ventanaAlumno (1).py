from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QTreeWidget, QTreeWidgetItem, QCalendarWidget, QTextEdit, QTabWidget
)
from PyQt6.QtCore import Qt
import sys
from .ventanaInscripcion import VentanaInscripcion
from database.consulta_alumno import Alumnos


class VentanaAlumno(QMainWindow):
    def __init__(self):
        super().__init__()

        
        self.setWindowTitle("Ventana del Alumno")
        self.setGeometry(100, 100, 800, 600)

        # Crear el widget central y el layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Layout para el botón "Regresar"
        top_layout = QHBoxLayout()
        main_layout.addLayout(top_layout)

        # Botón "Regresar"
        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.clicked.connect(self.fAtras)  # Conectar a un método
        top_layout.addWidget(self.btn_regresar)
        top_layout.addStretch()  # Añade un espaciador para empujar el botón a la derecha

        # Pestañas para organizar secciones
        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)

        # 1. Resumen de Materias y Calificaciones
        self.tab_materias = QWidget()
        self.init_tab_materias()
        tab_widget.addTab(self.tab_materias, "Materias y Calificaciones")

    
        # 2. Calendario Académico
        self.tab_calendario = QWidget()
        self.init_tab_calendario()
        tab_widget.addTab(self.tab_calendario, "Calendario Académico")

        # 3. Foro o Mensajería con Profesores
        self.tab_mensajeria = QWidget()
        self.init_tab_mensajeria()
        tab_widget.addTab(self.tab_mensajeria, "Mensajería")

        # 4. Recursos de Estudio
        self.tab_recursos = QWidget()
        self.init_tab_recursos()
        tab_widget.addTab(self.tab_recursos, "Recursos de Estudio")

        # 5. Perfil del Alumno
        self.tab_perfil = QWidget()
        self.init_tab_perfil()
        tab_widget.addTab(self.tab_perfil, "Perfil")

        # Botón para inscribirse en materias (debería estar en el layout principal)
        self.btn_inscripcion = QPushButton("Inscribirse en Materias")
        self.btn_inscripcion.clicked.connect(self.mostrar_inscripcion)
        main_layout.addWidget(self.btn_inscripcion)

        self.init_tab_materias()
    def init_tab_materias(self):
        layout = QVBoxLayout()
        self.tab_materias.setLayout(layout)

        label = QLabel("Resumen de Materias y Calificaciones")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        # Widget de calificaciones
        tree_widget = QTreeWidget()
        tree_widget.setColumnCount(3)
        tree_widget.setHeaderLabels(["Materia", "Profesor", "Calificación"])
        layout.addWidget(tree_widget)

          # Importa la clase necesaria
        self.consulta_alumnos = Alumnos()  # Inicializa la clase

          # Llama al método para inicializar las materias

        # Agregar algunas materias y calificaciones de ejemplo
        inscripciones = self.consulta_alumno.consulta_inscripciones(id_alumno=1)  # Cambia el ID por el del alumno actual
        for materia, id_profesor, fecha in inscripciones:
            # Aquí puedes obtener el nombre del profesor si lo deseas
            profesor_nombre = self.obtener_nombre_profesor(id_profesor)
            QTreeWidgetItem(tree_widget, [materia, profesor_nombre, ""])  # Aquí puedes añadir la calificación si la tienes

    def init_tab_calendario(self):
        layout = QVBoxLayout()
        self.tab_calendario.setLayout(layout)

        label = QLabel("Calendario Académico")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        # Calendario
        calendar = QCalendarWidget()
        layout.addWidget(calendar)

    def init_tab_mensajeria(self):
        layout = QVBoxLayout()
        self.tab_mensajeria.setLayout(layout)

        label = QLabel("Foro o Mensajería con Profesores")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        # Espacio de mensajes
        mensajes = QTextEdit()
        mensajes.setPlaceholderText("Mensajes de profesores...")
        mensajes.setReadOnly(True)
        layout.addWidget(mensajes)

        # Enviar mensaje
        self.nuevo_mensaje = QTextEdit()
        self.nuevo_mensaje.setPlaceholderText("Escribe tu mensaje aquí...")
        layout.addWidget(self.nuevo_mensaje)

        enviar_btn = QPushButton("Enviar Mensaje")
        enviar_btn.clicked.connect(self.enviar_mensaje)
        layout.addWidget(enviar_btn)

    def init_tab_recursos(self):
        layout = QVBoxLayout()
        self.tab_recursos.setLayout(layout)

        label = QLabel("Recursos de Estudio")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        # Lista de recursos
        tree_widget = QTreeWidget()
        tree_widget.setColumnCount(2)
        tree_widget.setHeaderLabels(["Recurso", "Descripción"])
        layout.addWidget(tree_widget)

        # Ejemplo de recursos
        recursos = [
            ("Presentación Matemáticas", "Temas de cálculo y álgebra."),
            ("PDF Historia", "Guía de estudio de la Edad Media."),
            ("Video Química", "Reacciones químicas en la vida diaria.")
        ]
        for recurso, descripcion in recursos:
            QTreeWidgetItem(tree_widget, [recurso, descripcion])

    def init_tab_perfil(self):
        layout = QVBoxLayout()
        self.tab_perfil.setLayout(layout)

        label = QLabel("Perfil del Alumno")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        # Información del alumno
        info = QLabel("Nombre: Juan Pérez\nCarrera: Ingeniería\nAño de Ingreso: 2020\nPromedio: 8.3")
        layout.addWidget(info)

    def enviar_mensaje(self):
        mensaje = self.nuevo_mensaje.toPlainText()
        if mensaje:
            print(f"Mensaje enviado: {mensaje}")
            self.nuevo_mensaje.clear()
        
    def mostrar_inscripcion(self):
        materias_existentes = self.alumnos_db.consulta_materias()  # Obtener materias de la base de datos
        self.ventana_inscripcion = VentanaInscripcion(materias_existentes, alumno_id=1)  # Cambiar ID por el del alumno actual
        self.ventana_inscripcion.show()
        

    def fAtras(self):
        self.close()
        self.ventana1.show()