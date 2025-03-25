

# GraphQL API Client

Этот скрипт взаимодействует с GraphQL API для получения данных о пользователе, расписании, преподаваемых предметах, темах и контенте.

## Содержание
1. [Авторизация](#авторизация)
2. [Получение данных пользователя (GetMe)](#получение-данных-пользователя-getme)
3. [Получение задач преподавателя (TeacherDisciplineTasks)](#получение-задач-преподавателя-teacherdisciplinetasks)
4. [Получение расписания (ManyClassesForSchedule)](#получение-расписания-manyclassesforschedule)
5. [Получение предметов преподавания (GetTeacherDisciplines)](#получение-предметов-преподавания-getteacherdisciplines)
6. [Получение информации о предмете (GetDisciplineInfoById)](#получение-информации-о-предмете-getdisciplineinfobyid)
7. [Получение глав и тем предмета (GetDisciplineDataWithChaptersById)](#получение-глав-и-тем-предмета-getdisciplinedatawithchaptersbyid)
8. [Показ контента темы (GetDisciplineChaptersForSidebar)](#показ-контента-темы-getdisciplinechaptersforsidebar)

---

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
      "password": "1Q2w3a4e$#"
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
