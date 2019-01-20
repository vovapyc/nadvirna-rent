# coding: utf-8

import requests
from bs4 import BeautifulSoup
from hashlib import md5
from time import sleep

PARSE_URL = 'http://www.vitryna.com.ua/nadvirna/section-287/'

open('houses.hash', 'a').close()  # створює файл для збереження хешів будинків


class House:
    def __init__(self, title, date):
        self.title = title
        self.date = date

        self.md5 = self.get_md5()

    def add_hash_to_file(self):
        """
        Записує хеш будинка до файлу з хешами
        :return:
        """
        with open('houses.hash', 'a+') as file:
            file.write(f'{self.md5}\n')

    def is_new(self):
        """
        Перевіряє чи будинок новий (перевірка чи його хеш є в файлі з хешами)
        :return:
        """
        with open('houses.hash', 'r') as file:
            for line in file:
                if self.md5 == line.strip():
                    return False
        return True

    def get_md5(self):
        return md5(f'{self.title}{self.date}'.encode('utf-8')).hexdigest()

    def __str__(self):
        return self.title


def get_all_houses():
    request = requests.get(PARSE_URL, headers={
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
    })
    soup = BeautifulSoup(request.text, 'html.parser')
    for house in reversed(list(soup.find_all('div', {'class': 'odd'}))):
        yield House(house.div.text, house.i.text.split(': ')[1])


def parse_houses(forever_alive=False):
    """
    Парсить будинки
    :param forever_alive: постійно запущений, незважаючи на помилки
    """
    if forever_alive:
        while True:
            try:
                for house in get_all_houses():
                    if house.is_new():
                        yield house
                        house.add_hash_to_file()
            except Exception as e:
                print(e)
            sleep(1)
    else:
        while True:
            for house in get_all_houses():
                if house.is_new():
                    yield house
                    house.add_hash_to_file()
            sleep(1)
