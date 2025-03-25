import requests
import json

API_URL = "https://api.newlxp.ru/graphql"
EMAIL="вашапочта"
PASSWORD="пороль"

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
        token = data["data"]["signIn"]["accessToken"]
        print(f"Авторизация успешна. Токен: {token}")
        return token
    else:
        print(f"Ошибка HTTP: {response.status_code}")
        print(response.text)
        exit(1)

# Получение данных пользователя
def get_user_data(token):
    query = """
    query GetMe {
      getMe {
        avatar
        createdAt
        email
        firstName
        id
        isLead
        roles
        phoneNumber
        legalDocumentsApprovedAt
        notificationsSettings {
          isPushDailyDigestOnEmail
          __typename
        }
        assignedSuborganizations {
          suborganization {
            name
            __typename
          }
          __typename
        }
        teacher {
          assignedDisciplines_V2 {
            discipline {
              name
              code
              studyPeriods {
                name
                startDate
                endDate
                __typename
              }
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
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(API_URL, json={"query": query}, headers=headers)
    if response.status_code == 200:
        print("Данные пользователя:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Ошибка HTTP: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    token = sign_in()
    get_user_data(token)
