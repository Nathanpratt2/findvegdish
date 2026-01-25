import feedparser
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dateutil import parser
import time
import re

# --- CONFIGURATION ---
TOP_BLOGGERS = [
    ("Simple Vegan Blog", "http://feeds.feedburner.com/simpleveganblog"),
    ("Vegan Richa", "https://www.veganricha.com/feed/"),
    ("It Doesn't Taste Like Chicken", "https://itdoesnttastelikechicken.com/feed/"),
    ("Pick Up Limes", "https://www.pickuplimes.com/recipe/latest/rss"),
    ("Sweet Potato Soul", "https://sweetpotatosoul.com/feed/"),
    ("Connoisseurus Veg", "https://www.connoisseurusveg.com/feed/"),
    ("VegNews", "https://vegnews.com/feed"),
    ("Lazy Cat Kitchen", "https://www.lazycatkitchen.com/feed/"),
    ("The Full Helping", "https://thefullhelping.com/feed/"),
    ("Love and Lemons", "https://www.loveandlemons.com/feed/"),
    ("Minimalist Baker", "https://minimalistbaker.com/feed/"),
    ("Nora Cooks", "https://www.noracooks.com/feed/"),
    ("Rainbow Plant Life", "https://rainbowplantlife.com/feed/"),
    ("Elavegan", "https://elavegan.com/feed/"),
    ("Running on Real Food", "https://runningonrealfood.com/feed/"),
    ("Vegconomist", "https://vegconomist.com/feed/"),
    ("Namely Marly", "https://namelymarly.com/feed/"),
    ("The First Mess", "https://thefirstmess.com/feed/"),
    ("My Darling Vegan", "https://www.mydarlingvegan.com/feed/"),
    ("The Foodie Takes Flight", "https://thefoodietakesflight.com/feed/")
]

DISRUPTORS = [
    ("School Night Vegan", "https://schoolnightvegan.com/feed/"),
    ("The Korean Vegan", "https://thekoreanvegan.com/feed/"),
    ("The Burger Dude", "https://theeburgerdude.com/feed/"),
    ("FitGreenMind", "https://fit-green-mind.com/feed/"),
    ("PlantYou", "https://plantyou.com/feed/"),
    ("Chez Jorge", "https://chejorge.com/feed/"),
    ("The Canadian African", "https://thecanadianafrican.com/feed/"),
    ("Zacchary Bird", "https://zaccharybird.com/feed/")
]

ALL_FEEDS = TOP_BLOGGERS + DISRUPTORS
cutoff_date = datetime.now().astimezone() - timedelta(days=60)

recipes = []

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
}

def is_pet_recipe(title):
    """
    Returns True if the recipe is for pets (treats/food).
    Careful not to filter out 'Hot Dogs' or 'Copycat' recipes.
    """
    t = title.lower()
    
    # 1. Check for explicit pet phrase
    pet_phrases = [
        'dog treat', 'cat treat', 
        'dog biscuit', 'cat biscuit',
        'dog food', 'cat food',
        'for dogs', 'for cats',
        'pup treat', 'kitty treat',
        'dog cookie'
    ]
    
    if any(phrase in t for phrase in pet_phrases):
        return True
        
    return False

def fetch_og_image(link):
    """
    FALLBACK: Visits the actual page to find the 'og:image'.
    """
    try:
        time.sleep(0.5) 
        r = requests.get(link, headers=HEADERS, timeout=5)
        soup = BeautifulSoup(r.content, 'lxml')
        
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            return og_image['content']
            
    except Exception as e:
        return None
    return None

def extract_image(entry, blog_name):
    image_candidate = None

    # 1. Try standard RSS media extensions
    if 'media_content' in entry:
        for media in entry.media_content:
            if 'url' in media:
                return media['url']
    
    if 'media_thumbnail' in entry:
        return entry.media_thumbnail[0]['url']

    # 2. Parse HTML Content
    content = entry.get('content', [{}])[0].get('value', '') or entry.get('summary', '')
    
    if content:
        soup = BeautifulSoup(content, 'lxml')
        images = soup.find_all('img')
        
        for img in images:
            src = (img.get('data-src') or 
                   img.get('data-lazy-src') or 
                   img.get('data-original') or 
                   img.get('src'))
            
            srcset = img.get('srcset') or img.get('data-srcset')
            if srcset:
                src = srcset.split(',')[0].split(' ')[0]

            if not src:
                continue
            
            src_lower = src.lower()
            
            if any(x in src_lower for x in ['pixel', 'emoji', 'icon', 'logo', 'gravatar', 'gif', 'facebook', 'pinterest', 'share']):
                continue
            
            width = img.get('width')
            if width and width.isdigit() and int(width) < 200:
                continue
            
            image_candidate = src
            break

    # 3. Fallback to OG Image
    if not image_candidate:
        print(f"   -> No RSS image for {entry.title[:30]}... visiting page.")
        image_candidate = fetch_og_image(entry.link)

    return image_candidate if image_candidate else "default.jpg"

print(f"Fetching recipes from {len(ALL_FEEDS)} blogs...")

for name, url in ALL_FEEDS:
    try:
        print(f"Checking {name}...")
        feed = feedparser.parse(url, agent=HEADERS['User-Agent'])
        
        for entry in feed.entries:
            try:
                published_time = parser.parse(entry.published if 'published' in entry else entry.updated)
                if published_time.tzinfo is None:
                    published_time = published_time.replace(tzinfo=datetime.now().astimezone().tzinfo)
            except:
                continue
            
            if published_time > cutoff_date:
                # --- NEW FILTER CHECK ---
                if is_pet_recipe(entry.title):
                    print(f"   Skipping Pet Recipe: {entry.title}")
                    continue

                image_url = extract_image(entry, name)
                
                if image_url and image_url.startswith('/'):
                    base = feed.feed.get('link', '')
                    if base:
                        image_url = base.rstrip('/') + image_url
                
                recipes.append({
                    "blog_name": name,
                    "title": entry.title,
                    "link": entry.link,
                    "image": image_url,
                    "date": published_time.isoformat(),
                    "is_disruptor": name in [d[0] for d in DISRUPTORS]
                })
    except Exception as e:
        print(f"Failed to parse {name}: {e}")

recipes.sort(key=lambda x: x['date'], reverse=True)

with open('data.json', 'w') as f:
    json.dump(recipes, f, indent=2)

print(f"Successfully scraped {len(recipes)} recipes.")
