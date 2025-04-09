from faker import Faker
import allure

fake = Faker()


class TestOrderData:
    test_track_number = 350031
    order_data = {
        "firstName": 'Taylor',
        "lastName": "Uchiha2",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2025-06-06",
        "comment": "Saske, come back to Konoha"
    }


class APIUrls:
    COURIER_LOGIN = 'https://qa-scooter.praktikum-services.ru/api/v1/courier/login'
    COURIER_CREATE = 'https://qa-scooter.praktikum-services.ru/api/v1/courier'
    ORDER_CREATE = 'https://qa-scooter.praktikum-services.ru/api/v1/orders'
    ORDER_TRACK = f'https://qa-scooter.praktikum-services.ru/api/v1/orders/track?t={TestOrderData.test_track_number}'


class CourierDataGenerator:
    @staticmethod
    @allure.step("Генерация данных для курьера")
    def generate_courier_data():
        login = fake.user_name()
        password = fake.password()
        first_name = fake.first_name()

        # Логируем сгенерированные данные для шага
        allure.attach(f"login: {login}, password: {password}, first_name: {first_name}",
                      name="Сгенерированные данные курьера",
                      attachment_type=allure.attachment_type.TEXT)

        return {
            'login': login,
            'password': password,
            'first_name': first_name
        }


class OrderDataGenerator:
    """Класс для генерации случайных данных заказа."""

    @staticmethod
    def generate_order_data():
        """Генерирует случайные данные заказа."""
        with allure.step("Генерация случайных данных для заказа"):
            order_data = {
                "firstName": fake.first_name(),
                "lastName": fake.last_name(),
                "address": fake.address(),
                "metroStation": fake.random_int(min=1, max=200),
                "phone": fake.phone_number(),
                "rentTime": fake.random_int(min=1, max=10),
                "deliveryDate": fake.date_this_year().isoformat(),
                "comment": fake.sentence()
            }
            allure.attach(str(order_data), name="Сгенерированные данные заказа",
                          attachment_type=allure.attachment_type.JSON)
            return order_data

