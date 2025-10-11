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

def test_delete_item_from_cart():
    """Удаление товара из корзины"""
    print("\n=== Шаг 5: Удаление товара из корзины ===")
    resp_cart = requests.get(f"{BASE_URL}/client/cart/view-cart", headers=HEADERS)
    assert resp_cart.status_code in [200, 201]

    cart_data = resp_cart.json()
    moderated_cart_items = cart_data.get("moderated_cart_items", [])

    if not moderated_cart_items:
        print("⚠Корзина пуста, нечего удалять!")
        return

    item = moderated_cart_items[0]
    moderated_offer_id = item.get("moderated_offer_id")
    product_name = item.get("name", "Неизвестный товар")

    resp_delete = requests.delete(
        f"{BASE_URL}/client/cart/authenticated/moderated-items/{moderated_offer_id}",
        headers=HEADERS
    )

    assert resp_delete.status_code in [200, 204]
    print(f"Товар '{product_name}' успешно удалён из корзины")
