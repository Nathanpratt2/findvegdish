import feedparser
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dateutil import parser
import time
import os

# --- CONFIGURATION ---
# Format: ("Blog Name", "Feed URL", ["SPECIAL_TAGS"])
# Tags can be "WFPB" for Whole Food Plant-Based or "Easy" for simple/quick recipes.
TOP_BLOGGERS = [
    ("Minimalist Baker", "https://minimalistbaker.com/recipes/vegan/feed/", ["Easy"]),
    ("Nora Cooks", "https://www.noracooks.com/feed/", []),
    ("PlantYou", "https://plantyou.com/feed/", ["WFPB", "Easy"]),
    ("The Korean Vegan", "https://thekoreanvegan.com/feed/", []),
    ("Rainbow Plant Life", "https://rainbowplantlife.com/feed/", []),
    ("Vegan Richa", "https://www.veganricha.com/feed/", []),
    ("It Doesn't Taste Like Chicken", "https://itdoesnttastelikechicken.com/feed/", []),
    ("Loving It Vegan", "https://lovingitvegan.com/feed/", []),
    ("Elavegan", "https://elavegan.com/feed/", []),
    ("Oh She Glows", "https://ohsheglows.com/feed/", []),
    ("The First Mess", "https://thefirstmess.com/feed/", []),
    ("Sweet Potato Soul", "https://sweetpotatosoul.com/feed/", []),
    ("Simple Vegan Blog", "https://simpleveganblog.com/feed/", ["Easy"]),
    ("Connoisseurus Veg", "https://www.connoisseurusveg.com/feed/", []),
    ("Jessica in the Kitchen", "https://jessicainthekitchen.com/feed/", []),
    ("Lazy Cat Kitchen", "https://www.lazycatkitchen.com/feed/", []),
    ("My Darling Vegan", "https://www.mydarlingvegan.com/feed/", []),
    ("The Burger Dude", "https://theeburgerdude.com/feed/", []),
    ("Hot for Food", "https://www.hotforfoodblog.com/feed/", []),
    ("The Vegan 8", "https://thevegan8.com/feed/", ["WFPB", "Easy"]),
    ("From My Bowl", "https://frommybowl.com/feed/", ["WFPB", "Easy"]),
    ("Rabbit and Wolves", "https://www.rabbitandwolves.com/feed/", []),
    ("Vegan Heaven", "https://veganheaven.org/feed/", []),
    ("The Hidden Veggies", "https://thehiddenveggies.com/feed/", []),
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
]

DISRUPTORS = [
    ("Full of Plants", "https://fullofplants.com/feed/", []),
    ("One Arab Vegan", "https://www.onearabvegan.com/feed/", []),
    ("Mary's Test Kitchen", "https://www.marystestkitchen.com/feed/", []),
    ("Unconventional Baker", "https://www.unconventionalbaker.com/feed/", []),
    ("Fragrant Vanilla Cake", "https://www.fragrantvanilla.com/feed/", []),
    ("Plantifully Based", "https://plantifullybasedblog.com/feed/", []),
    ("Nutriciously", "https://nutriciously.com/feed/", ["WFPB", "Easy"]),
    ("Cadry's Kitchen", "https://cadryskitchen.com/feed/", ["Easy"]),
    ("Veggies Don't Bite", "https://veggiesdontbite.com/feed/", ["WFPB"]),
    ("Watch Learn Eat", "https://watchlearneat.com/feed/", ["Easy"]),
    ("Strength and Sunshine", "https://strengthandsunshine.com/feed/", ["Easy"]),
    ("The Stingy Vegan", "https://thestingyvegan.com/feed/", ["Easy"]),
    ("Okonomi Kitchen", "https://okonomikitchen.com/feed/", []),
    ("The Foodie Takes Flight", "https://thefoodietakesflight.com/feed/", ["Easy"]),
    ("The Viet Vegan", "https://thevietvegan.com/feed/", []),
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
    ("My Pure Plants", "https://mypureplants.com/feed/", ["Easy"]),
    ("The Cheeky Chickpea", "https://thecheekychickpea.com/feed/", ["Easy"]),
    ("ZardyPlants", "https://zardyplants.com/feed/", ["WFPB"]),
]


ALL_FEEDS = TOP_BLOGGERS + DISRUPTORS
URL_MAP = dict((name, url) for name, url, tags in ALL_FEEDS)

MAX_RECIPES_PER_BLOG = 150 
cutoff_date = datetime.now().astimezone() - timedelta(days=360)

# --- LOAD EXISTING DATA ---
try:
    with open('data.json', 'r') as f:
        recipes = json.load(f)
        print(f"Loaded {len(recipes)} existing recipes.")
except (FileNotFoundError, json.JSONDecodeError):
    recipes = []
    print("No existing database found. Starting fresh.")

# --- CLEANSE DATABASE ---
initial_count = len(recipes)
recipes = [
    r for r in recipes 
    if not (r['blog_name'] == "VegNews" and "/recipes/" not in r['link'])
]

if len(recipes) < initial_count:
    print(f"Cleaned {initial_count - len(recipes)} items from database.")

existing_links = {r['link'] for r in recipes}

feed_stats = {} 

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/',
    'Upgrade-Insecure-Requests': '1'
}

def is_pet_recipe(title):
    t = title.lower()
    pet_phrases = ['dog treat', 'cat treat', 'dog biscuit', 'cat biscuit', 'dog food', 'cat food', 'pup treat', 'kitty treat', 'dog cookie']
    if any(phrase in t for phrase in pet_phrases): return True
    return False

def fetch_og_image(link):
    try:
        time.sleep(0.5) 
        r = requests.get(link, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.content, 'lxml')
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'): return og_image['content']
    except: return None
    return None

def extract_image(entry, blog_name):
    image_candidate = None
    if 'media_content' in entry:
        for media in entry.media_content:
            if 'url' in media: return media['url']
    if 'media_thumbnail' in entry: return entry.media_thumbnail[0]['url']
    content = entry.get('content', [{}])[0].get('value', '') or entry.get('summary', '')
    if content:
        soup = BeautifulSoup(content, 'lxml')
        images = soup.find_all('img')
        for img in images:
            src = (img.get('data-src') or img.get('data-lazy-src') or img.get('data-original') or img.get('src'))
            srcset = img.get('srcset') or img.get('data-srcset')
            if srcset: src = srcset.split(',')[0].split(' ')[0]
            if not src: continue
            src_lower = src.lower()
            if any(x in src_lower for x in ['pixel', 'emoji', 'icon', 'logo', 'gravatar', 'gif', 'facebook', 'pinterest', 'share']): continue
            width = img.get('width')
            if width and width.isdigit() and int(width) < 200: continue
            image_candidate = src
            break
    if not image_candidate: image_candidate = fetch_og_image(entry.link)
    return image_candidate if image_candidate else "icon.jpg"

print(f"Fetching recipes from {len(ALL_FEEDS)} blogs...")

# --- MAIN LOOP ---
# UPDATED: Loop now unpacks name, url, and the new tags list
for name, url, special_tags in ALL_FEEDS:
    new_count = 0
    status = "✅ OK"
    
    try:
        print(f"Checking {name}...")
        response = requests.get(url, headers=HEADERS, timeout=15)
        
        if response.status_code != 200 and name == "VegNews":
             response = requests.get("https://vegnews.com/rss", headers=HEADERS, timeout=15)

        if response.status_code != 200:
            status = f"❌ Error {response.status_code}"
            feed_stats[name] = {'new': 0, 'status': status}
            continue

        feed = feedparser.parse(response.content)
        
        if not feed.entries:
            if len(response.content) > 0: status = "⚠️ Parsed 0 items"
            else: status = "⚠️ Empty Feed"
        
        for entry in feed.entries:
            try:
                if name == "VegNews" and "/recipes/" not in entry.link: continue

                dt = entry.get('published', entry.get('updated', None))
                if not dt: continue
                published_time = parser.parse(dt)
                if published_time.tzinfo is None:
                    published_time = published_time.replace(tzinfo=datetime.now().astimezone().tzinfo)
                
                if published_time > cutoff_date:
                    if entry.link in existing_links: continue
                    if is_pet_recipe(entry.title): continue

                    image_url = extract_image(entry, name)
                    if image_url and image_url.startswith('/'):
                        base = feed.feed.get('link', '')
                        if base: image_url = base.rstrip('/') + image_url
                    
                    # UPDATED: New `special_tags` key added to the recipe object
                    recipes.append({
                        "blog_name": name,
                        "title": entry.title,
                        "link": entry.link,
                        "image": image_url,
                        "date": published_time.isoformat(),
                        "is_disruptor": name in [d[0] for d in DISRUPTORS],
                        "special_tags": special_tags 
                    })
                    existing_links.add(entry.link)
                    new_count += 1
            except Exception as e:
                continue
        
        feed_stats[name] = {'new': new_count, 'status': status}

    except Exception as e:
        print(f"Failed to parse {name}: {e}")
        feed_stats[name] = {'new': 0, 'status': f"❌ Crash: {str(e)[:20]}"}

# --- PRUNING STEP ---
print("Pruning database...")
recipes_by_blog = {}
for r in recipes:
    bname = r['blog_name']
    if bname not in recipes_by_blog: recipes_by_blog[bname] = []
    recipes_by_blog[bname].append(r)

final_pruned_list = []
total_counts = {} 
latest_dates = {} 

for bname, blog_recipes in recipes_by_blog.items():
    blog_recipes.sort(key=lambda x: x['date'], reverse=True)
    
    if len(blog_recipes) > 0:
        latest_dates[bname] = blog_recipes[0]['date'][:10] 
    
    kept_recipes = blog_recipes[:MAX_RECIPES_PER_BLOG]
    final_pruned_list.extend(kept_recipes)
    total_counts[bname] = len(kept_recipes)

final_pruned_list.sort(key=lambda x: x['date'], reverse=True)

with open('data.json', 'w') as f:
    json.dump(final_pruned_list, f, indent=2)

# --- GENERATE REPORT ---
with open('FEED_HEALTH.md', 'w') as f:
    f.write(f"# Feed Health Report\n")
    f.write(f"**Last Run:** {datetime.now().isoformat()}\n")
    f.write(f"**Total Database Size:** {len(final_pruned_list)}\n\n")
    f.write("| Blog Name | URL | New Today | Total in DB | Latest Post | Status |\n")
    f.write("|-----------|-----|-----------|-------------|-------------|--------|\n")
    
    all_names = set(list(feed_stats.keys()) + list(total_counts.keys()))
    
    report_rows = []
    for name in all_names:
        url = URL_MAP.get(name, "Unknown")
        new = feed_stats.get(name, {}).get('new', 0)
        status = feed_stats.get(name, {}).get('status', 'Skipped/DB Only')
        total = total_counts.get(name, 0)
        latest = latest_dates.get(name, "N/A")
        
        if total == 0 and "✅" in status:
            status = "❌ No Recipes"
            
        report_rows.append((name, url, new, total, latest, status))
    
    def sort_key(row):
        stat = row[5]
        priority = 2 
        if '❌' in stat: priority = 0
        elif '⚠️' in stat: priority = 1
        return (priority, row[0])

    report_rows.sort(key=sort_key)
    
    for row in report_rows:
        f.write(f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} |\n")

print(f"Successfully scraped. Database size: {len(final_pruned_list)}")
