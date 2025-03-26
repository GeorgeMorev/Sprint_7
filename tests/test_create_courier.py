import pytest
import requests
import allure
import uuid
import string
import random


class Courier:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/courier'

    def __init__(self, login=None, password=None, first_name=None):
        """Создает объект курьера с уникальными данными"""
        self.login = login or self._generate_random_string(8)
        self.password = password or self._generate_random_string(10)
        self.first_name = first_name or self._generate_random_string(6)
        self.courier_id = None

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
        response = requests.post(self.BASE_URL, json=payload)
        if response.status_code == 201:
            self.courier_id = self.get_courier_id()
        return response

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
    return Courier()


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