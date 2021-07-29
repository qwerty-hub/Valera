from selenium import webdriver
import time
import fake_useragent
from bs4 import BeautifulSoup
from create_db import add_to_db
# proxylist = []
# portlist = []

user_agent = fake_useragent.UserAgent().random
url = 'https://free-proxy-list.net/'
driver = webdriver.Chrome()
# options
options = webdriver.ChromeOptions()
# adding user-agent
options.add_argument(f'user-agent={user_agent}')
driver.maximize_window()

def help_parse():
    table = driver.find_element_by_tag_name('tbody')
    buf = table.text.split('\n')
    for item in buf:
        temp = item.split(' ')
        add_to_db(temp[0],temp[1])
        # proxylist.append(temp[0])
        # portlist.append(temp[1])
    driver.find_element_by_link_text('Next').click()
    time.sleep(5)


def parse1():
    try:
        driver.get(url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source,'lxml')
        pages = soup.find('ul',class_ = 'pagination').find_all('li')
        max_page = int(pages[-3].text) # -3 потому что последние кнопки идут так : ... 14 15 Next Last
        for i in range(max_page):
            help_parse()
        # print(proxylist)
        # print(portlist)
    except Exception:
        print(Exception)
    finally:
        driver.close()
        driver.quit()
