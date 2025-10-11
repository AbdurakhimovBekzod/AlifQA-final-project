import os
import requests
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()
BASE_URL = os.getenv("BASE_URL")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}


def test_view_cart():
    """Проверка, что товар добавлен в корзину"""

    # Вставьте здесь данные вашего добавленного товара (из шага добавления)
    added_moderated_offer_id = "7f3e05ba-97cf-4e93-859b-2baae464e8f7"  # пример
    expected_product_name = "Смартфон Apple iPhone 16 Pro Max 256 ГБ (eSIM/nano SIM), Пустынный Титан"

    print("\n=== Шаг 3: Проверка содержимого корзины ===")
    resp = requests.get(f"{BASE_URL}/client/cart/view-cart", headers=HEADERS)
    assert resp.status_code in [200, 201], f"Не удалось получить корзину, статус: {resp.status_code}"
    print("Корзина успешно получена (200/201)")

    cart_data = resp.json()
    # print("Ответ сервера (корзина):")
    # print(cart_data)

    moderated_cart_items = cart_data.get("moderated_cart_items", [])
    assert len(moderated_cart_items) > 0, "Корзина пуста!"
    print(f"В корзине найдено {len(moderated_cart_items)} товаров")

    found_item = next(
        (item for item in moderated_cart_items if item.get("moderated_offer_id") == added_moderated_offer_id),
        None
    )

    assert found_item, f"Товар '{expected_product_name}' не найден в корзине"
    print(f"Товар '{found_item.get('name')}' найден в корзине")
