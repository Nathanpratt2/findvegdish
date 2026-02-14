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
import shutil
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import create_urllib3_context
from requests.packages.urllib3.poolmanager import PoolManager

# Selenium Imports for robust fallback
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("⚠️ Selenium modules not found. Install 'selenium' and 'webdriver-manager' for better results.")

# --- CONFIGURATION ---
# Format: ("Blog Name", "Feed URL", ["SPECIAL_TAGS"])

TOP_BLOGGERS = [
    ("Minimalist Baker (Vegan Recipes)", "https://minimalistbaker.com/recipes/vegan/feed/", ["Easy"]),
    ("Nora Cooks", "https://www.noracooks.com/feed/", []),
    ("PlantYou", "https://plantyou.com/feed/", ["WFPB"]),
    ("The Korean Vegan", "https://thekoreanvegan.com/feed/", []),
    ("Rainbow Plant Life", "https://rainbowplantlife.com/feed/", []), # Main Feed
    ("Vegan Richa", "https://www.veganricha.com/feed/", []), # Main Feed
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
    ("From My Bowl", "https://frommybowl.com/feed/", []),
    ("Forks Over Knives", "https://www.forksoverknives.com/all-recipes/feed/", ["WFPB"]),
    ("Rabbit and Wolves", "https://www.rabbitandwolves.com/feed/", []),
    ("Vegan Heaven", "https://veganheaven.org/feed/", []),
    ("The Hidden Veggies", "https://thehiddenveggies.com/feed/", ["Budget"]), 
    ("Vegan in the Freezer", "https://veganinthefreezer.com/feed/", []),
    ("Bianca Zapatka", "https://biancazapatka.com/en/feed/", []),
    ("A Virtual Vegan", "https://avirtualvegan.com/feed/", []),
    ("Sarah's Vegan Kitchen", "https://sarahsvegankitchen.com/feed/", []),
    ("Make It Dairy Free", "https://makeitdairyfree.com/feed/", []),
    ("Addicted to Dates", "https://addictedtodates.com/category/recipes/feed/", []),
    ("Gretchen's Vegan Bakery", "https://www.gretchensveganbakery.com/feed/", []),
    ("Running on Real Food", "https://runningonrealfood.com/feed/", ["WFPB"]),
    ("Turnip Vegan", "https://turnipvegan.com/blogs/news.atom", []),
    ("VegNews", "https://vegnews.com/feed", []),
    ("HealthyGirl Kitchen", "https://healthygirlkitchen.com/feed/", []),
    ("Chef AJ", "https://chefaj.com/feed/", ["WFPB"]),
    ("Big Box Vegan", "https://bigboxvegan.com/category/recipes/feed/", []),
    ("The Plant-Based RD", "https://plantbasedrdblog.com/feed/", []),
    ("It's Liv B", "https://itslivb.com/feed/", []),
    ("NutritionFacts.org", "https://nutritionfacts.org/recipes/feed/", ["WFPB"])
]

DISRUPTORS = [
    ("Full of Plants", "https://fullofplants.com/feed/", []),
    ("One Arab Vegan", "https://www.onearabvegan.com/feed/", []),
    ("Mary's Test Kitchen", "https://www.marystestkitchen.com/feed/", []),
    ("Unconventional Baker", "https://www.unconventionalbaker.com/feed/", ["GF"]), # Will auto-tag GF
    ("Fragrant Vanilla Cake", "https://www.fragrantvanilla.com/feed/", []),
    ("Plantifully Based", "https://plantifullybasedblog.com/feed/", []),
    ("Cadry's Kitchen", "https://cadryskitchen.com/feed/", []),
    ("Dr. Vegan", "https://drveganblog.com/feed/", ["Easy"]),
    ("Picky Eater (Vegan Options)", "https://veggiesdontbite.com/feed/", []),
    ("Earth to Veg", "https://earthtoveg.com/feed/", []),
    ("Watch Learn Eat", "https://watchlearneat.com/feed/", ["Easy"]),
    ("Strength and Sunshine", "https://strengthandsunshine.com/feed/", ["Easy", "GF"]), # Will auto-tag GF
    ("The Stingy Vegan", "https://thestingyvegan.com/feed/", ["Easy", "Budget"]),
    ("The Foodie Takes Flight", "https://thefoodietakesflight.com/feed/", ["Easy"]),
    ("My Vegan Minimalist", "https://myveganminimalist.com/feed/", []),
    ("Messy Vegan Cook", "https://messyvegancook.com/feed/", []),
    ("The Conscious Plant Kitchen", "https://www.theconsciousplantkitchen.com/feed/", []),
    ("Choosing Chia (Vegan Recipes)", "https://choosingchia.com/category/diet%20/vegan/feed/", ["Easy"]),
    ("Flora & Vino", "https://www.floraandvino.com/feed/", ["WFPB"]),
    ("Namely Marly", "https://namelymarly.com/feed/", []),
    ("The Post-Punk Kitchen", "https://www.theppk.com/feed/", []),
    ("Plant Baes", "https://plantbaes.com/feed/", []),
    ("The Little Blog of Vegan", "https://www.thelittleblogofvegan.com/feed/", []),
    ("Eat Figs, Not Pigs", "https://www.eatfigsnotpigs.com/feed/", []),
    ("The Banana Diaries", "https://thebananadiaries.com/feed/", []),
    ("Plant Power Couple", "https://www.plantpowercouple.com/feed/", ["Easy"]),
    ("Rainbow Nourishments", "https://www.rainbownourishments.com/feed/", []),
    ("Rhian's Recipes", "https://www.rhiansrecipes.com/feed/", ["GF"]), # Will auto-tag GF
    ("Snixy Kitchen (Vegan Recipes)", "https://www.snixykitchen.com/special-diet/vegan/feed/", []),
    ("Monkey & Me Kitchen Adventures", "https://monkeyandmekitchenadventures.com/feed/", ["WFPB"]),
    ("My Goodness Kitchen", "https://mygoodnesskitchen.com/feed/", []),
    ("Ann Arbor Vegan Kitchen", "https://www.annarborvegankitchen.com/feed/", ["WFPB"]),
    ("Veggiekins", "https://veggiekinsblog.com/feed/", ["Easy","GF"]), # Will auto-tag GF
    ("ZardyPlants", "https://zardyplants.com/feed/", ["WFPB"]),
    ("Dreena Burton", "https://dreenaburton.com/feed/", ["WFPB"]),
    ("Holistic Chef Academy", "https://holisticchefacademy.com/feed/", []),
    ("Healthy Little Vittles", "https://healthylittlevittles.com/feed/", ["GF"]), # Will auto-tag GF
    ("Healthier Steps", "https://healthiersteps.com/feed/", [])
]

# --- DIRECT HTML SCRAPING SOURCES ---
HTML_SOURCES = [
    ("Pick Up Limes", "https://www.pickuplimes.com/recipe/", [], "custom_pul"),
    ("Zucker & Jagdwurst", "https://www.zuckerjagdwurst.com/en/archive/1", [], "custom_zj"),
    ("Rainbow Plant Life GF", "https://rainbowplantlife.com/diet/gluten-free/", ["GF"], "wordpress"),
    ("Vegan Richa GF", "https://www.veganricha.com/category/gluten-free/", ["GF"], "wordpress"),
    ("School Night Vegan", "https://schoolnightvegan.com/dinners/page/3/", [], "wordpress"), 
    ("Love and Lemons (Vegan Recipes)", "https://www.loveandlemons.com/category/recipes/vegan/", [], "wordpress"),
    ("Cookie and Kate (Vegan Recipes)", "https://cookieandkate.com/category/vegan-recipes/", [], "wordpress"), 
    ("The Loopy Whisk (Vegan Recipes)", "https://theloopywhisk.com/diet/vegan/", ["GF"], "wordpress"),
    ("Oh She Glows","https://www.ohsheglows.com/recipe-search/",[], "wordpress"),
    ("Zacchary Bird","https://www.zaccharybird.com/all-recipes/",[], "wordpress"),
    ("Elsa's Wholesome Life","https://www.elsaswholesomelife.com/blog?category=Recipes",[], "wordpress"),
    ("The Full Helping (Vegan Recipes)","https://www.thefullhelping.com/dietary/vegan/",[],"wordpress"),
    ("Hot For Food","https://www.hotforfoodblog.com/category/recipes/easy-recipes/page/3/",[],"wordpress"),
    ("Cupful of Kale", "https://cupfulofkale.com/category/recipes/page/4/", [], "wordpress"),
    ("The Veg Space", "https://www.thevegspace.co.uk/category/recipes/mains/page/3/", [], "wordpress"),
    ("Vegan Punks", "https://veganpunks.com/category/30-minutes/page/3/", [], "wordpress"),
    ("What Jew You Want to Eat", "https://whatjewwannaeat.com/category/vegan/", [], "wordpress"),
    ("Plant-Based on a Budget", "https://plantbasedonabudget.com/category/vegan-dinners/", ["Budget"], "wordpress"),
    ("Baking Hermann", "https://bakinghermann.com/recipes/", [], "custom_hermann"),
    ("Sweet Simple Vegan", "https://sweetsimplevegan.com/recipes/page/3/", [], "wordpress"),
    ("Gaz Oakley", "https://www.gazoakleychef.com/recipes/?sf_paged=4", [], "wordpress"),
    ("Vegan Huggs", "https://veganhuggs.com/recipes/", [], "wordpress"),
    ("The Edgy Veg", "https://www.theedgyveg.com/recipes/", [], "wordpress"),
    ("Vegan Yack Attack", "https://veganyackattack.com/entrees/", [], "wordpress"),
    ("Nadia's Healthy Kitchen (Vegan Recipes)", "https://nadiashealthykitchen.com/category/vegan/", [], "wordpress"),
    ("The Cheap Lazy Vegan", "https://thecheaplazyvegan.com/blog/", ["Budget", "Easy"], "wordpress"),
    ("Alison Roman (Vegan)", "https://www.alisoneroman.com/recipes/collections/vegan/page/5/", [], "wordpress"),
    ("Max La Manna", "https://www.maxlamanna.com/recipes", ["Low Waste"], "wordpress"),
    ("No Meat Disco", "https://www.nomeatdisco.com/recipes", [], "wordpress"),
    ("Chef Bai", "https://www.chefbai.kitchen/blog?offset=1710270365119", [], "wordpress")
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


MAX_RECIPES_PER_BLOG = 250 
cutoff_date = datetime.now().astimezone() - timedelta(days=360)

# --- KEYWORDS FOR AUTO TAGGING ---
WFPB_KEYWORDS = ['oil-free', 'oil free', 'no oil', 'wfpb', 'whole food', 'clean', 'refined sugar free', 'detox', 'healthy', 'salad', 'steamed']
EASY_KEYWORDS = ['easy', 'quick', 'simple', 'fast', '1-pot', 'one-pot', 'one pot', 'one bowl', 'one-bowl', '1 pan', 'one pan', '30-minute', 'minute', '15-minute', '20-minute', '5-ingredient', 'sheet pan', 'skillet', 'mug', 'blender', 'no-bake', 'raw','no bake','no-bake', 'air fryer']
BUDGET_KEYWORDS = ['budget', 'cheap', 'frugal', 'economical', 'pantry', 'low cost', 'money saving', '$', 'affordable', 'leftover', 'scraps', 'beans', 'rice', 'lentil', 'potato']
GF_KEYWORDS = ['gluten-free', 'gluten free', 'gf', 'wheat-free', 'flourless', 'almond flour', 'oat flour', 'rice flour']

# Words that usually indicate a recipe is NOT Gluten-Free (unless explicitly stated)
NON_GF_KEYWORDS = [
    'seitan', 'vital wheat gluten', 'wheat', 'barley', 'rye', 'couscous', 'farro', 
    'spelt', 'bulgur', 'semolina', 'sandwich', 'baguette', 'croissant', 'ciabatta', 
    'udon', 'beer', 'malt', 'burger bun', 'toast', 'sourdough']
    
NON_RECIPE_KEYWORDS = [
    "meal plan", "weekly menu", "menu plan", "gift guide", "cookbook", "review", 
    "giveaway", "roundup", "collection", "favorites", "best of", "kitchen tour", 
    "grocery haul", "what i eat", "routine", "travel", "restaurant", 
    "dining out", "interview", "guest post", "workshop", "class", "course", 
    "ebook", "merch", "store", "shop", "announcement", "update", "news", 
    "contest", "winner", "promo", "discount", "coupon", "deal", "top 10", 
    "top 20", "5 best", "10 best", "15 best", "20 best", "rpl", "going vegan", 
    "my story", "journey", "life lately", "coffee talk", "link love", 
    "weekend reading", "batch cooking", "staples", "essentials", "substitutes",
    "how to make", "101", "tutorial", "guide", "tips", "tricks", "faq",
    "policy", "terms", "privacy", "contact", "about", "search", "sitemap",
    "neighbor", "law", "videos", "planning", "rituals", "discontinued", 
    "forgotten", "finds", "live", "tests", "lab", "tracking", "progress", 
    "lifestyle", "success", "story", "obama", "trump", "stories", "appliances", 
    "books", "I met", "reading", "shows", "headshot", "just", "2026", "2025", "best seller"
]

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
# Mount to both protocols to handle redirects gracefully
scraper.mount('https://', LegacySSLAdapter())
scraper.mount('http://', LegacySSLAdapter())

fallback_session = requests.Session()
fallback_session.mount('https://', LegacySSLAdapter())
fallback_session.mount('http://', LegacySSLAdapter())
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

def fetch_with_selenium(url):
    """
    Last resort fetcher using Headless Chrome.
    Updated for 2026: Anti-detection, Eager Loading, and Explicit Waits.
    """
    if not SELENIUM_AVAILABLE:
        return None

    try:
        print(f"   [Selenium] Attempting fallback for {url}...")
        chrome_options = Options()
        
        # 1. Modern Headless Mode
        chrome_options.add_argument("--headless=new")
        
        # 2. Performance & Stability
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080") # Ensure desktop layout
        chrome_options.add_argument("--log-level=3")
        
        # 3. Anti-Detection / Stealth (Crucial for blocking evasion)
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        
        # 4. User Agent Rotation
        chrome_options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
        
        # 5. Page Load Strategy: 'eager' 
        # Waits for DOMContentLoaded (HTML+Scripts) but not all images/CSS. Much faster.
        chrome_options.page_load_strategy = 'eager'

        service = Service(ChromeDriverManager().install())
        driver = None
        
        try:
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Remove navigator.webdriver flag (Anti-detection)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            driver.set_page_load_timeout(30)
            
            driver.get(url)
            
            # 6. Explicit Wait logic instead of fixed sleep
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                time.sleep(2) 
            except Exception:
                pass 

            return driver.page_source
        except Exception as e:
            print(f"   [!] Selenium Driver Error: {str(e)[:100]}")
            return None
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
    except Exception as e:
        print(f"   [!] Selenium failed: {str(e)[:100]}")
    
    return None

def robust_fetch(url, is_binary=False, is_scraping_page=False):
    if is_scraping_page:
        time.sleep(random.uniform(2, 5)) 
    
    headers = get_headers(referer="https://www.google.com/")

    # 1. CloudScraper (Timeout 15s)
    try:
        response = scraper.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            return response.content if is_binary else response.text
    except Exception as e:
        print(f"   [!] Cloudscraper error for {url}: {str(e)[:50]}")
    
    # 2. Requests Fallback (Timeout 15s)
    try:
        fallback_session.headers.update(headers)
        response = fallback_session.get(url, timeout=15)
        if response.status_code == 200:
            return response.content if is_binary else response.text
    except Exception as e:
        print(f"   [!] Requests error for {url}: {str(e)[:50]}")

    # 3. Selenium Fallback (Only for text/HTML, not binary images)
    if not is_binary:
        return fetch_with_selenium(url)
        
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
    
    # 1. RSS Media Enclosures (Best source)
    if 'media_content' in entry:
        for media in entry.media_content:
            if 'url' in media: return media['url']
    if 'media_thumbnail' in entry: 
        return entry.media_thumbnail[0]['url']
        
    # 2. Parse HTML Content
    content = entry.get('content', [{}])[0].get('value', '') or entry.get('summary', '')
    if content:
        soup = BeautifulSoup(content, 'lxml')
        images = soup.find_all('img')
        
        for img in images:
            # Check for high-res source in srcset first
            srcset = img.get('srcset') or img.get('data-srcset')
            src = parse_srcset(srcset)
            
            # Fallback to standard attributes
            if not src:
                src = (img.get('data-src') or img.get('data-lazy-src') or img.get('data-original') or img.get('src'))
            
            if not src: continue
            
            # Filter out junk/placeholders
            src_lower = src.lower()
            if any(x in src_lower for x in ['pixel', 'emoji', 'icon', 'logo', 'gravatar', 'gif', 'facebook', 'pinterest', 'share', 'button', 'loader', 'placeholder', 'blank.jpg', '1x1']): 
                continue
                
            width = img.get('width')
            if width and width.isdigit() and int(width) < 200: continue
            
            image_candidate = src
            break
            
    # 3. Fallback to OpenGraph (Last resort)
    if not image_candidate or "placeholder" in str(image_candidate):
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

def generate_llms_txt(recipes):
    """Generates a robust llms.txt for AI/LLM indexing and GEO optimization."""
    count = len(recipes)
    sources_count = len(set(r['blog_name'] for r in recipes))
    last_updated = datetime.now().strftime("%Y-%m-%d")

    txt_content = f"""# Find Veg Dish (AI Context)

## Project Overview
FindVegDish.com is a curated, real-time aggregator of high-quality plant-based, vegan, and gluten-free recipes. It actively monitors {sources_count} distinct food blogs and chefs to provide a centralized feed of the latest vegan culinary content.

## Dataset Statistics
- **Total Recipes:** {count}
- **Last Updated:** {last_updated}
- **Content Types:** 100% Vegan. Includes Whole Food Plant Based (WFPB), Gluten-Free (GF), Budget-Friendly, and Easy/Quick recipes.

## Primary Sources
We aggregate content from verified sources including:
- Minimalist Baker
- Rainbow Plant Life
- Pick Up Limes
- Nora Cooks
- Vegan Richa
- And {sources_count - 5} others.

## Schema & Structure
Recipes are structured with:
- Title
- Source Blog Name
- Direct Link
- Thumbnail Image
- Published Date
- Special Tags (WFPB, GF, Easy, Budget)

## Access Points
- **Main Feed:** https://findvegdish.com/
- **Sitemap:** https://findvegdish.com/sitemap.xml
- **RSS Feed:** (Coming Soon)

## Usage
This file is intended to help Large Language Models (LLMs) understand the structure, freshness, and authority of the content on FindVegDish.com for better indexing and answer generation regarding vegan recipes.
"""
    with open('llms.txt', 'w') as f:
        f.write(txt_content)
    print("Generated robust llms.txt")

# --- HELPER FUNCTIONS FOR ROBUST HTML PARSING ---

def parse_srcset(srcset_str):
    """Parses a srcset string and returns the URL with the highest width."""
    if not srcset_str:
        return None
    
    candidates = []
    # Split by comma, handling potential commas in URLs is tricky but srcset standard helps
    parts = srcset_str.split(',')
    
    for p in parts:
        p = p.strip()
        if not p: continue
        
        # Split by space. Last part is usually width descriptor.
        subparts = p.split()
        if len(subparts) < 2:
             # Just a URL, assume width 0 or check if it's just a url
             if subparts: candidates.append((0, subparts[0]))
             continue
        
        url_part = subparts[0]
        width_part = subparts[-1]
        
        # Parse width
        width = 0
        if width_part.endswith('w'):
            try: width = int(width_part[:-1])
            except: pass
        elif width_part.endswith('x'):
            try: width = float(width_part[:-1]) * 1000 # Rough equivalent for density
            except: pass
            
        candidates.append((width, url_part))
        
    if not candidates: 
        return None
    
    # Sort by width desc
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][1]

def extract_metadata_from_page(url):
    """
    Fetches a specific recipe page to extract the precise date and high-res image.
    Used for new items that are missing data in the archive view.
    """
    html = robust_fetch(url, is_scraping_page=True)
    if not html: return None, None
    
    soup = BeautifulSoup(html, 'lxml')
    date_obj = None
    image_url = None

    # 1. Date Extraction
    # Strategy A: JSON-LD (Most reliable)
    scripts = soup.find_all('script', type='application/ld+json')
    for script in scripts:
        if not script.string: continue
        try:
            data = json.loads(script.string)
            nodes = []
            if isinstance(data, list): nodes = data
            elif isinstance(data, dict): nodes = data.get('@graph', [data])
            
            for node in nodes:
                # Look for Article or Recipe
                if node.get('@type') in ['Article', 'BlogPosting', 'Recipe', 'NewsArticle']:
                    dt = node.get('datePublished') or node.get('dateCreated')
                    if dt:
                        try:
                            date_obj = parser.parse(dt)
                            break
                        except: pass
            if date_obj: break
        except: continue

    # Strategy B: Meta Tags
    if not date_obj:
        meta_date = soup.find('meta', property='article:published_time') or \
                    soup.find('meta', property='og:updated_time') or \
                    soup.find('meta', itemprop='datePublished')
        if meta_date and meta_date.get('content'):
            try: date_obj = parser.parse(meta_date['content'])
            except: pass
            
    # Strategy C: Time Tags
    if not date_obj:
        time_tag = soup.find('time')
        if time_tag:
            dt_str = time_tag.get('datetime') or time_tag.get_text()
            try: date_obj = parser.parse(dt_str)
            except: pass

    # 2. Image Extraction (High Res)
    # OpenGraph is usually best for the main image
    og_img = soup.find('meta', property='og:image')
    if og_img and og_img.get('content'):
        image_url = og_img['content']
        
    return date_obj, image_url


# --- HTML SCRAPING LOGIC ---

def scrape_html_feed(name, url, mode, existing_links, recipes_list, source_tags):
    print(f"   🔎 HTML Scraping: {name} (Mode: {mode})...")
    time.sleep(random.uniform(5, 8)) # Safety delay
    
    html = robust_fetch(url, is_scraping_page=True)
    
    # --- BAKING HERMANN SPECIAL HANDLER ---
    # If standard fetch fails for Hermann, try a fallback session
    if mode == "custom_hermann" and not html:
        try:
            print(f"   [Combine] Trying insecure fetch for {url}...")
            # Use a fresh session with verification disabled (fixes Webflow/SSL issues)
            s = requests.Session()
            s.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            })
            r = s.get(url, timeout=20, verify=False)
            if r.status_code == 200:
                html = r.text
        except Exception as e:
            print(f"   [!] Hermann insecure fetch failed: {e}")

    if not html:
        return [], "❌ Blocked/HTML Fail"
    
    soup = BeautifulSoup(html, 'lxml')
    found_items = []
    
    # --- MODE 1: WORDPRESS / GENERIC AGGREGATION ---
    if mode == "wordpress":
        # 1. Scope to Main Content
        main_scope = soup.find('main') or \
                     soup.find(id='main') or \
                     soup.find(class_='site-main') or \
                     soup.find(id='content') or \
                     soup.find(class_='entry-content') or \
                     soup.find(class_='elementor-location-archive') or \
                     soup.find(class_='archive-container')
        
        if not main_scope: main_scope = soup

        # 2. Link Aggregation
        candidates = {} # URL -> {'title': str, 'image': str}

        all_links = main_scope.find_all('a', href=True)

        for a in all_links:
            raw_link = a['href']
            
            # Clean Link
            if any(x in raw_link for x in ['#', 'javascript:', 'mailto:', 'tel:', '/category/', '/tag/', '/author/', '/page/', '?share=', 'comment', '#comments']):
                continue
            
            full_link = urljoin(url, raw_link)
            if full_link.rstrip('/') == url.rstrip('/'): continue # Skip home link

            if full_link not in candidates:
                candidates[full_link] = {'title': '', 'image': None}

            # 2a. IMAGE EXTRACTION (Standard + Background)
            img = a.find('img')
            src = None
            
            if img:
                # 1. Try to get largest image from srcset
                srcset = img.get('srcset') or img.get('data-srcset')
                if srcset:
                    src = parse_srcset(srcset)
                
                # 2. Fallback to standard attributes if srcset failed
                if not src:
                    src = img.get('data-src') or img.get('data-lazy-src') or img.get('src')

            # Check for CSS Background Image (Fix for Zacchary Bird / Vegan Punks / Full Helping)
            if not src:
                style_source = a if a.has_attr('style') else a.find(style=True)
                if style_source and style_source.has_attr('style'):
                    style_str = style_source['style']
                    if 'background-image' in style_str and 'url(' in style_str:
                        try:
                            src = style_str.split('url(')[1].split(')')[0].strip('"').strip("'")
                        except: pass
            
            if src:
                # Clean up URL (remove query params for resizing if needed, though usually fine)
                candidates[full_link]['image'] = src

            # 2b. TITLE EXTRACTION
            link_text = a.get_text(" ", strip=True)
            h_child = a.find(['h2', 'h3', 'h4'])
            
            if h_child:
                candidates[full_link]['title'] = h_child.get_text(strip=True)
            elif len(link_text) > 10 and len(link_text) > len(candidates[full_link]['title']):
                # Filter utility links
                if not any(x == link_text.lower() for x in ['read more', 'continue reading', 'get the recipe', 'view recipe', 'cookie policy']):
                    candidates[full_link]['title'] = link_text

        # 3. Process Candidates
        for link_url, data in candidates.items():
            if not data['title']: continue
            
            t_low = data['title'].lower()
            if len(data['title']) < 5: continue
            if any(x in t_low for x in ['privacy policy', 'contact', 'about us', 'terms', 'accessibility', 'skip to content']): continue

            if (link_url, name) in existing_links: continue

            final_image = data['image']
            deep_date = None
            
            deep_date, deep_image = extract_metadata_from_page(link_url)
            
            if deep_image: 
                final_image = deep_image
            
            if not final_image: 
                continue

            final_date = deep_date if deep_date else datetime(2020, 1, 1).replace(tzinfo=timezone.utc)
            
            if final_image and not final_image.startswith('http'):
                final_image = urljoin(url, final_image)

            found_items.append({
                "blog_name": name,
                "title": data['title'],
                "link": link_url,
                "image": final_image,
                "date": final_date.isoformat(),
                "is_disruptor": False,
                "special_tags": list(source_tags)
            })
            existing_links.add((link_url, name))

    # --- MODE 2: CUSTOM PUL (Pick Up Limes) ---
    elif mode == "custom_pul":
        links = soup.find_all('a')
        for a in links:
            href = a.get('href', '')
            if '/recipe/' in href and href != '/recipe/':
                if a.find('img'):
                    link = urljoin("https://www.pickuplimes.com", href)
                    if (link, name) in existing_links: continue
                    t_tag = a.select_one("h3, h2, .article_title") 
                    title = t_tag.get_text(strip=True) if t_tag else "Recipe"
                    img_tag = a.find('img')
                    image = img_tag.get('src') if img_tag else "icon.jpg"
                    
                    # FIX: Force metadata extraction to get real date
                    deep_date, deep_image = extract_metadata_from_page(link)
                    if deep_image: image = deep_image
                    
                    # If date not found, use old date to prevent "new at top" issue
                    final_date = deep_date if deep_date else datetime(2022, 1, 1).replace(tzinfo=timezone.utc)

                    found_items.append({
                        "blog_name": name, "title": title, "link": link, "image": image,
                        "date": final_date.isoformat(), "is_disruptor": False, "special_tags": list(source_tags)
                    })
                    existing_links.add((link, name))

    # --- MODE 3: CUSTOM ZJ ---
    elif mode == "custom_zj":
        links = soup.select("a.post-item, .post-grid a, .archive-posts a") or soup.find_all('a', href=True)
        for a in links:
            href = a.get('href', '')
            if '/en/' in href and not any(x in href for x in ['/archive', '/page/', '/category/', '/about']):
                if a.find('img') or a.find(['h2', 'h3']):
                    link = urljoin(url, href)
                    if (link, name) in existing_links: continue
                    t_tag = a.select_one("h2, h3, .article-title")
                    title = t_tag.get_text(strip=True) if t_tag else "Recipe"
                    deep_date, deep_image = extract_metadata_from_page(link)
                    
                    found_items.append({
                        "blog_name": name, "title": title, "link": link, 
                        "image": deep_image if deep_image else "icon.jpg",
                        "date": deep_date.isoformat() if deep_date else datetime(2020,1,1).replace(tzinfo=timezone.utc).isoformat(),
                        "is_disruptor": False, "special_tags": list(source_tags)
                    })
                    existing_links.add((link, name))

    # --- MODE 4: CUSTOM HERMANN ---
    elif mode == "custom_hermann":
        # Baking Hermann (Robust Link Aggregation)
        candidates = soup.select(".w-dyn-item") + soup.find_all('a', href=True)
        processed_urls = set()
        
        for item in candidates:
            a_tag = item if item.name == 'a' else item.find('a', href=True)
            if not a_tag: continue
            
            href = a_tag['href']
            if '/recipes/' not in href or href.count('/') <= 2: continue
            
            link = urljoin("https://bakinghermann.com", href)
            if link in processed_urls or (link, name) in existing_links: continue
            processed_urls.add(link)

            title = "Recipe"
            t_elem = item.select_one("h3, h2, h4") if item.name != 'a' else None
            if t_elem: title = t_elem.get_text(strip=True)
            elif a_tag.find('img') and a_tag.find('img').get('alt'): title = a_tag.find('img')['alt']
            elif item.get_text(strip=True): title = item.get_text(strip=True)
            
            # Deep Fetch is mandatory for Hermann (using extraction logic)
            # We use the standard function, but it might fail if blocking continues.
            # However, extract_metadata relies on robust_fetch which we can't easily patch here without code duplication.
            # But the main loop getting 'html' passed, so we hope article pages are less protected or robust_fetch works occasionally.
            
            # To be safe, we will rely on extract_metadata_from_page but if it returns nothing, we just set a default.
            deep_date, deep_image = extract_metadata_from_page(link)
            
            # If standard extract failed, try our custom insecure fetch if needed
            if not deep_image:
                 # Minimal fallback attempt
                 try:
                    s = requests.Session()
                    r = s.get(link, headers={'User-Agent': 'Mozilla/5.0'}, verify=False, timeout=10)
                    if r.status_code == 200:
                        s2 = BeautifulSoup(r.text, 'lxml')
                        og = s2.find('meta', property='og:image')
                        if og: deep_image = og['content']
                        # Date
                        ld = s2.find('script', type='application/ld+json')
                        if ld and ld.string:
                             if '"datePublished":' in ld.string:
                                 # simple parse
                                 pass 
                 except: pass

            if deep_image:
                found_items.append({
                    "blog_name": name, "title": title, "link": link, "image": deep_image,
                    "date": deep_date.isoformat() if deep_date else datetime(2020,1,1).replace(tzinfo=timezone.utc).isoformat(),
                    "is_disruptor": False, "special_tags": list(source_tags)
                })
                existing_links.add((link, name))

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
    if len(item) != 3: continue
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
                
                # SAFETY: Prevent future dates (typos or timezone glitches)
                # Allow a small buffer (24h) for timezone differences, but discard obvious bad years
                now_utc = datetime.now(timezone.utc)
                if published_time > now_utc + timedelta(days=1):
                    # If date is way in the future, assume it's a mistake or sticky post; use Now
                    published_time = now_utc

                if published_time > cutoff_date:
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
    if len(item) != 4: continue
    name, url, tags, mode = item
    
    time.sleep(random.uniform(2, 7))

    try:
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
    base_tags = list(BLOG_TAG_MAP.get(bname, []))
    auto_tags = get_auto_tags(recipe['title'])
    combined_tags = list(set(current_tags + base_tags + auto_tags))
    
    # SAFETY: Remove GF tag if title contains obvious gluten words (unless explicitly marked GF in title)
    if "GF" in combined_tags:
        t_lower = recipe['title'].lower()
        # If it has a bad word (like 'seitan' or 'sandwich')...
        if any(kw in t_lower for kw in NON_GF_KEYWORDS):
            # ...and DOESN'T explicitly say "gluten free" or "gf" in the title...
            if not any(safe in t_lower for safe in GF_KEYWORDS):
                combined_tags.remove("GF")

    recipe['special_tags'] = combined_tags

# 5.5 Global Non-Recipe Filter
print("Running global non-recipe filter...")
non_recipes_removed_count = 0
valid_recipes = []

for r in recipes:
    title_lower = r['title'].lower()
    is_spam = False
    for kw in NON_RECIPE_KEYWORDS:
        if kw in title_lower:
            is_spam = True
            break
    
    if is_spam:
        non_recipes_removed_count += 1
    else:
        valid_recipes.append(r)

recipes = valid_recipes
print(f"   Removed {non_recipes_removed_count} non-recipe items.")
    
# 6. Prune & Stats
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

# --- GLOBAL DEDUPLICATION ---
print("   Running global deduplication (Rules: Title Match -> GF source > Older date)...")
deduped_recipes = {}
for recipe in final_pruned_list:
    title = recipe['title']
    
    if title not in deduped_recipes:
        deduped_recipes[title] = recipe
    else:
        existing = deduped_recipes[title]
        curr_is_gf = "GF" in recipe['blog_name']
        exist_is_gf = "GF" in existing['blog_name']
        
        if curr_is_gf and not exist_is_gf:
            deduped_recipes[title] = recipe
        elif exist_is_gf and not curr_is_gf:
            pass 
        else:
            if recipe['date'] < existing['date']:
                deduped_recipes[title] = recipe

final_pruned_list = list(deduped_recipes.values())
final_pruned_list.sort(key=lambda x: x['date'], reverse=True)

print("Pruning complete. Saving database with distinct source names...")

if len(final_pruned_list) > 50:
    # 1. Write to temp file first (Atomic Write Pattern)
    temp_file = "data.tmp.json"
    final_file = "data.json"
    
    try:
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(final_pruned_list, f, indent=2)
        
        # 2. Rename/Move only if write was successful
        # os.replace is atomic on POSIX, acts like move on Windows
        os.replace(temp_file, final_file)
        print(f"✅ Successfully wrote {len(final_pruned_list)} items to {final_file}")
        
        generate_sitemap(final_pruned_list)
        generate_llms_txt(final_pruned_list)
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR writing database: {e}")
        # Attempt cleanup of temp file
        if os.path.exists(temp_file):
            os.remove(temp_file)
else:
    print("⚠️ SAFETY ALERT: Database too small (<50 items). Skipping write to prevent data loss.")

# 8. Generate Report
with open('FEED_HEALTH.md', 'w', encoding='utf-8') as f:
    f.write(f"# Feed Health Report\n")
    f.write(f"**Last Run:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

    # --- CALCULATE STATS ---
    total_new_today = sum(stats.get('new', 0) for stats in feed_stats.values())
    total_in_db = len(final_pruned_list)
    all_monitored_names = set(list(feed_stats.keys()) + list(total_counts.keys()))
    total_blogs_monitored = len(all_monitored_names)
    
    active_sources_count = sum(1 for count in total_counts.values() if count >= 5)
    
    total_wfpb = sum(wfpb_counts.values())
    total_easy = sum(easy_counts.values())
    total_budget = sum(budget_counts.values())
    total_gf = sum(gf_counts.values())

    wfpb_percent = int((total_wfpb / total_in_db) * 100) if total_in_db > 0 else 0
    easy_percent = int((total_easy / total_in_db) * 100) if total_in_db > 0 else 0
    budget_percent = int((total_budget / total_in_db) * 100) if total_in_db > 0 else 0
    gf_percent = int((total_gf / total_in_db) * 100) if total_in_db > 0 else 0
    
    all_dates = [parser.parse(d) for d in latest_dates.values() if d != "N/A"]
    avg_date = datetime.fromtimestamp(sum(d.timestamp() for d in all_dates) / len(all_dates)).strftime('%Y-%m-%d') if all_dates else "N/A"

    # --- WRITE SUMMARY TABLE ---
    f.write("### 📊 System Summary\n")
    f.write("| Metric | Value | Breakdown |\n")
    f.write("| :--- | :--- | :--- |\n")
    f.write(f"| **Total Database** | {total_in_db} | {total_new_today} new today |\n")
    f.write(f"| **Blogs Monitored** | {total_blogs_monitored} | {len(HTML_SOURCES)} HTML / {len(ALL_FEEDS)} RSS |\n")
    f.write(f"| **Active Sources** | {active_sources_count} | 5+ recipes |\n")
    f.write(f"| **WFPB / GF** | {total_wfpb} / {total_gf} | {wfpb_percent}% / {gf_percent}% |\n")
    f.write(f"| **Easy / Budget** | {total_easy} / {total_budget} | {easy_percent}% / {budget_percent}% |\n\n")

    f.write("---\n\n")
    f.write("### 📋 Detailed Blog Status (Sorted: 0 Recipes First)\n")
    
    # --- CSS FOR CLEAN LAYOUT ---
    f.write("""
<style>
  .report-container { height: 600px; overflow-y: auto; border: 1px solid #ddd; border-radius: 8px; margin-top: 10px; }
  #statusTable { border-collapse: collapse; width: 100%; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
  #statusTable th { position: sticky; top: 0; background-color: #f8f9fa; border-bottom: 2px solid #dee2e6; padding: 12px 8px; text-align: left; font-size: 13px; z-index: 10; }
  #statusTable td { padding: 10px 8px; border-bottom: 1px solid #eee; font-size: 13px; }
  #statusTable tr:hover { background-color: #f1f3f5; }
  .status-badge { padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: bold; }
</style>
<div class="report-container">
<table id="statusTable">
<thead>
<tr>
 <th>Blog Name</th>
 <th>New</th>
 <th>Total</th>
 <th>WFPB</th>
 <th>Easy</th>
 <th>Budg</th>
 <th>GF</th>
 <th>Latest</th>
 <th>Status</th>
</tr>
</thead>
<tbody>
""")
    
    report_rows = []
    for name in all_monitored_names:
        new = feed_stats.get(name, {}).get('new', 0)
        status = feed_stats.get(name, {}).get('status', 'Skipped')
        total = total_counts.get(name, 0)
        latest = latest_dates.get(name, "N/A")
        
        # Normalize status
        if "Scraped 0" in status or "Parsed 0 items" in status:
            status = "✅ OK" if total > 0 else "❌ Empty"
        
        report_rows.append({
            "name": name, "new": new, "total": total,
            "wfpb": wfpb_counts.get(name, 0), "easy": easy_counts.get(name, 0),
            "budget": budget_counts.get(name, 0), "gf": gf_counts.get(name, 0),
            "latest": latest, "status": status
        })

    # --- CRITICAL: SORT BY TOTAL (0 FIRST), THEN BY NAME ---
    report_rows.sort(key=lambda r: (r['total'], r['name']))

    for r in report_rows:
        # Simple color for status
        status_color = "#28a745" if "✅" in r['status'] else "#dc3545" if "❌" in r['status'] else "#ffc107"
        f.write(f"<tr>"
                f"<td><strong>{r['name']}</strong></td>"
                f"<td>{r['new']}</td>"
                f"<td>{r['total']}</td>"
                f"<td>{r['wfpb']}</td>"
                f"<td>{r['easy']}</td>"
                f"<td>{r['budget']}</td>"
                f"<td>{r['gf']}</td>"
                f"<td>{r['latest']}</td>"
                f"<td><span style='color:{status_color}'>{r['status']}</span></td>"
                f"</tr>\n")

    f.write('</tbody></table></div>\n\n')
    f.write("---\n*Report generated automatically by FindVegDish Fetcher.*")
    # --- END SCROLLABLE CONTAINER ---

    f.write("---\n*Report generated automatically by FindVegDish Fetcher.*")

print(f"Successfully generated FEED_HEALTH.md with scrollable table. Database size: {len(final_pruned_list)}")
