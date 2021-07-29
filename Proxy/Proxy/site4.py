from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import fake_useragent
from bs4 import BeautifulSoup
from create_db import add_to_db
# proxylist = []
# portlist = []

user_agent = fake_useragent.UserAgent().random
url = 'http://free-proxy.cz/ru/'
driver = webdriver.Chrome()
# options
options = webdriver.ChromeOptions()
# adding user-agent
options.add_argument(f'user-agent={user_agent}')
driver.maximize_window()

def help_parse(url):
    try:
        driver.get(url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        pageslist = list(soup.find('div', class_='paginator'))
        index = 0
        for i in range(len(pageslist)):
            if pageslist[i].has_attr('class') and pageslist[i]['class'][0] =='current':
                index = i
                break
        rows = soup.find_all('tbody')[1].find_all('tr')
        for row in rows:
            items = row.find_all('td')
            if len(items) < 11:# В таблице есть рекламные вставки - этим условием их избегаем
                continue
            # proxylist.append(items[0].text)
            # portlist.append(items[1].text)
            add_to_db(items[0].text, items[1].text)
        #print(proxylist)
        #print(portlist)
        if index == len(pageslist) - 2:
            return

        new_page_num = index + 1
        href = pageslist[new_page_num].get('href')
        url = 'http://free-proxy.cz' + href

        button = driver.find_element_by_link_text('другой »')
        # нажатие стрелки мышкой
        ActionChains(driver).move_to_element(button).click(button).perform()

        help_parse(url)
    except TypeError as e:
        print('Meeting with CAPTCHA:',e)
def parse4():
    help_parse(url)
    # print(proxylist)
    # print(portlist)
    driver.close()
    driver.quit()
