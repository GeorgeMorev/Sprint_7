import pytest
import requests
import random
import string
import allure


@pytest.fixture
def register_new_courier_and_return_login_password():
    """Фикстура для создания нового курьера и возврата его учетных данных."""
    with allure.step("Генерация случайных учетных данных для курьера"):
        def generate_random_string(length):
            """Генерирует случайную строку из строчных букв заданной длины."""
            letters = string.ascii_lowercase
            return ''.join(random.choice(letters) for _ in range(length))

        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

    with allure.step("Отправка запроса на создание нового курьера"):
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', json=payload)

    with allure.step("Проверка, что курьер успешно создан"):
        assert response.status_code == 201

    return login, password, first_name


@allure.feature("Курьер")
@allure.story("Создание курьера")
@allure.title("Создание нового курьера с уникальным логином")
@allure.description("Этот тест проверяет, что можно создать нового курьера, и он успешно добавляется в систему.")
def test_create_courier(register_new_courier_and_return_login_password):
    with allure.step("Регистрация нового курьера"):
        login, password, first_name = register_new_courier_and_return_login_password

    with allure.step("Проверка, что данные курьера не пустые"):
        assert login
        assert password
        assert first_name


@allure.feature("Курьер")
@allure.story("Создание курьера")
@allure.title("Попытка создания дублирующего курьера")
@allure.description("Этот тест проверяет, что нельзя создать второго курьера с тем же логином.")
def test_create_duplicate_courier(register_new_courier_and_return_login_password):
    with allure.step("Регистрация первого курьера"):
        login, password, first_name = register_new_courier_and_return_login_password

    with allure.step("Попытка зарегистрировать второго курьера с тем же логином"):
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response_duplicate = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', json=payload)

    with allure.step("Проверка, что сервер вернул статус-код 409"):
        assert response_duplicate.status_code == 409
