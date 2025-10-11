import requests
import pytest
import allure
from conftest import BASE_URL, ACCESS_TOKEN, load_dotenv, HEADERS

@allure.epic("Проверка авторизации")
@allure.feature("Профиль пользователя")
@allure.story("Получение информации о профиле")
@pytest.mark.auth
def test_get_profile():
    """Проверка валидности токена и данных пользователя"""

    with allure.step("Проверка на получения профиля"):
        url = f"{BASE_URL}/client/profile/me"
        response = requests.get(url, headers=HEADERS)
        assert response.status_code == 200, f"Ошибка: {response.status_code} {response.text}"

    with allure.step("Проверка нужных полей в респонсе"):
        data = response.json()
        assert "phone" in data and data["phone"], "Поле 'phone' пустое или отсутствует"
        assert "name" in data and data["name"], "Поле 'name' пустое или отсутствует"

    with allure.step("Принтинг данных"):
        print(f"Name='{data['name']}', Phone='{data['phone']}'")
        allure.attach(str(data), name="Ответ профиля", attachment_type=allure.attachment_type.JSON)
