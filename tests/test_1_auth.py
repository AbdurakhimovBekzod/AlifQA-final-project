import os
import requests
from dotenv import load_dotenv
import pytest
import allure

load_dotenv()
BASE_URL = os.getenv("BASE_URL")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

@allure.epic("Проверка авторизации")
@allure.feature("Профиль пользователя")
@allure.story("Получение информации о профиле")
@pytest.mark.auth
def test_get_profile():
    """Проверка валидности токена и данных пользователя"""
    with allure.step("Отправка запроса на получение профиля"):
        url = f"{BASE_URL}/client/profile/me"
        response = requests.get(url, headers=HEADERS)
        assert response.status_code == 200, f"Ошибка: {response.status_code} {response.text}"

    with allure.step("Проверка полей в ответе"):
        data = response.json()
        assert "phone" in data and data["phone"], "Поле 'phone' пустое или отсутствует"
        assert "name" in data and data["name"], "Поле 'name' пустое или отсутствует"

    with allure.step("Вывод данных пользователя"):
        print(f"Name='{data['name']}', Phone='{data['phone']}'")
        allure.attach(str(data), name="Ответ профиля", attachment_type=allure.attachment_type.JSON)
