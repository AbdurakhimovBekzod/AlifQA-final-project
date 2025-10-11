import os
import requests
from dotenv import load_dotenv
import allure

load_dotenv()
BASE_URL = os.getenv("BASE_URL")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

@allure.epic("Корзина")
@allure.feature("Проверка корзины")
@allure.story("Проверка добавленного товара")
def test_view_cart():
    added_moderated_offer_id = "7f3e05ba-97cf-4e93-859b-2baae464e8f7"
    expected_product_name = "Смартфон Apple iPhone 16 Pro Max 256 ГБ (eSIM/nano SIM), Пустынный Титан"

    with allure.step("Получение содержимого корзины"):
        resp = requests.get(f"{BASE_URL}/client/cart/view-cart", headers=HEADERS)
        assert resp.status_code in [200, 201], f"Не удалось получить корзину, статус: {resp.status_code}"
        cart_data = resp.json()
        allure.attach(str(cart_data), name="Содержимое корзины", attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверка наличия товаров в корзине"):
        moderated_cart_items = cart_data.get("moderated_cart_items", [])
        assert len(moderated_cart_items) > 0, "Корзина пуста!"

    with allure.step("Проверка наличия конкретного товара"):
        found_item = next((item for item in moderated_cart_items
                           if item.get("moderated_offer_id") == added_moderated_offer_id), None)
        assert found_item, f"Товар '{expected_product_name}' не найден в корзине"
        print(f"Товар '{found_item.get('name')}' найден в корзине")
