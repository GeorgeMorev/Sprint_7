import pytest
import requests
from unittest.mock import patch
import allure


class CourierLogin:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/courier/login'

    VALID_LOGIN = "valid_login"
    VALID_PASSWORD = "valid_password"
    INVALID_LOGIN = "invalid_login"
    INVALID_PASSWORD = "invalid_password"
    MISSING_LOGIN = None
    MISSING_PASSWORD = None

    @staticmethod
    @allure.step("Отправка запроса на авторизацию курьера с логином {login} и паролем {password}")
    def login(login, password):
        payload = {"login": login, "password": password}
        response = requests.post(CourierLogin.BASE_URL, json=payload)

        return response


@allure.feature("Курьер")
@allure.story("Авторизация курьера")
@allure.title("Успешная авторизация курьера")
@allure.description("Этот тест проверяет успешную авторизацию курьера с правильным логином и паролем.")
def test_courier_login():
    """Тест на успешную авторизацию курьера."""

    with allure.step("Авторизация курьера с правильными данными"):
        response = CourierLogin.login(CourierLogin.VALID_LOGIN, CourierLogin.VALID_PASSWORD)

    with allure.step("Проверка, что сервер вернул статус-код 200"):
        assert response.status_code == 200, f"Ожидался статус-код 200, но получен {response.status_code} - {response.text}"

    with allure.step("Проверка, что в ответе есть id курьера"):
        response_json = response.json()
        assert "id" in response_json, f"Ожидалось, что в ответе будет id курьера, но его нет. Ответ: {response_json}"