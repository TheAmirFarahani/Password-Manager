from crud import read_all_master_users, read_all_user_services, read_all_user_passwords_for_service
from rich.console import Console
from rich.table import Table


def print_all_master_users():
    """
    Prints all the master users in a table, if they exist it returns true but if there are no master users returns false
    """
    all_users = read_all_master_users()
    if all_users:
        console = Console()
        table = Table(title = "Users")
        table.add_column("ID")
        table.add_column("Users")
        for index, user in enumerate(all_users):
            table.add_row(str(index+1), user.username)
        console.print(table)
        return True
    else:
        return False

def print_all_user_services(user_id):
    """
    Prints all the user services in a table, if they exist it returns true but if there are no master users returns false
    """
    all_services = read_all_user_services(user_id)
    if all_services:
        console = Console()
        table = Table(title = "Services")
        table.add_column("ID")
        table.add_column("Service")
        table.add_column("URL")
        for index, service in enumerate(all_services):
            table.add_row(str(index+1), service["Service Name"], service["URL"])
        console.print(table)
        return True
    else:
        return False
    

def print_all_user_passwords_for_service(user_id, service_id):
    """
    Prints all the passwords for a service in a table, if they exist it returns true but if there are no master users returns false
    """
    all_passwords = read_all_user_passwords_for_service(user_id, service_id)
    if all_passwords:
        console = Console()
        table = Table(title = "Passwords")
        table.add_column("ID")
        table.add_column("Password")
        table.add_column("Username")
        table.add_column("Email")
        table.add_column("Comments")
        for index, password in enumerate(all_passwords):
            table.add_row(str(index+1), password["Password"], password["Username"], password["Email"], password["Comments"])
        console.print(table)
        return True
    else:
        return False