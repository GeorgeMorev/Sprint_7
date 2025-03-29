import pytest
import allure
import requests
from config import APIUrls, CourierDataGenerator


@pytest.fixture
@allure.step("Создание курьера")
def create_courier():
    """Создает курьера с уникальными данными через API"""
    courier_data = CourierDataGenerator.generate_courier_data()  # Генерация данных курьера

    # Отправка запроса на создание курьера
    response = requests.post(APIUrls.COURIER_CREATE, json=courier_data)
    response_data = response.json()

    # Проверка успешности запроса
    assert response.status_code == 201, f"Ошибка при создании курьера: {response.text}"

    courier_id = response.json().get('id')

    # Логируем ответ и id курьера
    allure.attach(f"Response: {response.text}", name="Ответ API", attachment_type=allure.attachment_type.JSON)
    allure.attach(f"Courier ID: {courier_id}", name="ID курьера", attachment_type=allure.attachment_type.TEXT)


    # Возвращаем данные курьера и код ответа
    return {**courier_data, 'status_code': response.status_code, 'ok': response_data.get('ok')}


@pytest.fixture
@allure.step("Получение токена курьера")
def get_user_token(create_courier):
    """Получение токена курьера для дальнейшей работы с API"""
    login_data = {
        'login': create_courier['login'],
        'password': create_courier['password']
    }

    response = requests.post(APIUrls.COURIER_LOGIN, json=login_data)

    # Проверка успешности запроса
    assert response.status_code == 200, f"Ошибка при получении токена: {response.text}"

    token = response.json().get('token')

    # Логируем ответ и токен
    allure.attach(f"Response: {response.text}", name="Ответ API", attachment_type=allure.attachment_type.JSON)
    allure.attach(f"Token: {token}", name="Токен курьера", attachment_type=allure.attachment_type.TEXT)

    return token


@pytest.fixture(scope="function")
def login_courier(create_courier):
    """Фикстура для авторизации курьера"""
    def _login(login, password):
        login_data = {
            'login': login or create_courier['login'],
            'password': password or create_courier['password']
        }
        response = requests.post(APIUrls.COURIER_LOGIN, json=login_data)
        return response

    return _login


@pytest.fixture(scope="function")
def courier_data_with_missing_field(create_courier, missing_field):
    """Фикстура для создания данных курьера с отсутствующим обязательным полем"""
    # Генерируем данные курьера с помощью генератора
    courier_data = CourierDataGenerator.generate_courier_data()

    # Удаляем одно обязательное поле
    courier_data.pop(missing_field)

    return courier_data


@pytest.fixture
def duplicate_courier(create_courier):
    """Создает второй курьер с уже существующим логином"""
    duplicate_courier_data = {
        'login': create_courier['login'],  # Используем тот же логин
        'password': 'new_password',
        'first_name': 'NewFirstName'
    }
    response = requests.post(APIUrls.COURIER_CREATE, json=duplicate_courier_data)
    return response
