import pytest
import requests
import allure
import uuid
import string
import random


class CourierCreate:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/courier'

    def __init__(self, login=None, password=None, first_name=None):
        """Создает объект курьера с уникальными данными"""
        self.login = login or self._generate_random_string(8)
        self.password = password or self._generate_random_string(10)
        self.first_name = first_name or self._generate_random_string(6)
        self.courier_id = None
        self.last_response = None

    @staticmethod
    def _generate_random_string(length=10):
        """Генерирует случайную строку"""
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    def register(self):
        """Регистрирует курьера через API"""
        payload = {
            "login": self.login,
            "password": self.password,
            "firstName": self.first_name
        }
        try:
            self.last_response = requests.post(self.BASE_URL, json=payload)

            if self.last_response is not None and self.last_response.status_code == 201:
                self.courier_id = self.get_courier_id()

            return self.last_response
        except requests.RequestException as e:
            print(f"Ошибка при отправке запроса: {e}")
            return None

    def get_courier_id(self):
        """Получает ID курьера после успешной регистрации"""
        payload = {"login": self.login, "password": self.password}
        response = requests.post(f"{self.BASE_URL}/login", json=payload)
        if response.status_code == 200:
            return response.json().get('id')
        return None

    def delete(self):
        """Удаляет курьера через API"""
        if self.courier_id:
            response = requests.delete(f"{self.BASE_URL}/{self.courier_id}")
            return response
        return None


@pytest.fixture(scope="function")
def new_courier():
    """Фикстура создаёт объект курьера с уникальными данными"""
    return CourierCreate()


@pytest.fixture(scope="function")
def register_courier(new_courier):
    """Фикстура регистрирует нового курьера перед тестом"""
    response = new_courier.register()
    if response.status_code != 201:
        pytest.fail(f"Ошибка при регистрации курьера: {response.status_code} - {response.text}")
    return new_courier


@pytest.fixture(scope="function")
def delete_courier(register_courier):
    """Фикстура удаляет курьера после теста"""
    yield
    response = register_courier.delete()
    if response and response.status_code != 200:
        print(f"Ошибка при удалении курьера: {response.status_code} - {response.text}")


@allure.feature("Курьер")
@allure.story("Создание курьера")
@allure.title("Успешная регистрация курьера")
@allure.description("Этот тест проверяет успешную регистрацию нового курьера.")
def test_create_courier(register_courier, delete_courier):
    courier = register_courier
    with allure.step("Проверка, что ID курьера был получен после регистрации"):
        assert courier.courier_id is not None, "ID курьера не был получен после регистрации"

    with allure.step("Проверка, что ответ содержит {'ok': true}"):
        assert courier.last_response is not None, "Ошибка: last_response не был сохранен"
        expected_response = {"ok": True}
        assert courier.last_response.json() == expected_response, (
            f"Ожидался ответ {expected_response}, но получен {courier.last_response.json()}"
        )


@allure.feature("Курьер")
@allure.story("Создание курьера")
@allure.title("Попытка создать курьера с уже существующим логином")
@allure.description("Этот тест проверяет, что нельзя создать двух курьеров с одинаковым логином.")
def test_create_duplicate_courier(register_courier, delete_courier):
    courier = register_courier

    duplicate_courier = CourierCreate(login=courier.login, password="another_password", first_name="AnotherTest")

    with allure.step("Отправка запроса на регистрацию второго курьера с таким же логином"):
        response = duplicate_courier.register()

    with allure.step("Проверка, что сервер вернул статус-код 409"):
        assert response.status_code == 409, f"Ожидался 409, но получен {response.status_code} - {response.text}"

    with allure.step("Проверка, что сервер вернул корректное сообщение об ошибке"):
        assert response.json()["message"] == "Этот логин уже используется. Попробуйте другой.", \
            f"Некорректное сообщение об ошибке: {response.json()}"


import requests
import allure
import pytest

@allure.feature("Курьер")
@allure.story("Создание курьера")
@allure.title("Проверка создания курьера без обязательных полей")
@allure.description(
    "Этот тест проверяет, что курьер не может быть создан, если отсутствует хотя бы одно обязательное поле.")
@pytest.mark.parametrize("missing_field", ["login", "password"])
def test_create_courier_missing_fields(register_courier, missing_field):

    # Создаём данные курьера с отсутствующим обязательным полем
    courier_data = {
        "login": register_courier.login,
        "password": register_courier.password
    }

    # Удаляем одно обязательное поле
    courier_data.pop(missing_field)

    with allure.step(f"Отправка запроса без поля {missing_field}"):
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', json=courier_data)

    with allure.step("Проверка, что сервер вернул статус-код 400"):
        assert response.status_code == 400, f"Ожидался статус-код 400, но получен {response.status_code} - {response.text}"

    with allure.step("Проверка сообщения об ошибке"):
        expected_message = "Недостаточно данных для создания учетной записи"
        assert response.json().get("message") == expected_message, \
            f"Ожидалось сообщение '{expected_message}', но получено {response.json()}"
