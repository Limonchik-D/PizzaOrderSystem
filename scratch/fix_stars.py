import sys

def main():
    with open('scratch/build_html.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update CSS to remove fill: transparent and stroke: var(--border-subtle)
    old_css = """    .db-star-btn path {
      transform-origin: 12px 12px;
      stroke: var(--border-subtle);
      stroke-width: 1.4;
      fill: transparent;
      transition: none;
    }"""

    new_css = """    .db-star-btn path {
      transform-origin: 12px 12px;
      stroke-width: 1.4;
      transition: filter 150ms ease;
    }"""

    if old_css in content:
        content = content.replace(old_css, new_css, 1)
        print("CSS successfully updated")
    else:
        print("Error: old_css not found!")
        sys.exit(1)

    # 2. Update colStyle and renderFrame to use explicit style.fill / stroke / filter with vibrant gold #ffd23f
    old_js = """      function colStyle(f) {
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
      }"""

    new_js = """      function colStyle(f) {
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
      }"""

    if old_js in content:
        content = content.replace(old_js, new_js, 1)
        print("JS colStyle and renderFrame successfully updated")
    else:
        print("Error: old_js not found!")
        sys.exit(1)

    with open('scratch/build_html.py', 'w', encoding='utf-8') as f:
        f.write(content)

    print("scratch/build_html.py updated successfully!")

if __name__ == '__main__':
    main()
