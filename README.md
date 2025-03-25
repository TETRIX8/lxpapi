### Обновленный `README.md` с раскрывающимися разделами

Ниже приведен обновленный файл `README.md`, который включает описание всех параметров и функционала скрипта. Разделы организованы с использованием HTML-тегов `<details>` и `<summary>`, чтобы их можно было скрыть или раскрыть при нажатии.

---

# API GraphQL Скрипт для работы с платформой IThub Магас

Этот скрипт позволяет выполнять следующие операции:
1. **Авторизация** через GraphQL API.
2. **Получение данных пользователя** (например, профиль, роли, привязки к организациям).
3. **Получение задач преподавателя**, включая дедлайны, статистику выполнения и связанные данные.

## Установка и настройка

### Предварительные требования
1. Установите `curl` и `jq`:
   ```bash
   sudo apt install curl jq
   ```
2. Убедитесь, что у вас есть доступ к API (`https://api.newlxp.ru/graphql`).

### Настройка скрипта
1. Откройте файл скрипта и укажите свои учетные данные:
   ```bash
   EMAIL="ваш_email@example.com"
   PASSWORD="ваш_пароль"
   ```
2. Убедитесь, что `teacherId` соответствует вашему ID в системе (если вы используете запрос `TeacherDisciplineTasks`).

### Использование
1. Выполните скрипт:
   ```bash
   ./script.sh
   ```
2. Результаты будут сохранены в файлы:
   - `user_data.json`: Данные пользователя (результат запроса `GetMe`).
   - `teacher_tasks.json`: Задачи преподавателя (результат запроса `TeacherDisciplineTasks`).

---

## Подробное описание

<details>
<summary>Авторизация</summary>

### Описание
Скрипт выполняет авторизацию через GraphQL API, отправляя запрос `SignIn` с указанными учетными данными (`email` и `password`). В ответ сервер возвращает JWT-токен, который используется для аутентификации последующих запросов.

### Параметры запроса
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
      "email": "ваш_email@example.com",
      "password": "ваш_пароль"
    }
  }
  ```

### Пример ответа
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
</details>

---

<details>
<summary>Получение данных пользователя (GetMe)</summary>

### Описание
Запрос `GetMe` возвращает подробную информацию о текущем пользователе, включая профиль, роли, привязки к организациям и другие данные.

### Параметры запроса
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

### Пример ответа
```json
{
  "data": {
    "getMe": {
      "avatar": "https://example.com/avatar.jpg",
      "createdAt": "2024-10-09T10:24:37.577Z",
      "email": "evloevam@magas.ithub.ru",
      "firstName": "Абдул-Кадыр",
      "id": "d1cd62ba-b879-42c6-89d3-54a3f24d2490",
      "isLead": false,
      "roles": ["TEACHER"]
    }
  }
}
```
</details>

---

<details>
<summary>Получение задач преподавателя (TeacherDisciplineTasks)</summary>

### Описание
Запрос `TeacherDisciplineTasks` возвращает список задач преподавателя, включая дедлайны, статистику выполнения и связанные данные (например, темы, главы, дисциплины).

### Параметры запроса
- **operationName**: `TeacherDisciplineTasks`
- **query**:
  ```graphql
  query TeacherDisciplineTasks($input: TeacherDisciplinesTasksInput!) {
    teacherDisciplineTasks(input: $input) {
      ...TeacherAvailableTaskFragment
      __typename
    }
  }
  fragment TeacherAvailableTaskFragment on LearningGroupContentBlock {
    contentBlockId
    deadline
    canBeSentAfterDeadline
    testInterval {
      from
      to
      __typename
    }
    learningGroup {
      id
      name
      organizationId
      organization {
        name
        id
        isDeactivated
        timezoneMinutesOffset
        __typename
      }
      suborganizationIdV2
      suborganizationV2 {
        organization {
          id
          name
          isDeactivated
          timezoneMinutesOffset
          __typename
        }
        __typename
      }
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
          id
          name
          code
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
        statistics {
          answered
          scored
          total
          __typename
        }
        __typename
      }
      ... on TestDisciplineTopicContentBlock {
        id
        name
        kind
        testMaxScore: maxScore
        canBePassed
        testId
        statistics {
          passed
          total
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
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

### Пример ответа
```json
{
  "data": {
    "teacherDisciplineTasks": [
      {
        "contentBlockId": "9d27e5b9-ec98-4b0b-9fbb-5e6d7269fc18",
        "deadline": "2025-01-09T20:59:59.999Z",
        "contentBlock": {
          "name": "Написать код на закрепление темы: \"Алфавит и лексика\"",
          "maxScore": 2,
          "statistics": {
            "answered": 23,
            "scored": 22,
            "total": 24
          }
        }
      }
    ]
  }
}
```
</details>

---

## Возможности анализа данных

Используйте `jq` для извлечения нужных полей. Например:

<details>
<summary>Примеры использования jq</summary>

### Получить названия всех задач
```bash
cat teacher_tasks.json | jq '.data.teacherDisciplineTasks[].contentBlock.name'
```

### Получить сроки выполнения задач
```bash
cat teacher_tasks.json | jq '.data.teacherDisciplineTasks[].deadline'
```

### Фильтрация задач по дедлайну
```bash
cat teacher_tasks.json | jq '.data.teacherDisciplineTasks[] | select(.deadline < "2025-01-10")'
```
</details>

---

## Лицензия
MIT License

---

Теперь все разделы организованы в раскрывающиеся блоки, что делает документ более удобным для чтения. Если нужно добавить еще информацию или улучшить структуру, напишите! 😊
