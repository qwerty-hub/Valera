import urllib.request
import sqlite3
import fake_useragent

user_agent = fake_useragent.UserAgent().random

def proxychecker():
    with sqlite3.connect('ProxyDB.db') as con:
        cursor = con.cursor()
        cursor.execute("SELECT IP,port FROM Proxy")
        data  = cursor.fetchall()
        for elem in data:
            if is_proxy_work(elem[0],elem[1]):
                cursor.execute("""Update Proxy set Available = 'YES' where IP = ?""",(elem[0],))
                con.commit()
            else:
                continue

def is_proxy_work(ip,port):
    address = 'http://' + ip + ':' + port
    for site in ['http://www.google.com', 'https://yandex.ru', 'https://www.youtube.com/']:
        proxy_support = urllib.request.ProxyHandler({'http': address})
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)
        req = urllib.request.Request(site)
        req.add_header("User-Agent", user_agent)
        try:
            urllib.request.urlopen(req, timeout=1)
        except:
            return False
    return True

proxychecker()