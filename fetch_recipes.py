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
    # The Titans: Established, high-authority sources. Love and Lemons cannot be used.
    ("Minimalist Baker", "https://minimalistbaker.com/recipes/vegan/feed/"),
    ("Nora Cooks", "https://www.noracooks.com/feed/"),
    ("PlantYou", "https://plantyou.com/feed/"),
    ("The Korean Vegan", "https://thekoreanvegan.com/feed/"),
    ("Rainbow Plant Life", "https://rainbowplantlife.com/feed/"),
    ("Vegan Richa", "https://www.veganricha.com/feed/"),
    ("It Doesn't Taste Like Chicken", "https://itdoesnttastelikechicken.com/feed/"),
    ("Loving It Vegan", "https://lovingitvegan.com/feed/"),
    ("Elavegan", "https://elavegan.com/feed/"),
    ("Oh She Glows", "https://ohsheglows.com/feed/"),
    ("The First Mess", "https://thefirstmess.com/feed/"),
    ("Sweet Potato Soul", "https://sweetpotatosoul.com/feed/"),
    ("Simple Vegan Blog", "https://simpleveganblog.com/feed/"),
    ("Connoisseurus Veg", "https://www.connoisseurusveg.com/feed/"),
    ("Jessica in the Kitchen", "https://jessicainthekitchen.com/feed/"),
    ("The Simple Veganista", "https://www.thesimpleveganista.com/feed/"),
    ("Lazy Cat Kitchen", "https://www.lazycatkitchen.com/feed/"),
    ("My Darling Vegan", "https://www.mydarlingvegan.com/feed/"),
    ("The Burger Dude", "https://theeburgerdude.com/feed/"),
    ("Hot for Food", "https://www.hotforfoodblog.com/feed/"),
    ("The Vegan 8", "https://thevegan8.com/feed/"),
    ("From My Bowl", "https://frommybowl.com/feed/"),
    ("Rabbit and Wolves", "https://www.rabbitandwolves.com/feed/"),
    ("Vegan Heaven", "https://veganheaven.org/feed/"),
    ("The Hidden Veggies", "https://thehiddenveggies.com/feed/"),
    ("Vegan in the Freezer", "https://veganinthefreezer.com/feed/"),
    ("A Virtual Vegan", "https://avirtualvegan.com/feed/"),
    ("Sarah's Vegan Kitchen", "https://sarahsvegankitchen.com/feed/"),
    ("Pick Up Limes", "https://www.pickuplimes.com/recipe/feed"), 
    ("Bianca Zapatka", "https://biancazapatka.com/en/feed/"),
    ("Holy Cow Vegan", "https://holycowvegan.net/feed/"),
    ("Six Vegan Sisters", "https://sixvegansisters.com/feed/"),
    ("Sweet Simple Vegan", "https://sweetsimplevegan.com/feed/"),
    ("Make It Dairy Free", "https://makeitdairyfree.com/feed/"),
    ("Addicted to Dates", "https://addictedtodates.com/category/recipes/feed/"),
    ("Gretchen's Vegan Bakery", "https://www.gretchensveganbakery.com/feed/"),
    ("Running on Real Food", "https://runningonrealfood.com/feed/"),
    ("The Full Helping", "https://thefullhelping.com/feed/"),
    ("Turnip Vegan", "https://turnipvegan.com/blogs/news.atom")
]

DISRUPTORS = [
    # The Specialists: Niche focus, cultural heritage, or unique constraints
    ("Zucker & Jagdwurst", "https://www.zuckerjagdwurst.com/en/feed"),
        ("Full of Plants", "https://fullofplants.com/feed/"),
        ("Good Eatings", "https://goodeatings.com/feed/"),
        ("My Berry Forest", "https://myberryforest.com/feed/"),
        ("The Green Creator", "https://thegreencreator.com/feed/"),
        ("Nordic Delicious", "https://nordicdelicious.com/feed/"),
        ("Earth of Maria", "https://earthofmaria.com/feed/"),
        ("Elephantastic Vegan", "https://www.elephantasticvegan.com/feed/"),
        ("One Arab Vegan", "https://www.onearabvegan.com/feed/"),
        ("Tuulia", "http://tuulia.co/feed/"),     ("Mary's Test Kitchen", "https://www.marystestkitchen.com/feed/"),
        ("Unconventional Baker", "https://www.unconventionalbaker.com/feed/"),
        ("86 Eats", "https://www.86eats.com/feed/"),
        ("The Gentle Chef", "https://thegentlechef.com/feed/"),
        ("Fragrant Vanilla Cake", "https://www.fragrantvanilla.com/feed/"),
        ("Wholehearted Eats", "https://www.wholeheartedeats.com/feed/"),
        ("Avocados and Ales", "https://avocadosandales.com/feed/"),
        ("Plantifully Based", "https://plantifullybasedblog.com/feed/"),
        ("Nutriciously", "https://nutriciously.com/feed/"),       ("Cadry's Kitchen", "https://cadryskitchen.com/feed/"),
    ("Vegan on Board", "https://veganonboard.com/feed/"),
    ("Veggies Don't Bite", "https://veggiesdontbite.com/feed/"),
    ("Watch Learn Eat", "https://watchlearneat.com/feed/"),
    ("Strength and Sunshine", "https://strengthandsunshine.com/feed/"),
    ("The Stingy Vegan", "https://thestingyvegan.com/feed/"),
    ("Okonomi Kitchen", "https://okonomikitchen.com/feed/"),
    ("The Foodie Takes Flight", "https://thefoodietakesflight.com/feed/"),
    ("The Viet Vegan", "https://thevietvegan.com/feed/"),
    ("Vegan Yack Attack", "https://veganyackattack.com/feed/"),
    ("Vegan Scratch Kitchen", "https://veganscratchkitchen.com/feed/"),
    ("The Conscious Plant Kitchen", "https://www.theconsciousplantkitchen.com/feed/"),
    ("Shane & Simple", "https://shaneandsimple.com/feed/"),
    ("Choosing Chia", "https://choosingchia.com/feed/"),
    ("Flora & Vino", "https://www.floraandvino.com/feed/"),
    ("Emilie Eats", "https://emilieeats.com/feed/"),
    ("Dianne's Vegan Kitchen", "https://diannesvegankitchen.com/feed/"),
    ("Namely Marly", "https://namelymarly.com/feed/"),
    ("The Post-Punk Kitchen", "https://www.theppk.com/feed/"),
    ("Veganosity", "https://veganosity.com/feed/"),
    ("Short Girl Tall Order", "https://shortgirltallorder.com/feed/"),
    ("Vegan Huggs", "https://veganhuggs.com/feed/"),
    ("The Little Blog of Vegan", "https://www.thelittleblogofvegan.com/feed/"),
    ("Eat Figs, Not Pigs", "https://www.eatfigsnotpigs.com/feed/"),
    ("The Banana Diaries", "https://thebananadiaries.com/feed/"),
    ("Project Vegan Baking", "https://projectveganbaking.com/feed/"),
    ("Vegan Punks", "https://veganpunks.com/feed/"),
    ("Plant Power Couple", "https://www.plantpowercouple.com/feed/"),
    ("Exceedingly Vegan", "https://www.exceedinglyvegan.com/feed"),
    ("Wallflower Kitchen", "https://wallflowerkitchen.com/feed/"),
    ("Rainbow Nourishments", "https://www.rainbownourishments.com/feed/"),
    ("Nutriciously", "https://nutriciously.com/feed/"),
    ("The Minimalist Vegan", "https://theminimalistvegan.com/feed/"),
    ("Monkey & Me Kitchen Adventures", "https://monkeyandmekitchenadventures.com/feed/"),
    ("Veggiekins", "https://veggiekinsblog.com/feed/"),
    ("This Rawsome Vegan Life", "https://www.thisrawsomeveganlife.com/feeds/posts/default"),
    ("Fried Dandelions", "https://frieddandelions.com/feed/"),
    ("My Pure Plants", "https://mypureplants.com/feed/"),
    ("The Cheeky Chickpea", "https://thecheekychickpea.com/feed/"),
    ("ZardyPlants", "https://zardyplants.com/feed/"),
    ("Veggie Rose", "https://veggierose.com/feed/"),
    ("Bo's Kitchen", "https://www.boskitchen.com/feed/"),
    ("Elephantastic Vegan", "https://www.elephantasticvegan.com/feed/"),
    ("V Nutrition", "https://www.vnutritionandwellness.com/feed/")
]

ALL_FEEDS = TOP_BLOGGERS + DISRUPTORS
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

# --- CLEANSE DATABASE (VegNews Fix) ---
# Remove existing VegNews items that do not have '/recipes/' in the URL
initial_count = len(recipes)
recipes = [r for r in recipes if not (r['blog_name'] == "VegNews" and "/recipes/" not in r['link'])]
if len(recipes) < initial_count:
    print(f"Cleaned {initial_count - len(recipes)} non-recipe VegNews articles from database.")

if len(recipes) < initial_count:
    print(f"Cleaned {initial_count - len(recipes)} Love and Lemons recipes from database.")

# Create set for deduplication
existing_links = {r['link'] for r in recipes}

feed_stats = {} # Dictionary for easy lookup: {'BlogName': {'new': 0, 'status': 'OK'}}

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
for name, url in ALL_FEEDS:
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
                # VegNews FILTER: Skip if not a recipe URL
                if name == "VegNews" and "/recipes/" not in entry.link:
                    continue

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
                    
                    recipes.append({
                        "blog_name": name,
                        "title": entry.title,
                        "link": entry.link,
                        "image": image_url,
                        "date": published_time.isoformat(),
                        "is_disruptor": name in [d[0] for d in DISRUPTORS]
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
total_counts = {} # For report

for bname, blog_recipes in recipes_by_blog.items():
    blog_recipes.sort(key=lambda x: x['date'], reverse=True)
    kept_recipes = blog_recipes[:MAX_RECIPES_PER_BLOG]
    final_pruned_list.extend(kept_recipes)
    total_counts[bname] = len(kept_recipes) # Track total for report

final_pruned_list.sort(key=lambda x: x['date'], reverse=True)

with open('data.json', 'w') as f:
    json.dump(final_pruned_list, f, indent=2)

# --- GENERATE REPORT ---
with open('FEED_HEALTH.md', 'w') as f:
    f.write(f"# Feed Health Report\n")
    f.write(f"**Last Run:** {datetime.now().isoformat()}\n")
    f.write(f"**Total Database Size:** {len(final_pruned_list)}\n\n")
    f.write("| Blog Name | New Today | Total in DB | Status |\n")
    f.write("|-----------|-----------|-------------|--------|\n")
    
    # Merge stats lists to handle blogs that might have failed today but exist in DB
    all_names = set(list(feed_stats.keys()) + list(total_counts.keys()))
    
    report_rows = []
    for name in all_names:
        new = feed_stats.get(name, {}).get('new', 0)
        status = feed_stats.get(name, {}).get('status', 'Skipped/DB Only')
        total = total_counts.get(name, 0)
        report_rows.append((name, new, total, status))
        
    # Sort by Status (Errors top), then Name
    report_rows.sort(key=lambda x: (x[3].startswith('✅'), x[0]))
    
    for row in report_rows:
        f.write(f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} |\n")

print("Done.")
