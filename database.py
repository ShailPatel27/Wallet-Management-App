from psycopg2 import connect
from datetime import datetime
import os
from dotenv import load_dotenv

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"

load_dotenv()

conn = connect(
    host = "localhost",
    user = os.getenv("DB_USER") or "postgres",
    password = os.getenv("DB_PASSWORD") or "postgres",
    database = os.getenv("DB_NAME") or "wallet_management"
)

def remember(uid):
    choice = input("Stay logged in? (y) (n)\n")
    f = open("session.txt", "w")
    if(choice == 'y' or choice == 'Y'):
        f.write(str(uid))
    else:
        f.write("")
    f.close()
    os.system('cls' if os.name == 'nt' else 'clear')    #clear terminal

def signup(username, password):
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO users (username, password) values (%s, %s)", (username, password))
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
    else:
        conn.commit()
        print(f"{GREEN}Signup Successfull!{RESET}")
        
        uid = viewUid(username)
        createWallet(uid)
        
        remember(uid)
        
        return uid

def login(username, password):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT username, password from users where username=%s", (username,))
            row = cur.fetchone()
            
            if(row == "" or row == [] or row == None):
                print(f"\n{RED}User Not Found!{RESET}\n")
                return -1
        
    except Exception as e:
        print(f"{RED}User Not Found!{e}{RESET}\n")
        return -1
    else:
        
        if(row[0]==username):
            if(row[1]==password):
                print(f"{GREEN}Login Successfull!{RESET}")
                
                uid = viewUid(username)
                remember(uid)
                
                return uid       
            else:
                print(f"{RED}Incorrect Password!{RESET}")
                return -1
        else:
            print(f"{RED}Incorrect Username!{RESET}")
            return -1
        
def viewUid(username):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT user_id from users where username=%s", (username,))
            row = cur.fetchone()
            uid = row[0]
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
        return -1
    else:
        return uid

def createWallet(uid):
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO wallet (user_id) VALUES (%s) ON CONFLICT (user_id) DO NOTHING", (uid,))
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
    else:
        conn.commit()

def viewBalance(uid):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT balance from wallet where user_id=%s", (uid,))
            row = cur.fetchone()
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
    else:
        return row[0]

def updateBalance(uid, change):
    try:
        old_balance = viewBalance(uid)
        new_balance = old_balance + change
        
        with conn.cursor() as cur:
            cur.execute("Update wallet set balance=%s where user_id=%s", (new_balance, uid))
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
        return -1
    else:
        conn.commit()
        return new_balance
    
def insertItem(uid, name, price):
    bal = viewBalance(uid)
    
    if(price>bal):
        print(f"{RED}Insufficient Funds!{RESET}")
    else:
        try:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO purchases (user_id, product_name, product_price) values(%s, %s, %s)", (uid, name, price))
        except Exception as e:
            print(f"{RED}Error: {e}{RESET}")
        else:
            conn.commit()
            
            print(f"{GREEN}Item Purchased{RESET}")
            
            change = -price
            print(f"Balance: {GREEN}{updateBalance(uid, change)}{RESET}")

def purchaseHistory(uid):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT product_id, product_name, product_price, purchase_date from purchases where user_id=%s", (uid,))
            rows = cur.fetchall()
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
    else:
        if(rows == []):
            return f"{RED}No Items Purchased Yet{RESET}"
        else:
            itemsString = ""
            i=1
            itemsString+= f"{'ID':<5} | {'Name':<20} | {'Price($)':<12} | {'Date':<18} | {'Time':<12}\n"
            itemsString += "-"*80+"\n"
            for row in rows:
                pid = row[0]
                name = row[1]
                price = row[2]
                date_time: datetime = row[3]
                
                formattedDateTime = str(date_time.strftime("%d-%m-%Y %I:%M %p"))
                
                date = formattedDateTime.split(" ")[0]
                time = formattedDateTime.split(" ")[1]
                
                itemsString += f"{pid:<5} | {name:<20} | {price:<12} | {date:<18} | {time:<12}\n"
                i+=1
            
            return itemsString

def refund(uid, pid):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT product_price from purchases where user_id=%s AND product_id=%s",(uid,pid))
            row = cur.fetchone()
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
    else:
        conn.commit()
        
        try:
            with conn.cursor() as cur:
                cur.execute("Delete from purchases where product_id=%s", (pid,))
        except Exception as e:
            print(f"{RED}Error: {e}{RESET}")
        else:
            conn.commit()
    
            refund_amount = row[0]
            
            print(f"${refund_amount} were refunded to your wallet")
            print(f"Updated balance: {GREEN}{updateBalance(uid, refund_amount)}{RESET}")
            
            
def closeConn():
    conn.close()