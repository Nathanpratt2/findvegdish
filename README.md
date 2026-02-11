Daily Vegan Recipes (findvegdish.com)
A high-performance, minimal-maintenance discovery engine for new vegan recipes. This project is built with a "Creator First" philosophy, designed to send traffic directly to bloggers while remaining robust enough to rarely break.
🎯 Core Philosophy
1. Simple Frontend, Robust Backend
Frontend: The user-facing site is 100% Vanilla JS, HTML, and CSS. There are no build tools, no frameworks (React/Vue), and no client-side dependencies. This ensures the site loads instantly and never suffers from "dependency rot."
Backend: The data fetching logic is sophisticated. It employs a Hybrid Scraping Engine that combines RSS parsing, direct HTML scraping, and headless browser automation (Selenium) to ensure 99% uptime for feed retrieval.
2. Creator First (Traffic to Real People)
This site is a bridge, not a destination. We explicitly do not display ingredients or instructions. By keeping "time on site" low, we ensure that the value—and the traffic—is passed directly to the original creators.
3. "No-Break" Reliability
To ensure longevity:
Direct Linking: We load original images directly from the source (with referrer hiding). We do not use image proxies, removing a single point of failure.
Static Data: The site runs from a single data.json file. If the scraper fails one day, the site remains online and functional with yesterday's data.
🛠 Backend: The Hybrid Scraping Engine
The core logic resides in fetch_recipes.py. Unlike simple RSS readers, this system uses a tiered approach to gather content from over 100 sources.
1. Tiered Fetching Strategy
RSS Parsing: The preferred method. Fast and lightweight using feedparser.
HTML Scraping (Custom): For sites that dropped RSS support (e.g., Pick Up Limes, Baking Hermann), we use BeautifulSoup to scrape recipe indices directly.
Selenium Fallback (The Nuclear Option): If a site is protected by heavy Cloudflare rules or requires JavaScript to render, the script launches a headless Chrome instance to retrieve the content.
2. Smart Categorization & Tagging
Top Bloggers: Established giants (e.g., Minimalist Baker, Rainbow Plant Life).
Disruptors: High-quality, rising creators. In the UI, these are highlighted to encourage discovery of new voices.
Auto-Tagging: The script analyzes titles and feeds to apply tags automatically:
WFPB: "Oil-free", "Whole food"
GF: "Gluten-free", "Almond flour" (plus specific GF-only feed handling)
Easy: "1-pot", "30-minute", "Air fryer"
Budget: "Pantry", "Cheap", "Beans"
3. Data Hygiene
Pet Filter: Automatically removes recipes for dog/cat treats.
Non-Recipe Filter: Removes "Gift Guides," "Meal Plans," and "News" articles.
Deduplication: Logic exists to handle blogs that have both "Main" and "Gluten-Free" feeds, preventing duplicate entries while preserving specific GF tagging.
💻 Frontend: Performance & UX
The index.html file is a study in modern, vanilla web performance.
1. "Tight" Fuzzy Search
We do not use external search libraries (like Fuse.js) to save weight. Instead, we implemented a custom Levenshtein Distance algorithm.
Logic: It tokenizes the user's input and matches it against titles/authors.
Tolerance:
Words < 4 chars: Must match exactly.
Words 4-7 chars: Allows 1 typo.
Words > 7 chars: Allows 2 typos.
2. Performance Optimizations
LCP Optimization: The first 4 images are loaded with fetchpriority="high" and loading="eager".
Lazy Loading: All subsequent images use native loading="lazy" and decoding="async".
Skeleton Screens: CSS-only skeleton loaders prevent layout shift (CLS) during data fetching.
3. Features
Dark Mode: Long-press the logo to toggle. Persists via LocalStorage.
PWA: Fully installable on mobile devices (manifest.json included).
Shuffle: Randomizes the feed for discovery, complete with a CSS "jiggle" animation.
📂 File Structure & Artifacts
fetch_recipes.py: The worker script. Scrapes, cleans, and generates data.
data.json: The database. Contains ~1,000 active recipes.
FEED_HEALTH.md: A generated report detailing which blogs are active, blocked, or empty.
llms.txt: A standardized file providing context for AI bots/crawlers about the site's structure and authority.
sitemap.xml: Auto-generated SEO sitemap.
index.html: The application.
🚀 How to Run (Development)
Prerequisites
Python 3.9+
Google Chrome (for Selenium fallback)
1. Install Dependencies
code
Bash
pip install -r requirements.txt
# OR manually:
pip install feedparser beautifulsoup4 requests cloudscraper selenium webdriver-manager python-dateutil lxml
2. Run the Scraper
code
Bash
python fetch_recipes.py
This will iterate through ~100 feeds.
It may take 2-5 minutes depending on how many sites require Selenium.
Check FEED_HEALTH.md afterwards to see the status of every blog.
3. Launch the Site
Simply open index.html in a browser. No server required (though a local server is recommended for Service Worker/PWA testing).
🔍 Maintenance Guide
Monitor FEED_HEALTH.md:
Look for ❌ Blocked/HTML Fail. If a site consistently fails, their DOM structure may have changed, or they may have blocked the bot.
Look for ⚠️ Low Count. If a major blog shows 0-1 recipes, the date parsing logic might be failing for their specific format.
Updating Sources:
Edit the TOP_BLOGGERS, DISRUPTORS, or HTML_SOURCES lists in fetch_recipes.py.
Format: ("Display Name", "URL", ["Manual_Tags"])
Seasonal Rotation:
The script automatically prunes recipes older than 360 days. No manual cleanup is required.
