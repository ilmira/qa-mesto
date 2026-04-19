
import pytest
import allure
from config.application import Application
from config.environments import UserCredentials

@allure.feature("Функционал Авторизации")
class TestLogin:

    @pytest.mark.smoke
    @allure.title("Успешная авторизация пользователя")
    def test_user_successful_login(self, app: Application, authorized_user):
        with allure.step("Проверить, что URL после входа соответствует главной странице"):
            app.home_page.check_url_contains("https://qa-mesto.praktikum-services.ru/")

    @pytest.mark.regression
    @allure.title("Авторизация с неверным паролем")
    def test_login_with_invalid_password(self, app: Application, user: UserCredentials):
        with allure.step("Открыть страницу входа"):
            app.login_page.open()

        with allure.step("Ввести верный email и неверный пароль"):
            app.login_page.login(user.email, "wrong_password_123")

        with allure.step("Проверить отображение ошибки"):
            app.login_page.check_error_message("Что-то пошло не так!") #специлом падаем, для allure
