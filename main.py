import json

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By


# Browser connection
def connect_browser():

    path = ChromeDriverManager().install()
    browser_service = Service(executable_path=path)
    return Chrome(service=browser_service)


# Getting links to job vacancies
def add_links_vacancy(browser, page_link):

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


# Page next
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


# Vacancy data collection
def get_data(browser, vacancies):

    job_list = list()

    for vacancy_link in vacancies:

        job_data = dict()

        browser.get(vacancy_link)

        job_data['vacancy_link'] = vacancy_link
        company = browser.find_element(By.CLASS_NAME, "vacancy-company-name")

        job_data['company_link'] = company.find_element(By.TAG_NAME, 'a').get_attribute('href')
        job_data['name'] = company.text

        address = (browser.find_element(By.CLASS_NAME, "vacancy-company-redesigned").
                   find_element(By.CLASS_NAME, "magritte-text___pbpft_3-0-12")).text
        job_data['city'] = address.split(',')[0]

        salary = (browser.find_element(By.CLASS_NAME, "vacancy-title").
                  find_element(By.CLASS_NAME, "magritte-text___pbpft_3-0-12"))
        job_data['salary'] = salary.text

        job_list.append(job_data)

    return job_list


# Adding in json
def add_json(data):

    with open('data.json', 'w', encoding="utf-8") as f:
        json.dump(data, f, sort_keys=True, indent=2, ensure_ascii=False)

    f.close()


if __name__ == '__main__':

    browser = connect_browser()

    begin_link_python = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"
    begin_link_django_flask = ("https://spb.hh.ru/search/vacancy?"
                               "text=Django+AND+Flask&salary=&"
                               "ored_clusters=true&search_field=description&area=1&"
                               "area=2&hhtmFrom=vacancy_search_list&hhtmFromLabel=vacancy_search_line")

    res1 = add_links_vacancy(browser, begin_link_python)
    res2 = add_links_vacancy(browser, begin_link_django_flask)
    result = res1.intersection(res2)

    # result = ["https://spb.hh.ru/vacancy/104415649"]
    job_list = get_data(browser, result)
    add_json(job_list)




