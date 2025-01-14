from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QTabWidget,
    QWidget, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QLabel,
    QLineEdit, QCheckBox, QMessageBox,
    QDialogButtonBox
)
from PySide6.QtCore import Qt
from src.services.settings_manager import SettingsManager

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings_manager = SettingsManager()
        self.setWindowTitle("System Settings")
        self.resize(600, 400)
        
        # Main layout
        layout = QVBoxLayout()
        
        # Create tabs
        tabs = QTabWidget()
        
        # Vehicles Tab
        vehicles_tab = VehiclesTab(self.settings_manager)
        tabs.addTab(vehicles_tab, "Vehicles")
        
        # Drivers Tab
        drivers_tab = DriversTab(self.settings_manager)
        tabs.addTab(drivers_tab, "Drivers")
        
        # Parcel Types Tab
        parcel_types_tab = ParcelTypeTab(self.settings_manager)
        tabs.addTab(parcel_types_tab, "Parcel Types")
        
        layout.addWidget(tabs)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)

class EditDialog(QDialog):
    def __init__(self, title, fields, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.fields = {}
        
        layout = QVBoxLayout()
        
        # Create input fields
        for label, field_type, initial_value in fields:
            row_layout = QHBoxLayout()
            row_layout.addWidget(QLabel(label))
            
            if field_type == bool:
                field = QCheckBox()
                field.setChecked(initial_value)
            else:
                field = QLineEdit(str(initial_value) if initial_value is not None else "")
            
            row_layout.addWidget(field)
            layout.addLayout(row_layout)
            self.fields[label] = field
        
        # Dialog buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def get_values(self):
        return {label: field.isChecked() if isinstance(field, QCheckBox)
                else field.text() for label, field in self.fields.items()}

class VehiclesTab(QWidget):
    def __init__(self, settings_manager):
        super().__init__()
        self.settings_manager = settings_manager
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Add vehicle section
        add_layout = QHBoxLayout()
        add_layout.addWidget(QLabel("Registration:"))
        self.reg_input = QLineEdit()
        add_layout.addWidget(self.reg_input)
        
        add_btn = QPushButton("Add Vehicle")
        add_btn.clicked.connect(self.add_vehicle)
        add_layout.addWidget(add_btn)
        
        layout.addLayout(add_layout)
        
        # Vehicles table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Registration", "Active", "Edit", "Delete"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.load_vehicles()
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def load_vehicles(self):
        vehicles = self.settings_manager.get_active_vehicles()
        self.table.setRowCount(len(vehicles))
        
        for row, vehicle in enumerate(vehicles):
            # Registration (non-editable)
            reg_item = QTableWidgetItem(vehicle.registration)
            reg_item.setFlags(reg_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 0, reg_item)
            
            # Active status (non-editable)
            active_item = QTableWidgetItem("Yes" if vehicle.active else "No")
            active_item.setFlags(active_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 1, active_item)
            
            # Edit button
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda _, v=vehicle: self.edit_vehicle(v))
            self.table.setCellWidget(row, 2, edit_btn)
            
            # Delete button
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda _, v=vehicle: self.delete_vehicle(v))
            self.table.setCellWidget(row, 3, delete_btn)
        
        # Resize columns to content
        self.table.resizeColumnsToContents()
    
    def add_vehicle(self):
        registration = self.reg_input.text().strip()
        
        if not registration:
            QMessageBox.warning(self, "Error", "Registration cannot be empty")
            return
        
        try:
            self.settings_manager.add_vehicle(registration)
            self.load_vehicles()
            self.reg_input.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def edit_vehicle(self, vehicle):
        # Create edit dialog
        edit_dialog = EditDialog(
            "Edit Vehicle",
            [
                ("Registration", str, vehicle.registration),
                ("Active", bool, vehicle.active)
            ],
            self
        )
        
        if edit_dialog.exec():
            try:
                values = edit_dialog.get_values()
                self.settings_manager.update_vehicle(
                    vehicle.id,
                    registration=values["Registration"],
                    active=values["Active"]
                )
                self.load_vehicles()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
    
    def delete_vehicle(self, vehicle):
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete vehicle {vehicle.registration}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.settings_manager.delete_vehicle(vehicle.id)
                self.load_vehicles()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

class DriversTab(QWidget):
    def __init__(self, settings_manager):
        super().__init__()
        self.settings_manager = settings_manager
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Add driver section
        add_layout = QHBoxLayout()
        add_layout.addWidget(QLabel("Name:"))
        self.name_input = QLineEdit()
        add_layout.addWidget(self.name_input)
        
        add_btn = QPushButton("Add Driver")
        add_btn.clicked.connect(self.add_driver)
        add_layout.addWidget(add_btn)
        
        layout.addLayout(add_layout)
        
        # Drivers table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Name", "Active", "Edit", "Delete"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.load_drivers()
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def load_drivers(self):
        drivers = self.settings_manager.get_active_drivers()
        self.table.setRowCount(len(drivers))
        
        for row, driver in enumerate(drivers):
            # Name (non-editable)
            name_item = QTableWidgetItem(driver.name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 0, name_item)
            
            # Active status (non-editable)
            active_item = QTableWidgetItem("Yes" if driver.active else "No")
            active_item.setFlags(active_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 1, active_item)
            
            # Edit button
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda _, d=driver: self.edit_driver(d))
            self.table.setCellWidget(row, 2, edit_btn)
            
            # Delete button
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda _, d=driver: self.delete_driver(d))
            self.table.setCellWidget(row, 3, delete_btn)
        
        # Resize columns to content
        self.table.resizeColumnsToContents()
    
    def add_driver(self):
        name = self.name_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Error", "Name cannot be empty")
            return
        
        try:
            self.settings_manager.add_driver(name)
            self.load_drivers()
            self.name_input.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def edit_driver(self, driver):
        # Create edit dialog
        edit_dialog = EditDialog(
            "Edit Driver",
            [
                ("Name", str, driver.name),
                ("Active", bool, driver.active)
            ],
            self
        )
        
        if edit_dialog.exec():
            try:
                values = edit_dialog.get_values()
                self.settings_manager.update_driver(
                    driver.id,
                    name=values["Name"],
                    active=values["Active"]
                )
                self.load_drivers()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
    
    def delete_driver(self, driver):
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete driver {driver.name}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.settings_manager.delete_driver(driver.id)
                self.load_drivers()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

class ParcelTypeTab(QWidget):
    def __init__(self, settings_manager):
        super().__init__()
        self.settings_manager = settings_manager
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Add parcel type section
        add_layout = QHBoxLayout()
        
        # Code input
        add_layout.addWidget(QLabel("Code:"))
        self.code_input = QLineEdit()
        add_layout.addWidget(self.code_input)
        
        # Description input
        add_layout.addWidget(QLabel("Description:"))
        self.desc_input = QLineEdit()
        add_layout.addWidget(self.desc_input)
        
        # Signature required checkbox
        self.sig_required = QCheckBox("Requires Signature")
        add_layout.addWidget(self.sig_required)
        
        # Add button
        add_btn = QPushButton("Add Parcel Type")
        add_btn.clicked.connect(self.add_parcel_type)
        add_layout.addWidget(add_btn)
        
        layout.addLayout(add_layout)
        
        # Parcel types table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Code", "Description", "Signature Required", "Edit", "Delete"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.load_parcel_types()
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def load_parcel_types(self):
        parcel_types = self.settings_manager.get_parcel_types()
        self.table.setRowCount(len(parcel_types))
        
        for row, parcel_type in enumerate(parcel_types):
            # Code (non-editable)
            code_item = QTableWidgetItem(parcel_type.code)
            code_item.setFlags(code_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 0, code_item)
            
            # Description (non-editable)
            desc_item = QTableWidgetItem(parcel_type.description)
            desc_item.setFlags(desc_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 1, desc_item)
            
            # Signature Required (non-editable)
            sig_item = QTableWidgetItem("Yes" if parcel_type.requires_signature else "No")
            sig_item.setFlags(sig_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 2, sig_item)
            
            # Edit button
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda _, pt=parcel_type: self.edit_parcel_type(pt))
            self.table.setCellWidget(row, 3, edit_btn)
            
            # Delete button
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda _, pt=parcel_type: self.delete_parcel_type(pt))
            self.table.setCellWidget(row, 4, delete_btn)
        
        # Resize columns to content
        self.table.resizeColumnsToContents()
    
    def add_parcel_type(self):
        code = self.code_input.text().strip()
        description = self.desc_input.text().strip()
        
        if not code or not description:
            QMessageBox.warning(self, "Error", "Code and Description are required")
            return
        
        try:
            self.settings_manager.add_parcel_type(
                code,
                description,
                self.sig_required.isChecked()
            )
            self.load_parcel_types()
            self.code_input.clear()
            self.desc_input.clear()
            self.sig_required.setChecked(False)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def edit_parcel_type(self, parcel_type
