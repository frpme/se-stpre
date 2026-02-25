from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PartPrice:
    model: str
    issue_id: str
    purchase_price: float


# MVP-словарь для расчета. Можно заменить интеграцией с API/парсингом moba.ru.
MOBA_PRICE_CACHE: dict[tuple[str, str], float] = {
    ("iPhone 11", "display"): 5300,
    ("iPhone 11", "battery"): 2400,
    ("iPhone 11", "camera"): 3000,
    ("iPhone 12", "display"): 6900,
    ("iPhone 12", "battery"): 2900,
    ("iPhone 12", "charge"): 2800,
    ("iPhone 13", "display"): 8400,
    ("iPhone 13", "battery"): 3300,
    ("iPhone 13", "speaker"): 2500,
}


def get_purchase_price(model: str, issue_id: str) -> PartPrice | None:
    price = MOBA_PRICE_CACHE.get((model, issue_id))
    if price is None:
        return None
    return PartPrice(model=model, issue_id=issue_id, purchase_price=price)
