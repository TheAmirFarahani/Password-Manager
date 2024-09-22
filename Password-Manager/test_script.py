from crud import create_user, create_service, create_password, read_all_master_users, read_all_user_services, read_all_user_passwords_for_service, update_service, update_password, update_master_user_username, update_master_password
from db import get_session
from models import User
import random

def test_crud_operations():
    # Create a new user
    username = "test_user"
    plain_password = "password123"
    create_user(username, plain_password)
    print("User created")

    # Retrieve and check if user exists
    with get_session() as session:
        user = session.query(User).filter(User.username == username).first()
        if user:
            user_id = user.id
            print(f"User ID: {user_id}")

            # Create a service
            create_service(user_id, "test_service", "http://testservice.com")
            print("Service created")

            # Retrieve and check if service exists
            services = read_all_user_services(user_id)
            print(f"Services: {services}")

            # Create a password for the service
            create_password(1, "test_username", "test_email@example.com", "test_password", user_id, "test comments")
            print("Password created")

            # Retrieve and check if password exists
            passwords = read_all_user_passwords_for_service(user_id, 1)
            print(f"Passwords: {passwords}")

            # Update service
            update_service(user_id, 1, service_name="updated_service", url="http://updatedservice.com")
            print("Service updated")

            # Check updated service
            updated_services = read_all_user_services(user_id)
            print(f"Updated Services: {updated_services}")

            # Update password
            update_password(user_id, 1, username="updated_username", password="updated_password", email="updated_email@example.com", comments="updated comments")
            print("Password updated")

            # Check updated password
            updated_passwords = read_all_user_passwords_for_service(user_id, 1)
            print(f"Updated Passwords: {updated_passwords}")

            # Update master user username
            update_master_user_username(user_id, new_username="new_test_user")
            print("Username updated")

            # Check updated user
            updated_user = session.query(User).filter(User.id == user_id).first()
            print(f"Updated User: {updated_user.username}")

            # Update master password
            update_master_password(user_id, "newpassword123")
            print("Master password updated")

            # Check if master password update works
            if user.check_password("newpassword123"):
                print("Master password update successful")
            else:
                print("Master password update failed")
        else:
            print("User not found")

if __name__ == "__main__":
    test_crud_operations()