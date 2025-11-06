import database

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"

print("Welcome to the Wallet Management App!\n")

def start():
    uid = 0
    print(f"{YELLOW}1. Login\n2. Signup{RESET}\n")
    inp = input("Enter a number: ")
    username = input("\nEnter Username: ")
    password = input("Enter Password: ")
    
    match inp:
        case '1':
            uid = database.login(username, password)
            if(uid == -1): start()
            
            return uid
        case '2':
            uid = database.signup(username, password)
            
            if(uid == -1): start()
            return uid
        case _:
            print(f"{RED}Please Enter a valid input!{RESET}")
            start()