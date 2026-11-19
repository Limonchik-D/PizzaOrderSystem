import sys

def main():
    with open('scratch/build_html.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update CSS
    old_css = """    /* Star Rating by DesignBookmark (https://designbookmark.com/motion#db-star-rating) */
    .st-btn {
      position: relative;
      outline: none;
      user-select: none;
      -webkit-user-select: none;
      display: grid;
      place-items: center;
    }
    .st-btn:focus-visible {
      outline: 2px solid var(--accent-primary);
      outline-offset: 2px;
      border-radius: 8px;
    }
    .star-word {
      height: 20px;
      overflow: hidden;
    }
    .star-col {
      display: flex;
      flex-direction: column;
      will-change: transform;
    }
    .star-col b {
      display: block;
      height: 20px;
      line-height: 20px;
    }"""

    new_css = """    /* Star Rating by DesignBookmark (https://designbookmark.com/motion#db-star-rating) */
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
      stroke: var(--border-subtle);
      stroke-width: 1.4;
      fill: transparent;
      transition: none;
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
    }"""

    if old_css in content:
        content = content.replace(old_css, new_css, 1)
        print("CSS successfully updated")
    else:
        print("Error: old_css not found!")
        sys.exit(1)

    # 2. Update Detail Reviews and Helper Functions
    old_detail_reviews = """    function renderDetailReviews(sku) {
      const list = REVIEWS_DATA[sku] || REVIEWS_DATA['PZ-001'];
      document.getElementById('detail-reviews-list').innerHTML = list.map(r => `
        <div class="p-3.5 rounded-xl bg-elevated border border-borderSubtle space-y-1.5">
          <div class="flex items-center justify-between">
            <span class="font-bold text-textPrimary">${r.author} <span class="text-[10px] text-textSecondary font-normal">(${r.city})</span></span>
            <span class="text-amber-400 font-mono">★★★★★</span>
          </div>
          <p class="text-textSecondary leading-relaxed">${r.text}</p>
        </div>
      `).join('');
    }

    let detailReviewStars = 5;
    function setDetailReviewStars(s) { detailReviewStars = s; }
    function toggleReviewForm() {
      document.getElementById('detail-review-form').classList.toggle('hidden');
    }
    function submitDetailReview() {
      const text = document.getElementById('detail-review-input').value.trim();
      if (!text) {
        showToast('Пожалуйста, напишите пару слов в отзыве', 'error');
        return;
      }
      const reviewsContainer = document.getElementById('detail-reviews-list');
      const author = currentUser ? currentUser.fullName : 'Гость ресторана';
      reviewsContainer.insertAdjacentHTML('afterbegin', `
        <div class="p-3.5 rounded-xl bg-elevated border border-brand-700/40 space-y-1.5">
          <div class="flex items-center justify-between">
            <span class="font-bold text-textPrimary">${author} <span class="text-[10px] text-brand-700 font-semibold">(Только что)</span></span>
            <span class="text-amber-400 font-mono">★★★★★</span>
          </div>
          <p class="text-textSecondary leading-relaxed">${text}</p>
        </div>
      `);
      document.getElementById('detail-review-input').value = '';
      toggleReviewForm();
      showToast('Спасибо за ваш отзыв! Шеф-пиццайоло ценит каждое мнение.');
    }"""

    new_detail_reviews = """    // -------------------------------------------------------------------------
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
            fill: 'transparent'
          };
        }
        return {
          stroke: `rgba(245, 158, 11, ${(0.4 + f * 0.6).toFixed(2)})`,
          fill: `rgba(245, 158, 11, ${f.toFixed(2)})`
        };
      }

      function renderFrame() {
        for (let i = 0; i < 5; i++) {
          const s = stars[i];
          const el = starEl[i];
          const c = colStyle(Math.max(0, Math.min(1, s.f.x)));
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
    }"""

    if old_detail_reviews in content:
        content = content.replace(old_detail_reviews, new_detail_reviews, 1)
        print("Detail reviews and helper functions successfully updated")
    else:
        print("Error: old_detail_reviews not found!")
        sys.exit(1)

    # 3. Update Tracking Rating
    old_tracking_block = """      const isDelivered = order.status === 'Delivered';
      const ratingHtml = isDelivered ? `
        <div id="order-rating-box" class="p-4 rounded-xl bg-elevated border border-borderSubtle space-y-3">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <h4 class="text-xs font-bold text-textPrimary uppercase tracking-wider font-mono">Оцените пиццу и доставку</h4>
              <p class="text-[11px] text-textSecondary">Ваш отзыв помогает пиццайоло совершенствовать рецептуру</p>
            </div>
            <span id="star-rating-hint" class="font-mono text-xs font-semibold text-bonus">5/5 — Великолепно!</span>
          </div>
          <div class="flex items-center gap-2">
            ${[1, 2, 3, 4, 5].map(st => `
              <button type="button" onclick="setStarRating(${st})" onmouseenter="previewStarRating(${st})"
                id="star-btn-${st}" class="text-amber-400 hover:scale-115 transition text-2xl active:scale-95">★</button>
            `).join('')}
          </div>
          <div id="rating-feedback-form" class="space-y-2 pt-1">
            <input id="rating-comment" type="text" placeholder="Что вам особенно понравилось? (тесто, соус, хруст)"
              class="w-full px-3 py-1.5 text-xs bg-canvas border border-borderSubtle rounded-lg text-textPrimary focus:ring-1 focus:ring-brand-700" />
            <button type="button" onclick="submitRatingFeedback()"
              class="px-3.5 py-1.5 bg-brand-700 hover:bg-brand-800 text-white font-semibold text-xs rounded-lg transition shadow-sm">
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
    }

    const RATING_DESCS = {
      1: '1/5 — Требует доработки',
      2: '2/5 — Средне',
      3: '3/5 — Хорошо',
      4: '4/5 — Очень вкусно!',
      5: '5/5 — Великолепно!'
    };

    function previewStarRating(st) {
      document.getElementById('star-rating-hint').textContent = RATING_DESCS[st] || '5/5';
      for (let i = 1; i <= 5; i++) {
        const btn = document.getElementById(`star-btn-${i}`);
        if (btn) btn.style.opacity = i <= st ? '1' : '0.35';
      }
    }

    function setStarRating(st) {
      previewStarRating(st);
      showToast(`Спасибо за оценку ${st}/5!`);
    }

    function submitRatingFeedback() {
      const box = document.getElementById('order-rating-box');
      if (box) {
        box.innerHTML = `<div class="p-3 text-center text-xs font-semibold text-bonus bg-surface rounded-xl border border-borderSubtle">
          ✓ Спасибо! Ваш отзыв сохранён и отправлен шеф-пиццайоло.
        </div>`;
      }
    }"""

    new_tracking_block = """      const isDelivered = order.status === 'Delivered';
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
    }"""

    if old_tracking_block in content:
        content = content.replace(old_tracking_block, new_tracking_block, 1)
        print("Tracking block successfully updated")
    else:
        print("Error: old_tracking_block not found!")
        sys.exit(1)

    with open('scratch/build_html.py', 'w', encoding='utf-8') as f:
        f.write(content)

    print("Updated scratch/build_html.py successfully!")

if __name__ == '__main__':
    main()
