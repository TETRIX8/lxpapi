const axios = require("axios");

const API_URL = "https://api.newlxp.ru/graphql";
const EMAIL = "evloevam@magas.ithub.ru";
const PASSWORD = "password";

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
