from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import bcrypt

# Base class for SQLAlchemy models
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)

    # Relationship to stored_passwords
    passwords = relationship("StoredPassword", back_populates="user")

    def set_password(self, plain_password):
        """Set password hash using bcrypt."""
        self.password_hash = bcrypt.hashpw(plain_password, bcrypt.gensalt())

    def check_password(self, plain_password):
        """Check if the provided password matches the hash."""
        return bcrypt.checkpw(plain_password.encode('utf-8'), self.password_hash.encode('utf-8'))
    

class Services(Base):
    __tablename__= "services"


    id = Column(Integer, primary_key=True, autoincrement=True)
    service_name = Column(String, nullable=False)
    url = Column(String) #optional
    


class StoredPassword(Base):
    __tablename__ = 'stored_passwords'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    service_id = Column(String, ForeignKey('services.id'))
    username = Column(String, nullable=False)
    email = Column(String)  # Optional field
    password = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    access_count = Column(Integer, default=0)
    last_accessed = Column(TIMESTAMP)
    comments = Column(Text)  # Additional info
    
    # Relationship to user
    user = relationship("User", back_populates="passwords")

class AccessLog(Base):
    __tablename__ = 'access_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    password_id = Column(Integer, ForeignKey('stored_passwords.id'), nullable=False)
    access_time = Column(TIMESTAMP, server_default=func.current_timestamp())
    user_id = Column(Integer, ForeignKey('users.id'))

    # Relationships
    password = relationship("StoredPassword")
    user = relationship("User")

# Database URL (Change this to your database configuration)
DATABASE_URL = "sqlite:///password_manager.db"

# Create an engine and bind it to the Base class
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)
session = Session()

# Example usage: Create a new user
def create_user(username, plain_password):
    new_user = User(username=username)
    new_user.set_password(plain_password)
    session.add(new_user)
    session.commit()
def create_service(service_name, url=None):
    new_service = Services(
        service_name = service_name,
        url = url
    )
    session.add(new_service)
    session.commit()

def create_password(service_id, username, email, password, user_id, comments):
    new_password = StoredPassword(
        service_id=service_id,
        username=username,
        email=email,
        password=password,
        user_id=user_id,
        comments=comments
    )
    session.add(new_password)
    session.commit()

if __name__ == "__main__":
    # Example usage
    create_service('Epic Games', "https://store.epicgames.com/en-US/" )
    create_user('test_user', 'plain_password')
    create_password(1, 'test_user', 'user@example.com', 'encrypted_password', 1, 'Security question: What is your pet\'s name? Answer: Fluffy')
