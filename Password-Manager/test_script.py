from crud import create_user, create_service, create_password, read_all_master_users, read_all_user_services, read_all_user_passwords_for_service, update_service, update_password, update_master_user_username, update_master_password
from db import get_session
from encryption import EncryptionManager

def test_crud_operations():
    # Create a user
    print("Creating user...")
    create_user("test_user", "password123")
    
    # Retrieve all users
    print("Reading all master users...")
    users = read_all_master_users()
    print("Users:", users)

    # Assume the user created above has an ID of 1 (You need to adjust based on your actual user ID)
    user_id = 1
    
    # Create a service
    print("Creating service...")
    create_service(user_id, "test_service", "http://testservice.com")

    # Retrieve all services for the user
    print("Reading all user services...")
    services = read_all_user_services(user_id)
    print("Services:", services)

    # Create a password
    print("Creating password...")
    create_password(service_id=1, username="test_user", email="user@test.com", password="securepassword", user_id=user_id, comments="Test comment")

    # Retrieve all passwords for the service
    print("Reading all user passwords for service...")
    passwords = read_all_user_passwords_for_service(user_id, service_id=1)
    print("Passwords:", passwords)
    
    # Update a service
    print("Updating service...")
    update_service(user_id, service_id=1, service_name="updated_service_name", url="http://updatedservice.com")

    # Retrieve updated services
    print("Reading updated services...")
    updated_services = read_all_user_services(user_id)
    print("Updated Services:", updated_services)

    # Update a password
    print("Updating password...")
    update_password(user_id, password_id=1, username="updated_user", password="newsecurepassword", email="updateduser@test.com", comments="Updated comment")

    # Retrieve updated passwords
    print("Reading updated passwords for service...")
    updated_passwords = read_all_user_passwords_for_service(user_id, service_id=1)
    print("Updated Passwords:", updated_passwords)

    # Update user username
    print("Updating master user username...")
    update_master_user_username(user_id, new_username="new_test_user")

    # Retrieve all users after update
    print("Reading all master users after username update...")
    updated_users = read_all_master_users()
    print("Updated Users:", updated_users)

    # Update master password
    print("Updating master user password...")
    update_master_password(user_id, new_password="newpassword123")

    # Test if master password update works by creating another service or password

if __name__ == "__main__":
    test_crud_operations()
