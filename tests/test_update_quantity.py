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


def test_update_quantity():
    """Изменение количества товара в корзине"""
    print("\n=== Шаг 4: Увеличение количества товара в корзине ===")

    # Получаем текущую корзину
    resp_cart = requests.get(f"{BASE_URL}/client/cart/view-cart", headers=HEADERS)
    assert resp_cart.status_code in [200, 201], f"Не удалось получить корзину, статус: {resp_cart.status_code}"
    cart_data = resp_cart.json()

    moderated_cart_items = cart_data.get("moderated_cart_items", [])
    assert len(moderated_cart_items) > 0, "Корзина пуста, нечего обновлять"
    print(f"В корзине найдено {len(moderated_cart_items)} товаров")

    # Берем первый товар для обновления
    item = moderated_cart_items[0]
    moderated_offer_id = item.get("moderated_offer_id")
    condition_id = item["loan_condition"]["id"] if "loan_condition" in item else item["condition"]["id"]
    current_quantity = item.get("quantity", 1)

    # Определяем новое количество (динамически, добавляем 1)
    new_quantity = current_quantity + 1
    print(f"Текущие данные товара: {item['name']} (quantity={current_quantity})")
    print(f"Попытка увеличить количество до {new_quantity}")

    payload = {
        "moderated_offer_id": moderated_offer_id,
        "condition_id": condition_id,
        "quantity": new_quantity
    }

    resp_update = requests.patch(f"{BASE_URL}/client/cart/authenticated/moderated-items/quantity",
                                 json=payload, headers=HEADERS)

    if resp_update.status_code == 409:
        print("Достигнуто максимальное количество товара, увеличить нельзя")
        return
    assert resp_update.status_code in [200, 201], f"Не удалось обновить количество, статус: {resp_update.status_code}"
    print(f"Количество товара обновлено успешно (status {resp_update.status_code})")

    # Повторно получаем корзину для проверки актуального количества
    resp_cart_check = requests.get(f"{BASE_URL}/client/cart/view-cart", headers=HEADERS)
    cart_check_data = resp_cart_check.json()
    updated_item = next((i for i in cart_check_data.get("moderated_cart_items", [])
                         if i.get("moderated_offer_id") == moderated_offer_id), None)

    assert updated_item, "Товар не найден в корзине после обновления"
    actual_quantity = updated_item.get("quantity")
    print(f"Новое количество товара в корзине: {actual_quantity}")

    assert actual_quantity == new_quantity, f"Ожидалось quantity={new_quantity}, получено {actual_quantity}"
