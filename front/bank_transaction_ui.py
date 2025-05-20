import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QComboBox, QLineEdit, QPushButton, QMessageBox, QDialog)
from PyQt5.QtGui import QIcon, QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer

class FaceAuthWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Banco Estelar - Autenticación Facial")
        self.setWindowIcon(QIcon("bank-icon.jpg"))  # Asegúrate de tener un ícono en el directorio
        self.setGeometry(100, 100, 600, 500)
        self.setMinimumSize(400, 400)

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Estilo
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f7fa;
            }
            QLabel {
                font-size: 16px;
                color: #2c3e50;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 16px;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1f618d;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
        """)

        # Título
        title_label = QLabel("Autenticación Facial")
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Etiqueta para mostrar el video
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setMinimumSize(320, 240)
        main_layout.addWidget(self.video_label, stretch=1)

        # Botón de confirmación
        self.confirm_button = QPushButton("Confirmar Identidad")
        self.confirm_button.setEnabled(False)
        self.confirm_button.clicked.connect(self.accept)
        main_layout.addWidget(self.confirm_button, alignment=Qt.AlignCenter)

        # Configuración de la cámara y detección facial
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            QMessageBox.critical(self, "Error", "No se pudo acceder a la cámara.")
            self.reject()
            return

        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(50)  # Actualizar cada 50ms

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Convertir a escala de grises para detección
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # Dibujar rectángulo alrededor de los rostros
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Habilitar botón si se detecta al menos un rostro
            self.confirm_button.setEnabled(len(faces) > 0)

            # Convertir frame a formato QPixmap
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            q_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image).scaled(self.video_label.size(), Qt.KeepAspectRatio)
            self.video_label.setPixmap(pixmap)

    def closeEvent(self, event):
        self.cap.release()
        self.timer.stop()
        event.accept()

class BankTransactionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Banco Estelar - Transacciones")
        self.setWindowIcon(QIcon("bank-icon.jpg"))
        self.setGeometry(100, 100, 600, 400)
        self.setMinimumSize(400, 300)

        # Widget central y layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Estilo general con fondo degradado
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #e6f0fa, stop:1 #ffffff);
            }
            QLabel {
                font-family: 'Roboto', 'Arial';
                font-size: 16px;
                color: #2c3e50;
                background-color: #f8fafc;
                border: 1px solid #dfe6e9;
                border-radius: 4px;
                padding: 8px;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
            }
            QLabel#titleLabel {
                font-size: 22px;
                font-weight: bold;
                color: #2c3e50;
                background-color: transparent;
                border: none;
                box-shadow: none;
                padding: 0;
            }
            QComboBox, QLineEdit {
                padding: 8px;
                font-size: 14px;
                border: 1px solid #3498db;
                border-radius: 5px;
                background-color: #ffffff;
            }
            QComboBox:hover, QLineEdit:hover {
                border: 1px solid #2980b9;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 16px;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1f618d;
            }
        """)

        # Título
        title_label = QLabel("Realizar Transacción")
        title_label.setObjectName("titleLabel")  # Identificador para estilo específico
        title_label.setFont(QFont("Roboto", 22, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Selección de tipo de transacción
        transaction_layout = QHBoxLayout()
        transaction_label = QLabel("Tipo de transacción:")
        transaction_label.setFixedWidth(150)
        self.transaction_combo = QComboBox()
        self.transaction_combo.addItems(["Depósito", "Retiro"])
        self.transaction_combo.setFixedWidth(200)
        transaction_layout.addWidget(transaction_label)
        transaction_layout.addWidget(self.transaction_combo)
        transaction_layout.addStretch()
        main_layout.addLayout(transaction_layout)

        # Monto
        amount_layout = QHBoxLayout()
        amount_label = QLabel("Monto:")
        amount_label.setFixedWidth(150)
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Ej. 100.00")
        self.amount_input.setFixedWidth(200)
        amount_layout.addWidget(amount_label)
        amount_layout.addWidget(self.amount_input)
        amount_layout.addStretch()
        main_layout.addLayout(amount_layout)

        # Cuenta destino
        account_layout = QHBoxLayout()
        account_label = QLabel("Cuenta destino:")
        account_label.setFixedWidth(150)
        self.account_combo = QComboBox()
        self.account_combo.addItems(["Cuenta Ahorros - ****1234", "Cuenta Corriente - ****5678"])
        self.account_combo.setFixedWidth(200)
        account_layout.addWidget(account_label)
        account_layout.addWidget(self.account_combo)
        account_layout.addStretch()
        main_layout.addLayout(account_layout)

        # Botón de realizar transacción
        self.submit_button = QPushButton("Confirmar Transacción")
        self.submit_button.clicked.connect(self.process_transaction)
        main_layout.addWidget(self.submit_button, alignment=Qt.AlignCenter)

        # Espaciador para diseño responsivo
        main_layout.addStretch()

    def process_transaction(self):
        transaction_type = self.transaction_combo.currentText()
        amount = self.amount_input.text()
        account = self.account_combo.currentText()

        # Validación básica
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("El monto debe ser mayor a 0")
        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor, ingrese un monto válido.")
            return

        # Mensaje de confirmación
        message = f"Transacción realizada:\n\nTipo: {transaction_type}\nMonto: ${amount:.2f}\nCuenta: {account}"
        QMessageBox.information(self, "Éxito", message)
        self.amount_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Mostrar ventana de autenticación primero
    auth_window = FaceAuthWindow()
    if auth_window.exec_() == QDialog.Accepted:
        # Si la autenticación es exitosa, mostrar ventana de transacciones
        window = BankTransactionWindow()
        window.show()
    sys.exit(app.exec_())