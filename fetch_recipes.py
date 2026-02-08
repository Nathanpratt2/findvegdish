import feedparser
import json
import requests
import cloudscraper
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
from dateutil import parser
from urllib.parse import urljoin, urlparse
import time
import random
import os
import ssl
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import create_urllib3_context
from requests.packages.urllib3.poolmanager import PoolManager

# --- CONFIGURATION ---
# Format: ("Blog Name", "Feed URL", ["SPECIAL_TAGS"])

TOP_BLOGGERS = [
    ("Minimalist Baker (Vegan Recipes)", "https://minimalistbaker.com/recipes/vegan/feed/", ["Easy"]),
    ("Nora Cooks", "https://www.noracooks.com/feed/", []),
    ("PlantYou", "https://plantyou.com/feed/", ["WFPB"]),
    ("The Korean Vegan", "https://thekoreanvegan.com/feed/", []),
    ("Rainbow Plant Life", "https://rainbowplantlife.com/feed/", []), # Main Feed
    ("Vegan Richa", "https://www.veganricha.com/feed/", []), # Main Feed
    ("Forks Over Knives", "https://www.forksoverknives.com/feed/?post_type=recipe", []),
    ("It Doesn't Taste Like Chicken", "https://itdoesnttastelikechicken.com/feed/", []), 
    ("Elavegan", "https://elavegan.com/feed/", ["GF"]), # Will auto-tag GF
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
    ("Bianca Zapatka", "https://https://biancazapatka.com/en/feed/", []),
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
    ("VegNews", "https://vegnews.com/feed", []),
    ("Plant-Based on a Budget", "https://plantbasedonabudget.com/feed/", ["Budget"]),
    ("HealthyGirl Kitchen", "https://healthygirlkitchen.com/feed/", [])
]

DISRUPTORS = [
    ("Full of Plants", "https://fullofplants.com/feed/", []),
    ("One Arab Vegan", "https://www.onearabvegan.com/feed/", []),
    ("Mary's Test Kitchen", "https://www.marystestkitchen.com/feed/", []),
    ("Unconventional Baker", "https://www.unconventionalbaker.com/feed/", ["GF"]), # Will auto-tag GF
    ("Fragrant Vanilla Cake", "https://www.fragrantvanilla.com/feed/", []),
    ("Plantifully Based", "https://plantifullybasedblog.com/feed/", []),
    ("Cadry's Kitchen (Vegan Recipes)", "https://cadryskitchen.com/vegan-recipes/feed/", ["Easy"]),
    ("Dr. Vegan", "https://drveganblog.com/feed/", ["Easy"]),
    ("Veggies Don't Bite", "https://veggiesdontbite.com/feed/", []),
    ("Watch Learn Eat", "https://watchlearneat.com/feed/", ["Easy"]),
    ("Strength and Sunshine", "https://strengthandsunshine.com/feed/", ["Easy"],["GF"]), # Will auto-tag GF
    ("The Stingy Vegan", "https://thestingyvegan.com/feed/", ["Easy", "Budget"]),
    ("The Foodie Takes Flight", "https://thefoodietakesflight.com/feed/", ["Easy"]),
    ("Vegan Yack Attack", "https://veganyackattack.com/feed/", []),
    ("Messy Vegan Cook", "https://messyvegancook.com/feed/", []),
    ("The Conscious Plant Kitchen", "https://www.theconsciousplantkitchen.com/feed/", []),
    ("Choosing Chia (Vegan Recipes)", "https://choosingchia.com/category/diet%20/vegan/feed/", ["Easy"]),
    ("Flora & Vino", "https://www.floraandvino.com/feed/", ["WFPB"], ["Easy"]),
    ("Namely Marly", "https://namelymarly.com/feed/", []),
    ("The Post-Punk Kitchen", "https://www.theppk.com/feed/", []),
    ("The Little Blog of Vegan", "https://www.thelittleblogofvegan.com/feed/", []),
    ("Eat Figs, Not Pigs", "https://www.eatfigsnotpigs.com/feed/", []),
    ("The Banana Diaries", "https://thebananadiaries.com/feed/", []),
    ("Plant Power Couple", "https://www.plantpowercouple.com/feed/", ["Easy"]),
    ("Rainbow Nourishments", "https://www.rainbownourishments.com/feed/", []),
    ("Rhian's Recipes", "https://www.rhiansrecipes.com/feed/", ["GF"]), # Will auto-tag GF
    ("Snixy Kitchen (Vegan Recipes)", "https://www.snixykitchen.com/special-diet/vegan/feed/", []),
    ("Monkey & Me Kitchen Adventures", "https://monkeyandmekitchenadventures.com/feed/", ["WFPB"]),
    ("Ann Arbor Vegan Kitchen", "https://www.annarborvegankitchen.com/feed/", ["WFPB"]),
    ("Veggiekins", "https://veggiekinsblog.com/feed/", ["Easy"],["GF"]), # Will auto-tag GF
    ("ZardyPlants", "https://zardyplants.com/feed/", ["WFPB"]),
    ("Dreena Burton", "https://dreenaburton.com/feed/", ["WFPB"]),
    ("Cupful of Kale", "https://cupfulofkale.com/feed/", []),
    ("What Jew You Want to Eat", "https://whatjewwannaeat.com/vegan/feed/", []),
    ("Holistic Chef Academy", "https://https://holisticchefacademy.com/feed/", []),
    ("Healthy Little Vittles", "https://healthylittlevittles.com/feed/", ["GF"]), # Will auto-tag GF
    ("Healthier Steps", "https://healthiersteps.com/feed/", [])
]

# --- DIRECT HTML SCRAPING SOURCES ---
HTML_SOURCES = [
    ("Pick Up Limes", "https://www.pickuplimes.com/recipe/", [], "custom_pul"),
    ("Zucker & Jagdwurst", "https://www.zuckerjagdwurst.com/en/archive/1", [], "wordpress"),
    ("Rainbow Plant Life GF", "https://rainbowplantlife.com/diet/gluten-free/", ["GF"], "wordpress"),
    ("Vegan Richa GF", "https://www.veganricha.com/category/gluten-free/", ["GF"], "wordpress"),
    ("School Night Vegan", "https://schoolnightvegan.com/category/recipes/", [], "custom_pul"),
    ("Love and Lemons (Vegan Recipes)", "https://www.loveandlemons.com/category/recipes/vegan/", [], "wordpress"),
    ("Cookie and Kate (Vegan Recipes)", "https://cookieandkate.com/category/vegan-recipes/", [], "custom_pul"),
    ("The Loopy Whisk (Vegan Recipes)", "https://theloopywhisk.com/diet/vegan/", ["GF"], "wordpress"),
    ("Oh She Glows","https://www.ohsheglows.com/recipe-search/",[], "wordpress"),
    ("The Full Helping (Vegan Recipes)","https://www.thefullhelping.com/dietary/vegan/",[],"wordpress"),
    ("Hot For Food","https://www.hotforfoodblog.com/recipe-index/",[],"wordpress")
]

# --- DISPLAY NAME MAPPING ---
# Maps Internal Name -> Public Display Name
# Updated: We do NOT merge GF blogs back to main names anymore. 
# They will appear separately (e.g. "Rainbow Plant Life GF").
DISPLAY_NAME_MAP = {}

ALL_FEEDS = TOP_BLOGGERS + DISRUPTORS

# --- MAPS ---
URL_MAP = {}
BLOG_TAG_MAP = {}

# Process RSS Feeds
for item in ALL_FEEDS:
    if len(item) == 3:
        name, url, tags = item
        URL_MAP[name] = url
        BLOG_TAG_MAP[name] = tags
    else:
        print(f"⚠️ Warning: Skipping malformed RSS config: {item}")

# Process HTML Sources
for item in HTML_SOURCES:
    if len(item) == 4:
        name, url, tags, mode = item
        URL_MAP[name] = url
        BLOG_TAG_MAP[name] = tags
    else:
        print(f"⚠️ Warning: Skipping malformed HTML config: {item}")


MAX_RECIPES_PER_BLOG = 50 
cutoff_date = datetime.now().astimezone() - timedelta(days=360)

# --- KEYWORDS FOR AUTO TAGGING ---
WFPB_KEYWORDS = ['oil-free', 'oil free', 'no oil', 'wfpb', 'whole food', 'clean', 'refined sugar free', 'detox', 'healthy', 'salad', 'steamed']
EASY_KEYWORDS = ['easy', 'quick', 'simple', 'fast', '1-pot', 'one-pot', 'one pot', 'one bowl', 'one-bowl', '30-minute', 'minute', '15-minute', '20-minute', '5-ingredient', 'sheet pan', 'skillet', 'mug', 'blender', 'no-bake', 'raw','no bake','no-bake', 'air fryer']
BUDGET_KEYWORDS = ['budget', 'cheap', 'frugal', 'economical', 'pantry', 'low cost', 'money saving', '$', 'affordable', 'leftover', 'scraps', 'beans', 'rice', 'lentil', 'potato']
GF_KEYWORDS = ['gluten-free', 'gluten free', 'gf', 'wheat-free', 'flourless', 'almond flour', 'oat flour', 'rice flour']

# --- ADVANCED SCRAPER SETUP & SSL FIX ---

class LegacySSLAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        ctx = create_urllib3_context()
        ctx.load_default_certs()
        try:
            ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        except Exception:
            ctx.set_ciphers('DEFAULT')
        self.poolmanager = PoolManager(num_pools=connections, maxsize=maxsize, block=block, ssl_context=ctx)

scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True})
scraper.mount('https://', LegacySSLAdapter())

fallback_session = requests.Session()
fallback_session.mount('https://', LegacySSLAdapter())

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15'
]

def get_headers(referer=None):
    h = {'User-Agent': random.choice(USER_AGENTS)}
    if referer:
        h['Referer'] = referer
    return h

def get_auto_tags(title):
    tags = []
    t_lower = title.lower()
    if any(k in t_lower for k in WFPB_KEYWORDS): tags.append("WFPB")
    if any(k in t_lower for k in EASY_KEYWORDS): tags.append("Easy")
    if any(k in t_lower for k in BUDGET_KEYWORDS): tags.append("Budget")
    if any(k in t_lower for k in GF_KEYWORDS): tags.append("GF")
    return tags

def is_pet_recipe(title):
    t = title.lower()
    pet_phrases = ['dog treat', 'cat treat', 'dog biscuit', 'cat biscuit', 'dog food', 'cat food', 'pup treat', 'kitty treat', 'dog cookie']
    if any(phrase in t for phrase in pet_phrases): return True
    return False

def robust_fetch(url, is_binary=False, is_scraping_page=False):
    if is_scraping_page:
        time.sleep(random.uniform(2, 5)) 
    
    headers = get_headers(referer="https://www.google.com/")

    try:
        response = scraper.get(url, headers=headers, timeout=20)
        if response.status_code == 200:
            return response.content if is_binary else response.text
    except Exception as e:
        print(f"   [!] Cloudscraper error for {url}: {e}")
    
    try:
        fallback_session.headers.update(headers)
        response = fallback_session.get(url, timeout=15)
        if response.status_code == 200:
            return response.content if is_binary else response.text
    except Exception as e:
        print(f"   [!] Requests error for {url}: {e}")
        
    return None

def fetch_og_image(link):
    try:
        html = robust_fetch(link, is_scraping_page=True)
        if not html: return None
        soup = BeautifulSoup(html, 'lxml')
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'): return og_image['content']
        twitter_image = soup.find('meta', name='twitter:image')
        if twitter_image and twitter_image.get('content'): return twitter_image['content']
    except Exception:
        return None
    return None

def extract_image(entry, blog_name, link):
    image_candidate = None
    if 'media_content' in entry:
        for media in entry.media_content:
            if 'url' in media: return media['url']
    if 'media_thumbnail' in entry: 
        return entry.media_thumbnail[0]['url']
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
    if not image_candidate:
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

# --- HTML SCRAPING LOGIC ---

def scrape_html_feed(name, url, mode, existing_links, recipes_list, source_tags):
    print(f"   🔎 HTML Scraping: {name} (Mode: {mode})...")
    time.sleep(random.uniform(4, 7))
    
    html = robust_fetch(url, is_scraping_page=True)
    if not html:
        return [], "❌ Blocked/HTML Fail"
    
    soup = BeautifulSoup(html, 'lxml')
    found_items = []
    articles = []
    
    if mode == "wordpress":
        articles = soup.select("article")
        if not articles:
            articles = soup.select(".post, .type-post, .blog-entry")
            
    elif mode == "custom_pul":
        links = soup.find_all('a')
        for a in links:
            href = a.get('href', '')
            if '/recipe/' in href and href != '/recipe/':
                if a.find('img'):
                    articles.append(a)

    for art in articles:
        try:
            title = None
            link = None
            image = None
            date_obj = None
            
            if mode == "wordpress":
                title_tag = art.select_one(".entry-title a, .post-title a, h2 a, h3 a")
                if title_tag:
                    title = title_tag.get_text(strip=True)
                    link = title_tag['href']
                
                img_tag = art.select_one("img")
                if img_tag:
                    image = img_tag.get('data-src') or img_tag.get('data-lazy-src') or img_tag.get('src')
                    
                time_tag = art.select_one("time")
                if time_tag and time_tag.has_attr('datetime'):
                    try:
                        date_obj = parser.parse(time_tag['datetime'])
                    except: pass
                
            elif mode == "custom_pul":
                link = art.get('href')
                if link and not link.startswith('http'):
                    link = urljoin("https://www.pickuplimes.com", link)
                
                t_tag = art.select_one("h3, h2, .article_title") 
                if t_tag:
                    title = t_tag.get_text(strip=True)
                else:
                    divs = art.select("div")
                    for d in divs:
                        if len(d.get_text(strip=True)) > 10:
                            title = d.get_text(strip=True)
                            break
                            
                img_tag = art.find('img')
                if img_tag:
                    image = img_tag.get('src') or img_tag.get('data-src')

                date_obj = datetime.now() 

            if not title or not link: continue
            if is_pet_recipe(title): continue
            
            # --- SEPARATE ENTRY LOGIC ---
            # We treat (link, blog_name) as the unique key.
            # If "Rainbow Plant Life GF" is scraping a link that "Rainbow Plant Life" already has,
            # we allow it as a NEW entry because the blog_name is different.
            if (link, name) in existing_links:
                continue

            if not date_obj:
                date_obj = datetime.now() 
                
            if date_obj.tzinfo is None:
                date_obj = date_obj.replace(tzinfo=timezone.utc)
            else:
                date_obj = date_obj.astimezone(timezone.utc)

            if image and not image.startswith('http'):
                 image = urljoin(url, image) 
            
            if date_obj > cutoff_date:
                found_items.append({
                    "blog_name": name,
                    "title": title,
                    "link": link,
                    "image": image if image else "icon.jpg",
                    "date": date_obj.isoformat(),
                    "is_disruptor": False,
                    "special_tags": list(source_tags) # Initialize with source tags
                })
                existing_links.add((link, name))

        except Exception as e:
            continue
            
    status = f"✅ OK ({len(found_items)})" if found_items else "⚠️ Scraped 0"
    return found_items, status

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
recipes = [r for r in recipes if not (r['blog_name'] == "VegNews" and "/recipes/" not in r['link'])]

# Update existing_links to be tuples of (link, blog_name) to allow separate entries for GF blogs
existing_links = {(r['link'], r['blog_name']) for r in recipes}

feed_stats = {}
previous_domain = ""

print(f"Fetching recipes from {len(ALL_FEEDS)} RSS feeds & {len(HTML_SOURCES)} HTML sources...")

# 3. Scrape RSS Feeds
for item in ALL_FEEDS:
    # Safe unpacking to avoid crashes if bad data slipped in
    if len(item) != 3:
        continue
    name, url, special_tags = item

    new_count = 0
    status = "✅ OK"
    
    current_domain = urlparse(url).netloc
    if current_domain == previous_domain:
        print(f"   (Pausing 5s for same domain: {current_domain})")
        time.sleep(5)
    previous_domain = current_domain
    
    try:
        print(f"Checking RSS: {name}...")
        xml_content = robust_fetch(url, is_scraping_page=False)
        
        if (not xml_content) and name == "VegNews":
             xml_content = robust_fetch("https://vegnews.com/rss", is_scraping_page=False)

        if not xml_content:
            status = f"❌ Blocked/ConnErr"
            feed_stats[name] = {'new': 0, 'status': status}
            continue

        feed = feedparser.parse(xml_content)
        if not feed.entries:
            status = "⚠️ Parsed 0 items"
        
        for entry in feed.entries:
            try:
                if "vegnews.com" in entry.link and "/recipes/" not in entry.link: continue

                dt = entry.get('published', entry.get('updated', None))
                if not dt: continue
                try:
                    published_time = parser.parse(dt)
                except Exception: continue

                if published_time.tzinfo is None:
                    published_time = published_time.replace(tzinfo=timezone.utc)
                else:
                    published_time = published_time.astimezone(timezone.utc)
                
                if published_time > cutoff_date:
                    # Check Uniqueness using (link, name)
                    if (entry.link, name) not in existing_links:
                        if is_pet_recipe(entry.title): continue
                        image_url = extract_image(entry, name, entry.link)
                        if image_url and image_url.startswith('/'):
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
                        existing_links.add((entry.link, name))
                        new_count += 1
            except Exception as e:
                continue
        feed_stats[name] = {'new': new_count, 'status': status}

    except Exception as e:
        print(f"Failed to parse {name}: {e}")
        feed_stats[name] = {'new': 0, 'status': f"❌ Crash: {str(e)[:20]}"}

# 4. Scrape HTML Sources
print("\n--- STARTING HTML SCRAPING ---")
for item in HTML_SOURCES:
    if len(item) != 4:
        continue
    name, url, tags, mode = item
    
    try:
        # Pass 'recipes' list and current 'tags' (e.g. ['GF']).
        # Note: existing_links now handles (link, name) uniqueness inside the function.
        new_items, status = scrape_html_feed(name, url, mode, existing_links, recipes, tags)
        recipes.extend(new_items)
        feed_stats[name] = {'new': len(new_items), 'status': status}
    except Exception as e:
        print(f"   [!] Critical Error scraping {name}: {e}")
        feed_stats[name] = {'new': 0, 'status': "❌ HTML Crash"}

# 5. Backfill Tags (Including GF)
print("\nUpdating tags for all recipes...")
for recipe in recipes:
    bname = recipe['blog_name']
    
    current_tags = recipe.get('special_tags', []) 

    # 1. Base tags (from configuration)
    base_tags = list(BLOG_TAG_MAP.get(bname, []))
    
    # 2. Auto tags (WFPB, Easy, Budget, GF via Keywords)
    auto_tags = get_auto_tags(recipe['title'])
    
    # Merge Current + Base + Auto
    combined_tags = list(set(current_tags + base_tags + auto_tags))
    recipe['special_tags'] = combined_tags
    
# 6. Prune & Stats (Using Internal Names)
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
gf_counts = {}

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
    gf_counts[bname] = sum(1 for r in kept_recipes if "GF" in r['special_tags'])

final_pruned_list.sort(key=lambda x: x['date'], reverse=True)

# 7. Normalize Display Names (SKIPPED)
# We strictly keep the names distinct (e.g. "Rainbow Plant Life" vs "Rainbow Plant Life GF").
print("Pruning complete. Saving database with distinct source names...")

if len(final_pruned_list) > 50:
    with open('data.json', 'w') as f:
        json.dump(final_pruned_list, f, indent=2)
    generate_sitemap(final_pruned_list)
else:
    print("⚠️ SAFETY ALERT: Database too small (<50 items). Skipping write.")

# 8. Generate Report
with open('FEED_HEALTH.md', 'w') as f:
    f.write(f"# Feed Health Report\n")
    f.write(f"**Last Run:** {datetime.now().isoformat()}\n")

    total_new_today = sum(stats.get('new', 0) for stats in feed_stats.values())
    total_in_db = len(final_pruned_list)
    
    all_monitored_names = set(list(feed_stats.keys()) + list(total_counts.keys()))
    total_blogs_monitored = len(all_monitored_names)
    
    total_wfpb = sum(wfpb_counts.values())
    total_easy = sum(easy_counts.values())
    total_budget = sum(budget_counts.values())
    total_gf = sum(gf_counts.values())

    wfpb_percent = int((total_wfpb / total_in_db) * 100) if total_in_db > 0 else 0
    easy_percent = int((total_easy / total_in_db) * 100) if total_in_db > 0 else 0
    budget_percent = int((total_budget / total_in_db) * 100) if total_in_db > 0 else 0
    gf_percent = int((total_gf / total_in_db) * 100) if total_in_db > 0 else 0
    
    all_dates = [parser.parse(d) for d in latest_dates.values() if d != "N/A"]
    if all_dates:
        avg_date = datetime.fromtimestamp(sum(d.timestamp() for d in all_dates) / len(all_dates)).strftime('%Y-%m-%d')
    else:
        avg_date = "N/A"

    report_rows = []
    three_months_ago = datetime.now() - timedelta(days=90)
    stale_count = 0
    
    for name in all_monitored_names:
        url = URL_MAP.get(name, "Unknown")
        new = feed_stats.get(name, {}).get('new', 0)
        status = feed_stats.get(name, {}).get('status', 'Skipped/DB Only')
        total = total_counts.get(name, 0)
        latest = latest_dates.get(name, "N/A")
        
        if name in DISPLAY_NAME_MAP:
            name_display = f"{name} (-> {DISPLAY_NAME_MAP[name]})"
        else:
            name_display = name

        if latest != "N/A":
            try:
                latest_dt = parser.parse(latest)
                if latest_dt.replace(tzinfo=None) < three_months_ago.replace(tzinfo=None):
                    stale_count += 1
                    if "❌" not in status:
                        status = f"⚠️ Stale (>90d) {status.replace('✅ OK', '')}"
            except: pass
        
        if total == 0 and "✅" in status:
            status = "❌ No Recipes"
            
        report_rows.append((name_display, url, new, total, wfpb_counts.get(name,0), easy_counts.get(name,0), budget_counts.get(name,0), gf_counts.get(name,0), latest, status))

    f.write(f"**Total Blogs:** {total_blogs_monitored}\n")
    f.write(f"**Active Blogs (Last 90d):** {total_blogs_monitored - stale_count} / {total_blogs_monitored}\n")
    f.write(f"**Total Database Size:** {total_in_db}\n")
    f.write(f"**New Today:** {total_new_today}\n")
    f.write(f"**WFPB:** {total_wfpb} ({wfpb_percent}%)\n")
    f.write(f"**Easy:** {total_easy} ({easy_percent}%)\n")
    f.write(f"**Budget:** {total_budget} ({budget_percent}%)\n")
    f.write(f"**Gluten-Free:** {total_gf} ({gf_percent}%)\n")
    f.write(f"**Average Latest Post:** {avg_date}\n\n")

    f.write("| Blog Name | URL | New | Total | WFPB | Easy | Budget | GF | Latest | Status |\n")
    f.write("|-----------|-----|-----|-------|------|------|--------|----|--------|--------|\n")
    
    def sort_key(row):
        stat = row[9] 
        priority = 3 
        if '❌' in stat: priority = 0
        elif 'Stale' in stat: priority = 1
        elif '⚠️' in stat: priority = 2
        return (priority, row[0])

    report_rows.sort(key=sort_key)
    for row in report_rows:
        f.write(f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]} | {row[7]} | {row[8]} | {row[9]} |\n")

print(f"Successfully scraped. Database size: {len(final_pruned_list)}")
