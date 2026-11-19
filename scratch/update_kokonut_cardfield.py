import sys

def main():
    with open('scratch/build_html.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update CSS
    old_css = """    /* Kokonut CardField Flip Animation */
    .cardfield-brand-flip {
      transition: transform 200ms var(--ease-out), opacity 200ms var(--ease-out);
    }"""

    new_css = """    /* Kokonut UI CardField (https://kokonutui.com, MIT license) */
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
    }"""

    if old_css in content:
        content = content.replace(old_css, new_css, 1)
        print("CSS successfully updated")
    else:
        print("Error: old_css not found!")
        sys.exit(1)

    # 2. Update HTML
    old_html = """          <!-- Kokonut UI Interactive CardField (No demo button) -->
          <div id="cardfield-container" class="space-y-2 p-3 bg-canvas border border-borderSubtle rounded-xl">
            <div class="flex items-center justify-between text-[11px]">
              <span class="font-medium text-textSecondary flex items-center gap-1">
                <span id="cardfield-brand-badge" class="font-bold text-textPrimary">Банковская карта</span>
                <span id="cardfield-luhn-status" class="hidden text-[10px] text-emerald-600 font-bold">✓ Валидна</span>
              </span>
            </div>

            <!-- Single-line compact cardfield -->
            <div id="cardfield-row" class="relative flex items-center gap-2 p-2 bg-surface border border-borderSubtle rounded-lg transition focus-within:ring-1 focus-within:ring-brand-700">
              <!-- Brand SVG Icon Slot -->
              <div id="cardfield-brand-icon" class="w-7 h-5 flex items-center justify-center shrink-0">
                <svg width="22" height="16" viewBox="0 0 24 24" fill="none" class="text-textSecondary" xmlns="http://www.w3.org/2000/svg">
                  <rect x="2" y="5" width="20" height="14" rx="3" stroke="currentColor" stroke-width="1.6"/>
                  <line x1="2" y1="10" x2="22" y2="10" stroke="currentColor" stroke-width="1.6"/>
                  <line x1="6" y1="15" x2="10" y2="15" stroke="currentColor" stroke-width="1.6"/>
                </svg>
              </div>

              <!-- Number Input / Collapsed 4-digits -->
              <div class="relative flex-1 min-w-0">
                <input id="card-num-input" type="text" maxlength="19" placeholder="0000 0000 0000 0000"
                  oninput="handleCardNumberInput(this)"
                  class="w-full bg-transparent font-mono text-xs sm:text-sm text-textPrimary outline-none tracking-wider placeholder:text-textSecondary/40" />
                <div id="card-num-collapsed" onclick="expandCardNumber()" class="hidden absolute inset-0 bg-surface flex items-center font-mono text-xs sm:text-sm font-bold text-textPrimary cursor-pointer">
                  •••• <span id="card-last4-digits" class="ml-1">4242</span>
                  <span class="text-[10px] text-textSecondary font-sans font-normal ml-2 hover:underline">(изменить)</span>
                </div>
              </div>

              <!-- Revealable Expiry & CVC inputs -->
              <div id="card-extra-fields" class="hidden flex items-center gap-1.5 shrink-0 pl-1 border-l border-borderSubtle">
                <input id="card-exp-input" type="text" maxlength="5" placeholder="MM/YY"
                  onfocus="flipCardBrandIcon('exp')"
                  oninput="formatCardExpiry(this)"
                  class="w-14 bg-transparent font-mono text-xs text-textPrimary outline-none text-center" />
                <input id="card-cvc-input" type="password" maxlength="3" placeholder="CVC"
                  onfocus="flipCardBrandIcon('cvc')"
                  onblur="flipCardBrandIcon('blur')"
                  class="w-10 bg-transparent font-mono text-xs text-textPrimary outline-none text-center" />
              </div>
            </div>
          </div>"""

    new_html = """          <!-- Kokonut UI CardField (https://kokonutui.com, MIT license) -->
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
          </div>"""

    if old_html in content:
        content = content.replace(old_html, new_html, 1)
        print("HTML successfully updated")
    else:
        print("Error: old_html not found!")
        sys.exit(1)

    # 3. Update JavaScript Functions
    old_js = """    // -------------------------------------------------------------------------
    // 15. Kokonut UI CardField (Luhn Check, Card Brand Flip)
    // -------------------------------------------------------------------------
    function handlePaymentMethodChange(method) {
      const container = document.getElementById('cardfield-container');
      if (container) container.classList.toggle('hidden', method !== 'CardOnline');
    }

    function checkLuhn(val) {
      const clean = val.replace(/\D/g, '');
      if (clean.length < 15) return false;
      let sum = 0;
      let shouldDouble = false;
      for (let i = clean.length - 1; i >= 0; i--) {
        let digit = parseInt(clean.charAt(i), 10);
        if (shouldDouble) {
          digit *= 2;
          if (digit > 9) digit -= 9;
        }
        sum += digit;
        shouldDouble = !shouldDouble;
      }
      return (sum % 10) === 0;
    }

    function detectCardBrand(num) {
      const clean = num.replace(/\D/g, '');
      if (/^4/.test(clean)) return 'visa';
      if (/^(5[1-5]|2[2-7])/.test(clean)) return 'mastercard';
      if (/^3[47]/.test(clean)) return 'amex';
      return 'generic';
    }

    function renderBrandIconSvg(brand) {
      if (brand === 'visa') {
        return `<svg width="24" height="16" viewBox="0 0 36 24" fill="none"><rect width="36" height="24" rx="3" fill="#1A1F71"/><text x="6" y="16" fill="#fff" font-family="sans-serif" font-weight="900" font-size="12" font-style="italic">VISA</text></svg>`;
      }
      if (brand === 'mastercard') {
        return `<svg width="24" height="16" viewBox="0 0 36 24" fill="none"><rect width="36" height="24" rx="3" fill="#222"/><circle cx="14" cy="12" r="7" fill="#EB001B"/><circle cx="22" cy="12" r="7" fill="#F79E1B" fill-opacity="0.8"/></svg>`;
      }
      if (brand === 'amex') {
        return `<svg width="24" height="16" viewBox="0 0 36 24" fill="none"><rect width="36" height="24" rx="3" fill="#0077A6"/><text x="4" y="15" fill="#fff" font-family="sans-serif" font-weight="800" font-size="9">AMEX</text></svg>`;
      }
      return `<svg width="22" height="16" viewBox="0 0 24 24" fill="none" class="text-textSecondary"><rect x="2" y="5" width="20" height="14" rx="3" stroke="currentColor" stroke-width="1.6"/><line x1="2" y1="10" x2="22" y2="10" stroke="currentColor" stroke-width="1.6"/></svg>`;
    }

    function handleCardNumberInput(input) {
      let raw = input.value.replace(/\D/g, '').slice(0, 16);
      let formatted = raw.replace(/(\d{4})(?=\d)/g, '$1 ');
      input.value = formatted;

      const brand = detectCardBrand(raw);
      const iconSlot = document.getElementById('cardfield-brand-icon');
      const badge = document.getElementById('cardfield-brand-badge');
      if (iconSlot) iconSlot.innerHTML = renderBrandIconSvg(brand);
      if (badge) badge.textContent = brand === 'visa' ? 'Visa' : brand === 'mastercard' ? 'Mastercard' : brand === 'amex' ? 'Amex' : 'Банковская карта';

      if (raw.length === 16) {
        const isValid = checkLuhn(raw);
        const luhnStatus = document.getElementById('cardfield-luhn-status');
        if (isValid) {
          luhnStatus?.classList.remove('hidden');
          collapseCardNumber(raw);
        } else {
          luhnStatus?.classList.add('hidden');
          shakeCardField();
        }
      }
    }

    function collapseCardNumber(raw) {
      const input = document.getElementById('card-num-input');
      const collapsed = document.getElementById('card-num-collapsed');
      const last4 = document.getElementById('card-last4-digits');
      const extra = document.getElementById('card-extra-fields');

      if (last4) last4.textContent = raw.slice(-4);
      if (input) input.classList.add('hidden');
      if (collapsed) collapsed.classList.remove('hidden');
      if (extra) {
        extra.classList.remove('hidden');
        document.getElementById('card-exp-input')?.focus();
      }
    }

    function expandCardNumber() {
      const input = document.getElementById('card-num-input');
      const collapsed = document.getElementById('card-num-collapsed');
      const extra = document.getElementById('card-extra-fields');

      if (collapsed) collapsed.classList.add('hidden');
      if (extra) extra.classList.add('hidden');
      if (input) {
        input.classList.remove('hidden');
        input.focus();
      }
    }

    function shakeCardField() {
      const row = document.getElementById('cardfield-row');
      if (row && typeof gsap !== 'undefined') {
        gsap.fromTo(row, { x: 0 }, { x: -8, duration: 0.06, yoyo: true, repeat: 5, onComplete: () => gsap.set(row, { x: 0 }) });
      }
    }

    function formatCardExpiry(input) {
      let v = input.value.replace(/\D/g, '').slice(0, 4);
      if (v.length > 2) v = v.slice(0, 2) + '/' + v.slice(2);
      input.value = v;
      if (v.length === 5) {
        document.getElementById('card-cvc-input')?.focus();
      }
    }

    function flipCardBrandIcon(field) {
      const iconSlot = document.getElementById('cardfield-brand-icon');
      if (field === 'cvc') {
        iconSlot.innerHTML = `<svg width="22" height="16" viewBox="0 0 24 24" fill="none" class="text-brand-700"><rect x="3" y="11" width="18" height="11" rx="2" stroke="currentColor" stroke-width="1.6"/><path d="M7 11V7a5 5 0 0 1 10 0v4" stroke="currentColor" stroke-width="1.6"/></svg>`;
      } else {
        const raw = document.getElementById('card-num-input')?.value || '';
        iconSlot.innerHTML = renderBrandIconSvg(detectCardBrand(raw));
      }
    }"""

    new_js = """    // -------------------------------------------------------------------------
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
    }"""

    if old_js in content:
        content = content.replace(old_js, new_js, 1)
        print("JS successfully updated")
    else:
        print("Error: old_js not found!")
        sys.exit(1)

    # 4. Update init calls at bottom
    old_init = """    // Initialize application
    initTheme();
    initWordRolls();
    loadAllData();"""

    new_init = """    // Initialize application
    initTheme();
    initWordRolls();
    initCardFieldListeners();
    loadAllData();"""

    if old_init in content:
        content = content.replace(old_init, new_init, 1)
        print("Init calls successfully updated")
    else:
        print("Error: old_init not found!")
        sys.exit(1)

    with open('scratch/build_html.py', 'w', encoding='utf-8') as f:
        f.write(content)

    print("Updated scratch/build_html.py successfully!")

if __name__ == '__main__':
    main()
