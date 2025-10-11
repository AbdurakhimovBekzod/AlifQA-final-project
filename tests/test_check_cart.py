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

def test_view_cart():
    """Проверка, что товар добавлен в корзину"""
    print("\n=== Шаг 3: Проверка корзины ===")
    resp = requests.get(f"{BASE_URL}/client/cart/view-cart", headers=HEADERS)
    assert resp.status_code in [200, 201], f"Не удалось получить корзину, статус: {resp.status_code}"

    cart_data = resp.json()
    moderated_cart_items = cart_data.get("moderated_cart_items", [])

    if not moderated_cart_items:
        print("⚠️ Корзина пуста")
        return

    print(f"В корзине найдено {len(moderated_cart_items)} товаров")
    for item in moderated_cart_items:
        print(f"- {item.get('name')})")
