from classes import HeadHunter, SuperJob, Connector
from utils import sort_by_salary_from_desc


def main():
    vacancies_json = []
    #keyword = input("Введите ключевое слово для поиска: ")
    keyword = "Python"
# Создание экземпляра класса для работы с API сайтов с вакансиями
    sj = SuperJob(keyword)
    hh = HeadHunter(keyword)

    for api in (hh,sj):
        api.get_vacancies(pages_count=10)
        vacancies_json.extend(api.get_formatted_vacancies())

    connector = Connector(keyword=keyword)
    connector.insert(vacancies_json=vacancies_json)
    all_vacancies = connector.select()

    vacancies =[]
    while True:
        command = input(
            "1 - Вывести списек вакансий;\n"
            "2 - Отсортировать по зарплате;\n"
            "exit - выход. \n"
            ">>>"
        )
        if command.lower() == 'exit':
            break
        elif command == "1":
            vacancies = all_vacancies
        elif command == "2":
            vacancies = sort_by_salary_from_desc(all_vacancies)

        for vacancy in vacancies:
            print(vacancy, end='\n')


if __name__ == "__main__":
    main()
