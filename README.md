# se:Store Repair Calculator Bot

MVP Telegram-бот для расчета стоимости ремонта:
1. Клиент выбирает модель.
2. Клиент выбирает неисправность.
3. Бот получает закупочную цену (MVP: локальный кэш, точка расширения для moba.ru).
4. Бот применяет наценку + стоимость услуги и показывает итоговую цену.

## Как запустить

### 1) Требования
- Python 3.11+
- Telegram Bot Token (получить у [@BotFather](https://t.me/BotFather))

### 2) Установка

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3) Настройка окружения

```bash
cp .env.example .env
```

Откройте `.env` и заполните минимум `BOT_TOKEN`.

Пример:
```env
BOT_TOKEN=123456:ABCDEF...
MARKUP_PERCENT=35
SERVICE_COST=1500
ADMIN_IDS=123456789,987654321
```

### 4) Запуск бота

```bash
python main.py
```

Если всё ок, бот начнет polling Telegram API. После этого в Telegram отправьте боту команду `/start`.

## Проверка, что всё работает

```bash
python -m pytest -q
```

Ожидаемо: `4 passed`.

## Частые проблемы

- `ValueError: BOT_TOKEN is required in environment`
  - Не заполнен `BOT_TOKEN` в `.env`.
- Бот не отвечает в Telegram
  - Проверьте, что процесс `python main.py` запущен и токен корректный.
- Ошибка установки зависимостей
  - Обновите pip: `python -m pip install --upgrade pip` и повторите `pip install -r requirements.txt`.

## Переменные окружения

- `BOT_TOKEN` — токен Telegram-бота.
- `MARKUP_PERCENT` — наценка в процентах (по умолчанию 35).
- `SERVICE_COST` — базовая стоимость услуги (по умолчанию 1500).
- `ADMIN_IDS` — список id админов через запятую (MVP-резерв).

## Где менять бизнес-логику

- Каталог моделей/неисправностей: `bot/data/catalog.py`
- Закупочные цены (MVP): `bot/services/moba_provider.py`
- Формула расчета: `bot/services/pricing.py`
