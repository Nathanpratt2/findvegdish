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
    ("Simple Vegan Blog", "https://simpleveganblog.com/feed/"),
    ("Vegan Richa", "https://www.veganricha.com/feed/"),
    ("It Doesn't Taste Like Chicken", "https://itdoesnttastelikechicken.com/feed/"),
    # Pick Up Limes REMOVED (No RSS)
    ("Sweet Potato Soul", "https://sweetpotatosoul.com/feed/"),
    ("Connoisseurus Veg", "https://www.connoisseurusveg.com/feed/"),
    ("VegNews", "https://vegnews.com/feed"), 
    ("Lazy Cat Kitchen", "https://www.lazycatkitchen.com/feed/"),
    ("The Full Helping", "https://thefullhelping.com/feed/"),
    ("Love and Lemons", "https://www.loveandlemons.com/feed/"),
    ("Minimalist Baker", "https://minimalistbaker.com/recipes/vegan/feed/"), 
    ("Nora Cooks", "https://www.noracooks.com/feed/"),
    ("Rainbow Plant Life", "https://rainbowplantlife.com/feed/"),
    ("Elavegan", "https://elavegan.com/feed/"),
    ("Running on Real Food", "https://runningonrealfood.com/feed/"),
    # Vegconomist REMOVED (Blocked)
    ("Namely Marly", "https://namelymarly.com/feed/"),
    ("The First Mess", "https://thefirstmess.com/feed/"),
    ("My Darling Vegan", "https://www.mydarlingvegan.com/feed/"),
    ("The Foodie Takes Flight", "https://thefoodietakesflight.com/feed/")
]

DISRUPTORS = [
    ("School Night Vegan", "https://schoolnightvegan.com/feed/"),
    ("The Korean Vegan", "https://thekoreanvegan.com/feed/"),
    ("The Burger Dude", "https://theeburgerdude.com/feed/"),
    ("FitGreenMind", "https://fit-green-mind.com/recipes/feed/"), 
    ("PlantYou", "https://plantyou.com/feed/"),
    ("Chez Jorge", "https://chejorge.com/feed/"),
    ("The Canadian African", "http://thecanadianafrican.com/feed/"), 
    ("Zacchary Bird", "https://zaccharybird.com/recipes/feed/") 
]

ALL_FEEDS = TOP_BLOGGERS + DISRUPTORS
MAX_RECIPES_PER_BLOG = 100  # <--- LIMIT SETTING

# Keeping 360 days of history check, but the 100 limit will override this if they post often
cutoff_date = datetime.now().astimezone() - timedelta(days=360)

# --- LOAD EXISTING DATA (ACCUMULATIVE MEMORY) ---
try:
    with open('data.json', 'r') as f:
        recipes = json.load(f)
        print(f"Loaded {len(recipes)} existing recipes from database.")
except (FileNotFoundError, json.JSONDecodeError):
    recipes = []
    print("No existing database found. Starting fresh.")

# Create a set of existing links to prevent duplicates
existing_links = {r['link'] for r in recipes}

feed_stats = [] 

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/',
    'Upgrade-Insecure-Requests': '1'
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
        r = requests.get(link, headers=HEADERS, timeout=10)
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
        response = requests.get(url, headers=HEADERS, timeout=15)
        
        if response.status_code != 200 and name == "VegNews":
             print("   -> Retrying VegNews with fallback RSS...")
             response = requests.get("https://vegnews.com/rss", headers=HEADERS, timeout=15)

        if response.status_code != 200:
            status = f"❌ Error {response.status_code}"
            feed_stats.append({"name": name, "count": 0, "status": status})
            continue

        feed = feedparser.parse(response.content)
        
        if not feed.entries:
            if len(response.content) > 0:
                 status = "⚠️ Parsed 0 items (Cloudflare?)"
            else:
                 status = "⚠️ Empty Feed"
        
        for entry in feed.entries:
            try:
                dt = entry.get('published', entry.get('updated', None))
                if not dt: continue
                
                published_time = parser.parse(dt)
                if published_time.tzinfo is None:
                    published_time = published_time.replace(tzinfo=datetime.now().astimezone().tzinfo)
                
                # Filter by date
                if published_time > cutoff_date:
                    # Deduplication Check
                    if entry.link in existing_links:
                        continue

                    if is_pet_recipe(entry.title): continue

                    image_url = extract_image(entry, name)
                    
                    if image_url and image_url.startswith('/'):
                        base = feed.feed.get('link', '')
                        if base: image_url = base.rstrip('/') + image_url
                    
                    new_recipe = {
                        "blog_name": name,
                        "title": entry.title,
                        "link": entry.link,
                        "image": image_url,
                        "date": published_time.isoformat(),
                        "is_disruptor": name in [d[0] for d in DISRUPTORS]
                    }
                    
                    recipes.append(new_recipe)
                    existing_links.add(entry.link) # Add to set to prevent duplicate in same run
                    blog_recipe_count += 1
            except Exception as e:
                continue
        
        feed_stats.append({"name": name, "count": blog_recipe_count, "status": status})

    except Exception as e:
        print(f"Failed to parse {name}: {e}")
        feed_stats.append({"name": name, "count": 0, "status": f"❌ Crash: {str(e)[:20]}"})


# --- PRUNING STEP: LIMIT 100 PER BLOG ---
print("Pruning database to max 100 recipes per blog...")

recipes_by_blog = {}
for r in recipes:
    bname = r['blog_name']
    if bname not in recipes_by_blog:
        recipes_by_blog[bname] = []
    recipes_by_blog[bname].append(r)

final_pruned_list = []

for bname, blog_recipes in recipes_by_blog.items():
    # Sort descending by date (newest first)
    blog_recipes.sort(key=lambda x: x['date'], reverse=True)
    
    # Keep only the top 100
    kept_recipes = blog_recipes[:MAX_RECIPES_PER_BLOG]
    final_pruned_list.extend(kept_recipes)
    
    if len(blog_recipes) > MAX_RECIPES_PER_BLOG:
        print(f"   Trimmed {bname}: Removed {len(blog_recipes) - MAX_RECIPES_PER_BLOG} old recipes.")

# Final Sort of the master list
final_pruned_list.sort(key=lambda x: x['date'], reverse=True)

# Save JSON
with open('data.json', 'w') as f:
    json.dump(final_pruned_list, f, indent=2)

# --- GENERATE REPORT (FEED_HEALTH.md) ---
with open('FEED_HEALTH.md', 'w') as f:
    f.write(f"# Feed Health Report\n")
    f.write(f"**Last Run:** {datetime.now().isoformat()}\n")
    f.write(f"**Total Database Size:** {len(final_pruned_list)}\n\n")
    f.write("| Blog Name | New Items Found Today | Status |\n")
    f.write("|-----------|-----------------------|--------|\n")
    
    feed_stats.sort(key=lambda x: (x['status'] == '✅ OK', x['count']), reverse=False)
    
    for stat in feed_stats:
        f.write(f"| {stat['name']} | {stat['count']} | {stat['status']} |\n")

print(f"Successfully scraped. Database size: {len(final_pruned_list)}")
