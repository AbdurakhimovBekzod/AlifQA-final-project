import os
import requests
from dotenv import load_dotenv
import pytest

# Загружаем переменные из .env
load_dotenv()

BASE_URL = os.getenv("BASE_URL")  # https://gw.alifshop.uz/web
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

@pytest.mark.auth
def test_get_profile():
    """
    Проверка, что токен валиден и можно получить информацию о пользователе,
    а также проверка корректности полей name и phone
    """
    url = f"{BASE_URL}/client/profile/me"
    response = requests.get(url, headers=HEADERS)

    # Проверяем статус-код
    assert response.status_code == 200, f"Ошибка: {response.status_code} {response.text}"

    data = response.json()

    # Проверяем наличие полей
    assert "phone" in data, "Ошибка: поле 'phone' отсутствует в ответе"
    assert "name" in data, "Ошибка: поле 'name' отсутствует в ответе"

    # Проверяем, что поля не пустые
    assert data["phone"], "Ошибка: поле 'phone' пустое"
    assert data["name"], "Ошибка: поле 'name' пустое"

    print(f"Токен валиден, данные пользователя: Name='{data['name']}', Phone='{data['phone']}'")
