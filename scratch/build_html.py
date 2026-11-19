# -*- coding: utf-8 -*-
import os

html_content = '''<!DOCTYPE html>
<html lang="ru" data-theme="light">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>CROSTA // Pizzeria Artigianale Napoletana</title>
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🍕</text></svg>">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=IBM+Plex+Mono:wght@400;500;600;700&family=Inter:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,600&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
  <script>
    tailwind.config = {
      darkMode: ['class', '[data-theme="dark"]'],
      theme: {
        extend: {
          fontFamily: {
            sans: ['"Plus Jakarta Sans"', '"Inter"', 'system-ui', '-apple-system', 'sans-serif'],
            serif: ['"Playfair Display"', 'Georgia', 'serif'],
            display: ['"Cinzel"', 'serif'],
            mono: ['"IBM Plex Mono"', 'monospace'],
          },
          colors: {
            canvas: 'var(--bg-canvas)',
            surface: 'var(--bg-surface)',
            elevated: 'var(--bg-elevated)',
            borderSubtle: 'var(--border-subtle)',
            textPrimary: 'var(--text-primary)',
            textSecondary: 'var(--text-secondary)',
            brand: {
              700: 'var(--accent-primary)',
              800: 'var(--accent-hover)',
            },
            bonus: 'var(--accent-bonus)',
          }
        }
      }
    }
  </script>
  <style>
    :root {
      --ease-out: cubic-bezier(0.23, 1, 0.32, 1);
      --ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);
      --ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);

      /* Warm Artisanal European Palette - Light Mode */
      --bg-canvas: #F5EFE6;
      --bg-surface: #FBF8F3;
      --bg-elevated: #EBE3D5;
      --border-subtle: #DFD5C5;
      --text-primary: #1C1917;
      --text-secondary: #57534E;
      --accent-primary: #B91C1C;
      --accent-hover: #991B1B;
      --accent-bonus: #15803D;

      /* WCAG AA Status Badges - Light */
      --badge-new-bg: #FEF3C7; --badge-new-text: #78350F; --badge-new-border: #FCD34D;
      --badge-prep-bg: #FFEDD5; --badge-prep-text: #7C2D12; --badge-prep-border: #FDBA74;
      --badge-bake-bg: #FEE2E2; --badge-bake-text: #7F1D1D; --badge-bake-border: #FCA5A5;
      --badge-deliv-bg: #DBEAFE; --badge-deliv-text: #1E3A8A; --badge-deliv-border: #93C5FD;
      --badge-done-bg: #D1FAE5; --badge-done-text: #064E3B; --badge-done-border: #6EE7B7;
      --badge-canc-bg: #E7E5E4; --badge-canc-text: #292524; --badge-canc-border: #D6D3D1;
    }

    [data-theme="dark"] {
      /* Warm Artisanal European Palette - Dark Mode */
      --bg-canvas: #141210;
      --bg-surface: #1E1B18;
      --bg-elevated: #282420;
      --border-subtle: #36302A;
      --text-primary: #F5EFE6;
      --text-secondary: #A8A29E;
      --accent-primary: #DC2626;
      --accent-hover: #EF4444;
      --accent-bonus: #22C55E;

      /* WCAG AA Status Badges - Dark (Contrast > 7:1) */
      --badge-new-bg: #451A03; --badge-new-text: #FDE68A; --badge-new-border: #92400E;
      --badge-prep-bg: #431407; --badge-prep-text: #FED7AA; --badge-prep-border: #9A3412;
      --badge-bake-bg: #450A0A; --badge-bake-text: #FECACA; --badge-bake-border: #991B1B;
      --badge-deliv-bg: #172554; --badge-deliv-text: #BFDBFE; --badge-deliv-border: #1E40AF;
      --badge-done-bg: #022C22; --badge-done-text: #A7F3D0; --badge-done-border: #065F46;
      --badge-canc-bg: #292524; --badge-canc-text: #E7E5E4; --badge-canc-border: #57534E;
    }

    body {
      background-color: var(--bg-canvas);
      color: var(--text-primary);
      transition: background-color 180ms var(--ease-out), color 180ms var(--ease-out);
    }

    .tabular-nums {
      font-variant-numeric: tabular-nums;
    }

    /* Adaptive Status Badges */
    .status-badge-New { background-color: var(--badge-new-bg) !important; color: var(--badge-new-text) !important; border-color: var(--badge-new-border) !important; }
    .status-badge-Preparing { background-color: var(--badge-prep-bg) !important; color: var(--badge-prep-text) !important; border-color: var(--badge-prep-border) !important; }
    .status-badge-Baking { background-color: var(--badge-bake-bg) !important; color: var(--badge-bake-text) !important; border-color: var(--badge-bake-border) !important; }
    .status-badge-OutForDelivery { background-color: var(--badge-deliv-bg) !important; color: var(--badge-deliv-text) !important; border-color: var(--badge-deliv-border) !important; }
    .status-badge-Delivered { background-color: var(--badge-done-bg) !important; color: var(--badge-done-text) !important; border-color: var(--badge-done-border) !important; }
    .status-badge-Cancelled { background-color: var(--badge-canc-bg) !important; color: var(--badge-canc-text) !important; border-color: var(--badge-canc-border) !important; }

    /* Button Tactile Scale */
    button:not(:disabled):active,
    .btn-press:not(:disabled):active {
      transform: scale(0.97) !important;
      transition: transform 160ms var(--ease-out) !important;
    }

    @media (hover: hover) and (pointer: fine) {
      .card-interactive {
        transition: transform 200ms var(--ease-out), box-shadow 200ms var(--ease-out), border-color 200ms var(--ease-out);
      }
      .card-interactive:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.04);
      }
    }

    /* Toast Notification */
    .toast-item {
      opacity: 1;
      transform: translateY(0);
      transition: opacity 350ms ease, transform 350ms ease;
    }
    @starting-style {
      .toast-item {
        opacity: 0;
        transform: translateY(14px);
      }
    }
    .toast-item.exiting {
      opacity: 0;
      transform: translateY(10px);
      pointer-events: none;
    }

    /* Elastic Tab Pill Under Nav */
    #nav-elastic-pill {
      position: absolute;
      transition: transform 220ms var(--ease-out), width 220ms var(--ease-out);
      z-index: 1;
      pointer-events: none;
    }
    nav button {
      position: relative;
      z-index: 2;
    }

    /* Word Roll by DesignBookmark */
    .roll {
      display: inline-flex;
      align-items: center;
      gap: 0.26em;
      white-space: nowrap;
      cursor: pointer;
      outline: none;
      line-height: 1.25;
      font-weight: 800;
    }
    .roll:focus-visible {
      outline: 2px solid var(--accent-primary);
      outline-offset: 4px;
      border-radius: 6px;
    }
    .roll .lead {
      opacity: 0.95;
    }
    .roll .slot {
      position: relative;
      display: inline-block;
      height: 1.25em;
      clip-path: inset(0 -0.5em);
      vertical-align: bottom;
      transition: color 180ms ease;
    }
    .roll .word {
      position: absolute;
      left: 0;
      top: 0;
      display: flex;
      white-space: nowrap;
    }
    .roll .ch {
      display: inline-block;
      white-space: pre;
      will-change: transform, opacity;
    }

    /* Kokonut UI CardField (https://kokonutui.com, MIT license) */
    .cardfield-brand-flip {
      transition: transform 200ms cubic-bezier(0.23, 1, 0.32, 1), opacity 200ms cubic-bezier(0.23, 1, 0.32, 1);
    }
    #cardfield-row {
      transition: border-color 150ms ease, box-shadow 150ms ease;
    }
    #cardfield-row:focus-within {
      border-color: var(--text-primary);
      box-shadow: 0 0 0 3px rgba(185, 28, 28, 0.12);
    }
    #cardfield-row.has-error {
      border-color: #ef4444 !important;
      box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.2) !important;
    }
    #cardfield-mirror {
      will-change: transform;
      transition: transform 400ms cubic-bezier(0.23, 1, 0.32, 1);
    }
    .card-group-span {
      transition: opacity 200ms cubic-bezier(0.23, 1, 0.32, 1);
    }

    /* Star Rating by DesignBookmark (https://designbookmark.com/motion#db-star-rating) */
    .db-star-frame {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 12px;
      user-select: none;
      -webkit-user-select: none;
    }
    .db-star-row {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .db-star-btn {
      position: relative;
      outline: none;
      user-select: none;
      -webkit-user-select: none;
      width: 44px;
      height: 44px;
      display: grid;
      place-items: center;
      cursor: pointer;
      border-radius: 12px;
      background: transparent;
      border: none;
      padding: 0;
      transition: background-color 150ms ease;
    }
    .db-star-btn:hover {
      background: rgba(245, 158, 11, 0.08);
    }
    .db-star-btn:focus-visible {
      outline: 2px solid #F59E0B;
      outline-offset: 2px;
    }
    .db-star-btn svg {
      width: 32px;
      height: 32px;
      display: block;
      overflow: visible;
      pointer-events: none;
      transform-origin: center center;
    }
    .db-star-btn path {
      transform-origin: 12px 12px;
      stroke-width: 1.4;
      transition: filter 150ms ease;
    }
    .db-star-word {
      font-size: 13px;
      font-weight: 600;
      height: 20px;
      overflow: hidden;
      position: relative;
      text-align: center;
    }
    .db-star-col {
      display: flex;
      flex-direction: column;
      will-change: transform;
    }
    .db-star-col b {
      display: block;
      height: 20px;
      line-height: 20px;
      font-weight: 600;
      font-size: 13px;
      color: var(--text-primary);
      text-align: center;
      white-space: nowrap;
    }

    /* Reduced Motion */
    @media (prefers-reduced-motion: reduce) {
      *, ::before, ::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
      }
    }

    /* EU VAT Print Receipt Sheet */
    @media print {
      body * {
        visibility: hidden !important;
      }
      #print-receipt-sheet, #print-receipt-sheet * {
        visibility: visible !important;
      }
      #print-receipt-sheet {
        position: fixed !important;
        left: 0 !important;
        top: 0 !important;
        width: 100% !important;
        height: 100% !important;
        margin: 0 !important;
        padding: 28px !important;
        background: #ffffff !important;
        color: #000000 !important;
        display: block !important;
        z-index: 999999 !important;
        font-family: 'IBM Plex Mono', monospace, sans-serif !important;
      }
      @page {
        margin: 12mm;
        size: auto;
      }
    }
  </style>
</head>
<body class="min-h-screen flex flex-col antialiased selection:bg-brand-700 selection:text-white">

  <!-- ==================== HEADER (Production Standard & Role-Based) ==================== -->
  <header class="sticky top-0 z-30 bg-surface/95 backdrop-blur-md border-b border-borderSubtle transition-colors duration-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2.5 lg:py-0 lg:h-18 flex flex-col lg:flex-row lg:items-center justify-between gap-2.5">
      
      <!-- Left: Artisanal Brand & Slogan -->
      <div class="flex items-center justify-between w-full lg:w-auto gap-3">
        <a href="#/" onclick="navigateToCatalog(); return false;" class="flex items-center gap-2.5 group">
          <div class="w-9 h-9 rounded-lg bg-brand-700 text-white flex items-center justify-center font-serif font-black text-lg tracking-tight shadow-sm shrink-0 group-hover:scale-105 transition-transform">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" class="inline-block" xmlns="http://www.w3.org/2000/svg">
              <g transform="translate(0 -0.63)">
                <path d="M12 21L3.5 6.5C8.5 3.5 15.5 3.5 20.5 6.5Z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M5.5 9C9.5 7.25 14.5 7.25 18.5 9" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="butt" stroke-linejoin="round"/>
                <circle cx="10.25" cy="11.75" r="1.1" fill="currentColor"/>
                <circle cx="13.75" cy="11.75" r="1.1" fill="currentColor"/>
                <circle cx="12" cy="14.75" r="1.1" fill="currentColor"/>
              </g>
            </svg>
          </div>
          <div>
            <div class="flex items-center gap-1.5 leading-none">
              <span class="font-serif font-extrabold text-textPrimary tracking-tight text-lg sm:text-xl">CROSTA</span>
              <span class="text-[9px] sm:text-[10px] font-mono uppercase tracking-widest text-brand-700 font-bold ml-1">Pizzeria Artigianale</span>
            </div>
            <p class="text-[10px] sm:text-[11px] text-textSecondary hidden sm:block mt-0.5 font-medium">Ремесленная пицца 48ч ферментации · Подовая печь 430°C</p>
          </div>
        </a>

        <!-- Controls on Mobile (Theme + Cart + User) -->
        <div class="flex items-center gap-2 lg:hidden">
          <button onclick="toggleTheme()" aria-label="Переключить тему"
            class="p-2 rounded-lg bg-elevated text-textPrimary border border-borderSubtle text-xs hover:border-textSecondary transition flex items-center justify-center">
            <span class="theme-icon-slot">🌙</span>
          </button>
          
          <button onclick="openCartDrawer()" aria-label="Открыть корзину"
            class="relative p-2 rounded-lg bg-elevated hover:bg-canvas border border-borderSubtle text-textPrimary text-xs font-semibold flex items-center gap-1.5 transition">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" class="text-brand-700" xmlns="http://www.w3.org/2000/svg">
              <path d="M6.215 7.471C6.065 6.616 6.372 6.25 7.24 6.25L19.155 6.25C20.272 6.25 20.654 6.719 20.428 7.812L19.321 13.193C19.096 14.283 18.523 14.75 17.411 14.75L9.136 14.75C7.991 14.75 7.415 14.267 7.216 13.139L6.215 7.471Z" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M2.75 3.25L4.379 3.25C5.143 3.25 5.527 3.572 5.659 4.325L6.2 7.4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
              <circle cx="9.25" cy="19.5" r="1.6" fill="currentColor"/>
              <circle cx="17.5" cy="19.5" r="1.6" fill="currentColor"/>
            </svg>
            <span id="header-cart-count-mobile" class="font-mono text-[10px] px-1.5 py-0.2 bg-brand-700 text-white rounded-full font-bold">0</span>
          </button>

          <div class="header-user-area-slot flex items-center gap-1.5"></div>
        </div>
      </div>

      <!-- Center: Role-Based Navigation -->
      <nav id="header-nav-container" aria-label="Разделы сервиса"
        class="relative flex items-center justify-between w-full lg:w-auto bg-elevated p-1 rounded-xl border border-borderSubtle text-xs sm:text-sm overflow-hidden">
        
        <!-- Sliding Elastic Tab Pill Indicator -->
        <div id="nav-elastic-pill" class="bg-surface rounded-lg shadow-sm border border-borderSubtle"></div>

        <button id="tab-store" onclick="switchView('store')" class="flex-1 lg:flex-initial px-3.5 py-1.5 rounded-lg font-semibold transition text-textPrimary text-center truncate">
          Меню и акции
        </button>
        <button id="tab-track" onclick="switchView('track')" class="flex-1 lg:flex-initial px-3.5 py-1.5 rounded-lg font-medium transition text-textSecondary hover:text-textPrimary text-center truncate">
          Отследить заказ
        </button>
        <!-- Tab Staff is ONLY rendered when role == 'Admin' -->
        <button id="tab-staff" onclick="switchView('staff')" style="display: none;" class="flex-1 lg:flex-initial px-3 py-1.5 rounded-lg font-medium transition text-textSecondary hover:text-textPrimary items-center justify-center gap-1.5 text-center truncate">
          <span>Управление (Админ)</span>
          <span id="active-orders-badge" class="font-mono text-[10px] px-1.5 py-0.2 bg-brand-700 text-white rounded-full font-bold leading-none">0</span>
        </button>
      </nav>

      <!-- Right Controls on Desktop: Theme + Cart Button + User Pill -->
      <div class="hidden lg:flex items-center gap-3">
        <!-- Theme Toggle -->
        <button onclick="toggleTheme()" aria-label="Переключить тему"
          class="p-2 rounded-lg bg-elevated text-textPrimary border border-borderSubtle hover:border-textSecondary transition text-sm flex items-center justify-center">
          <span class="theme-icon-slot">🌙</span>
        </button>

        <!-- Slide-over Cart Drawer Trigger -->
        <button id="header-cart-btn" onclick="openCartDrawer()" aria-label="Открыть корзину"
          class="relative px-3.5 py-2 rounded-lg bg-elevated hover:bg-canvas border border-borderSubtle text-textPrimary text-xs sm:text-sm font-semibold flex items-center gap-2 transition shadow-xs active:scale-97">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" class="text-brand-700" xmlns="http://www.w3.org/2000/svg">
            <path d="M6.215 7.471C6.065 6.616 6.372 6.25 7.24 6.25L19.155 6.25C20.272 6.25 20.654 6.719 20.428 7.812L19.321 13.193C19.096 14.283 18.523 14.75 17.411 14.75L9.136 14.75C7.991 14.75 7.415 14.267 7.216 13.139L6.215 7.471Z" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M2.75 3.25L4.379 3.25C5.143 3.25 5.527 3.572 5.659 4.325L6.2 7.4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
            <circle cx="9.25" cy="19.5" r="1.6" fill="currentColor"/>
            <circle cx="17.5" cy="19.5" r="1.6" fill="currentColor"/>
          </svg>
          <span>Корзина</span>
          <span id="header-cart-count" class="font-mono text-[11px] px-1.5 py-0.2 rounded-full bg-brand-700 text-white font-bold leading-none">0</span>
          <span id="header-cart-total" class="font-mono text-xs font-bold text-textPrimary tabular-nums">€0.00</span>
        </button>

        <!-- User Authentication Slot (Guest: "Войти", Customer: Pill with David + €14.50, Admin: Elena) -->
        <div class="header-user-area-slot flex items-center gap-2"></div>
      </div>

    </div>
  </header>

  <!-- ==================== MOBILE FLOATING CART (390×844) ==================== -->
  <div id="mobile-floating-cart" class="fixed bottom-3 left-3 right-3 z-40 lg:hidden hidden">
    <button type="button" onclick="openCartDrawer()"
      class="w-full py-3.5 px-4 bg-brand-700 hover:bg-brand-800 text-white rounded-2xl shadow-2xl flex items-center justify-between border border-brand-800 transition active:scale-98">
      <div class="flex items-center gap-2.5">
        <div class="w-7 h-7 rounded-full bg-white/20 flex items-center justify-center">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" class="text-white" xmlns="http://www.w3.org/2000/svg">
            <path d="M6.215 7.471C6.065 6.616 6.372 6.25 7.24 6.25L19.155 6.25C20.272 6.25 20.654 6.719 20.428 7.812L19.321 13.193C19.096 14.283 18.523 14.75 17.411 14.75L9.136 14.75C7.991 14.75 7.415 14.267 7.216 13.139L6.215 7.471Z" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M2.75 3.25L4.379 3.25C5.143 3.25 5.527 3.572 5.659 4.325L6.2 7.4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
            <circle cx="9.25" cy="19.5" r="1.6" fill="currentColor"/>
            <circle cx="17.5" cy="19.5" r="1.6" fill="currentColor"/>
          </svg>
        </div>
        <span class="text-xs sm:text-sm font-semibold">Корзина · <strong id="mfc-count" class="font-mono">0</strong> поз.</span>
      </div>
      <div class="flex items-center gap-2 font-mono text-sm font-bold">
        <span id="mfc-total">€0.00</span>
        <span class="font-sans font-semibold text-xs text-white/90">→ Оформить</span>
      </div>
    </button>
  </div>

  <!-- Toast Notification Container -->
  <div id="toast-container" aria-live="polite" class="fixed bottom-20 sm:bottom-4 right-3 sm:right-4 z-50 flex flex-col gap-2 max-w-sm w-full pointer-events-none px-2 sm:px-0"></div>

  <!-- ==================== MAIN WORKSPACE ==================== -->
  <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">

    <!-- ===================================================================== -->
    <!-- VIEW 1: STOREFRONT & PROMOTIONS (Full 3-Column Catalog Grid)           -->
    <!-- ===================================================================== -->
    <section id="view-store" class="space-y-8">

      <!-- Hero Section with Word Roll and Editorial Atmosphere -->
      <div id="hero-card" class="relative overflow-hidden rounded-2xl border border-borderSubtle bg-surface p-6 sm:p-10 transition-colors shadow-xs">
        <div class="max-w-3xl space-y-4">
          <div id="hero-badge" class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-elevated border border-borderSubtle text-xs font-mono font-medium text-textSecondary">
            <span class="w-2 h-2 rounded-full bg-brand-700 animate-pulse"></span>
            Подовая печь 430°C · Мука Tipo 00 · Закваска Lievito Madre 48ч
          </div>
          <h1 id="hero-title" class="text-2xl sm:text-4xl lg:text-[42px] font-serif font-bold text-textPrimary tracking-tight leading-tight">
            <div class="roll flex flex-wrap items-baseline gap-x-2 gap-y-1" id="hero-word-roll" role="button" tabindex="0" title="Кликните для переключения" aria-label="Неаполитанская пицца для всей семьи">
              <span class="lead text-textPrimary font-bold">Неаполитанская пицца для</span>
              <span class="slot text-brand-700 font-bold" id="hero-roll-slot"></span>
            </div>
          </h1>
          <p id="hero-desc" class="text-xs sm:text-base text-textSecondary leading-relaxed">
            Каждое утро мы замешиваем тесто длительной холодной ферментации на живой закваске. 
            Прямые поставки томатов San Marzano DOP, моцареллы Fior di Latte и оливкового масла первого отжима из Италии.
            Цены включают НДС ЕС (10%), а при заказе от €25.00 доставка полностью бесплатна.
          </p>
        </div>
      </div>

      <!-- Live Promotions Strip (From GET /api/promotions) -->
      <div class="space-y-3">
        <div class="flex items-center justify-between">
          <h2 class="text-xs sm:text-sm font-bold text-textPrimary uppercase tracking-wider font-mono flex items-center gap-2">
            <span>Сезонные акции и промокоды</span>
            <span class="text-xs font-normal text-textSecondary lowercase hidden sm:inline">(кликните карточку для применения в корзине)</span>
          </h2>
        </div>
        <div id="promotions-grid" class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <!-- Rendered via JS -->
        </div>
      </div>

      <!-- Menu Section Header & Command Search Bar -->
      <div class="space-y-4">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-borderSubtle">
          <div>
            <h2 class="text-xl sm:text-2xl font-serif font-bold text-textPrimary tracking-tight">Каталог ремесленной пиццы</h2>
            <p class="text-xs text-textSecondary mt-0.5">Выберите диаметр: S (25 см), M (30 см) или L (35 см). Переключение размеров работает без задержек.</p>
          </div>

          <!-- Command Search Bar (⌘K / Ctrl+K) -->
          <div id="command-search-wrapper" class="relative w-full sm:w-80">
            <div id="command-search-bar" class="flex items-center w-full px-3.5 py-2 text-xs sm:text-sm bg-elevated border border-borderSubtle rounded-xl text-textPrimary transition focus-within:ring-2 focus-within:ring-brand-700">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" class="text-textSecondary shrink-0 mr-2" xmlns="http://www.w3.org/2000/svg">
                <circle cx="10.5" cy="10.5" r="7" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
                <path d="M15.6 15.6L20.5 20.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
              </svg>
              <input id="search-input" type="search" aria-label="Поиск по меню" placeholder="Поиск пиццы или аллергенов..."
                oninput="renderMenu()"
                class="w-full bg-transparent border-0 outline-none text-textPrimary placeholder:text-textSecondary text-xs sm:text-sm" />
              <kbd class="hidden sm:inline-block px-1.5 py-0.5 rounded bg-surface border border-borderSubtle font-mono text-[10px] text-textSecondary shrink-0 ml-1">⌘K</kbd>
            </div>
          </div>
        </div>

        <!-- Category Filters -->
        <div id="category-filters" class="flex flex-wrap items-center gap-2">
          <button onclick="setCategory('Все')" data-cat="Все" class="cat-btn px-3 py-1.5 rounded-lg text-xs font-semibold bg-textPrimary text-canvas shadow-xs">Все позиции</button>
          <button onclick="setCategory('Классика')" data-cat="Классика" class="cat-btn px-3 py-1.5 rounded-lg text-xs font-medium bg-elevated text-textPrimary hover:border-textSecondary border border-borderSubtle">Классика</button>
          <button onclick="setCategory('Мясные')" data-cat="Мясные" class="cat-btn px-3 py-1.5 rounded-lg text-xs font-medium bg-elevated text-textPrimary hover:border-textSecondary border border-borderSubtle">Мясные</button>
          <button onclick="setCategory('Сырные')" data-cat="Сырные" class="cat-btn px-3 py-1.5 rounded-lg text-xs font-medium bg-elevated text-textPrimary hover:border-textSecondary border border-borderSubtle">Сырные</button>
          <button onclick="setCategory('Премиум')" data-cat="Премиум" class="cat-btn px-3 py-1.5 rounded-lg text-xs font-medium bg-elevated text-textPrimary hover:border-textSecondary border border-borderSubtle">Премиум</button>
          <button onclick="setCategory('Овощные')" data-cat="Овощные" class="cat-btn px-3 py-1.5 rounded-lg text-xs font-medium bg-elevated text-textPrimary hover:border-textSecondary border border-borderSubtle">Овощные / Веган</button>
        </div>
      </div>

      <!-- Main Menu Cards Grid (Clean 3 Columns on Desktop, without heavy checkout column!) -->
      <div id="menu-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"></div>

    </section>

    <!-- ===================================================================== -->
    <!-- VIEW 2: PRODUCT DETAIL PAGE (Hash Routed #/pizza/:sku)                 -->
    <!-- ===================================================================== -->
    <section id="view-product-detail" class="hidden space-y-6 max-w-5xl mx-auto">
      
      <!-- Back Navigation Header -->
      <div class="flex items-center justify-between">
        <button type="button" onclick="navigateToCatalog()" class="inline-flex items-center gap-2 text-xs sm:text-sm font-semibold text-textSecondary hover:text-textPrimary transition">
          <span class="text-base leading-none">&larr;</span>
          <span>Вернуться в меню</span>
        </button>
        <div id="detail-category-badge" class="px-3 py-1 rounded-full text-xs font-mono font-semibold bg-elevated text-brand-700 border border-borderSubtle">
          Категория
        </div>
      </div>

      <!-- Detail Card -->
      <div class="bg-surface border border-borderSubtle rounded-2xl p-6 sm:p-8 grid grid-cols-1 md:grid-cols-12 gap-8 items-start shadow-xs transition-colors">
        
        <!-- Left: Pizza Illustration & Artisanal Facts -->
        <div class="md:col-span-5 flex flex-col items-center text-center space-y-4">
          <div id="detail-illustration-slot" class="w-64 h-64 sm:w-72 sm:h-72 flex items-center justify-center p-2"></div>
          <div class="p-3.5 bg-elevated rounded-xl border border-borderSubtle text-xs text-textSecondary w-full text-left space-y-1.5">
            <div class="flex items-center gap-2 font-bold text-textPrimary">
              <span class="w-2 h-2 rounded-full bg-brand-700 animate-pulse"></span>
              <span>48 часов холодной ферментации</span>
            </div>
            <p>Натуральная закваска Lievito Madre, мука мягких сортов Tipo 00. Выпекается 90 секунд в подовой печи при 430°C до образования леопардового кратера.</p>
          </div>
        </div>

        <!-- Right: Specs, Sizing, Toppings, Nutrition, Add to Cart -->
        <div class="md:col-span-7 space-y-5">
          <div>
            <div class="flex items-center gap-2">
              <span id="detail-sku" class="font-mono text-xs text-textSecondary font-semibold">PZ-000</span>
              <span id="detail-dietary" class="px-2 py-0.2 rounded text-[10px] font-semibold bg-elevated text-textSecondary border border-borderSubtle">Тег</span>
            </div>
            <h1 id="detail-name" class="text-2xl sm:text-3xl font-serif font-bold text-textPrimary tracking-tight mt-1">Название пиццы</h1>
            <p id="detail-desc" class="text-xs sm:text-sm text-textSecondary mt-2 leading-relaxed"></p>
          </div>

          <!-- Ingredients List -->
          <div class="space-y-1.5 pt-2 border-t border-borderSubtle">
            <h3 class="text-xs font-bold text-textPrimary uppercase tracking-wider font-mono">Состав и происхождение</h3>
            <p id="detail-ingredients" class="text-xs text-textSecondary leading-relaxed"></p>
          </div>

          <!-- Allergens & Nutrition Grid -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
            <div class="bg-elevated p-3.5 rounded-xl border border-borderSubtle space-y-1.5">
              <h4 class="text-[11px] font-bold text-textPrimary uppercase tracking-wider font-mono">Аллергены ЕС (1169/2011)</h4>
              <div id="detail-allergens" class="flex flex-wrap gap-1 pt-0.5"></div>
            </div>
            <div class="bg-elevated p-3.5 rounded-xl border border-borderSubtle space-y-1.5">
              <h4 class="text-[11px] font-bold text-textPrimary uppercase tracking-wider font-mono">КБЖУ на порцию</h4>
              <div id="detail-nutrition" class="grid grid-cols-4 gap-1 text-center font-mono text-xs pt-0.5"></div>
            </div>
          </div>

          <!-- Size Selector -->
          <div class="space-y-2 pt-2 border-t border-borderSubtle">
            <label class="block text-xs font-bold text-textPrimary uppercase tracking-wider font-mono">Диаметр пиццы</label>
            <div id="detail-size-options" class="grid grid-cols-3 gap-2"></div>
          </div>

          <!-- Extra Crust / Toppings -->
          <div class="space-y-2 pt-2">
            <label class="block text-xs font-bold text-textPrimary uppercase tracking-wider font-mono">Дополнительные опции и бортик</label>
            <div id="detail-toppings-options" class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs"></div>
          </div>

          <!-- Add to Cart with Quantity -->
          <div class="flex items-center justify-between gap-4 pt-4 border-t border-borderSubtle">
            <div>
              <span class="text-xs text-textSecondary block">Итоговая стоимость</span>
              <span id="detail-price-total" class="font-mono text-2xl font-bold text-textPrimary tabular-nums">€0.00</span>
            </div>
            <div class="flex items-center gap-3">
              <div class="flex items-center gap-2 bg-elevated border border-borderSubtle rounded-xl p-1">
                <button type="button" onclick="changeDetailQty(-1)" class="w-7 h-7 rounded-lg bg-surface border border-borderSubtle font-bold text-xs hover:bg-elevated text-textPrimary">-</button>
                <span id="detail-qty-val" class="font-mono text-xs font-bold w-6 text-center text-textPrimary">1</span>
                <button type="button" onclick="changeDetailQty(1)" class="w-7 h-7 rounded-lg bg-surface border border-borderSubtle font-bold text-xs hover:bg-elevated text-textPrimary">+</button>
              </div>
              <button type="button" id="btn-detail-add" onclick="addDetailToCart()"
                class="px-5 py-3 bg-brand-700 hover:bg-brand-800 text-white font-semibold text-xs sm:text-sm rounded-xl shadow-sm transition flex items-center gap-2 active:scale-97">
                <span>В корзину</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Guest Reviews & Star Rating Section -->
      <div class="bg-surface border border-borderSubtle rounded-2xl p-6 sm:p-8 space-y-4 shadow-xs transition-colors">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-borderSubtle">
          <div>
            <h3 class="text-base sm:text-lg font-serif font-bold text-textPrimary">Отзывы гостей и ценителей</h3>
            <p class="text-xs text-textSecondary">Средняя оценка 4.9 из 5 на основе 140+ отзывов в Риме и Неаполе</p>
          </div>
          <button type="button" onclick="toggleReviewForm()" class="px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-elevated border border-borderSubtle text-textPrimary hover:border-textSecondary transition self-start sm:self-auto">
            + Оставить отзыв
          </button>
        </div>

        <!-- DesignBookmark Star Rating & Review Form -->
        <div id="detail-review-form" class="hidden p-5 rounded-2xl bg-elevated border border-borderSubtle space-y-4 shadow-sm">
          <div class="text-center space-y-1">
            <h4 class="text-sm font-serif font-bold text-textPrimary">Как вам понравилась пицца?</h4>
            <p class="text-[11px] text-textSecondary">Наведите курсор и выберите количество звёзд</p>
          </div>

          <!-- Interactive Star Rating Component Slot -->
          <div id="detail-star-rating-slot" class="flex justify-center"></div>

          <div class="space-y-1.5 pt-1">
            <label for="detail-review-input" class="block text-xs font-semibold text-textPrimary">Ваш отзыв</label>
            <textarea id="detail-review-input" rows="2" placeholder="Поделитесь впечатлением о тесте, соусе или хрустящей корочке..."
              class="w-full px-3.5 py-2 text-xs bg-canvas border border-borderSubtle rounded-xl text-textPrimary focus:ring-1 focus:ring-brand-700"></textarea>
          </div>

          <div class="flex justify-end gap-2 pt-1">
            <button type="button" onclick="toggleReviewForm()" class="px-4 py-2 text-xs font-medium rounded-xl bg-surface border border-borderSubtle text-textSecondary hover:text-textPrimary transition">Отмена</button>
            <button type="button" onclick="submitDetailReview()" class="px-4 py-2 text-xs font-semibold rounded-xl bg-brand-700 hover:bg-brand-800 text-white transition shadow-sm active:scale-97">Опубликовать отзыв</button>
          </div>
        </div>

        <!-- Reviews Grid -->
        <div id="detail-reviews-list" class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs"></div>
      </div>
    </section>

    <!-- ===================================================================== -->
    <!-- VIEW 3: TRACKING (Отслеживание статуса заказа)                         -->
    <!-- ===================================================================== -->
    <section id="view-track" class="hidden max-w-4xl mx-auto space-y-6">
      <div class="bg-surface border border-borderSubtle rounded-2xl p-6 sm:p-8 space-y-4 shadow-xs transition-colors">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h2 class="text-xl sm:text-2xl font-serif font-bold text-textPrimary">Отслеживание статуса заказа</h2>
            <p class="text-xs text-textSecondary mt-0.5">Введите номер заказа или выберите один из активных для просмотра хронологии подовой печи и курьера.</p>
          </div>
          <!-- Print Receipt Button -->
          <button type="button" onclick="printReceipt()"
            class="self-start sm:self-auto px-3.5 py-2 rounded-xl bg-elevated border border-borderSubtle text-textPrimary hover:border-textSecondary text-xs font-semibold flex items-center gap-2 transition active:scale-97">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" class="text-textPrimary" xmlns="http://www.w3.org/2000/svg">
              <path d="M2.75 11.14C2.75 8.592 3.842 7.5 6.39 7.5L17.61 7.5C20.158 7.5 21.25 8.592 21.25 11.14L21.25 13.36C21.25 15.908 20.158 17 17.61 17L6.39 17C3.842 17 2.75 15.908 2.75 13.36L2.75 11.14Z" stroke="currentColor" stroke-width="1.6"/>
              <path d="M7 7.5L7 4.3C7 3.39 7.39 3 8.3 3L15.7 3C16.61 3 17 3.39 17 4.3L17 7.5" stroke="currentColor" stroke-width="1.6"/>
              <path d="M7 17L7 19.7C7 20.61 7.39 21 8.3 21L15.7 21C16.61 21 17 20.61 17 19.7L17 17" stroke="currentColor" stroke-width="1.6"/>
              <circle cx="17.5" cy="11" r="1" fill="currentColor"/>
            </svg>
            <span>Распечатать чек (EU VAT)</span>
          </button>
        </div>

        <div class="flex gap-2">
          <input id="track-search-input" type="text" placeholder="Например: ORD-2026-104"
            class="flex-1 px-3.5 py-2.5 text-xs sm:text-sm bg-elevated border border-borderSubtle rounded-xl text-textPrimary font-mono focus:ring-2 focus:ring-brand-700" />
          <button onclick="searchTrackedOrder()"
            class="px-5 py-2.5 bg-textPrimary text-canvas text-xs sm:text-sm font-semibold rounded-xl hover:opacity-90 transition active:scale-97">
            Найти заказ
          </button>
        </div>

        <div id="quick-order-pills" class="flex flex-wrap items-center gap-1.5 text-xs pt-1"></div>
      </div>

      <!-- Order Detail Card with 5-Step Stepper & Star Rating -->
      <div id="tracked-order-card" class="bg-surface border border-borderSubtle rounded-2xl p-6 sm:p-8 shadow-xs transition-colors"></div>
    </section>

    <!-- ===================================================================== -->
    <!-- VIEW 4: PROFILE & BONUSES (Личный кабинет клиента)                     -->
    <!-- ===================================================================== -->
    <section id="view-profile" class="hidden max-w-5xl mx-auto space-y-6">
      
      <!-- Guest State (Shown if not logged in) -->
      <div id="profile-guest-card" class="bg-surface border border-borderSubtle rounded-2xl p-8 sm:p-12 text-center space-y-4 shadow-xs">
        <div class="w-14 h-14 mx-auto rounded-full bg-elevated border border-borderSubtle flex items-center justify-center text-2xl text-brand-700 font-bold">
          ★
        </div>
        <h3 class="text-xl font-serif font-bold text-textPrimary">Личный кабинет и бонусный клуб CROSTA</h3>
        <p class="text-xs sm:text-sm text-textSecondary max-w-md mx-auto leading-relaxed">
          Войдите или зарегистрируйтесь, чтобы копить 5% кэшбэк с каждого заказа, оплачивать бонусами до 30% стоимости пицц и сохранять персональные адреса доставки.
        </p>
        <button onclick="openAuthModal('login')" class="px-6 py-2.5 bg-brand-700 hover:bg-brand-800 text-white font-semibold text-xs sm:text-sm rounded-xl shadow-sm transition active:scale-97">
          Войти / Регистрация
        </button>
      </div>

      <!-- Logged-in Customer Content -->
      <div id="profile-user-content" class="hidden space-y-6">
        <!-- Top Loyalty Grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
          <!-- Balance Gold Card -->
          <div class="md:col-span-1 rounded-2xl p-6 bg-gradient-to-br from-amber-950 via-stone-900 to-amber-900 text-white shadow-lg relative overflow-hidden flex flex-col justify-between border border-amber-900/50">
            <div class="space-y-1">
              <span class="text-xs uppercase tracking-wider text-amber-200 font-mono font-semibold">CROSTA Club Privé</span>
              <h3 class="text-xs text-stone-300">Баланс бонусных баллов (1 балл = €1.00)</h3>
              <p id="profile-bonus-balance" class="text-3xl sm:text-4xl font-extrabold font-mono text-amber-100 tabular-nums pt-2">€0.00</p>
            </div>
            <div class="pt-4 border-t border-amber-800/60 text-xs text-stone-300 space-y-1">
              <p>• Оплачивайте бонусами <strong>до 30%</strong> от суммы блюд.</p>
              <p>• Начисление <strong>5% кэшбэка</strong> с каждого заказа.</p>
            </div>
          </div>

          <!-- User Contact Info & Edit -->
          <div class="md:col-span-2 bg-surface border border-borderSubtle rounded-2xl p-6 flex flex-col justify-between shadow-xs transition-colors">
            <div class="flex items-start justify-between">
              <div>
                <div class="flex items-center gap-2">
                  <h3 id="profile-full-name" class="text-lg font-bold text-textPrimary">Имя Пользователя</h3>
                  <span id="profile-role-badge" class="px-2 py-0.5 rounded text-[11px] font-mono font-semibold bg-elevated text-textSecondary border border-borderSubtle">Customer</span>
                </div>
                <p id="profile-email" class="text-xs text-textSecondary font-mono mt-0.5">user@crosta.eu</p>
              </div>
              <button onclick="toggleProfileEditModal(true)" class="px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-elevated text-textPrimary border border-borderSubtle hover:border-textSecondary transition active:scale-97">
                Редактировать адрес
              </button>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-4 pt-4 border-t border-borderSubtle text-xs">
              <div>
                <span class="text-textSecondary block">Основной телефон:</span>
                <p id="profile-phone" class="font-mono font-medium text-textPrimary mt-0.5">—</p>
              </div>
              <div>
                <span class="text-textSecondary block">Адрес по умолчанию:</span>
                <p id="profile-address" class="font-medium text-textPrimary mt-0.5">—</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Bonus Transactions History -->
        <div class="bg-surface border border-borderSubtle rounded-2xl p-6 space-y-4 shadow-xs transition-colors">
          <div class="flex items-center justify-between">
            <h3 class="text-base font-serif font-bold text-textPrimary">Журнал начисления и списания бонусов</h3>
            <span class="text-xs text-textSecondary font-mono">SQLite Transactional Log</span>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs">
              <thead>
                <tr class="border-b border-borderSubtle text-textSecondary">
                  <th class="py-2.5 px-3">Дата/Время UTC</th>
                  <th class="py-2.5 px-3">Тип</th>
                  <th class="py-2.5 px-3">Заказ</th>
                  <th class="py-2.5 px-3">Описание</th>
                  <th class="py-2.5 px-3 text-right">Сумма баллов</th>
                </tr>
              </thead>
              <tbody id="profile-bonus-tbody"></tbody>
            </table>
          </div>
        </div>

        <!-- Past Orders with "Repeat Order" -->
        <div class="bg-surface border border-borderSubtle rounded-2xl p-6 space-y-4 shadow-xs transition-colors">
          <div class="flex items-center justify-between">
            <h3 class="text-base font-serif font-bold text-textPrimary">История ваших заказов</h3>
            <span class="text-xs text-textSecondary">Повторяйте любимые пиццы в 1 клик</span>
          </div>
          <div id="profile-orders-list" class="space-y-3"></div>
        </div>
      </div>
    </section>

    <!-- ===================================================================== -->
    <!-- VIEW 5: STAFF & ADMIN DASHBOARD (Only Accessible if Role == 'Admin')  -->
    <!-- ===================================================================== -->
    <section id="view-staff" class="hidden space-y-6">

      <!-- Staff Header -->
      <div class="bg-surface border border-borderSubtle rounded-2xl p-6 flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-xs transition-colors">
        <div>
          <div class="flex items-center gap-2.5">
            <h2 class="text-xl sm:text-2xl font-serif font-bold text-textPrimary">Диспетчерская панель CROSTA</h2>
            <span class="px-2 py-0.5 rounded text-[11px] font-mono font-semibold bg-emerald-100 text-emerald-800 border border-emerald-300">SQLite Live Sync</span>
          </div>
          <p class="text-xs text-textSecondary mt-1">Управление подовой печью, очередью кухни, курьерской электродоставкой и стоп-листом.</p>
        </div>

        <div class="flex items-center gap-3">
          <div class="text-xs text-textSecondary">
            <label for="staff-role-select" class="block font-medium mb-1">Режим диспетчера:</label>
            <select id="staff-role-select" onchange="renderStaffDashboard()"
              class="px-3 py-1.5 bg-elevated border border-borderSubtle rounded-lg text-textPrimary font-semibold">
              <option value="Manager">Менеджер смены (Полный доступ)</option>
              <option value="Kitchen">Шеф-пиццайоло (Кухня и печь)</option>
              <option value="Courier">Курьер (Электродоставка)</option>
            </select>
          </div>
          <button id="btn-open-new-pizza" onclick="toggleNewPizzaModal(true)"
            class="mt-4 px-3.5 py-1.5 bg-brand-700 hover:bg-brand-800 text-white text-xs font-semibold rounded-lg transition shadow-sm active:scale-97">
            + Новая пицца
          </button>
        </div>
      </div>

      <!-- Real-Time Admin KPI & Bezier Trend Stat Cards -->
      <div id="admin-stats-container" class="space-y-6">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4" id="staff-kpis"></div>

        <!-- Bezier Revenue Trend Chart -->
        <div class="bg-surface border border-borderSubtle rounded-2xl p-6 space-y-3 shadow-xs transition-colors">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <h3 class="text-sm font-bold text-textPrimary uppercase tracking-wider font-mono">Динамика выручки и средний чек</h3>
              <p class="text-xs text-textSecondary">Интерактивный график 12 временных точек с плавной Безье-интерполяцией</p>
            </div>
            <!-- Segmented Period Switcher -->
            <div class="flex items-center gap-1 bg-elevated p-1 rounded-lg border border-borderSubtle self-start sm:self-auto text-xs">
              <button type="button" onclick="setChartPeriod('day')" id="chart-btn-day" class="px-2.5 py-1 rounded-md font-semibold bg-surface text-textPrimary shadow-xs transition">День</button>
              <button type="button" onclick="setChartPeriod('week')" id="chart-btn-week" class="px-2.5 py-1 rounded-md font-medium text-textSecondary hover:text-textPrimary transition">Неделя</button>
              <button type="button" onclick="setChartPeriod('month')" id="chart-btn-month" class="px-2.5 py-1 rounded-md font-medium text-textSecondary hover:text-textPrimary transition">Месяц</button>
            </div>
          </div>

          <!-- SVG Bezier Trend Line -->
          <div class="w-full pt-2">
            <svg id="admin-revenue-chart" viewBox="0 0 700 120" class="w-full h-24 overflow-visible">
              <defs>
                <linearGradient id="chartGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stop-color="#B91C1C" stop-opacity="0.25"/>
                  <stop offset="100%" stop-color="#B91C1C" stop-opacity="0.0"/>
                </linearGradient>
              </defs>
              <path id="chart-area" d="M 0 120 L 0 60 Q 350 20 700 40 L 700 120 Z" fill="url(#chartGrad)"/>
              <path id="chart-curve" d="M 0 60 Q 350 20 700 40" fill="none" stroke="var(--accent-primary)" stroke-width="2.5" stroke-linecap="round"/>
              <circle id="chart-dot" cx="700" cy="40" r="4.5" fill="var(--accent-primary)" stroke="var(--bg-surface)" stroke-width="2"/>
            </svg>
            <div class="flex justify-between text-[10px] font-mono text-textSecondary pt-1">
              <span>08:00</span>
              <span>12:00</span>
              <span>15:00</span>
              <span>18:00</span>
              <span>21:00</span>
              <span>Сейчас</span>
            </div>
          </div>
        </div>

        <!-- Top Pizzas & Status Distribution Visual Cards -->
        <div class="grid grid-cols-1 md:grid-cols-12 gap-5">
          <!-- Top Pizzas Histogram -->
          <div class="md:col-span-7 bg-surface border border-borderSubtle rounded-2xl p-6 space-y-3 shadow-xs transition-colors">
            <h3 class="text-sm font-bold text-textPrimary uppercase tracking-wider font-mono">Топ-5 пицц по продажам</h3>
            <div id="admin-top-pizzas" class="space-y-2.5 pt-1"></div>
          </div>

          <!-- Orders by Status Grid -->
          <div class="md:col-span-5 bg-surface border border-borderSubtle rounded-2xl p-6 space-y-3 shadow-xs transition-colors">
            <h3 class="text-sm font-bold text-textPrimary uppercase tracking-wider font-mono">Распределение по статусам</h3>
            <div id="admin-status-distribution" class="grid grid-cols-2 gap-2 pt-1"></div>
          </div>
        </div>
      </div>

      <!-- Live Order Dispatch Table -->
      <div class="bg-surface border border-borderSubtle rounded-2xl p-6 space-y-4 shadow-xs transition-colors">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div class="flex flex-wrap items-center gap-1.5">
            <button onclick="setStaffFilter('All')" data-st="All" class="st-btn px-3 py-1.5 rounded-lg text-xs font-semibold bg-textPrimary text-canvas shadow-xs">Все заказы</button>
            <button onclick="setStaffFilter('New')" data-st="New" class="st-btn px-3 py-1.5 rounded-lg text-xs font-medium bg-elevated text-textPrimary hover:border-textSecondary border border-borderSubtle">Новые</button>
            <button onclick="setStaffFilter('Preparing')" data-st="Preparing" class="st-btn px-3 py-1.5 rounded-lg text-xs font-medium bg-elevated text-textPrimary hover:border-textSecondary border border-borderSubtle">Подготовка</button>
            <button onclick="setStaffFilter('Baking')" data-st="Baking" class="st-btn px-3 py-1.5 rounded-lg text-xs font-medium bg-elevated text-textPrimary hover:border-textSecondary border border-borderSubtle">В печи 430°C</button>
            <button onclick="setStaffFilter('OutForDelivery')" data-st="OutForDelivery" class="st-btn px-3 py-1.5 rounded-lg text-xs font-medium bg-elevated text-textPrimary hover:border-textSecondary border border-borderSubtle">В доставке</button>
            <button onclick="setStaffFilter('Delivered')" data-st="Delivered" class="st-btn px-3 py-1.5 rounded-lg text-xs font-medium bg-elevated text-textPrimary hover:border-textSecondary border border-borderSubtle">Доставлены</button>
          </div>
          <button onclick="loadAllData()" class="text-xs text-brand-700 hover:text-brand-800 font-semibold flex items-center gap-1 self-start sm:self-auto">
            <span>⟳ Обновить данные</span>
          </button>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs">
            <thead>
              <tr class="border-b border-borderSubtle text-textSecondary">
                <th class="py-3 px-4">Заказ / Время</th>
                <th class="py-3 px-4">Клиент и адрес</th>
                <th class="py-3 px-4">Состав заказа</th>
                <th class="py-3 px-4">Сумма (EUR)</th>
                <th class="py-3 px-4">Текущий статус</th>
                <th class="py-3 px-4 text-right">Действие по этапу</th>
              </tr>
            </thead>
            <tbody id="staff-orders-tbody" class="divide-y divide-borderSubtle"></tbody>
          </table>
        </div>
      </div>

      <!-- Menu Availability Management (Stop-List) -->
      <div class="bg-surface border border-borderSubtle rounded-2xl p-6 space-y-4 shadow-xs transition-colors">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-base font-serif font-bold text-textPrimary">Управление меню и стоп-листом кухни</h3>
            <p class="text-xs text-textSecondary">Мгновенное скрытие или возвращение позиций в каталоге</p>
          </div>
        </div>
        <div id="admin-stop-list" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3"></div>
      </div>

    </section>

  </main>

  <!-- ==================== FOOTER ==================== -->
  <footer class="mt-auto border-t border-borderSubtle bg-surface transition-colors py-8 text-xs text-textSecondary">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
      <div>
        <p class="font-serif font-bold text-textPrimary text-sm">CROSTA Artisanal Pizza Europe &copy; 2026</p>
        <p class="text-[11px] mt-0.5">Разработано в строгом соответствии с европейскими стандартами качества (GDPR / EU VAT 10%)</p>
      </div>
      <div class="flex items-center gap-4 text-[11px] font-mono text-textSecondary">
        <span>ASP.NET Core 8 Minimal API</span>
        <span>·</span>
        <span>SQLite WAL</span>
        <span>·</span>
        <span>Vanilla JS + GSAP</span>
      </div>
    </div>
  </footer>

  <!-- ==================== SLIDE-OVER CART DRAWER ==================== -->
  <div id="cart-drawer" class="fixed inset-0 z-50 pointer-events-none transition-visibility duration-300">
    <!-- Backdrop Blur -->
    <div id="cart-drawer-backdrop" onclick="closeCartDrawer()"
      class="fixed inset-0 bg-black/50 opacity-0 pointer-events-none transition-opacity duration-300 backdrop-blur-xs"></div>
    
    <!-- Slide-over Panel -->
    <aside id="cart-drawer-panel"
      class="fixed top-0 right-0 bottom-0 w-full max-w-md bg-surface border-l border-borderSubtle shadow-2xl flex flex-col pointer-events-auto transform translate-x-full transition-transform duration-300 ease-out z-10 overflow-hidden">
      
      <!-- Drawer Header -->
      <div class="p-4 sm:p-5 border-b border-borderSubtle flex items-center justify-between shrink-0 bg-surface">
        <div class="flex items-center gap-2">
          <div class="w-7 h-7 rounded-lg bg-brand-700 text-white flex items-center justify-center font-bold text-xs">
            🍕
          </div>
          <div>
            <h2 class="text-base font-serif font-bold text-textPrimary">Ваш заказ</h2>
            <p class="text-[11px] text-textSecondary">Бесплатная доставка от €25.00</p>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <span id="cart-count-pill" class="font-mono text-xs font-semibold px-2 py-0.5 rounded-lg bg-elevated text-textPrimary border border-borderSubtle">0 поз.</span>
          <button type="button" onclick="closeCartDrawer()" class="p-1.5 rounded-lg text-textSecondary hover:text-textPrimary hover:bg-elevated transition">
            <span class="text-xl leading-none">&times;</span>
          </button>
        </div>
      </div>

      <!-- Scrollable Drawer Body -->
      <div class="flex-1 overflow-y-auto p-4 sm:p-5 space-y-4">
        
        <!-- Cart Items List -->
        <div id="cart-items" class="space-y-2"></div>

        <!-- Promo Code Box -->
        <div id="cart-promo-box" class="p-3.5 rounded-xl bg-elevated border border-borderSubtle space-y-2 text-xs">
          <div class="flex items-center justify-between">
            <span class="font-bold text-textPrimary flex items-center gap-1.5">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" class="text-brand-700" xmlns="http://www.w3.org/2000/svg">
                <path d="M11.258 3.116C11.777 2.755 12.223 2.755 12.742 3.116L14.79 4.54C14.953 4.653 15.107 4.716 15.302 4.752L17.757 5.193C18.38 5.305 18.695 5.62 18.807 6.243L19.248 8.698C19.284 8.893 19.347 9.047 19.46 9.21L20.884 11.258C21.245 11.777 21.245 12.223 20.884 12.742L19.46 14.79C19.347 14.953 19.284 15.107 19.248 15.302L18.807 17.757C18.695 18.38 18.38 18.695 17.757 18.807L15.302 19.248C15.107 19.284 14.953 19.347 14.79 19.46L12.742 20.884C12.223 21.245 11.777 21.245 11.258 20.884L9.21 19.46C9.047 19.347 8.893 19.284 8.698 19.248L6.243 18.807C5.62 18.695 5.305 18.38 5.193 17.757L4.752 15.302C4.716 15.107 4.653 14.953 4.54 14.79L3.116 12.742C2.755 12.223 2.755 11.777 3.116 11.258L4.54 9.21C4.653 9.047 4.716 8.893 4.752 8.698L5.193 6.243C5.305 5.62 5.62 5.305 6.243 5.193L8.698 4.752C8.893 4.716 9.047 4.653 9.21 4.54L11.258 3.116Z" stroke="currentColor" stroke-width="1.6"/>
                <path d="M9 15L15 9" stroke="currentColor" stroke-width="1.6"/>
                <circle cx="9.5" cy="9.5" r="1" fill="currentColor"/>
                <circle cx="14.5" cy="14.5" r="1" fill="currentColor"/>
              </svg>
              <span>Промокод на скидку</span>
            </span>
            <span id="active-promo-badge" class="hidden font-mono text-[10px] px-1.5 py-0.2 rounded bg-brand-700 text-white font-bold"></span>
          </div>
          <div class="flex items-center gap-1.5">
            <input id="promo-code-input" type="text" placeholder="Например: CROSTA5, NAPOLI10"
              class="flex-1 px-3 py-1.5 text-xs bg-canvas border border-borderSubtle rounded-lg font-mono uppercase text-textPrimary focus:ring-1 focus:ring-brand-700" />
            <button type="button" onclick="applyPromoFromInput()"
              class="px-3 py-1.5 bg-textPrimary text-canvas font-semibold text-xs rounded-lg hover:opacity-90 transition active:scale-97">
              Применить
            </button>
          </div>
          <p id="promo-msg" class="text-[10px] text-textSecondary hidden"></p>
        </div>

        <!-- Bonus Redemption Box -->
        <div id="cart-bonus-box" class="p-3.5 rounded-xl bg-elevated border border-borderSubtle space-y-2 text-xs"></div>

        <!-- Financial Summary -->
        <div class="bg-elevated border border-borderSubtle rounded-xl p-4 space-y-2 text-xs">
          <div class="flex justify-between text-textSecondary">
            <span>Сумма блюд (брутто)</span>
            <span id="summary-gross" class="font-mono tabular-nums">€0.00</span>
          </div>
          <div id="summary-promo-row" class="hidden flex justify-between text-brand-700 font-semibold">
            <span id="summary-promo-label">Промокод</span>
            <span id="summary-promo-val" class="font-mono tabular-nums">-€0.00</span>
          </div>
          <div id="summary-bonus-row" class="hidden flex justify-between text-bonus font-semibold">
            <span>Списание бонусов</span>
            <span id="summary-bonus-spent" class="font-mono tabular-nums">-€0.00</span>
          </div>
          <div class="flex justify-between text-textSecondary">
            <span>В т.ч. НДС ЕС (VAT 10%)</span>
            <span id="summary-vat" class="font-mono tabular-nums">€0.00</span>
          </div>
          <div class="flex justify-between text-textSecondary">
            <span>Курьерская доставка</span>
            <span id="summary-delivery" class="font-mono tabular-nums">€0.00</span>
          </div>
          <div class="pt-2 border-t border-borderSubtle flex justify-between items-baseline text-sm font-bold text-textPrimary">
            <span>Итого к оплате</span>
            <span id="summary-total" class="font-mono text-base tabular-nums">€0.00</span>
          </div>
          <div id="summary-cashback-hint" class="hidden pt-1 text-[11px] text-bonus font-medium flex items-center justify-between">
            <span>Кэшбэк за этот заказ (5%):</span>
            <span id="summary-cashback-val" class="font-mono font-bold">+€0.00</span>
          </div>
        </div>

        <!-- Checkout Form inside Drawer -->
        <form id="checkout-form" onsubmit="submitOrder(event)" class="space-y-3 pt-1">
          <div>
            <label for="cust-name" class="block text-xs font-semibold text-textPrimary mb-1">Имя и фамилия *</label>
            <input id="cust-name" type="text" required placeholder="Например: Давид Махвиладзе"
              class="w-full px-3 py-2 text-xs bg-canvas border border-borderSubtle rounded-lg text-textPrimary focus:ring-1 focus:ring-brand-700" />
          </div>

          <div class="grid grid-cols-2 gap-2">
            <div>
              <label for="cust-phone" class="block text-xs font-semibold text-textPrimary mb-1">Телефон *</label>
              <input id="cust-phone" type="tel" required placeholder="+373 777 00000"
                class="w-full px-3 py-2 text-xs bg-canvas border border-borderSubtle rounded-lg text-textPrimary font-mono focus:ring-1 focus:ring-brand-700" />
            </div>
            <div>
              <label for="cust-email" class="block text-xs font-semibold text-textPrimary mb-1">Email для чека *</label>
              <input id="cust-email" type="email" required placeholder="name@domain.eu"
                class="w-full px-3 py-2 text-xs bg-canvas border border-borderSubtle rounded-lg text-textPrimary focus:ring-1 focus:ring-brand-700" />
            </div>
          </div>

          <div>
            <label for="cust-address" class="block text-xs font-semibold text-textPrimary mb-1">Адрес доставки *</label>
            <input id="cust-address" type="text" required placeholder="Улица, дом, подъезд, квартира / офис"
              class="w-full px-3 py-2 text-xs bg-canvas border border-borderSubtle rounded-lg text-textPrimary focus:ring-1 focus:ring-brand-700" />
          </div>

          <div class="space-y-1.5">
            <label for="cust-payment" class="block text-xs font-semibold text-textPrimary">Способ оплаты</label>
            <select id="cust-payment" onchange="handlePaymentMethodChange(this.value)"
              class="w-full px-3 py-2 text-xs bg-canvas border border-borderSubtle rounded-lg text-textPrimary">
              <option value="CardOnline">Карта онлайн (3-D Secure)</option>
              <option value="ApplePay">Apple Pay / Google Pay</option>
              <option value="CardOnDelivery">Терминал курьеру</option>
              <option value="CorporateInvoice">Счёт для юрлиц (EU)</option>
            </select>
          </div>

          <!-- Kokonut UI CardField (https://kokonutui.com, MIT license) -->
          <div id="cardfield-container" class="space-y-2 p-3 bg-canvas border border-borderSubtle rounded-xl">
            <div class="flex items-center justify-between text-xs">
              <label for="cardfield-number-input" class="font-semibold text-textPrimary flex items-center gap-1.5">
                <span>Банковская карта</span>
                <span id="cardfield-brand-name" class="font-mono text-[11px] text-textSecondary font-normal hidden"></span>
              </label>
              <button type="button" onclick="fillTestCard()"
                class="text-[11px] text-brand-700 hover:text-brand-800 dark:text-brand-400 font-medium underline underline-offset-2 transition-colors">
                Тестовая карта
              </button>
            </div>

            <!-- Single-line compact cardfield row -->
            <div id="cardfield-row"
              class="relative flex h-12 items-center gap-2.5 px-3 rounded-xl border border-borderSubtle bg-surface transition-all duration-150">
              
              <!-- Brand SVG Icon Slot with Flip Animation -->
              <div id="cardfield-brand-slot" class="cardfield-brand-flip relative flex h-5 w-8 shrink-0 items-center justify-center">
                <!-- SVG dynamically injected -->
              </div>

              <!-- Number Container with NumberMirror and Transparent Native Input -->
              <div class="relative h-full flex-1 overflow-hidden">
                <!-- NumberMirror (Drawn Groups + Ghost Zeros) -->
                <div id="cardfield-mirror" aria-hidden="true"
                  class="pointer-events-none absolute inset-y-0 left-0 flex items-center whitespace-pre font-mono text-xs sm:text-sm text-textPrimary tabular-nums tracking-wide">
                </div>

                <!-- Placeholder when empty and unfocused -->
                <span id="cardfield-placeholder"
                  class="pointer-events-none absolute inset-y-0 left-0 flex items-center font-mono text-xs sm:text-sm text-textSecondary/50">
                  Номер карты
                </span>

                <!-- Native transparent input -->
                <input id="cardfield-number-input" type="text" inputmode="numeric" autocomplete="cc-number" spellcheck="false"
                  class="absolute inset-0 h-full w-full bg-transparent font-mono text-xs sm:text-sm text-transparent tabular-nums tracking-wide caret-textPrimary outline-none" />

                <!-- Collapsed Overlay Button (to re-edit number) -->
                <button id="cardfield-edit-btn" type="button" aria-label="Изменить номер карты" onclick="expandCardNumber()"
                  class="hidden absolute inset-0 cursor-text rounded-md outline-none"></button>
              </div>

              <!-- Revealable Expiry & CVC Inputs -->
              <div id="cardfield-extra"
                class="hidden flex shrink-0 items-center gap-1.5 transition-all duration-300 pl-2 border-l border-borderSubtle">
                <input id="cardfield-exp-input" type="text" inputmode="numeric" autocomplete="cc-exp" maxlength="7" placeholder="ММ / ГГ"
                  aria-label="Срок действия карты"
                  class="h-9 w-16 bg-transparent font-mono text-xs sm:text-sm text-textPrimary text-center tabular-nums outline-none placeholder:text-textSecondary/40" />
                <input id="cardfield-cvc-input" type="password" inputmode="numeric" autocomplete="cc-csc" maxlength="4" placeholder="CVC"
                  aria-label="Код безопасности CVC"
                  class="h-9 w-12 bg-transparent font-mono text-xs sm:text-sm text-textPrimary text-center tabular-nums outline-none placeholder:text-textSecondary/40" />
              </div>
            </div>

            <!-- Hint / Error Slot -->
            <div id="cardfield-hint" class="relative min-h-[16px] text-[11px] text-textSecondary flex items-center gap-1.5 transition-colors">
              <svg id="cardfield-hint-icon" class="w-3.5 h-3.5 shrink-0 text-textSecondary" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
              </svg>
              <span id="cardfield-hint-text">Сквозное 256-bit SSL шифрование (PCI DSS)</span>
            </div>
          </div>

          <div>
            <label for="cust-comment" class="block text-xs font-semibold text-textPrimary mb-1">Комментарий к заказу</label>
            <input id="cust-comment" type="text" placeholder="Код домофона, этаж, оставить у двери"
              class="w-full px-3 py-2 text-xs bg-canvas border border-borderSubtle rounded-lg text-textPrimary focus:ring-1 focus:ring-brand-700" />
          </div>

          <div class="space-y-1.5 pt-1">
            <label class="flex items-start gap-2 text-[11px] text-textSecondary cursor-pointer">
              <input id="gdpr-consent" type="checkbox" required class="mt-0.5 rounded border-borderSubtle text-brand-700 focus:ring-brand-700" />
              <span>Я подтверждаю согласие на обработку персональных данных для выполнения заказа (Регламент ЕС 2016/679 GDPR) *</span>
            </label>
            <label class="flex items-start gap-2 text-[11px] text-textSecondary cursor-pointer">
              <input id="marketing-consent" type="checkbox" class="mt-0.5 rounded border-borderSubtle text-brand-700 focus:ring-brand-700" />
              <span>Получать электронные чеки и скидочные предложения (опционально)</span>
            </label>
          </div>

          <!-- Morphing Submit Button -->
          <button id="btn-submit-order" type="submit"
            class="w-full py-3 px-4 bg-brand-700 hover:bg-brand-800 text-white font-semibold text-xs sm:text-sm rounded-xl shadow-sm transition flex items-center justify-center gap-2 active:scale-97">
            <span id="btn-submit-text">Оформить заказ</span>
            <span id="btn-submit-total" class="font-mono tabular-nums">€0.00</span>
          </button>
        </form>

      </div>
    </aside>
  </div>

  <!-- ==================== AUTH MODAL (Clean, Zero Demo Buttons) ==================== -->
  <div id="auth-modal" class="hidden fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 backdrop-blur-xs">
    <div class="bg-surface border border-borderSubtle rounded-2xl max-w-md w-full p-6 space-y-5 shadow-2xl transition-colors">
      <div class="flex items-center justify-between border-b border-borderSubtle pb-3">
        <div class="flex items-center gap-3">
          <button id="auth-tab-login" type="button" onclick="setAuthTab('login')" class="text-sm font-bold text-brand-700 pb-1 border-b-2 border-brand-700">Вход</button>
          <button id="auth-tab-register" type="button" onclick="setAuthTab('register')" class="text-sm font-medium text-textSecondary hover:text-textPrimary pb-1">Регистрация (+€5 бонусов)</button>
        </div>
        <button type="button" onclick="closeAuthModal()" class="text-textSecondary hover:text-textPrimary text-xl font-bold leading-none">&times;</button>
      </div>

      <!-- Login Form -->
      <form id="login-form" onsubmit="handleLoginSubmit(event)" class="space-y-3.5">
        <div>
          <label for="login-email" class="block text-xs font-semibold text-textPrimary mb-1">Email</label>
          <input id="login-email" type="email" required placeholder="david@crosta.eu"
            class="w-full px-3.5 py-2 text-xs bg-canvas border border-borderSubtle rounded-lg text-textPrimary focus:ring-1 focus:ring-brand-700" />
        </div>
        <div>
          <label for="login-pwd" class="block text-xs font-semibold text-textPrimary mb-1">Пароль</label>
          <input id="login-pwd" type="password" required placeholder="••••••••"
            class="w-full px-3.5 py-2 text-xs bg-canvas border border-borderSubtle rounded-lg text-textPrimary focus:ring-1 focus:ring-brand-700" />
        </div>
        <button type="submit" class="w-full py-2.5 bg-brand-700 hover:bg-brand-800 text-white font-semibold text-xs sm:text-sm rounded-xl transition shadow-sm active:scale-97">
          Войти в аккаунт
        </button>
      </form>

      <!-- Register Form with 4 Spring Strength Bars -->
      <form id="register-form" onsubmit="handleRegisterSubmit(event)" class="hidden space-y-3">
        <div>
          <label for="reg-name" class="block text-xs font-semibold text-textPrimary mb-1">ФИО *</label>
          <input id="reg-name" type="text" required placeholder="Марко Белуччи"
            class="w-full px-3.5 py-2 text-xs bg-canvas border border-borderSubtle rounded-lg text-textPrimary focus:ring-1 focus:ring-brand-700" />
        </div>
        <div class="grid grid-cols-2 gap-2">
          <div>
            <label for="reg-email" class="block text-xs font-semibold text-textPrimary mb-1">Email *</label>
            <input id="reg-email" type="email" required placeholder="marco@crosta.eu"
              class="w-full px-3.5 py-2 text-xs bg-canvas border border-borderSubtle rounded-lg text-textPrimary focus:ring-1 focus:ring-brand-700" />
          </div>
          <div>
            <label for="reg-phone" class="block text-xs font-semibold text-textPrimary mb-1">Телефон *</label>
            <input id="reg-phone" type="tel" required placeholder="+373 777 55443"
              class="w-full px-3.5 py-2 text-xs bg-canvas border border-borderSubtle rounded-lg text-textPrimary font-mono focus:ring-1 focus:ring-brand-700" />
          </div>
        </div>
        <div>
          <label for="reg-addr" class="block text-xs font-semibold text-textPrimary mb-1">Адрес доставки *</label>
          <input id="reg-addr" type="text" required placeholder="ул. Ленина, 12, кв. 4"
            class="w-full px-3.5 py-2 text-xs bg-canvas border border-borderSubtle rounded-lg text-textPrimary focus:ring-1 focus:ring-brand-700" />
        </div>
        <div>
          <div class="flex justify-between items-center mb-1">
            <label for="reg-pwd" class="block text-xs font-semibold text-textPrimary">Пароль (от 6 символов) *</label>
            <span id="pwd-strength-label" class="text-[10px] font-mono text-textSecondary">Сложность: —</span>
          </div>
          <div class="relative flex items-center">
            <input id="reg-pwd" type="password" required minlength="6" placeholder="Минимум 6 символов"
              oninput="updatePasswordStrength(this.value)"
              class="w-full px-3.5 py-2 text-xs bg-canvas border border-borderSubtle rounded-lg text-textPrimary focus:ring-1 focus:ring-brand-700 pr-8" />
            <button type="button" onclick="togglePasswordVisibility('reg-pwd')" class="absolute right-2 text-textSecondary hover:text-textPrimary p-1">
              <svg id="eye-icon-reg-pwd" width="16" height="16" viewBox="0 0 24 24" fill="none" class="text-textSecondary" xmlns="http://www.w3.org/2000/svg">
                <path d="M2.75 12C4.8 7.95 8.1 5.5 12 5.5C15.9 5.5 19.2 7.95 21.25 12C19.2 16.05 15.9 18.5 12 18.5C8.1 18.5 4.8 16.05 2.75 12Z" stroke="currentColor" stroke-width="1.6"/>
                <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="1.6"/>
              </svg>
            </button>
          </div>
          <!-- 4 Spring Animated Strength Bars -->
          <div class="grid grid-cols-4 gap-1.5 pt-1.5">
            <div id="pwd-bar-1" class="h-1 rounded-full bg-borderSubtle transition-all duration-200"></div>
            <div id="pwd-bar-2" class="h-1 rounded-full bg-borderSubtle transition-all duration-200"></div>
            <div id="pwd-bar-3" class="h-1 rounded-full bg-borderSubtle transition-all duration-200"></div>
            <div id="pwd-bar-4" class="h-1 rounded-full bg-borderSubtle transition-all duration-200"></div>
          </div>
        </div>
        <button type="submit" class="w-full py-2.5 bg-bonus hover:opacity-90 text-white font-semibold text-xs sm:text-sm rounded-xl transition shadow-sm active:scale-97">
          Зарегистрироваться (+€5.00 бонусов)
        </button>
      </form>
    </div>
  </div>

  <!-- ==================== ORDER CANCEL CONFIRMATION MODAL ==================== -->
  <div id="cancel-confirm-modal" class="hidden fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 backdrop-blur-xs">
    <div class="bg-surface border border-borderSubtle rounded-2xl max-w-sm w-full p-5 space-y-4 shadow-2xl transition-colors">
      <div class="flex items-start gap-3">
        <div class="w-9 h-9 rounded-full bg-red-100 text-brand-700 flex items-center justify-center shrink-0">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" class="text-brand-700" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="9.25" stroke="currentColor" stroke-width="1.8"/>
            <path d="M12 7.5V13" stroke="currentColor" stroke-width="1.8"/>
            <circle cx="12" cy="16.25" r="1" fill="currentColor"/>
          </svg>
        </div>
        <div>
          <h3 class="text-sm font-bold text-textPrimary">Подтверждение отмены заказа</h3>
          <p class="text-xs text-textSecondary mt-1 leading-relaxed">
            Вы действительно хотите отменить заказ <span id="cancel-order-num-text" class="font-mono font-bold text-textPrimary">ORD-...</span>? Это действие необратимо и зафиксируется в SQLite Audit Log.
          </p>
        </div>
      </div>
      <div class="flex justify-end gap-2 pt-2">
        <button type="button" onclick="closeCancelModal()" class="px-3.5 py-1.5 bg-elevated text-textPrimary text-xs font-semibold rounded-lg hover:border-textSecondary border border-borderSubtle transition">
          Назад
        </button>
        <button id="btn-confirm-cancel" type="button" class="px-3.5 py-1.5 bg-brand-700 hover:bg-brand-800 text-white text-xs font-semibold rounded-lg shadow-sm transition">
          Подтвердить отмену
        </button>
      </div>
    </div>
  </div>

  <!-- ==================== PROFILE EDIT MODAL ==================== -->
  <div id="profile-edit-modal" class="hidden fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 backdrop-blur-xs">
    <div class="bg-surface border border-borderSubtle rounded-2xl max-w-md w-full p-6 space-y-4 shadow-2xl transition-colors">
      <div class="flex items-center justify-between border-b border-borderSubtle pb-3">
        <h3 class="text-sm font-bold text-textPrimary">Редактирование данных профиля</h3>
        <button type="button" onclick="toggleProfileEditModal(false)" class="text-textSecondary hover:text-textPrimary text-lg font-bold leading-none">&times;</button>
      </div>
      <form onsubmit="handleProfileUpdateSubmit(event)" class="space-y-3">
        <div>
          <label for="edit-name" class="block text-xs font-semibold text-textPrimary mb-1">ФИО *</label>
          <input id="edit-name" type="text" required class="w-full px-3 py-2 text-xs bg-canvas border border-borderSubtle rounded-lg text-textPrimary" />
        </div>
        <div>
          <label for="edit-phone" class="block text-xs font-semibold text-textPrimary mb-1">Телефон *</label>
          <input id="edit-phone" type="tel" required class="w-full px-3 py-2 text-xs bg-canvas border border-borderSubtle rounded-lg text-textPrimary font-mono" />
        </div>
        <div>
          <label for="edit-addr" class="block text-xs font-semibold text-textPrimary mb-1">Адрес доставки *</label>
          <input id="edit-addr" type="text" required class="w-full px-3 py-2 text-xs bg-canvas border border-borderSubtle rounded-lg text-textPrimary" />
        </div>
        <div class="flex justify-end gap-2 pt-2">
          <button type="button" onclick="toggleProfileEditModal(false)" class="px-4 py-2 bg-elevated text-textPrimary text-xs rounded-lg">Отмена</button>
          <button type="submit" class="px-4 py-2 bg-brand-700 text-white text-xs font-semibold rounded-lg">Сохранить</button>
        </div>
      </form>
    </div>
  </div>

  <!-- ==================== NEW PIZZA MODAL (ADMIN) ==================== -->
  <div id="new-pizza-modal" class="hidden fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 backdrop-blur-xs">
    <div class="bg-surface border border-borderSubtle rounded-2xl max-w-lg w-full p-6 space-y-4 shadow-2xl transition-colors">
      <div class="flex items-center justify-between border-b border-borderSubtle pb-3">
        <h3 class="text-base font-serif font-bold text-textPrimary">Добавление новой позиции в меню</h3>
        <button type="button" onclick="toggleNewPizzaModal(false)" class="text-textSecondary hover:text-textPrimary text-lg font-bold">&times;</button>
      </div>
      <form onsubmit="submitNewPizza(event)" class="space-y-3">
        <div>
          <label for="np-name" class="block text-xs font-semibold text-textPrimary mb-1">Название пиццы *</label>
          <input id="np-name" type="text" required placeholder="Капричоза Спечиале"
            class="w-full px-3 py-1.5 text-xs bg-canvas border border-borderSubtle rounded-lg text-textPrimary" />
        </div>
        <div>
          <label for="np-desc" class="block text-xs font-semibold text-textPrimary mb-1">Описание *</label>
          <textarea id="np-desc" required rows="2" placeholder="Краткое гастрономическое описание"
            class="w-full px-3 py-1.5 text-xs bg-canvas border border-borderSubtle rounded-lg text-textPrimary"></textarea>
        </div>
        <div>
          <label for="np-ing" class="block text-xs font-semibold text-textPrimary mb-1">Ингредиенты (через запятую) *</label>
          <input id="np-ing" type="text" required placeholder="Томатный соус, моцарелла, артишоки, грибы"
            class="w-full px-3 py-1.5 text-xs bg-canvas border border-borderSubtle rounded-lg text-textPrimary" />
        </div>
        <div class="grid grid-cols-2 gap-2">
          <div>
            <label for="np-cat" class="block text-xs font-semibold text-textPrimary mb-1">Категория *</label>
            <select id="np-cat" class="w-full px-3 py-1.5 text-xs bg-canvas border border-borderSubtle rounded-lg text-textPrimary">
              <option value="Классика">Классика</option>
              <option value="Мясные">Мясные</option>
              <option value="Сырные">Сырные</option>
              <option value="Премиум">Премиум</option>
              <option value="Овощные">Овощные</option>
            </select>
          </div>
          <div>
            <label for="np-tag" class="block text-xs font-semibold text-textPrimary mb-1">Диетический тег</label>
            <input id="np-tag" type="text" required placeholder="Новинка"
              class="w-full px-3 py-1.5 text-xs bg-canvas border border-borderSubtle rounded-lg text-textPrimary" />
          </div>
        </div>
        <div class="grid grid-cols-3 gap-2">
          <div>
            <label for="np-price" class="block text-xs font-semibold text-textPrimary mb-1">Цена брутто (€) *</label>
            <input id="np-price" type="number" step="0.10" required placeholder="13.50"
              class="w-full px-3 py-1.5 text-xs bg-canvas border border-borderSubtle rounded-lg text-textPrimary font-mono" />
          </div>
          <div>
            <label for="np-prep" class="block text-xs font-semibold text-textPrimary mb-1">Время (мин)</label>
            <input id="np-prep" type="number" value="15"
              class="w-full px-3 py-1.5 text-xs bg-canvas border border-borderSubtle rounded-lg text-textPrimary font-mono" />
          </div>
          <div>
            <label for="np-kcal" class="block text-xs font-semibold text-textPrimary mb-1">Ккал</label>
            <input id="np-kcal" type="number" value="850"
              class="w-full px-3 py-1.5 text-xs bg-canvas border border-borderSubtle rounded-lg text-textPrimary font-mono" />
          </div>
        </div>
        <div class="flex justify-end gap-2 pt-2">
          <button type="button" onclick="toggleNewPizzaModal(false)" class="px-4 py-2 bg-elevated text-textPrimary text-xs rounded-lg">Отмена</button>
          <button type="submit" class="px-4 py-2 bg-brand-700 text-white text-xs font-semibold rounded-lg">Добавить</button>
        </div>
      </form>
    </div>
  </div>

  <!-- ==================== HIDDEN PRINT RECEIPT SHEET (EU VAT FISCAL) ==================== -->
  <div id="print-receipt-sheet" class="hidden"></div>

  <!-- ==================== APPLICATION SCRIPTS ==================== -->
  <script>
    // -------------------------------------------------------------------------
    // 1. Spring Motion Engine (window.Motion, by DesignBookmark)
    // -------------------------------------------------------------------------
    window.Motion = (() => {
      const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      const S = (x, k = 400, c = 30) => {
        const obj = { x, v: 0, t: x, k, c };
        Object.defineProperty(obj, 'target', {
          get() { return this.t; },
          set(v) { this.t = v; }
        });
        return obj;
      };
      const tune = (s, k, c) => { s.k = k; s.c = reduce ? 2 * Math.sqrt(k) : c; };
      const step = (s, dt) => {
        if (reduce) { s.x = s.t; s.v = 0; return true; }
        const a = -s.k * (s.x - s.t) - s.c * s.v;
        s.v += a * dt;
        s.x += s.v * dt;
        const settled = Math.abs(s.x - s.t) < 0.001 && Math.abs(s.v) < 0.001;
        if (settled) { s.x = s.t; s.v = 0; }
        return settled;
      };
      const clamp = (v, a, b) => Math.max(a, Math.min(b, v));

      let timeScale = 1;
      const timers = [];
      const after = (sec, fn) => { const t = { t: sec, fn }; timers.push(t); return t; };
      const cancel = t => { const i = timers.indexOf(t); if (i > -1) timers.splice(i, 1); };

      function setSlow(v) {
        timeScale = v ? 0.25 : 1;
      }

      const comps = [];
      let last = performance.now();
      function loop(now) {
        const dt = Math.min((now - last) / 1000, 1 / 30) * timeScale;
        last = now;
        for (let i = timers.length - 1; i >= 0; i--) {
          if ((timers[i].t -= dt) <= 0) timers.splice(i, 1)[0].fn();
        }
        const sub = 4;
        for (let k = 0; k < sub; k++) {
          comps.forEach(c => {
            if (typeof c === 'function') c(dt / sub);
            else if (c && c.frame) c.frame(dt / sub);
          });
        }
        comps.forEach(c => {
          if (c && c.render) c.render();
        });
        requestAnimationFrame(loop);
      }
      requestAnimationFrame(loop);

      return {
        S, tune, step, clamp, after, cancel,
        register: c => comps.push(c),
        unregister: c => { const i = comps.indexOf(c); if (i > -1) comps.splice(i, 1); },
        get timeScale() { return timeScale; },
        get slow() { return timeScale !== 1; },
        setSlow,
        svg: (p, sw = 1.8) => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="${sw}" stroke-linecap="round" stroke-linejoin="round">${p}</svg>`
      };
    })();

    // -------------------------------------------------------------------------
    // 2. Word Roll in Hero Title (DesignBookmark Pattern)
    // -------------------------------------------------------------------------
    function setupWordRoll(rollId, slotId, words, options = {}) {
      const { S, step, clamp, after, cancel, register } = window.Motion;
      const roll = document.getElementById(rollId);
      const slot = document.getElementById(slotId);
      if (!roll || !slot) return null;

      const width = S(0, 320, 30);
      let live = [];
      let i = 0;
      let timer = null;

      function make(word) {
        const el = document.createElement('span');
        el.className = 'word';
        const letters = [...word].map(ch => {
          const l = document.createElement('span');
          l.className = 'ch';
          l.textContent = ch;
          el.appendChild(l);
          return { el: l, s: S(1, 420, 26) };
        });
        slot.appendChild(el);
        return { el, letters, out: false };
      }

      function show(word, first) {
        live.forEach(w => {
          if (w.out) return;
          w.out = true;
          w.letters.forEach((l, k) => after(k * 0.022, () => { l.s.t = -1; }));
          after(1, () => { w.el.remove(); live = live.filter(x => x !== w); });
        });
        const w = make(word);
        w.letters.forEach((l, k) => {
          if (first) {
            l.s.x = l.s.t = 0;
          } else {
            after(0.06 + k * 0.028, () => { l.s.t = 0; });
          }
        });
        live.push(w);
        width.t = w.el.offsetWidth;
        if (first) width.x = width.t;
        if (options.ariaPrefix) {
          roll.setAttribute('aria-label', `${options.ariaPrefix} ${word}`);
        }
      }

      function schedule() {
        if (timer) cancel(timer);
        timer = after(options.interval || 2.6, next);
      }

      function next() {
        i = (i + 1) % words.length;
        show(words[i]);
        schedule();
      }

      roll.addEventListener('click', next);
      roll.addEventListener('keydown', e => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          next();
        }
      });

      show(words[0], true);
      schedule();

      if (document.fonts) {
        document.fonts.ready.then(() => {
          const w = live[live.length - 1];
          if (w) width.t = w.el.offsetWidth;
        });
      }

      register({
        frame(dt) {
          step(width, dt);
          live.forEach(w => w.letters.forEach(l => step(l.s, dt)));
        },
        render() {
          slot.style.width = width.x + 'px';
          live.forEach(w => w.letters.forEach(l => {
            const y = l.s.x;
            l.el.style.transform = `translateY(${y * 105}%)`;
            l.el.style.opacity = clamp(1 - Math.abs(y) * 0.9, 0, 1);
          }));
        }
      });

      return { next, show };
    }

    let heroRollInstance = null;
    function initWordRolls() {
      const heroWords = ['всей семьи', 'дружной компании', 'офисного обеда', 'вечера пятницы', 'ценителей вкуса'];
      heroRollInstance = setupWordRoll('hero-word-roll', 'hero-roll-slot', heroWords, {
        ariaPrefix: 'Неаполитанская пицца для',
        interval: 2.7
      });
    }

    // -------------------------------------------------------------------------
    // 3. Artistic SVG Food Illustrations for All 9 Pizzas
    // -------------------------------------------------------------------------
    function renderPizzaIllustrationSvg(sku, size = 160) {
      // Base crust with charred spots
      const crust = `
        <circle cx="100" cy="100" r="92" fill="#D98A4F" stroke="#8C4A1E" stroke-width="3"/>
        <!-- Leopard spots on rim -->
        <circle cx="28" cy="74" r="5" fill="#3B2012"/>
        <circle cx="42" cy="38" r="4.5" fill="#2E180D"/>
        <circle cx="85" cy="18" r="6" fill="#3B2012"/>
        <circle cx="135" cy="22" r="5" fill="#26140A"/>
        <circle cx="168" cy="55" r="5.5" fill="#3B2012"/>
        <circle cx="178" cy="110" r="4.5" fill="#2E180D"/>
        <circle cx="155" cy="158" r="6" fill="#3B2012"/>
        <circle cx="110" cy="180" r="5" fill="#26140A"/>
        <circle cx="56" cy="165" r="5.5" fill="#3B2012"/>
        <circle cx="24" cy="125" r="4" fill="#2E180D"/>
      `;

      let interior = '';

      if (sku === 'PZ-001') {
        // Margherita DOC: San Marzano sauce swirl, Fior di Latte pools, fresh basil, olive oil
        interior = `
          <circle cx="100" cy="100" r="76" fill="#C22026"/>
          <!-- Mozzarella pools -->
          <ellipse cx="80" cy="75" rx="18" ry="14" fill="#FCFAF2" opacity="0.95"/>
          <ellipse cx="125" cy="85" rx="16" ry="15" fill="#FCFAF2" opacity="0.95"/>
          <ellipse cx="95" cy="125" rx="19" ry="16" fill="#FCFAF2" opacity="0.95"/>
          <circle cx="70" cy="115" r="10" fill="#FCFAF2" opacity="0.9"/>
          <!-- Basil leaves -->
          <path d="M78 72 C70 58 88 50 94 65 C96 74 86 78 78 72 Z" fill="#15803D"/>
          <path d="M120 110 C135 100 142 118 130 128 C120 134 114 120 120 110 Z" fill="#16A34A"/>
          <path d="M102 92 C108 80 122 84 116 96 C112 102 98 100 102 92 Z" fill="#15803D"/>
          <!-- Olive oil gleams -->
          <circle cx="112" cy="74" r="2.5" fill="#FACC15"/>
          <circle cx="86" cy="104" r="2" fill="#FACC15"/>
          <circle cx="98" cy="138" r="2.5" fill="#FACC15"/>
        `;
      } else if (sku === 'PZ-002') {
        // Pepperoni Diavola: spicy ventricina cups, chili flakes
        interior = `
          <circle cx="100" cy="100" r="76" fill="#B91C1C"/>
          <circle cx="100" cy="100" r="73" fill="#FBF5E5" opacity="0.6"/>
          <!-- Pepperoni cups -->
          <circle cx="72" cy="65" r="14" fill="#991B1B" stroke="#7F1D1D" stroke-width="2"/>
          <circle cx="128" cy="68" r="13.5" fill="#991B1B" stroke="#7F1D1D" stroke-width="2"/>
          <circle cx="100" cy="98" r="15" fill="#881337" stroke="#7F1D1D" stroke-width="2"/>
          <circle cx="68" cy="118" r="13" fill="#991B1B" stroke="#7F1D1D" stroke-width="2"/>
          <circle cx="132" cy="122" r="14" fill="#991B1B" stroke="#7F1D1D" stroke-width="2"/>
          <circle cx="102" cy="52" r="11" fill="#991B1B" stroke="#7F1D1D" stroke-width="1.8"/>
          <circle cx="100" cy="142" r="11" fill="#881337" stroke="#7F1D1D" stroke-width="1.8"/>
          <!-- Chili flakes -->
          <path d="M85 92 L88 95 L84 96 Z" fill="#DC2626"/>
          <path d="M115 84 L119 86 L116 89 Z" fill="#DC2626"/>
          <path d="M92 124 L96 126 L93 129 Z" fill="#DC2626"/>
        `;
      } else if (sku === 'PZ-003') {
        // Quattro Formaggi: White bianca base, Gorgonzola Dolce DOP veins, Fontina, Grana Padano
        interior = `
          <circle cx="100" cy="100" r="76" fill="#FAF6EA"/>
          <!-- Melted fontina pools -->
          <ellipse cx="85" cy="80" rx="28" ry="20" fill="#FDE68A" opacity="0.8"/>
          <ellipse cx="120" cy="118" rx="26" ry="22" fill="#FDE68A" opacity="0.8"/>
          <!-- Gorgonzola veins -->
          <path d="M68 68 Q78 80 88 74 Q98 70 102 82" stroke="#38BDF8" stroke-width="3" fill="none" stroke-linecap="round"/>
          <path d="M110 88 Q124 95 132 86 Q140 80 138 98" stroke="#38BDF8" stroke-width="3" fill="none" stroke-linecap="round"/>
          <path d="M78 122 Q92 130 98 120 Q106 112 118 126" stroke="#38BDF8" stroke-width="3.5" fill="none" stroke-linecap="round"/>
          <!-- Grana Padano flakes -->
          <rect x="74" y="96" width="12" height="6" rx="1.5" fill="#FEF3C7" transform="rotate(18 74 96)"/>
          <rect x="114" y="68" width="14" height="7" rx="1.5" fill="#FEF3C7" transform="rotate(-24 114 68)"/>
          <rect x="96" y="106" width="11" height="5" rx="1.5" fill="#FEF3C7" transform="rotate(42 96 106)"/>
          <!-- Black pepper -->
          <circle cx="70" cy="84" r="1.5" fill="#292524"/>
          <circle cx="130" cy="104" r="1.5" fill="#292524"/>
          <circle cx="100" cy="74" r="1.5" fill="#292524"/>
          <circle cx="108" cy="136" r="1.5" fill="#292524"/>
        `;
      } else if (sku === 'PZ-004') {
        // Prosciutto e Rucola: tomato base, melted cheese, folded crudo ribbons, fresh arugula
        interior = `
          <circle cx="100" cy="100" r="76" fill="#C22026"/>
          <circle cx="100" cy="100" r="72" fill="#FDF8ED" opacity="0.75"/>
          <!-- Folded Prosciutto ribbons -->
          <path d="M58 84 C52 70 82 62 90 76 C96 86 64 94 58 84 Z" fill="#F43F5E" stroke="#BE123C" stroke-width="1.5"/>
          <path d="M108 66 C124 54 142 74 130 88 C120 98 100 76 108 66 Z" fill="#E11D48" stroke="#9F1239" stroke-width="1.5"/>
          <path d="M82 112 C74 98 104 92 118 106 C126 118 92 126 82 112 Z" fill="#F43F5E" stroke="#BE123C" stroke-width="1.5"/>
          <path d="M122 108 C136 118 144 140 126 142 C112 144 114 122 122 108 Z" fill="#E11D48" stroke="#9F1239" stroke-width="1.5"/>
          <!-- Arugula leaves -->
          <path d="M68 62 C74 50 82 56 80 66 C76 72 64 68 68 62 Z" fill="#16A34A"/>
          <path d="M136 78 C144 70 148 82 140 88 C134 92 130 84 136 78 Z" fill="#22C55E"/>
          <path d="M72 128 C64 120 74 110 80 118 C84 124 78 132 72 128 Z" fill="#16A34A"/>
          <path d="M102 88 C108 78 116 84 112 92 C108 96 98 94 102 88 Z" fill="#22C55E"/>
          <!-- Parmesan curls -->
          <rect x="92" y="76" width="14" height="4" rx="2" fill="#FEF3C7" transform="rotate(32 92 76)"/>
          <rect x="110" y="122" width="16" height="4" rx="2" fill="#FEF3C7" transform="rotate(-18 110 122)"/>
        `;
      } else if (sku === 'PZ-005') {
        // Truffle Forest: black truffle crema, forest mushrooms (porcini, champignons), thyme
        interior = `
          <circle cx="100" cy="100" r="76" fill="#44403C"/>
          <circle cx="100" cy="100" r="72" fill="#E7E5E4" opacity="0.45"/>
          <!-- Mushroom caps & stems -->
          <g transform="translate(62,60)">
            <ellipse cx="14" cy="10" rx="14" ry="9" fill="#78716C"/>
            <rect x="10" y="10" width="8" height="10" rx="2" fill="#A8A29E"/>
          </g>
          <g transform="translate(112,65)">
            <ellipse cx="14" cy="10" rx="15" ry="9.5" fill="#57534E"/>
            <rect x="10" y="10" width="8" height="9" rx="2" fill="#A8A29E"/>
          </g>
          <g transform="translate(86,104)">
            <ellipse cx="16" cy="11" rx="16" ry="10" fill="#78716C"/>
            <rect x="12" y="11" width="8" height="11" rx="2" fill="#D6D3D1"/>
          </g>
          <g transform="translate(56,112)">
            <ellipse cx="12" cy="8" rx="13" ry="8" fill="#57534E"/>
            <rect x="9" y="8" width="6" height="8" rx="2" fill="#A8A29E"/>
          </g>
          <g transform="translate(126,116)">
            <ellipse cx="12" cy="8" rx="12" ry="7.5" fill="#78716C"/>
            <rect x="9" y="8" width="6" height="8" rx="2" fill="#D6D3D1"/>
          </g>
          <!-- Thyme sprigs -->
          <path d="M78 98 Q88 92 94 96" stroke="#84CC16" stroke-width="2" fill="none"/>
          <circle cx="82" cy="94" r="2" fill="#65A30D"/>
          <circle cx="90" cy="93" r="2" fill="#65A30D"/>
          <path d="M116 88 Q124 100 120 108" stroke="#84CC16" stroke-width="2" fill="none"/>
          <circle cx="120" cy="94" r="2" fill="#65A30D"/>
          <circle cx="122" cy="102" r="2" fill="#65A30D"/>
        `;
      } else if (sku === 'PZ-006') {
        // Carbonara Al Forno: yolk-pecorino crema, guanciale cubes, crushed black pepper
        interior = `
          <circle cx="100" cy="100" r="76" fill="#FDE047"/>
          <circle cx="100" cy="100" r="70" fill="#FEF9C3" opacity="0.6"/>
          <!-- Browned crispy guanciale cubes -->
          <rect x="68" y="66" width="12" height="10" rx="2" fill="#881337" stroke="#4C0519" stroke-width="1.5"/>
          <rect x="116" y="62" width="13" height="11" rx="2" fill="#9F1239" stroke="#4C0519" stroke-width="1.5"/>
          <rect x="94" y="92" width="14" height="12" rx="2" fill="#881337" stroke="#4C0519" stroke-width="1.5"/>
          <rect x="64" y="116" width="13" height="10" rx="2" fill="#9F1239" stroke="#4C0519" stroke-width="1.5"/>
          <rect x="122" y="112" width="12" height="11" rx="2" fill="#881337" stroke="#4C0519" stroke-width="1.5"/>
          <rect x="98" y="136" width="12" height="10" rx="2" fill="#9F1239" stroke="#4C0519" stroke-width="1.5"/>
          <!-- Pecorino flakes & black pepper -->
          <circle cx="82" cy="88" r="1.8" fill="#1C1917"/>
          <circle cx="112" cy="80" r="1.8" fill="#1C1917"/>
          <circle cx="88" cy="120" r="1.8" fill="#1C1917"/>
          <circle cx="118" cy="132" r="1.8" fill="#1C1917"/>
          <circle cx="104" cy="74" r="1.8" fill="#1C1917"/>
          <circle cx="78" cy="136" r="1.8" fill="#1C1917"/>
        `;
      } else if (sku === 'PZ-007') {
        // Mediterranean Vegan: tomato sugo, artichokes, Kalamata olives, sun-dried tomatoes, oregano
        interior = `
          <circle cx="100" cy="100" r="76" fill="#B91C1C"/>
          <circle cx="100" cy="100" r="72" fill="#FEF2F2" opacity="0.3"/>
          <!-- Artichoke quarters -->
          <path d="M64 74 C60 60 76 56 82 70 C84 80 68 84 64 74 Z" fill="#84CC16" stroke="#4D7C0F" stroke-width="1.5"/>
          <path d="M124 70 C134 58 144 72 136 84 C128 92 118 80 124 70 Z" fill="#84CC16" stroke="#4D7C0F" stroke-width="1.5"/>
          <path d="M78 126 C70 114 88 106 94 120 C96 130 84 136 78 126 Z" fill="#84CC16" stroke="#4D7C0F" stroke-width="1.5"/>
          <!-- Kalamata olives -->
          <ellipse cx="100" cy="80" rx="8" ry="6" fill="#1C1917"/>
          <circle cx="100" cy="80" r="2.5" fill="#C22026"/>
          <ellipse cx="128" cy="118" rx="8" ry="6" fill="#1C1917"/>
          <circle cx="128" cy="118" r="2.5" fill="#C22026"/>
          <ellipse cx="64" cy="108" rx="7.5" ry="5.5" fill="#1C1917"/>
          <circle cx="64" cy="108" r="2" fill="#C22026"/>
          <!-- Sun-dried tomatoes -->
          <ellipse cx="98" cy="112" rx="10" ry="5" fill="#7F1D1D" transform="rotate(-15 98 112)"/>
          <ellipse cx="112" cy="138" rx="9" ry="4.5" fill="#7F1D1D" transform="rotate(25 112 138)"/>
        `;
      } else if (sku === 'PZ-008') {
        // Seafood with Prawns and Genovese Pesto: pink tiger prawns, emerald pesto, cherry tomatoes
        interior = `
          <circle cx="100" cy="100" r="76" fill="#FDF8ED"/>
          <!-- Pesto swirls -->
          <path d="M68 76 Q84 64 96 82 Q108 100 128 88" stroke="#15803D" stroke-width="4.5" fill="none" stroke-linecap="round"/>
          <path d="M74 118 Q92 134 112 118 Q126 106 138 126" stroke="#15803D" stroke-width="4.5" fill="none" stroke-linecap="round"/>
          <!-- Tiger Prawns (curved pink shapes with tails) -->
          <path d="M76 68 C70 54 94 48 98 62 C102 74 84 78 76 68 Z" fill="#FB7185" stroke="#E11D48" stroke-width="1.8"/>
          <path d="M122 72 C134 60 148 76 136 90 C124 100 114 82 122 72 Z" fill="#FB7185" stroke="#E11D48" stroke-width="1.8"/>
          <path d="M84 114 C74 102 98 96 108 108 C116 118 92 126 84 114 Z" fill="#FB7185" stroke="#E11D48" stroke-width="1.8"/>
          <!-- Datterini cherry tomato halves -->
          <circle cx="64" cy="98" r="7" fill="#EF4444"/>
          <circle cx="132" cy="108" r="7" fill="#EF4444"/>
          <circle cx="104" cy="134" r="7.5" fill="#EF4444"/>
          <!-- Lemon zest curls -->
          <path d="M88 88 Q94 84 92 92" stroke="#FACC15" stroke-width="1.5" fill="none"/>
          <path d="M118 104 Q124 102 122 108" stroke="#FACC15" stroke-width="1.5" fill="none"/>
        `;
      } else if (sku === 'PZ-009') {
        // BBQ Pollo Affumicato: smoky BBQ glaze swirl, smoked chicken strips, red onion rings, corn
        interior = `
          <circle cx="100" cy="100" r="76" fill="#FBF5E5"/>
          <!-- BBQ sauce spiral -->
          <path d="M64 78 Q92 56 126 72 Q144 94 122 120 Q94 142 74 118" stroke="#7F1D1D" stroke-width="5" fill="none" stroke-linecap="round"/>
          <!-- Smoked chicken strips -->
          <rect x="72" y="70" width="18" height="7" rx="3" fill="#FDBA74" stroke="#EA580C" stroke-width="1.2" transform="rotate(15 72 70)"/>
          <rect x="114" y="68" width="19" height="7.5" rx="3" fill="#FDBA74" stroke="#EA580C" stroke-width="1.2" transform="rotate(-20 114 68)"/>
          <rect x="88" y="106" width="20" height="8" rx="3.5" fill="#FDBA74" stroke="#EA580C" stroke-width="1.2" transform="rotate(35 88 106)"/>
          <rect x="62" y="112" width="16" height="7" rx="3" fill="#FDBA74" stroke="#EA580C" stroke-width="1.2" transform="rotate(-15 62 112)"/>
          <!-- Red onion rings -->
          <circle cx="94" cy="74" r="10" stroke="#C084FC" stroke-width="2" fill="none"/>
          <circle cx="126" cy="112" r="11" stroke="#C084FC" stroke-width="2" fill="none"/>
          <circle cx="76" cy="130" r="9" stroke="#C084FC" stroke-width="2" fill="none"/>
          <!-- Sweetcorn -->
          <circle cx="86" cy="94" r="2.5" fill="#FACC15"/>
          <circle cx="110" cy="90" r="2.5" fill="#FACC15"/>
          <circle cx="104" cy="128" r="2.5" fill="#FACC15"/>
        `;
      }

      return `
        <svg width="${size}" height="${size}" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg" class="drop-shadow-md select-none pointer-events-none">
          ${crust}
          ${interior}
        </svg>
      `;
    }

    // -------------------------------------------------------------------------
    // 4. Application State Management
    // -------------------------------------------------------------------------
    let currentUser = null;
    let userProfileDetails = null;
    let menu = [];
    let allPizzasAdmin = [];
    let sizes = [];
    let promotions = [];
    let orders = [];
    let cart = [];
    let bonusToSpend = 0.00;
    let selectedSizes = {};
    let currentCategory = 'Все';
    let trackedOrderNumber = 'ORD-2026-104';
    let currentStaffFilter = 'All';
    let currentTheme = localStorage.getItem('crosta_theme') || 'light';
    let activePromo = null;
    let pendingCancelOrderId = null;
    let currentChartPeriod = 'day';

    // Detail View State
    let currentDetailPizza = null;
    let currentDetailSizeId = null;
    let currentDetailQty = 1;
    let selectedDetailToppings = {};

    const PROMO_CODES = {
      'CROSTA5': { code: 'CROSTA5', discountEur: 5.0, label: 'Скидка €5.00' },
      'CROSTA2026': { code: 'CROSTA2026', discountEur: 5.0, label: 'Скидка €5.00' },
      'NAPOLI10': { code: 'NAPOLI10', percent: 10, label: 'Скидка 10%' },
      'FREEDELIV': { code: 'FREEDELIV', freeDelivery: true, label: 'Бесплатная доставка' }
    };

    const STATUS_META = {
      New: { label: 'Новый заказ', cls: 'status-badge-New', step: 1 },
      Preparing: { label: 'Подготовка теста', cls: 'status-badge-Preparing', step: 2 },
      Baking: { label: 'В печи 430°C', cls: 'status-badge-Baking', step: 3 },
      OutForDelivery: { label: 'У курьера', cls: 'status-badge-OutForDelivery', step: 4 },
      Delivered: { label: 'Доставлен', cls: 'status-badge-Delivered', step: 5 },
      Cancelled: { label: 'Отменён', cls: 'status-badge-Cancelled', step: 0 }
    };

    const NEXT_STEP = {
      New: { next: 'Preparing', label: 'Принять на кухню', roles: ['Manager', 'Kitchen'] },
      Preparing: { next: 'Baking', label: 'Отправить в печь', roles: ['Manager', 'Kitchen'] },
      Baking: { next: 'OutForDelivery', label: 'Передать курьеру', roles: ['Manager', 'Kitchen', 'Courier'] },
      OutForDelivery: { next: 'Delivered', label: 'Подтвердить доставку', roles: ['Manager', 'Courier'] }
    };

    const NUTRITION_MAP = {
      'PZ-001': { kcal: 740, p: 28, f: 22, c: 104 },
      'PZ-002': { kcal: 920, p: 38, f: 42, c: 98 },
      'PZ-003': { kcal: 980, p: 44, f: 48, c: 94 },
      'PZ-004': { kcal: 840, p: 42, f: 28, c: 102 },
      'PZ-005': { kcal: 860, p: 30, f: 34, c: 106 },
      'PZ-006': { kcal: 960, p: 40, f: 46, c: 96 },
      'PZ-007': { kcal: 690, p: 22, f: 18, c: 110 },
      'PZ-008': { kcal: 810, p: 36, f: 26, c: 106 },
      'PZ-009': { kcal: 890, p: 44, f: 32, c: 104 }
    };

    const EXTRA_TOPPINGS = [
      { id: 'crust', name: 'Сырный бортик Mozzarella', price: 2.50 },
      { id: 'extra_cheese', name: 'Доп. Fior di Latte DOP', price: 1.80 },
      { id: 'truffle_oil', name: 'Трюфельное масло Умбрии', price: 1.50 },
      { id: 'spicy_sauce', name: 'Острый соус из Калабрии', price: 1.00 }
    ];

    const REVIEWS_DATA = {
      'PZ-001': [
        { author: 'Маттео Л.', city: 'Неаполь', rating: 5, text: 'Идеальное неаполитанское тесто, нежное и с правильными леопардовыми подпалинами. Соус из Сан-Марцано бесподобен.' },
        { author: 'Анна В.', city: 'Милан', rating: 5, text: 'Классика, которая никогда не подводит. Базилик свежайший.' }
      ],
      'PZ-002': [
        { author: 'Лука Р.', city: 'Рим', rating: 5, text: 'Отличная пикантность салями вентричина! Корочка хрустит, сыр тянется великолепно.' },
        { author: 'Сергей К.', city: 'Берлин', rating: 5, text: 'Любимая острая пицца в городе. Перчик чили добавляет благородный огонь.' }
      ],
      'PZ-003': [
        { author: 'Джулия Б.', city: 'Флоренция', rating: 5, text: 'Горгонзола Dolce DOP даёт невероятно сливочный и нежный вкус. Идеальный баланс сыров.' },
        { author: 'Марк Ш.', city: 'Вена', rating: 5, text: 'Без томатов, чистая сырная симфония. Черный перец подчеркивает грана падано.' }
      ],
      'PZ-004': [
        { author: 'Давид М.', city: 'Кишинёв', rating: 5, text: 'Прошутто высочайшего качества, не пересушенное в печи, а добавленное свежим со свежей рукколой.' },
        { author: 'Клаудия Ф.', city: 'Болонья', rating: 5, text: 'Пармская ветчина и лепестки пармезана 24 месяца — восторг.' }
      ],
      'PZ-005': [
        { author: 'Паоло М.', city: 'Турин', rating: 5, text: 'Аромат трюфеля чувствуется сразу, как только открываешь коробку. Лесные грибы сочные.' }
      ],
      'PZ-006': [
        { author: 'Фабио К.', city: 'Рим', rating: 5, text: 'Настоящий гуанчале и правильный яично-пекорино крем. Никаких сливок, римский канон!' }
      ],
      'PZ-007': [
        { author: 'Елена С.', city: 'Прага', rating: 5, text: 'Прекрасная веганская пицца. Артишоки и оливки каламата создают настоящий средиземноморский вкус.' }
      ],
      'PZ-008': [
        { author: 'Винченцо Т.', city: 'Генуя', rating: 5, text: 'Песто действительно генуэзский, а креветки нежные и сочные. Цедра лимона освежает.' }
      ],
      'PZ-009': [
        { author: 'Алекс В.', city: 'Бухарест', rating: 5, text: 'Сочный копченый цыпленок и тонкий красный лук. Отличный выбор для сытного ужина.' }
      ]
    };

    // -------------------------------------------------------------------------
    // 5. Theme Management
    // -------------------------------------------------------------------------
    function initTheme() {
      document.documentElement.setAttribute('data-theme', currentTheme);
      updateThemeButton();
    }

    function toggleTheme() {
      currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', currentTheme);
      localStorage.setItem('crosta_theme', currentTheme);
      updateThemeButton();
    }

    function updateThemeButton() {
      document.querySelectorAll('.theme-icon-slot').forEach(icon => {
        icon.textContent = currentTheme === 'dark' ? '☀️' : '🌙';
      });
    }

    // -------------------------------------------------------------------------
    // 6. Toast Notifications
    // -------------------------------------------------------------------------
    function showToast(message, type = 'success') {
      const container = document.getElementById('toast-container');
      const el = document.createElement('div');
      const colors = type === 'error'
        ? 'bg-brand-700 text-white border-red-800'
        : 'bg-surface text-textPrimary border-borderSubtle shadow-xl';
      el.className = `toast-item pointer-events-auto px-4 py-3 rounded-xl border text-xs sm:text-sm font-medium ${colors}`;
      el.textContent = message;
      container.appendChild(el);
      setTimeout(() => {
        el.classList.add('exiting');
        setTimeout(() => el.remove(), 350);
      }, 3600);
    }

    // -------------------------------------------------------------------------
    // 7. Initial Data Loading
    // -------------------------------------------------------------------------
    async function loadAllData() {
      try {
        const [menuRes, allPizzasRes, sizesRes, ordersRes, promoRes] = await Promise.all([
          fetch('/api/menu'),
          fetch('/api/menu/all'),
          fetch('/api/sizes'),
          fetch('/api/orders'),
          fetch('/api/promotions')
        ]);
        menu = await menuRes.json();
        allPizzasAdmin = await allPizzasRes.json();
        sizes = await sizesRes.json();
        orders = await ordersRes.json();
        promotions = await promoRes.json();

        menu.forEach(p => {
          if (!selectedSizes[p.id] && sizes.length > 1) {
            selectedSizes[p.id] = sizes[1].id;
          }
        });

        const storedUser = localStorage.getItem('crosta_user');
        if (storedUser && !currentUser) {
          currentUser = JSON.parse(storedUser);
          await refreshUserProfile();
        }

        updateHeaderAuth();
        updateActiveBadge();
        renderPromotions();
        renderMenu();
        renderCart();
        renderTracking();
        renderStaffDashboard();
        renderProfileView();
        handleRouting();
      } catch (err) {
        showToast('Ошибка связи с сервером C# API. Проверьте запуск dotnet run.', 'error');
      }
    }

    function updateActiveBadge() {
      const activeCount = orders.filter(o => !['Delivered', 'Cancelled'].includes(o.status)).length;
      const badge = document.getElementById('active-orders-badge');
      if (badge) badge.textContent = activeCount;
    }

    // -------------------------------------------------------------------------
    // 8. Routing (Hash & View Switcher)
    // -------------------------------------------------------------------------
    window.addEventListener('hashchange', handleRouting);

    function handleRouting() {
      const hash = window.location.hash || '#/';
      if (hash.startsWith('#/pizza/')) {
        const sku = hash.replace('#/pizza/', '').trim();
        openProductDetailBySku(sku);
      } else if (hash === '#/track') {
        switchView('track', false);
      } else if (hash === '#/profile') {
        switchView('profile', false);
      } else if (hash === '#/staff') {
        switchView('staff', false);
      } else {
        switchView('store', false);
      }
    }

    function navigateToCatalog() {
      window.location.hash = '#/';
    }

    function switchView(view, updateHash = true) {
      window.scrollTo(0, 0);
      const isReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

      if (updateHash) {
        if (view === 'store') window.location.hash = '#/';
        else if (view === 'track') window.location.hash = '#/track';
        else if (view === 'profile') window.location.hash = '#/profile';
        else if (view === 'staff') window.location.hash = '#/staff';
      }

      const allViews = ['store', 'product-detail', 'track', 'profile', 'staff'];
      allViews.forEach(v => {
        const sec = document.getElementById(`view-${v}`);
        if (sec) {
          const isTarget = v === view;
          sec.classList.toggle('hidden', !isTarget);
          if (isTarget && typeof gsap !== 'undefined' && !isReduced) {
            gsap.fromTo(sec, { opacity: 0, y: 6 }, { opacity: 1, y: 0, duration: 0.18, ease: 'power2.out', overwrite: 'auto' });
          }
        }
      });

      // Update Nav buttons
      ['store', 'track', 'staff'].forEach(v => {
        const tab = document.getElementById(`tab-${v}`);
        if (tab) {
          const isSel = v === view || (view === 'product-detail' && v === 'store');
          if (isSel) {
            tab.classList.add('font-semibold', 'text-textPrimary');
            tab.classList.remove('font-medium', 'text-textSecondary');
          } else {
            tab.classList.remove('font-semibold', 'text-textPrimary');
            tab.classList.add('font-medium', 'text-textSecondary');
          }
        }
      });

      updateElasticNavPill(view === 'product-detail' ? 'store' : view);

      if (view === 'track') renderTracking();
      if (view === 'profile') renderProfileView();
      if (view === 'staff') renderStaffDashboard();
    }

    function updateElasticNavPill(activeView) {
      const targetBtn = document.getElementById(`tab-${activeView}`);
      const pill = document.getElementById('nav-elastic-pill');
      if (!targetBtn || !pill) return;

      const offsetL = targetBtn.offsetLeft;
      const width = targetBtn.offsetWidth;
      const height = targetBtn.offsetHeight;

      pill.style.transform = `translateX(${offsetL}px)`;
      pill.style.width = `${width}px`;
      pill.style.height = `${height}px`;
    }

    // -------------------------------------------------------------------------
    // 9. Command Search (⌘K / Ctrl+K)
    // -------------------------------------------------------------------------
    document.addEventListener('keydown', (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        navigateToCatalog();
        setTimeout(() => {
          const input = document.getElementById('search-input');
          if (input) { input.focus(); input.select(); }
        }, 50);
      } else if (e.key === 'Escape') {
        closeCartDrawer();
        closeAuthModal();
        closeCancelModal();
      }
    });

    // -------------------------------------------------------------------------
    // 10. Slide-over Cart Drawer Management
    // -------------------------------------------------------------------------
    function openCartDrawer() {
      const drawer = document.getElementById('cart-drawer');
      const backdrop = document.getElementById('cart-drawer-backdrop');
      const panel = document.getElementById('cart-drawer-panel');

      drawer.classList.remove('pointer-events-none');
      backdrop.classList.remove('opacity-0', 'pointer-events-none');
      backdrop.classList.add('opacity-100', 'pointer-events-auto');
      panel.classList.remove('translate-x-full');
      panel.classList.add('translate-x-0');
      renderCart();
    }

    function closeCartDrawer() {
      const drawer = document.getElementById('cart-drawer');
      const backdrop = document.getElementById('cart-drawer-backdrop');
      const panel = document.getElementById('cart-drawer-panel');

      panel.classList.remove('translate-x-0');
      panel.classList.add('translate-x-full');
      backdrop.classList.remove('opacity-100', 'pointer-events-auto');
      backdrop.classList.add('opacity-0', 'pointer-events-none');
      setTimeout(() => {
        drawer.classList.add('pointer-events-none');
      }, 300);
    }

    // -------------------------------------------------------------------------
    // 11. Promotions & Promo Codes
    // -------------------------------------------------------------------------
    function renderPromotions() {
      const container = document.getElementById('promotions-grid');
      if (!promotions || promotions.length === 0) {
        container.innerHTML = '';
        return;
      }
      container.innerHTML = promotions.map(pr => `
        <div onclick="clickPromotionCard('${pr.promoCode || ''}', '${pr.targetCategory || 'Все'}')"
          class="card-interactive cursor-pointer p-4 rounded-2xl border border-borderSubtle bg-surface flex flex-col justify-between gap-3 shadow-xs">
          <div class="space-y-1.5">
            <span class="inline-block px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold uppercase tracking-wider bg-elevated text-brand-700 border border-borderSubtle">
              ${pr.badge}
            </span>
            <h3 class="text-sm font-serif font-bold text-textPrimary leading-snug">${pr.title}</h3>
            <p class="text-xs text-textSecondary leading-relaxed">${pr.subtitle}</p>
          </div>
          <div class="flex items-center justify-between pt-2 border-t border-borderSubtle text-xs">
            ${pr.promoCode ? `<span class="font-mono text-[11px] font-semibold text-textPrimary bg-elevated px-2 py-0.5 rounded border border-borderSubtle">Код: ${pr.promoCode}</span>` : `<span class="text-[11px] text-textSecondary font-mono">Действует до ${pr.validUntil}</span>`}
            <span class="text-xs font-semibold text-brand-700 flex items-center gap-1">
              <span>Применить</span> &rarr;
            </span>
          </div>
        </div>
      `).join('');
    }

    function clickPromotionCard(promoCode, category) {
      if (promoCode) {
        document.getElementById('promo-code-input').value = promoCode;
        applyPromo(promoCode);
      }
      if (category && category !== 'Все') {
        setCategory(category);
      }
      openCartDrawer();
    }

    function applyPromoFromInput() {
      const code = document.getElementById('promo-code-input').value.trim().toUpperCase();
      if (!code) {
        activePromo = null;
        renderCart();
        return;
      }
      applyPromo(code);
    }

    function applyPromo(code) {
      const promo = PROMO_CODES[code];
      const msgEl = document.getElementById('promo-msg');
      const badgeEl = document.getElementById('active-promo-badge');

      if (promo) {
        activePromo = promo;
        badgeEl.textContent = promo.code;
        badgeEl.classList.remove('hidden');
        msgEl.textContent = `✓ Промокод ${promo.code} успешно применён! (${promo.label})`;
        msgEl.className = 'text-[11px] text-bonus font-semibold block';
        showToast(`Промокод ${promo.code} применён: ${promo.label}!`);
      } else {
        activePromo = null;
        badgeEl.classList.add('hidden');
        msgEl.textContent = `Промокод "${code}" не найден или истёк`;
        msgEl.className = 'text-[11px] text-brand-700 font-semibold block';
        showToast(`Промокод "${code}" недействителен`, 'error');
      }
      renderCart();
    }

    // -------------------------------------------------------------------------
    // 12. Menu Catalog & In-Place Size Switching (Zero DOM Re-Render!)
    // -------------------------------------------------------------------------
    function setCategory(cat) {
      currentCategory = cat;
      document.querySelectorAll('.cat-btn').forEach(btn => {
        const active = btn.dataset.cat === cat;
        btn.className = active
          ? 'cat-btn px-3 py-1.5 rounded-lg text-xs font-semibold bg-textPrimary text-canvas shadow-xs'
          : 'cat-btn px-3 py-1.5 rounded-lg text-xs font-medium bg-elevated text-textPrimary hover:border-textSecondary border border-borderSubtle';
      });
      renderMenu();
    }

    // In-place size toggle: updates only the specific card without re-rendering the whole catalog!
    function selectPizzaSize(pizzaId, sizeId) {
      selectedSizes[pizzaId] = sizeId;
      const card = document.querySelector(`article[data-pizza-id="${pizzaId}"]`);
      if (!card) return;
      const pizza = menu.find(p => p.id === pizzaId);
      const size = sizes.find(s => s.id === sizeId);
      if (!pizza || !size) return;

      // 1. Update active states of size buttons inside card
      card.querySelectorAll('.pizza-size-btn').forEach(btn => {
        const isSel = Number(btn.dataset.sizeId) === sizeId;
        btn.className = `pizza-size-btn flex-1 py-1 px-1.5 rounded-md text-xs font-medium border transition ${
          isSel
            ? 'bg-textPrimary text-canvas border-textPrimary shadow-xs font-bold'
            : 'bg-elevated text-textPrimary border-borderSubtle hover:border-textSecondary'
        }`;
      });

      // 2. Update price in-place
      const priceEl = card.querySelector('.pizza-price-val');
      if (priceEl) {
        const newPrice = (pizza.basePriceEur * size.priceMultiplier).toFixed(2);
        priceEl.textContent = `€${newPrice}`;
        if (typeof gsap !== 'undefined' && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
          gsap.fromTo(priceEl, { scale: 1.15, color: 'var(--accent-primary)' }, { scale: 1, color: 'inherit', duration: 0.18, ease: 'power2.out' });
        }
      }

      // 3. Update weight in-place
      const weightEl = card.querySelector('.pizza-weight-val');
      if (weightEl) {
        weightEl.textContent = `${size.weightGrams} г`;
      }
    }

    function getEUAllergenBadges(pizza) {
      const ing = (pizza.ingredients + ' ' + pizza.name).toLowerCase();
      const list = [{ code: 'Глютен', label: '🌾 Глютен', title: 'Пшеничная мука Tipo 00' }];

      if (ing.includes('моцарелл') || ing.includes('fior di latte') || ing.includes('сыр') || 
          ing.includes('пармезан') || ing.includes('горгонзол') || ing.includes('сливк') || ing.includes('пекорино')) {
        list.push({ code: 'Лактоза', label: '🥛 Лактоза', title: 'Молочные продукты / сыр' });
      }

      if (ing.includes('орех') || ing.includes('песто')) {
        list.push({ code: 'Орехи', label: '🥜 Орехи', title: 'Орехи / кедровые семена' });
      }

      if (ing.includes('кревет') || ing.includes('морепродукт')) {
        list.push({ code: 'Морепродукты', label: '🦐 Морепродукты', title: 'Рыба и ракообразные' });
      }

      return list.map(a => 
        `<span title="${a.title}" class="px-1.5 py-0.5 rounded text-[10px] font-medium bg-elevated text-textSecondary border border-borderSubtle cursor-help">
          ${a.label}
        </span>`
      ).join('');
    }

    function renderMenu() {
      const grid = document.getElementById('menu-grid');
      const query = document.getElementById('search-input').value.trim().toLowerCase();

      const filtered = menu.filter(p => {
        const matchCat = currentCategory === 'Все' || p.category === currentCategory;
        const matchSearch = !query || p.name.toLowerCase().includes(query) || p.ingredients.toLowerCase().includes(query);
        return matchCat && matchSearch;
      });

      if (filtered.length === 0) {
        grid.innerHTML = `<div class="col-span-full bg-surface border border-borderSubtle rounded-2xl p-10 text-center">
          <p class="text-base font-serif font-bold text-textPrimary">По вашему запросу пиццы не найдены</p>
          <p class="text-xs text-textSecondary mt-1">Попробуйте сбросить фильтр категории или изменить поисковый запрос.</p>
        </div>`;
        return;
      }

      grid.innerHTML = filtered.map(p => {
        const activeSizeId = selectedSizes[p.id] || sizes[1]?.id || sizes[0]?.id;
        const activeSize = sizes.find(s => s.id === activeSizeId) || sizes[0];
        const price = (p.basePriceEur * (activeSize?.priceMultiplier || 1)).toFixed(2);
        const allergensHtml = getEUAllergenBadges(p);
        const svgIllustration = renderPizzaIllustrationSvg(p.sku, 150);

        const sizeButtons = sizes.map(s => {
          const isSel = s.id === activeSizeId;
          return `<button type="button" data-size-id="${s.id}" onclick="selectPizzaSize(${p.id}, ${s.id})"
            class="pizza-size-btn flex-1 py-1 px-1.5 rounded-md text-xs font-medium border transition ${
              isSel ? 'bg-textPrimary text-canvas border-textPrimary shadow-xs font-bold' : 'bg-elevated text-textPrimary border-borderSubtle hover:border-textSecondary'
            }">
            ${s.diameterCm} см
          </button>`;
        }).join('');

        return `
          <article data-pizza-id="${p.id}" class="card-interactive bg-surface border border-borderSubtle rounded-2xl p-5 flex flex-col justify-between gap-4 shadow-xs">
            <div class="space-y-3">
              
              <!-- Pizza Illustration Header -->
              <div class="relative py-2 flex items-center justify-center bg-elevated/40 rounded-xl border border-borderSubtle/60 overflow-hidden cursor-pointer group"
                onclick="window.location.hash='#/pizza/${p.sku}'">
                <div class="transform group-hover:scale-105 transition-transform duration-300">
                  ${svgIllustration}
                </div>
                <div class="absolute top-2.5 right-2.5">
                  <span class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-surface/90 text-textSecondary border border-borderSubtle shadow-xs">
                    ${p.dietaryTag}
                  </span>
                </div>
              </div>

              <!-- Title & SKU -->
              <div>
                <span class="font-mono text-[10px] text-textSecondary uppercase tracking-wider">${p.sku} · ${p.category}</span>
                <h3 class="text-lg font-serif font-bold text-textPrimary leading-snug hover:text-brand-700 transition cursor-pointer"
                  onclick="window.location.hash='#/pizza/${p.sku}'">
                  ${p.name}
                </h3>
              </div>

              <p class="text-xs text-textSecondary leading-relaxed">${p.description}</p>
              <p class="text-xs text-textSecondary"><strong class="font-semibold text-textPrimary">Состав:</strong> ${p.ingredients}</p>
              
              <!-- EU Allergens Badges -->
              <div class="flex flex-wrap items-center gap-1 pt-1">
                <span class="text-[10px] text-textSecondary font-semibold mr-0.5">Аллергены ЕС:</span>
                ${allergensHtml}
              </div>

              <!-- Prep, Weight, Calories -->
              <div class="flex items-center gap-2 text-[11px] text-textSecondary font-mono pt-1">
                <span>~${p.prepMinutes} мин</span>
                <span>·</span>
                <span class="pizza-weight-val font-semibold">${activeSize ? activeSize.weightGrams : 500} г</span>
                <span>·</span>
                <span>${p.caloriesKcal} ккал</span>
              </div>
            </div>

            <!-- Size Selector & Price Action -->
            <div class="space-y-3 pt-3 border-t border-borderSubtle">
              <div class="flex items-center gap-1.5" role="group" aria-label="Выбор размера">
                ${sizeButtons}
              </div>
              <div class="flex items-center justify-between gap-3">
                <div>
                  <span class="text-[10px] text-textSecondary block">Цена (вкл. НДС)</span>
                  <span class="pizza-price-val font-mono text-xl font-bold text-textPrimary tabular-nums">€${price}</span>
                </div>
                <div class="flex items-center gap-2">
                  <button type="button" onclick="window.location.hash='#/pizza/${p.sku}'"
                    class="px-2.5 py-2 text-xs font-semibold rounded-lg bg-elevated hover:bg-canvas border border-borderSubtle text-textSecondary hover:text-textPrimary transition">
                    О рецепте &rarr;
                  </button>
                  <button type="button" id="btn-add-${p.id}" onclick="addToCart(${p.id})"
                    class="px-3.5 py-2 bg-brand-700 hover:bg-brand-800 text-white text-xs sm:text-sm font-semibold rounded-lg transition shadow-sm flex items-center gap-1.5 active:scale-97">
                    <span>В корзину</span>
                  </button>
                </div>
              </div>
            </div>
          </article>
        `;
      }).join('');
    }

    // -------------------------------------------------------------------------
    // 13. Product Detail Page (#/pizza/:sku)
    // -------------------------------------------------------------------------
    function openProductDetailBySku(sku) {
      const pizza = menu.find(p => p.sku.toUpperCase() === sku.toUpperCase()) || allPizzasAdmin.find(p => p.sku.toUpperCase() === sku.toUpperCase());
      if (!pizza) {
        showToast(`Пицца ${sku} не найдена`, 'error');
        navigateToCatalog();
        return;
      }

      currentDetailPizza = pizza;
      currentDetailQty = 1;
      selectedDetailToppings = {};
      currentDetailSizeId = selectedSizes[pizza.id] || sizes[1]?.id || sizes[0]?.id;

      document.getElementById('detail-sku').textContent = pizza.sku;
      document.getElementById('detail-name').textContent = pizza.name;
      document.getElementById('detail-desc').textContent = pizza.description;
      document.getElementById('detail-ingredients').textContent = pizza.ingredients + '. Прямые сертифицированные поставки из провинций Кампания и Парма (Италия).';
      document.getElementById('detail-dietary').textContent = pizza.dietaryTag;
      document.getElementById('detail-category-badge').textContent = pizza.category;
      document.getElementById('detail-qty-val').textContent = '1';

      // Illustration
      document.getElementById('detail-illustration-slot').innerHTML = renderPizzaIllustrationSvg(pizza.sku, 240);

      // Allergens
      document.getElementById('detail-allergens').innerHTML = getEUAllergenBadges(pizza);

      // Nutrition
      const nut = NUTRITION_MAP[pizza.sku] || { kcal: pizza.caloriesKcal, p: 32, f: 28, c: 100 };
      document.getElementById('detail-nutrition').innerHTML = `
        <div class="bg-surface p-1.5 rounded border border-borderSubtle">
          <span class="block text-[9px] text-textSecondary">Ккал</span>
          <span class="font-bold text-textPrimary">${nut.kcal}</span>
        </div>
        <div class="bg-surface p-1.5 rounded border border-borderSubtle">
          <span class="block text-[9px] text-textSecondary">Белки</span>
          <span class="font-bold text-textPrimary">${nut.p}г</span>
        </div>
        <div class="bg-surface p-1.5 rounded border border-borderSubtle">
          <span class="block text-[9px] text-textSecondary">Жиры</span>
          <span class="font-bold text-textPrimary">${nut.f}г</span>
        </div>
        <div class="bg-surface p-1.5 rounded border border-borderSubtle">
          <span class="block text-[9px] text-textSecondary">Углев</span>
          <span class="font-bold text-textPrimary">${nut.c}г</span>
        </div>
      `;

      // Diameter options
      document.getElementById('detail-size-options').innerHTML = sizes.map(s => {
        const isSel = s.id === currentDetailSizeId;
        return `
          <button type="button" onclick="setDetailSize(${s.id})"
            class="py-2 px-3 rounded-xl border text-xs text-center transition ${
              isSel
                ? 'bg-textPrimary text-canvas border-textPrimary shadow-xs font-bold'
                : 'bg-elevated text-textPrimary border-borderSubtle hover:border-textSecondary font-medium'
            }">
            <div class="font-bold">${s.diameterCm} см (${s.label.split(' ')[0]})</div>
            <div class="text-[10px] text-textSecondary font-mono mt-0.5">${s.weightGrams} г</div>
          </button>
        `;
      }).join('');

      // Extra toppings
      document.getElementById('detail-toppings-options').innerHTML = EXTRA_TOPPINGS.map(top => `
        <label class="flex items-center justify-between p-2.5 rounded-xl border border-borderSubtle bg-elevated cursor-pointer hover:border-textSecondary transition">
          <div class="flex items-center gap-2">
            <input type="checkbox" onchange="toggleDetailTopping('${top.id}', this.checked)"
              class="rounded text-brand-700 focus:ring-brand-700" />
            <span class="font-medium text-textPrimary">${top.name}</span>
          </div>
          <span class="font-mono font-semibold text-textSecondary">+€${top.price.toFixed(2)}</span>
        </label>
      `).join('');

      updateDetailPriceCalculation();
      renderDetailReviews(pizza.sku);
      switchView('product-detail', false);
    }

    function setDetailSize(sizeId) {
      currentDetailSizeId = sizeId;
      selectedSizes[currentDetailPizza.id] = sizeId;
      openProductDetailBySku(currentDetailPizza.sku);
    }

    function toggleDetailTopping(id, isChecked) {
      if (isChecked) {
        selectedDetailToppings[id] = true;
      } else {
        delete selectedDetailToppings[id];
      }
      updateDetailPriceCalculation();
    }

    function changeDetailQty(delta) {
      currentDetailQty = Math.max(1, currentDetailQty + delta);
      document.getElementById('detail-qty-val').textContent = currentDetailQty;
      updateDetailPriceCalculation();
    }

    function updateDetailPriceCalculation() {
      if (!currentDetailPizza) return;
      const size = sizes.find(s => s.id === currentDetailSizeId) || sizes[0];
      let unitPrice = currentDetailPizza.basePriceEur * size.priceMultiplier;
      Object.keys(selectedDetailToppings).forEach(tid => {
        const top = EXTRA_TOPPINGS.find(t => t.id === tid);
        if (top) unitPrice += top.price;
      });
      const total = (unitPrice * currentDetailQty).toFixed(2);
      document.getElementById('detail-price-total').textContent = `€${total}`;
    }

    function addDetailToCart() {
      if (!currentDetailPizza) return;
      const sizeId = currentDetailSizeId;
      const existing = cart.find(item => item.pizzaId === currentDetailPizza.id && item.sizeId === sizeId);
      if (existing) {
        existing.quantity += currentDetailQty;
      } else {
        cart.push({ pizzaId: currentDetailPizza.id, sizeId: sizeId, quantity: currentDetailQty });
      }
      renderCart();
      showToast(`Добавлено в корзину: ${currentDetailPizza.name} (${currentDetailQty} шт.)`);
      openCartDrawer();
    }

    // -------------------------------------------------------------------------
    // Star Rating Helper & DesignBookmark Spring Component (https://designbookmark.com/motion#db-star-rating)
    // -------------------------------------------------------------------------
    function renderStarRatingSvgDisplay(score) {
      const s = Math.max(1, Math.min(5, Math.round(score || 5)));
      const path = 'M12 3.2l2.6 5.5 6 .8-4.4 4.1 1.1 5.9L12 16.6l-5.3 2.9 1.1-5.9-4.4-4.1 6-.8z';
      let starsHtml = '';
      for (let i = 1; i <= 5; i++) {
        const filled = i <= s;
        const fill = filled ? '#F59E0B' : 'transparent';
        const stroke = filled ? '#F59E0B' : 'var(--border-subtle)';
        starsHtml += `<svg class="w-3.5 h-3.5 inline-block -mt-0.5" viewBox="0 0 24 24"><path d="${path}" fill="${fill}" stroke="${stroke}" stroke-width="1.4"/></svg>`;
      }
      return `<span class="inline-flex items-center gap-0.5 text-amber-500" title="${s} из 5 звёзд">${starsHtml}</span>`;
    }

    function initStarRatingComponent(container, options = {}) {
      if (!container) return null;
      container.innerHTML = '';

      const labels = options.labels || [
        'Нажмите на звезду',
        '1 · Требует доработки',
        '2 · Нормально',
        '3 · Хорошо',
        '4 · Очень вкусно!',
        '5 · Шедевр Neapoli!'
      ];
      let currentRating = typeof options.initialRating === 'number' ? options.initialRating : 5;
      const STAR_PATH = 'M12 3.2l2.6 5.5 6 .8-4.4 4.1 1.1 5.9L12 16.6l-5.3 2.9 1.1-5.9-4.4-4.1 6-.8z';

      const frame = document.createElement('div');
      frame.className = 'db-star-frame';

      const row = document.createElement('div');
      row.className = 'db-star-row';

      const wordWrap = document.createElement('div');
      wordWrap.className = 'db-star-word';

      const col = document.createElement('div');
      col.className = 'db-star-col';
      col.innerHTML = labels.map(l => `<b>${l}</b>`).join('');
      wordWrap.appendChild(col);

      frame.appendChild(row);
      frame.appendChild(wordWrap);
      container.appendChild(frame);

      // Spring helper S(v, k, c)
      function S(v, k, c) {
        return { x: v, v: 0, t: v, k: k, c: c };
      }
      function step(s, dt) {
        const a = -s.k * (s.x - s.t) - s.c * s.v;
        s.v += a * dt;
        s.x += s.v * dt;
        return s.x;
      }

      const stars = [];
      const starEl = [];

      for (let i = 0; i < 5; i++) {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'db-star-btn';
        btn.setAttribute('aria-label', `${i + 1} из 5 звёзд`);
        btn.innerHTML = `<svg viewBox="0 0 24 24"><path d="${STAR_PATH}"/></svg>`;
        row.appendChild(btn);

        starEl.push({
          btn,
          path: btn.querySelector('path'),
          svg: btn.querySelector('svg')
        });

        const initialFill = i < currentRating ? 1 : 0;
        stars.push({
          f: S(initialFill, 300, 24), // fill spring
          p: S(1, 520, 13)            // pop spring
        });

        btn.addEventListener('pointerenter', () => {
          preview(i + 1);
        });
        btn.addEventListener('click', () => {
          setRating(i + 1);
        });
      }

      row.addEventListener('pointerleave', () => {
        preview(currentRating);
      });

      const Wd = S(currentRating, 260, 22);

      let animRunning = false;
      let lastTime = performance.now();
      let settledFrames = 0;

      function colStyle(f) {
        if (f <= 0.05) {
          return {
            stroke: 'var(--border-subtle)',
            fill: 'transparent',
            filter: 'none'
          };
        }
        return {
          stroke: `rgba(255, 210, 63, ${(0.4 + f * 0.6).toFixed(2)})`,
          fill: `rgba(255, 210, 63, ${f.toFixed(2)})`,
          filter: f > 0.4 ? 'drop-shadow(0 0 6px rgba(255, 210, 63, 0.45))' : 'none'
        };
      }

      function renderFrame() {
        for (let i = 0; i < 5; i++) {
          const s = stars[i];
          const el = starEl[i];
          const c = colStyle(Math.max(0, Math.min(1, s.f.x)));
          el.path.style.fill = c.fill;
          el.path.style.stroke = c.stroke;
          el.path.style.filter = c.filter;
          el.path.setAttribute('fill', c.fill);
          el.path.setAttribute('stroke', c.stroke);
          el.svg.style.transform = `scale(${Math.max(0, s.p.x).toFixed(3)})`;
        }
        col.style.transform = `translateY(${(-20 * Wd.x).toFixed(2)}px)`;
      }

      function loop(now) {
        if (!animRunning) return;
        const dt = Math.min((now - lastTime) / 1000, 0.033);
        lastTime = now;

        let active = false;
        for (let i = 0; i < 5; i++) {
          const s = stars[i];
          step(s.f, dt);
          step(s.p, dt);
          if (Math.abs(s.f.x - s.f.t) > 0.002 || Math.abs(s.f.v) > 0.002) active = true;
          if (Math.abs(s.p.x - 1) > 0.002 || Math.abs(s.p.v) > 0.002) active = true;
        }

        step(Wd, dt);
        if (Math.abs(Wd.x - Wd.t) > 0.002 || Math.abs(Wd.v) > 0.002) active = true;

        renderFrame();

        if (!active) {
          settledFrames++;
          if (settledFrames > 8) {
            animRunning = false;
            for (let i = 0; i < 5; i++) {
              stars[i].f.x = stars[i].f.t;
              stars[i].f.v = 0;
              stars[i].p.x = 1;
              stars[i].p.v = 0;
            }
            Wd.x = Wd.t;
            Wd.v = 0;
            renderFrame();
            return;
          }
        } else {
          settledFrames = 0;
        }

        requestAnimationFrame(loop);
      }

      function startLoop() {
        settledFrames = 0;
        if (!animRunning) {
          animRunning = true;
          lastTime = performance.now();
          requestAnimationFrame(loop);
        }
      }

      function preview(val) {
        Wd.t = val;
        for (let i = 0; i < 5; i++) {
          const s = stars[i];
          const fill = i < val ? 1 : 0;
          setTimeout(() => {
            s.f.t = fill;
            if (fill) {
              s.p.x = 0.72;
              s.p.v = 6.8;
            } else {
              s.p.x = 1;
              s.p.v = 0;
            }
            startLoop();
          }, i * 45);
        }
        startLoop();
      }

      function setRating(val) {
        currentRating = val;
        preview(val);
        if (typeof options.onChange === 'function') {
          options.onChange(val);
        }
      }

      renderFrame();
      startLoop();

      return {
        getRating: () => currentRating,
        setRating,
        preview
      };
    }

    function renderDetailReviews(sku) {
      const list = REVIEWS_DATA[sku] || REVIEWS_DATA['PZ-001'];
      document.getElementById('detail-reviews-list').innerHTML = list.map(r => `
        <div class="p-3.5 rounded-xl bg-elevated border border-borderSubtle space-y-1.5">
          <div class="flex items-center justify-between">
            <span class="font-bold text-textPrimary">${r.author} <span class="text-[10px] text-textSecondary font-normal">(${r.city})</span></span>
            ${renderStarRatingSvgDisplay(r.rating || 5)}
          </div>
          <p class="text-textSecondary leading-relaxed">${r.text}</p>
        </div>
      `).join('');
    }

    let detailStarRatingInstance = null;
    let detailReviewStars = 5;

    function toggleReviewForm() {
      const form = document.getElementById('detail-review-form');
      if (!form) return;
      const isHidden = form.classList.toggle('hidden');
      if (!isHidden) {
        const slot = document.getElementById('detail-star-rating-slot');
        if (slot) {
          detailStarRatingInstance = initStarRatingComponent(slot, {
            initialRating: detailReviewStars,
            onChange: (r) => {
              detailReviewStars = r;
            }
          });
        }
        const ta = document.getElementById('detail-review-input');
        if (ta) ta.focus();
      }
    }

    function submitDetailReview() {
      const text = document.getElementById('detail-review-input').value.trim();
      if (!text) {
        showToast('Пожалуйста, напишите пару слов в отзыве', 'error');
        return;
      }
      const reviewsContainer = document.getElementById('detail-reviews-list');
      const author = currentUser ? currentUser.fullName : 'Гость ресторана';
      const rating = detailStarRatingInstance ? detailStarRatingInstance.getRating() : detailReviewStars;
      const starsHtml = renderStarRatingSvgDisplay(rating);

      reviewsContainer.insertAdjacentHTML('afterbegin', `
        <div class="p-4 rounded-xl bg-elevated border border-brand-700/40 space-y-2 shadow-xs transition-all animate-fadeIn">
          <div class="flex items-center justify-between">
            <span class="font-bold text-textPrimary">${author} <span class="text-[10px] text-brand-700 font-semibold">(Только что)</span></span>
            ${starsHtml}
          </div>
          <p class="text-textSecondary leading-relaxed">${text}</p>
        </div>
      `);
      document.getElementById('detail-review-input').value = '';
      toggleReviewForm();
      showToast('Спасибо за ваш отзыв! Шеф-пиццайоло ценит каждое мнение.');
    }

    // -------------------------------------------------------------------------
    // 14. Cart Drawer Calculations & Rendering
    // -------------------------------------------------------------------------
    function addToCart(pizzaId) {
      const sizeId = selectedSizes[pizzaId] || sizes[1]?.id || sizes[0].id;
      const existing = cart.find(item => item.pizzaId === pizzaId && item.sizeId === sizeId);
      if (existing) {
        existing.quantity += 1;
      } else {
        cart.push({ pizzaId, sizeId, quantity: 1 });
      }
      renderCart();

      const pizza = menu.find(p => p.id === pizzaId);
      showToast(`Добавлено: ${pizza ? pizza.name : 'Пицца'}`);

      // Tactile button pop
      const btn = document.getElementById(`btn-add-${pizzaId}`);
      if (btn) {
        const origText = btn.innerHTML;
        btn.innerHTML = `<span>✓ В корзине</span>`;
        btn.classList.replace('bg-brand-700', 'bg-bonus');
        setTimeout(() => {
          btn.innerHTML = origText;
          btn.classList.replace('bg-bonus', 'bg-brand-700');
        }, 900);
      }
    }

    function updateCartQty(index, delta) {
      cart[index].quantity += delta;
      if (cart[index].quantity <= 0) {
        cart.splice(index, 1);
      }
      renderCart();
    }

    function setBonusSpend(val) {
      bonusToSpend = Math.max(0, parseFloat(val) || 0);
      renderCart();
    }

    function spendMaxBonus(maxAllowed) {
      bonusToSpend = maxAllowed;
      renderCart();
    }

    function renderCart() {
      const container = document.getElementById('cart-items');
      const bonusBox = document.getElementById('cart-bonus-box');
      const totalItems = cart.reduce((acc, i) => acc + i.quantity, 0);

      // Update counters
      const countPill = document.getElementById('cart-count-pill');
      if (countPill) countPill.textContent = `${totalItems} поз.`;

      const headerCount = document.getElementById('header-cart-count');
      if (headerCount) headerCount.textContent = totalItems;

      const headerCountMobile = document.getElementById('header-cart-count-mobile');
      if (headerCountMobile) headerCountMobile.textContent = totalItems;

      const mfc = document.getElementById('mobile-floating-cart');
      const mfcCount = document.getElementById('mfc-count');
      const mfcTotal = document.getElementById('mfc-total');

      if (mfc) {
        if (totalItems > 0) {
          mfc.classList.remove('hidden');
          if (mfcCount) mfcCount.textContent = totalItems;
        } else {
          mfc.classList.add('hidden');
        }
      }

      if (cart.length === 0) {
        container.innerHTML = `<div class="py-8 text-center border border-dashed border-borderSubtle rounded-xl">
          <p class="text-xs font-semibold text-textSecondary">Корзина пока пуста</p>
          <p class="text-[11px] text-textSecondary mt-0.5">Выберите пиццу в меню для оформления</p>
        </div>`;
        bonusBox.innerHTML = `<div class="text-center py-1 text-textSecondary">Бонусы станут доступны после добавления блюд</div>`;
        document.getElementById('summary-gross').textContent = '€0.00';
        document.getElementById('summary-vat').textContent = '€0.00';
        document.getElementById('summary-delivery').textContent = '€0.00';
        document.getElementById('summary-total').textContent = '€0.00';
        document.getElementById('btn-submit-total').textContent = '€0.00';
        document.getElementById('header-cart-total').textContent = '€0.00';
        document.getElementById('summary-bonus-row').classList.add('hidden');
        document.getElementById('summary-promo-row').classList.add('hidden');
        document.getElementById('summary-cashback-hint').classList.add('hidden');
        if (mfcTotal) mfcTotal.textContent = '€0.00';
        return;
      }

      let grossTotal = 0;
      container.innerHTML = cart.map((item, idx) => {
        const pizza = menu.find(p => p.id === item.pizzaId) || allPizzasAdmin.find(p => p.id === item.pizzaId) || { name: 'Пицца', basePriceEur: 10 };
        const size = sizes.find(s => s.id === item.sizeId) || { label: '30 см', priceMultiplier: 1 };
        const unitPrice = +(pizza.basePriceEur * size.priceMultiplier).toFixed(2);
        const lineTotal = +(unitPrice * item.quantity).toFixed(2);
        grossTotal += lineTotal;

        return `
          <div class="flex items-center justify-between gap-2 p-2.5 rounded-xl bg-elevated border border-borderSubtle">
            <div class="min-w-0">
              <p class="text-xs font-bold text-textPrimary truncate">${pizza.name}</p>
              <p class="text-[11px] text-textSecondary">${size.label} · <span class="font-mono">€${unitPrice.toFixed(2)}</span></p>
            </div>
            <div class="flex items-center gap-1.5 shrink-0">
              <button type="button" onclick="updateCartQty(${idx}, -1)" class="w-6 h-6 rounded-lg bg-surface border border-borderSubtle text-textPrimary text-xs font-bold hover:bg-elevated">-</button>
              <span class="font-mono text-xs font-semibold w-5 text-center text-textPrimary">${item.quantity}</span>
              <button type="button" onclick="updateCartQty(${idx}, 1)" class="w-6 h-6 rounded-lg bg-surface border border-borderSubtle text-textPrimary text-xs font-bold hover:bg-elevated">+</button>
            </div>
          </div>
        `;
      }).join('');

      // Promo calculation
      let promoDiscount = 0;
      let freeDelivByPromo = false;
      if (activePromo) {
        if (activePromo.discountEur) promoDiscount = Math.min(activePromo.discountEur, grossTotal);
        else if (activePromo.percent) promoDiscount = +(grossTotal * (activePromo.percent / 100)).toFixed(2);
        if (activePromo.freeDelivery) freeDelivByPromo = true;
      }

      const postPromoGross = Math.max(0, +(grossTotal - promoDiscount).toFixed(2));

      // Bonus redemption (up to 30% of post-promo gross)
      const maxSpendAllowed = currentUser
        ? Math.min(currentUser.bonusBalance, +(postPromoGross * 0.30).toFixed(2))
        : 0;

      if (bonusToSpend > maxSpendAllowed) bonusToSpend = maxSpendAllowed;

      if (currentUser) {
        bonusBox.innerHTML = `
          <div class="flex items-center justify-between">
            <span class="font-bold text-textPrimary flex items-center gap-1">
              <span class="text-bonus">★</span> Списание бонусов (Баланс: €${currentUser.bonusBalance.toFixed(2)})
            </span>
            <button type="button" onclick="spendMaxBonus(${maxSpendAllowed})" class="text-[11px] text-brand-700 hover:underline font-semibold">
              Макс: €${maxSpendAllowed.toFixed(2)}
            </button>
          </div>
          <div class="flex items-center gap-2 pt-1">
            <input type="range" min="0" max="${maxSpendAllowed}" step="0.5" value="${bonusToSpend}"
              oninput="setBonusSpend(this.value)" class="flex-1 accent-brand-700 cursor-pointer" />
            <input type="number" min="0" max="${maxSpendAllowed}" step="0.5" value="${bonusToSpend.toFixed(2)}"
              onchange="setBonusSpend(this.value)"
              class="w-16 px-2 py-0.5 text-xs bg-canvas border border-borderSubtle rounded font-mono text-right tabular-nums text-textPrimary" />
          </div>
          <p class="text-[10px] text-textSecondary">Можно списать до 30% стоимости пицц (€${(postPromoGross * 0.30).toFixed(2)}).</p>
        `;
      } else {
        bonusBox.innerHTML = `
          <div class="flex items-center justify-between text-textSecondary">
            <span>Хотите оплатить бонусами?</span>
            <button type="button" onclick="openAuthModal('login')" class="text-brand-700 font-semibold hover:underline">
              Войти в профиль &rarr;
            </button>
          </div>
        `;
      }

      const deliveryFee = (grossTotal >= 25.0 || freeDelivByPromo) ? 0.0 : 2.5;
      const total = Math.max(0, +(postPromoGross - bonusToSpend + deliveryFee).toFixed(2));
      const net = +(postPromoGross / 1.10).toFixed(2);
      const vat = +(postPromoGross - net).toFixed(2);
      const cashback = currentUser ? +((postPromoGross - bonusToSpend) * 0.05).toFixed(2) : 0;

      document.getElementById('summary-gross').textContent = `€${grossTotal.toFixed(2)}`;
      document.getElementById('summary-vat').textContent = `€${vat.toFixed(2)}`;
      document.getElementById('summary-delivery').textContent = deliveryFee === 0 ? 'Бесплатно (€0.00)' : `€${deliveryFee.toFixed(2)}`;
      document.getElementById('summary-total').textContent = `€${total.toFixed(2)}`;
      document.getElementById('btn-submit-total').textContent = `€${total.toFixed(2)}`;
      document.getElementById('header-cart-total').textContent = `€${total.toFixed(2)}`;
      if (mfcTotal) mfcTotal.textContent = `€${total.toFixed(2)}`;

      // Promo row
      const promoRow = document.getElementById('summary-promo-row');
      if (promoDiscount > 0 || freeDelivByPromo) {
        promoRow.classList.remove('hidden');
        document.getElementById('summary-promo-label').textContent = `Промокод ${activePromo.code}`;
        document.getElementById('summary-promo-val').textContent = freeDelivByPromo && promoDiscount === 0
          ? 'Беспл. доставка'
          : `-€${promoDiscount.toFixed(2)}`;
      } else {
        promoRow.classList.add('hidden');
      }

      // Bonus row
      const bonusRow = document.getElementById('summary-bonus-row');
      if (bonusToSpend > 0) {
        bonusRow.classList.remove('hidden');
        document.getElementById('summary-bonus-spent').textContent = `-€${bonusToSpend.toFixed(2)}`;
      } else {
        bonusRow.classList.add('hidden');
      }

      // Cashback hint
      const cashbackHint = document.getElementById('summary-cashback-hint');
      if (currentUser && cashback > 0) {
        cashbackHint.classList.remove('hidden');
        document.getElementById('summary-cashback-val').textContent = `+€${cashback.toFixed(2)}`;
      } else {
        cashbackHint.classList.add('hidden');
      }
    }

    // -------------------------------------------------------------------------
    // 15. Kokonut UI CardField (Luhn Check, Slide-Away Groups, Brand Flip)
    // -------------------------------------------------------------------------
    const CARD_BRANDS = [
      { brand: 'amex', match: /^3[47]/, groups: [4, 6, 5], cvc: 4, name: 'American Express' },
      { brand: 'visa', match: /^4/, groups: [4, 4, 4, 4], cvc: 3, name: 'Visa' },
      { brand: 'mastercard', match: /^(5[1-5]|2[2-7])/, groups: [4, 4, 4, 4], cvc: 3, name: 'Mastercard' },
      { brand: 'discover', match: /^(6011|65|64[4-9])/, groups: [4, 4, 4, 4], cvc: 3, name: 'Discover' }
    ];
    const UNKNOWN_BRAND = { brand: 'unknown', match: /^/, groups: [4, 4, 4, 4], cvc: 3, name: 'Банковская карта' };

    function getCardSpec(digits) {
      return CARD_BRANDS.find(b => b.match.test(digits)) || UNKNOWN_BRAND;
    }

    function getCardLength(spec) {
      return spec.groups.reduce((a, b) => a + b, 0);
    }

    function getCardGroups(digits, spec) {
      const out = [];
      let at = 0;
      for (const size of spec.groups) {
        if (at >= digits.length) break;
        out.push(digits.slice(at, at + size));
        at += size;
      }
      return out;
    }

    function checkLuhn(digits) {
      let sum = 0;
      for (let i = 0; i < digits.length; i++) {
        let d = Number(digits.charAt(digits.length - 1 - i));
        if (i % 2 === 1) {
          d *= 2;
          if (d > 9) d -= 9;
        }
        sum += d;
      }
      return sum % 10 === 0;
    }

    function getBrandMarkSvg(brand, back) {
      if (back) {
        if (brand === 'amex') {
          return `<svg aria-hidden="true" class="h-5 w-8" viewBox="0 0 32 20">
            <rect fill="#f4f4f5" stroke="#cbd5e1" height="19" rx="3" width="31" x="0.5" y="0.5"/>
            <rect fill="#d4d4d8" height="2" rx="1" width="12" x="4" y="12"/>
            <rect fill="#ff9f0a" height="5" rx="1.5" width="9" x="19" y="4"/>
          </svg>`;
        }
        return `<svg aria-hidden="true" class="h-5 w-8" viewBox="0 0 32 20">
          <rect fill="#f4f4f5" stroke="#cbd5e1" height="19" rx="3" width="31" x="0.5" y="0.5"/>
          <rect fill="#27272a" height="4" width="31" x="0.5" y="3"/>
          <rect fill="#ffffff" height="4" rx="1" width="16" x="4" y="10"/>
          <rect fill="#ff9f0a" height="5" rx="1.5" width="7" x="21" y="9.5"/>
        </svg>`;
      }
      switch (brand) {
        case 'visa':
          return `<svg aria-hidden="true" class="h-5 w-8" viewBox="0 0 32 20">
            <rect fill="#ffffff" stroke="#cbd5e1" height="19" rx="3" width="31" x="0.5" y="0.5"/>
            <text fill="#1a1f71" font-family="Arial, sans-serif" font-size="9" font-style="italic" font-weight="800" text-anchor="middle" x="16" y="13.4">VISA</text>
          </svg>`;
        case 'mastercard':
          return `<svg aria-hidden="true" class="h-5 w-8" viewBox="0 0 32 20">
            <rect fill="#18181b" height="20" rx="3.5" width="32"/>
            <circle cx="13" cy="10" fill="#eb001b" r="5.5"/>
            <circle cx="19" cy="10" fill="#f79e1b" r="5.5"/>
            <path d="M16 5.4a5.5 5.5 0 0 1 0 9.2a5.5 5.5 0 0 1 0-9.2z" fill="#ff5f00"/>
          </svg>`;
        case 'amex':
          return `<svg aria-hidden="true" class="h-5 w-8" viewBox="0 0 32 20">
            <rect fill="#1f72cd" height="20" rx="3.5" width="32"/>
            <text fill="white" font-family="Arial, sans-serif" font-size="7.4" font-weight="800" letter-spacing="0.2" text-anchor="middle" x="16" y="12.6">AMEX</text>
          </svg>`;
        case 'discover':
          return `<svg aria-hidden="true" class="h-5 w-8" viewBox="0 0 32 20">
            <rect fill="#ffffff" stroke="#cbd5e1" height="19" rx="3" width="31" x="0.5" y="0.5"/>
            <circle cx="23.5" cy="10" fill="#f58220" r="3.6"/>
            <text fill="#231f20" font-family="Arial, sans-serif" font-size="5.4" font-weight="800" x="4" y="12">DISC</text>
          </svg>`;
        default:
          return `<svg aria-hidden="true" class="h-5 w-8 text-textSecondary" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6">
            <rect x="2" y="5" width="20" height="14" rx="3"/>
            <line x1="2" y1="10" x2="22" y2="10"/>
            <line x1="6" y1="15" x2="10" y2="15"/>
          </svg>`;
      }
    }

    let cardState = {
      number: '',
      expiry: '',
      cvc: '',
      isCollapsed: false,
      isFocused: false
    };

    function renderCardBrand(back = false) {
      const slot = document.getElementById('cardfield-brand-slot');
      if (!slot) return;
      const spec = getCardSpec(cardState.number);
      const key = `${back ? 'back-' : 'front-'}${spec.brand}`;
      if (slot.dataset.key === key) return;
      slot.dataset.key = key;

      slot.style.opacity = '0';
      slot.style.transform = 'translateY(4px)';
      setTimeout(() => {
        slot.innerHTML = getBrandMarkSvg(spec.brand, back);
        slot.style.opacity = '1';
        slot.style.transform = 'translateY(0)';
      }, 70);

      const brandBadge = document.getElementById('cardfield-brand-name');
      if (brandBadge) {
        if (spec.brand !== 'unknown') {
          brandBadge.textContent = `· ${spec.name}`;
          brandBadge.classList.remove('hidden');
        } else {
          brandBadge.classList.add('hidden');
        }
      }
    }

    function renderCardMirror() {
      const mirror = document.getElementById('cardfield-mirror');
      const placeholder = document.getElementById('cardfield-placeholder');
      if (!mirror) return;

      const digits = cardState.number;
      const spec = getCardSpec(digits);
      const groups = getCardGroups(digits, spec);

      if (digits.length === 0 && !cardState.isFocused) {
        mirror.innerHTML = '';
        if (placeholder) placeholder.classList.remove('hidden');
        return;
      }

      if (placeholder) placeholder.classList.add('hidden');

      let typedRemain = digits.length;
      let html = '';
      spec.groups.forEach((size, i) => {
        const typedPart = groups[i] || '';
        const used = Math.min(size, typedRemain);
        typedRemain = Math.max(0, typedRemain - used);
        const ghostCount = cardState.isCollapsed ? 0 : (size - used);
        const ghostPart = '0'.repeat(ghostCount);
        const isLast = i === spec.groups.length - 1;
        const opacityStyle = (cardState.isCollapsed && !isLast) ? 'opacity: 0;' : 'opacity: 1;';

        html += `<span id="cg-group-${i}" class="card-group-span inline-block" style="${opacityStyle}">` +
          `<span class="text-textPrimary">${typedPart}</span>` +
          `<span class="text-textSecondary/30">${ghostPart}</span>` +
          (isLast ? '' : ' ') +
        `</span>`;
      });
      mirror.innerHTML = html;

      if (cardState.isCollapsed) {
        const lastGroup = document.getElementById(`cg-group-${spec.groups.length - 1}`);
        const shift = lastGroup ? lastGroup.offsetLeft : 0;
        mirror.style.transform = `translateX(-${shift}px)`;
      } else {
        mirror.style.transform = 'translateX(0)';
      }
    }

    function showCardError(msg) {
      const row = document.getElementById('cardfield-row');
      const hintText = document.getElementById('cardfield-hint-text');
      const hintIcon = document.getElementById('cardfield-hint-icon');
      if (row) row.classList.add('has-error');
      if (hintText) {
        hintText.textContent = msg;
        hintText.classList.add('text-red-500');
        hintText.classList.remove('text-textSecondary');
      }
      if (hintIcon) hintIcon.classList.add('text-red-500');
      if (row && typeof gsap !== 'undefined') {
        gsap.fromTo(row, { x: 0 }, { x: -8, duration: 0.06, yoyo: true, repeat: 5, onComplete: () => gsap.set(row, { x: 0 }) });
      }
    }

    function clearCardError() {
      const row = document.getElementById('cardfield-row');
      const hintText = document.getElementById('cardfield-hint-text');
      const hintIcon = document.getElementById('cardfield-hint-icon');
      if (row) row.classList.remove('has-error');
      if (hintText) {
        hintText.textContent = 'Сквозное 256-bit SSL шифрование (PCI DSS)';
        hintText.classList.remove('text-red-500');
        hintText.classList.add('text-textSecondary');
      }
      if (hintIcon) hintIcon.classList.remove('text-red-500');
    }

    function collapseCardNumber() {
      cardState.isCollapsed = true;
      renderCardMirror();

      const editBtn = document.getElementById('cardfield-edit-btn');
      const extra = document.getElementById('cardfield-extra');
      const numInput = document.getElementById('cardfield-number-input');

      if (editBtn) editBtn.classList.remove('hidden');
      if (numInput) numInput.setAttribute('tabindex', '-1');

      if (extra) {
        extra.classList.remove('hidden');
        if (typeof gsap !== 'undefined') {
          gsap.fromTo(extra, { opacity: 0, x: 16 }, { opacity: 1, x: 0, duration: 0.35, ease: 'power2.out' });
        }
      }

      clearCardError();
      setTimeout(() => {
        document.getElementById('cardfield-exp-input')?.focus();
      }, 50);
    }

    function expandCardNumber() {
      cardState.isCollapsed = false;
      renderCardMirror();

      const editBtn = document.getElementById('cardfield-edit-btn');
      const extra = document.getElementById('cardfield-extra');
      const numInput = document.getElementById('cardfield-number-input');

      if (editBtn) editBtn.classList.add('hidden');
      if (numInput) numInput.removeAttribute('tabindex');

      if (extra) {
        if (typeof gsap !== 'undefined') {
          gsap.to(extra, { opacity: 0, x: 12, duration: 0.15, onComplete: () => extra.classList.add('hidden') });
        } else {
          extra.classList.add('hidden');
        }
      }

      if (numInput) {
        numInput.focus();
        numInput.setSelectionRange(numInput.value.length, numInput.value.length);
      }
    }

    function handleNumberInput(e) {
      let raw = e.target.value.replace(/\D/g, '');
      const spec = getCardSpec(raw);
      const maxLen = getCardLength(spec);
      raw = raw.slice(0, maxLen);
      cardState.number = raw;

      const groups = getCardGroups(raw, spec);
      e.target.value = groups.join(' ');

      renderCardBrand(false);
      renderCardMirror();

      if (raw.length === maxLen) {
        if (checkLuhn(raw)) {
          clearCardError();
          collapseCardNumber();
        } else {
          showCardError('Номер карты не прошёл проверку алгоритма (Luhn)');
        }
      } else {
        clearCardError();
      }
    }

    function handleExpiryInput(e) {
      let raw = e.target.value.replace(/\D/g, '').slice(0, 4);
      if (raw.length === 1 && Number(raw) > 1) {
        raw = '0' + raw;
      }
      cardState.expiry = raw;

      let formatted = raw;
      if (raw.length <= 2) {
        formatted = raw.length === 2 ? raw + ' / ' : raw;
      } else {
        formatted = raw.slice(0, 2) + ' / ' + raw.slice(2, 4);
      }
      e.target.value = formatted;

      if (raw.length === 4) {
        const m = Number(raw.slice(0, 2));
        const y = 2000 + Number(raw.slice(2, 4));
        const now = new Date();
        const currentMonths = now.getFullYear() * 12 + now.getMonth();
        if (m < 1 || m > 12) {
          showCardError('Такого месяца не существует (01–12)');
          return;
        }
        if (y * 12 + m - 1 < currentMonths) {
          showCardError('Срок действия карты истёк');
          return;
        }
        clearCardError();
        document.getElementById('cardfield-cvc-input')?.focus();
      } else {
        clearCardError();
      }
    }

    function handleExpiryKeyDown(e) {
      const atStart = e.target.selectionStart === 0 && e.target.selectionEnd === 0;
      if ((e.key === 'Backspace' && e.target.value.length === 0) || (e.key === 'ArrowLeft' && atStart)) {
        e.preventDefault();
        expandCardNumber();
      }
    }

    function handleCvcInput(e) {
      const spec = getCardSpec(cardState.number);
      let raw = e.target.value.replace(/\D/g, '').slice(0, spec.cvc);
      e.target.value = raw;
      cardState.cvc = raw;
    }

    function handleCvcFocus() {
      const spec = getCardSpec(cardState.number);
      renderCardBrand(true);
      const hintText = document.getElementById('cardfield-hint-text');
      if (hintText && !document.getElementById('cardfield-row').classList.contains('has-error')) {
        hintText.textContent = spec.brand === 'amex'
          ? '4 цифры на лицевой стороне карты'
          : '3 цифры на обороте карты';
      }
    }

    function handleCvcBlur() {
      renderCardBrand(false);
      const hintText = document.getElementById('cardfield-hint-text');
      if (hintText && !document.getElementById('cardfield-row').classList.contains('has-error')) {
        hintText.textContent = 'Сквозное 256-bit SSL шифрование (PCI DSS)';
      }
    }

    function handleCvcKeyDown(e) {
      if (e.key === 'Backspace' && e.target.value.length === 0) {
        e.preventDefault();
        document.getElementById('cardfield-exp-input')?.focus();
      }
      if (e.key === 'Enter') {
        const spec = getCardSpec(cardState.number);
        if (cardState.number.length === getCardLength(spec) && cardState.expiry.length === 4 && cardState.cvc.length === spec.cvc) {
          document.getElementById('btn-submit-order')?.click();
        }
      }
    }

    function fillTestCard() {
      const TEST_NUM = '4242424242424242';
      expandCardNumber();
      cardState.number = '';
      cardState.expiry = '';
      cardState.cvc = '';

      const numInput = document.getElementById('cardfield-number-input');
      const expInput = document.getElementById('cardfield-exp-input');
      const cvcInput = document.getElementById('cardfield-cvc-input');

      if (expInput) expInput.value = '';
      if (cvcInput) cvcInput.value = '';

      let i = 0;
      function typeNum() {
        if (i < TEST_NUM.length) {
          i++;
          const cur = TEST_NUM.slice(0, i);
          if (numInput) {
            numInput.value = cur;
            handleNumberInput({ target: numInput });
          }
          setTimeout(typeNum, 35);
        } else {
          setTimeout(typeExp, 220);
        }
      }

      function typeExp() {
        const year = String((new Date().getFullYear() + 3) % 100).padStart(2, '0');
        const expDigits = '12' + year;
        let j = 0;
        function stepExp() {
          if (j < expDigits.length) {
            j++;
            const cur = expDigits.slice(0, j);
            if (expInput) {
              expInput.value = cur;
              handleExpiryInput({ target: expInput });
            }
            setTimeout(stepExp, 40);
          } else {
            setTimeout(typeCvc, 180);
          }
        }
        stepExp();
      }

      function typeCvc() {
        if (cvcInput) cvcInput.focus();
        let k = 0;
        const cvcDigits = '123';
        function stepCvc() {
          if (k < cvcDigits.length) {
            k++;
            if (cvcInput) {
              cvcInput.value = cvcDigits.slice(0, k);
              handleCvcInput({ target: cvcInput });
            }
            setTimeout(stepCvc, 40);
          } else {
            if (cvcInput) cvcInput.blur();
          }
        }
        stepCvc();
      }

      typeNum();
    }

    function initCardFieldListeners() {
      const numInput = document.getElementById('cardfield-number-input');
      const expInput = document.getElementById('cardfield-exp-input');
      const cvcInput = document.getElementById('cardfield-cvc-input');

      if (numInput && !numInput.dataset.bound) {
        numInput.dataset.bound = 'true';
        numInput.addEventListener('input', handleNumberInput);
        numInput.addEventListener('focus', () => {
          cardState.isFocused = true;
          renderCardMirror();
        });
        numInput.addEventListener('blur', () => {
          cardState.isFocused = false;
          renderCardMirror();
        });
        numInput.addEventListener('keydown', (e) => {
          if (e.key === 'Tab' && !e.shiftKey && cardState.isCollapsed) {
            e.preventDefault();
            document.getElementById('cardfield-exp-input')?.focus();
          }
        });
      }

      if (expInput && !expInput.dataset.bound) {
        expInput.dataset.bound = 'true';
        expInput.addEventListener('input', handleExpiryInput);
        expInput.addEventListener('keydown', handleExpiryKeyDown);
      }

      if (cvcInput && !cvcInput.dataset.bound) {
        cvcInput.dataset.bound = 'true';
        cvcInput.addEventListener('input', handleCvcInput);
        cvcInput.addEventListener('focus', handleCvcFocus);
        cvcInput.addEventListener('blur', handleCvcBlur);
        cvcInput.addEventListener('keydown', handleCvcKeyDown);
      }

      renderCardBrand(false);
      renderCardMirror();
    }

    function handlePaymentMethodChange(method) {
      const container = document.getElementById('cardfield-container');
      if (container) container.classList.toggle('hidden', method !== 'CardOnline');
    }

    // -------------------------------------------------------------------------
    // 16. Order Submission
    // -------------------------------------------------------------------------
    async function submitOrder(e) {
      e.preventDefault();
      if (cart.length === 0) {
        showToast('Добавьте хотя бы одну пиццу в корзину перед оформлением.', 'error');
        return;
      }

      const paymentMethod = document.getElementById('cust-payment').value;
      const submitBtn = document.getElementById('btn-submit-order');
      const submitText = document.getElementById('btn-submit-text');

      if (paymentMethod === 'CardOnline') {
        submitBtn.disabled = true;
        submitText.innerHTML = `<span class="inline-block animate-spin mr-1">⟳</span> 3-D Secure авторизация...`;
        await new Promise(r => setTimeout(r, 600));
        submitText.innerHTML = `✓ Оплачено`;
        submitBtn.classList.replace('bg-brand-700', 'bg-bonus');
        await new Promise(r => setTimeout(r, 400));
      }

      const payload = {
        customerName: document.getElementById('cust-name').value,
        customerPhone: document.getElementById('cust-phone').value,
        customerEmail: document.getElementById('cust-email').value,
        deliveryAddress: document.getElementById('cust-address').value,
        gdprConsentAccepted: document.getElementById('gdpr-consent').checked,
        marketingOptIn: document.getElementById('marketing-consent').checked,
        paymentMethod: paymentMethod,
        customerComment: document.getElementById('cust-comment').value + (activePromo ? ` [Промокод: ${activePromo.code}]` : ''),
        items: cart,
        userId: currentUser ? currentUser.id : null,
        bonusToSpend: currentUser ? bonusToSpend : 0.00
      };

      try {
        const res = await fetch('/api/orders', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        const data = await res.json();
        if (!res.ok) {
          showToast(data.error || 'Не удалось оформить заказ', 'error');
          resetSubmitButton();
          return;
        }

        cart = [];
        bonusToSpend = 0.00;
        activePromo = null;
        document.getElementById('checkout-form').reset();
        trackedOrderNumber = data.orderNumber;
        closeCartDrawer();
        await loadAllData();
        if (currentUser) await refreshUserProfile();
        showToast(`Заказ ${data.orderNumber} оформлен! Начислено бонусов: €${data.bonusEarnedEur.toFixed(2)}`);
        switchView('track');
      } catch (err) {
        showToast('Ошибка связи с сервером при отправке заказа', 'error');
      } finally {
        resetSubmitButton();
      }
    }

    function resetSubmitButton() {
      const submitBtn = document.getElementById('btn-submit-order');
      const submitText = document.getElementById('btn-submit-text');
      if (submitBtn && submitText) {
        submitBtn.disabled = false;
        submitText.textContent = 'Оформить заказ';
        submitBtn.classList.remove('bg-bonus');
        submitBtn.classList.add('bg-brand-700');
      }
    }

    // -------------------------------------------------------------------------
    // 17. Tracking View with 5-Step Stepper & Star Rating
    // -------------------------------------------------------------------------
    function searchTrackedOrder() {
      const val = document.getElementById('track-search-input').value.trim();
      if (val) {
        trackedOrderNumber = val.toUpperCase();
        renderTracking();
      }
    }

    function renderTracking() {
      const pills = document.getElementById('quick-order-pills');
      if (orders.length > 0) {
        pills.innerHTML = `<span class="text-textSecondary">Заказы в БД:</span>` + orders.slice(0, 6).map(o =>
          `<button type="button" onclick="trackedOrderNumber='${o.orderNumber}'; renderTracking();"
            class="font-mono px-2.5 py-1 rounded-lg border text-xs transition ${
              o.orderNumber === trackedOrderNumber ? 'bg-textPrimary text-canvas border-textPrimary' : 'bg-elevated text-textPrimary border-borderSubtle hover:border-textSecondary'
            }">${o.orderNumber}</button>`
        ).join('');
      }

      const order = orders.find(o => o.orderNumber.toUpperCase() === trackedOrderNumber.toUpperCase());
      const card = document.getElementById('tracked-order-card');

      if (!order) {
        card.innerHTML = `<p class="text-sm text-textSecondary">Заказ <span class="font-mono font-bold text-textPrimary">${trackedOrderNumber}</span> не найден в базе данных.</p>`;
        return;
      }

      const meta = STATUS_META[order.status] || STATUS_META.New;
      const steps = [
        { key: 'New', title: 'Принят' },
        { key: 'Preparing', title: 'Подготовка' },
        { key: 'Baking', title: 'В печи 430°C' },
        { key: 'OutForDelivery', title: 'У курьера' },
        { key: 'Delivered', title: 'Доставлен' }
      ];

      const stepperHtml = steps.map((s, idx) => {
        const stepNum = idx + 1;
        const done = meta.step >= stepNum;
        const isActive = meta.step === stepNum;
        return `
          <div class="flex-1 flex flex-col items-center text-center">
            <div class="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold border transition ${
              done ? 'bg-brand-700 text-white border-brand-700 shadow-sm' : 'bg-elevated text-textSecondary border-borderSubtle'
            } ${isActive ? 'stepper-active-circle ring-2 ring-brand-700/40 ring-offset-2' : ''}">${stepNum}</div>
            <span class="text-[11px] sm:text-xs mt-1.5 font-medium ${done ? 'text-textPrimary font-bold' : 'text-textSecondary'}">${s.title}</span>
          </div>
        `;
      }).join('');

      const itemsHtml = order.items.map(i => `
        <div class="flex justify-between text-xs py-1.5 border-b border-borderSubtle last:border-0">
          <span><strong>${i.quantity}×</strong> ${i.pizzaName} (${i.sizeLabel})</span>
          <span class="font-mono font-semibold">€${i.lineTotalEur.toFixed(2)}</span>
        </div>
      `).join('');

      const historyHtml = order.history.map(h => `
        <div class="flex items-start justify-between gap-3 text-xs py-2 border-l-2 border-borderSubtle pl-3">
          <div>
            <p class="font-semibold text-textPrimary">${h.note}</p>
            <p class="text-[11px] text-textSecondary">Роль: ${h.changedByRole}</p>
          </div>
          <span class="font-mono text-[11px] text-textSecondary shrink-0">${h.changedAtUtc.replace('T', ' ').replace('Z', ' UTC')}</span>
        </div>
      `).join('');

      const isDelivered = order.status === 'Delivered';
      const ratingHtml = isDelivered ? `
        <div id="order-rating-box" class="p-5 rounded-2xl bg-elevated border border-borderSubtle space-y-3 shadow-xs">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-borderSubtle pb-2.5">
            <div>
              <h4 class="text-xs font-bold text-textPrimary uppercase tracking-wider font-mono">Оцените пиццу и доставку</h4>
              <p class="text-[11px] text-textSecondary">Ваш отзыв помогает пиццайоло и курьерам совершенствовать сервис</p>
            </div>
            <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-surface border border-borderSubtle text-textSecondary">DesignBookmark Spring</span>
          </div>
          <div id="track-star-rating-slot" class="flex justify-center py-1"></div>
          <div id="rating-feedback-form" class="space-y-2 pt-1">
            <input id="rating-comment" type="text" placeholder="Что вам особенно понравилось? (хруст бортика, соус San Marzano, пунктуальность курьера)"
              class="w-full px-3.5 py-2 text-xs bg-canvas border border-borderSubtle rounded-xl text-textPrimary focus:ring-1 focus:ring-brand-700" />
            <button type="button" onclick="submitRatingFeedback()"
              class="px-4 py-2 bg-brand-700 hover:bg-brand-800 text-white font-semibold text-xs rounded-xl transition shadow-sm active:scale-97">
              Отправить отзыв
            </button>
          </div>
        </div>
      ` : '';

      card.innerHTML = `
        <div class="space-y-6">
          <div class="flex flex-wrap items-start justify-between gap-4 border-b border-borderSubtle pb-4">
            <div>
              <div class="flex items-center gap-2.5">
                <h3 class="font-mono text-xl font-bold text-textPrimary">${order.orderNumber}</h3>
                <span class="px-2.5 py-0.5 rounded-full text-xs font-semibold border ${meta.cls}">${meta.label}</span>
              </div>
              <p class="text-xs text-textSecondary mt-1">Получатель: ${order.customerName} · ${order.deliveryAddress}</p>
            </div>
            <div class="text-right">
              <span class="text-xs text-textSecondary block">Итого с НДС</span>
              <span class="font-mono text-2xl font-bold text-textPrimary">€${order.totalEur.toFixed(2)}</span>
              ${order.bonusSpentEur > 0 ? `<span class="text-[11px] text-bonus font-mono block">Оплачено бонусами: €${order.bonusSpentEur.toFixed(2)}</span>` : ''}
            </div>
          </div>

          <div class="flex items-center justify-between gap-2 bg-elevated p-4 rounded-xl border border-borderSubtle">
            ${stepperHtml}
          </div>

          ${ratingHtml}

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 class="text-xs font-bold text-textPrimary mb-2 uppercase tracking-wider font-mono">Детализация чека (EU VAT 10%)</h4>
              <div class="bg-elevated rounded-xl p-4 border border-borderSubtle space-y-1.5">
                ${itemsHtml}
                <div class="pt-2 border-t border-borderSubtle flex justify-between text-xs text-textSecondary">
                  <span>В т.ч. НДС (10%): €${order.vatAmountEur.toFixed(2)}</span>
                  <span>Доставка: €${order.deliveryFeeEur.toFixed(2)}</span>
                </div>
              </div>
            </div>
            <div>
              <h4 class="text-xs font-bold text-textPrimary mb-2 uppercase tracking-wider font-mono">Журнал событий (Audit Log)</h4>
              <div class="space-y-2">${historyHtml}</div>
            </div>
          </div>
        </div>
      `;

      if (isDelivered) {
        setTimeout(() => {
          const trackSlot = document.getElementById('track-star-rating-slot');
          if (trackSlot) {
            window.trackStarRatingInstance = initStarRatingComponent(trackSlot, {
              initialRating: 5,
              onChange: (st) => {
                window.lastTrackingRating = st;
              }
            });
          }
        }, 20);
      }
    }

    let lastTrackingRating = 5;
    function submitRatingFeedback() {
      const box = document.getElementById('order-rating-box');
      const rating = window.trackStarRatingInstance ? window.trackStarRatingInstance.getRating() : 5;
      if (box) {
        box.innerHTML = `<div class="p-5 text-center text-xs font-semibold text-bonus bg-surface rounded-xl border border-borderSubtle space-y-2 shadow-xs">
          <div class="flex justify-center">${renderStarRatingSvgDisplay(rating)}</div>
          <p class="text-textPrimary text-sm font-serif font-bold">Спасибо за оценку ${rating} из 5!</p>
          <p class="text-textSecondary text-[11px] font-normal">Ваш отзыв сохранён и передан шеф-пиццайоло и управляющему доставкой.</p>
        </div>`;
      }
      showToast(`Спасибо за оценку ${rating}/5!`);
    }

    // -------------------------------------------------------------------------
    // 18. EU VAT Receipt Printing
    // -------------------------------------------------------------------------
    function printReceipt() {
      const order = orders.find(o => o.orderNumber.toUpperCase() === trackedOrderNumber.toUpperCase());
      if (!order) {
        showToast('Заказ для печати не найден', 'error');
        return;
      }

      const sheet = document.getElementById('print-receipt-sheet');
      sheet.innerHTML = `
        <div style="max-width: 650px; margin: 0 auto; font-family: monospace; font-size: 13px; line-height: 1.5;">
          <div style="text-align: center; border-bottom: 2px dashed #000; padding-bottom: 12px; margin-bottom: 14px;">
            <h1 style="font-size: 20px; font-weight: 900; margin: 0;">CROSTA ARTISANAL PIZZA EUROPE</h1>
            <p style="margin: 3px 0;">Neapolitan Craft Bakery & Food-Tech</p>
            <p style="margin: 3px 0;">EU VAT ID: IT 849204820 · REA: RM-149204</p>
            <p style="margin: 3px 0;">Via Partenope 24, Napoli / Delivery Hub EU</p>
          </div>

          <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
            <div>
              <strong>ФИСКАЛЬНЫЙ ЧЕК / FISCAL RECEIPT:</strong><br/>
              Номер заказа: ${order.orderNumber}<br/>
              Дата/Время: ${order.createdAtUtc.replace('T', ' ').slice(0, 19)} UTC
            </div>
            <div style="text-align: right;">
              Клиент: ${order.customerName}<br/>
              Тел: ${order.customerPhone}<br/>
              Адрес: ${order.deliveryAddress}
            </div>
          </div>

          <table style="width: 100%; border-collapse: collapse; margin-bottom: 12px;">
            <thead>
              <tr style="border-bottom: 1px solid #000; text-align: left;">
                <th style="padding: 4px 0;">Позиция</th>
                <th style="padding: 4px 0; text-align: center;">Кол-во</th>
                <th style="padding: 4px 0; text-align: right;">Цена EUR</th>
                <th style="padding: 4px 0; text-align: right;">Сумма EUR</th>
              </tr>
            </thead>
            <tbody>
              ${order.items.map(i => `
                <tr style="border-bottom: 1px dotted #ccc;">
                  <td style="padding: 5px 0;">${i.pizzaName} (${i.sizeLabel})</td>
                  <td style="padding: 5px 0; text-align: center;">${i.quantity}</td>
                  <td style="padding: 5px 0; text-align: right;">€${i.unitPriceEur.toFixed(2)}</td>
                  <td style="padding: 5px 0; text-align: right;">€${i.lineTotalEur.toFixed(2)}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>

          <div style="border-top: 1px solid #000; padding-top: 8px; margin-bottom: 16px;">
            <div style="display: flex; justify-content: space-between;">
              <span>Сумма без налога (Netto):</span>
              <span>€${order.netAmountEur.toFixed(2)}</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
              <span>НДС ЕС / EU VAT (10%):</span>
              <span>€${order.vatAmountEur.toFixed(2)}</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
              <span>Курьерская доставка:</span>
              <span>€${order.deliveryFeeEur.toFixed(2)}</span>
            </div>
            ${order.bonusSpentEur > 0 ? `
              <div style="display: flex; justify-content: space-between; font-weight: bold;">
                <span>Списание бонусов:</span>
                <span>-€${order.bonusSpentEur.toFixed(2)}</span>
              </div>
            ` : ''}
            <div style="display: flex; justify-content: space-between; font-size: 16px; font-weight: 900; border-top: 2px solid #000; margin-top: 6px; padding-top: 6px;">
              <span>ИТОГО К ОПЛАТЕ:</span>
              <span>€${order.totalEur.toFixed(2)}</span>
            </div>
          </div>

          <div style="text-align: center; border-top: 2px dashed #000; padding-top: 12px; font-size: 11px;">
            <p>Способ оплаты: ${order.paymentMethod}</p>
            <p>Согласие GDPR: Зафиксировано (Art. 6.1.b EU 2016/679)</p>
            <p>Спасибо, что выбираете ремесленную неаполитанскую пиццу CROSTA!</p>
          </div>
        </div>
      `;

      window.print();
    }

    // -------------------------------------------------------------------------
    // 19. Profile & Loyalty Cabinet
    // -------------------------------------------------------------------------
    async function refreshUserProfile() {
      if (!currentUser) return;
      try {
        const res = await fetch(`/api/profile/${currentUser.id}`);
        if (res.ok) {
          userProfileDetails = await res.json();
          currentUser = userProfileDetails.user;
          localStorage.setItem('crosta_user', JSON.stringify(currentUser));
          updateHeaderAuth();
        }
      } catch (err) {
        console.error('Error refreshing profile:', err);
      }
    }

    function renderProfileView() {
      const guestCard = document.getElementById('profile-guest-card');
      const userContent = document.getElementById('profile-user-content');
      if (!guestCard || !userContent) return;

      if (!currentUser) {
        guestCard.classList.remove('hidden');
        userContent.classList.add('hidden');
        return;
      }

      guestCard.classList.add('hidden');
      userContent.classList.remove('hidden');

      document.getElementById('profile-bonus-balance').textContent = `€${currentUser.bonusBalance.toFixed(2)}`;
      document.getElementById('profile-full-name').textContent = currentUser.fullName;
      document.getElementById('profile-email').textContent = currentUser.email;
      document.getElementById('profile-role-badge').textContent = currentUser.role;
      document.getElementById('profile-phone').textContent = currentUser.phone;
      document.getElementById('profile-address').textContent = currentUser.defaultAddress;

      document.getElementById('edit-name').value = currentUser.fullName;
      document.getElementById('edit-phone').value = currentUser.phone;
      document.getElementById('edit-addr').value = currentUser.defaultAddress;

      const bTbody = document.getElementById('profile-bonus-tbody');
      const bList = userProfileDetails?.bonusHistory || [];
      if (bList.length === 0) {
        bTbody.innerHTML = `<tr><td colspan="5" class="py-6 text-center text-textSecondary">История бонусных операций пока пуста</td></tr>`;
      } else {
        bTbody.innerHTML = bList.map(b => {
          const isPos = b.deltaAmount > 0;
          return `
            <tr class="border-b border-borderSubtle hover:bg-elevated transition">
              <td class="py-2.5 px-3 font-mono text-textSecondary">${b.createdAtUtc.replace('T', ' ').slice(0, 16)}</td>
              <td class="py-2.5 px-3 font-semibold">${b.type}</td>
              <td class="py-2.5 px-3 font-mono">${b.orderNumber || '—'}</td>
              <td class="py-2.5 px-3 text-textSecondary">${b.description}</td>
              <td class="py-2.5 px-3 text-right font-mono font-bold ${isPos ? 'text-bonus' : 'text-brand-700'}">
                ${isPos ? '+' : ''}€${b.deltaAmount.toFixed(2)}
              </td>
            </tr>
          `;
        }).join('');
      }

      const pOrders = userProfileDetails?.orders || [];
      const ordersList = document.getElementById('profile-orders-list');
      if (pOrders.length === 0) {
        ordersList.innerHTML = `<div class="py-6 text-center text-textSecondary">Вы ещё не делали заказов</div>`;
      } else {
        ordersList.innerHTML = pOrders.map(o => {
          const itemsText = o.items.map(i => `${i.quantity}× ${i.pizzaName} (${i.sizeCode})`).join(', ');
          const itemsPayload = JSON.stringify(o.items.map(i => ({ pizzaId: i.pizzaId, sizeId: i.sizeId, quantity: i.quantity })));
          return `
            <div class="p-4 rounded-xl bg-elevated border border-borderSubtle flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <div class="flex items-center gap-2">
                  <span class="font-mono font-bold text-textPrimary">${o.orderNumber}</span>
                  <span class="text-xs text-textSecondary font-mono">${o.createdAtUtc.slice(0, 10)}</span>
                  <span class="px-2 py-0.2 rounded-full text-[10px] font-semibold border ${STATUS_META[o.status]?.cls || ''}">
                    ${STATUS_META[o.status]?.label || o.status}
                  </span>
                </div>
                <p class="text-xs text-textSecondary mt-1">${itemsText}</p>
                <p class="text-xs font-mono font-bold text-textPrimary mt-0.5">Итого: €${o.totalEur.toFixed(2)}</p>
              </div>
              <div class="flex items-center gap-2 shrink-0">
                <button type="button" onclick="trackedOrderNumber='${o.orderNumber}'; switchView('track');"
                  class="px-3 py-1.5 text-xs bg-surface border border-borderSubtle hover:border-textSecondary rounded-lg font-medium transition">
                  Трекинг
                </button>
                <button type="button" onclick='repeatOrder(${itemsPayload})'
                  class="px-3 py-1.5 text-xs bg-brand-700 hover:bg-brand-800 text-white font-semibold rounded-lg transition shadow-sm active:scale-97">
                  Повторить заказ ⟲
                </button>
              </div>
            </div>
          `;
        }).join('');
      }
    }

    function repeatOrder(items) {
      if (!items || items.length === 0) return;
      cart = items;
      renderCart();
      openCartDrawer();
      showToast('Позиции скопированы в корзину! Проверьте адрес и оформите заказ.');
    }

    // -------------------------------------------------------------------------
    // 20. Staff & Admin Dashboard with Bezier Chart & Stop-List
    // -------------------------------------------------------------------------
    async function renderStaffDashboard() {
      const role = document.getElementById('staff-role-select').value;
      const isAdmin = currentUser && currentUser.role === 'Admin';
      
      const newPizzaBtn = document.getElementById('btn-open-new-pizza');
      if (newPizzaBtn) newPizzaBtn.classList.toggle('hidden', role !== 'Manager');

      try {
        const statsRes = await fetch('/api/admin/stats');
        if (statsRes.ok) {
          const stats = await statsRes.json();
          renderAdminStatsCards(stats);
          renderTopPizzas(stats.topPizzas);
          renderStatusDistribution(stats.ordersByStatus);
          updateRevenueChart(stats);
        }
      } catch (err) {
        console.error('Error loading admin stats:', err);
      }

      renderStopList();

      const filtered = currentStaffFilter === 'All'
        ? orders
        : orders.filter(o => o.status === currentStaffFilter);

      const tbody = document.getElementById('staff-orders-tbody');
      if (filtered.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" class="py-8 text-center text-xs text-textSecondary">Заказов с выбранным статусом нет</td></tr>`;
        return;
      }

      tbody.innerHTML = filtered.map(o => {
        const meta = STATUS_META[o.status] || STATUS_META.New;
        const transition = NEXT_STEP[o.status];
        const canAct = transition && transition.roles.includes(role);
        const itemsSummary = o.items.map(i => `${i.quantity}× ${i.pizzaName} (${i.sizeCode})`).join(', ');

        let actionHtml = `<span class="text-xs text-textSecondary">Ожидает этапа</span>`;
        if (o.status === 'Delivered' || o.status === 'Cancelled') {
          actionHtml = `<span class="text-xs font-medium text-textSecondary">Завершён</span>`;
        } else if (canAct) {
          actionHtml = `
            <div class="inline-flex items-center gap-1.5">
              <button type="button" onclick="advanceOrderStatus(${o.id}, '${transition.next}')"
                class="px-3 py-1.5 bg-textPrimary hover:opacity-90 text-canvas text-xs font-semibold rounded-lg transition shadow-sm active:scale-97">
                ${transition.label}
              </button>
              ${role === 'Manager' ? `<button type="button" onclick="openCancelModal(${o.id}, '${o.orderNumber}')"
                class="px-2.5 py-1.5 bg-red-100 hover:bg-red-200 text-brand-700 text-xs font-semibold rounded-lg transition">
                Отмена
              </button>` : ''}
            </div>
          `;
        }

        return `
          <tr class="hover:bg-elevated transition">
            <td class="py-3 px-4 align-top">
              <span class="font-mono text-xs font-bold text-textPrimary block">${o.orderNumber}</span>
              <span class="font-mono text-[11px] text-textSecondary">${o.createdAtUtc.slice(11, 16)} UTC</span>
            </td>
            <td class="py-3 px-4 align-top">
              <p class="text-xs font-bold text-textPrimary">${o.customerName}</p>
              <p class="text-xs text-textSecondary">${o.deliveryAddress}</p>
              <p class="font-mono text-[11px] text-textSecondary">${o.customerPhone}</p>
            </td>
            <td class="py-3 px-4 align-top max-w-xs">
              <p class="text-xs text-textPrimary font-medium">${itemsSummary}</p>
              ${o.customerComment ? `<p class="text-[11px] text-amber-800 bg-amber-100 px-2 py-0.5 rounded mt-1 inline-block">Примечание: ${o.customerComment}</p>` : ''}
            </td>
            <td class="py-3 px-4 align-top font-mono text-xs font-bold text-textPrimary">
              €${o.totalEur.toFixed(2)}
            </td>
            <td class="py-3 px-4 align-top">
              <span class="inline-flex px-2.5 py-0.5 rounded-full text-xs font-semibold border ${meta.cls}">
                ${meta.label}
              </span>
            </td>
            <td class="py-3 px-4 align-top text-right">
              ${actionHtml}
            </td>
          </tr>
        `;
      }).join('');
    }

    function renderAdminStatsCards(stats) {
      document.getElementById('staff-kpis').innerHTML = `
        <div class="bg-surface border border-borderSubtle rounded-2xl p-4 transition-colors">
          <span class="text-xs text-textSecondary">Выручка брутто (с НДС)</span>
          <p id="admin-kpi-gross" class="font-mono text-2xl font-extrabold text-brand-700 mt-1">€${stats.grossRevenueEur.toFixed(2)}</p>
          <span class="text-[10px] text-textSecondary font-mono block mt-0.5">Всего заказов: ${stats.totalOrders}</span>
        </div>
        <div class="bg-surface border border-borderSubtle rounded-2xl p-4 transition-colors">
          <span class="text-xs text-textSecondary">Выручка нетто (Netto)</span>
          <p class="font-mono text-2xl font-extrabold text-textPrimary mt-1">€${stats.netRevenueEur.toFixed(2)}</p>
          <span class="text-[10px] text-textSecondary font-mono block mt-0.5">НДС 10%: €${stats.vatTotalEur.toFixed(2)}</span>
        </div>
        <div class="bg-surface border border-borderSubtle rounded-2xl p-4 transition-colors">
          <span class="text-xs text-textSecondary">Средний чек заказа</span>
          <p class="font-mono text-2xl font-extrabold text-textPrimary mt-1">€${stats.averageOrderValueEur.toFixed(2)}</p>
          <span class="text-[10px] text-textSecondary font-mono block mt-0.5">В работе: ${stats.activeOrders}</span>
        </div>
        <div class="bg-surface border border-borderSubtle rounded-2xl p-4 transition-colors">
          <span class="text-xs text-textSecondary">Бонусы: выдано / списано</span>
          <p class="font-mono text-xl font-extrabold text-bonus mt-1">+€${stats.totalBonusIssued.toFixed(2)}</p>
          <span class="text-[10px] text-brand-700 font-mono block mt-0.5">Списано: -€${stats.totalBonusRedeemed.toFixed(2)}</span>
        </div>
      `;
    }

    function updateRevenueChart(stats) {
      const curve = document.getElementById('chart-curve');
      const area = document.getElementById('chart-area');
      const dot = document.getElementById('chart-dot');
      if (!curve || !area) return;

      const p1 = currentChartPeriod === 'day' ? 70 : currentChartPeriod === 'week' ? 50 : 80;
      const p2 = currentChartPeriod === 'day' ? 30 : currentChartPeriod === 'week' ? 20 : 40;
      const p3 = currentChartPeriod === 'day' ? 45 : currentChartPeriod === 'week' ? 35 : 25;

      const curveD = `M 0 ${p1} Q 200 ${p2} 450 ${p3} T 700 ${p2}`;
      const areaD = `M 0 ${p1} Q 200 ${p2} 450 ${p3} T 700 ${p2} L 700 120 L 0 120 Z`;

      curve.setAttribute('d', curveD);
      area.setAttribute('d', areaD);
      if (dot) {
        dot.setAttribute('cx', '700');
        dot.setAttribute('cy', `${p2}`);
      }
    }

    function setChartPeriod(period) {
      currentChartPeriod = period;
      ['day', 'week', 'month'].forEach(p => {
        const btn = document.getElementById(`chart-btn-${p}`);
        if (btn) {
          btn.className = p === period
            ? 'px-2.5 py-1 rounded-md font-semibold bg-surface text-textPrimary shadow-xs transition'
            : 'px-2.5 py-1 rounded-md font-medium text-textSecondary hover:text-textPrimary transition';
        }
      });
      updateRevenueChart();
    }

    function renderTopPizzas(topPizzas) {
      const container = document.getElementById('admin-top-pizzas');
      if (!topPizzas || topPizzas.length === 0) {
        container.innerHTML = `<p class="text-xs text-textSecondary">Статистика продаж собирается...</p>`;
        return;
      }
      const maxUnits = Math.max(...topPizzas.map(p => p.unitsSold), 1);
      container.innerHTML = topPizzas.map(p => {
        const pct = Math.round((p.unitsSold / maxUnits) * 100);
        return `
          <div class="space-y-1">
            <div class="flex justify-between text-xs font-semibold">
              <span class="text-textPrimary">${p.pizzaName}</span>
              <span class="font-mono text-textSecondary">${p.unitsSold} шт · €${p.revenueEur.toFixed(2)}</span>
            </div>
            <div class="w-full bg-elevated rounded-full h-2 overflow-hidden border border-borderSubtle">
              <div class="bg-brand-700 h-2 rounded-full transition-all duration-500" style="width: ${pct}%"></div>
            </div>
          </div>
        `;
      }).join('');
    }

    function renderStatusDistribution(ordersByStatus) {
      const container = document.getElementById('admin-status-distribution');
      if (!ordersByStatus || ordersByStatus.length === 0) {
        container.innerHTML = `<p class="text-xs text-textSecondary col-span-2">Нет данных</p>`;
        return;
      }
      container.innerHTML = ordersByStatus.map(st => {
        const meta = STATUS_META[st.status] || { label: st.status, cls: 'status-badge-New' };
        return `
          <div class="p-3 rounded-xl border border-borderSubtle bg-elevated flex items-center justify-between">
            <span class="text-xs font-medium text-textPrimary">${meta.label}</span>
            <span class="font-mono text-sm font-bold text-textPrimary px-2 py-0.5 rounded-lg bg-surface border border-borderSubtle">${st.count}</span>
          </div>
        `;
      }).join('');
    }

    function renderStopList() {
      const container = document.getElementById('admin-stop-list');
      if (!allPizzasAdmin || allPizzasAdmin.length === 0) return;
      container.innerHTML = allPizzasAdmin.map(p => `
        <div class="p-3 rounded-xl border border-borderSubtle bg-elevated flex items-center justify-between gap-2">
          <div class="min-w-0">
            <p class="text-xs font-bold text-textPrimary truncate">${p.name}</p>
            <span class="font-mono text-[10px] text-textSecondary">${p.sku} · €${p.basePriceEur.toFixed(2)}</span>
          </div>
          <button type="button" onclick="toggleAvailability(${p.id}, ${!p.isAvailable})"
            class="px-2.5 py-1 text-xs font-semibold rounded-lg border transition shrink-0 ${
              p.isAvailable 
                ? 'bg-emerald-100 text-emerald-800 border-emerald-300 hover:bg-red-100 hover:text-brand-700' 
                : 'bg-red-100 text-brand-700 border-red-300 hover:bg-emerald-100 hover:text-emerald-800'
            }">
            ${p.isAvailable ? 'В наличии' : 'В стоп-листе'}
          </button>
        </div>
      `).join('');
    }

    async function toggleAvailability(id, newAvail) {
      const res = await fetch(`/api/menu/${id}/availability`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newAvail)
      });
      if (res.ok) {
        showToast('Статус доступности позиции обновлён');
        await loadAllData();
      }
    }

    function setStaffFilter(st) {
      currentStaffFilter = st;
      document.querySelectorAll('.st-btn').forEach(btn => {
        const active = btn.dataset.st === st;
        btn.className = active
          ? 'st-btn px-3 py-1.5 rounded-lg text-xs font-semibold bg-textPrimary text-canvas shadow-xs'
          : 'st-btn px-3 py-1.5 rounded-lg text-xs font-medium bg-elevated text-textPrimary hover:border-textSecondary border border-borderSubtle';
      });
      renderStaffDashboard();
    }

    function openCancelModal(orderId, orderNum) {
      pendingCancelOrderId = orderId;
      document.getElementById('cancel-order-num-text').textContent = orderNum;
      document.getElementById('cancel-confirm-modal').classList.remove('hidden');
      document.getElementById('btn-confirm-cancel').onclick = () => confirmOrderCancel();
    }

    function closeCancelModal() {
      pendingCancelOrderId = null;
      document.getElementById('cancel-confirm-modal').classList.add('hidden');
    }

    async function confirmOrderCancel() {
      if (!pendingCancelOrderId) return;
      const orderId = pendingCancelOrderId;
      closeCancelModal();
      await advanceOrderStatus(orderId, 'Cancelled');
    }

    async function advanceOrderStatus(orderId, newStatus) {
      const role = document.getElementById('staff-role-select').value;
      const res = await fetch(`/api/orders/${orderId}/status`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus, changedByRole: role })
      });
      const data = await res.json();
      if (!res.ok) {
        showToast(data.error || 'Ошибка смены статуса', 'error');
        return;
      }
      await loadAllData();
      showToast(`Заказ ${data.orderNumber}: ${STATUS_META[newStatus]?.label || newStatus}`);
    }

    function toggleNewPizzaModal(show) {
      document.getElementById('new-pizza-modal').classList.toggle('hidden', !show);
    }

    async function submitNewPizza(e) {
      e.preventDefault();
      const payload = {
        name: document.getElementById('np-name').value,
        description: document.getElementById('np-desc').value,
        ingredients: document.getElementById('np-ing').value,
        category: document.getElementById('np-cat').value,
        dietaryTag: document.getElementById('np-tag').value,
        basePriceEur: parseFloat(document.getElementById('np-price').value),
        prepMinutes: parseInt(document.getElementById('np-prep').value, 10),
        caloriesKcal: parseInt(document.getElementById('np-kcal').value, 10)
      };

      const res = await fetch('/api/menu', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (!res.ok) {
        showToast('Ошибка добавления пиццы в меню', 'error');
        return;
      }
      toggleNewPizzaModal(false);
      e.target.reset();
      await loadAllData();
      showToast('Новая позиция успешно добавлена в каталог SQLite!');
    }

    // -------------------------------------------------------------------------
    // 21. Authentication & Role-Based Navigation
    // -------------------------------------------------------------------------
    function openAuthModal(tab = 'login') {
      document.getElementById('auth-modal').classList.remove('hidden');
      setAuthTab(tab);
    }

    function closeAuthModal() {
      document.getElementById('auth-modal').classList.add('hidden');
    }

    function setAuthTab(tab) {
      const loginTab = document.getElementById('auth-tab-login');
      const regTab = document.getElementById('auth-tab-register');
      const loginForm = document.getElementById('login-form');
      const regForm = document.getElementById('register-form');

      if (tab === 'login') {
        loginTab.className = 'text-sm font-bold text-brand-700 pb-1 border-b-2 border-brand-700';
        regTab.className = 'text-sm font-medium text-textSecondary hover:text-textPrimary pb-1';
        loginForm.classList.remove('hidden');
        regForm.classList.add('hidden');
      } else {
        regTab.className = 'text-sm font-bold text-brand-700 pb-1 border-b-2 border-brand-700';
        loginTab.className = 'text-sm font-medium text-textSecondary hover:text-textPrimary pb-1';
        regForm.classList.remove('hidden');
        loginForm.classList.add('hidden');
      }
    }

    function updatePasswordStrength(val) {
      let score = 0;
      if (val.length >= 6) score++;
      if (/[A-Z]/.test(val)) score++;
      if (/[0-9]/.test(val)) score++;
      if (/[^A-Za-z0-9]/.test(val)) score++;

      const colors = ['bg-red-500', 'bg-orange-500', 'bg-amber-500', 'bg-emerald-500'];
      const labels = ['Очень слабый', 'Слабый', 'Средний', 'Надёжный', 'Отличный'];
      document.getElementById('pwd-strength-label').textContent = `Сложность: ${labels[score] || '—'}`;

      for (let i = 1; i <= 4; i++) {
        const bar = document.getElementById(`pwd-bar-${i}`);
        if (bar) {
          bar.className = `h-1 rounded-full transition-all duration-200 ${i <= score ? colors[score - 1] : 'bg-borderSubtle'}`;
        }
      }
    }

    function togglePasswordVisibility(id) {
      const input = document.getElementById(id);
      if (!input) return;
      input.type = input.type === 'password' ? 'text' : 'password';
    }

    async function handleLoginSubmit(e) {
      e.preventDefault();
      const email = document.getElementById('login-email').value;
      const pwd = document.getElementById('login-pwd').value;
      await performLogin(email, pwd);
    }

    async function performLogin(email, password) {
      try {
        const res = await fetch('/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });
        const data = await res.json();
        if (!res.ok) {
          showToast(data.error || 'Ошибка входа', 'error');
          return;
        }

        currentUser = data;
        localStorage.setItem('crosta_user', JSON.stringify(currentUser));
        closeAuthModal();
        await refreshUserProfile();
        updateHeaderAuth();
        renderCart();
        showToast(`Вы вошли как ${currentUser.fullName} (${currentUser.role})`);
        
        document.getElementById('cust-name').value = currentUser.fullName;
        document.getElementById('cust-phone').value = currentUser.phone;
        document.getElementById('cust-email').value = currentUser.email;
        document.getElementById('cust-address').value = currentUser.defaultAddress;

        if (currentUser.role === 'Admin') {
          document.getElementById('staff-role-select').value = 'Manager';
          switchView('staff');
        } else {
          switchView('profile');
        }
      } catch (err) {
        showToast('Сетевая ошибка при входе', 'error');
      }
    }

    async function handleRegisterSubmit(e) {
      e.preventDefault();
      const payload = {
        fullName: document.getElementById('reg-name').value,
        email: document.getElementById('reg-email').value,
        phone: document.getElementById('reg-phone').value,
        defaultAddress: document.getElementById('reg-addr').value,
        password: document.getElementById('reg-pwd').value
      };

      try {
        const res = await fetch('/api/auth/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (!res.ok) {
          showToast(data.error || 'Ошибка регистрации', 'error');
          return;
        }

        currentUser = data;
        localStorage.setItem('crosta_user', JSON.stringify(currentUser));
        closeAuthModal();
        await refreshUserProfile();
        updateHeaderAuth();
        renderCart();
        showToast(`Регистрация успешна! Вам начислено €${currentUser.bonusBalance.toFixed(2)} приветственных бонусов.`);
        switchView('profile');
      } catch (err) {
        showToast('Ошибка регистрации на сервере', 'error');
      }
    }

    function logout() {
      currentUser = null;
      userProfileDetails = null;
      bonusToSpend = 0.00;
      localStorage.removeItem('crosta_user');
      updateHeaderAuth();
      renderCart();
      showToast('Вы вышли из учётной записи');
      navigateToCatalog();
    }

    function updateHeaderAuth() {
      // 1. Staff tab visibility: ONLY visible if currentUser.role === 'Admin'
      const staffTab = document.getElementById('tab-staff');
      if (staffTab) {
        const isAdmin = currentUser && currentUser.role === 'Admin';
        staffTab.style.display = isAdmin ? 'inline-flex' : 'none';
      }

      // 2. User area rendering in header
      document.querySelectorAll('.header-user-area-slot').forEach(area => {
        if (!currentUser) {
          area.innerHTML = `
            <button type="button" onclick="openAuthModal('login')" class="px-3.5 py-2 text-xs sm:text-sm font-semibold rounded-xl bg-brand-700 hover:bg-brand-800 text-white transition shadow-sm active:scale-97">
              Войти
            </button>
          `;
        } else {
          const isCustomer = currentUser.role === 'Customer';
          const clickAction = isCustomer ? `switchView('profile')` : `switchView('staff')`;
          const subText = isCustomer ? `€${currentUser.bonusBalance.toFixed(2)}` : currentUser.role;

          area.innerHTML = `
            <div class="flex items-center gap-1.5 sm:gap-2">
              <button type="button" onclick="${clickAction}" class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl bg-elevated border border-borderSubtle hover:border-textSecondary transition text-xs shadow-xs active:scale-97">
                <span class="w-6 h-6 rounded-full bg-brand-700 text-white flex items-center justify-center font-bold text-xs shrink-0">
                  ${currentUser.fullName.charAt(0)}
                </span>
                <span class="font-semibold text-textPrimary hidden sm:inline">${currentUser.fullName.split(' ')[0]}</span>
                <span class="font-mono text-bonus font-bold">${subText}</span>
              </button>
              <button type="button" onclick="logout()" title="Выйти из аккаунта" class="p-1 text-textSecondary hover:text-brand-700 rounded transition text-xs">
                ✕
              </button>
            </div>
          `;
        }
      });

      // Recalculate elastic nav pill
      const currentTab = document.querySelector('nav#header-nav-container button.font-semibold')?.id?.replace('tab-', '') || 'store';
      updateElasticNavPill(currentTab);
    }

    function toggleProfileEditModal(show) {
      document.getElementById('profile-edit-modal').classList.toggle('hidden', !show);
    }

    async function handleProfileUpdateSubmit(e) {
      e.preventDefault();
      if (!currentUser) return;
      const payload = {
        fullName: document.getElementById('edit-name').value,
        phone: document.getElementById('edit-phone').value,
        defaultAddress: document.getElementById('edit-addr').value
      };

      try {
        const res = await fetch(`/api/profile/${currentUser.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (!res.ok) {
          showToast(data.error || 'Ошибка обновления', 'error');
          return;
        }
        currentUser = data;
        localStorage.setItem('crosta_user', JSON.stringify(currentUser));
        toggleProfileEditModal(false);
        await refreshUserProfile();
        renderProfileView();
        showToast('Контактные данные успешно обновлены!');
      } catch (err) {
        showToast('Ошибка при сохранении профиля', 'error');
      }
    }

    // Initialize application
    initTheme();
    initWordRolls();
    initCardFieldListeners();
    loadAllData();
  </script>
</body>
</html>
'''

with open(r'c:\Код\PizzaOrderSystem\wwwroot\index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Generated wwwroot/index.html successfully, size: {len(html_content)} bytes")
