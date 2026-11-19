# ЭТАП 1: Бэкенд C#, SQLite v2.0, Авторизация (без Google), Бонусы и Автотесты

Опираясь на спецификации в `CROSTA_Antigravity_Blueprint/docs/01_SRS_AND_BUSINESS_RULES.md`, `02_DB_SCHEMA_V2.md` и `03_API_CONTRACT.md`:
1. Обнови `Database/schema_and_seed.sql`:
   - Добавь таблицы `Users`, `BonusTransactions`, `Promotions` и новые поля в `Orders` (`UserId`, `BonusSpentEur`, `BonusEarnedEur`).
   - Добавь тестовые аккаунты `david@crosta.eu` / `User123!` (с балансом `14.50` бонусов и историей) и `admin@crosta.eu` / `Admin123!`, а также 3 промо-акции для главной страницы.
2. Обнови `Models/DomainModels.cs`, `Data/PizzaRepository.cs` и `Program.cs`:
   - Реализуй регистрацию (`POST /api/auth/register` с приветственным бонусом `5.00`), вход (`POST /api/auth/login`), просмотр и обновление профиля (`GET/PUT /api/profile/{userId}`), список акций (`GET /api/promotions`) и статистику администратора (`GET /api/admin/stats`).
   - Обнови `CreateOrder`: поддержи списание бонусов (до 30% от суммы блюд) и начисление кэшбэка 5% для авторизованных клиентов.
3. Обнови `Tests/SelfTestRunner.cs`, добавив автотесты для регистрации, входа, начисления/списания бонусов и расчёта статистики администратора.
4. Удали старый `pizza_orders.db` и запусти `dotnet run -- --test`. Убедись, что все тесты проходят со статусом `[PASS]`.
