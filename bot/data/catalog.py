from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RepairIssue:
    id: str
    title: str
    service_cost: float | None = None


MODEL_ISSUES: dict[str, list[RepairIssue]] = {
    "iPhone 11": [
        RepairIssue(id="display", title="Разбит экран", service_cost=2500),
        RepairIssue(id="battery", title="Быстро разряжается", service_cost=1800),
        RepairIssue(id="camera", title="Не работает камера", service_cost=2200),
    ],
    "iPhone 12": [
        RepairIssue(id="display", title="Разбит экран", service_cost=2900),
        RepairIssue(id="battery", title="Быстро разряжается", service_cost=2000),
        RepairIssue(id="charge", title="Не заряжается", service_cost=2100),
    ],
    "iPhone 13": [
        RepairIssue(id="display", title="Разбит экран", service_cost=3200),
        RepairIssue(id="battery", title="Быстро разряжается", service_cost=2200),
        RepairIssue(id="speaker", title="Не работает динамик", service_cost=1900),
    ],
}


def get_models() -> list[str]:
    return list(MODEL_ISSUES.keys())


def get_issues_for_model(model: str) -> list[RepairIssue]:
    return MODEL_ISSUES.get(model, [])


def get_issue(model: str, issue_id: str) -> RepairIssue | None:
    for issue in get_issues_for_model(model):
        if issue.id == issue_id:
            return issue
    return None
