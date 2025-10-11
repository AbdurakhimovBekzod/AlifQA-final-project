import os
import requests
import pytest
import allure
from conftest import BASE_URL, ACCESS_TOKEN, load_dotenv, HEADERS

@allure.epic("Товары")
@allure.feature("Список товаров")
@allure.story("Получение активных товаров")
@pytest.mark.products
def test_get_active_products():
    """Проверка получения активных товаров"""
    with allure.step("Запрос активных товаров"):
        url = f"{BASE_URL}/client/events/active"
        response = requests.get(url, headers=HEADERS)
        assert response.status_code == 200, f"Не удалось получить список товаров, статус: {response.status_code}"
        data = response.json()
        allure.attach(str(data), name="Ответ сервера", attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверка наличия хотя бы одного оффера"):
        offer = None
        for event in data:
            offer = next((o for o in event.get("offers", []) if o.get("moderated_offer_id")), None)
            if offer:
                break
        assert offer is not None, "Не найден оффер с moderated_offer_id"

    with allure.step("Проверка обязательных полей оффера"):
        required_fields = ["moderated_offer_id", "name", "price", "quantity", "condition"]
        missing_fields = [f for f in required_fields if f not in offer]
        assert not missing_fields, f"Отсутствуют поля: {missing_fields}"

    with allure.step("Вывод выбранного оффера"):
        product_info = {
            "moderated_offer_id": offer["moderated_offer_id"],
            "name": offer["name"],
            "price": offer["price"],
            "quantity": offer["quantity"],
            "condition_id": offer["condition"]["id"]
        }
        print(f"Товар выбран: {product_info['name']} ({product_info['price']} сум)")
        allure.attach(str(product_info), name="Выбранный товар", attachment_type=allure.attachment_type.JSON)
