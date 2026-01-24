import feedparser
import json
import os
import requests
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

def extract_image(entry):
    """Attempts to find an image in the RSS entry or content."""
    # 1. Try media_content (standard RSS media extension)
    if 'media_content' in entry:
        return entry.media_content[0]['url']
    
    # 2. Try media_thumbnail
    if 'media_thumbnail' in entry:
        return entry.media_thumbnail[0]['url']
        
    # 3. Parse HTML content to find the first <img> tag
    content = entry.get('content', [{}])[0].get('value', '') or entry.get('summary', '')
    if content:
        soup = BeautifulSoup(content, 'lxml')
        img = soup.find('img')
        if img and img.get('src'):
            return img['src']
            
    # 4. Fallback: No image found
    return "default.jpg"

print(f"Fetching recipes from {len(ALL_FEEDS)} blogs...")

for name, url in ALL_FEEDS:
    try:
        print(f"Checking {name}...")
        feed = feedparser.parse(url)
        
        for entry in feed.entries:
            # Parse date safely
            try:
                published_time = parser.parse(entry.published if 'published' in entry else entry.updated)
                # Ensure timezone awareness for comparison
                if published_time.tzinfo is None:
                    published_time = published_time.replace(tzinfo=datetime.now().astimezone().tzinfo)
            except:
                continue # Skip if no valid date
            
            # Filter: Keep only last 2 months
            if published_time > cutoff_date:
                image_url = extract_image(entry)
                
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

# Sort by date (newest first)
recipes.sort(key=lambda x: x['date'], reverse=True)

# Save to JSON
with open('data.json', 'w') as f:
    json.dump(recipes, f, indent=2)

print(f"Successfully scraped {len(recipes)} recipes.")
