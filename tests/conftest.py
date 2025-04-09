import pytest
import allure
import requests
from config import APIUrls, CourierDataGenerator, TestOrderData

@pytest.fixture
@allure.step("Отправка запроса на создание курьера")
def send_create_courier_request():
    """Фикстура для отправки запроса на создание курьера"""
    def _send_request(courier_data):
        """Отправляем запрос на создание курьера"""
        response = requests.post(APIUrls.COURIER_CREATE, json=courier_data)
        return response
    return _send_request

@pytest.fixture
def create_courier():
    """Фикстура для создания курьера и удаления после теста"""
    courier_data = CourierDataGenerator.generate_courier_data()
    response = requests.post(APIUrls.COURIER_CREATE, json=courier_data)
    response_data = response.json()

    assert response.status_code == 201, f"Не удалось создать курьера: {response.text}"

    courier_id = requests.post(APIUrls.COURIER_LOGIN, json={
        'login': courier_data['login'],
        'password': courier_data['password']
    }).json().get('id')

    allure.attach(f"Courier ID: {courier_id}", name="ID курьера", attachment_type=allure.attachment_type.TEXT)

    yield {**courier_data, 'status_code': response.status_code, 'ok': response_data.get('ok'), 'id': courier_id}

    # Удаляем курьера после теста
    if courier_id:
        delete_response = requests.delete(f"{APIUrls.COURIER_CREATE}/{courier_id}")
        assert delete_response.status_code == 200, f"Не удалось удалить курьера: {delete_response.text}"

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
@allure.step("Авторизация курьера")
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
@allure.step("Получение данных из генератора и удаление одного из обязательных полей")
def courier_data_with_missing_field(create_courier, missing_field):
    """Фикстура для создания данных курьера с отсутствующим обязательным полем"""
    # Генерируем данные курьера с помощью генератора
    courier_data = CourierDataGenerator.generate_courier_data()

    # Удаляем одно обязательное поле
    courier_data.pop(missing_field)

    return courier_data


@pytest.fixture
@allure.step("Попытка создать курьера с уже существующим логином")
def duplicate_courier(create_courier, send_create_courier_request):
    """Фикстура для попытки повторного создания курьера с уже существующим логином"""
    # Используем данные первого курьера
    existing_courier_data = create_courier
    response = send_create_courier_request(existing_courier_data)  # Отправка запроса на создание курьера

    # Логируем запрос
    allure.attach(f"Duplicate Courier Request: {existing_courier_data}",
                  name="Данные для повторной регистрации курьера", attachment_type=allure.attachment_type.JSON)

    return response


@pytest.fixture
@allure.step("Получение данных заказа")
def order_data_fixture():
    """Фикстура для получения данных заказа."""
    with allure.step("Получение данных для заказа"):
        return TestOrderData.order_data
