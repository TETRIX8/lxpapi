## Сайт демо 
[Перейти на сайт]( https://ithubrating.vercel.app/)

### Настройка перед работой 
1. [Выбор языка  ](#выбор-языка)
2.  [Установка зависимостей   ](#установка-зависимостей)


## Содержание
1. [Авторизация  для студентов ](#авторизация-для-учеников)
2.  [Получение данных дневника ученика  ](#запрос-дневника)
3.  [Получение данных о Учебный задачник для NewLXP   ](#учебный-задачник-для-NewLXP)
4.  
### Раздел для Учеников дополняется скоро будет больше






 ##  Все остальное только для учителей 
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




# Учебный задачник для NewLXP

Скрипт для просмотра учебных заданий через API образовательной платформы NewLXP.

## 📌 Основные функции

<details>
<summary>🔍 Просмотр списка заданий</summary>

- Пагинация (постраничный вывод)
- Фильтрация заданий
- Сортировка по срокам сдачи
- Статус выполнения каждого задания
</details>

<details>
<summary>📝 Детальный просмотр задания</summary>

- Полное описание задания
- Сроки сдачи (основной и индивидуальный)
- Максимальный балл
- Статус выполнения
- Связанные компетенции
- Возможность отправки ответа
</details>

## 🛠 Техническая реализация

<details>
 
<summary>Полный Код </summary>

```javascript
const axios = require("axios");
const readline = require("readline");

const API_URL = "https://api.newlxp.ru/graphql";
const EMAIL = "evloevam@magas.ithub.ru";
const PASSWORD = "password";

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function askQuestion(query) {
  return new Promise(resolve => rl.question(query, resolve));
}

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
        return response.data.data.signIn.accessToken;
    } catch (error) {
        console.error("Ошибка авторизации:", error.response?.data?.errors?.[0]?.message || error.message);
        process.exit(1);
    }
}

async function getUserData(token) {
    const query = `
    query GetMe {
      getMe {
        id
        firstName
        lastName
        roles
        __typename
      }
    }
    `;
    const headers = { Authorization: `Bearer ${token}` };
    try {
        const response = await axios.post(API_URL, { query }, { headers });
        return response.data.data.getMe;
    } catch (error) {
        console.error("Ошибка получения данных пользователя:", error.response?.data?.errors?.[0]?.message || error.message);
        return null;
    }
}

async function getTasksPage(token, studentId, pageSize, page = 1) {
    const query = `
    query StudentAvailableTasks($input: StudentAvailableTasksInput!) {
      studentAvailableTasks(input: $input) {
        hasMore
        page
        perPage
        total
        totalPages
        items {
          ...StudentAvailableTaskFragment
          __typename
        }
        __typename
      }
    }
    
    fragment StudentAvailableTaskFragment on StudentContentBlock {
      kind
      taskDeadline
      taskCanBeAnsweredAfterDeadline
      passDate
      testScore
      task {
        id
        scoreInPercent
        answers {
          id
          __typename
        }
        __typename
      }
      testInterval {
        from
        to
        __typename
      }
      customTaskDeadline {
        deadline
        formEducation {
          id
          startedAt
          finishedAt
          form
          studentId
          comment
          __typename
        }
        __typename
      }
      customTestInterval {
        interval {
          from
          to
          __typename
        }
        formEducation {
          id
          startedAt
          finishedAt
          form
          studentId
          comment
          __typename
        }
        __typename
      }
      studentTopic {
        status
        __typename
      }
      topic {
        name
        id
        isCheckPoint
        isForPortfolio
        chapterId
        chapter {
          id
          name
          disciplineId
          discipline {
            name
            code
            suborganization {
              organization {
                id
                name
                timezoneMinutesOffset
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
      contentBlock {
        ... on TaskDisciplineTopicContentBlock {
          id
          kind
          name
          maxScore
          __typename
        }
        ... on TestDisciplineTopicContentBlock {
          id
          name
          kind
          testMaxScore: maxScore
          canBePassed
          testId
          __typename
        }
        __typename
      }
      __typename
    }
    `;
    
    const variables = {
        input: {
            studentId: studentId,
            pageSize: pageSize,
            page: page,
            filters: {
                fromArchivedDiscipline: false
            }
        }
    };
    
    const headers = { Authorization: `Bearer ${token}` };
    
    try {
        const response = await axios.post(API_URL, { 
            operationName: "StudentAvailableTasks",
            query,
            variables 
        }, { headers });
        
        return response.data.data.studentAvailableTasks;
    } catch (error) {
        console.error("Ошибка получения заданий:", error.response?.data?.errors?.[0]?.message || error.message);
        return null;
    }
}

async function getTaskDetails(token, studentId, topicId, contentId) {
    const query = `
    query GetDisciplineTaskBlockByTopicIdAndContentId($input: GetByTopicIdAndContentIdInput!, $studentId: UUID!) {
      getDisciplineTaskBlockByTopicIdAndContentId(input: $input) {
        id
        name
        maxScore
        body
        studentCanSendAnswers(studentId: $studentId)
        studentDeadline(studentId: $studentId)
        studentCanSendAnswersAfterDeadline(studentId: $studentId)
        customStudentDeadline(studentId: $studentId) {
          deadline
          __typename
        }
        competencies {
          id
          name
          __typename
        }
        __typename
      }
    }
    `;
    
    const variables = {
        input: {
            contentId,
            topicId
        },
        studentId
    };
    
    const headers = { Authorization: `Bearer ${token}` };
    
    try {
        const response = await axios.post(API_URL, { 
            operationName: "GetDisciplineTaskBlockByTopicIdAndContentId",
            query,
            variables 
        }, { headers });
        
        return response.data.data.getDisciplineTaskBlockByTopicIdAndContentId;
    } catch (error) {
        console.error("Ошибка получения задания:", error.response?.data?.errors?.[0]?.message || error.message);
        return null;
    }
}

function formatTasksList(tasksData) {
    if (!tasksData || !tasksData.items || tasksData.items.length === 0) {
        return "🚫 Нет заданий для отображения";
    }

    let output = `\n📖 Задания (${tasksData.page}/${tasksData.totalPages})`;
    output += ` | Всего: ${tasksData.total} | На странице: ${tasksData.items.length}`;
    output += `\n${"━".repeat(60)}\n`;

    tasksData.items.forEach((task, index) => {
        const taskNum = index + 1;
        const taskType = task.kind === 'TASK' ? '📝 Задание' : '🧪 Тест';
        const taskName = task.contentBlock?.name || 'Без названия';
        const discipline = task.topic?.chapter?.discipline?.name || 'Неизвестно';
        const status = task.studentTopic?.status || '❓ Не начато';
        const deadline = task.taskDeadline ? new Date(task.taskDeadline).toLocaleString() : '⏳ Нет срока';

        output += `\n${taskNum}. ${taskType}: ${taskName}`;
        output += `\n   🏫 Дисциплина: ${discipline}`;
        output += `\n   📌 Статус: ${status}`;
        output += `\n   ⏰ Срок: ${deadline}`;
        output += `\n   🔗 ID задания: ${task.contentBlock?.id || 'Нет ID'}`;
        output += `\n${"─".repeat(60)}`;
    });

    output += `\n\n📜 Страницы: ${tasksData.hasMore ? 'Есть еще' : 'Последняя'}`;
    return output;
}

function formatTaskDetails(task) {
    if (!task) return "🚫 Задание не найдено";

    let output = `\n📌 ${task.name}`;
    output += `\n${"━".repeat(60)}`;
    output += `\n💯 Макс. балл: ${task.maxScore || 'Не указан'}`;
    output += `\n⏳ Срок сдачи: ${task.studentDeadline ? new Date(task.studentDeadline).toLocaleString() : 'Не указан'}`;
    output += `\n📤 Можно отправить: ${task.studentCanSendAnswers ? '✅ Да' : '❌ Нет'}`;
    
    if (task.customStudentDeadline) {
        output += `\n⏱️ Индивидуальный срок: ${new Date(task.customStudentDeadline.deadline).toLocaleString()}`;
    }

    if (task.body) {
        try {
            const bodyJson = JSON.parse(task.body);
            let cleanBody = '';
            
            bodyJson.forEach(item => {
                if (item.type === 'paragraph' && item.data?.text) {
                    cleanBody += item.data.text
                        .replace(/<[^>]+>/g, ' ')
                        .replace(/\s{2,}/g, ' ')
                        .trim() + '\n\n';
                }
            });
            
            if (cleanBody) {
                output += `\n\n📝 Описание задания:\n${"─".repeat(60)}\n${cleanBody}`;
            }
        } catch (e) {
            console.error("Ошибка парсинга тела задания:", e);
        }
    }

    if (task.competencies?.length > 0) {
        output += `\n\n🏆 Компетенции:`;
        task.competencies.forEach(comp => {
            output += `\n   • ${comp.name}`;
        });
    }

    return output;
}

async function mainMenu(token, studentId) {
    let currentPage = 1;
    let pageSize = 10;
    let tasksData = null;

    while (true) {
        console.clear();
        console.log("=== 📚 Учебные задания ===");
        
        if (!tasksData || currentPage !== tasksData?.page) {
            console.log(`\n⌛ Загружаю страницу ${currentPage}...`);
            tasksData = await getTasksPage(token, studentId, pageSize, currentPage);
        }

        if (tasksData) {
            console.log(formatTasksList(tasksData));
        } else {
            console.log("🚫 Не удалось загрузить задания");
            await askQuestion("\nНажмите Enter чтобы продолжить...");
            continue;
        }

        console.log("\n1. Выбрать страницу");
        console.log("2. Изменить количество заданий на странице");
        console.log("3. Просмотреть задание по номеру");
        console.log("4. Выход");

        const choice = await askQuestion("\nВыберите действие: ");

        switch (choice) {
            case '1':
                if (!tasksData) {
                    console.log("❌ Данные заданий не загружены!");
                    await askQuestion("Нажмите Enter чтобы продолжить...");
                    break;
                }
                const newPage = parseInt(await askQuestion(`Введите номер страницы (1-${tasksData.totalPages}): `));
                if (newPage >= 1 && newPage <= tasksData.totalPages) {
                    currentPage = newPage;
                } else {
                    console.log("❌ Некорректный номер страницы!");
                    await askQuestion("Нажмите Enter чтобы продолжить...");
                }
                break;

            case '2':
                const newSize = parseInt(await askQuestion("Количество заданий на странице (по умолчанию 10): "));
                if (newSize > 0 && newSize <= 100) {
                    pageSize = newSize;
                    currentPage = 1;
                    tasksData = null;
                } else {
                    console.log("❌ Количество должно быть от 1 до 100!");
                    await askQuestion("Нажмите Enter чтобы продолжить...");
                }
                break;

            case '3':
                if (!tasksData || tasksData.items.length === 0) {
                    console.log("❌ Нет заданий для просмотра!");
                    await askQuestion("Нажмите Enter чтобы продолжить...");
                    break;
                }

                const taskNum = parseInt(await askQuestion(`Введите номер задания (1-${tasksData.items.length}): `));
                if (taskNum >= 1 && taskNum <= tasksData.items.length) {
                    const selectedTask = tasksData.items[taskNum - 1];
                    const taskDetails = await getTaskDetails(
                        token,
                        studentId,
                        selectedTask.topic.id,
                        selectedTask.contentBlock.id
                    );
                    
                    console.clear();
                    console.log(formatTaskDetails(taskDetails));
                    await askQuestion("\nНажмите Enter чтобы вернуться...");
                } else {
                    console.log("❌ Некорректный номер задания!");
                    await askQuestion("Нажмите Enter чтобы продолжить...");
                }
                break;

            case '4':
                return;

            default:
                console.log("❌ Некорректный выбор!");
                await askQuestion("Нажмите Enter чтобы продолжить...");
                break;
        }
    }
}

(async () => {
    try {
        console.log("=== Система проверки учебных заданий ===");
        
        const token = await signIn();
        const userData = await getUserData(token);
        
        if (userData) {
            console.log(`\n👤 Добро пожаловать, ${userData.firstName} ${userData.lastName || ''}!`);
            await mainMenu(token, userData.id);
        }
    } catch (error) {
        console.error("❌ Ошибка:", error.message);
    } finally {
        rl.close();
    }
})();
```
- Использует GraphQL-запрос для входа
- Возвращает JWT-токен для последующих запросов
- Обрабатывает ошибки авторизации
</details>

<details>
<summary>📦 Получение списка заданий</summary>

```javascript
async function getTasksPage(token, studentId, pageSize, page) {
    const query = `
    query StudentAvailableTasks($input: StudentAvailableTasksInput!) {
      studentAvailableTasks(input: $input) {
        items {
          ...StudentAvailableTaskFragment
        }
      }
    }`;
    // ... реализация
}
```
- Поддерживает пагинацию (page, pageSize)
- Фильтрация по статусу и дисциплинам
- Возвращает структурированные данные о заданиях
</details>

## 🖥 Пример работы

<details>
<summary>📸 Скриншоты выполнения</summary>

**1. Авторизация:**
```
=== Система проверки учебных заданий ===
Авторизация успешна. Токен получен.
👤 Добро пожаловать, Иван Петров!
```

**2. Список заданий:**
```
📖 Задания (1/5) | Всего: 50 | На странице: 10
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 📝 Практическая работа
   🏫 Python на web
   📌 Статус: В работе
   ⏰ Срок: 15.12.2023, 23:59:00
```

**3. Детали задания:**
```
📌 Создание веб-приложения
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💯 Макс. балл: 35
⏳ Срок сдачи: 31.12.2024, 23:59:59
📤 Можно отправить: ✅ Да

📝 Описание:
Разработать веб-приложение с использованием Django...
```
</details>

## ⚙️ Установка и запуск

<details>
<summary>🔧 Требования</summary>

1. Node.js v16+
2. Установленные зависимости:
```bash
npm install axios readline
```
3. Файл конфигурации `.env` с учетными данными:
```
EMAIL=user@example.com
PASSWORD=secret
API_URL=https://api.newlxp.ru/graphql
```
</details>

<details>
<summary>🚀 Запуск</summary>

```bash
node script.js
```
После запуска откроется интерактивное меню с возможностью:
- Перехода по страницам
- Выбора количества заданий
- Просмотра деталей задания
</details>

## 🐛 Возможные ошибки

<details>
<summary>❌ Распространенные проблемы</summary>

**Ошибка авторизации:**
- Проверьте правильность логина/пароля
- Убедитесь, что аккаунт не заблокирован

**Нет данных о заданиях:**
- Проверьте подключение к интернету
- Убедитесь, что у вас есть активные курсы

**Ошибка формата данных:**
- API могло измениться - проверьте актуальность запросов
</details>
















### Запрос Дневника 

API предоставляет возможность авторизоваться и получить данные дневника студента. Для работы с API используется GraphQL.

### Конечные точки:
- **Авторизация**: `https://api.newlxp.ru/graphql`
- **Данные дневника**: `https://api.newlxp.ru/graphql`

---


## 1. Авторизация для учеников

Для выполнения запросов необходимо получить токен доступа через авторизацию.

### Параметры авторизации:
- **Email**: Адрес электронной почты пользователя.
- **Password**: Пароль пользователя.

<details>
<summary>Код на Python</summary>

```python
import requests

# Константы
AUTH_URL = "https://api.newlxp.ru/graphql"

# Запрос авторизации
auth_query = """
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

# Переменные для авторизации
auth_variables = {
    "input": {
        "email": "KostoevAB24@magas.ithub.ru",
        "password": "password"
    }
}

# Выполняем POST-запрос для авторизации
auth_response = requests.post(
    AUTH_URL,
    json={
        "operationName": "SignIn",
        "query": auth_query,
        "variables": auth_variables
    },
    headers={
        "Content-Type": "application/json",
        "apollographql-client-name": "web"
    }
)

# Проверяем успешность авторизации
if auth_response.status_code == 200:
    auth_data = auth_response.json()
    access_token = auth_data["data"]["signIn"]["accessToken"]
    student_id = auth_data["data"]["signIn"]["user"]["id"]
    print(f"Авторизация успешна! Токен: {access_token}, ID студента: {student_id}")
else:
    print("Ошибка авторизации:", auth_response.status_code, auth_response.text)
```

</details>

<details>
<summary>Код на JavaScript</summary>

```javascript
const axios = require('axios');

// Константы
const AUTH_URL = "https://api.newlxp.ru/graphql";

// Запрос авторизации
const authQuery = `
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

// Переменные для авторизации
const authVariables = {
  input: {
    email: "KostoevAB24@magas.ithub.ru",
    password: "password!"
  }
};

// Выполняем POST-запрос для авторизации
axios.post(AUTH_URL, {
  operationName: "SignIn",
  query: authQuery,
  variables: authVariables
}, {
  headers: {
    "Content-Type": "application/json",
    "apollographql-client-name": "web"
  }
}).then(authResponse => {
  if (authResponse.status === 200) {
    const authData = authResponse.data;
    const accessToken = authData.data.signIn.accessToken;
    const studentId = authData.data.signIn.user.id;
    console.log(`Авторизация успешна! Токен: ${accessToken}, ID студента: ${studentId}`);
  } else {
    console.error("Ошибка авторизации:", authResponse.status, authResponse.statusText);
  }
}).catch(error => {
  console.error("Произошла ошибка:", error.message);
});
```

</details>

---

## 2. Получение данных дневника

После успешной авторизации можно получить данные дневника студента.

### Параметры запроса:
- **studentId**: Идентификатор студента (получается при авторизации).
- **studyPeriodEndDate**: Дата окончания учебного периода (например, `"2025-06-29T21:00:00.000Z"`).

<details>
<summary>Код на Python</summary>

```python
# Запрос данных дневника
diary_query = """
query SearchStudentDisciplinesForDisciplinesTableWithPeriod($input: SearchStudentDisciplinesInput!, $studyPeriodEndDate: String, $studentId: UUID!) {
  searchStudentDisciplines(input: $input) {
    studentId
    disciplineId
    studyPeriod {
      endDate
      id
      name
      startDate
      status
      archivedAt
      __typename
    }
    academicDifferenceDisciplines {
      id
      academicDifferenceStudent(studentId: $studentId) {
        academicDifferenceStudentScore {
          academicDifferenceAbsoluteScore
          __typename
        }
        scoreForAnsweredAcademicDifferenceTasks
        __typename
      }
      maxScore
      teachers {
        user {
          id
          firstName
          lastName
          middleName
          __typename
        }
        __typename
      }
      __typename
    }
    discipline {
      maxScore
      code
      studyHoursCount
      archivedAt
      suborganization {
        id
        organizationId
        __typename
      }
      teachers {
        user {
          id
          firstName
          lastName
          middleName
          __typename
        }
        __typename
      }
      id
      name
      __typename
    }
    disciplineAttendance {
      percent
      total
      visited
      __typename
    }
    studentRecalculationScore {
      academicDifferenceAbsoluteScore
      __typename
    }
    academicDifferenceDisciplineGrade
    learningGroup {
      id
      name
      __typename
    }
    scoreForAnsweredTasks
    disciplineGrade(studyPeriodEndDate: $studyPeriodEndDate)
    disciplineGrade_V2(studyPeriodEndDate: $studyPeriodEndDate)
    retakeDisciplineGrade
    maxScoreForAnsweredTasks
    scoreForAnsweredRetakeTasks
    retakeScore
    hasRetake
    __typename
  }
}
"""

# Переменные для запроса дневника
diary_variables = {
    "input": {
        "studentId": student_id  # Используем ID студента из авторизации
    },
    "studyPeriodEndDate": "2025-06-29T21:00:00.000Z",
    "studentId": student_id  # Используем ID студента из авторизации
}

# Выполняем POST-запрос для получения данных дневника
diary_response = requests.post(
    DIARY_URL,
    json={
        "operationName": "SearchStudentDisciplinesForDisciplinesTableWithPeriod",
        "query": diary_query,
        "variables": diary_variables
    },
    headers={
        "Content-Type": "application/json",
        "apollographql-client-name": "web",
        "authorization": f"Bearer {access_token}"  # Используем токен из авторизации
    }
)

# Проверяем успешность запроса
if diary_response.status_code == 200:
    diary_data = diary_response.json()
    print("Данные дневника успешно получены:")
    print(diary_data)
else:
    print("Ошибка при запросе данных дневника:", diary_response.status_code, diary_response.text)
```

</details>

<details>
<summary>Код на JavaScript</summary>

```javascript
// Запрос данных дневника
const diaryQuery = `
query SearchStudentDisciplinesForDisciplinesTableWithPeriod($input: SearchStudentDisciplinesInput!, $studyPeriodEndDate: String, $studentId: UUID!) {
  searchStudentDisciplines(input: $input) {
    studentId
    disciplineId
    studyPeriod {
      endDate
      id
      name
      startDate
      status
      archivedAt
      __typename
    }
    academicDifferenceDisciplines {
      id
      academicDifferenceStudent(studentId: $studentId) {
        academicDifferenceStudentScore {
          academicDifferenceAbsoluteScore
          __typename
        }
        scoreForAnsweredAcademicDifferenceTasks
        __typename
      }
      maxScore
      teachers {
        user {
          id
          firstName
          lastName
          middleName
          __typename
        }
        __typename
      }
      __typename
    }
    discipline {
      maxScore
      code
      studyHoursCount
      archivedAt
      suborganization {
        id
        organizationId
        __typename
      }
      teachers {
        user {
          id
          firstName
          lastName
          middleName
          __typename
        }
        __typename
      }
      id
      name
      __typename
    }
    disciplineAttendance {
      percent
      total
      visited
      __typename
    }
    studentRecalculationScore {
      academicDifferenceAbsoluteScore
      __typename
    }
    academicDifferenceDisciplineGrade
    learningGroup {
      id
      name
      __typename
    }
    scoreForAnsweredTasks
    disciplineGrade(studyPeriodEndDate: $studyPeriodEndDate)
    disciplineGrade_V2(studyPeriodEndDate: $studyPeriodEndDate)
    retakeDisciplineGrade
    maxScoreForAnsweredTasks
    scoreForAnsweredRetakeTasks
    retakeScore
    hasRetake
    __typename
  }
}
`;

// Переменные для запроса дневника
const diaryVariables = {
  input: {
    studentId: studentId // Используем ID студента из авторизации
  },
  studyPeriodEndDate: "2025-06-29T21:00:00.000Z",
  studentId: studentId // Используем ID студента из авторизации
};

// Выполняем POST-запрос для получения данных дневника
axios.post(DIARY_URL, {
  operationName: "SearchStudentDisciplinesForDisciplinesTableWithPeriod",
  query: diaryQuery,
  variables: diaryVariables
}, {
  headers: {
    "Content-Type": "application/json",
    "apollographql-client-name": "web",
    "authorization": `Bearer ${accessToken}` // Используем токен из авторизации
  }
}).then(diaryResponse => {
  if (diaryResponse.status === 200) {
    const diaryData = diaryResponse.data;
    console.log("Данные дневника успешно получены:");
    console.log(diaryData);
  } else {
    console.error("Ошибка при запросе данных дневника:", diaryResponse.status, diaryResponse.statusText);
  }
}).catch(error => {
  console.error("Произошла ошибка:", error.message);
});
```

</details>







### Дальше Для учителей 




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
