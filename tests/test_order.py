import pytest
import allure
import requests
from config import APIUrls


@pytest.mark.parametrize("color, expected_status_code", [
    (["BLACK"], 201),
    (["GREY"], 201),
    (["BLACK", "GREY"], 201),
    ([], 201),
])
def test_create_order_with_colors(order_data_fixture, color, expected_status_code):
    order_data_fixture["color"] = color  # Добавляем цвет в данные заказа

    response = requests.post(APIUrls.ORDER_CREATE, json=order_data_fixture)

    with allure.step(f"Проверка, что запрос возвращает статус код {expected_status_code}"):
        assert response.status_code == expected_status_code, \
            f"Ожидался статус-код {expected_status_code}, но получен {response.status_code} - {response.text}"

    with allure.step("Проверка, что тело ответа содержит track"):
        response_json = response.json()
        assert "track" in response_json, f"Ожидалось, что в ответе будет track, но его нет. Ответ: {response_json}"


@allure.feature("Получение заказа по трек-номеру")
@allure.story("Успешное получение заказа")
def test_get_order_by_track():
    """Проверяет успешное получение заказа по трек-номеру."""

    with allure.step("Отправка запроса на получение заказа"):
        response = requests.get(APIUrls.ORDER_TRACK)

    with allure.step("Проверка, что статус-код 200"):
        assert response.status_code == 200, f"Ожидался 200, но получен {response.status_code} - {response.text}"

    with allure.step("Проверка, что в ответе есть поле 'order'"):
        response_json = response.json()
        assert "order" in response_json, f"Ожидалось поле 'order', но его нет. Ответ: {response_json}"