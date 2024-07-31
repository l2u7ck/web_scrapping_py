import re

import requests
import bs4
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By


def add_links_vacancy(page_link):

    path = ChromeDriverManager().install()
    browser_service = Service(executable_path=path)
    browser = Chrome(service=browser_service)
    check = True
    box = set()

    while check:

        browser.get(page_link)
        b = browser.find_element(By.CLASS_NAME, "vacancy-serp-content")

        links = b.find_elements(By.CLASS_NAME, "serp-item__title-link-wrapper")

        for item in links:
            box.add(item.find_element(By.CLASS_NAME, "bloko-link").get_attribute("href").split('?')[0])

        value = next_page(b)

        if value is None:
            check = False

        else:
            page_link = value

    return box


def next_page(b):

    buttons = b.find_elements(By.CLASS_NAME, "bloko-gap")

    if buttons:
        next_page_link = buttons[0].find_elements(By.LINK_TEXT, "дальше")

        if next_page_link:
            link = next_page_link[0].get_attribute('href')

            return link

        else:
            return None

    else:
        return None


def k():
    pass

if __name__ == '__main__':

    begin_link_py = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"
    begin_link_django_flask = ("https://spb.hh.ru/search/vacancy?"
                               "text=Django+AND+Flask&salary=&"
                               "ored_clusters=true&search_field=description&area=1&"
                               "area=2&hhtmFrom=vacancy_search_list&hhtmFromLabel=vacancy_search_line")
    res1 = add_links_vacancy(begin_link_py)
    res2 = add_links_vacancy(begin_link_django_flask)
    result = res1.intersection(res2)
    print(result)

