import requests
import time

ERROR_TEXT = ':( Здесь должна была быть картинка с '
API_CATS_URL = 'https://api.thecatapi.com/v1/images/search'
DOGS_API_URL = "https://random.dog/woof.json"
FOXES_API_URL = "https://randomfox.ca/floof/"
CAPYBARA_API_URL = "https://api.capy.lol/v1/capybara?json=true"

offset = -2
counter = 0
chat_id: int
cat_response: requests.Response
cat_link: str
updates: dict
timeout = 60


def cat_answer():
    cat_response = requests.get(API_CATS_URL)
    if cat_response.status_code == 200:
        cat_link = cat_response.json()[0]['url']

    else:
        cat_link = ERROR_TEXT + "котиком"

    return cat_link


def dog_answer():
    dog_response = requests.get(DOGS_API_URL)
    if dog_response.status_code == 200:
        dog_link = dog_response.json()['url']
    else:
        dog_link = ERROR_TEXT + "пёселем"

    return dog_link


def fox_answer():
    fox_response = requests.get(FOXES_API_URL)
    if fox_response.status_code == 200:
        fox_link = fox_response.json()['image']

    else:
        fox_link = ERROR_TEXT + "фоксом"

    return fox_link


def capybara_answer():
    capybara_response = requests.get(CAPYBARA_API_URL)
    if capybara_response.status_code == 200:
        capybara_link = capybara_response.json()['data']['url']

    else:
        capybara_link = ERROR_TEXT + "копибаркой забавной"

    return capybara_link