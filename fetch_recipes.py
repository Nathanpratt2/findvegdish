import feedparser
import json
import requests
import cloudscraper
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
from dateutil import parser
from urllib.parse import urljoin
import time
import random
import os

# --- CONFIGURATION ---
# Format: ("Blog Name", "Feed URL", ["SPECIAL_TAGS"])
# Tags: "WFPB", "Easy", "Budget"
#Blog notes: Oh She Glows and Avant-Garde Vegan posts to a closed app now - not accessible. 

TOP_BLOGGERS = [
    ("Minimalist Baker", "https://minimalistbaker.com/recipes/vegan/feed/", ["Easy"]),
    ("Nora Cooks", "https://www.noracooks.com/feed/", []),
    ("PlantYou", "https://plantyou.com/feed/", ["WFPB"]),
    ("The Korean Vegan", "https://thekoreanvegan.com/feed/", []),
    ("Rainbow Plant Life", "https://rainbowplantlife.com/feed/", []),
    ("Vegan Richa", "https://www.veganricha.com/feed/", []),
    ("It Doesn't Taste Like Chicken", "https://itdoesnttastelikechicken.com/feed/", ["Budget"]), 
    ("Elavegan", "https://elavegan.com/feed/", []),
    ("The First Mess", "https://thefirstmess.com/feed/", []),
    ("Sweet Potato Soul", "https://sweetpotatosoul.com/feed/", []),
    ("Simple Vegan Blog", "https://simpleveganblog.com/feed/", ["Easy"]),
    ("Connoisseurus Veg", "https://www.connoisseurusveg.com/feed/", []),
    ("Jessica in the Kitchen", "https://jessicainthekitchen.com/feed/", []),
    ("Lazy Cat Kitchen", "https://www.lazycatkitchen.com/feed/", []),
    ("My Darling Vegan", "https://www.mydarlingvegan.com/feed/", []),
    ("The Burger Dude", "https://theeburgerdude.com/feed/", []),
    ("The Vegan 8", "https://thevegan8.com/feed/", ["Easy", "Budget"]), 
    ("From My Bowl", "https://frommybowl.com/feed/", ["WFPB", "Easy"]),
    ("Forks Over Knives", "https://www.forksoverknives.com/all-recipes/feed/", ["WFPB"]),
    ("Rabbit and Wolves", "https://www.rabbitandwolves.com/feed/", []),
    ("Vegan Heaven", "https://veganheaven.org/feed/", []),
    ("The Hidden Veggies", "https://thehiddenveggies.com/feed/", ["Budget"]), 
    ("Vegan in the Freezer", "https://veganinthefreezer.com/feed/", []),
    ("A Virtual Vegan", "https://avirtualvegan.com/feed/", []),
    ("Sarah's Vegan Kitchen", "https://sarahsvegankitchen.com/feed/", []),
    ("Bianca Zapatka", "https://biancazapatka.com/en/feed/", []),
    ("Sweet Simple Vegan", "https://sweetsimplevegan.com/feed/", []),
    ("Make It Dairy Free", "https://makeitdairyfree.com/feed/", []),
    ("Addicted to Dates", "https://addictedtodates.com/category/recipes/feed/", []),
    ("Gretchen's Vegan Bakery", "https://www.gretchensveganbakery.com/feed/", []),
    ("Running on Real Food", "https://runningonrealfood.com/feed/", ["WFPB"]),
    ("The Full Helping", "https://thefullhelping.com/feed/", []),
    ("Turnip Vegan", "https://turnipvegan.com/blogs/news.atom", []),
    ("VegNews", "https://vegnews.com/feed", [])
    ("Plant-Based on a Budget", "https://plantbasedonabudget.com/feed/", ["Budget", "Easy"]),
    ("Woon Heng", "https://woonheng.com/feed/", ["Easy"]),
    ("HealthyGirl Kitchen", "https://healthygirlkitchen.com/feed/", ["Easy", "WFPB"]),
    ("School Night Vegan", "https://schoolnightvegan.com/feed/", []),
]

DISRUPTORS = [
    ("Full of Plants", "https://fullofplants.com/feed/", []),
    ("One Arab Vegan", "https://www.onearabvegan.com/feed/", []),
    ("Mary's Test Kitchen", "https://www.marystestkitchen.com/feed/", []),
    ("Unconventional Baker", "https://www.unconventionalbaker.com/feed/", []),
    ("Fragrant Vanilla Cake", "https://www.fragrantvanilla.com/feed/", []),
    ("Plantifully Based", "https://plantifullybasedblog.com/feed/", []),
    ("Cadry's Kitchen", "https://cadryskitchen.com/feed/", ["Easy"]),
    ("Dr. Vegan", "https://drveganblog.com/feed/", ["Easy"]),
    ("Veggies Don't Bite", "https://veggiesdontbite.com/feed/", []),
    ("Watch Learn Eat", "https://watchlearneat.com/feed/", ["Easy"]),
    ("Strength and Sunshine", "https://strengthandsunshine.com/feed/", ["Easy"]),
    ("The Stingy Vegan", "https://thestingyvegan.com/feed/", ["Easy", "Budget"]), 
    ("Okonomi Kitchen", "https://okonomikitchen.com/feed/", []),
    ("The Foodie Takes Flight", "https://thefoodietakesflight.com/feed/", ["Easy"]),
    ("Vegan Yack Attack", "https://veganyackattack.com/feed/", []),
    ("The Conscious Plant Kitchen", "https://www.theconsciousplantkitchen.com/feed/", ["WFPB"]),
    ("Choosing Chia", "https://choosingchia.com/feed/", ["Easy"]),
    ("Flora & Vino", "https://www.floraandvino.com/feed/", ["WFPB", "Easy"]),
    ("Namely Marly", "https://namelymarly.com/feed/", []),
    ("The Post-Punk Kitchen", "https://www.theppk.com/feed/", []),
    ("The Little Blog of Vegan", "https://www.thelittleblogofvegan.com/feed/", []),
    ("Eat Figs, Not Pigs", "https://www.eatfigsnotpigs.com/feed/", []),
    ("The Banana Diaries", "https://thebananadiaries.com/feed/", []),
    ("Plant Power Couple", "https://www.plantpowercouple.com/feed/", ["Easy"]),
    ("Rainbow Nourishments", "https://www.rainbownourishments.com/feed/", []),
    ("Monkey & Me Kitchen Adventures", "https://monkeyandmekitchenadventures.com/feed/", ["WFPB"]),
    ("Veggiekins", "https://veggiekinsblog.com/feed/", ["Easy"]),
    ("ZardyPlants", "https://zardyplants.com/feed/", ["WFPB"]),
    ("Dreena Burton", "https://dreenaburton.com/feed/", ["WFPB"]),
]

ALL_FEEDS = TOP_BLOGGERS + DISRUPTORS

# --- MAPS ---
URL_MAP = dict((name, url) for name, url, tags in ALL_FEEDS)
BLOG_TAG_MAP = dict((name, tags) for name, url, tags in ALL_FEEDS)

MAX_RECIPES_PER_BLOG = 50 
cutoff_date = datetime.now().astimezone() - timedelta(days=360)

# --- KEYWORDS FOR AUTO TAGGING ---
WFPB_KEYWORDS = ['oil-free', 'oil free', 'no oil', 'wfpb', 'whole food', 'clean', 'refined sugar free', 'detox', 'healthy', 'salad', 'steamed']
EASY_KEYWORDS = ['easy', 'quick', 'simple', 'fast', '1-pot', 'one-pot', 'one pot', '30-minute', 'minute', '15-minute', '20-minute', '5-ingredient', 'sheet pan', 'skillet', 'mug', 'blender', 'no-bake', 'raw','no bake','no-bake', 'air fryer']
BUDGET_KEYWORDS = ['budget', 'cheap', 'frugal', 'economical', 'pantry', 'low cost', 'money saving', '$', 'affordable', 'leftover', 'scraps', 'beans', 'rice', 'lentil', 'potato']

# --- ADVANCED SCRAPER SETUP ---
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'windows',
        'desktop': True
    }
)

def get_auto_tags(title):
    tags = []
    t_lower = title.lower()
    if any(k in t_lower for k in WFPB_KEYWORDS): tags.append("WFPB")
    if any(k in t_lower for k in EASY_KEYWORDS): tags.append("Easy")
    if any(k in t_lower for k in BUDGET_KEYWORDS): tags.append("Budget")
    return tags

def is_pet_recipe(title):
    t = title.lower()
    pet_phrases = ['dog treat', 'cat treat', 'dog biscuit', 'cat biscuit', 'dog food', 'cat food', 'pup treat', 'kitty treat', 'dog cookie']
    if any(phrase in t for phrase in pet_phrases): return True
    return False

def robust_fetch(url, is_binary=False, is_scraping_page=False):
    """
    WATERFALL TECHNIQUE with SMART SLEEP:
    1. Only sleep if we are actively scraping a full page (deep scraping), not checking RSS.
    2. Try Cloudscraper (best for Cloudflare/WP blocks).
    3. Fallback to standard requests if Cloudscraper fails.
    """
    if is_scraping_page:
        time.sleep(random.uniform(2, 4))
    
    try:
        response = scraper.get(url, timeout=20)
        if response.status_code == 200:
            return response.content if is_binary else response.text
    except Exception as e:
        print(f"   [!] Cloudscraper error for {url}: {e}")
    
    # Fallback to standard requests
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            return response.content if is_binary else response.text
    except Exception as e:
        print(f"   [!] Requests error for {url}: {e}")
        
    return None

def fetch_og_image(link):
    """
    Fetches the article HTML to find the High-Res OpenGraph Image.
    Flag is_scraping_page=True to trigger polite sleep delays.
    """
    try:
        html = robust_fetch(link, is_scraping_page=True)
        if not html: return None
        
        soup = BeautifulSoup(html, 'lxml')
        
        # Priority 1: Open Graph Image
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'): 
            return og_image['content']
            
        # Priority 2: Twitter Image
        twitter_image = soup.find('meta', name='twitter:image')
        if twitter_image and twitter_image.get('content'):
            return twitter_image['content']
            
    except Exception:
        return None
    return None

def extract_image(entry, blog_name, link):
    image_candidate = None
    
    # 1. Try Media Content (RSS standard)
    if 'media_content' in entry:
        for media in entry.media_content:
            if 'url' in media: return media['url']
            
    # 2. Try Media Thumbnail
    if 'media_thumbnail' in entry: 
        return entry.media_thumbnail[0]['url']
        
    # 3. Parse HTML Content in Feed
    content = entry.get('content', [{}])[0].get('value', '') or entry.get('summary', '')
    if content:
        soup = BeautifulSoup(content, 'lxml')
        images = soup.find_all('img')
        for img in images:
            src = (img.get('data-src') or img.get('data-lazy-src') or img.get('data-original') or img.get('src'))
            if not src: continue
            
            src_lower = src.lower()
            if any(x in src_lower for x in ['pixel', 'emoji', 'icon', 'logo', 'gravatar', 'gif', 'facebook', 'pinterest', 'share', 'button']): continue
            
            width = img.get('width')
            if width and width.isdigit() and int(width) < 200: continue
            
            image_candidate = src
            break
    
    # 4. Fallback: Waterfall to Scrape the specific page
    if not image_candidate:
        print(f"   ... No image in feed, scraping page: {link[:40]}...")
        image_candidate = fetch_og_image(link)
        
    return image_candidate if image_candidate else "icon.jpg"

def generate_sitemap(recipes):
    now = datetime.now().strftime("%Y-%m-%d")
    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
   <url>
      <loc>https://findvegdish.com/</loc>
      <lastmod>{now}</lastmod>
      <changefreq>daily</changefreq>
      <priority>1.0</priority>
   </url>
</urlset>"""
    with open('sitemap.xml', 'w') as f:
        f.write(sitemap_content)
    print("Generated sitemap.xml")

# --- MAIN EXECUTION ---

# 1. Load Existing Data
try:
    with open('data.json', 'r') as f:
        recipes = json.load(f)
        print(f"Loaded {len(recipes)} existing recipes.")
except (FileNotFoundError, json.JSONDecodeError):
    recipes = []
    print("No existing database found. Starting fresh.")

# 2. Cleanse Database
initial_count = len(recipes)
# Cleanse old VegNews entries if they exist
recipes = [r for r in recipes if not (r['blog_name'] == "VegNews" and "/recipes/" not in r['link'])]
existing_links = {r['link'] for r in recipes}
feed_stats = {} 

print(f"Fetching recipes from {len(ALL_FEEDS)} blogs using Cloudscraper...")

# 3. Scrape Feeds
for name, url, special_tags in ALL_FEEDS:
    new_count = 0
    status = "✅ OK"
    
    try:
        print(f"Checking {name}...")
        
        # STEP 1: Fetch Raw XML string via Cloudscraper (is_scraping_page=False for speed)
        xml_content = robust_fetch(url, is_scraping_page=False)
        
        # Fallback for VegNews specifically
        if (not xml_content) and name == "VegNews":
             xml_content = robust_fetch("https://vegnews.com/rss", is_scraping_page=False)

        if not xml_content:
            status = f"❌ Blocked/ConnErr"
            feed_stats[name] = {'new': 0, 'status': status}
            continue

        # STEP 2: Parse the String
        feed = feedparser.parse(xml_content)
        
        if not feed.entries:
            status = "⚠️ Parsed 0 items"
        
        for entry in feed.entries:
            try:
                # FIX: Improved VegNews Filter using Link
                if "vegnews.com" in entry.link and "/recipes/" not in entry.link: continue

                dt = entry.get('published', entry.get('updated', None))
                if not dt: continue
                
                try:
                    published_time = parser.parse(dt)
                except Exception:
                    continue

                # FIX: Standardize Timezone to UTC
                if published_time.tzinfo is None:
                    published_time = published_time.replace(tzinfo=timezone.utc)
                else:
                    published_time = published_time.astimezone(timezone.utc)
                
                if published_time > cutoff_date:
                    if entry.link not in existing_links:
                        if is_pet_recipe(entry.title): continue

                        # Extract Image (includes Waterfall fallback)
                        image_url = extract_image(entry, name, entry.link)
                        
                        # FIX: Robust URL Joining
                        if image_url and image_url.startswith('/'):
                            # Try to get the base from the feed object, fallback to feed URL
                            base = feed.feed.get('link') or url
                            image_url = urljoin(base, image_url)
                        
                        recipes.append({
                            "blog_name": name,
                            "title": entry.title,
                            "link": entry.link,
                            "image": image_url,
                            "date": published_time.isoformat(),
                            "is_disruptor": name in [d[0] for d in DISRUPTORS],
                            "special_tags": [] 
                        })
                        existing_links.add(entry.link)
                        new_count += 1
            except Exception as e:
                continue
        
        feed_stats[name] = {'new': new_count, 'status': status}

    except Exception as e:
        print(f"Failed to parse {name}: {e}")
        feed_stats[name] = {'new': 0, 'status': f"❌ Crash: {str(e)[:20]}"}

# 4. Backfill Tags
print("Updating tags for all recipes...")
for recipe in recipes:
    base_tags = list(BLOG_TAG_MAP.get(recipe['blog_name'], []))
    auto_tags = get_auto_tags(recipe['title'])
    combined_tags = list(set(base_tags + auto_tags))
    recipe['special_tags'] = combined_tags

# 5. Prune & Stats
print("Pruning database and calculating stats...")
recipes_by_blog = {}
for r in recipes:
    bname = r['blog_name']
    if bname not in recipes_by_blog: recipes_by_blog[bname] = []
    recipes_by_blog[bname].append(r)

final_pruned_list = []
total_counts = {} 
latest_dates = {} 
wfpb_counts = {}
easy_counts = {}
budget_counts = {}

for bname, blog_recipes in recipes_by_blog.items():
    blog_recipes.sort(key=lambda x: x['date'], reverse=True)
    
    if len(blog_recipes) > 0:
        latest_dates[bname] = blog_recipes[0]['date'][:10] 
    
    kept_recipes = blog_recipes[:MAX_RECIPES_PER_BLOG]
    final_pruned_list.extend(kept_recipes)
    total_counts[bname] = len(kept_recipes)
    
    wfpb_counts[bname] = sum(1 for r in kept_recipes if "WFPB" in r['special_tags'])
    easy_counts[bname] = sum(1 for r in kept_recipes if "Easy" in r['special_tags'])
    budget_counts[bname] = sum(1 for r in kept_recipes if "Budget" in r['special_tags'])

final_pruned_list.sort(key=lambda x: x['date'], reverse=True)

if len(final_pruned_list) > 50:
    with open('data.json', 'w') as f:
        json.dump(final_pruned_list, f, indent=2)
    generate_sitemap(final_pruned_list)
else:
    print("⚠️ SAFETY ALERT: Database too small (<50 items). Skipping write.")

# 6. Generate Report
with open('FEED_HEALTH.md', 'w') as f:
    f.write(f"# Feed Health Report\n")
    f.write(f"**Last Run:** {datetime.now().isoformat()}\n")

    total_new_today = sum(stats.get('new', 0) for stats in feed_stats.values())
    total_in_db = len(final_pruned_list)
    total_blogs_monitored = len(ALL_FEEDS)
    
    all_dates = [parser.parse(d) for d in latest_dates.values() if d != "N/A"]
    if all_dates:
        avg_date_timestamp = sum(d.timestamp() for d in all_dates) / len(all_dates)
        avg_date = datetime.fromtimestamp(avg_date_timestamp).strftime('%Y-%m-%d')
    else:
        avg_date = "N/A"

    three_months_ago = datetime.now() - timedelta(days=90)
    stale_count = 0
    report_rows = []
    
    all_names = set(list(feed_stats.keys()) + list(total_counts.keys()))
    
    for name in all_names:
        url = URL_MAP.get(name, "Unknown")
        new = feed_stats.get(name, {}).get('new', 0)
        status = feed_stats.get(name, {}).get('status', 'Skipped/DB Only')
        total = total_counts.get(name, 0)
        latest = latest_dates.get(name, "N/A")
        
        if latest != "N/A":
            try:
                latest_dt = parser.parse(latest)
                if latest_dt.replace(tzinfo=None) < three_months_ago.replace(tzinfo=None):
                    stale_count += 1
                    if "❌" not in status: status = f"⚠️ Stale (>90d) {status.replace('✅ OK', '')}"
            except: pass
        
        if total == 0 and "✅" in status: status = "❌ No Recipes"
            
        report_rows.append((name, url, new, total, latest, status))

    f.write(f"**Active Blogs (Last 90d):** {total_blogs_monitored - stale_count} / {total_blogs_monitored}\n")
    f.write(f"**Total Database Size:** {total_in_db}\n")
    f.write(f"**New Today:** {total_new_today}\n\n")

    f.write("| Blog Name | New | Total | Latest | Status |\n")
    f.write("|-----------|-----|-------|--------|--------|\n")
    
    report_rows.sort(key=lambda x: (0 if '❌' in x[5] else 1, x[0]))
    
    for row in report_rows:
        f.write(f"| {row[0]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} |\n")

print(f"Done. Database: {len(final_pruned_list)}")
