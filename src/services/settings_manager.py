from src.database.database import get_db_session
from src.database.models import Vehicle, Driver, SystemSetting, ParcelType
from sqlalchemy.orm.exc import NoResultFound

class SettingsManager:
    def __init__(self):
        self.session = get_db_session()
    
    # Vehicle Methods
    def get_active_vehicles(self):
        """Retrieve active vehicles"""
        return self.session.query(Vehicle).filter_by(active=True).all()
    
    def add_vehicle(self, registration):
        """Add a new vehicle"""
        vehicle = Vehicle(
            registration=registration,
            active=True
        )
        self.session.add(vehicle)
        self.session.commit()
        return vehicle
    
    def update_vehicle(self, vehicle_id, registration=None, active=None):
        """Update an existing vehicle"""
        try:
            vehicle = self.session.query(Vehicle).filter_by(id=vehicle_id).one()
            
            if registration is not None:
                vehicle.registration = registration
            
            if active is not None:
                vehicle.active = active
            
            self.session.commit()
            return vehicle
        except NoResultFound:
            raise ValueError(f"Vehicle with id {vehicle_id} not found")
    
    def delete_vehicle(self, vehicle_id):
        """Delete a vehicle"""
        try:
            vehicle = self.session.query(Vehicle).filter_by(id=vehicle_id).one()
            self.session.delete(vehicle)
            self.session.commit()
        except NoResultFound:
            raise ValueError(f"Vehicle with id {vehicle_id} not found")
    
    # Driver Methods
    def get_active_drivers(self):
        """Retrieve active drivers"""
        return self.session.query(Driver).filter_by(active=True).all()
    
    def add_driver(self, name):
        """Add a new driver"""
        driver = Driver(
            name=name,
            active=True
        )
        self.session.add(driver)
        self.session.commit()
        return driver
    
    def update_driver(self, driver_id, name=None, active=None):
        """Update an existing driver"""
        try:
            driver = self.session.query(Driver).filter_by(id=driver_id).one()
            
            if name is not None:
                driver.name = name
            
            if active is not None:
                driver.active = active
            
            self.session.commit()
            return driver
        except NoResultFound:
            raise ValueError(f"Driver with id {driver_id} not found")
    
    def delete_driver(self, driver_id):
        """Delete a driver"""
        try:
            driver = self.session.query(Driver).filter_by(id=driver_id).one()
            self.session.delete(driver)
            self.session.commit()
        except NoResultFound:
            raise ValueError(f"Driver with id {driver_id} not found")
    
    # Parcel Type Methods
    def get_parcel_types(self):
        """Retrieve all parcel types"""
        return self.session.query(ParcelType).all()

    def add_parcel_type(self, code, description, requires_signature=False):
        """Add a new parcel type"""
        parcel_type = ParcelType(
            code=code,
            description=description,
            requires_signature=requires_signature
        )
        self.session.add(parcel_type)
        self.session.commit()
        return parcel_type

    def update_parcel_type(self, parcel_type_id, code=None, description=None, requires_signature=None):
        """Update an existing parcel type"""
        try:
            parcel_type = self.session.query(ParcelType).filter_by(id=parcel_type_id).one()
            
            if code is not None:
                parcel_type.code = code
            
            if description is not None:
                parcel_type.description = description
            
            if requires_signature is not None:
                parcel_type.requires_signature = requires_signature
            
            self.session.commit()
            return parcel_type
        except NoResultFound:
            raise ValueError(f"Parcel type with id {parcel_type_id} not found")

    def delete_parcel_type(self, parcel_type_id):
        """Delete a parcel type"""
        try:
            parcel_type = self.session.query(ParcelType).filter_by(id=parcel_type_id).one()
            self.session.delete(parcel_type)
            self.session.commit()
        except NoResultFound:
            raise ValueError(f"Parcel type with id {parcel_type_id} not found")
    
    # System Settings Methods
    def get_system_setting(self, key, default=None):
        """Retrieve a system setting"""
        setting = self.session.query(SystemSetting).filter_by(key=key).first()
        return setting.value if setting else default
    
    def set_system_setting(self, key, value, description=None):
        """Set a system setting"""
        setting = self.session.query(SystemSetting).filter_by(key=key).first()
        if setting:
            setting.value = value
        else:
            setting = SystemSetting(key=key, value=value, description=description)
            self.session.add(setting)
        self.session.commit()
        return setting
    
    def __del__(self):
        """Ensure session is closed when object is deleted"""
        self.session.close()
