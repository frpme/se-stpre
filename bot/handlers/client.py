from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.config import load_settings
from bot.data.catalog import get_issue, get_issues_for_model, get_models
from bot.services.moba_provider import get_purchase_price
from bot.services.pricing import calculate_final_price

router = Router()


class RepairFlow(StatesGroup):
    waiting_for_model = State()
    waiting_for_issue = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    kb = InlineKeyboardBuilder()
    for model in get_models():
        kb.button(text=model, callback_data=f"model:{model}")
    kb.adjust(1)
    await state.set_state(RepairFlow.waiting_for_model)
    await message.answer(
        "Привет! Я помогу рассчитать стоимость ремонта для se:Store.\nВыберите модель:",
        reply_markup=kb.as_markup(),
    )


@router.callback_query(F.data.startswith("model:"), RepairFlow.waiting_for_model)
async def select_model(callback: CallbackQuery, state: FSMContext) -> None:
    model = callback.data.split(":", maxsplit=1)[1]
    issues = get_issues_for_model(model)

    if not issues:
        await callback.message.answer("Для выбранной модели пока нет доступных неисправностей.")
        await callback.answer()
        return

    kb = InlineKeyboardBuilder()
    for issue in issues:
        kb.button(text=issue.title, callback_data=f"issue:{issue.id}")
    kb.adjust(1)

    await state.update_data(model=model)
    await state.set_state(RepairFlow.waiting_for_issue)
    await callback.message.answer(f"Модель: <b>{model}</b>\nВыберите неисправность:", reply_markup=kb.as_markup())
    await callback.answer()


@router.callback_query(F.data.startswith("issue:"), RepairFlow.waiting_for_issue)
async def select_issue(callback: CallbackQuery, state: FSMContext) -> None:
    settings = load_settings()
    issue_id = callback.data.split(":", maxsplit=1)[1]
    data = await state.get_data()
    model = data.get("model")

    if not model:
        await callback.message.answer("Сессия истекла. Нажмите /start и начните заново.")
        await state.clear()
        await callback.answer()
        return

    issue = get_issue(model, issue_id)
    if issue is None:
        await callback.message.answer("Неисправность не найдена. Попробуйте снова через /start.")
        await state.clear()
        await callback.answer()
        return

    part_price = get_purchase_price(model, issue_id)
    if part_price is None:
        await callback.message.answer("Не удалось получить закупочную цену. Уточните у менеджера se:Store.")
        await state.clear()
        await callback.answer()
        return

    service_cost = issue.service_cost if issue.service_cost is not None else settings.service_cost
    final_price = calculate_final_price(
        purchase_price=part_price.purchase_price,
        markup_percent=settings.markup_percent,
        service_cost=service_cost,
    )

    await callback.message.answer(
        "<b>Итоговый расчет</b>\n"
        f"Модель: {model}\n"
        f"Неисправность: {issue.title}\n"
        f"Закупка: {part_price.purchase_price:.2f} ₽\n"
        f"Наценка: {settings.markup_percent:.1f}%\n"
        f"Работа: {service_cost:.2f} ₽\n"
        f"<b>Итого: {final_price:.2f} ₽</b>"
    )
    await state.clear()
    await callback.answer()
