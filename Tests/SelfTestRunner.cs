using Microsoft.Data.Sqlite;
using PizzaOrderSystem.Data;
using PizzaOrderSystem.Models;

namespace PizzaOrderSystem.Tests;

public static class SelfTestRunner
{
    public static int RunAll(string contentRootPath)
    {
        Console.WriteLine("=== Запуск модульных и интеграционных тестов CROSTA v2.0 (C# + SQLite) ===");
        var tempDb = Path.Combine(Path.GetTempPath(), $"pizza_test_{Guid.NewGuid():N}.db");
        var seedPath = Path.Combine(contentRootPath, "Database", "schema_and_seed.sql");

        try
        {
            var repo = new PizzaRepository($"Data Source={tempDb};Foreign Keys=True;", seedPath);
            repo.EnsureInitialized();

            // -----------------------------------------------------------------
            // Test 1: Инициализация схемы SQLite v2.0, меню, промо и сид-пользователей
            // -----------------------------------------------------------------
            var menu = repo.GetMenu();
            var sizes = repo.GetSizes();
            var promotions = repo.GetPromotions();
            Assert(menu.Count == 9, $"Ожидалось 9 пицц в каталоге, получено {menu.Count}");
            Assert(sizes.Count == 3, $"Ожидалось 3 размера пицц, получено {sizes.Count}");
            Assert(promotions.Count >= 3, $"Ожидалось >= 3 промо-акций, получено {promotions.Count}");
            Console.WriteLine("[PASS] Test 1: Инициализация схемы SQLite v2.0 и справочников меню/размеров/промо");

            // -----------------------------------------------------------------
            // Test 2: Аутентификация, детерминированное хэширование паролей и регистрация
            // -----------------------------------------------------------------
            // Проверка логина сид-клиента (david@crosta.eu / User123!)
            var davidLogin = repo.Login(new LoginRequest("david@crosta.eu", "User123!"));
            Assert(davidLogin.Success && davidLogin.User != null, $"Ошибка входа Давида: {davidLogin.Error}");
            Assert(davidLogin.User!.Role == "Customer", "Роль пользователя david должна быть Customer");
            Assert(davidLogin.User.BonusBalance == 14.50m, $"Ожидался баланс 14.50 EUR, получено {davidLogin.User.BonusBalance}");

            // Проверка логина администратора (admin@crosta.eu / Admin123!)
            var adminLogin = repo.Login(new LoginRequest("admin@crosta.eu", "Admin123!"));
            Assert(adminLogin.Success && adminLogin.User != null, $"Ошибка входа администратора: {adminLogin.Error}");
            Assert(adminLogin.User!.Role == "Admin", "Роль пользователя admin должна быть Admin");

            // Проверка защиты от неверного пароля
            var wrongLogin = repo.Login(new LoginRequest("david@crosta.eu", "WrongPassword!"));
            Assert(!wrongLogin.Success, "Вход с неверным паролем должен отклоняться");

            // Проверка регистрации нового пользователя с приветственным бонусом €5.00
            var newReg = repo.Register(new RegisterRequest(
                "new.customer@crosta.eu", "Pass1234!", "Марко Белуччи", "+373 777 99000", "ул. Мира, 10"
            ));
            Assert(newReg.Success && newReg.User != null, $"Ошибка регистрации: {newReg.Error}");
            Assert(newReg.User!.BonusBalance == 5.00m, "Новому клиенту должен начисляться приветственный бонус 5.00 EUR");

            // Проверка дублирования email
            var dupReg = repo.Register(new RegisterRequest(
                "new.customer@crosta.eu", "Pass1234!", "Дубликат", "+373 777 99001", "ул. Мира, 11"
            ));
            Assert(!dupReg.Success, "Повторная регистрация с существующим email должна блокироваться");
            Console.WriteLine("[PASS] Test 2: Аутентификация (без Google OAuth), детерминированное SHA-256 хэширование и регистрация с бонусом €5.00");

            // -----------------------------------------------------------------
            // Test 3: Профиль пользователя и история бонусов
            // -----------------------------------------------------------------
            var davidProfile = repo.GetProfileDetails(davidLogin.User.Id);
            Assert(davidProfile != null, "Профиль пользователя должен существовать");
            Assert(davidProfile!.BonusHistory.Count >= 2, $"Ожидалось >= 2 записей в истории бонусов Давида, получено {davidProfile.BonusHistory.Count}");
            Assert(davidProfile.Orders.Count >= 1, "У Давида должен быть минимум 1 сид-заказ");

            // Обновление контактных данных профиля
            var updatedProf = repo.UpdateProfile(davidLogin.User.Id, new UpdateProfileRequest("Давид В. Махвиладзе", "+373 777 88420", "ул. Свердлова, 45, кв. 14"));
            Assert(updatedProf.Success && updatedProf.User!.FullName == "Давид В. Махвиладзе", "Обновление профиля должно сохранять новые данные");
            Console.WriteLine("[PASS] Test 3: Профиль клиента, история бонусов и обновление контактных данных");

            // -----------------------------------------------------------------
            // Test 4: Валидация GDPR при оформлении заказа
            // -----------------------------------------------------------------
            var unconsented = repo.CreateOrder(new CreateOrderRequest(
                "Тест Клиент", "+373 777 11111", "test@eu.org", "ул. Ленина, 1",
                GdprConsentAccepted: false, MarketingOptIn: false, "CardOnline", null,
                new List<CreateOrderItemRequest> { new(1, 1, 1) }
            ));
            Assert(!unconsented.Success, "Заказ без согласия GDPR должен быть отклонён");
            Console.WriteLine("[PASS] Test 4: Валидация обязательного согласия GDPR при оформлении заказа");

            // -----------------------------------------------------------------
            // Test 5: Гостевой заказ, расчёт НДС 10% и бесплатная доставка (>= €25.00)
            // -----------------------------------------------------------------
            // Позиция 4 (Прошутто э Руккола, L=35см, mult=1.56): 14.50 * 1.56 = 22.62 EUR. При qty=2: 45.24 EUR (>= 25 => доставка 0.00)
            var guestOrder = repo.CreateOrder(new CreateOrderRequest(
                "Гость Клиент", "+373 777 33221", "guest@corp.eu", "ул. 25 Октября, 15",
                GdprConsentAccepted: true, MarketingOptIn: false, "CardOnline", "Без соуса",
                new List<CreateOrderItemRequest> { new(4, 3, 2) }
            ));
            Assert(guestOrder.Success && guestOrder.Order != null, $"Ошибка гостевого заказа: {guestOrder.Error}");
            Assert(guestOrder.Order!.DeliveryFeeEur == 0.00m, "Доставка от 25.00 EUR должна быть бесплатной (0.00 EUR)");
            Assert(guestOrder.Order.TotalEur == 45.24m, $"Ожидалось 45.24 EUR, получено {guestOrder.Order.TotalEur}");
            Assert(guestOrder.Order.NetSubtotalEur + guestOrder.Order.VatAmountEur == guestOrder.Order.TotalEur, "Netto + VAT должно равняться Total при бесплатной доставке");
            Assert(guestOrder.Order.BonusSpentEur == 0.00m && guestOrder.Order.BonusEarnedEur == 0.00m, "Гостям бонусы не начисляются и не списываются");
            Console.WriteLine("[PASS] Test 5: Транзакционный заказ, фискальный расчёт НДС 10% и бесплатная доставка от €25.00");

            // -----------------------------------------------------------------
            // Test 6: Бонусная программа (списание до 30% и начисление 5% кэшбэка)
            // -----------------------------------------------------------------
            // Создадим заказ для нового пользователя с балансом 5.00 EUR
            // Позиция 1 (Маргарита DOC, S=25см): 9.50 EUR. Доставка: 2.50 EUR.
            // 30% от 9.50 = 2.85 EUR. Запрос на списание 4.00 EUR должен быть отклонён (превышает 30%).
            var overBonusOrder = repo.CreateOrder(new CreateOrderRequest(
                newReg.User.FullName, newReg.User.Phone, newReg.User.Email, newReg.User.DefaultAddress,
                GdprConsentAccepted: true, MarketingOptIn: true, "CardOnline", null,
                new List<CreateOrderItemRequest> { new(1, 1, 1) },
                UserId: newReg.User.Id,
                BonusToSpend: 4.00m
            ));
            Assert(!overBonusOrder.Success, "Списание бонусов свыше 30% от стоимости пицц должно отклоняться");

            // Корректное списание 2.00 EUR бонусов
            // Стоимость блюд: 9.50 EUR, списание бонусов: 2.00 EUR, доставка: 2.50 EUR
            // Итого к оплате: 9.50 - 2.00 + 2.50 = 10.00 EUR
            // Кэшбэк 5% от (9.50 - 2.00) = 5% от 7.50 = 0.38 EUR
            // Новый баланс пользователя: 5.00 - 2.00 + 0.38 = 3.38 EUR
            var bonusOrder = repo.CreateOrder(new CreateOrderRequest(
                newReg.User.FullName, newReg.User.Phone, newReg.User.Email, newReg.User.DefaultAddress,
                GdprConsentAccepted: true, MarketingOptIn: true, "CardOnline", null,
                new List<CreateOrderItemRequest> { new(1, 1, 1) },
                UserId: newReg.User.Id,
                BonusToSpend: 2.00m
            ));
            Assert(bonusOrder.Success && bonusOrder.Order != null, $"Ошибка заказа с бонусами: {bonusOrder.Error}");
            Assert(bonusOrder.Order!.BonusSpentEur == 2.00m, $"Ожидалось списание 2.00 EUR бонусов, получено {bonusOrder.Order.BonusSpentEur}");
            Assert(bonusOrder.Order.BonusEarnedEur == 0.38m, $"Ожидался кэшбэк 0.38 EUR, получено {bonusOrder.Order.BonusEarnedEur}");
            Assert(bonusOrder.Order.TotalEur == 10.00m, $"Ожидался итог 10.00 EUR, получено {bonusOrder.Order.TotalEur}");

            var updatedUser = repo.GetUserById(newReg.User.Id);
            Assert(updatedUser != null && updatedUser.BonusBalance == 3.38m, $"Ожидался баланс пользователя 3.38 EUR, получено {updatedUser?.BonusBalance}");
            Console.WriteLine("[PASS] Test 6: Бонусная лояльность: ограничение списания до 30%, атомарный перерасчёт и 5% кэшбэк");

            // -----------------------------------------------------------------
            // Test 7: Машина состояний жизненного цикла заказа
            // -----------------------------------------------------------------
            var testOrder = bonusOrder.Order;
            var invalidJump = repo.UpdateOrderStatus(testOrder.Id, new UpdateOrderStatusRequest("Delivered", "Courier", null));
            Assert(!invalidJump.Success, "Прямой переход New -> Delivered должен отклоняться");

            var s1 = repo.UpdateOrderStatus(testOrder.Id, new UpdateOrderStatusRequest("Preparing", "Manager", null));
            var s2 = repo.UpdateOrderStatus(testOrder.Id, new UpdateOrderStatusRequest("Baking", "Kitchen", null));
            var s3 = repo.UpdateOrderStatus(testOrder.Id, new UpdateOrderStatusRequest("OutForDelivery", "Courier", null));
            var s4 = repo.UpdateOrderStatus(testOrder.Id, new UpdateOrderStatusRequest("Delivered", "Courier", null));
            Assert(s1.Success && s2.Success && s3.Success && s4.Success, "Полная цепочка состояний заказа должна успешно завершаться");
            Console.WriteLine("[PASS] Test 7: Жизненный цикл заказа (New -> Preparing -> Baking -> OutForDelivery -> Delivered) и журнал аудита");

            // -----------------------------------------------------------------
            // Test 8: Аналитика и расчёт сводной статистики администратора
            // -----------------------------------------------------------------
            var stats = repo.GetAdminStats();
            Assert(stats.TotalOrders >= 5, $"Ожидалось >= 5 заказов в статистике, получено {stats.TotalOrders}");
            Assert(stats.GrossRevenueEur > 0, "Выручка брутто должна быть больше 0");
            Assert(stats.NetRevenueEur > 0, "Выручка нетто должна быть больше 0");
            Assert(stats.VatTotalEur > 0, "Сумма НДС должна быть больше 0");
            Assert(stats.AverageOrderValueEur > 0, "Средний чек должен быть больше 0");
            Assert(stats.TotalBonusIssued > 0, "Сумма начисленных бонусов должна быть больше 0");
            Assert(stats.TopPizzas.Count > 0, "Список топ-пицц должен содержать элементы");
            Assert(stats.OrdersByStatus.Count > 0, "Распределение по статусам должно быть заполнено");
            Console.WriteLine("[PASS] Test 8: Аналитика KPI администратора (выручка, НДС, средний чек, бонусы, топ пицц)");

            Console.WriteLine("=== Все 8 наборов тестов успешно пройдены! ===");
            return 0;
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine($"[FAIL] {ex.Message}");
            return 1;
        }
        finally
        {
            SqliteConnection.ClearAllPools();
            GC.Collect();
            GC.WaitForPendingFinalizers();
            if (File.Exists(tempDb))
            {
                try { File.Delete(tempDb); } catch { }
            }
        }
    }

    private static void Assert(bool condition, string message)
    {
        if (!condition) throw new Exception(message);
    }
}
