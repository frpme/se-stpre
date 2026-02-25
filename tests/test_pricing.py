import pytest

from bot.services.pricing import calculate_final_price


def test_calculate_final_price_ok() -> None:
    result = calculate_final_price(purchase_price=1000, markup_percent=30, service_cost=500)
    assert result == 1800


@pytest.mark.parametrize(
    "purchase_price,markup_percent,service_cost",
    [(-1, 20, 100), (100, -2, 100), (100, 20, -100)],
)
def test_calculate_final_price_validation(
    purchase_price: float,
    markup_percent: float,
    service_cost: float,
) -> None:
    with pytest.raises(ValueError):
        calculate_final_price(
            purchase_price=purchase_price,
            markup_percent=markup_percent,
            service_cost=service_cost,
        )
