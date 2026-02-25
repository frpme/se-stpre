def calculate_final_price(
    purchase_price: float,
    markup_percent: float,
    service_cost: float,
) -> float:
    if purchase_price < 0:
        raise ValueError("purchase_price must be >= 0")
    if service_cost < 0:
        raise ValueError("service_cost must be >= 0")
    if markup_percent < 0:
        raise ValueError("markup_percent must be >= 0")

    markup_value = purchase_price * markup_percent / 100
    final_price = purchase_price + markup_value + service_cost
    return round(final_price, 2)
