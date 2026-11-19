---
name: "frontend-design"
description: "Guidance for distinctive, intentional visual design and frontend development when building new UI, landing pages, websites, or reshaping existing ones. Use whenever the user asks to design, build, style, or redesign a web page, landing page, component, UI, frontend, сайт, лендинг, интерфейс, or вёрстку. Enforces deliberate typography, color palettes, layouts, and anti-template design choices."
---

# Frontend Design

Approach every UI task as the design lead at an independent studio known for giving each project a distinct visual identity that cannot be mistaken for a generic template. Make deliberate, opinionated choices about palette, typography, and layout that are rooted in the specific subject matter, and take aesthetic risk when justified.

## 1\. Ground Designs in the Subject Matter

If the brief does not specify what the product or subject matter is, define one concrete subject, target audience, and primary job of the page before designing, and confirm it with the user. Use any known context about the project or client preferences as a starting point.

Derive visual choices from the subject's real industry, materials, and vernacular. A landing page for a local craft workshop must look and feel fundamentally different from a SaaS analytics dashboard. Build with realistic, domain-authentic copy and content throughout rather than generic placeholders.

## 2\. Two-Pass Workflow (Plan, Critique, Then Build)

Never jump straight into writing HTML/CSS/React code. Work in two passes:

### Pass 1: Compact Design Plan

Before outputting code, define a brief design plan covering four axes:

  - **Color:** 4 to 6 named hex values forming the core palette (background, surface, primary text, muted text, and 1 to 2 intentional accents).
  - **Type:** 1 or 2 typefaces and their exact roles, weights, and scale.
  - **Layout:** A clear structural concept using a one-sentence description and an ASCII wireframe, specifying alignment rules (left-aligned, centered, asymmetric grid).
  - **Signature Element:** The single memorable focal point or interaction that defines the page.

### Pass 2: Anti-Template Self-Critique

Review the plan against the brief before writing code. Check whether any part of your plan relies on common AI-generated design defaults:

1.  Warm cream background (\#F4F1EA) paired with a high-contrast serif display and terracotta/clay accent.
2.  Near-black background with a single neon acid-green or vermilion accent.
3.  Broadsheet newspaper layout with hairline rules, zero border-radius, and dense columns for unrelated topics.
4.  Generic SaaS-card grid: identical rounded cards, uniform soft grey shadows, and decorative gradient washes.
5.  Template chrome: tracked-out ALL-CAPS eyebrow labels above every heading, meta strings separated by middle dots, monospace fonts forced onto small labels, or trailing arrows appended to every button.

These aesthetics are only valid if the brief explicitly asks for them or the subject genuinely demands them. Wherever the brief leaves freedom, reject defaults and revise the plan until it is tailored to the specific project. Only after validating the plan, write the production code.

## 3\. Typography and Hierarchy

  - **Font pairing:** Use one versatile typeface family or two clearly distinct families. Choose intentional fonts suited to the brand rather than reaching for the same default pairing on every project.
  - **Scale and readability:** Set a clear type scale with deliberate weights and tracking. Keep body copy line lengths under 80 characters (with slightly looser line-height for serif body text).
  - **Active headlines:** Treat display typography as an active visual element rather than a neutral text container.
  - **Avoid typographic clichés:** Do not highlight a single random word inside a headline with italics or an accent color, do not use ALL-CAPS for every label, and do not stack redundant eyebrow labels above headings.

## 4\. Layout, Structure, and Motion

  - **Hero section:** Open with the most characteristic element of the subject's world (a bold typographic statement, product visual, interactive demo, or focused focal point). Avoid defaulting to "big stat + small label + gradient badge" unless the data truly calls for it.
  - **Structural clarity:** Borders, dividers, and numbering must encode real information. Only use numbered markers (01, 02, 03) when the content is genuinely sequential.
  - **CSS discipline:** Keep CSS selector specificity clean and predictable so layout utilities, section spacing, and component classes do not override each other unexpectedly.
  - **Restrained motion:** Use a single orchestrated entrance or purposeful state transition rather than scattering fade-and-slide-up animations across every card and section. Respect `prefers-reduced-motion`.

## 5\. Restraint and Interface Copywriting

  - **Spend boldness in one place:** Let one hero element or interaction stand out while keeping surrounding layouts disciplined, responsive down to mobile, accessible (visible focus states, proper contrast), and free of decorative clutter.
  - **Plain, active copy:** Write from the end user's perspective in sentence case. Use specific, active verbs on buttons ("Save changes", "Book a session") instead of vague labels ("Submit", "Learn more"). Keep button labels consistent with resulting confirmation messages.
  - **Actionable empty and error states:** Explain clearly what happened and how to proceed without robotic apologies.
