#!/usr/bin/env python3
import os
import sys
import io
import json
import urllib.request
import urllib.parse
from PIL import Image

DEST_DIR = "/home/manish/projects/nepalihangul/images/quiz"
os.makedirs(DEST_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "NepaliHangulEducationalApp/1.0 (contact@nepalihangul.local; Python urllib)"
}

TARGETS = [
    # Core 12 picture quiz words
    ("factory.webp", "modern industrial factory building exterior"),
    ("helmet.webp", "yellow construction safety hard hat"),
    ("water.webp", "glass of fresh drinking water on table"),
    ("rice.webp", "bowl of cooked white rice"),
    ("bus.webp", "city public transit passenger bus"),
    ("hospital.webp", "modern hospital medical center building"),
    ("money.webp", "korean won bank notes or currency coins"),
    ("machine.webp", "industrial metal lathe CNC manufacturing machine"),
    ("box.webp", "cardboard parcel shipping box"),
    ("truck.webp", "commercial logistics freight delivery cargo truck"),
    ("medicine.webp", "capsules tablets prescription medicine pills"),
    ("bag.webp", "school student backpack travel bag"),

    # Sejong 1A PDF Objects & Places
    ("desk.webp", "wooden office study writing desk"),
    ("chair.webp", "wooden office dining room chair"),
    ("clock.webp", "round modern wall clock watch"),
    ("phone.webp", "modern touchscreen smartphone cellphone"),
    ("pencil.webp", "wooden graphite yellow writing pencil"),
    ("computer.webp", "desktop personal computer monitor and keyboard"),
    ("hat.webp", "baseball cap headwear hat"),
    ("bank.webp", "commercial bank building entrance"),
    ("cafe.webp", "coffee shop cafe interior or storefront"),
    ("cinema.webp", "movie theater cinema screen and auditorium"),
    ("restaurant.webp", "dining restaurant tables with food"),
    ("classroom.webp", "school classroom desks and blackboard"),
    ("blackboard.webp", "school classroom chalk blackboard chalkboard"),
    ("photo.webp", "printed family photograph picture frame")
]

def search_commons_image(query):
    endpoint = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrnamespace": "6", # File namespace
        "gsrsearch": f"filetype:bitmap {query}",
        "gsrlimit": "6",
        "prop": "imageinfo",
        "iiprop": "url|mime|size|thumburl",
        "iiurlwidth": "800"
    }
    url = f"{endpoint}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            pages = data.get("query", {}).get("pages", {})
            for pid, page in pages.items():
                info = page.get("imageinfo", [{}])[0]
                mime = info.get("mime", "")
                if mime in ["image/jpeg", "image/png", "image/webp"]:
                    thumb = info.get("thumburl") or info.get("url")
                    if thumb:
                        return thumb
    except Exception as e:
        print(f"Error querying Commons for '{query}': {e}", file=sys.stderr)
    return None

def process_and_save(img_url, dest_path):
    req = urllib.request.Request(img_url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=12) as resp:
        img_bytes = resp.read()

    im = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    w, h = im.size
    min_dim = min(w, h)
    left = (w - min_dim) // 2
    top = (h - min_dim) // 2
    im_cropped = im.crop((left, top, left + min_dim, top + min_dim))
    im_resized = im_cropped.resize((512, 512), Image.Resampling.LANCZOS)
    im_resized.save(dest_path, "WEBP", quality=82)
    print(f"Saved: {os.path.basename(dest_path)} ({os.path.getsize(dest_path)//1024} KB)")

print(f"Fetching {len(TARGETS)} visual quiz & vocabulary images...")
success = 0
for filename, query in TARGETS:
    dest = os.path.join(DEST_DIR, filename)
    if os.path.exists(dest) and os.path.getsize(dest) > 2000:
        print(f"Already exists: {filename}")
        success += 1
        continue

    print(f"Searching for: {filename} ('{query}')...")
    img_url = search_commons_image(query)
    if img_url:
        try:
            process_and_save(img_url, dest)
            success += 1
        except Exception as e:
            print(f"Failed to process {filename}: {e}", file=sys.stderr)
    else:
        print(f"No image found for {filename}", file=sys.stderr)

print(f"Done! {success}/{len(TARGETS)} images ready in {DEST_DIR}")
