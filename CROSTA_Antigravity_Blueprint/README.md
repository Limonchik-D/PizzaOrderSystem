# CROSTA EU Dispatch v2.0 — Пакет проектирования и этапов для Antigravity IDE

**Студент:** Махвиладзе Давид Васильевич  
**Предметная область:** Простая система заказов пиццы (Европейский стандарт Food-Tech)  
**Стек:** ASP.NET Core 8 Minimal API + SQLite + Vanilla JS / Tailwind CSS + GSAP

---

## Как скармливать этот пакет Antigravity

Распакуй эту папку в корень проекта `PizzaOrderSystem/` (рядом с `Program.cs` и `PizzaOrderSystem.csproj`), чтобы у агента был прямой доступ ко всем спецификациям.

Затем подавай этапы **строго по одному**, дожидаясь завершения каждого этапа, прогона `dotnet run -- --test` и визуальной проверки скриншотов:

1. **Этап 0 (`stages/STAGE_0_BASELINE.md`)** — разведка кодовой базы, чтение локальных скиллов и снятие базовых скриншотов «ДО».
2. **Этап 1 (`stages/STAGE_1_DB_AND_AUTH.md`)** — расширение SQLite (`Users`, `BonusTransactions`, `Promotions`), регистрация/вход без Google OAuth, бонусная экономика (5% кэшбэк / списание до 30%) и обновление автотестов.
3. **Этап 2 (`stages/STAGE_2_DESIGN_AND_PAGES.md`)** — внедрение дизайн-системы (тёплый бежевый `#F5EFE6` + тёмная тема `#141210` по скиллу `frontend-design`), главной страницы с акциями/новостями, личного профиля с бонусами и админ-панели со статистикой.
4. **Этап 3 (`stages/STAGE_3_MOTION_AND_SKILLS.md`)** — последовательное применение motion-скиллов (`find-animation-opportunities` → `animate` → `choreograph` → `gsap-scrolltrigger` → `animation-performance` → `review-animations`).
5. **Этап 4 (`stages/STAGE_4_QA_AND_SCREENSHOTS.md`)** — сквозное тестирование (`dotnet run -- --test`), проверка сценариев в браузере и финальный пакет скриншотов «ПОСЛЕ».

---

## Состав документации (`docs/`)
- `docs/01_SRS_AND_BUSINESS_RULES.md` — формальные функциональные/нефункциональные требования (v2.0), формулы бонусов, НДС 10% и правила ролей.
- `docs/02_DB_SCHEMA_V2.md` — точная DDL-схема SQLite (10 таблиц), ограничения целостности и тестовые аккаунты.
- `docs/03_API_CONTRACT.md` — спецификация всех REST API эндпоинтов, JSON-контрактов и кодов ошибок.
- `docs/04_DESIGN_SYSTEM_TOKENS.md` — CSS-токены тёплой бежевой и тёмной тем, типографика, правила контрастности WCAG AA и карта анимаций.
