from db import get_session
from models import User, Services, StoredPassword
from password_generator import generate_password
from encryption import EncryptionManager

#master password and salt

def get_master_password_and_salt(user_id):
    """Returns the master password and salt for the given user ID."""
    with get_session() as session:
        master_user = session.query(User).filter(User.id == user_id).first()
        if master_user:
            master_password = input("Please input the master password: ")
            if master_user.check_password(master_password):
                return master_password, master_user.salt
    return None, None
        
def check_master_password(user_id):
    """returns the master password"""
    with get_session() as session:
        master_user = session.query(User).filter(User.id == user_id).first()
        if master_user:
            master_password = input("Please input the master password: ")
            return master_user.check_password(master_password)
        






#create section
def create_user(username, plain_password):
    """creates new master user"""
    with get_session() as session:  # Open the session using 'with' for context management
        new_user = User(username=username)
        new_user.set_password(plain_password)  # Password hashing with encoding
        new_user.salt = EncryptionManager.generate_salt()
        session.add(new_user)
        session.commit()

def create_service(user_id, service_name , url=None):
    """creates new service"""
    master_password, salt = get_master_password_and_salt(user_id)
    if master_password:
        with get_session() as session:  
            new_service = Services(
                user_id = user_id,
                service_name = EncryptionManager.encrypt(EncryptionManager.derive_key(master_password , salt),service_name.capitalize()), #Capitalizing the service 
                url= EncryptionManager.encrypt(EncryptionManager.derive_key(master_password , salt),url)) 
            session.add(new_service)
            session.commit()

def create_password(service_id, username, email, password, user_id, comments):
    """creates new password"""
    master_password, salt = get_master_password_and_salt(user_id)
    if master_password:
        with get_session() as session:
            new_password = StoredPassword(
                service_id=service_id,
                username=EncryptionManager.encrypt(EncryptionManager.derive_key(master_password , salt),username),
                email=EncryptionManager.encrypt(EncryptionManager.derive_key(master_password , salt),email),
                password=EncryptionManager.encrypt(EncryptionManager.derive_key(master_password , salt),password),
                user_id=user_id,
                comments=EncryptionManager.encrypt(EncryptionManager.derive_key(master_password , salt),comments)
            )
            session.add(new_password)
            session.commit()






#read section
def read_all_master_users():
    """Return all service objects in the services table"""
    with get_session() as session:
        all_users = session.query(User).all()
        if all_users:
            return all_users
        else:
            return None
        
def read_all_user_services(user_id):
    """Return all service objects in the services table"""
    master_password, salt = get_master_password_and_salt(user_id)
    with get_session() as session:
        all_services = session.query(Services).filter(Services.user_id==user_id)
        if all_services:
            service_list = []
            for service in all_services:
                service_dict = {}
                service_dict['Service Name'] = EncryptionManager.decrypt(EncryptionManager.derive_key(master_password , salt) , service.service_name)
                service_dict['URL'] = EncryptionManager.decrypt(EncryptionManager.derive_key(master_password , salt) , service.url)
                service_list.append(service_dict)
            return service_list
        else:
            return None

def read_all_user_passwords_for_service(user_id, service_id):
    master_password, salt = get_master_password_and_salt(user_id)
    if master_password:
        with get_session() as session:
            """Return all passwords objects of user for a service and returns it as dictionaries in a list, if there are no passwords saved it returns false"""
            all_passwords = session.query(StoredPassword).filter(StoredPassword.user_id==user_id).filter(StoredPassword.service_id==service_id) #Using two filters to filter for service and user
            if all_passwords:
                password_list = []
                for password in all_passwords:
                    password_dict = {}
                    password_dict['Password'] = EncryptionManager.decrypt(EncryptionManager.derive_key(master_password , salt) ,password.password )
                    password_dict['Username'] = EncryptionManager.decrypt(EncryptionManager.derive_key(master_password , salt) ,password.username )
                    password_dict['Email'] = EncryptionManager.decrypt(EncryptionManager.derive_key(master_password , salt) ,password.email )
                    password_dict['Comments'] = EncryptionManager.decrypt(EncryptionManager.derive_key(master_password , salt) ,password.comments )
                    password_list.append(password_dict)
                return password_list
            else:
                return False







#update section
def update_service(user_id, service_id, service_name = None, url = None):
    """Updates the parameters if the service exists"""
    master_password, salt = get_master_password_and_salt(user_id)
    if master_password:
        with get_session() as session:
            service = session.query(Services).filter(Services.id == service_id).first()
            if service:
                if service_name:
                    service.service_name = EncryptionManager.encrypt(EncryptionManager.derive_key(master_password , salt), service_name.capitalize()) #Capitalizing the service 
                if url:
                    service.url = EncryptionManager.encrypt(EncryptionManager.derive_key(master_password , salt), url)
                session.commit()

def update_password(user_id, password_id, username=None, password=None, email=None, comments=None):
    """Updates the parameters if the password exists"""
    master_password, salt = get_master_password_and_salt(user_id)
    if master_password:
        with get_session() as session:
            stored_password = session.query(StoredPassword).filter(StoredPassword.id == password_id).first()
            if stored_password:
                if password:
                    # Add symmetrical encryption
                    stored_password.password = EncryptionManager.encrypt(EncryptionManager.derive_key(master_password , salt),password)
                if username:
                    # Add symmetrical encryption
                    stored_password.username = EncryptionManager.encrypt(EncryptionManager.derive_key(master_password , salt), username)
                if email:
                    # Add symmetrical encryption
                    stored_password.email = EncryptionManager.encrypt(EncryptionManager.derive_key(master_password , salt), email)
                if comments:
                    # Add symmetrical encryption
                    stored_password.comments = EncryptionManager.encrypt(EncryptionManager.derive_key(master_password , salt), comments)
                # Commit the changes
                session.commit()
    
def update_master_user_username(user_id, new_username=None):
    """updates master username"""
    with get_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            if new_username:
                user.username = new_username
            session.commit()


def update_master_password(user_id, new_password):
    """Updates the master password and changes the encryption."""
    old_password, old_salt = get_master_password_and_salt(user_id)
    if old_password:
        with get_session() as session:
            # Retrieve the current user
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                print("User not found.")
                return
            
            # Generate new salt and hash the new password
            new_salt = EncryptionManager.generate_salt()
            user.set_password(new_password)  # Hash the new password
            user.salt = new_salt
            session.commit()

            # Derive keys from old and new passwords
            key_old = EncryptionManager.derive_key(old_password, old_salt)
            key_new = EncryptionManager.derive_key(new_password, new_salt)
            
            # Re-encrypt services
            services = session.query(Services).filter(Services.user_id == user_id).all()
            for service in services:
                decrypted_service_name = EncryptionManager.decrypt(key_old, service.service_name)
                decrypted_url = EncryptionManager.decrypt(key_old, service.url)
                service.service_name = EncryptionManager.encrypt(key_new, decrypted_service_name)
                service.url = EncryptionManager.encrypt(key_new, decrypted_url)
            
            # Re-encrypt passwords
            passwords = session.query(StoredPassword).filter(StoredPassword.user_id == user_id).all()
            for password in passwords:
                decrypted_username = EncryptionManager.decrypt(key_old, password.username)
                decrypted_email = EncryptionManager.decrypt(key_old, password.email)
                decrypted_password = EncryptionManager.decrypt(key_old, password.password)
                decrypted_comments = EncryptionManager.decrypt(key_old, password.comments)
                password.username = EncryptionManager.encrypt(key_new, decrypted_username)
                password.email = EncryptionManager.encrypt(key_new, decrypted_email)
                password.password = EncryptionManager.encrypt(key_new, decrypted_password)
                password.comments = EncryptionManager.encrypt(key_new, decrypted_comments)
            
            session.commit()