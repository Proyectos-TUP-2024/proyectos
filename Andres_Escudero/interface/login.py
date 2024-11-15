from PyQt6.QtWidgets import (
    QApplication, QComboBox, QWidget,QInputDialog, QDateEdit, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QMainWindow, QHBoxLayout
)
from PyQt6.QtCore import Qt, QFile,QIODevice,QTextStream
from PyQt6.QtGui import QPixmap
import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from database.db_nueva import Alumnos, Inscripciones
from database.db_nueva import Database, Usuarios  
from interface.ventanaAdministrador import VentanaAdmin
from interface.ventanaProfesor import VentanaProfesor
from interface.ventanaAlumno import VentanaAlumno

class VentanaLogin(QMainWindow):
    def __init__(self,db):
        super().__init__()
        self.db = db
        self.usuarios = Usuarios(self.db)
        
        self.scale = 70
        self.setGeometry(40, 100, 400, 300)
        self.setWindowTitle("Login")  

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setStyleSheet("background-color: rgb(105, 105, 105);")
        

        self.layout_general = QHBoxLayout()
        self.form_layout = QVBoxLayout() 
        self.form_input_layout = QVBoxLayout()
        self.form_widget = QWidget()
        self.form_layout = QVBoxLayout(self.form_widget)
        

        self.img = QLabel()
        self.pixmap = QPixmap("./layout/fondo_logo.jpg").scaled(600, 600)
        self.img.setPixmap(self.pixmap)

 
        self.title = QLabel("Login")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("color: black; font-size: 36px; font-weight:bold;")
        self.title.setMaximumHeight(50)
        
        self.email = QLineEdit()
        self.email.setPlaceholderText("Usuario")
        self.email.setTextMargins(20, 0, 0, 0)
        self.email.setStyleSheet("background-color: white; border-radius: 15px; padding: 10px;") 
        self.email.setMinimumSize(int(self.width() * 0.5), 50)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Contraseña")
        self.password.setTextMargins(20, 0, 0, 0)
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setStyleSheet("background-color: white; border-radius: 15px; padding: 10px;")
        self.password.setMinimumSize(int(self.width() * 0.5), 50)

        self.btnLogin = QPushButton("Iniciar Sesion")
        self.btnLogin.setStyleSheet("background-color: #6339A7; font-size: 15px; font-weight: bold; border-radius: 15px; padding: 10px;")
        self.btnLogin.setMinimumSize(int(self.width() * 0.6), 50)
        self.btnLogin.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btnLogin.clicked.connect(self.iniciar_sesion)

        self.btnregistrar = QPushButton("Registrarse")
        self.btnregistrar.setStyleSheet("background-color: #6339A7; font-size: 15px; font-weight: bold; border-radius: 15px; padding: 10px;")
        self.btnregistrar.setMinimumSize(int(self.width() * 0.6), 50)
        self.btnregistrar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btnregistrar.clicked.connect(self.mostrar_registro)


        self.form_input_layout.addWidget(self.email)
        self.form_input_layout.addWidget(self.password)
        self.form_input_layout.addWidget(self.btnLogin)
        self.form_input_layout.addWidget(self.btnregistrar)
        self.form_input_layout.setSpacing(10)
        
      
        self.form_layout.addWidget(self.title)
        self.form_layout.addLayout(self.form_input_layout)
        self.form_layout.setSpacing(0)


        self.layout_general.addWidget(self.img)
        self.layout_general.addWidget(self.form_widget)
        self.layout_general.addLayout(self.form_layout)

        self.centralWidget.setLayout(self.layout_general)
        
     
        self.setMinimumSize(14 * self.scale, 7 * self.scale)
        self.setMaximumSize(14 * self.scale, 7 * self.scale)

    def mostrar_registro(self):
        self.ventana_registro = VentanaRegistro()
        self.ventana_registro.show()

    def iniciar_sesion(self):
        usuario = self.email.text()
        contraseña = self.password.text()
        usuarios = Usuarios(self.db)
        
        if usuarios.verificar_usuario(usuario, contraseña):
            rol = usuarios.obtener_rol_usuario(usuario)
            id_alumnos = usuarios.obtener_id_alumno(usuario)
            id_profesor = usuarios.obtener_id_profesor(usuario)
            self.mostrar_ventana_por_rol(rol, id_alumnos, id_profesor)
        else:
            QMessageBox.critical(self, "Error", "Usuario o contraseña incorrectos.")
                
    def mostrar_ventana_por_rol(self, rol, id_alumnos=None, id_profesor=None):
        if rol == "Profesor":
            self.ventana = VentanaProfesor(self, self.db, id_profesor)
        elif rol == "Alumno":
            self.ventana = VentanaAlumno(self, self.db, id_alumnos, id_profesor)
        elif rol == "Admin":
            self.ventana = VentanaAdmin(self, self.db)
        else:
            QMessageBox.warning(self, "Error", "Rol de usuario no reconocido.")
            return

        self.ventana.show()
        self.close()


    def show_login(self):
        print("Mostrando ventana de login")
        self.show()
    
class VentanaRegistro(QWidget):
    def __init__(self):
        super().__init__()
        
        css_path = os.path.join(os.path.dirname(__file__), "../css/styles.css")
        css_file = QFile(css_path)
        if css_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(css_file)
            self.setStyleSheet(stream.readAll())
            css_file.close()
            
        self.setObjectName("VentanaRegistro")
        self.setWindowTitle("Registro de Usuario")
        self.setGeometry(150, 150, 400, 250)
        
        layout = QVBoxLayout()
        
        self.rol = QComboBox()
        self.rol.setObjectName("rolComboBox")
        self.rol.addItems(["Seleccionar Rol", "Alumno", "Profesor"])  
        self.rol.currentTextChanged.connect(self.mostrar_combo_materia)  
        layout.addWidget(self.rol)
        
        self.nombre = QLineEdit()
        self.nombre.setPlaceholderText("Nombre")
        layout.addWidget(self.nombre)
        
        self.apellido = QLineEdit()
        self.apellido.setPlaceholderText("Apellido")
        layout.addWidget(self.apellido)
        
        self.edad = QLineEdit()
        self.edad.setPlaceholderText("Edad")
        layout.addWidget(self.edad)
        
        h_layout_fecha = QHBoxLayout()

        
        self.label_fecha_nacimiento = QLabel("Fecha de Nacimiento:")
        h_layout_fecha.addWidget(self.label_fecha_nacimiento)

        self.fecha_nacimiento = QDateEdit()
        self.fecha_nacimiento.setDisplayFormat("dd/MM/yyyy")
        self.fecha_nacimiento.setCalendarPopup(True)
        h_layout_fecha.addWidget(self.fecha_nacimiento)

        layout.addLayout(h_layout_fecha)
                
        self.password = QLineEdit()
        self.password.setPlaceholderText("Contraseña")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password)
        
  
        self.combo_materia = QComboBox()
        self.combo_materia.setVisible(False) 
        layout.addWidget(self.combo_materia)

 
        self.label_no_materias = QLabel("No hay materias disponibles. Por favor, crea una nueva materia.")
        self.label_no_materias.setVisible(False)
        layout.addWidget(self.label_no_materias)

    
        self.btnNuevaMateria = QPushButton("Crear Nueva Materia")
        self.btnNuevaMateria.setVisible(False)
        self.btnNuevaMateria.clicked.connect(self.crear_nueva_materia)
        layout.addWidget(self.btnNuevaMateria)

     
        self.btnRegistrar = QPushButton("Registrar")
        self.btnRegistrar.clicked.connect(self.registrar_usuario)
        layout.addWidget(self.btnRegistrar)

        self.setLayout(layout)

    def mostrar_combo_materia(self, rol):
        """Muestra el ComboBox de materias y opciones si el rol es Profesor."""
        if rol == "Profesor":
            self.cargar_materias()
            self.combo_materia.setVisible(True)
            if self.combo_materia.count() == 0:
                self.label_no_materias.setVisible(True)
                self.btnNuevaMateria.setVisible(True)
            else:
                self.label_no_materias.setVisible(False)
                self.btnNuevaMateria.setVisible(False)
        else:
            self.combo_materia.setVisible(False)
            self.label_no_materias.setVisible(False)
            self.btnNuevaMateria.setVisible(False)

    def cargar_materias(self):
        """Carga las materias en el ComboBox desde la base de datos."""
        db = Database()
        cursor = db.cnn.cursor()
        cursor.execute("SELECT id_materia, nombre FROM materia WHERE id_profesor IS NULL OR id_profesor = ''")
        materias = cursor.fetchall()
        cursor.close()

        self.combo_materia.clear()
        for id_materia, nombre in materias:
            self.combo_materia.addItem(nombre, id_materia)

    def crear_nueva_materia(self):
        """Crea una nueva materia sin asignar un profesor (id_profesor = NULL)."""
        nombre_materia, ok = QInputDialog.getText(self, "Crear Materia", "Nombre de la nueva materia:")
        if ok and nombre_materia:
            db = Database()
            cursor = db.cnn.cursor()
            cursor.execute("INSERT INTO materia (nombre) VALUES (?)", (nombre_materia,))
            db.cnn.commit()
            cursor.close()
            self.cargar_materias()
            QMessageBox.information(self, "Materia Creada", f"Materia '{nombre_materia}' creada exitosamente.")

    def registrar_usuario(self):
        """Registra el usuario y, si es profesor, asigna las materias seleccionadas."""
        nombre = self.nombre.text()
        apellido = self.apellido.text()
        edad = self.edad.text()
        contraseña = self.password.text()
        rol_seleccionado = self.rol.currentText()

        if rol_seleccionado == "Seleccionar Rol":
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione un rol.")
            return

        db = Database()
        db_usuarios = Usuarios(db)
        resultado = db_usuarios.registrar_usuario(nombre, apellido, edad, contraseña, rol_seleccionado)

        if resultado and rol_seleccionado == "Profesor":
            id_profesor = resultado  
            id_materia = self.combo_materia.currentData()  
            
            if id_materia:
                cursor = db.cnn.cursor()
                cursor.execute("UPDATE materia SET id_profesor = ? WHERE id_materia = ?", (id_profesor, id_materia))
                db.cnn.commit()
                cursor.close()

        if resultado:
            QMessageBox.information(self, "Éxito", "Usuario registrado exitosamente.")
            self.close()
        else:
            QMessageBox.critical(self, "Error", "Error al registrar el usuario.")