from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import bcrypt
import os

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    salt = Column(String, nullable=False)  # Store encryption key salt as a string

    passwords = relationship("StoredPassword", back_populates="user")

    def set_password(self, plain_password):
        """Hash the plain password and store it as a string."""
        # Hash the password (bcrypt returns bytes), then decode to store it as a string.
        hashed = bcrypt.hashpw(plain_password, bcrypt.gensalt())
        self.password_hash = hashed  # Store as a string in the database.

    def check_password(self, plain_password):
        """Check if the provided password matches the hash."""
        # Encode the plain password and the stored hash before checking.
        return bcrypt.checkpw(plain_password, self.password_hash)

class Services(Base):
    __tablename__= "services"
    user_id = Column(Integer, ForeignKey('users.id'))
    id = Column(Integer, primary_key=True, autoincrement=True)
    service_name = Column(String, nullable=False) 
    url = Column(String) # optional

class StoredPassword(Base):
    __tablename__ = 'stored_passwords'

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    username = Column(String, nullable=False)
    email = Column(String)  # Optional field
    password = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    access_count = Column(Integer, default=0)
    last_accessed = Column(TIMESTAMP)
    comments = Column(Text)  # Additional info

    user = relationship("User", back_populates="passwords")

class AccessLog(Base):
    __tablename__ = 'access_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    password_id = Column(Integer, ForeignKey('stored_passwords.id'), nullable=False)
    access_time = Column(TIMESTAMP, server_default=func.current_timestamp())
    user_id = Column(Integer, ForeignKey('users.id'))

    password = relationship("StoredPassword")
    user = relationship("User")
