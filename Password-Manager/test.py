from db import get_session
from models import User, Services, StoredPassword, AccessLog
from password_generator import generate_password

def create_user(username, plain_password):
    session = next(get_session())  # Get the session
    new_user = User(username=username)
    new_user.set_password(plain_password)
    session.add(new_user)
    session.commit()

def create_service(service_name, url=None):
    session = next(get_session())
    new_service = Services(service_name=service_name, url=url)
    session.add(new_service)
    session.commit()

def create_password(service_id, username, email, password, user_id, comments):
    session = next(get_session())
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
    create_service('Epic Games', 'https://store.epicgames.com/en-US/')
    create_user('test_user', 'plain_password')
    encrypted_password = generate_password(16)
    create_password(1, 'test_user', 'user@example.com', encrypted_password, 1, 'Security question: What is your pet\'s name? Answer: Fluffy')
    print("User and password created successfully!")
