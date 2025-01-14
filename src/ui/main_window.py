from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget,
    QLabel, QPushButton
)
from PySide6.QtGui import QFont
from src.ui.dialogs.settings_dialog import SettingsDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set window properties
        self.setWindowTitle("Delivery Management System")
        self.resize(800, 600)
        
        # Create central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        # Add a welcome label
        welcome_label = QLabel("Welcome to Delivery Management System")
        welcome_label.setFont(QFont("Arial", 16))
        layout.addWidget(welcome_label)
        
        # Add a test button
        test_button = QPushButton("Click Me!")
        test_button.clicked.connect(self.on_button_click)
        layout.addWidget(test_button)
        
        # Add a settings button
        settings_button = QPushButton("Settings")
        settings_button.clicked.connect(self.open_settings)
        layout.addWidget(settings_button)
        
        # Set the central widget
        self.setCentralWidget(central_widget)
    
    def open_settings(self):
        # Create and show the settings dialog
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec()
    
    def on_button_click(self):
        print("Button was clicked!")
