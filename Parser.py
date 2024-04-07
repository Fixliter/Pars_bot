import requests
from bs4 import BeautifulSoup
import lxml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import undetected_chromedriver as undetected
from selenium.webdriver.common.by import By
import logging
from webdriver_manager.core.logger import set_logger
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime

# Ручная настройка логгера без конфигуратора:
# logger = logging.getLogger("parser_logger")
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())
# logger.addHandler(logging.FileHandler("parser.log"))
# set_logger(logger)

logger = logging.getLogger(__name__)


class Parsa:
    list_of_sites = ["https://www.exapro.com/product-search/?text=Cryovac",
                     "https://www.sigmaequipment.com/equipment/search/?searchphrase=cryovac",
                     'https://www.resale.info/resalesearch.php?such=1&beginn=5&lang=en&searchgroupid=0&order=13&seite=1&search=cryovac']

    def try_to_categorize(self):
        pass

    @staticmethod
    def simple_req():
        http_current = "https://www.exapro.com/"
        result = requests.get(http_current)
        html = result.text

        soup = BeautifulSoup(html, "lxml")
        spans = soup.find_all("span")
        print(spans)

    @staticmethod
    def selenium_in_use():
        # Подключим движок браузера, если его нет, то сначала установим
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        driver.get("https://www.exapro.com/")
        time.sleep(200)
        spans = driver.find_elements(By.TAG_NAME, "placeholder='Search by manufacturer or model'")
        print(len(spans))
        print(spans[0].text)

    @staticmethod
    def parser_exapro():
        logger.debug('Лог DEBUG')
        logger.info('Лог INFO')
        logger.warning('Лог WARNING')
        logger.error('Лог ERROR')
        logger.critical('Лог CRITICAL')

        print("start parsing")
        # Подключим движок браузера, если его нет, то сначала установим
        # service = Service(ChromeDriverManager().install())
        # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))  # тоже рабочий вариант, сайт не защищается от ботов
        driver = undetected.Chrome(service=ChromeService(ChromeDriverManager().install()))
        count = 1
        products = 1

        http = "https://www.exapro.com/product-search/?text=Cryovac"
        driver.get(http)
        pages = driver.find_elements(By.CLASS_NAME, 'page-item')

        number_of_pages = len(pages)

        for i in range(1, number_of_pages + 1):
            http = "https://www.exapro.com/product-search/?text=Cryovac&area=None&order_by=-created&page=" + str(i)

            print(len(pages), "len pages")
            driver.get(http)
            print(http)

            # driver.get("https://mail.ru/")  # test

            machines = driver.find_elements(By.CLASS_NAME, 'ps-product__title__list')
            description = driver.find_elements(By.CLASS_NAME, 'ps-product__content.col-sm-9')
            machine_year = driver.find_elements(By.CLASS_NAME, 'ps-product__vendor')
            href = driver.find_elements(By.CLASS_NAME, 'mb-0')
            price = driver.find_elements(By.CLASS_NAME, 'price')
            picture = driver.find_elements(By.CLASS_NAME, 'ps-product__thumbnail.col-lg-3')
            country_name = driver.find_elements(By.CLASS_NAME, 'mt-4')

            print(len(machines))
            # for k in range(len(machines)):
            machines_cards = [(machines[k].text,
                               href[k].find_element(By.TAG_NAME, "a").get_attribute("href"),
                               machine_year[k].find_element(By.TAG_NAME, "span").get_attribute("Year"),
                               description[k].text,
                               price[k].text,
                               picture[k].find_element(By.TAG_NAME, "a").find_element(By.TAG_NAME, "img").get_attribute(
                                   "src"),
                               country_name[k].text,
                               country_name[k].find_element(By.TAG_NAME, "img").get_attribute("src")
                               ) for k in range(len(machines))]

            # print(machines[k].text)  # наименование машины
            # print(href[k].find_element(By.TAG_NAME, "a").get_attribute("href"))  # ссылка на страницу машины
            # print(machine_year[k].find_element(By.TAG_NAME, "span").get_attribute(
            #     "Year"))  # год производства оборудования
            # print(description[k].text)  # краткое описание оборудования
            # print(price[k].text)  # цена
            # print(picture[k].find_element(By.TAG_NAME, "a").find_element(By.TAG_NAME, "img").get_attribute(
            #     "src"))  # фото оборудования из каталога
            # print(country_name[k].text)  # название страны нахождения
            # print(country_name[k].find_element(By.TAG_NAME, "img").get_attribute("src"))  # флаг страны нахождения
            for machine in machines_cards:
                print(machine)
                new_http = machine[1]
                print(new_http)
                driver.get(new_http)
                time.sleep(1.1)

        spec = driver.find_elements(By.CLASS_NAME, 'ps-btn.ps-btn--sm')
        print(spec)
        for element in spec:
            print(element.get_attribute("href"))
            # element.click()
            print("клика сработала")

        time.sleep(20)
        # count += 1
        print("finish parsing")

    @staticmethod
    def parser_sigma():
        logger.debug('Лог DEBUG')
        logger.info('Лог INFO')
        logger.warning('Лог WARNING')
        logger.error('Лог ERROR')
        logger.critical('Лог CRITICAL')

        service = ChromeService(ChromeDriverManager().install())
        driver = undetected.Chrome(service=service)

        http = "https://www.sigmaequipment.com/equipment/search/?searchphrase=cryovac"
        driver.get(http)

        titles = driver.find_elements(By.CLASS_NAME, "flush-top")
        print(titles, len(titles))
        new_http = []
        for element in titles:
            print(element.text)
            a = element.find_elements(By.TAG_NAME, "a")

            for h in a:
                new_link = h.get_attribute("href")
                new_http.append(new_link)
                print(new_link)

        for link in new_http:
            driver.get(link)
            time.sleep(1)
            # print(element.find_element(By.TAG_NAME, "a").get_attribute("href"))

    @staticmethod
    def parser_resale():
        logger.debug('Лог DEBUG')
        logger.info('Лог INFO')
        logger.warning('Лог WARNING')
        logger.error('Лог ERROR')
        logger.critical('Лог CRITICAL')

        # Указываем параметры запроса в виде словаря

        params = {'key1': 'value1', 'key2': 'value2'}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br'
        }
        # response = requests.get(
        #     'https://www.resale.info/resalesearch.php?such=1&beginn=5&lang=en&searchgroupid=0&order=13&seite=1&search=cryovac',
        #     params=params)

        # на случай, если понадобится авторизация:
        # response_with_auth = requests.get(
        #     'https://www.resale.info/resalesearch.php?such=1&beginn=5&lang=en&searchgroupid=0&order=13&seite=1&search=cryovac',
        #     params=params, auth=HTTPBasicAuth('user', 'pass'))  # c авторизацией

        with requests.Session() as s:
            s.get(
                'https://www.resale.info/resalesearch.php?such=1&beginn=5&lang=en&searchgroupid=0&order=13&seite=1&search=cryovac')
        try:
            response = s.get(
                'https://www.resale.info/resalesearch.php?such=1&beginn=5&lang=en&searchgroupid=0&order=13&seite=1&search=cryovac',
                timeout=10, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            machine_cards = soup.find_all("div", class_="mobileansicht")
            # print(machine_cards)

            machines_dict = {}
            for card in machine_cards:
                machine_title = (
                    f"{card.find('div', class_=['col-md-9', 'maschinename']).find('div', class_=['row']).find('div', class_=['col-sm', 'col-mobile', 'pt-0', 'pt-md-2', 'pb-2']).find('a').text.strip()}")
                machine_desc = card.find("p", class_=["my-0", "pe-2", "pe-md-0"]).text.strip()
                machine_card_date = \
                    card.find("div", class_="row").find("div", class_=["col-lg-5"]).find("span").text.split(" ")[1]
                machine_url = f"https://www.resale.info/{card.find('div', class_=['col-md-9', 'maschinename']).find('div', class_=['row']).find('div', class_=['col-sm', 'col-mobile', 'pt-0', 'pt-md-2', 'pb-2']).find('a').get('href')}"
                machine_price = card.find("div", class_=["price"]).text.strip().split(" ")[3] if \
                    card.find("div", class_=["price"]).text.strip().split(" ")[1] == "VB" else \
                    f'{card.find("div", class_=["price"]).text.strip().split(" ")[0]} {card.find("div", class_=["price"]).text.strip().split(" ")[1]}' if \
                        card.find("div", class_=["price"]).text.strip().split(" ")[0].lower() == "request" else \
                        card.find("div", class_=["price"]).text.strip().split(" ")[1]
                machine_id = machine_url.split("/")[-1]
                machine_id = machine_id[3:]
                machine_image = card.find("div", class_=["carousel-item", "active"]).find("a").get("href")

                print(machine_title)
                print(machine_desc)
                print(machine_card_date)
                print(machine_price)
                # print(machine_item_number)
                print(machine_url)
                print(machine_id)
                print(machine_image)

                # Парсинг строки в формате дд.мм.гггг в объект datetime
                date_obj = datetime.strptime(machine_card_date, "%d.%m.%Y")

                # Преобразование объекта datetime в timestamp (количество секунд с начала эпохи)
                machine_date_timestamp = date_obj.timestamp()
                print(machine_date_timestamp)
                #

                machines_dict[machine_id] = {
                    "machine_date_timestamp": machine_date_timestamp,
                    "machine_title": machine_title,
                    "machine_url": machine_url,
                    "machine_desc": machine_desc,
                    "machine_price": machine_price,
                    "machine_image": machine_image,
                }

                print(machines_dict)

            with open("list_machines_resale.json", "w") as file:
                json.dump(machines_dict, file, indent=4, ensure_ascii=False)

            return machines_dict

        except requests.Timeout:
            print("Слишком долгое ожидание!")
        except requests.RequestException as e:
            print(f"Произошла ошибка: {e}")

    def check_new_updates(self):

        with open("list_machines_resale.json") as file:
            machines_dict = json.load(file)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br'}

        with requests.Session() as s:
            s.get(
                'https://www.resale.info/resalesearch.php?such=1&beginn=5&lang=en&searchgroupid=0&order=13&seite=1&search=cryovac')
        try:
            response = s.get(
                'https://www.resale.info/resalesearch.php?such=1&beginn=5&lang=en&searchgroupid=0&order=13&seite=1&search=cryovac',
                timeout=10, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            machine_cards = soup.find_all("div", class_="mobileansicht")

            new_updates_dict = {}
            for card in machine_cards:
                machine_url = f"https://www.resale.info/{card.find('div', class_=['col-md-9', 'maschinename']).find('div', class_=['row']).find('div', class_=['col-sm', 'col-mobile', 'pt-0', 'pt-md-2', 'pb-2']).find('a').get('href')}"
                machine_id = machine_url.split("/")[-1]
                machine_id = machine_id[3:]

                if machine_id in machines_dict:
                    continue
                else:
                    machine_title = (
                        f"{card.find('div', class_=['col-md-9', 'maschinename']).find('div', class_=['row']).find('div', class_=['col-sm', 'col-mobile', 'pt-0', 'pt-md-2', 'pb-2']).find('a').text.strip()}")
                    machine_desc = card.find("p", class_=["my-0", "pe-2", "pe-md-0"]).text.strip()
                    machine_card_date = \
                        card.find("div", class_="row").find("div", class_=["col-lg-5"]).find("span").text.split(" ")[1]
                    machine_price = card.find("div", class_=["price"]).text.strip().split(" ")[3] if \
                        card.find("div", class_=["price"]).text.strip().split(" ")[1] == "VB" else \
                        f'{card.find("div", class_=["price"]).text.strip().split(" ")[0]} {card.find("div", class_=["price"]).text.strip().split(" ")[1]}' if \
                            card.find("div", class_=["price"]).text.strip().split(" ")[0].lower() == "request" else \
                            card.find("div", class_=["price"]).text.strip().split(" ")[1]
                    machine_image = card.find("div", class_=["carousel-item", "active"]).find("a").get("href")

                    # Парсинг строки в формате дд.мм.гггг в объект datetime
                    date_obj = datetime.strptime(machine_card_date, "%d.%m.%Y")

                    # Преобразование объекта datetime в timestamp (количество секунд с начала эпохи)
                    machine_date_timestamp = date_obj.timestamp()

                    machines_dict[machine_id] = {
                        "machine_date_timestamp": machine_date_timestamp,
                        "machine_title": machine_title,
                        "machine_url": machine_url,
                        "machine_desc": machine_desc,
                        "machine_price": machine_price,
                        "machine_image": machine_image,
                    }

                    new_updates_dict[machine_id] = {
                        "machine_date_timestamp": machine_date_timestamp,
                        "machine_title": machine_title,
                        "machine_url": machine_url,
                        "machine_desc": machine_desc,
                        "machine_price": machine_price,
                        "machine_image": machine_image,
                    }

            with open("list_machines_resale.json", "w") as file:
                json.dump(machines_dict, file, indent=4, ensure_ascii=False)

            return new_updates_dict


        except requests.Timeout:
            print("Слишком долгое ожидание!")
        except requests.RequestException as e:
            print(f"Произошла ошибка: {e}")

    def main(self):
        self.parser_resale()
        # print(self.check_new_updates())

        # print(response.text)
        # print(response.status_code)
        # print(response.cookies)
        # print(response.encoding)
        # print(response.headers)
        # print(response.content)
        # print(response.elapsed)
        # print(response.history)
        # print(response.ok)
        # print(response.reason)
        # print(response.is_redirect)
        # print(response.url)
        # json_response = response.json()
        # print(json_response)


if __name__ == '__main__':
    attempting = Parsa()
    # attempting.simple_req()
    # attempting.selenium_in_use()`
    # attempting.parser_exapro()
    # attempting.parser_sigma()
    # attempting.parser_resale()
    attempting.main()
