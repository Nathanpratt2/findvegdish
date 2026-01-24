import feedparser
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dateutil import parser
import time
import re

# --- CONFIGURATION ---
# Updated Simple Vegan Blog URL to FeedBurner (more reliable)
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
    ("PlantYou", "https://plantyou.com/feed/")
]

ALL_FEEDS = TOP_BLOGGERS + DISRUPTORS
cutoff_date = datetime.now().astimezone() - timedelta(days=60)

recipes = []

# Pretend to be a real browser to avoid blocks
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
}

def fetch_og_image(link):
    """
    FALLBACK: Visits the actual page to find the 'og:image' (Facebook share image).
    This is the most reliable method for stubborn sites.
    """
    try:
        # Respectful delay to not hammer servers
        time.sleep(0.5) 
        r = requests.get(link, headers=HEADERS, timeout=5)
        soup = BeautifulSoup(r.content, 'lxml')
        
        # Look for the Open Graph image tag
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            return og_image['content']
            
    except Exception as e:
        # Fail silently if page visit fails
        return None
    return None

def extract_image(entry, blog_name):
    """
    Attempts to find an image in the RSS entry. 
    If failing, calls fetch_og_image to look at the real page.
    """
    image_candidate = None

    # 1. Try standard RSS media extensions (Highest Quality)
    if 'media_content' in entry:
        for media in entry.media_content:
            if 'url' in media:
                return media['url']
    
    if 'media_thumbnail' in entry:
        return entry.media_thumbnail[0]['url']

    # 2. Parse HTML Content for <img> tags
    content = entry.get('content', [{}])[0].get('value', '') or entry.get('summary', '')
    
    if content:
        soup = BeautifulSoup(content, 'lxml')
        images = soup.find_all('img')
        
        for img in images:
            # Check all possible lazy load attributes
            src = (img.get('data-src') or 
                   img.get('data-lazy-src') or 
                   img.get('data-original') or 
                   img.get('src'))
            
            # Handle srcset (comma separated list of images)
            srcset = img.get('srcset') or img.get('data-srcset')
            if srcset:
                # Grab the first URL from the srcset list
                src = srcset.split(',')[0].split(' ')[0]

            if not src:
                continue
            
            src_lower = src.lower()
            
            # Filter out bad images
            if any(x in src_lower for x in ['pixel', 'emoji', 'icon', 'logo', 'gravatar', 'gif', 'facebook', 'pinterest', 'share']):
                continue
            
            # Skip tiny images
            width = img.get('width')
            if width and width.isdigit() and int(width) < 200:
                continue
            
            # Found a good candidate
            image_candidate = src
            break

    # 3. IF NO IMAGE FOUND IN RSS -> VISIT THE PAGE (The Nuclear Option)
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
                # Handle dates safely
                published_time = parser.parse(entry.published if 'published' in entry else entry.updated)
                if published_time.tzinfo is None:
                    published_time = published_time.replace(tzinfo=datetime.now().astimezone().tzinfo)
            except:
                continue
            
            if published_time > cutoff_date:
                image_url = extract_image(entry, name)
                
                # Fix relative URLs
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

# Sort new -> old
recipes.sort(key=lambda x: x['date'], reverse=True)

# Save
with open('data.json', 'w') as f:
    json.dump(recipes, f, indent=2)

print(f"Successfully scraped {len(recipes)} recipes.")
