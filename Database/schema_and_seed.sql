-- ============================================================================
-- Схема базы данных SQLite и начальные тестовые данные (v2.0)
-- Проект: Простая система заказов пиццы (CROSTA EU Ordering Platform)
-- Студент: Махвиладзе Давид Васильевич
-- ============================================================================

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS OrderStatusHistory;
DROP TABLE IF EXISTS OrderItems;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS BonusTransactions;
DROP TABLE IF EXISTS Promotions;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Customers;
DROP TABLE IF EXISTS Staff;
DROP TABLE IF EXISTS PizzaSizes;
DROP TABLE IF EXISTS Pizzas;

CREATE TABLE Pizzas (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Sku TEXT NOT NULL UNIQUE,
    Name TEXT NOT NULL,
    Description TEXT NOT NULL,
    Ingredients TEXT NOT NULL,
    Category TEXT NOT NULL,
    DietaryTag TEXT NOT NULL,
    BasePriceEur REAL NOT NULL CHECK (BasePriceEur > 0),
    PrepMinutes INTEGER NOT NULL DEFAULT 15,
    CaloriesKcal INTEGER NOT NULL DEFAULT 820,
    IsAvailable INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE PizzaSizes (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Code TEXT NOT NULL UNIQUE,
    Label TEXT NOT NULL,
    DiameterCm INTEGER NOT NULL,
    WeightGrams INTEGER NOT NULL,
    PriceMultiplier REAL NOT NULL
);

CREATE TABLE Staff (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    FullName TEXT NOT NULL,
    Role TEXT NOT NULL CHECK (Role IN ('Manager', 'Kitchen', 'Courier')),
    RoleDisplayRu TEXT NOT NULL,
    BadgeCode TEXT NOT NULL UNIQUE,
    IsActive INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE Customers (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    FullName TEXT NOT NULL,
    Phone TEXT NOT NULL,
    Email TEXT NOT NULL,
    DeliveryAddress TEXT NOT NULL,
    GdprConsentAccepted INTEGER NOT NULL CHECK (GdprConsentAccepted = 1),
    MarketingOptIn INTEGER NOT NULL DEFAULT 0,
    CreatedAtUtc TEXT NOT NULL
);

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

CREATE TABLE Orders (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    OrderNumber TEXT NOT NULL UNIQUE,
    CustomerId INTEGER NOT NULL,
    UserId INTEGER NULL,
    AssignedStaffId INTEGER NULL,
    Status TEXT NOT NULL CHECK (Status IN ('New', 'Preparing', 'Baking', 'OutForDelivery', 'Delivered', 'Cancelled')),
    PaymentMethod TEXT NOT NULL,
    NetSubtotalEur REAL NOT NULL,
    VatAmountEur REAL NOT NULL,
    DeliveryFeeEur REAL NOT NULL,
    BonusSpentEur REAL NOT NULL DEFAULT 0.00,
    BonusEarnedEur REAL NOT NULL DEFAULT 0.00,
    TotalEur REAL NOT NULL,
    CustomerComment TEXT NULL,
    CreatedAtUtc TEXT NOT NULL,
    UpdatedAtUtc TEXT NOT NULL,
    FOREIGN KEY (CustomerId) REFERENCES Customers(Id),
    FOREIGN KEY (UserId) REFERENCES Users(Id),
    FOREIGN KEY (AssignedStaffId) REFERENCES Staff(Id)
);

CREATE TABLE OrderItems (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    OrderId INTEGER NOT NULL,
    PizzaId INTEGER NOT NULL,
    SizeId INTEGER NOT NULL,
    Quantity INTEGER NOT NULL CHECK (Quantity > 0),
    UnitPriceEur REAL NOT NULL,
    LineTotalEur REAL NOT NULL,
    FOREIGN KEY (OrderId) REFERENCES Orders(Id) ON DELETE CASCADE,
    FOREIGN KEY (PizzaId) REFERENCES Pizzas(Id),
    FOREIGN KEY (SizeId) REFERENCES PizzaSizes(Id)
);

CREATE TABLE OrderStatusHistory (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    OrderId INTEGER NOT NULL,
    Status TEXT NOT NULL,
    Note TEXT NOT NULL,
    ChangedByRole TEXT NOT NULL,
    ChangedAtUtc TEXT NOT NULL,
    FOREIGN KEY (OrderId) REFERENCES Orders(Id) ON DELETE CASCADE
);

-- ============================================================================
-- Начальное наполнение (Seed Data)
-- ============================================================================

INSERT INTO PizzaSizes (Code, Label, DiameterCm, WeightGrams, PriceMultiplier) VALUES
('S', 'Стандарт (25 см)', 25, 440, 1.00),
('M', 'Классик (30 см)', 30, 620, 1.28),
('L', 'Семейная (35 см)', 35, 850, 1.56);

INSERT INTO Pizzas (Sku, Name, Description, Ingredients, Category, DietaryTag, BasePriceEur, PrepMinutes, CaloriesKcal, IsAvailable) VALUES
('PZ-001', 'Маргарита DOC', 'Классическая неаполитанская рецептура с томатами Сан-Марцано и свежим базиликом.', 'Томаты San Marzano DOP, моцарелла Fior di Latte, свежий базилик, оливковое масло Extra Virgin', 'Классика', 'Вегетарианская', 9.50, 12, 740, 1),
('PZ-002', 'Пепперони Диавола', 'Пикантная салями вентричина с хрустящей корочкой и выдержанным пармезаном.', 'Томатный соус, моцарелла, острая салями Ventricina, перец чили, пармезан 24 мес.', 'Мясные', 'Острая', 12.40, 14, 920, 1),
('PZ-003', 'Кватро Формаджи', 'Благородный купаж четырёх европейских сыров на сливочной основе без томатов.', 'Сливки, моцарелла, горгонзола Dolce DOP, грана падано, эмменталь, чёрный перец', 'Сырные', 'Вегетарианская', 13.20, 13, 980, 1),
('PZ-004', 'Прошутто э Руккола', 'Тонкие ломтики пармской ветчины, добавляемые после печи, со свежей рукколой.', 'Томаты San Marzano, моцарелла, прошутто крудо, руккола, лепестки пармезана', 'Премиум', 'Хит ЕС', 14.50, 15, 840, 1),
('PZ-005', 'Трюфельная с лесными грибами', 'Ароматный крем из чёрного трюфеля, запечённые шампиньоны и тимьян.', 'Трюфельный соус, моцарелла, шампиньоны, вешенки, свежий тимьян, трюфельное масло', 'Премиум', 'Вегетарианская', 14.90, 16, 860, 1),
('PZ-006', 'Карбонара Аль Форно', 'Сыровяленый гуанчале, яичный крем с пекорино романо и свежемолотым перцем.', 'Моцарелла, гуанчале, соус пекорино-желток, чёрный перец Телличерри', 'Мясные', 'Новинка', 13.50, 15, 960, 1),
('PZ-007', 'Средиземноморская Веган', 'Лёгкая овощная пицца на тесте 48-часовой ферментации с артишоками и оливками.', 'Томатный соус, веган-моцарелла, артишоки, оливки Каламата, вяленые томаты, орегано', 'Овощные', 'Веган', 11.80, 14, 690, 1),
('PZ-008', 'Морская с креветками и песто', 'Тигровые креветки, домашний генуэзский песто и цедра сицилийского лимона.', 'Моцарелла, тигровые креветки, соус песто Genovese, томаты черри, цедра лимона', 'Премиум', 'Морепродукты', 15.80, 17, 810, 1),
('PZ-009', 'Барбекю Поло Аффумикато', 'Копчёное куриное филе, красный ялтинский лук и соус smoky BBQ.', 'Соус BBQ, моцарелла, копчёная куриная грудка, красный лук, кукуруза, петрушка', 'Мясные', 'Без свинины', 12.90, 15, 890, 1);

INSERT INTO Staff (FullName, Role, RoleDisplayRu, BadgeCode, IsActive) VALUES
('Елена Ковальчук', 'Manager', 'Менеджер смены', 'MGR-01', 1),
('Марко Росси', 'Kitchen', 'Шеф-пиццайоло', 'KIT-04', 1),
('Андрей Мельник', 'Courier', 'Курьер (Электробайк #3)', 'DRV-12', 1);

-- Тестовые пользователи с детерминированным SHA-256 хэшированием (соль: crosta_salt_2026_)
-- david@crosta.eu / User123!
-- admin@crosta.eu / Admin123!
INSERT INTO Users (Id, Email, PasswordHash, FullName, Phone, DefaultAddress, Role, BonusBalance, CreatedAtUtc) VALUES
(1, 'david@crosta.eu', '36188f5d2250aec9d8cd512ccc16156b2b5f60d8c812f0140414870306612bd8', 'Давид Махвиладзе', '+373 777 88420', 'ул. Свердлова, 45, кв. 12', 'Customer', 14.50, '2026-11-15T10:00:00Z'),
(2, 'admin@crosta.eu', 'd1ff96fd4cd2059ccf6af81c763db71fe11b3aad842808288b15f12ca9d20a45', 'Елена Ковальчук', '+373 777 00001', 'Офис CROSTA, ул. Ленина, 1', 'Admin', 0.00, '2026-11-01T08:00:00Z');

-- Журнал бонусов для Давида (5.00 Welcome + 9.50 Начисление = 14.50)
INSERT INTO BonusTransactions (UserId, OrderNumber, Type, DeltaAmount, Description, CreatedAtUtc) VALUES
(1, NULL, 'WelcomeBonus', 5.00, 'Приветственный бонус при регистрации', '2026-11-15T10:00:00Z'),
(1, 'ORD-2026-104', 'Accrual', 9.50, 'Бонусное начисление за заказ ORD-2026-104', '2026-11-18T10:12:00Z');

-- Промо-акции для главной страницы
INSERT INTO Promotions (Badge, Title, Subtitle, PromoCode, ValidUntil, TargetCategory, IsActive) VALUES
('АКЦИЯ ЕС', 'Бесплатная курьерская доставка от €25.00', 'Электродоставка в термосумках за 35 минут.', 'FREEDELIV', '2026-12-31', 'Все', 1),
('БОНУСЫ 2X', 'Двойной кэшбэк 10% по будням (12:00–15:00)', 'Оплачивайте бонусами до 30% стоимости следующих заказов.', 'LUNCH2X', '2026-12-31', 'Все', 1),
('НОВОЕ В МЕНЮ', 'Тесто 48-часовой ферментации на закваске Lievito Madre', 'Попробуйте «Трюфельную с лесными грибами» и «Карбонара Аль Форно».', NULL, '2026-12-31', 'Премиум', 1);

INSERT INTO Customers (FullName, Phone, Email, DeliveryAddress, GdprConsentAccepted, MarketingOptIn, CreatedAtUtc) VALUES
('Анна Бергман', '+373 777 41209', 'anna.bergman@example.eu', 'ул. Карла Либкнехта, 142, кв. 18', 1, 1, '2026-11-18T08:15:00Z'),
('Виктор Морозов', '+373 778 90311', 'v.morozov@corp-mail.eu', 'ул. 25 Октября, 78, офис 402', 1, 0, '2026-11-18T09:05:00Z'),
('София Лоренц', '+373 779 55104', 'sofia.lorenz@designhub.eu', 'пер. Днестровский, 9, подъезд 2', 1, 1, '2026-11-18T09:42:00Z'),
('Давид Махвиладзе', '+373 777 88420', 'david@crosta.eu', 'ул. Свердлова, 45, кв. 12', 1, 0, '2026-11-18T10:05:00Z');

INSERT INTO Orders (OrderNumber, CustomerId, UserId, AssignedStaffId, Status, PaymentMethod, NetSubtotalEur, VatAmountEur, DeliveryFeeEur, BonusSpentEur, BonusEarnedEur, TotalEur, CustomerComment, CreatedAtUtc, UpdatedAtUtc) VALUES
('ORD-2026-101', 1, NULL, 3, 'Delivered', 'CardOnline', 25.51, 2.55, 0.00, 0.00, 0.00, 28.06, 'Домофон 18К, оставить у двери при необходимости.', '2026-11-18T08:16:00Z', '2026-11-18T08:54:00Z'),
('ORD-2026-102', 2, NULL, 3, 'OutForDelivery', 'CorporateInvoice', 32.95, 3.29, 0.00, 0.00, 0.00, 36.24, 'Бизнес-центр, пропуск на ресепшене заказан.', '2026-11-18T09:07:00Z', '2026-11-18T09:38:00Z'),
('ORD-2026-103', 3, NULL, 2, 'Baking', 'ApplePay', 15.36, 1.54, 2.50, 0.00, 0.00, 19.40, 'Без острого перца, положить салфетки.', '2026-11-18T09:45:00Z', '2026-11-18T09:58:00Z'),
('ORD-2026-104', 4, 1, 1, 'New', 'CardOnDelivery', 25.97, 2.60, 0.00, 0.00, 1.43, 28.57, 'Позвонить за 5 минут до прибытия курьера.', '2026-11-18T10:12:00Z', '2026-11-18T10:12:00Z');

INSERT INTO OrderItems (OrderId, PizzaId, SizeId, Quantity, UnitPriceEur, LineTotalEur) VALUES
(1, 4, 2, 1, 18.56, 18.56),
(1, 1, 1, 1, 9.50, 9.50),
(2, 2, 3, 1, 19.34, 19.34),
(2, 3, 2, 1, 16.90, 16.90),
(3, 3, 2, 1, 16.90, 16.90),
(4, 5, 2, 1, 19.07, 19.07),
(4, 1, 1, 1, 9.50, 9.50);

INSERT INTO OrderStatusHistory (OrderId, Status, Note, ChangedByRole, ChangedAtUtc) VALUES
(1, 'New', 'Заказ оформлен клиентом онлайн', 'System', '2026-11-18T08:16:00Z'),
(1, 'Preparing', 'Передан на станцию пиццайоло', 'Manager', '2026-11-18T08:19:00Z'),
(1, 'Baking', 'Выпекается в подовой печи при 430°C', 'Kitchen', '2026-11-18T08:27:00Z'),
(1, 'OutForDelivery', 'Курьер Андрей Мельник забрал термосумку', 'Courier', '2026-11-18T08:35:00Z'),
(1, 'Delivered', 'Заказ вручён клиенту', 'Courier', '2026-11-18T08:54:00Z'),
(2, 'New', 'Корпоративный заказ принят', 'System', '2026-11-18T09:07:00Z'),
(2, 'Preparing', 'Подтверждён менеджером смены', 'Manager', '2026-11-18T09:10:00Z'),
(2, 'Baking', 'В печи (2 пиццы)', 'Kitchen', '2026-11-18T09:22:00Z'),
(2, 'OutForDelivery', 'Курьер выехал по адресу ул. 25 Октября, 78', 'Courier', '2026-11-18T09:38:00Z'),
(3, 'New', 'Заказ оформлен через Apple Pay', 'System', '2026-11-18T09:45:00Z'),
(3, 'Preparing', 'Тесто раскатано, добавлены сыры', 'Kitchen', '2026-11-18T09:50:00Z'),
(3, 'Baking', 'Выпекается в печи', 'Kitchen', '2026-11-18T09:58:00Z'),
(4, 'New', 'Новый заказ ожидает подтверждения менеджера', 'System', '2026-11-18T10:12:00Z');
