using PizzaOrderSystem.Data;
using PizzaOrderSystem.Models;
using PizzaOrderSystem.Tests;

if (args.Contains("--test", StringComparer.OrdinalIgnoreCase))
{
    var exitCode = SelfTestRunner.RunAll(Directory.GetCurrentDirectory());
    Environment.Exit(exitCode);
}

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddSingleton<PizzaRepository>();
builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>
        policy.AllowAnyOrigin().AllowAnyHeader().AllowAnyMethod());
});

var app = builder.Build();

using (var scope = app.Services.CreateScope())
{
    var repo = scope.ServiceProvider.GetRequiredService<PizzaRepository>();
    repo.EnsureInitialized();
}

app.UseCors();
app.UseDefaultFiles();
app.UseStaticFiles();

// =============================================================================
// 1. Аутентификация и профиль (без Google OAuth)
// =============================================================================

app.MapPost("/api/auth/register", (PizzaRepository repo, RegisterRequest req) =>
{
    var (success, error, user) = repo.Register(req);
    return success && user is not null
        ? Results.Created($"/api/profile/{user.Id}", user)
        : Results.BadRequest(new { error });
});

app.MapPost("/api/auth/login", (PizzaRepository repo, LoginRequest req) =>
{
    var (success, error, user) = repo.Login(req);
    return success && user is not null
        ? Results.Ok(user)
        : Results.Json(new { error }, statusCode: StatusCodes.Status401Unauthorized);
});

app.MapGet("/api/profile/{userId:int}", (PizzaRepository repo, int userId) =>
{
    var details = repo.GetProfileDetails(userId);
    return details is not null
        ? Results.Ok(details)
        : Results.NotFound(new { error = "Профиль пользователя не найден." });
});

app.MapPut("/api/profile/{userId:int}", (PizzaRepository repo, int userId, UpdateProfileRequest req) =>
{
    var (success, error, user) = repo.UpdateProfile(userId, req);
    return success && user is not null
        ? Results.Ok(user)
        : Results.BadRequest(new { error });
});

// =============================================================================
// 2. Акции, новости и каталог
// =============================================================================

app.MapGet("/api/promotions", (PizzaRepository repo) =>
    Results.Ok(repo.GetPromotions()));

app.MapGet("/api/menu", (PizzaRepository repo, string? category, string? search) =>
    Results.Ok(repo.GetMenu(category, search)));

app.MapGet("/api/menu/all", (PizzaRepository repo) =>
    Results.Ok(repo.GetAllPizzasForAdmin()));

app.MapPost("/api/menu", (PizzaRepository repo, CreatePizzaRequest req) =>
{
    if (string.IsNullOrWhiteSpace(req.Name) || req.BasePriceEur <= 0)
        return Results.BadRequest(new { error = "Укажите корректное название и цену пиццы." });

    var created = repo.CreatePizza(req);
    return Results.Created($"/api/menu/{created.Id}", created);
});

app.MapPatch("/api/menu/{id:int}/availability", (PizzaRepository repo, int id, bool? isAvailable) =>
{
    var updated = repo.TogglePizzaAvailability(id, isAvailable);
    return updated
        ? Results.Ok(new { success = true, id })
        : Results.NotFound(new { error = "Пицца с указанным ID не найдена." });
});

app.MapGet("/api/sizes", (PizzaRepository repo) =>
    Results.Ok(repo.GetSizes()));

app.MapGet("/api/staff", (PizzaRepository repo) =>
    Results.Ok(repo.GetStaff()));

// =============================================================================
// 3. Заказы и аналитика
// =============================================================================

app.MapGet("/api/orders", (PizzaRepository repo, string? status, int? userId) =>
    Results.Ok(repo.GetOrders(status, userId)));

app.MapGet("/api/orders/{orderNumber}", (PizzaRepository repo, string orderNumber) =>
{
    var order = repo.GetOrderByNumber(orderNumber);
    return order is not null 
        ? Results.Ok(order) 
        : Results.NotFound(new { error = "Заказ с указанным номером не найден." });
});

app.MapPost("/api/orders", (PizzaRepository repo, CreateOrderRequest req) =>
{
    var (success, error, order) = repo.CreateOrder(req);
    return success && order is not null
        ? Results.Created($"/api/orders/{order.OrderNumber}", order)
        : Results.BadRequest(new { error });
});

app.MapPatch("/api/orders/{id:int}/status", (PizzaRepository repo, int id, UpdateOrderStatusRequest req) =>
{
    var (success, error, order) = repo.UpdateOrderStatus(id, req);
    return success && order is not null
        ? Results.Ok(order)
        : Results.BadRequest(new { error });
});

app.MapGet("/api/admin/stats", (PizzaRepository repo) =>
    Results.Ok(repo.GetAdminStats()));

app.Run();
