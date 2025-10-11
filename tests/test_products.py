import os
import requests
from dotenv import load_dotenv
import pytest

# Загружаем переменные окружения
load_dotenv()

BASE_URL = os.getenv("BASE_URL")  # например https://gw.alifshop.uz/web
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

@pytest.mark.products
def test_get_active_products():
    """
    1. Получаем список активных товаров
    2. Проверяем, что есть хотя бы один товар
    3. Находим первый оффер с moderated_offer_id
    4. Проверяем обязательные поля
    5. Выводим выбранный товар
    """
    url = f"{BASE_URL}/client/events/active"
    response = requests.get(url, headers=HEADERS)

    # --- Шаг 1 ---
    try:
        assert response.status_code == 200
        print("Запрос выполнен успешно!")
    except AssertionError:
        print(f"Запрос выполнен успешно! Статус: {response.status_code}")
        raise

    # Парсим JSON
    try:
        data = response.json()
    except Exception as e:
        print(f"Ошибка парсинга JSON: {e}")
        raise

    # --- Шаг 2 ---
    try:
        assert len(data) > 0
        print("В ответе есть хотя бы один активный товар")
    except AssertionError:
        print("В ответе есть хотя бы один активный товар")
        raise

    # --- Шаг 3 ---
    offer = None
    for event in data:
        offer = next((o for o in event.get("offers", []) if o.get("moderated_offer_id")), None)
        if offer:
            break

    try:
        assert offer is not None
        print("Найден оффер с moderated_offer_id")
    except AssertionError:
        print("Найден оффер с moderated_offer_id")
        raise

    # --- Шаг 4 ---
    required_fields = ["moderated_offer_id", "name", "price", "quantity", "condition"]
    missing_fields = [f for f in required_fields if f not in offer]
    if missing_fields:
        print(f"Оффер содержит все нужные данные Отсутствуют поля: {missing_fields}")
        raise AssertionError(f"Отсутствуют поля: {missing_fields}")
    else:
        print("Оффер содержит все нужные данные")

    # Проверка типа condition.id
    try:
        assert isinstance(offer["condition"]["id"], int)
    except AssertionError:
        print("Поле 'condition.id' должно быть числом")
        raise

    # --- Шаг 5 ---
    global first_offer
    first_offer = {
        "moderated_offer_id": offer["moderated_offer_id"],
        "name": offer["name"],
        "price": offer["price"],
        "quantity": offer["quantity"],
        "condition_id": offer["condition"]["id"]
    }
    print(f"Товар выбран: {first_offer['name']} ({first_offer['price']} сум)")
