import os
import requests
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("BASE_URL")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def test_update_quantity():
    """Изменение количества товара в корзине"""
    print("\n=== Шаг 4: Обновление количества товара в корзине ===")
    resp_cart = requests.get(f"{BASE_URL}/client/cart/view-cart", headers=HEADERS)
    assert resp_cart.status_code in [200, 201]

    cart_data = resp_cart.json()
    moderated_cart_items = cart_data.get("moderated_cart_items", [])

    if not moderated_cart_items:
        print("⚠Корзина пуста, нечего обновлять!")
        return

    item = moderated_cart_items[0]
    moderated_offer_id = item.get("moderated_offer_id")
    condition_id = item["loan_condition"]["id"] if "loan_condition" in item else item["condition"]["id"]
    current_quantity = item.get("quantity", 1)
    new_quantity = current_quantity + 1

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

    assert resp_update.status_code in [200, 201]
    print(f"Количество товара увеличено с {current_quantity} до {new_quantity}")
