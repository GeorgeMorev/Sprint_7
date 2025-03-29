import requests
import allure
import pytest
import config


@allure.feature("Курьер")
@allure.story("Создание курьера")
@allure.title("Успешная регистрация курьера")
@allure.description("Этот тест проверяет успешную регистрацию нового курьера.")
def test_create_courier(create_courier):
    response_ok = create_courier.get('ok')
    with allure.step("Проверка, что статус ответа равен 201"):
        response_status = create_courier.get('status_code')
        assert response_status == 201, f"Ожидался статус 201, но получен {response_status}"
    assert response_ok is True, "Ожидалось, что ответ будет {'ok': true}"


@allure.feature("Курьер")
@allure.story("Создание курьера")
@allure.title("Попытка создать курьера с уже существующим логином")
@allure.description("Этот тест проверяет, что нельзя создать двух курьеров с одинаковым логином.")
def test_create_duplicate_courier(duplicate_courier):
    with allure.step("Проверка, что сервер вернул статус-код 409"):
        assert duplicate_courier.status_code == 409, f"Ожидался 409, но получен {duplicate_courier.status_code} - {duplicate_courier.text}"

    with allure.step("Проверка, что сервер вернул корректное сообщение об ошибке"):
        assert duplicate_courier.json()["message"] == "Этот логин уже используется. Попробуйте другой.", \
            f"Некорректное сообщение об ошибке: {duplicate_courier.json()}"


@allure.feature("Курьер")
@allure.story("Создание курьера")
@allure.title("Проверка создания курьера без обязательных полей")
@allure.description(
    "Этот тест проверяет, что курьер не может быть создан, если отсутствует хотя бы одно обязательное поле.")
@pytest.mark.parametrize("missing_field", ["login", "password"])
def test_create_courier_missing_fields(courier_data_with_missing_field, missing_field):
    # Удаляем одно обязательное поле с помощью фикстуры
    courier_data = courier_data_with_missing_field

    with allure.step(f"Отправка запроса без поля {missing_field}"):
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', json=courier_data)

    with allure.step("Проверка, что сервер вернул статус-код 400"):
        assert response.status_code == 400, f"Ожидался статус-код 400, но получен {response.status_code} - {response.text}"

    with allure.step("Проверка сообщения об ошибке"):
        expected_message = "Недостаточно данных для создания учетной записи"
        assert response.json().get("message") == expected_message, \
            f"Ожидалось сообщение '{expected_message}', но получено {response.json()}"
