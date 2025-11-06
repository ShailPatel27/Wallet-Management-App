import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="internship",
    user="shail",
    password="shail"
)

with conn.cursor() as cur:
    cur.execute("TRUNCATE table users CASCADE")     #clear table users and all tables dependent on it
    conn.commit()

    print("All tables truncated")
    
    with open("C:\\Coding\\Python\\internship\\Wallet Management App\\session.txt", "w") as f:
        
        f.write("")
        
        print("All sessions cleared")

    
conn.close()