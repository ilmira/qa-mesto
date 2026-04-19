from playwright.sync_api import Page, Locator, expect
from pages.base_page import BasePage


class LoginPage(BasePage):
    PAGE_PATH = "/signin"

    def __init__(self, page: Page):
        super().__init__(page)
        self.email_input: Locator = self.page.locator("#email")
        self.password_input: Locator = self.page.locator("#password")
        self.login_button: Locator = self.page.get_by_role("button", name="Войти")
        self.error_message: Locator = page.locator(".popup__status-message")

    def open(self):
        """Открывает страницу входа, используя путь, определенный в классе."""
        super().open(self.PAGE_PATH)
        self.check_url_contains(self.PAGE_PATH)

    def login(self, email: str, password: str):
        """Выполняет полный процесс входа."""
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()

    def check_error_message(self, expected_text: str):
        """Проверяет, что на странице отображается корректное сообщение об ошибке."""
        expect(self.error_message).to_be_visible()
        expect(self.error_message).to_have_text(expected_text)
