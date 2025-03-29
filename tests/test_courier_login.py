import pytest
import conftest
import allure


@allure.feature("Курьер")
@allure.story("Авторизация курьера")
@allure.title("Успешная авторизация курьера")
@allure.description("Этот тест проверяет успешную авторизацию курьера с правильным логином и паролем.")
def test_courier_login(login_courier, create_courier):
    response = login_courier(create_courier['login'], create_courier['password'])
    with allure.step("Проверка, что сервер вернул статус-код 200"):
        assert response.status_code == 200, (f"Ожидался статус-код 200, но получен "
                                             f"{response.status_code} - {response.text}")
    with allure.step("Проверка, что в ответе есть id курьера"):
        response_json = response.json()
        assert "id" in response_json, f"Ожидалось, что в ответе будет id курьера, но его нет. Ответ: {response_json}"

@allure.feature("Курьер")
@allure.story("Авторизация курьера")
@allure.title("Авторизация с недостающими полями")
@allure.description(
    "Этот тест проверяет, что запрос на авторизацию вернет ошибку, если не указать одно из обязательных полей.")
@pytest.mark.parametrize(
    "login, password, expected_status_code",
    [
        (None, None, 200),  # Без логина и пароля
        (None, 'valid_password', 404),  # Без логина
        ('valid_login', None, 404),  # Без пароля
    ]
)
def test_authorization_missing_fields(login, password, expected_status_code, login_courier):
    """Тест на проверку авторизации без обязательных полей."""

    with allure.step(f"Попытка авторизации с логином: {login}, паролем: {password}"):
        response = login_courier(login, password)  # Убедитесь, что login_courier — это функция, а не Response объект

    with allure.step(f"Проверка, что код ошибки {expected_status_code} был возвращен"):
        assert response.status_code == expected_status_code, \
            f"Ожидался статус-код {expected_status_code}, но получен {response.status_code} - {response.text}"