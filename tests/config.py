from faker import Faker
import allure

fake = Faker()


class APIUrls:
    COURIER_LOGIN = 'https://qa-scooter.praktikum-services.ru/api/v1/courier/login'
    COURIER_CREATE = 'https://qa-scooter.praktikum-services.ru/api/v1/courier'


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