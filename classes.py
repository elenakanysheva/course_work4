from abc import ABC, abstractmethod
from exception import ParsingError
from utils import get_currencies
import requests
import json


class Engine(ABC):
    """Абстрактный класс для получения данных с сайта по API"""
    @abstractmethod
    def get_requests(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass


class HeadHunter(Engine):
    url = 'https://api.hh.ru/vacancies/'

    def __init__(self, keyword, page=0):
        self.params = {
            "per_page": 100,
            "page": page,
            "text": keyword,
            "archive": False
        }
        self.vacancies = []

    def get_requests(self):
        response = requests.get(self.url, params=self.params)
        if response.status_code != 200:
            raise ParsingError(f"Ошибка получения вакансий! Статус: {response.status_code}")
        return response.json()

    def get_formatted_vacancies(self):
        formatted_vacancies = []
        #currencies = get_currencies()
        sj_currencies = {
            "rub": "RUR",
            "uah": "UAH",
            "uzs": "UZS"
        }
        for vacancy in self.vacancies:
            formatted_vacancy = {
                "employer": vacancy["employer"],
                "title": vacancy["name"],
                "url": vacancy["url"],
                "api": "HeadHunter",
                "salary_from": vacancy['salary']['from'] if vacancy['salary'] else None,
                "salary_to": vacancy["salary"]['to'] if vacancy['salary'] else None,
            }
            #if vacancy["currency"] in sj_currencies:
            #    formatted_vacancy["currency"] = sj_currencies[vacancy["currency"]]
            #    formatted_vacancy["currency_value"] = currencies[sj_currencies[vacancy["currency"]]] if sj_currencies[vacancy["currency"]] in currencies else 1
            #elif vacancy["currency"]:
            #    formatted_vacancy["currency"] = "RUR"
            #    formatted_vacancy["currency_value"] = 1
            #else:
            #    formatted_vacancy["currency"] = None
            #    formatted_vacancy["currency_value"] = None

            formatted_vacancies.append(formatted_vacancy)

        return formatted_vacancies

    def get_vacancies(self, pages_count=2):
        self.vacancies = []
        for page in range(pages_count):
            page_vacancies = []
            self.params["page"] = page
            print(f"({self.__class__.__name__}) Парсинг страницы {page} -", end=" ")
            try:
                page_vacancies = self.get_requests()
            except ParsingError as error:
                print(error)
            else:
                self.vacancies.extend(page_vacancies)
                print(f"Загружено вакансий: {len(page_vacancies)}")
            if len(page_vacancies) == 0:
                break


class SuperJob(Engine):
    url = "https://api.superjob.ru/2.0/vacancies/"

    def __init__(self, keyword, page=0):
        self.params = {
            "count": 100,
            "page": page,
            "keyword": keyword,
            "archive": False
        }
        self.headers = {"X-Api-App-Id":
            "v3.r.137791167.1f514c9cbc840606e75754777399b37e0e9180ad.8137e53e47cecc4f576494cc962cc7b0e10a4b09"
        }
        self.vacancies = []

    def get_requests(self):
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise ParsingError(f"Ошибка получения вакансий! Статус: {response.status_code}")
        return response.json()["objects"]

    def get_formatted_vacancies(self):
        formatted_vacancies = []
        #currencies = get_currencies()
        sj_currencies = {
            "rub": "RUR",
            "uah": "UAH",
            "uzs": "UZS"
        }
        for vacancy in self.vacancies:
            formatted_vacancy = {
                "employer": vacancy["firm_name"],
                "title": vacancy["profession"],
                "url": vacancy["link"],
                "api": "SuperJob",
                "salary_from": vacancy["payment_from"] if vacancy["payment_from"] and vacancy["payment_from"] != 0 else None,
                "salary_to": vacancy["payment_to"] if vacancy["payment_to"] and vacancy["payment_to"] != 0 else None
            }
            #   formatted_vacancy["currency"] = sj_currencies[vacancy["currency"]]
            #    formatted_vacancy["currency_value"] = currencies[sj_currencies[vacancy["currency"]]] if sj_currencies[vacancy["currency"]] in currencies else 1
            #elif vacancy["currency"]:
             #   formatted_vacancy["currency"] = "RUR"
            #    formatted_vacancy["currency_value"] = 1
            #else:
            #    formatted_vacancy["currency"] = None
            #    formatted_vacancy["currency_value"] = None

            formatted_vacancies.append(formatted_vacancy)

        return formatted_vacancies

    def get_vacancies(self, pages_count=2):
        self.vacancies = []
        for page in range(pages_count):
            page_vacancies = []
            self.params["page"] = page
            print(f"({self.__class__.__name__}) Парсинг страницы {page} -", end=" ")
            try:
                page_vacancies = self.get_requests()
            except ParsingError as error:
                print(error)
            else:
                self.vacancies.extend(page_vacancies)
                print(f"Загружено вакансий: {len(page_vacancies)}")
            if len(page_vacancies) == 0:
                break


class Vacancy:
    def __init__(self, vacancy):
        self.employer = vacancy["employer"]
        self.title = vacancy["title"]
        self.url = vacancy["url"]
        self.api = vacancy["api"]
        self.salary_from = vacancy["salary_from"]
        self.salary_to = vacancy["salary_to"]
        self.currency = vacancy["currency"]
        self.currency_value = vacancy["currency_value"]

    def __str__(self):
        if not self.salary_from and not self.salary_to:
            salary = "Не указана"


class Connector:
    def __init__(self, keyword):
        self.filename = f"{keyword.title()}.json"

    def insert(self, vacancies_json):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(vacancies_json, file, indent=4, ensure_ascii=False)

    def select(self):
        with open(self.filename, "r", encoding="utf-8") as file:
            vacancies = json.load(file)
        return [Vacancy(x) for x in vacancies]




