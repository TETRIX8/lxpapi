#!/bin/bash

API_URL="https://api.newlxp.ru/graphql"
EMAIL="evloevam@magas.ithub.ru"
PASSWORD="1Q2w3a4e\$#"

# Авторизация
response=$(curl -s -o response.json -w "%{http_code}" -X POST $API_URL \
-H "Content-Type: application/json" \
-H "Accept: */*" \
-d '{
  "operationName": "SignIn",
  "query": "query SignIn($input: SignInInput!) { signIn(input: $input) { user { id isLead __typename } accessToken __typename } }",
  "variables": {
    "input": {
      "email": "'"$EMAIL"'",
      "password": "'"$PASSWORD"'"
    }
  }
}')

if [ "$response" -ne 200 ]; then
  echo "Ошибка HTTP: $response"
  cat response.json
  exit 1
fi

# Проверка токена
TOKEN=$(cat response.json | jq -r '.data.signIn.accessToken')
if [ "$TOKEN" == "null" ]; then
  echo "Ошибка: Токен не получен."
  ERROR_MESSAGE=$(cat response.json | jq -r '.errors[0].message')
  echo "Сообщение об ошибке: $ERROR_MESSAGE"
  exit 1
fi

echo "Авторизация успешна. Токен: $TOKEN"

# Запрос данных пользователя (GetMe)
curl -X POST $API_URL \
-H "Content-Type: application/json" \
-H "Accept: */*" \
-H "Authorization: Bearer $TOKEN" \
-d '{
  "operationName": "GetMe",
  "query": "query GetMe { getMe { avatar createdAt email firstName id isLead roles phoneNumber legalDocumentsApprovedAt notificationsSettings { isPushDailyDigestOnEmail __typename } assignedSuborganizations { suborganization { name __typename } __typename } teacher { assignedDisciplines_V2 { discipline { name code studyPeriods { name startDate endDate __typename } __typename } __typename } __typename } __typename } }",
  "variables": {}
}' > user_data.json

# Форматированный вывод данных пользователя
echo "Данные пользователя:"
cat user_data.json | jq .

# Запрос задач преподавателя (TeacherDisciplineTasks)
curl -X POST $API_URL \
-H "Content-Type: application/json" \
-H "Accept: */*" \
-H "Authorization: Bearer $TOKEN" \
-d '{
  "operationName": "TeacherDisciplineTasks",
  "query": "query TeacherDisciplineTasks($input: TeacherDisciplinesTasksInput!) { teacherDisciplineTasks(input: $input) { ...TeacherAvailableTaskFragment __typename } } fragment TeacherAvailableTaskFragment on LearningGroupContentBlock { contentBlockId deadline canBeSentAfterDeadline testInterval { from to __typename } learningGroup { id name organizationId organization { name id isDeactivated timezoneMinutesOffset __typename } suborganizationIdV2 suborganizationV2 { organization { id name isDeactivated timezoneMinutesOffset __typename } __typename } __typename } topic { name id isCheckPoint isForPortfolio chapterId chapter { id name disciplineId discipline { id name code __typename } __typename } __typename } contentBlock { ... on TaskDisciplineTopicContentBlock { id kind name maxScore statistics { answered scored total __typename } __typename } ... on TestDisciplineTopicContentBlock { id name kind testMaxScore: maxScore canBePassed testId statistics { passed total __typename } __typename } __typename } __typename }",
  "variables": {
    "input": {
      "teacherId": "d1cd62ba-b879-42c6-89d3-54a3f24d2490",
      "filters": {},
      "limit": 6
    }
  }
}' > teacher_tasks.json

# Форматированный вывод задач преподавателя
echo "Задачи преподавателя:"
cat teacher_tasks.json | jq .

# Запрос расписания (ManyClassesForSchedule)
curl -X POST $API_URL \
-H "Content-Type: application/json" \
-H "Accept: */*" \
-H "Authorization: Bearer $TOKEN" \
-d '{
  "operationName": "ManyClassesForSchedule",
  "query": "query ManyClassesForSchedule($input: ManyClassesInput!, $isAdministrationSchedule: Boolean = false) { manyClasses(input: $input) { ...ClassInScheduleFragment __typename } } fragment ClassInScheduleFragment on Class { id from to name role isOnline isAutoMeetingLink meetingLink suborganizationId suborganization { id name __typename } retakingGroup { id name disciplineId __typename } discipline { id name code archivedAt templateDiscipline { id disciplinesGroup { id name __typename } __typename } suborganization { id organizationId __typename } __typename } learningGroup { id name isArchived __typename } classroom { id name buildingArea { id name __typename } __typename } teacher { id user { id firstName lastName middleName __typename } __typename } flow { id name learningGroups { id name __typename } __typename } hasAttendance @include(if: $isAdministrationSchedule) errors { ...ClassParamsErrorsFragment __typename } ctpTopics { id name __typename } __typename } fragment ClassParamsErrorsFragment on ClassParamsErrors { buildingArea classroom discipline teacher classCount classTime learningGroup __typename }",
  "variables": {
    "isAdministrationSchedule": false,
    "input": {
      "page": 1,
      "pageSize": 50
    }
  }
}' > schedule.json

# Форматированный вывод расписания
echo "Расписание:"
cat schedule.json | jq .

# Запрос предметов преподавания (GetTeacherDisciplines)
curl -X POST $API_URL \
-H "Content-Type: application/json" \
-H "Accept: */*" \
-H "Authorization: Bearer $TOKEN" \
-d '{
  "operationName": "GetTeacherDisciplines",
  "query": "query GetTeacherDisciplines { getMe { id roles teacher { academicDifference { disciplineId discipline { id name code archivedAt suborganization { id name organizationId __typename } studyPeriods { id name organizationId startDate endDate archivedAt __typename } __typename } __typename } assignedDisciplines_V2 { isActivated discipline { id name code archivedAt suborganization { id name organizationId __typename } studyPeriods { id name organizationId startDate endDate archivedAt __typename } __typename } learningGroups { id name isArchived __typename } __typename } onlyAssignedDisciplines { isActivated discipline { id name code archivedAt suborganization { id name organizationId __typename } studyPeriods { id name organizationId startDate endDate archivedAt __typename } __typename } learningGroups { id name isArchived __typename } __typename } __typename } __typename } }",
  "variables": {}
}' > teacher_disciplines.json

# Форматированный вывод предметов преподавания
echo "Предметы преподавания:"
cat teacher_disciplines.json | jq .

# Получение ID предметов из ответа
DISCIPLINE_IDS=$(cat teacher_disciplines.json | jq -r '.data.getMe.teacher.assignedDisciplines_V2[].discipline.id')

# Запрос информации о каждом предмете (GetDisciplineInfoById)
for DISCIPLINE_ID in $DISCIPLINE_IDS; do
  echo "Запрос информации о предмете с ID: $DISCIPLINE_ID"
  curl -X POST $API_URL \
  -H "Content-Type: application/json" \
  -H "Accept: */*" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "operationName": "GetDisciplineInfoById",
    "query": "query GetDisciplineInfoById($input: GetDisciplineByIdInput!) { getDisciplineById(input: $input) { code description id materials maxScore name studyHoursCount suborganizationId someStudentHasClassAttendance archivedAt isAutoMeetingLink synchronizedAt studyPeriods { id name organizationId __typename } sections { id name templateSection { suborganization { id organizationId __typename } __typename } __typename } suborganization { organizationId id name organization { timezoneMinutesOffset __typename } __typename } chapters { id __typename } templateDiscipline { id name disciplinesGroup { id name organizationId classesInRow classesPerDay classroomProperties { id name __typename } __typename } suborganization { id organization { id name __typename } __typename } __typename } __typename } }",
    "variables": {
      "input": {
        "disciplineId": "'"$DISCIPLINE_ID"'"
      }
    }
  }' > "discipline_$DISCIPLINE_ID.json"

  # Форматированный вывод информации о предмете
  echo "Информация о предмете с ID: $DISCIPLINE_ID"
  cat "discipline_$DISCIPLINE_ID.json" | jq .
done

# Запрос глав и тем для каждого предмета (GetDisciplineDataWithChaptersById)
for DISCIPLINE_ID in $DISCIPLINE_IDS; do
  echo "Запрос глав и тем для предмета с ID: $DISCIPLINE_ID"
  curl -X POST $API_URL \
  -H "Content-Type: application/json" \
  -H "Accept: */*" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "operationName": "GetDisciplineDataWithChaptersById",
    "query": "query GetDisciplineDataWithChaptersById($input: GetDisciplineByIdInput!, $userId: UUID!, $userRole: Identity_RoleType) { getDisciplineById(input: $input) { id maxScore name studyHoursCount archivedAt isAutoMeetingLink academicDifferenceDiscipline { id completionStatus __typename } suborganizationId retake { completionStatus contentFillingTeacherId content(userId: $userId, userRole: $userRole) { id __typename } __typename } chapters { description id name templateDisciplineChapterId topics { id isCheckPoint isUneditable isForPortfolio maxScore methodologicalType name order studyHoursCount chapterId templateDisciplineTopicId content { blocks { ... on InfoDisciplineTopicContentBlock { id kind __typename } ... on TestDisciplineTopicContentBlock { id kind __typename } ... on TaskDisciplineTopicContentBlock { id kind __typename } __typename } __typename } __typename } discipline { maxScore studyHoursCount templateDiscipline { name __typename } __typename } __typename } __typename } }",
    "variables": {
      "input": {
        "disciplineId": "'"$DISCIPLINE_ID"'"
      },
      "userId": "d1cd62ba-b879-42c6-89d3-54a3f24d2490",
      "userRole": "TEACHER"
    }
  }' > "chapters_and_topics_$DISCIPLINE_ID.json"

  # Форматированный вывод глав и тем
  echo "Главы и темы для предмета с ID: $DISCIPLINE_ID"
  cat "chapters_and_topics_$DISCIPLINE_ID.json" | jq .
done

# Запрос контента каждой темы (GetDisciplineChaptersForSidebar)
for DISCIPLINE_ID in $DISCIPLINE_IDS; do
  echo "Запрос контента для предмета с ID: $DISCIPLINE_ID"
  curl -X POST $API_URL \
  -H "Content-Type: application/json" \
  -H "Accept: */*" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "operationName": "GetDisciplineChaptersForSidebar",
    "query": "query GetDisciplineChaptersForSidebar($input: GetDisciplineByIdInput!) { getDisciplineById(input: $input) { name code chapters { id name topics { id name content { howStudyIt whyStudyIt blocks { ... on InfoDisciplineTopicContentBlock { id name kind order __typename } ... on TaskDisciplineTopicContentBlock { id name kind order __typename } ... on TestDisciplineTopicContentBlock { id name kind order __typename } __typename } __typename } __typename } __typename } suborganization { id organizationId __typename } __typename } }",
    "variables": {
      "input": {
        "disciplineId": "'"$DISCIPLINE_ID"'"
      }
    }
  }' > "topic_content_$DISCIPLINE_ID.json"

  # Форматированный вывод контента тем
  echo "Контент тем для предмета с ID: $DISCIPLINE_ID"
  cat "topic_content_$DISCIPLINE_ID.json" | jq .
done
