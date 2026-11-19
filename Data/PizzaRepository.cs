using System.Security.Cryptography;
using System.Text;
using Microsoft.Data.Sqlite;
using PizzaOrderSystem.Models;

namespace PizzaOrderSystem.Data;

public class PizzaRepository
{
    private readonly string _connectionString;
    private readonly string _seedSqlPath;

    public static readonly Dictionary<string, string[]> AllowedTransitions = new(StringComparer.OrdinalIgnoreCase)
    {
        ["New"] = new[] { "Preparing", "Cancelled" },
        ["Preparing"] = new[] { "Baking", "Cancelled" },
        ["Baking"] = new[] { "OutForDelivery", "Cancelled" },
        ["OutForDelivery"] = new[] { "Delivered", "Cancelled" },
        ["Delivered"] = Array.Empty<string>(),
        ["Cancelled"] = Array.Empty<string>()
    };

    public PizzaRepository(IConfiguration configuration, IWebHostEnvironment env)
    {
        var dbPath = Path.Combine(env.ContentRootPath, "pizza_orders.db");
        _connectionString = $"Data Source={dbPath};Foreign Keys=True;";
        _seedSqlPath = Path.Combine(env.ContentRootPath, "Database", "schema_and_seed.sql");
    }

    public PizzaRepository(string connectionString, string seedSqlPath)
    {
        _connectionString = connectionString;
        _seedSqlPath = seedSqlPath;
    }

    public static string HashPassword(string password)
    {
        using var sha256 = SHA256.Create();
        var bytes = Encoding.UTF8.GetBytes("crosta_salt_2026_" + password);
        var hash = sha256.ComputeHash(bytes);
        return Convert.ToHexString(hash).ToLowerInvariant();
    }

    public void EnsureInitialized()
    {
        using var connection = new SqliteConnection(_connectionString);
        connection.Open();

        using var checkCmd = connection.CreateCommand();
        checkCmd.CommandText = "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='Users';";
        var exists = Convert.ToInt64(checkCmd.ExecuteScalar()) > 0;

        if (!exists && File.Exists(_seedSqlPath))
        {
            var sql = File.ReadAllText(_seedSqlPath);
            using var seedCmd = connection.CreateCommand();
            seedCmd.CommandText = sql;
            seedCmd.ExecuteNonQuery();
        }
    }

    // =========================================================================
    // Аутентификация и управление пользователями
    // =========================================================================

    public (bool Success, string Error, UserProfileDto? User) Register(RegisterRequest req)
    {
        if (string.IsNullOrWhiteSpace(req.Email) || !req.Email.Contains('@'))
            return (false, "Укажите корректный адрес электронной почты.", null);

        if (string.IsNullOrWhiteSpace(req.Password) || req.Password.Length < 6)
            return (false, "Пароль должен содержать не менее 6 символов.", null);

        if (string.IsNullOrWhiteSpace(req.FullName) || string.IsNullOrWhiteSpace(req.Phone) || string.IsNullOrWhiteSpace(req.DefaultAddress))
            return (false, "Заполните все обязательные поля (ФИО, телефон, адрес).", null);

        using var connection = new SqliteConnection(_connectionString);
        connection.Open();
        using var tx = connection.BeginTransaction();

        try
        {
            using var checkCmd = connection.CreateCommand();
            checkCmd.Transaction = tx;
            checkCmd.CommandText = "SELECT COUNT(*) FROM Users WHERE LOWER(Email) = LOWER(@email);";
            checkCmd.Parameters.AddWithValue("@email", req.Email.Trim());
            if (Convert.ToInt64(checkCmd.ExecuteScalar()) > 0)
                return (false, "Пользователь с таким email уже зарегистрирован.", null);

            var nowIso = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ");
            var pwdHash = HashPassword(req.Password);

            using var insertCmd = connection.CreateCommand();
            insertCmd.Transaction = tx;
            insertCmd.CommandText = @"
                INSERT INTO Users (Email, PasswordHash, FullName, Phone, DefaultAddress, Role, BonusBalance, CreatedAtUtc)
                VALUES (@email, @pwd, @name, @phone, @addr, 'Customer', 5.00, @now);
                SELECT last_insert_rowid();";
            insertCmd.Parameters.AddWithValue("@email", req.Email.Trim().ToLowerInvariant());
            insertCmd.Parameters.AddWithValue("@pwd", pwdHash);
            insertCmd.Parameters.AddWithValue("@name", req.FullName.Trim());
            insertCmd.Parameters.AddWithValue("@phone", req.Phone.Trim());
            insertCmd.Parameters.AddWithValue("@addr", req.DefaultAddress.Trim());
            insertCmd.Parameters.AddWithValue("@now", nowIso);

            var userId = Convert.ToInt32(insertCmd.ExecuteScalar());

            // Приветственный бонус 5.00 баллов
            using var bonusCmd = connection.CreateCommand();
            bonusCmd.Transaction = tx;
            bonusCmd.CommandText = @"
                INSERT INTO BonusTransactions (UserId, OrderNumber, Type, DeltaAmount, Description, CreatedAtUtc)
                VALUES (@uid, NULL, 'WelcomeBonus', 5.00, 'Приветственный бонус при регистрации', @now);";
            bonusCmd.Parameters.AddWithValue("@uid", userId);
            bonusCmd.Parameters.AddWithValue("@now", nowIso);
            bonusCmd.ExecuteNonQuery();

            tx.Commit();

            var user = new UserProfileDto(
                userId, req.Email.Trim().ToLowerInvariant(), req.FullName.Trim(),
                req.Phone.Trim(), req.DefaultAddress.Trim(), "Customer", 5.00m, nowIso
            );
            return (true, string.Empty, user);
        }
        catch (Exception ex)
        {
            tx.Rollback();
            return (false, $"Ошибка регистрации: {ex.Message}", null);
        }
    }

    public (bool Success, string Error, UserProfileDto? User) Login(LoginRequest req)
    {
        if (string.IsNullOrWhiteSpace(req.Email) || string.IsNullOrWhiteSpace(req.Password))
            return (false, "Укажите email и пароль.", null);

        using var connection = new SqliteConnection(_connectionString);
        connection.Open();

        var hash = HashPassword(req.Password);
        using var cmd = connection.CreateCommand();
        cmd.CommandText = @"
            SELECT Id, Email, FullName, Phone, DefaultAddress, Role, BonusBalance, CreatedAtUtc
            FROM Users
            WHERE LOWER(Email) = LOWER(@email) AND PasswordHash = @hash;";
        cmd.Parameters.AddWithValue("@email", req.Email.Trim());
        cmd.Parameters.AddWithValue("@hash", hash);

        using var reader = cmd.ExecuteReader();
        if (!reader.Read())
            return (false, "Неверный email или пароль.", null);

        var user = new UserProfileDto(
            reader.GetInt32(0),
            reader.GetString(1),
            reader.GetString(2),
            reader.GetString(3),
            reader.GetString(4),
            reader.GetString(5),
            reader.GetDecimal(6),
            reader.GetString(7)
        );
        return (true, string.Empty, user);
    }

    public UserProfileDto? GetUserById(int userId)
    {
        using var connection = new SqliteConnection(_connectionString);
        connection.Open();

        using var cmd = connection.CreateCommand();
        cmd.CommandText = @"
            SELECT Id, Email, FullName, Phone, DefaultAddress, Role, BonusBalance, CreatedAtUtc
            FROM Users
            WHERE Id = @id;";
        cmd.Parameters.AddWithValue("@id", userId);

        using var reader = cmd.ExecuteReader();
        if (!reader.Read()) return null;

        return new UserProfileDto(
            reader.GetInt32(0),
            reader.GetString(1),
            reader.GetString(2),
            reader.GetString(3),
            reader.GetString(4),
            reader.GetString(5),
            reader.GetDecimal(6),
            reader.GetString(7)
        );
    }

    public (bool Success, string Error, UserProfileDto? User) UpdateProfile(int userId, UpdateProfileRequest req)
    {
        if (string.IsNullOrWhiteSpace(req.FullName) || string.IsNullOrWhiteSpace(req.Phone) || string.IsNullOrWhiteSpace(req.DefaultAddress))
            return (false, "Заполните все контактные данные.", null);

        using var connection = new SqliteConnection(_connectionString);
        connection.Open();

        using var cmd = connection.CreateCommand();
        cmd.CommandText = @"
            UPDATE Users 
            SET FullName = @name, Phone = @phone, DefaultAddress = @addr
            WHERE Id = @id;";
        cmd.Parameters.AddWithValue("@name", req.FullName.Trim());
        cmd.Parameters.AddWithValue("@phone", req.Phone.Trim());
        cmd.Parameters.AddWithValue("@addr", req.DefaultAddress.Trim());
        cmd.Parameters.AddWithValue("@id", userId);

        var affected = cmd.ExecuteNonQuery();
        if (affected == 0)
            return (false, "Пользователь не найден.", null);

        return (true, string.Empty, GetUserById(userId));
    }

    public ProfileDetailsDto? GetProfileDetails(int userId)
    {
        var user = GetUserById(userId);
        if (user == null) return null;

        using var connection = new SqliteConnection(_connectionString);
        connection.Open();

        // Бонусная история
        var bonusHistory = new List<BonusTransactionDto>();
        using (var bCmd = connection.CreateCommand())
        {
            bCmd.CommandText = @"
                SELECT Id, UserId, OrderNumber, Type, DeltaAmount, Description, CreatedAtUtc
                FROM BonusTransactions
                WHERE UserId = @uid
                ORDER BY Id DESC;";
            bCmd.Parameters.AddWithValue("@uid", userId);
            using var r = bCmd.ExecuteReader();
            while (r.Read())
            {
                bonusHistory.Add(new BonusTransactionDto(
                    r.GetInt32(0),
                    r.GetInt32(1),
                    r.IsDBNull(2) ? null : r.GetString(2),
                    r.GetString(3),
                    r.GetDecimal(4),
                    r.GetString(5),
                    r.GetString(6)
                ));
            }
        }

        var orders = GetOrders(null, userId);
        return new ProfileDetailsDto(user, bonusHistory, orders);
    }

    // =========================================================================
    // Промо-акции
    // =========================================================================

    public List<PromotionDto> GetPromotions()
    {
        using var connection = new SqliteConnection(_connectionString);
        connection.Open();

        using var cmd = connection.CreateCommand();
        cmd.CommandText = @"
            SELECT Id, Badge, Title, Subtitle, PromoCode, ValidUntil, TargetCategory, IsActive
            FROM Promotions
            WHERE IsActive = 1
            ORDER BY Id ASC;";

        var list = new List<PromotionDto>();
        using var r = cmd.ExecuteReader();
        while (r.Read())
        {
            list.Add(new PromotionDto(
                r.GetInt32(0),
                r.GetString(1),
                r.GetString(2),
                r.GetString(3),
                r.IsDBNull(4) ? null : r.GetString(4),
                r.GetString(5),
                r.IsDBNull(6) ? null : r.GetString(6),
                r.GetInt32(7) == 1
            ));
        }
        return list;
    }

    // =========================================================================
    // Меню и справочники
    // =========================================================================

    public List<PizzaDto> GetMenu(string? category = null, string? search = null)
    {
        using var connection = new SqliteConnection(_connectionString);
        connection.Open();

        var sql = @"SELECT Id, Sku, Name, Description, Ingredients, Category, DietaryTag, 
                           BasePriceEur, PrepMinutes, CaloriesKcal, IsAvailable
                    FROM Pizzas
                    WHERE IsAvailable = 1";

        using var cmd = connection.CreateCommand();
        if (!string.IsNullOrWhiteSpace(category) && !category.Equals("Все", StringComparison.OrdinalIgnoreCase))
        {
            sql += " AND Category = @category";
            cmd.Parameters.AddWithValue("@category", category.Trim());
        }
        if (!string.IsNullOrWhiteSpace(search))
        {
            sql += " AND (LOWER(Name) LIKE @q OR LOWER(Ingredients) LIKE @q)";
            cmd.Parameters.AddWithValue("@q", $"%{search.Trim().ToLowerInvariant()}%");
        }
        sql += " ORDER BY Id ASC;";
        cmd.CommandText = sql;

        var list = new List<PizzaDto>();
        using var reader = cmd.ExecuteReader();
        while (reader.Read())
        {
            list.Add(new PizzaDto(
                reader.GetInt32(0),
                reader.GetString(1),
                reader.GetString(2),
                reader.GetString(3),
                reader.GetString(4),
                reader.GetString(5),
                reader.GetString(6),
                reader.GetDecimal(7),
                reader.GetInt32(8),
                reader.GetInt32(9),
                reader.GetInt32(10) == 1
            ));
        }
        return list;
    }

    public List<PizzaDto> GetAllPizzasForAdmin()
    {
        using var connection = new SqliteConnection(_connectionString);
        connection.Open();

        using var cmd = connection.CreateCommand();
        cmd.CommandText = @"SELECT Id, Sku, Name, Description, Ingredients, Category, DietaryTag, 
                                   BasePriceEur, PrepMinutes, CaloriesKcal, IsAvailable
                            FROM Pizzas
                            ORDER BY Id ASC;";

        var list = new List<PizzaDto>();
        using var reader = cmd.ExecuteReader();
        while (reader.Read())
        {
            list.Add(new PizzaDto(
                reader.GetInt32(0),
                reader.GetString(1),
                reader.GetString(2),
                reader.GetString(3),
                reader.GetString(4),
                reader.GetString(5),
                reader.GetString(6),
                reader.GetDecimal(7),
                reader.GetInt32(8),
                reader.GetInt32(9),
                reader.GetInt32(10) == 1
            ));
        }
        return list;
    }

    public bool TogglePizzaAvailability(int pizzaId, bool? isAvailable = null)
    {
        using var connection = new SqliteConnection(_connectionString);
        connection.Open();

        using var cmd = connection.CreateCommand();
        if (isAvailable.HasValue)
        {
            cmd.CommandText = "UPDATE Pizzas SET IsAvailable = @avail WHERE Id = @id;";
            cmd.Parameters.AddWithValue("@avail", isAvailable.Value ? 1 : 0);
        }
        else
        {
            cmd.CommandText = "UPDATE Pizzas SET IsAvailable = 1 - IsAvailable WHERE Id = @id;";
        }
        cmd.Parameters.AddWithValue("@id", pizzaId);
        return cmd.ExecuteNonQuery() > 0;
    }

    public List<PizzaSizeDto> GetSizes()
    {
        using var connection = new SqliteConnection(_connectionString);
        connection.Open();

        using var cmd = connection.CreateCommand();
        cmd.CommandText = "SELECT Id, Code, Label, DiameterCm, WeightGrams, PriceMultiplier FROM PizzaSizes ORDER BY Id ASC;";

        var list = new List<PizzaSizeDto>();
        using var reader = cmd.ExecuteReader();
        while (reader.Read())
        {
            list.Add(new PizzaSizeDto(
                reader.GetInt32(0),
                reader.GetString(1),
                reader.GetString(2),
                reader.GetInt32(3),
                reader.GetInt32(4),
                reader.GetDecimal(5)
            ));
        }
        return list;
    }

    public List<StaffDto> GetStaff()
    {
        using var connection = new SqliteConnection(_connectionString);
        connection.Open();

        using var cmd = connection.CreateCommand();
        cmd.CommandText = "SELECT Id, FullName, Role, RoleDisplayRu, BadgeCode, IsActive FROM Staff WHERE IsActive = 1 ORDER BY Id ASC;";

        var list = new List<StaffDto>();
        using var reader = cmd.ExecuteReader();
        while (reader.Read())
        {
            list.Add(new StaffDto(
                reader.GetInt32(0),
                reader.GetString(1),
                reader.GetString(2),
                reader.GetString(3),
                reader.GetString(4),
                reader.GetInt32(5) == 1
            ));
        }
        return list;
    }

    // =========================================================================
    // Заказы и бонусная программа
    // =========================================================================

    public List<OrderDetailDto> GetOrders(string? status = null, int? userId = null)
    {
        using var connection = new SqliteConnection(_connectionString);
        connection.Open();

        var sql = @"SELECT o.Id, o.OrderNumber, o.UserId, c.FullName, c.Phone, c.Email, c.DeliveryAddress,
                           c.GdprConsentAccepted, c.MarketingOptIn, o.Status, o.PaymentMethod,
                           o.NetSubtotalEur, o.VatAmountEur, o.DeliveryFeeEur, o.BonusSpentEur, o.BonusEarnedEur, o.TotalEur,
                           o.CustomerComment, o.CreatedAtUtc, o.UpdatedAtUtc
                    FROM Orders o
                    INNER JOIN Customers c ON c.Id = o.CustomerId
                    WHERE 1=1";

        using var cmd = connection.CreateCommand();
        if (!string.IsNullOrWhiteSpace(status) && !status.Equals("All", StringComparison.OrdinalIgnoreCase))
        {
            sql += " AND o.Status = @status";
            cmd.Parameters.AddWithValue("@status", status.Trim());
        }
        if (userId.HasValue)
        {
            sql += " AND o.UserId = @uid";
            cmd.Parameters.AddWithValue("@uid", userId.Value);
        }
        sql += " ORDER BY o.Id DESC;";
        cmd.CommandText = sql;

        var orders = new List<OrderDetailDto>();
        using var reader = cmd.ExecuteReader();
        while (reader.Read())
        {
            var orderId = reader.GetInt32(0);
            orders.Add(new OrderDetailDto(
                orderId,
                reader.GetString(1),
                reader.IsDBNull(2) ? null : reader.GetInt32(2),
                reader.GetString(3),
                reader.GetString(4),
                reader.GetString(5),
                reader.GetString(6),
                reader.GetInt32(7) == 1,
                reader.GetInt32(8) == 1,
                reader.GetString(9),
                reader.GetString(10),
                reader.GetDecimal(11),
                reader.GetDecimal(12),
                reader.GetDecimal(13),
                reader.GetDecimal(14),
                reader.GetDecimal(15),
                reader.GetDecimal(16),
                reader.IsDBNull(17) ? null : reader.GetString(17),
                reader.GetString(18),
                reader.GetString(19),
                GetOrderItems(connection, orderId),
                GetOrderHistory(connection, orderId)
            ));
        }
        return orders;
    }

    public OrderDetailDto? GetOrderByNumber(string orderNumber)
    {
        return GetOrders().FirstOrDefault(o =>
            o.OrderNumber.Equals(orderNumber.Trim(), StringComparison.OrdinalIgnoreCase));
    }

    public (bool Success, string Error, OrderDetailDto? Order) CreateOrder(CreateOrderRequest req)
    {
        if (!req.GdprConsentAccepted)
            return (false, "Согласно регламенту ЕС (GDPR), необходимо подтвердить согласие на обработку персональных данных.", null);

        if (string.IsNullOrWhiteSpace(req.CustomerName) || string.IsNullOrWhiteSpace(req.CustomerPhone) ||
            string.IsNullOrWhiteSpace(req.CustomerEmail) || string.IsNullOrWhiteSpace(req.DeliveryAddress))
            return (false, "Заполните все обязательные контактные данные и адрес доставки.", null);

        if (req.Items == null || req.Items.Count == 0)
            return (false, "Корзина пуста. Добавьте хотя бы одну пиццу.", null);

        using var connection = new SqliteConnection(_connectionString);
        connection.Open();
        using var tx = connection.BeginTransaction();

        try
        {
            var nowIso = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ");

            using var custCmd = connection.CreateCommand();
            custCmd.Transaction = tx;
            custCmd.CommandText = @"
                INSERT INTO Customers (FullName, Phone, Email, DeliveryAddress, GdprConsentAccepted, MarketingOptIn, CreatedAtUtc)
                VALUES (@name, @phone, @email, @addr, 1, @mkt, @now);
                SELECT last_insert_rowid();";
            custCmd.Parameters.AddWithValue("@name", req.CustomerName.Trim());
            custCmd.Parameters.AddWithValue("@phone", req.CustomerPhone.Trim());
            custCmd.Parameters.AddWithValue("@email", req.CustomerEmail.Trim());
            custCmd.Parameters.AddWithValue("@addr", req.DeliveryAddress.Trim());
            custCmd.Parameters.AddWithValue("@mkt", req.MarketingOptIn ? 1 : 0);
            custCmd.Parameters.AddWithValue("@now", nowIso);
            var customerId = Convert.ToInt32(custCmd.ExecuteScalar());

            decimal grossItemsTotal = 0m;
            var computedLines = new List<(int PizzaId, int SizeId, int Qty, decimal UnitPrice, decimal LineTotal)>();

            foreach (var item in req.Items)
            {
                if (item.Quantity <= 0 || item.Quantity > 20)
                    return (false, "Количество каждой позиции должно быть от 1 до 20.", null);

                using var priceCmd = connection.CreateCommand();
                priceCmd.Transaction = tx;
                priceCmd.CommandText = @"
                    SELECT p.BasePriceEur, s.PriceMultiplier
                    FROM Pizzas p, PizzaSizes s
                    WHERE p.Id = @pid AND p.IsAvailable = 1 AND s.Id = @sid;";
                priceCmd.Parameters.AddWithValue("@pid", item.PizzaId);
                priceCmd.Parameters.AddWithValue("@sid", item.SizeId);

                using var r = priceCmd.ExecuteReader();
                if (!r.Read())
                    return (false, $"Некорректная позиция меню (PizzaId={item.PizzaId}, SizeId={item.SizeId}).", null);

                var basePrice = r.GetDecimal(0);
                var mult = r.GetDecimal(1);
                var unitPrice = Math.Round(basePrice * mult, 2, MidpointRounding.AwayFromZero);
                var lineTotal = Math.Round(unitPrice * item.Quantity, 2, MidpointRounding.AwayFromZero);
                grossItemsTotal += lineTotal;
                computedLines.Add((item.PizzaId, item.SizeId, item.Quantity, unitPrice, lineTotal));
            }

            // Доставка: порог €25.00 считается от суммы блюд ДО списания бонусов
            decimal deliveryFee = grossItemsTotal >= 25.00m ? 0.00m : 2.50m;
            decimal bonusSpent = 0.00m;
            decimal bonusEarned = 0.00m;

            if (req.UserId.HasValue && req.UserId.Value > 0)
            {
                using var uCmd = connection.CreateCommand();
                uCmd.Transaction = tx;
                uCmd.CommandText = "SELECT BonusBalance FROM Users WHERE Id = @uid;";
                uCmd.Parameters.AddWithValue("@uid", req.UserId.Value);
                var balObj = uCmd.ExecuteScalar();
                if (balObj == null)
                    return (false, "Указанный пользователь не найден.", null);

                var currentBalance = Convert.ToDecimal(balObj);

                if (req.BonusToSpend < 0)
                    return (false, "Количество бонусов не может быть отрицательным.", null);

                // Максимум 30% от суммы блюд и не более текущего баланса
                var maxBonusAllowed = Math.Min(currentBalance, Math.Round(grossItemsTotal * 0.30m, 2, MidpointRounding.AwayFromZero));

                if (req.BonusToSpend > maxBonusAllowed + 0.001m)
                    return (false, $"Превышен лимит списания бонусов. Доступно максимум €{maxBonusAllowed:F2} (до 30% от заказа).", null);

                bonusSpent = Math.Round(req.BonusToSpend, 2, MidpointRounding.AwayFromZero);

                // 5% кэшбэк от фактически оплаченной стоимости блюд
                var netPaidItems = Math.Max(0m, grossItemsTotal - bonusSpent);
                bonusEarned = Math.Round(netPaidItems * 0.05m, 2, MidpointRounding.AwayFromZero);
            }

            decimal totalEur = Math.Round(grossItemsTotal - bonusSpent + deliveryFee, 2, MidpointRounding.AwayFromZero);
            decimal netSubtotal = Math.Round(grossItemsTotal / 1.10m, 2, MidpointRounding.AwayFromZero);
            decimal vatAmount = Math.Round(grossItemsTotal - netSubtotal, 2, MidpointRounding.AwayFromZero);

            using var seqCmd = connection.CreateCommand();
            seqCmd.Transaction = tx;
            seqCmd.CommandText = "SELECT COALESCE(MAX(Id), 0) + 101 FROM Orders;";
            var nextNum = Convert.ToInt32(seqCmd.ExecuteScalar());
            var orderNumber = $"ORD-2026-{nextNum}";

            using var ordCmd = connection.CreateCommand();
            ordCmd.Transaction = tx;
            ordCmd.CommandText = @"
                INSERT INTO Orders (OrderNumber, CustomerId, UserId, AssignedStaffId, Status, PaymentMethod,
                                    NetSubtotalEur, VatAmountEur, DeliveryFeeEur, BonusSpentEur, BonusEarnedEur, TotalEur,
                                    CustomerComment, CreatedAtUtc, UpdatedAtUtc)
                VALUES (@num, @cid, @uid, 1, 'New', @pay, @net, @vat, @deliv, @bspent, @bearned, @tot, @comm, @now, @now);
                SELECT last_insert_rowid();";
            ordCmd.Parameters.AddWithValue("@num", orderNumber);
            ordCmd.Parameters.AddWithValue("@cid", customerId);
            ordCmd.Parameters.AddWithValue("@uid", (object?)req.UserId ?? DBNull.Value);
            ordCmd.Parameters.AddWithValue("@pay", string.IsNullOrWhiteSpace(req.PaymentMethod) ? "CardOnline" : req.PaymentMethod.Trim());
            ordCmd.Parameters.AddWithValue("@net", netSubtotal);
            ordCmd.Parameters.AddWithValue("@vat", vatAmount);
            ordCmd.Parameters.AddWithValue("@deliv", deliveryFee);
            ordCmd.Parameters.AddWithValue("@bspent", bonusSpent);
            ordCmd.Parameters.AddWithValue("@bearned", bonusEarned);
            ordCmd.Parameters.AddWithValue("@tot", totalEur);
            ordCmd.Parameters.AddWithValue("@comm", (object?)req.CustomerComment?.Trim() ?? DBNull.Value);
            ordCmd.Parameters.AddWithValue("@now", nowIso);
            var orderId = Convert.ToInt32(ordCmd.ExecuteScalar());

            foreach (var line in computedLines)
            {
                using var itemCmd = connection.CreateCommand();
                itemCmd.Transaction = tx;
                itemCmd.CommandText = @"
                    INSERT INTO OrderItems (OrderId, PizzaId, SizeId, Quantity, UnitPriceEur, LineTotalEur)
                    VALUES (@oid, @pid, @sid, @qty, @uprice, @ltotal);";
                itemCmd.Parameters.AddWithValue("@oid", orderId);
                itemCmd.Parameters.AddWithValue("@pid", line.PizzaId);
                itemCmd.Parameters.AddWithValue("@sid", line.SizeId);
                itemCmd.Parameters.AddWithValue("@qty", line.Qty);
                itemCmd.Parameters.AddWithValue("@uprice", line.UnitPrice);
                itemCmd.Parameters.AddWithValue("@ltotal", line.LineTotal);
                itemCmd.ExecuteNonQuery();
            }

            using var histCmd = connection.CreateCommand();
            histCmd.Transaction = tx;
            histCmd.CommandText = @"
                INSERT INTO OrderStatusHistory (OrderId, Status, Note, ChangedByRole, ChangedAtUtc)
                VALUES (@oid, 'New', 'Заказ оформлен клиентом (GDPR подтверждено)', 'Customer', @now);";
            histCmd.Parameters.AddWithValue("@oid", orderId);
            histCmd.Parameters.AddWithValue("@now", nowIso);
            histCmd.ExecuteNonQuery();

            // Проведение бонусных транзакций и обновление баланса пользователя
            if (req.UserId.HasValue && req.UserId.Value > 0)
            {
                if (bonusSpent > 0)
                {
                    using var bRedeemCmd = connection.CreateCommand();
                    bRedeemCmd.Transaction = tx;
                    bRedeemCmd.CommandText = @"
                        INSERT INTO BonusTransactions (UserId, OrderNumber, Type, DeltaAmount, Description, CreatedAtUtc)
                        VALUES (@uid, @ord, 'Redemption', @delta, @desc, @now);";
                    bRedeemCmd.Parameters.AddWithValue("@uid", req.UserId.Value);
                    bRedeemCmd.Parameters.AddWithValue("@ord", orderNumber);
                    bRedeemCmd.Parameters.AddWithValue("@delta", -bonusSpent);
                    bRedeemCmd.Parameters.AddWithValue("@desc", $"Оплата бонусами части заказа {orderNumber}");
                    bRedeemCmd.Parameters.AddWithValue("@now", nowIso);
                    bRedeemCmd.ExecuteNonQuery();
                }

                if (bonusEarned > 0)
                {
                    using var bAccrualCmd = connection.CreateCommand();
                    bAccrualCmd.Transaction = tx;
                    bAccrualCmd.CommandText = @"
                        INSERT INTO BonusTransactions (UserId, OrderNumber, Type, DeltaAmount, Description, CreatedAtUtc)
                        VALUES (@uid, @ord, 'Accrual', @delta, @desc, @now);";
                    bAccrualCmd.Parameters.AddWithValue("@uid", req.UserId.Value);
                    bAccrualCmd.Parameters.AddWithValue("@ord", orderNumber);
                    bAccrualCmd.Parameters.AddWithValue("@delta", bonusEarned);
                    bAccrualCmd.Parameters.AddWithValue("@desc", $"Кэшбэк 5% за заказ {orderNumber}");
                    bAccrualCmd.Parameters.AddWithValue("@now", nowIso);
                    bAccrualCmd.ExecuteNonQuery();
                }

                using var updBalCmd = connection.CreateCommand();
                updBalCmd.Transaction = tx;
                updBalCmd.CommandText = @"
                    UPDATE Users 
                    SET BonusBalance = BonusBalance - @spent + @earned
                    WHERE Id = @uid;";
                updBalCmd.Parameters.AddWithValue("@spent", bonusSpent);
                updBalCmd.Parameters.AddWithValue("@earned", bonusEarned);
                updBalCmd.Parameters.AddWithValue("@uid", req.UserId.Value);
                updBalCmd.ExecuteNonQuery();
            }

            tx.Commit();
            return (true, string.Empty, GetOrderByNumber(orderNumber));
        }
        catch (Exception ex)
        {
            tx.Rollback();
            return (false, $"Ошибка сохранения заказа: {ex.Message}", null);
        }
    }

    public (bool Success, string Error, OrderDetailDto? Order) UpdateOrderStatus(int orderId, UpdateOrderStatusRequest req)
    {
        using var connection = new SqliteConnection(_connectionString);
        connection.Open();

        using var getCmd = connection.CreateCommand();
        getCmd.CommandText = "SELECT OrderNumber, Status FROM Orders WHERE Id = @id;";
        getCmd.Parameters.AddWithValue("@id", orderId);

        using var reader = getCmd.ExecuteReader();
        if (!reader.Read())
            return (false, "Заказ не найден.", null);

        var orderNumber = reader.GetString(0);
        var currentStatus = reader.GetString(1);
        reader.Close();

        if (!AllowedTransitions.TryGetValue(currentStatus, out var allowed) || !allowed.Contains(req.Status))
            return (false, $"Недопустимый переход статуса: из '{currentStatus}' в '{req.Status}'.", null);

        var nowIso = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ");
        var defaultNote = req.Status switch
        {
            "Preparing" => "Заказ принят в работу на кухне",
            "Baking" => "Пицца отправлена в подовую печь (430°C)",
            "OutForDelivery" => "Передано курьеру в термосумке",
            "Delivered" => "Заказ успешно доставлен клиенту",
            "Cancelled" => "Заказ отменён менеджером",
            _ => "Статус обновлён"
        };

        using var updCmd = connection.CreateCommand();
        updCmd.CommandText = "UPDATE Orders SET Status = @st, UpdatedAtUtc = @now WHERE Id = @id;";
        updCmd.Parameters.AddWithValue("@st", req.Status);
        updCmd.Parameters.AddWithValue("@now", nowIso);
        updCmd.Parameters.AddWithValue("@id", orderId);
        updCmd.ExecuteNonQuery();

        using var histCmd = connection.CreateCommand();
        histCmd.CommandText = @"
            INSERT INTO OrderStatusHistory (OrderId, Status, Note, ChangedByRole, ChangedAtUtc)
            VALUES (@oid, @st, @note, @role, @now);";
        histCmd.Parameters.AddWithValue("@oid", orderId);
        histCmd.Parameters.AddWithValue("@st", req.Status);
        histCmd.Parameters.AddWithValue("@note", string.IsNullOrWhiteSpace(req.Note) ? defaultNote : req.Note.Trim());
        histCmd.Parameters.AddWithValue("@role", string.IsNullOrWhiteSpace(req.ChangedByRole) ? "Manager" : req.ChangedByRole.Trim());
        histCmd.Parameters.AddWithValue("@now", nowIso);
        histCmd.ExecuteNonQuery();

        return (true, string.Empty, GetOrderByNumber(orderNumber));
    }

    public PizzaDto CreatePizza(CreatePizzaRequest req)
    {
        using var connection = new SqliteConnection(_connectionString);
        connection.Open();

        using var seqCmd = connection.CreateCommand();
        seqCmd.CommandText = "SELECT COALESCE(MAX(Id), 0) + 1 FROM Pizzas;";
        var nextId = Convert.ToInt32(seqCmd.ExecuteScalar());
        var sku = $"PZ-{nextId:D3}";

        using var cmd = connection.CreateCommand();
        cmd.CommandText = @"
            INSERT INTO Pizzas (Sku, Name, Description, Ingredients, Category, DietaryTag, BasePriceEur, PrepMinutes, CaloriesKcal, IsAvailable)
            VALUES (@sku, @name, @desc, @ing, @cat, @tag, @price, @prep, @kcal, 1);
            SELECT last_insert_rowid();";
        cmd.Parameters.AddWithValue("@sku", sku);
        cmd.Parameters.AddWithValue("@name", req.Name.Trim());
        cmd.Parameters.AddWithValue("@desc", req.Description.Trim());
        cmd.Parameters.AddWithValue("@ing", req.Ingredients.Trim());
        cmd.Parameters.AddWithValue("@cat", req.Category.Trim());
        cmd.Parameters.AddWithValue("@tag", req.DietaryTag.Trim());
        cmd.Parameters.AddWithValue("@price", Math.Round(req.BasePriceEur, 2));
        cmd.Parameters.AddWithValue("@prep", req.PrepMinutes > 0 ? req.PrepMinutes : 15);
        cmd.Parameters.AddWithValue("@kcal", req.CaloriesKcal > 0 ? req.CaloriesKcal : 850);

        var id = Convert.ToInt32(cmd.ExecuteScalar());
        return GetMenu().First(p => p.Id == id);
    }

    // =========================================================================
    // Аналитика и статистика администратора
    // =========================================================================

    public AdminStatsDto GetAdminStats()
    {
        using var connection = new SqliteConnection(_connectionString);
        connection.Open();

        int totalOrders = 0;
        int activeOrders = 0;
        decimal grossRevenueEur = 0m;
        decimal netRevenueEur = 0m;
        decimal vatTotalEur = 0m;
        decimal totalBonusIssued = 0m;
        decimal totalBonusRedeemed = 0m;

        using (var cmd = connection.CreateCommand())
        {
            cmd.CommandText = @"
                SELECT 
                    COUNT(*),
                    SUM(CASE WHEN Status NOT IN ('Delivered', 'Cancelled') THEN 1 ELSE 0 END),
                    COALESCE(SUM(CASE WHEN Status != 'Cancelled' THEN TotalEur ELSE 0 END), 0),
                    COALESCE(SUM(CASE WHEN Status != 'Cancelled' THEN NetSubtotalEur ELSE 0 END), 0),
                    COALESCE(SUM(CASE WHEN Status != 'Cancelled' THEN VatAmountEur ELSE 0 END), 0)
                FROM Orders;";
            using var r = cmd.ExecuteReader();
            if (r.Read())
            {
                totalOrders = r.GetInt32(0);
                activeOrders = r.IsDBNull(1) ? 0 : r.GetInt32(1);
                grossRevenueEur = Math.Round(r.GetDecimal(2), 2);
                netRevenueEur = Math.Round(r.GetDecimal(3), 2);
                vatTotalEur = Math.Round(r.GetDecimal(4), 2);
            }
        }

        decimal averageOrderValueEur = totalOrders > 0
            ? Math.Round(grossRevenueEur / totalOrders, 2)
            : 0m;

        using (var cmd = connection.CreateCommand())
        {
            cmd.CommandText = @"
                SELECT 
                    COALESCE(SUM(CASE WHEN DeltaAmount > 0 THEN DeltaAmount ELSE 0 END), 0),
                    COALESCE(SUM(CASE WHEN DeltaAmount < 0 THEN ABS(DeltaAmount) ELSE 0 END), 0)
                FROM BonusTransactions;";
            using var r = cmd.ExecuteReader();
            if (r.Read())
            {
                totalBonusIssued = Math.Round(r.GetDecimal(0), 2);
                totalBonusRedeemed = Math.Round(r.GetDecimal(1), 2);
            }
        }

        var ordersByStatus = new List<OrderStatusCountDto>();
        using (var cmd = connection.CreateCommand())
        {
            cmd.CommandText = "SELECT Status, COUNT(*) FROM Orders GROUP BY Status ORDER BY COUNT(*) DESC;";
            using var r = cmd.ExecuteReader();
            while (r.Read())
            {
                ordersByStatus.Add(new OrderStatusCountDto(r.GetString(0), r.GetInt32(1)));
            }
        }

        var topPizzas = new List<TopPizzaDto>();
        using (var cmd = connection.CreateCommand())
        {
            cmd.CommandText = @"
                SELECT p.Name, SUM(oi.Quantity) as UnitsSold, SUM(oi.LineTotalEur) as Revenue
                FROM OrderItems oi
                JOIN Pizzas p ON p.Id = oi.PizzaId
                JOIN Orders o ON o.Id = oi.OrderId
                WHERE o.Status != 'Cancelled'
                GROUP BY p.Id, p.Name
                ORDER BY UnitsSold DESC, Revenue DESC
                LIMIT 5;";
            using var r = cmd.ExecuteReader();
            while (r.Read())
            {
                topPizzas.Add(new TopPizzaDto(r.GetString(0), r.GetInt32(1), Math.Round(r.GetDecimal(2), 2)));
            }
        }

        return new AdminStatsDto(
            totalOrders,
            activeOrders,
            grossRevenueEur,
            netRevenueEur,
            vatTotalEur,
            averageOrderValueEur,
            totalBonusIssued,
            totalBonusRedeemed,
            ordersByStatus,
            topPizzas
        );
    }

    private static List<OrderItemDetailDto> GetOrderItems(SqliteConnection connection, int orderId)
    {
        using var cmd = connection.CreateCommand();
        cmd.CommandText = @"
            SELECT oi.Id, oi.PizzaId, p.Name, s.Code, s.Label, oi.Quantity, oi.UnitPriceEur, oi.LineTotalEur
            FROM OrderItems oi
            INNER JOIN Pizzas p ON p.Id = oi.PizzaId
            INNER JOIN PizzaSizes s ON s.Id = oi.SizeId
            WHERE oi.OrderId = @oid;";
        cmd.Parameters.AddWithValue("@oid", orderId);

        var list = new List<OrderItemDetailDto>();
        using var r = cmd.ExecuteReader();
        while (r.Read())
        {
            list.Add(new OrderItemDetailDto(
                r.GetInt32(0), r.GetInt32(1), r.GetString(2), r.GetString(3),
                r.GetString(4), r.GetInt32(5), r.GetDecimal(6), r.GetDecimal(7)
            ));
        }
        return list;
    }

    private static List<OrderStatusHistoryDto> GetOrderHistory(SqliteConnection connection, int orderId)
    {
        using var cmd = connection.CreateCommand();
        cmd.CommandText = @"
            SELECT Id, Status, Note, ChangedByRole, ChangedAtUtc
            FROM OrderStatusHistory
            WHERE OrderId = @oid
            ORDER BY Id ASC;";
        cmd.Parameters.AddWithValue("@oid", orderId);

        var list = new List<OrderStatusHistoryDto>();
        using var r = cmd.ExecuteReader();
        while (r.Read())
        {
            list.Add(new OrderStatusHistoryDto(
                r.GetInt32(0), r.GetString(1), r.GetString(2), r.GetString(3), r.GetString(4)
            ));
        }
        return list;
    }
}
