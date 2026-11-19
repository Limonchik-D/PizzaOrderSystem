# 02. Схема базы данных SQLite (v2.0)

При обновлении схемы удали старый файл `pizza_orders.db`, чтобы `PizzaRepository.EnsureInitialized()` пересоздал базу из обновлённого `Database/schema_and_seed.sql`.

## Новые и обновлённые таблицы

```sql
-- Пользователи (Клиенты и Администраторы, без Google OAuth)
CREATE TABLE Users (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Email TEXT NOT NULL UNIQUE,
    PasswordHash TEXT NOT NULL,
    FullName TEXT NOT NULL,
    Phone TEXT NOT NULL,
    DefaultAddress TEXT NOT NULL,
    Role TEXT NOT NULL CHECK (Role IN ('Customer', 'Admin')),
    BonusBalance REAL NOT NULL DEFAULT 0.00 CHECK (BonusBalance >= 0),
    CreatedAtUtc TEXT NOT NULL
);

-- Журнал бонусных операций
CREATE TABLE BonusTransactions (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    UserId INTEGER NOT NULL,
    OrderNumber TEXT NULL,
    Type TEXT NOT NULL CHECK (Type IN ('Accrual', 'Redemption', 'WelcomeBonus')),
    DeltaAmount REAL NOT NULL,
    Description TEXT NOT NULL,
    CreatedAtUtc TEXT NOT NULL,
    FOREIGN KEY (UserId) REFERENCES Users(Id) ON DELETE CASCADE
);

-- Акции и новости для главной страницы
CREATE TABLE Promotions (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Badge TEXT NOT NULL,
    Title TEXT NOT NULL,
    Subtitle TEXT NOT NULL,
    PromoCode TEXT NULL,
    ValidUntil TEXT NOT NULL,
    TargetCategory TEXT NULL,
    IsActive INTEGER NOT NULL DEFAULT 1
);
```

## Изменения в таблице `Orders`
Добавить колонки:
- `UserId INTEGER NULL REFERENCES Users(Id)`
- `BonusSpentEur REAL NOT NULL DEFAULT 0.00`
- `BonusEarnedEur REAL NOT NULL DEFAULT 0.00`

## Обязательные тестовые аккаунты (Seed Data)
1. **Клиент:**
   - Email: `david@crosta.eu`
   - Пароль: `User123!`
   - Имя: `Давид Махвиладзе`
   - Телефон: `+373 777 88420`
   - Адрес: `ул. Свердлова, 45, кв. 12`
   - Стартовый баланс бонусов: `14.50` (с 2 записями в `BonusTransactions` и привязанными заказами).
2. **Администратор:**
   - Email: `admin@crosta.eu`
   - Пароль: `Admin123!`
   - Имя: `Елена Ковальчук`
   - Роль: `Admin`

## Промо-блоки для таблицы `Promotions` (Seed Data)
1. `АКЦИЯ ЕС` — **Бесплатная курьерская доставка от €25.00** (Электродоставка в термосумках за 35 минут).
2. `БОНУСЫ 2X` — **Двойной кэшбэк 10% по будням (12:00–15:00)** (Оплачивайте бонусами до 30% следующих заказов).
3. `НОВОЕ В МЕНЮ` — **Тесто 48-часовой ферментации на закваске Lievito Madre** (Попробуйте «Трюфельную с лесными грибами» и «Карбонара Аль Форно»).
