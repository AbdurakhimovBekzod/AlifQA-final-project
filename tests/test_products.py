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

@pytest.mark.products
def test_get_active_products():
    """Получение активных товаров и выбор первого оффера"""
    print("\n=== Тест 2: Получение активных товаров ===")
    url = f"{BASE_URL}/client/events/active"
    response = requests.get(url, headers=HEADERS)
    assert response.status_code == 200, f"Не удалось получить список товаров, статус: {response.status_code}"
    print("Запрос выполнен успешно!")

    data = response.json()
    assert len(data) > 0, "Список товаров пуст"
    print(f"В ответе есть {len(data)} активных разделов")

    # Берем первый оффер с moderated_offer_id
    offer = None
    for event in data:
        offer = next((o for o in event.get("offers", []) if o.get("moderated_offer_id")), None)
        if offer:
            break
    assert offer is not None, "Нет оффера с moderated_offer_id"
    print("Найден оффер с moderated_offer_id")

    required_fields = ["moderated_offer_id", "name", "price", "quantity", "condition"]
    missing_fields = [f for f in required_fields if f not in offer]
    assert not missing_fields, f"Отсутствуют поля: {missing_fields}"
    print("Оффер содержит все нужные данные")

    # Сохраняем для последующих тестов
    global first_offer
    first_offer = {
        "moderated_offer_id": offer["moderated_offer_id"],
        "name": offer["name"],
        "price": offer["price"],
        "quantity": offer["quantity"],
        "condition_id": offer["condition"]["id"]
    }
    print(f"Товар выбран: {first_offer['name']} ({first_offer['price']} сум)")
