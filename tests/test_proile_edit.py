import pytest
import allure
from config.application import Application
from faker import Faker

# Инициализируем Faker для генерации случайных имен
fake = Faker("ru_RU")


@allure.feature("Функционал Профиля пользователя")
class TestProfile:

    @pytest.mark.smoke
    @allure.title("Редактирование данных профиля")
    def test_user_can_edit_profile(self, app: Application, authorized_user):
        new_name = fake.name()
        new_description = "lolol"

        with allure.step("Открыть попап редактирования и изменить данные"):
            app.home_page.edit_profile(new_name, new_description)

        with allure.step("Проверить, что новые данные сохранились и отображаются на странице"):
            app.home_page.check_profile_data(new_name, new_description)
