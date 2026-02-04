# Daily Vegan Recipes (findvegdish.com)

A high-performance, minimal-maintenance discovery engine for new vegan recipes. This project is built with a "Creator First" philosophy, designed to send traffic directly to bloggers while remaining robust enough to rarely break.

## 🎯 Core Philosophy

### 1. Simple & Robust
The goal is to have as few moving parts as possible. It is better to have fewer features that work perfectly than complex features that require constant fixing. If a feature isn't essential to finding a meal, it isn't included.

### 2. Creator First (Traffic to Real People)
This site is a bridge, not a destination. We do not display ingredients or instructions. By keeping "time on site" low, we ensure that the value—and the traffic—is passed directly to the original creators.

### 3. Zero Dependencies & "No-Break" Programming
To ensure the site remains functional for years with zero intervention:
- **No Image Proxies:** We load original images directly. We do not use services like `weserv.nl` because they create a single point of failure.
- **No Production LLMs:** We do not use AI in the live environment. This prevents API failures and allows the site to run completely free
- **No Frameworks:** Built with 100% Vanilla JS, HTML, and CSS. There are no libraries to update or build-tools to manage.

---

## 📊 Data & Inventory Logic

### Seasonal Rotation (Not a Database)
This site is designed to be seasonally relevant, not a permanent archive. 
- **The 3-Month Window:** We maintain roughly **1,000 recipes** at a time
- **Volume:** With ~40+ blogs posting roughly 2.5 meals/day, a 100-day window provides ~250 new meals. We keep 3x that amount to ensure variety.
- **The 50 Cap:** To prevent a single large blog from dominating the feed, we cap each creator at **50 recipes**. This ensures a diverse mix of voices.

### Categorization (Top vs. Rising)
We avoid complex, subjective ranking systems. Creators are categorized simply:
- **Top Site:** High-traffic, established blogs as of February 2026 (can be updated annually if needed). 
- **Rising Blog:** Up-and-coming creators with high-quality content but not the social / blog following that the Top Sites have
- **The 50/50 Split:** We want all blogs to have either assignment to avoid a view that somehow they are not as good as other blogs. We aim for an even split between Top and Rising sites in the spirit of this being a discovery engine not seeing the same stuff you have always seen. This ensures new creators get discovered alongside established favorites without requiring constant manual monitoring.

---

## 🛠 Technical Implementation

### Smart Filtering & Exclusion Logic
The search and category logic uses "Smart Exclusion" to maintain high accuracy without needing complex tagging or AI:
- **Meals Filter:** Targets savory keywords but strictly **excludes** things like `treats`, `sauce`, or `dressing`.
- **Sweets Filter:** Targets dessert keywords but strictly **excludes** savory overlaps such as `spicy`, `chili`, `shepherd's`, `egg`, or `pot`.
- **Accuracy:** Tags are associated at the blog level or via title-matching. We prioritize broad discoverability over 100% granular perfection.
- Keeping this filtering simple, avoids overly complex or more intelligent yet costly LLM assignments

### Performance & UI
- **Lazy Loading:** Uses native browser `loading="lazy"` to keep initial load speeds fast.
- **Mobile-First:** Navigation and action buttons to ensure they are easy to hit on mobile devices.
- **Batch Rendering:** Recipes are rendered in batches of 48 to keep the DOM light and the scrolling smooth.

---

## 🚀 Deployment & Maintenance
- **Hosting:** GitHub Pages + Cloudflare.
- **Updates:** Content updates are handled by pushing a new `data.json` file.
- **Maintenance:** Near-zero. Since there are no external APIs or frameworks, the site will continue to function as long as the domain and hosting are active.
