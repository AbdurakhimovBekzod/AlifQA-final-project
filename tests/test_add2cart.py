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

@pytest.fixture
def product_to_add():
    """Берем первый активный товар"""
    print("\n=== Шаг 1: Получение списка товаров ===")
    resp = requests.get(f"{BASE_URL}/client/events/active", headers=HEADERS)
    assert resp.status_code == 200, f"Не удалось получить список товаров, статус: {resp.status_code}"

    data = resp.json()
    assert len(data) > 0, "Список товаров пуст"

    offer = data[0]["offers"][0]
    assert offer.get("moderated_offer_id"), "Нет moderated_offer_id у оффера"

    print(f"Товар выбран: {offer['name']} ({offer['price']} сум)")
    return offer

def test_add_to_cart(product_to_add):
    """Добавление товара в корзину"""
    print("\n=== Шаг 2: Добавление товара в корзину ===")
    payload = {
        "moderated_offer_id": product_to_add["moderated_offer_id"],
        "condition_id": product_to_add["condition"]["id"],
        "quantity": 1
    }

    resp = requests.post(f"{BASE_URL}/client/cart/authenticated/moderated-items",
                         json=payload, headers=HEADERS)

    if resp.status_code in [200, 201]:
        print(f"Товар '{product_to_add['name']}' успешно добавлен в корзину")
    elif resp.status_code == 409:
        print("Достигнуто максимальное количество товара в корзине")
    else:
        assert False, f"Ошибка при добавлении товара, статус: {resp.status_code}"
