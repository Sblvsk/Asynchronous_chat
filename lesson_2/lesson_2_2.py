import json


def write_order_to_json(item, quantity, price, buyer, date):
    with open('orders.json') as f:
        order = {
            "item": item,
            "quantity": quantity,
            "price": price,
            "buyer": buyer,
            "date": date
        }

        json_file = json.load(f)
        json_file['orders'].append(order)


    with open('orders.json', 'w') as f:
        json.dump(json_file, f, indent=4)


write_order_to_json("Book", 1, 1000, "Ivan", "2023-02-22")



