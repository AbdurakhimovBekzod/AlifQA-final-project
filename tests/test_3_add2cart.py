import os
import requests
from dotenv import load_dotenv
import pytest
import allure

load_dotenv()
BASE_URL = os.getenv("BASE_URL")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

@pytest.fixture
def product_to_add():
    with allure.step("Получение первого активного товара для добавления в корзину"):
        resp = requests.get(f"{BASE_URL}/client/events/active", headers=HEADERS)
        assert resp.status_code == 200
        data = resp.json()
        offer = data[0]["offers"][0]
        return offer

@allure.epic("Корзина")
@allure.feature("Добавление товара")
@allure.story("Добавление товара в корзину")
def test_add_to_cart(product_to_add):
    with allure.step(f"Добавление товара '{product_to_add['name']}' в корзину"):
        payload = {
            "moderated_offer_id": product_to_add["moderated_offer_id"],
            "condition_id": product_to_add["condition"]["id"],
            "quantity": 1
        }
        resp = requests.post(f"{BASE_URL}/client/cart/authenticated/moderated-items",
                             json=payload, headers=HEADERS)

        if resp.status_code in [200, 201]:
            print(f"Товар добавлен: {product_to_add['name']}")
        elif resp.status_code == 409:
            print("Достигнуто максимальное количество товара в корзине")
        else:
            assert False, f"Ошибка при добавлении товара: {resp.status_code}"

        allure.attach(str(resp.json()), name="Ответ сервера", attachment_type=allure.attachment_type.JSON)
