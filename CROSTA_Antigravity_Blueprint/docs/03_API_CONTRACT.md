# 03. Спецификация REST API (v2.0)

Базовый URL: `http://localhost:5000/api` (или порт запуска `dotnet run`).

## 1. Аутентификация и профиль
- `POST /api/auth/register`
  - Body: `{ "email", "password", "fullName", "phone", "defaultAddress" }`
  - Валидация: уникальный Email, пароль >= 6 символов. Начисляет приветственный бонус `5.00` баллов в `BonusTransactions`.
  - Response `201 Created`: `UserProfileDto` (без `PasswordHash`).
- `POST /api/auth/login`
  - Body: `{ "email", "password" }`
  - Response `200 OK`: `UserProfileDto` | `401 Unauthorized`: `{ "error": "Неверный email или пароль." }`.
- `GET /api/profile/{userId}`
  - Response `200 OK`: `{ user: UserProfileDto, bonusHistory: BonusTransactionDto[], orders: OrderDetailDto[] }`.
- `PUT /api/profile/{userId}`
  - Body: `{ "fullName", "phone", "defaultAddress" }`
  - Response `200 OK`: обновлённый `UserProfileDto`.

## 2. Акции и меню
- `GET /api/promotions` — список активных акций и новостей (`IsActive = 1`).
- `GET /api/menu?category=&search=` — список пицц.
- `POST /api/menu` — создание новой пиццы (для `Admin`).
- `PATCH /api/menu/{id}/availability` — скрытие/возврат позиции в стоп-лист (для `Admin`).

## 3. Заказы и аналитика администратора
- `POST /api/orders`
  - Расширенный Body: включает опциональные `userId` (`int?`) и `bonusToSpend` (`decimal`).
  - Проверяет GDPR-чекбокс, лимит списания бонусов (<= 30% от суммы блюд и <= `User.BonusBalance`), атомарно списывает и начисляет новые бонусы (5%).
- `GET /api/admin/stats`
  - Response `200 OK`:
    ```json
    {
      "totalOrders": 5,
      "activeOrders": 3,
      "grossRevenueEur": 140.27,
      "netRevenueEur": 127.52,
      "vatTotalEur": 12.75,
      "averageOrderValueEur": 28.05,
      "totalBonusIssued": 19.50,
      "totalBonusRedeemed": 4.20,
      "ordersByStatus": [
        { "status": "New", "count": 1 },
        { "status": "Baking", "count": 1 }
      ],
      "topPizzas": [
        { "pizzaName": "Маргарита DOC", "unitsSold": 4, "revenueEur": 38.00 }
      ]
    }
    ```
