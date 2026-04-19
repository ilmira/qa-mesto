import pytest
import allure
from playwright.sync_api import Page
from config.application import Application
from config.environments import *

# ============================================================
#
#   Хуки Pytest (Настройка и отчетность)
#
# ============================================================

def pytest_addoption(parser):
    """Добавляем опции для выбора окружения и типа пользователя."""
    parser.addoption("--env", default="dev", choices=[e.value for e in Environment],
                     help="Выберите окружение: dev или stage")
    parser.addoption("--user-type", default=None, choices=common_users.keys(),
                     help="Выберите тип пользователя: user или admin")

def pytest_configure(config):
    """Выводит информацию о тестовом окружении перед запуском."""
    env_name = config.getoption("--env")
    user_type = config.getoption("--user-type")
    print_environment_info(env_name, user_type)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Создает скриншот в Allure при падении теста."""
    outcome = yield
    report = outcome.get_result()
    if report.when == 'call' and report.failed:
        try:
            page = item.funcargs['page']
            allure.attach(
                page.screenshot(full_page=True), name=f"screenshot_{item.nodeid}",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            print(f"Не удалось сделать скриншот: {e}")

# ============================================================
#
#   Базовые фикстуры фреймворка (Браузер и Приложение)
#
# ============================================================

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, env_config):
    """Настраивает контекст браузера (URL, viewport, и т.д.)."""
    return {
        **browser_context_args,
        "base_url": env_config.url,
        "ignore_https_errors": True,
        "viewport": {"width": 1920, "height": 1080}
    }

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "headless": True
    }


@pytest.fixture(scope="function")
def app(page: Page) -> Application:
    """Основная фикстура, предоставляющая точку входа ко всем страницам."""
    return Application(page)

# ============================================================
#
#   Фикстуры конфигурации и данных
#
# ============================================================

@pytest.fixture(scope="session")
def env_config(request):
    """Предоставляет конфигурацию окружения (URL и т.д.)."""
    env_name = request.config.getoption("--env")
    return environments[Environment(env_name)]

@pytest.fixture(scope="function")
def user(request, env_config) -> UserCredentials:
    """Предоставляет учетные данные пользователя."""
    user_type = request.config.getoption("--user-type") or env_config.default_user
    if not user_type:
        pytest.fail("Тип пользователя не указан ни через --user-type, ни в конфиге окружения.")
    return common_users[user_type]

# ============================================================
#
#   Фикстуры состояния (State Fixtures)
#
# ============================================================

@pytest.fixture(scope="function")
def authorized_user(app: Application, user: UserCredentials):
    """Выполняет вход в систему и предоставляет авторизованного пользователя."""
    with allure.step(f"Авторизация под пользователем: {user.email}"):
        app.login_page.open()
        app.login_page.login(user.email, user.password)
        app.home_page.check_is_loaded()
    yield user
