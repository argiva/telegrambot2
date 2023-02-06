import json
import requests


def get_city_id(city: str) -> dict:
    """
    Функция парсинга данных для получения ID локации, в которой будет вестись поиски отелей
    :param city: заданный пользвоателем город для поиска
    :return: словарь с уточнением мест по локации
    """
    city_list = dict()
    url = 'https://hotels4.p.rapidapi.com/locations/v3/search'
    querystring = {'q': city, 'locale': 'ru_RU'}
    headers = {
        'X-RapidAPI-Key': '74d6a078f8msh9cb0ed5a9e798ebp177cd9jsn2910c7c1d0f8',
        'X-RapidAPI-Host': 'hotels4.p.rapidapi.com'
    }
    response = requests.request('GET', url, headers=headers, params=querystring)
    js = json.loads(response.text)

    for key in js['sr']:
        if key['type'] != 'HOTEL':
            city_list[key['gaiaId']] = key['regionNames']['shortName']
    return city_list


def get_hotel_detail(hotel_id: int, cache: dict, price: float) -> dict:
    """
    Функция парсинга для получения деталей отелей

    :param hotel_id: ID отеля
    :param cache: данные выборки пользователя
    :param price: цена отеля
    :return: словарь с деталями отеля
    """
    url = "https://hotels4.p.rapidapi.com/properties/v2/detail"
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "propertyId": hotel_id
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "2c72d2b8ccmsh03dfc0b34d679c0p1279c9jsn3e72599e48af",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    js = json.loads(response.text)

    result = {'text': f"Отель: {js['data']['propertyInfo']['summary']['name']}\n\n"
                      f"Информация: {js['data']['propertyInfo']['summary']['tagline']}\n"
                      f"Адрес отеля:\n\t{js['data']['propertyInfo']['summary']['location']['address']['addressLine']}\n"
                      f"\t{js['data']['propertyInfo']['summary']['location']['address']['city']}\n"
                      f"\t{js['data']['propertyInfo']['summary']['location']['address']['province']}\n\n"
                      f"Координаты:\n\t{js['data']['propertyInfo']['summary']['location']['coordinates']['latitude']}\n"
                      f"\t{js['data']['propertyInfo']['summary']['location']['coordinates']['longitude']}\n\n"
                      f"Цена за ночь: {price}\n",
              'photo': [photo['image']['url'] for num, photo in
                        zip(cache['photo'], js['data']['propertyInfo']['propertyGallery']['images'])]}

    return result


def get_hotel_id(cache:dict) -> list:
    """
    Функция парсинга получения ID отеля

    :param cache: данные выборки пользователя
    :return: список отелей для отправки пользователю
    """

    url = "https://hotels4.p.rapidapi.com/properties/v2/list"
    hotels_data = list()
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "destination": {"regionId": cache['city_id']},
        "checkInDate": {
            "day": cache['check_in'].day,
            "month": cache['check_in'].month,
            "year": cache['check_in'].year
        },
        "checkOutDate": {
            "day": cache['check_out'].day,
            "month": cache['check_out'].month,
            "year": cache['check_out'].year
        },
        "rooms": [
            {
                "adults": 2
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": cache['resultsSize'],
        "sort": "PRICE"
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "2c72d2b8ccmsh03dfc0b34d679c0p1279c9jsn3e72599e48af",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    for hotel_id in json.loads(response.text)['data']['propertySearch']['properties']:
        hotels_data.append(
            get_hotel_detail(hotel_id=hotel_id['id'], cache=cache, price=hotel_id['price']['lead']['formatted']))
    return hotels_data
