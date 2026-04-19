from playwright.sync_api import Page, Locator, expect
from pages.base_page import BasePage

class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.add_button: Locator = self.page.locator(".profile__add-button")
        self.edit_profile_button: Locator = self.page.locator(".profile__edit-button")
        self.user_name: Locator = self.page.locator(".profile__title")
        self.user_description: Locator = self.page.locator(".profile__description")

        # Элементы попапа редактирования
        self.edit_popup: Locator = self.page.locator(".popup_type_edit")
        self.name_input: Locator = self.page.locator("#owner-name")
        self.description_input: Locator = self.page.locator("#owner-description")
        self.save_button: Locator = self.edit_popup.locator('button:has-text("Сохранить")')

    def check_is_loaded(self):
        """Проверяет, что ключевые элементы домашней страницы видны."""
        expect(self.add_button).to_be_visible()
        expect(self.edit_profile_button).to_be_visible()

    def edit_profile(self, name: str, description: str):
        """Полный цикл редактирования профиля."""
        self.edit_profile_button.click()
        expect(self.edit_popup).to_be_visible()
        self.name_input.fill(name)
        self.description_input.fill(description)
        self.save_button.click()
        expect(self.edit_popup).to_be_hidden()

    def check_profile_data(self, name: str, description: str):
        """Проверяет имя и описание пользователя в профиле."""
        expect(self.user_name).to_have_text(name)
        expect(self.user_description).to_have_text(description)
