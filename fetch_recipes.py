import feedparser
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dateutil import parser
import time
import os

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

# CHANGED: You can increase this to 120 or 365 if you want more history
cutoff_date = datetime.now().astimezone() - timedelta(days=360)

recipes = []
feed_stats = [] # To store the health report

# UPDATED: Headers to look exactly like a real Chrome Browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/'
}

def is_pet_recipe(title):
    t = title.lower()
    pet_phrases = [
        'dog treat', 'cat treat', 'dog biscuit', 'cat biscuit',
        'dog food', 'cat food', 'for dogs', 'for cats',
        'pup treat', 'kitty treat', 'dog cookie'
    ]
    if any(phrase in t for phrase in pet_phrases):
        return True
    return False

def fetch_og_image(link):
    try:
        time.sleep(0.5) 
        r = requests.get(link, headers=HEADERS, timeout=10) # Increased timeout
        soup = BeautifulSoup(r.content, 'lxml')
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            return og_image['content']
    except:
        return None
    return None

def extract_image(entry, blog_name):
    image_candidate = None

    if 'media_content' in entry:
        for media in entry.media_content:
            if 'url' in media:
                return media['url']
    
    if 'media_thumbnail' in entry:
        return entry.media_thumbnail[0]['url']

    content = entry.get('content', [{}])[0].get('value', '') or entry.get('summary', '')
    
    if content:
        soup = BeautifulSoup(content, 'lxml')
        images = soup.find_all('img')
        
        for img in images:
            src = (img.get('data-src') or img.get('data-lazy-src') or img.get('data-original') or img.get('src'))
            srcset = img.get('srcset') or img.get('data-srcset')
            if srcset:
                src = srcset.split(',')[0].split(' ')[0]

            if not src: continue
            
            src_lower = src.lower()
            if any(x in src_lower for x in ['pixel', 'emoji', 'icon', 'logo', 'gravatar', 'gif', 'facebook', 'pinterest', 'share']):
                continue
            
            width = img.get('width')
            if width and width.isdigit() and int(width) < 200:
                continue
            
            image_candidate = src
            break

    if not image_candidate:
        image_candidate = fetch_og_image(entry.link)

    return image_candidate if image_candidate else "default.jpg"

print(f"Fetching recipes from {len(ALL_FEEDS)} blogs...")

# --- MAIN LOOP ---
for name, url in ALL_FEEDS:
    blog_recipe_count = 0
    status = "✅ OK"
    
    try:
        print(f"Checking {name}...")
        # We use requests to get the feed content first, passing headers to fool filters
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        # If the blog blocks us, record it
        if response.status_code != 200:
            status = f"❌ Error {response.status_code}"
            feed_stats.append({"name": name, "count": 0, "status": status})
            continue

        feed = feedparser.parse(response.content)
        
        if not feed.entries:
            status = "⚠️ Empty Feed (Format changed?)"
        
        for entry in feed.entries:
            try:
                # Flexible date parsing
                dt = entry.get('published', entry.get('updated', None))
                if not dt: continue
                
                published_time = parser.parse(dt)
                if published_time.tzinfo is None:
                    published_time = published_time.replace(tzinfo=datetime.now().astimezone().tzinfo)
                
                if published_time > cutoff_date:
                    if is_pet_recipe(entry.title): continue

                    image_url = extract_image(entry, name)
                    
                    # Relative URL fix
                    if image_url and image_url.startswith('/'):
                        base = feed.feed.get('link', '')
                        if base: image_url = base.rstrip('/') + image_url
                    
                    recipes.append({
                        "blog_name": name,
                        "title": entry.title,
                        "link": entry.link,
                        "image": image_url,
                        "date": published_time.isoformat(),
                        "is_disruptor": name in [d[0] for d in DISRUPTORS]
                    })
                    blog_recipe_count += 1
            except Exception as e:
                continue
        
        feed_stats.append({"name": name, "count": blog_recipe_count, "status": status})

    except Exception as e:
        print(f"Failed to parse {name}: {e}")
        feed_stats.append({"name": name, "count": 0, "status": f"❌ Crash: {str(e)[:20]}"})

# Sort new -> old
recipes.sort(key=lambda x: x['date'], reverse=True)

# Save JSON
with open('data.json', 'w') as f:
    json.dump(recipes, f, indent=2)

# --- GENERATE REPORT (FEED_HEALTH.md) ---
with open('FEED_HEALTH.md', 'w') as f:
    f.write(f"# Feed Health Report\n")
    f.write(f"**Last Run:** {datetime.now().isoformat()}\n")
    f.write(f"**Total Recipes Fetched:** {len(recipes)}\n\n")
    f.write("| Blog Name | Recipes Found (360 Days) | Status |\n")
    f.write("|-----------|-------------------------|--------|\n")
    
    # Sort stats: Errors first, then Empty, then Success
    feed_stats.sort(key=lambda x: (x['status'] == '✅ OK', x['count']), reverse=False)
    
    for stat in feed_stats:
        f.write(f"| {stat['name']} | {stat['count']} | {stat['status']} |\n")

print(f"Successfully scraped {len(recipes)} recipes. Check FEED_HEALTH.md for errors.")
