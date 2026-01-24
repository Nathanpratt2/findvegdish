import feedparser
import json
import os
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dateutil import parser
import time

# --- CONFIGURATION ---
TOP_BLOGGERS = [
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
    ("Simple Vegan Blog", "https://simpleveganblog.com/feed/"),
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
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

def extract_image(entry):
    """
    Smarter extraction: checks for media tags, handles lazy loading, 
    and filters out tracking pixels/icons.
    """
    
    # 1. Try standard RSS media extensions (Highest Quality)
    if 'media_content' in entry:
        # Some feeds return a list, try to find the 'medium' or 'large' one
        for media in entry.media_content:
            if 'url' in media and ('image' in media.get('type', '') or 'jpg' in media.get('url', '')):
                return media['url']
    
    if 'media_thumbnail' in entry:
        return entry.media_thumbnail[0]['url']

    # 2. Parse HTML Content
    content = entry.get('content', [{}])[0].get('value', '') or entry.get('summary', '')
    
    if content:
        soup = BeautifulSoup(content, 'lxml')
        images = soup.find_all('img')
        
        for img in images:
            # Check for Lazy Loading attributes first
            src = img.get('data-src') or img.get('data-lazy-src') or img.get('data-original') or img.get('src')
            
            if not src:
                continue
            
            src_lower = src.lower()
            
            # FILTERS: Skip bad images
            # Skip generic icons, tracking pixels, and emojis
            if any(x in src_lower for x in ['pixel', 'emoji', 'icon', 'logo', 'badge', 'gravatar', 'gif', 'facebook', 'pinterest']):
                continue
                
            # Skip tiny images if width is specified in HTML
            width = img.get('width')
            if width and width.isdigit() and int(width) < 150:
                continue
            
            # If we made it here, it's likely a real recipe photo
            return src

    # 3. Fallback
    return "default.jpg"

print(f"Fetching recipes from {len(ALL_FEEDS)} blogs...")

for name, url in ALL_FEEDS:
    try:
        print(f"Checking {name}...")
        # Use custom agent to prevent 403 Forbidden errors
        feed = feedparser.parse(url, agent=USER_AGENT)
        
        for entry in feed.entries:
            try:
                # Handle dates safely
                published_time = parser.parse(entry.published if 'published' in entry else entry.updated)
                if published_time.tzinfo is None:
                    published_time = published_time.replace(tzinfo=datetime.now().astimezone().tzinfo)
            except:
                continue
            
            if published_time > cutoff_date:
                image_url = extract_image(entry)
                
                # Double check: If image URL is relative, make it absolute
                if image_url and image_url.startswith('/'):
                    # Simple fix for relative URLs (rare in RSS but happens)
                    base_url = feed.feed.get('link', '')
                    if base_url:
                        image_url = base_url.rstrip('/') + image_url
                
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
