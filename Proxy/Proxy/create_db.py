import sqlite3

def create_db():
    con = sqlite3.connect('ProxyDB.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS Proxy
        (id INTEGER PRIMARY KEY AUTOINCREMENT, IP VARCHAR,Port VARCHAR, Available VARCHAR DEFAULT('NO')''')
    con.commit()
    con.close()

def add_to_db(ip,port):
    with sqlite3.connect('ProxyDB.db') as con:
        cursor = con.cursor()
        try:
            cursor.execute("INSERT INTO Proxy (IP, Port) VALUES (?, ?)", (ip,port))
            con.commit()
            print("Data was added successfully")
        except Exception as e:
            print(e)

