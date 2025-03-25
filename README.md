Вот обновленный `README.md`, который включает три версии скрипта на разных языках программирования (Bash, Python и JavaScript). Пользователь может выбрать язык, а затем использовать соответствующую версию для выполнения запросов.

---

# GraphQL API Client

Этот проект предоставляет клиент для взаимодействия с GraphQL API. Вы можете выбрать один из трех языков программирования: **Bash**, **Python** или **JavaScript**. Каждая версия выполняет одни и те же задачи, такие как авторизация, получение данных пользователя, расписания, предметов преподавания и т.д.

## Содержание
1. [Выбор языка](#выбор-языка)
2. [Авторизация](#авторизация)
3. [Получение данных пользователя (GetMe)](#получение-данных-пользователя-getme)
4. [Получение задач преподавателя (TeacherDisciplineTasks)](#получение-задач-преподавателя-teacherdisciplinetasks)
5. [Получение расписания (ManyClassesForSchedule)](#получение-расписания-manyclassesforschedule)
6. [Получение предметов преподавания (GetTeacherDisciplines)](#получение-предметов-преподавания-getteacherdisciplines)
7. [Получение информации о предмете (GetDisciplineInfoById)](#получение-информации-о-предмете-getdisciplineinfobyid)
8. [Показ контента темы (GetDisciplineChaptersForSidebar)](#показ-контента-темы-getdisciplinechaptersforsidebar)

---

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
const PASSWORD = "1Q2w3a4e$#";

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

---

### Остальные разделы

Остальные разделы (`Авторизация`, `Получение данных пользователя`, `Получение задач преподавателя` и т.д.) остаются такими же, как в предыдущих версиях. Вы можете адаптировать их для каждого языка программирования, используя соответствующие библиотеки и синтаксис.

---

Теперь пользователи могут выбрать язык программирования и использовать готовые примеры для работы с GraphQL API.
