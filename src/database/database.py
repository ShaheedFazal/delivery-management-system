from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from pathlib import Path
from .models import Base

class DatabaseManager:
    _instance = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        # Ensure data directory exists
        data_dir = Path.home() / ".delivery_system"
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # Create database path
        self.db_path = data_dir / "delivery_system.sqlite"
        
        # Create engine with SQLite
        self.engine = create_engine(
            f"sqlite:///{self.db_path}",
            connect_args={'check_same_thread': False},
            poolclass=StaticPool
        )
        
        # Create session factory
        self.SessionLocal = sessionmaker(
            autocommit=False, 
            autoflush=False, 
            bind=self.engine
        )
        
        # Create tables
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self) -> Session:
        """Get a new database session"""
        return self.SessionLocal()
    
    def drop_tables(self):
        """Drop all tables in the database"""
        Base.metadata.drop_all(bind=self.engine)

# Singleton instance
db_manager = DatabaseManager()

def get_db_session():
    """Convenience function to get a database session"""
    return db_manager.get_session()
