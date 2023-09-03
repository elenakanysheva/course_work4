from classes import HeadHunter, SuperJob, Connector


def main():
    vacancies_json = []
    #keyword = input("Введите ключевое слово для поиска: ")
    keyword = "Python"
# Создание экземпляра класса для работы с API сайтов с вакансиями
    sj = SuperJob(keyword)
    hh = HeadHunter(keyword)

    for api in (sj, hh):
        api.get_vacancies(pages_count=10)
        vacancies_json.extend(api.get_formatted_vacancies())

    connector = Connector(keyword=keyword)
    connector.insert(vacancies_json=vacancies_json)

    while True:
        command = input(
            "1 - Вывести списек вакансий;\n"
            "2 - Отсортировать по минимальной зарплате;\n"
            "exit - для выхода. \n;"
            ">>>"
        )
        if command.lower() == 'exit':
            break
        elif command == "1":
            vacancies = connector.select()
        elif command == "2":
            vacancies = connector.sort_by_salary_from_desc()
        elif command == "3":
            vacancies = connector.sort_by_salary_from_desc()

        for vacancy in vacancies:
            print(vacancy, end='\n')


if __name__ == "__main__":
    main()
