from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Patient(Base):
    __tablename__ = 'patients'
    
    patient_id = Column(Integer, primary_key=True)
    house_number = Column(String)
    street_name = Column(String)
    town = Column(String)
    exemption_category = Column(String)
    
    # Relationships
    deliveries = relationship("Delivery", back_populates="patient")

class Street(Base):
    __tablename__ = 'streets'
    
    id = Column(Integer, primary_key=True)
    road_name = Column(String, nullable=False)
    town = Column(String, nullable=False)
    route_order = Column(Integer)
    van_3_assignment = Column(Integer)
    van_4_assignment = Column(Integer)

class Delivery(Base):
    __tablename__ = 'deliveries'
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.patient_id'))
    delivery_date = Column(Date)
    van_number = Column(Integer)
    route_order = Column(Integer)
    notes = Column(Text)
    status = Column(String)
    parcel_type_id = Column(Integer, ForeignKey('parcel_types.id'))
    
    # Relationships
    patient = relationship("Patient", back_populates="deliveries")
    parcel_type = relationship("ParcelType")

class Vehicle(Base):
    __tablename__ = 'vehicles'
    
    id = Column(Integer, primary_key=True)
    registration = Column(String, nullable=False, unique=True)
    active = Column(Boolean, default=True)

class Driver(Base):
    __tablename__ = 'drivers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    active = Column(Boolean, default=True)

class ParcelType(Base):
    __tablename__ = 'parcel_types'
    
    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    requires_signature = Column(Boolean, default=False)

class SystemSetting(Base):
    __tablename__ = 'system_settings'
    
    key = Column(String, primary_key=True)
    value = Column(String)
    description = Column(Text)
