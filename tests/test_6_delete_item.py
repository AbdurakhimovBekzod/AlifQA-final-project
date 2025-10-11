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
@allure.feature("Удаление товара")
@allure.story("Удаление товара из корзины")
def test_delete_item_from_cart():
    with allure.step("Получение корзины"):
        resp_cart = requests.get(f"{BASE_URL}/client/cart/view-cart", headers=HEADERS)
        assert resp_cart.status_code in [200, 201]
        cart_data = resp_cart.json()
        moderated_cart_items = cart_data.get("moderated_cart_items", [])

    if not moderated_cart_items:
        print("Корзина пуста, нечего удалять")
        return

    item = moderated_cart_items[0]
    moderated_offer_id = item.get("moderated_offer_id")
    product_name = item.get("name", "Неизвестный товар")

    with allure.step(f"Удаление товара '{product_name}' из корзины"):
        resp_delete = requests.delete(
            f"{BASE_URL}/client/cart/authenticated/moderated-items/{moderated_offer_id}",
            headers=HEADERS
        )
        assert resp_delete.status_code in [200, 204]
        allure.attach(str(resp_delete.json() if resp_delete.content else {}), name="Ответ сервера", attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверка, что товар удалён"):
        resp_cart_check = requests.get(f"{BASE_URL}/client/cart/view-cart", headers=HEADERS)
        remaining_item = next((i for i in resp_cart_check.json().get("moderated_cart_items", [])
                               if i.get("moderated_offer_id") == moderated_offer_id), None)
        assert remaining_item is None
        print(f"Товар '{product_name}' отсутствует в корзине")
