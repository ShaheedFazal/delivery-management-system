import sys
from PySide6.QtWidgets import QApplication
from src.database.database import db_manager
from src.ui.main_window import MainWindow

def main():
    """Main application entry point"""
    # Initialize database
    db_manager  # This triggers table creation
    
    # Create application
    app = QApplication(sys.argv)
    
    # Create main window
    main_window = MainWindow()
    main_window.show()
    
    # Run application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
