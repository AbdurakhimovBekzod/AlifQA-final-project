import os
import requests
from dotenv import load_dotenv
import pytest

load_dotenv()
BASE_URL = os.getenv("BASE_URL")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

@pytest.mark.auth
def test_get_profile():
    """Проверка валидности токена и данных пользователя"""
    print("\n=== Тест 1: Проверка профиля пользователя ===")
    url = f"{BASE_URL}/client/profile/me"
    response = requests.get(url, headers=HEADERS)

    assert response.status_code == 200, f"Ошибка: {response.status_code} {response.text}"
    print("Токен валиден, статус 200")

    data = response.json()
    assert "phone" in data and data["phone"], "Ошибка: поле 'phone' пустое или отсутствует"
    assert "name" in data and data["name"], "Ошибка: поле 'name' пустое или отсутствует"

    print(f"Данные пользователя: Name='{data['name']}', Phone='{data['phone']}'")
