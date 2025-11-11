import requests
import json

API_URL = "https://api.newlxp.ru/graphql"
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
        if 'errors' in data:
            print(f"Ошибка GraphQL при авторизации: {data['errors']}")
            exit(1)
        token = data["data"]["signIn"]["accessToken"]
        user_id = data["data"]["signIn"]["user"]["id"]
        print(f"Авторизация успешна.")
        return token, user_id
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
        if 'errors' in data:
            print(f"Ошибка GraphQL при получении дисциплин: {data['errors']}")
            return []
        return data["data"]["getMe"]["teacher"]["assignedDisciplines_V2"]
    else:
        print(f"Ошибка HTTP при получении дисциплин: {response.status_code}")
        print(response.text)
        return []

# Получение структуры дисциплины (главы и темы) - ИСПРАВЛЕННЫЙ ЗАПРОС ПО ОРИГИНАЛУ
def get_discipline_structure(token, discipline_id, user_id):
    query = """
    query GetDisciplineDataWithChaptersById($input: GetDisciplineByIdInput!, $userId: UUID!, $userRole: Identity_RoleType) {
      getDisciplineById(input: $input) {
        id
        maxScore
        name
        studyHoursCount
        archivedAt
        isAutoMeetingLink
        academicDifferenceDiscipline {
          id
          completionStatus
          __typename
        }
        suborganizationId
        retake {
          completionStatus
          contentFillingTeacherId
          content(userId: $userId, userRole: $userRole) {
            id
            __typename
          }
          __typename
        }
        chapters {
          description
          id
          name
          templateDisciplineChapterId
          topics {
            id
            isCheckPoint
            isUneditable
            isForPortfolio
            maxScore
            methodologicalType
            name
            order
            studyHoursCount
            chapterId
            templateDisciplineTopicId
            content {
              blocks {
                ... on InfoDisciplineTopicContentBlock {
                  id
                  kind
                  __typename
                }
                ... on TestDisciplineTopicContentBlock {
                  id
                  kind
                  __typename
                }
                ... on TaskDisciplineTopicContentBlock {
                  id
                  kind
                  __typename
                }
                __typename
              }
            }
            __typename
          }
          discipline {
            maxScore
            studyHoursCount
            templateDiscipline {
              name
              __typename
            }
            __typename
          }
          __typename
        }
        __typename
      }
    }
    """
    # Передаем disciplineId внутри объекта input
    # userId и userRole передаем как отдельные переменные
    variables = {
        "input": {"disciplineId": discipline_id},
        "userId": user_id,
        "userRole": "TEACHER" # Указываем вашу роль
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(API_URL, json={"query": query, "variables": variables}, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # Проверяем на наличие ошибок GraphQL в ответе
        if 'errors' in data:
            print(f"Ошибка GraphQL при получении структуры дисциплины: {data['errors']}")
            return None
        return data["data"]["getDisciplineById"]
    else:
        print(f"Ошибка HTTP при получении структуры дисциплины: {response.status_code}")
        print(response.text)
        return None

def main():
    token, user_id = sign_in()

    disciplines_data = get_my_disciplines(token)

    if not disciplines_data:
        print("У вас нет назначенных дисциплин или произошла ошибка.")
        return

    print("\n--- Ваши дисциплины ---")
    active_disciplines = [item for item in disciplines_data if item['isActivated'] and not item['discipline']['archivedAt']]
    for idx, item in enumerate(active_disciplines):
        disc = item['discipline']
        print(f"{idx + 1}. {disc['name']} (код: {disc['code']})")
        print(f"   ID: {disc['id']}")
        print(f"   Организация: {disc['suborganization']['organization']['name']}")
        print(f"   Подорганизация: {disc['suborganization']['name']}")
        # Проверяем учебные периоды
        if disc['studyPeriods']:
            current_period = next((p for p in disc['studyPeriods'] if p['status'] in ['STARTED', 'PLANNED']), None)
            if current_period:
                 print(f"   Учебный период: {current_period['name']} ({current_period['status']})")
        print("-" * 20)

    if not active_disciplines:
        print("У вас нет активных (не архивных) дисциплин.")
        return

    while True:
        try:
            choice = int(input(f"\nВыберите номер дисциплины (1-{len(active_disciplines)}): ")) - 1
            if 0 <= choice < len(active_disciplines):
                selected_discipline = active_disciplines[choice]
                break
            else:
                print("Неверный номер. Попробуйте снова.")
        except ValueError:
            print("Пожалуйста, введите число.")

    selected_discipline_id = selected_discipline['discipline']['id']
    selected_discipline_name = selected_discipline['discipline']['name']

    print(f"\n--- Загрузка структуры дисциплины: {selected_discipline_name} ---")
    discipline_structure = get_discipline_structure(token, selected_discipline_id, user_id)

    if not discipline_structure:
        print("Не удалось получить структуру дисциплины.")
        return

    print(f"\nДисциплина: {discipline_structure['name']}")
    print(f"Всего часов: {discipline_structure['studyHoursCount']}")
    print(f"Макс. баллов: {discipline_structure['maxScore']}")
    print(f"Архивирована: {'Да' if discipline_structure['archivedAt'] else 'Нет'}\n")

    for chapter in discipline_structure['chapters']:
        print(f"--- Глава: {chapter['name']} ---")
        print(f"    Описание: {chapter['description'] if chapter['description'] else 'Нет'}")
        total_chapter_hours = 0
        for topic in sorted(chapter['topics'], key=lambda x: x['order']):
            checkpoint_str = " (Контрольная точка)" if topic['isCheckPoint'] else ""
            print(f"  {topic['order'] + 1:2d}. {topic['name']}{checkpoint_str} - {topic['studyHoursCount']} ч. (Тип: {topic['methodologicalType']})")
            total_chapter_hours += topic['studyHoursCount']
            # Выводим типы блоков контента (если нужно)
            # if topic['content']['blocks']:
            #     block_types = [block['kind'] for block in topic['content']['blocks']]
            #     print(f"       Блоки: {', '.join(block_types)}")
        print(f"  Итого по главе: {total_chapter_hours} ч.\n")


if __name__ == "__main__":
    main()
