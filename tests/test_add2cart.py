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


@pytest.fixture
def product_to_add():
    """Берем первый активный товар из списка товаров"""
    print("\n=== Шаг 1: Получение списка товаров ===")
    resp = requests.get(f"{BASE_URL}/client/events/active", headers=HEADERS)
    assert resp.status_code == 200, f"Не удалось получить список товаров, статус: {resp.status_code}"
    print("Запрос выполнен успешно!")

    data = resp.json()
    assert len(data) > 0, "Список товаров пуст"
    print(f"В ответе есть хотя бы один активный товар (найдено {len(data)} разделов)")

    offer = data[0]["offers"][0]
    assert offer.get("moderated_offer_id"), "Нет moderated_offer_id у оффера"
    print("Найден оффер с moderated_offer_id")

    # Печатаем детали выбранного товара
    product_name = offer["name"]
    price = offer["price"]
    moderated_offer_id = offer["moderated_offer_id"]
    condition_id = offer["condition"]["id"]

    print("Оффер содержит все нужные данные:")
    print(f"Название: {product_name}")
    print(f"Цена: {price}")
    # print(f"moderated_offer_id: {moderated_offer_id}")
    # print(f"condition_id: {condition_id}")
    print(f"Товар выбран: {product_name} ({price} сум)")

    return offer

def test_add_to_cart(product_to_add):
    """Добавление товара в корзину с обработкой ошибок"""
    print("\n=== Шаг 2: Добавление товара в корзину ===")
    payload = {
        "moderated_offer_id": product_to_add["moderated_offer_id"],
        "condition_id": product_to_add["condition"]["id"],
        "quantity": 1
    }

    resp = requests.post(f"{BASE_URL}/client/cart/authenticated/moderated-items",
                         json=payload, headers=HEADERS)

    try:
        assert resp.status_code in [200, 201], f"Товар не добавлен в корзину, статус: {resp.status_code}"
        print("Товар успешно добавлен в корзину")

    except AssertionError as e:
        # Обработка ошибок, например 409 Conflict
        if resp.status_code == 409:
            print(f"Ошибка: достигнуто максимальное количество товара в корзине")
            print("Ответ сервера:", resp.json())
        else:
            raise e

    else:
        # Если добавление прошло успешно, выводим детали товара
        json_data = resp.json()

        #print("Ответ от сервера после добавления товара:")
        # print(json_data)
        print('Сервер успешно возврашает ответ')
        # Берем первый элемент из cart_items или moderated_cart_items
        first_item = (json_data.get("cart_items") and json_data["cart_items"][0]) or \
                     (json_data.get("moderated_cart_items") and json_data["moderated_cart_items"][0])

        if first_item:
            product_name = first_item.get("name") or "Неизвестный товар"
            added_item_id = first_item.get("item_id") or first_item.get("id")
            added_moderated_offer_id = first_item.get("moderated_offer_id")

            print(f"'{product_name}' добавлен в корзину")
            # print(f"added_item_id: {added_item_id}")
            # print(f"added_moderated_offer_id: {added_moderated_offer_id}")
        else:
            print("Не найден объект товара в ответе")
