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
@allure.feature("Изменение количества товара")
@allure.story("Обновление quantity")
def test_update_quantity():
    with allure.step("Получение корзины"):
        resp_cart = requests.get(f"{BASE_URL}/client/cart/view-cart", headers=HEADERS)
        assert resp_cart.status_code in [200, 201]
        cart_data = resp_cart.json()
        moderated_cart_items = cart_data.get("moderated_cart_items", [])
        assert moderated_cart_items, "Корзина пуста, нечего обновлять"

    item = moderated_cart_items[0]
    moderated_offer_id = item.get("moderated_offer_id")
    condition_id = item["loan_condition"]["id"] if "loan_condition" in item else item["condition"]["id"]
    current_quantity = item.get("quantity", 1)
    new_quantity = current_quantity + 1

    with allure.step(f"Обновление количества товара '{item['name']}' с {current_quantity} до {new_quantity}"):
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
        allure.attach(str(resp_update.json()), name="Ответ сервера", attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверка актуального количества товара в корзине"):
        resp_cart_check = requests.get(f"{BASE_URL}/client/cart/view-cart", headers=HEADERS)
        updated_item = next((i for i in resp_cart_check.json().get("moderated_cart_items", [])
                             if i.get("moderated_offer_id") == moderated_offer_id), None)
        assert updated_item
        assert updated_item.get("quantity") == new_quantity
