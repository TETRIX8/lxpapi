import requests
import json

API_URL = "https://api.newlxp.ru/graphql"  # Убрана лишняя кавычка в конце
EMAIL = "evloevam@magas.ithub.ru"
PASSWORD = "1Q2w3a4e$#"

# Авторизация
def sign_in():
    query = """
    query SignIn($input: SignInInput!) {
      signIn(input: $input) {
        user {
          id
          isLead
          __typename
        }
        accessToken
        __typename
      }
    }
    """
    variables = {
        "input": {
            "email": EMAIL,
            "password": PASSWORD
        }
    }
    response = requests.post(API_URL, json={"query": query, "variables": variables})
    if response.status_code == 200:
        data = response.json()
        # Проверяем, есть ли ошибка в GraphQL
        if 'errors' in data:
            print(f"Ошибка GraphQL при авторизации: {data['errors']}")
            exit(1)
        token = data["data"]["signIn"]["accessToken"]
        print(f"Авторизация успешна. Токен: {token}")
        return token
    else:
        print(f"Ошибка HTTP при авторизации: {response.status_code}")
        print(response.text)
        exit(1)

# Получение дисциплин, которые вы преподаёте
def get_my_disciplines(token):
    query = """
    query GetTeacherDisciplines {
        getMe {
            teacher {
                assignedDisciplines_V2 {
                    isActivated
                    disciplineId
                    discipline {
                        id
                        name
                        code
                        archivedAt
                        suborganization {
                            id
                            name
                            organization {
                                id
                                name
                            }
                        }
                        studyPeriods {
                            id
                            name
                            status
                            startDate
                            endDate
                        }
                    }
                }
            }
        }
    }
    """

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(API_URL, json={"query": query}, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # Проверяем, есть ли ошибка в GraphQL
        if 'errors' in data:
            print(f"Ошибка GraphQL при получении дисциплин: {data['errors']}")
            return []
        return data["data"]["getMe"]["teacher"]["assignedDisciplines_V2"]
    else:
        print(f"Ошибка HTTP при получении дисциплин: {response.status_code}")
        print(response.text)
        return []

# Основная функция
def main():
    # 1. Авторизоваться
    token = sign_in()

    # 2. Получить дисциплины
    disciplines_data = get_my_disciplines(token)

    # 3. Вывести информацию о дисциплинах
    print("\n--- Дисциплины, которые я преподаю ---")
    if not disciplines_data:
        print("Дисциплины не найдены или произошла ошибка при их получении.")
    else:
        for item in disciplines_data:
            discipline = item['discipline']
            is_activated = item['isActivated']
            archived_at = discipline['archivedAt']

            # Показываем только активные дисциплины (если это нужно)
            # if not is_activated:
            #     continue

            print(f"Название: {discipline['name']}")
            print(f"Код: {discipline['code']}")
            print(f"ID: {discipline['id']}")
            print(f"Активна: {is_activated}")
            print(f"Архивирована: {'Да' if archived_at else 'Нет'}")
            if archived_at:
                print(f"Дата архивации: {archived_at}")

            suborg = discipline['suborganization']
            print(f"Подорганизация: {suborg['name']} (ID: {suborg['id']})")
            org = suborg['organization']
            print(f"Организация: {org['name']} (ID: {org['id']})")

            if discipline['studyPeriods']:
                current_period = next((p for p in discipline['studyPeriods'] if p['status'] in ['STARTED', 'PLANNED']), None)
                if current_period:
                    print(f"Текущий/ближайший период: {current_period['name']} (Статус: {current_period['status']})")
                # Вывести все периоды (если нужно)
                # for period in discipline['studyPeriods']:
                #     print(f"  - {period['name']}: {period['status']} ({period['startDate']} - {period['endDate']})")
            else:
                print("Учебные периоды не указаны.")

            print("-" * 20)

if __name__ == "__main__":
    main()
