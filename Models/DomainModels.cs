namespace PizzaOrderSystem.Models;

public record PizzaDto(
    int Id,
    string Sku,
    string Name,
    string Description,
    string Ingredients,
    string Category,
    string DietaryTag,
    decimal BasePriceEur,
    int PrepMinutes,
    int CaloriesKcal,
    bool IsAvailable
);

public record PizzaSizeDto(
    int Id,
    string Code,
    string Label,
    int DiameterCm,
    int WeightGrams,
    decimal PriceMultiplier
);

public record StaffDto(
    int Id,
    string FullName,
    string Role,
    string RoleDisplayRu,
    string BadgeCode,
    bool IsActive
);

public record UserProfileDto(
    int Id,
    string Email,
    string FullName,
    string Phone,
    string DefaultAddress,
    string Role,
    decimal BonusBalance,
    string CreatedAtUtc
);

public record RegisterRequest(
    string Email,
    string Password,
    string FullName,
    string Phone,
    string DefaultAddress
);

public record LoginRequest(
    string Email,
    string Password
);

public record UpdateProfileRequest(
    string FullName,
    string Phone,
    string DefaultAddress
);

public record BonusTransactionDto(
    int Id,
    int UserId,
    string? OrderNumber,
    string Type,
    decimal DeltaAmount,
    string Description,
    string CreatedAtUtc
);

public record PromotionDto(
    int Id,
    string Badge,
    string Title,
    string Subtitle,
    string? PromoCode,
    string ValidUntil,
    string? TargetCategory,
    bool IsActive
);

public record OrderItemDetailDto(
    int Id,
    int PizzaId,
    string PizzaName,
    string SizeCode,
    string SizeLabel,
    int Quantity,
    decimal UnitPriceEur,
    decimal LineTotalEur
);

public record OrderStatusHistoryDto(
    int Id,
    string Status,
    string Note,
    string ChangedByRole,
    string ChangedAtUtc
);

public record OrderDetailDto(
    int Id,
    string OrderNumber,
    int? UserId,
    string CustomerName,
    string CustomerPhone,
    string CustomerEmail,
    string DeliveryAddress,
    bool GdprConsentAccepted,
    bool MarketingOptIn,
    string Status,
    string PaymentMethod,
    decimal NetSubtotalEur,
    decimal VatAmountEur,
    decimal DeliveryFeeEur,
    decimal BonusSpentEur,
    decimal BonusEarnedEur,
    decimal TotalEur,
    string? CustomerComment,
    string CreatedAtUtc,
    string UpdatedAtUtc,
    List<OrderItemDetailDto> Items,
    List<OrderStatusHistoryDto> History
);

public record ProfileDetailsDto(
    UserProfileDto User,
    List<BonusTransactionDto> BonusHistory,
    List<OrderDetailDto> Orders
);

public record CreateOrderItemRequest(
    int PizzaId,
    int SizeId,
    int Quantity
);

public record CreateOrderRequest(
    string CustomerName,
    string CustomerPhone,
    string CustomerEmail,
    string DeliveryAddress,
    bool GdprConsentAccepted,
    bool MarketingOptIn,
    string PaymentMethod,
    string? CustomerComment,
    List<CreateOrderItemRequest> Items,
    int? UserId = null,
    decimal BonusToSpend = 0.00m
);

public record UpdateOrderStatusRequest(
    string Status,
    string ChangedByRole,
    string? Note
);

public record CreatePizzaRequest(
    string Name,
    string Description,
    string Ingredients,
    string Category,
    string DietaryTag,
    decimal BasePriceEur,
    int PrepMinutes,
    int CaloriesKcal
);

public record OrderStatusCountDto(
    string Status,
    int Count
);

public record TopPizzaDto(
    string PizzaName,
    int UnitsSold,
    decimal RevenueEur
);

public record AdminStatsDto(
    int TotalOrders,
    int ActiveOrders,
    decimal GrossRevenueEur,
    decimal NetRevenueEur,
    decimal VatTotalEur,
    decimal AverageOrderValueEur,
    decimal TotalBonusIssued,
    decimal TotalBonusRedeemed,
    List<OrderStatusCountDto> OrdersByStatus,
    List<TopPizzaDto> TopPizzas
);
