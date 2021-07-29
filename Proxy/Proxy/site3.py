from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import fake_useragent
from bs4 import BeautifulSoup
from create_db import add_to_db
# proxylist = []
# portlist = []

user_agent = fake_useragent.UserAgent().random
url = 'https://hidemy.name/ru/proxy-list/'
driver = webdriver.Chrome()
# options
options = webdriver.ChromeOptions()
# adding user-agent
options.add_argument(f'user-agent={user_agent}')
driver.maximize_window()

def help_parse(url):
    driver.get(url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    pageslist = soup.find('div', class_='pagination').find_all('li')
    index = 0
    for i in range(len(pageslist)):
        if pageslist[i].has_attr('class') and \
           (pageslist[i]['class'][0] =='active' or pageslist[i]['class'][0] =='is-active'):
            index = i
            break
    rows = soup.find('tbody').find_all('tr')
    for row in rows:
        info = row.find_all('td')
        # proxylist.append(info[0].text)
        # portlist.append(info[1].text)
        add_to_db(info[0].text, info[1].text)
    # print(proxylist)
    # print(portlist)
    if index == len(pageslist)-1:
        return

    new_page_num = index + 1
    href = pageslist[new_page_num].find('a').get('href')
    new_url = 'https://hidemy.name' + href

    button = driver.find_element_by_css_selector(
        'body > div.wrap > div.services_proxylist.services > div > div.pagination > ul > li.next_array > a')
    # нажатие стрелки мышкой
    ActionChains(driver).move_to_element(button).click(button).perform()

    help_parse(new_url)

def parse3():
    help_parse(url)
    # print(proxylist)
    # print(portlist)
    driver.close()
    driver.quit()
