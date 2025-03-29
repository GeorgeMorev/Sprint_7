import pytest
import requests
from unittest.mock import patch
import allure


class CourierLogin:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/courier/login'

    VALID_LOGIN = 'valid_login'
    VALID_PASSWORD = 'valid_password'
    INVALID_LOGIN = "invalid_login"
    INVALID_PASSWORD = "invalid_password"
    MISSING_LOGIN = None
    MISSING_PASSWORD = None

    @staticmethod
    @allure.step("Отправка запроса на авторизацию курьера с логином {login} и паролем {password}")
    def login(login, password):
        payload = {"login": login, "password": password}
        response = requests.post(CourierLogin.BASE_URL, json=payload,  timeout=30)

        return response


@allure.feature("Курьер")
@allure.story("Авторизация курьера")
@allure.title("Успешная авторизация курьера")
@allure.description("Этот тест проверяет успешную авторизацию курьера с правильным логином и паролем.")
def test_courier_login():

    with allure.step("Авторизация курьера с правильными данными"):
        response = CourierLogin.login(CourierLogin.VALID_LOGIN, CourierLogin.VALID_PASSWORD)

    with allure.step("Проверка, что сервер вернул статус-код 200"):
        assert response.status_code == 200, f"Ожидался статус-код 200, но получен {response.status_code} - {response.text}"

    with allure.step("Проверка, что в ответе есть id курьера"):
        response_json = response.json()
        assert "id" in response_json, f"Ожидалось, что в ответе будет id курьера, но его нет. Ответ: {response_json}"


@allure.feature("Курьер")
@allure.story("Авторизация курьера")
@allure.title("Авторизация с недостающими полями")
@allure.description("Этот тест проверяет, что запрос на авторизацию вернет ошибку, если не указать одно из обязательных полей.")
@pytest.mark.parametrize(
    "login, password, expected_status_code",
    [
        (CourierLogin.MISSING_LOGIN, CourierLogin.MISSING_PASSWORD, 400),  # Без логина и пароля
        (CourierLogin.MISSING_LOGIN, CourierLogin.VALID_PASSWORD, 400),  # Без логина
        (CourierLogin.VALID_LOGIN, CourierLogin.MISSING_PASSWORD, 400),  # Без пароля
    ]
)
def test_authorization_missing_fields(login, password, expected_status_code):
    """Тест на проверку авторизации без обязательных полей."""

    with allure.step(f"Попытка авторизации с логином: {login}, паролем: {password}"):
        response = CourierLogin.login(login, password)

    with allure.step(f"Проверка, что код ошибки {expected_status_code} был возвращен"):
        assert response.status_code == expected_status_code, \
            f"Ожидался статус-код {expected_status_code}, но получен {response.status_code} - {response.text}"