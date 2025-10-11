import os
import requests
from dotenv import load_dotenv
import pytest

# Загружаем переменные из .env
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

    # Получаем текущую корзину
    resp_cart = requests.get(f"{BASE_URL}/client/cart/view-cart", headers=HEADERS)
    assert resp_cart.status_code in [200, 201], f"Не удалось получить корзину, статус: {resp_cart.status_code}"
    cart_data = resp_cart.json()

    moderated_cart_items = cart_data.get("moderated_cart_items", [])

    if not moderated_cart_items:
        print("Корзина пуста, нечего удалять")
        return  # Завершаем тест, так как удалять нечего

    print(f"В корзине найдено {len(moderated_cart_items)} товаров")

    # Берем первый товар для удаления
    item = moderated_cart_items[0]
    moderated_offer_id = item.get("moderated_offer_id")
    item_id = item.get("item_id") or item.get("id")
    product_name = item.get("name", "Неизвестный товар")

    print(f"Товар для удаления: {product_name}")

    # Отправляем DELETE запрос
    resp_delete = requests.delete(
        f"{BASE_URL}/client/cart/authenticated/moderated-items/{moderated_offer_id}",
        headers=HEADERS
    )

    assert resp_delete.status_code in [200, 204], f"Не удалось удалить товар, статус: {resp_delete.status_code}"
    print(f"Товар '{product_name}' успешно удалён из корзины (status {resp_delete.status_code})")

    # Повторно получаем корзину для проверки
    resp_cart_check = requests.get(f"{BASE_URL}/client/cart/view-cart", headers=HEADERS)
    cart_check_data = resp_cart_check.json()
    remaining_item = next((i for i in cart_check_data.get("moderated_cart_items", [])
                           if i.get("moderated_offer_id") == moderated_offer_id), None)

    assert remaining_item is None, f"Товар '{product_name}' всё ещё присутствует в корзине!"
    print(f"Проверка пройдена: товар '{product_name}' отсутствует в корзине после удаления")
