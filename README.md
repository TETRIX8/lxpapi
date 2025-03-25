## Сайт демо 
[Перейти на сайт]( https://lxpapi.vercel.app/)
## Содержание
1. [Авторизация  и получение данных профиля для всех на разных языках](#выбор-языка)
 ##  Все остальное только для учителей Скоро будет Для учеников 
2. [Авторизация](#авторизация)
3. [Получение данных пользователя (GetMe)](#получение-данных-пользователя-getme)
4. [Получение задач преподавателя (TeacherDisciplineTasks)](#получение-задач-преподавателя-teacherdisciplinetasks)
5. [Получение расписания (ManyClassesForSchedule)](#получение-расписания-manyclassesforschedule)
6. [Получение предметов преподавания (GetTeacherDisciplines)](#получение-предметов-преподавания-getteacherdisciplines)
7. [Получение информации о предмете (GetDisciplineInfoById)](#получение-информации-о-предмете-getdisciplineinfobyid)
8. [Получение глав и тем предмета (GetDisciplineDataWithChaptersById)](#получение-глав-и-тем-предмета-getdisciplinedatawithchaptersbyid)
9. [Показ контента темы (GetDisciplineChaptersForSidebar)](#показ-контента-темы-getdisciplinechaptersforsidebar)


### Выбор языка

Перед началом работы выберите язык программирования, который вы хотите использовать:

1. **Bash**: Подходит для использования в Unix-подобных системах.
2. **Python**: Удобен для кроссплатформенной разработки и обработки данных.
3. **JavaScript**: Идеально подходит для интеграции с Node.js или браузерными приложениями.

#### Как начать:
1. Выберите язык.
2. Перейдите в соответствующий раздел ниже.
3. Следуйте инструкциям для установки зависимостей и запуска скрипта.

---

### Bash

#### Установка зависимостей
Убедитесь, что у вас установлены следующие инструменты:
- `curl`
- `jq`

```bash
sudo apt install curl jq
```

#### Запуск скрипта
1. Создайте файл `api_client.sh` и скопируйте код из раздела выше.
2. Сделайте файл исполняемым:
   ```bash
   chmod +x api_client.sh
   ```
3. Запустите скрипт:
   ```bash
   ./api_client.sh
   ```

---

### Python

#### Установка зависимостей
Убедитесь, что у вас установлен Python 3.x и `pip`. Установите необходимые библиотеки:
```bash
pip install requests
```

#### Пример кода
```python
import requests
import json

API_URL = "https://api.newlxp.ru/graphql"
EMAIL = "evloevam@magas.ithub.ru"
PASSWORD = "Password$#"

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
```

#### Запуск скрипта
```bash
python api_client.py
```

---

### JavaScript (Node.js)

#### Установка зависимостей
Убедитесь, что у вас установлен Node.js. Установите необходимые пакеты:
```bash
npm install axios
```

#### Пример кода
```javascript
const axios = require("axios");

const API_URL = "https://api.newlxp.ru/graphql";
const EMAIL = "evloevam@magas.ithub.ru";
const PASSWORD = "Password$#";

// Авторизация
async function signIn() {
    const query = `
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
    `;
    const variables = {
        input: {
            email: EMAIL,
            password: PASSWORD
        }
    };
    try {
        const response = await axios.post(API_URL, { query, variables });
        const token = response.data.data.signIn.accessToken;
        console.log(`Авторизация успешна. Токен: ${token}`);
        return token;
    } catch (error) {
        console.error("Ошибка HTTP:", error.response.status);
        console.error(error.response.data);
        process.exit(1);
    }
}

// Получение данных пользователя
async function getUserData(token) {
    const query = `
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
    `;
    const headers = { Authorization: `Bearer ${token}` };
    try {
        const response = await axios.post(API_URL, { query }, { headers });
        console.log("Данные пользователя:");
        console.log(JSON.stringify(response.data, null, 2));
    } catch (error) {
        console.error("Ошибка HTTP:", error.response.status);
        console.error(error.response.data);
    }
}

(async () => {
    const token = await signIn();
    await getUserData(token);
})();
```

#### Запуск скрипта
```bash
node api_client.js
```



### Авторизация

#### Описание
Запрос выполняет вход в систему и получает токен доступа для последующих запросов.

#### Параметры запроса
- **operationName**: `SignIn`
- **query**:
  ```graphql
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
  ```

- **variables**:
  ```json
  {
    "input": {
      "email": "evloevam@magas.ithub.ru",
      "password": "Password$#"
    }
  }
  ```

#### Пример ответа
```json
{
  "data": {
    "signIn": {
      "user": {
        "id": "d1cd62ba-b879-42c6-89d3-54a3f24d2490",
        "isLead": false,
        "__typename": "User"
      },
      "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
  }
}
```

---

### Получение данных пользователя (GetMe)

#### Описание
Запрос возвращает информацию о текущем пользователе, включая ID, имя, роли, подразделения и другие параметры.

#### Параметры запроса
- **operationName**: `GetMe`
- **query**:
  ```graphql
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
  ```

#### Пример ответа
```json
{
  "data": {
    "getMe": {
      "avatar": null,
      "createdAt": "2023-09-15T12:34:56.789Z",
      "email": "evloevam@magas.ithub.ru",
      "firstName": "Абдул-Кадыр",
      "id": "d1cd62ba-b879-42c6-89d3-54a3f24d2490",
      "isLead": false,
      "roles": ["TEACHER"],
      "phoneNumber": "+79281234567",
      "legalDocumentsApprovedAt": "2023-09-16T10:00:00.000Z",
      "notificationsSettings": {
        "isPushDailyDigestOnEmail": true
      },
      "assignedSuborganizations": [
        {
          "suborganization": {
            "name": "ИСиП Магас"
          }
        }
      ],
      "teacher": {
        "assignedDisciplines_V2": [
          {
            "discipline": {
              "name": "Введение в программирование",
              "code": "161.ВВП.25В",
              "studyPeriods": [
                {
                  "name": "Осень 2024",
                  "startDate": "2024-09-01T00:00:00.000Z",
                  "endDate": "2024-12-31T23:59:59.999Z"
                }
              ]
            }
          }
        ]
      }
    }
  }
}
```

---

### Получение задач преподавателя (TeacherDisciplineTasks)

#### Описание
Запрос возвращает список задач преподавателя, включая информацию о группах, дисциплинах и типах задач.

#### Параметры запроса
- **operationName**: `TeacherDisciplineTasks`
- **query**:
  ```graphql
  query TeacherDisciplineTasks($input: TeacherDisciplinesTasksInput!) {
    teacherDisciplineTasks(input: $input) {
      contentBlockId
      deadline
      learningGroup {
        id
        name
        __typename
      }
      topic {
        id
        name
        __typename
      }
      contentBlock {
        id
        name
        kind
        __typename
      }
      __typename
    }
  }
  ```

- **variables**:
  ```json
  {
    "input": {
      "teacherId": "d1cd62ba-b879-42c6-89d3-54a3f24d2490",
      "filters": {},
      "limit": 6
    }
  }
  ```

#### Пример ответа
```json
{
  "data": {
    "teacherDisciplineTasks": [
      {
        "contentBlockId": "12345678-1234-1234-1234-123456789abc",
        "deadline": "2025-03-24T23:59:59.000Z",
        "learningGroup": {
          "id": "048431c0-e42b-4476-b70a-a797b26a58f6",
          "name": "2Р1-11.23"
        },
        "topic": {
          "id": "afe8e555-06ae-433d-87c0-fb9c542f2705",
          "name": "Введение в DevOps"
        },
        "contentBlock": {
          "id": "ddf99523-57fd-4a01-9a38-4a896d05953f",
          "name": "Раньше было лучше? Каскадная модель разработки",
          "kind": "INFO"
        }
      }
    ]
  }
}
```

---

### Получение расписания (ManyClassesForSchedule)

#### Описание
Запрос возвращает расписание занятий, включая время начала и окончания, дисциплины, группы, преподавателей и аудитории.

#### Параметры запроса
- **operationName**: `ManyClassesForSchedule`
- **query**:
  ```graphql
  query ManyClassesForSchedule($input: ManyClassesInput!, $isAdministrationSchedule: Boolean = false) {
    manyClasses(input: $input) {
      id
      from
      to
      name
      role
      isOnline
      isAutoMeetingLink
      meetingLink
      discipline {
        id
        name
        code
        __typename
      }
      learningGroup {
        id
        name
        __typename
      }
      classroom {
        id
        name
        __typename
      }
      teacher {
        id
        user {
          id
          firstName
          lastName
          __typename
        }
        __typename
      }
      __typename
    }
  }
  ```

- **variables**:
  ```json
  {
    "isAdministrationSchedule": false,
    "input": {
      "page": 1,
      "pageSize": 50
    }
  }
  ```

#### Пример ответа
```json
{
  "data": {
    "manyClasses": [
      {
        "id": "94fbc880-083c-47ef-bb5c-ccdf7f176562",
        "from": "2025-03-24T07:40:00.000Z",
        "to": "2025-03-24T09:15:00.000Z",
        "name": null,
        "role": "TEACHER",
        "isOnline": false,
        "isAutoMeetingLink": true,
        "meetingLink": "https://my.mts-link.ru/97601155/197574913/record-new/945835986",
        "discipline": {
          "id": "ddb1449d-f247-4b65-b8ec-877b33665420",
          "name": "Введение в программирование",
          "code": "161.ВВП.25В"
        },
        "learningGroup": {
          "id": "539824fd-cfd3-446b-b5b3-ceafb2a1686e",
          "name": "1П3-9.24"
        }
      }
    ]
  }
}
```

---

### Получение предметов преподавания (GetTeacherDisciplines)

#### Описание
Запрос возвращает список дисциплин, которые преподает пользователь, включая информацию о подразделениях, учебных периодах и группах.

#### Параметры запроса
- **operationName**: `GetTeacherDisciplines`
- **query**:
  ```graphql
  query GetTeacherDisciplines {
    getMe {
      teacher {
        assignedDisciplines_V2 {
          discipline {
            id
            name
            code
            studyPeriods {
              id
              name
              startDate
              endDate
              __typename
            }
            __typename
          }
          learningGroups {
            id
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
  ```

#### Пример ответа
```json
{
  "data": {
    "getMe": {
      "teacher": {
        "assignedDisciplines_V2": [
          {
            "discipline": {
              "id": "229b29ef-01a9-43d5-8537-582ce9a25b2f",
              "name": "Введение в DevOps",
              "code": "3309.ВВД.25В",
              "studyPeriods": [
                {
                  "id": "9d2b0f2d-52b2-4fff-8459-c5a46c51bbaf",
                  "name": "Весенний семестр 24-25",
                  "startDate": "2025-01-08T21:00:00.000Z",
                  "endDate": "2025-06-29T21:00:00.000Z"
                }
              ]
            },
            "learningGroups": [
              {
                "id": "0484
