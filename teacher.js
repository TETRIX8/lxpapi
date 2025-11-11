// Конфигурация
const API_URL = "https://api.newlxp.ru/graphql";
const EMAIL = "evloevam@magas.ithub.ru";
const PASSWORD = "1Q2w3a4e$#";

// Функция для выполнения запросов GraphQL
async function graphqlRequest(query, variables, token = null) {
  const headers = {
    "Content-Type": "application/json",
  };
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(API_URL, {
    method: "POST",
    headers,
    body: JSON.stringify({
      query,
      variables,
    }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const result = await response.json();

  if (result.errors) {
    console.error("GraphQL errors:", result.errors);
    throw new Error(`GraphQL Error: ${result.errors[0]?.message || "Unknown error"}`);
  }

  return result.data;
}

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
      password: PASSWORD,
    },
  };

  const data = await graphqlRequest(query, variables);
  const token = data.signIn.accessToken;
  const userId = data.signIn.user.id;
  console.log("Авторизация успешна.");
  return { token, userId };
}

// Получение дисциплин, которые вы преподаёте
async function getMyDisciplines(token) {
  const query = `
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
  `;

  const data = await graphqlRequest(query, {}, token);
  return data.getMe.teacher.assignedDisciplines_V2;
}

// Получение структуры дисциплины (главы и темы) - ИСПРАВЛЕННЫЙ ЗАПРОС ПО ОРИГИНАЛУ
async function getDisciplineStructure(token, disciplineId, userId) {
  const query = `
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
  `;

  const variables = {
    input: { disciplineId: disciplineId },
    userId: userId,
    userRole: "TEACHER", // Указываем вашу роль
  };

  const data = await graphqlRequest(query, variables, token);
  return data.getDisciplineById;
}

// Основная функция
async function main() {
  try {
    const { token, userId } = await signIn();

    const disciplinesData = await getMyDisciplines(token);

    if (!disciplinesData || disciplinesData.length === 0) {
      console.log("У вас нет назначенных дисциплин или произошла ошибка.");
      return;
    }

    console.log("\n--- Ваши дисциплины ---");
    const activeDisciplines = disciplinesData.filter(item => item.isActivated && !item.discipline.archivedAt);
    activeDisciplines.forEach((item, index) => {
      const disc = item.discipline;
      console.log(`${index + 1}. ${disc.name} (код: ${disc.code})`);
      console.log(`   ID: ${disc.id}`);
      console.log(`   Организация: ${disc.suborganization.organization.name}`);
      console.log(`   Подорганизация: ${disc.suborganization.name}`);
      // Проверяем учебные периоды
      if (disc.studyPeriods && disc.studyPeriods.length > 0) {
        const currentPeriod = disc.studyPeriods.find(p => p.status === 'STARTED' || p.status === 'PLANNED');
        if (currentPeriod) {
          console.log(`   Учебный период: ${currentPeriod.name} (${currentPeriod.status})`);
        }
      }
      console.log("-".repeat(20));
    });

    if (activeDisciplines.length === 0) {
      console.log("У вас нет активных (не архивных) дисциплин.");
      return;
    }

    // Для чтения ввода в Node.js нужно использовать readline или стороннюю библиотеку
    // Используем readline для примера
    const readline = require('readline');
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });

    const question = (query) => new Promise((resolve) => rl.question(query, resolve));

    let choice;
    while (true) {
      const answer = await question(`\nВыберите номер дисциплины (1-${activeDisciplines.length}): `);
      choice = parseInt(answer) - 1;
      if (choice >= 0 && choice < activeDisciplines.length) {
        break;
      } else {
        console.log("Неверный номер. Попробуйте снова.");
      }
    }
    rl.close(); // Закрываем интерфейс readline после получения ввода

    const selectedDiscipline = activeDisciplines[choice];
    const selectedDisciplineId = selectedDiscipline.discipline.id;
    const selectedDisciplineName = selectedDiscipline.discipline.name;

    console.log(`\n--- Загрузка структуры дисциплины: ${selectedDisciplineName} ---`);
    const disciplineStructure = await getDisciplineStructure(token, selectedDisciplineId, userId);

    if (!disciplineStructure) {
      console.log("Не удалось получить структуру дисциплины.");
      return;
    }

    console.log(`\nДисциплина: ${disciplineStructure.name}`);
    console.log(`Всего часов: ${disciplineStructure.studyHoursCount}`);
    console.log(`Макс. баллов: ${disciplineStructure.maxScore}`);
    console.log(`Архивирована: ${disciplineStructure.archivedAt ? 'Да' : 'Нет'}\n`);

    disciplineStructure.chapters.forEach(chapter => {
      console.log(`--- Глава: ${chapter.name} ---`);
      console.log(`    Описание: ${chapter.description || 'Нет'}`);
      let totalChapterHours = 0;
      chapter.topics
        .sort((a, b) => a.order - b.order) // Сортировка тем по порядку
        .forEach(topic => {
          const checkpointStr = topic.isCheckPoint ? " (Контрольная точка)" : "";
          // Исправленная строка с форматированием номера
          console.log(`  ${(topic.order + 1).toString().padStart(2, '0')}. ${topic.name}${checkpointStr} - ${topic.studyHoursCount} ч. (Тип: ${topic.methodologicalType})`);
          totalChapterHours += topic.studyHoursCount;
        });
      console.log(`  Итого по главе: ${totalChapterHours} ч.\n`);
    });

  } catch (error) {
    console.error("Произошла ошибка:", error.message);
  }
}

// Запуск основной функции
main();
