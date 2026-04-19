from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.home_page import HomePage
# Сюда мы будем добавлять импорты для новых страниц

class Application:
    def __init__(self, page: Page):
        self.page = page

        # Инициализируем все наши Page Objects здесь
        self.login_page = LoginPage(self.page)
        self.home_page = HomePage(self.page)
        # Когда появится, например, страница профиля, мы добавим:
        # self.profile_page = ProfilePage(self.page)
