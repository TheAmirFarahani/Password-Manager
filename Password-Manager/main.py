import crud
import cli
import rich
import password_generator

run = True
while run:
    cli.print_all_master_users()
    user_index = input("""\nPlease input your user ID: """)
    user_id_map = crud.link_user_id_to_index()
    try:
        user_index = int(user_index)
    except:
        print("\nID is needs to be an integer")
        continue
    if user_index in user_id_map:
        user_id = user_id_map[user_index]
        valid_user_id = True 
        pass
    else:        
        print("\nID is invalid")
        continue
    while valid_user_id:
        cli.print_all_user_services(user_id)
        service_index = input("""\nPlease input your service ID: """)
        service_id_map = crud.link_service_id_to_index(user_id)
        try:
            service_index = int(service_index)
        except:
            print("\nID is needs to be an integer")
            continue
        if service_index in service_id_map:
            service_id = service_id_map[service_index]
            valid_service_id = True 
            pass
        else:        
            print("\nID is invalid")
            continue

        while valid_service_id:
            cli.print_all_user_passwords_for_service(user_id, service_id)
            password_index = input("""\nPlease input your password ID: """)
            password_id_map = crud.link_service_id_to_index(user_id)
            try:
                password_index = int(password_index)
            except:
                print("\nID is needs to be an integer")
                continue
            if password_index in password_id_map:
                password_id = password_id_map[password_index]
                valid_password_id = True 
                pass
            else:        
                print("\nID is invalid")
                continue