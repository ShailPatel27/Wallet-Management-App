import os
import database
import signupLogin

with open("session.txt") as f:
    uid = f.read()
    
    if(uid == ""):
        uid = signupLogin.start()
    else:
        uid = int(uid)
        
money = 0.0
item = {}

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"

while True:
    print(f"{YELLOW}\n1. Buy Item\n2. Add money to your wallet\n3. View Balance\n4. View purchase history\n5. Remove a Purchase/Refund\n6. Export purchase history to file\n7. Logout\n8. Exit\n{RESET}")
    inp = input("Enter a number: ")
    
    os.system('cls' if os.name == 'nt' else 'clear')    #clear terminal
                
    match inp:
        case '1':   #insert
            item_name: str = input("Item name: ")
            item_price: float = float(input("Item Price: "))

            database.insertItem(uid, item_name, item_price)
            
        case '2':   #add to wallet
            change = float(input("Enter extra money to be added: "))
            
            database.updateBalance(uid, change)
            
        case '3':    #display balance
            bal = database.viewBalance(uid)
            
            if(bal>0):                   
                print(f"Balance: {GREEN}{bal}{RESET}")
            else:
                print(f"Balance: {RED}{bal}{RESET}")
            
        case '4':   #purchase history
            print(database.purchaseHistory(uid))
            
        case '5':   #refund
            history = database.purchaseHistory(uid)
            print(history)
            if("No Items Purchased Yet" not in history):  
                pid = input("\nEnter the Product ID of the product to be refunded: ")
                    
                database.refund(uid, pid)
            
        case '6':
            history = database.purchaseHistory(uid)
            if("No Items Purchased Yet" not in history):    
                with open("history.txt", "w") as f:
                    f.write(f"Balance: {database.viewBalance(uid)}\n\n{database.purchaseHistory(uid)}")
                
        case '7':
            with open("session.txt", "w") as f:
                f.write("")
                uid = signupLogin.start()
        case '8':
            break
        
        case _:
            print(f"{RED}Please provide a valid input{RESET}")
        
database.closeConn()