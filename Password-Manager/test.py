from db import get_session
from models import User, Services, StoredPassword
from password_generator import generate_password
from crud import create_user, create_password , create_service
 #   if __name__ == "__main__":
 #       create_service('Epic Games', 'https://store.epicgames.com/en-US/')
  #      create_user('test_user', 'plain_password')
 #       encrypted_password = generate_password(16)
#        create_password(1, 'test_user', 'user@example.com', encrypted_password, 1, 'Security question: What is your pet\'s name? Answer: Fluffy')
 #       print("User and password created successfully!")
with get_session() as session:
    """Return all passwords objects of user for a service, if there are no passwords saved it returns false"""
    password = session.query(StoredPassword).first()
for kir in password:
    print(kir)