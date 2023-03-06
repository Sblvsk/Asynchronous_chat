import json


def write_order_to_json(item, quantity, price, buyer, date):
    order = {
        "item": item,
        "quantity": quantity,
        "price": price,
        "buyer": buyer,
        "date": date
    }

    with open("orders.json", "a") as f:
        json.dump(order, f, indent=4)


write_order_to_json("Книга", 1, 1000, "Иванов Иван", "2023-02-22")
