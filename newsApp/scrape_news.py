import requests
from django.core.files.base import ContentFile
from .models import News

from .scrape_individuals_world import *
from .scrape_individuals_local import *

# -------------------- Main Scrape Method -------------------
def scrape_method(generate_images=False):
    """
    Main scraping function that calls individual site scrapers,
    updates the database, downloads images, and optionally generates AI images.
    """
    # Clear old news
    News.objects.all().delete()

    all_headings = []
    message_map = {}

    # List of scraper functions with their news_type
    scraper_functions = [
        # World news scrapers
        (scrape_bbc, "world"),
        (scrape_nation, "local"),
        (scrape_star, "local"),
        (scrape_guardian, "world"),
        (scrape_nytimes, "world"),
        (scrape_washingtonpost, "world"),
        # (scrape_france24, "world"),
        # (scrape_bbc_pidgin, "world"),
        # (scrape_dw, "world"),
        # (scrape_apnews, "world"),
        # (scrape_euronews, "world"),
        # (scrape_cbsnews, "world"),
        # (scrape_nbcnews, "world"),
        # (scrape_foxnews, "world"),
        # (scrape_usatoday, "world"),
        # (scrape_wsj, "world"),
        # (scrape_bloomberg, "world"),
        # (scrape_aljazeera, "world"),

        # Local news scrapers
        (scrape_standard, "local"),
        (scrape_capitalfm, "local"),
        (scrape_kbc, "local"),
        (scrape_pd, "local"),
        (scrape_businessdaily, "local"),
        (scrape_eastafrican, "local"),
        (scrape_citizen, "local"),
        (scrape_ippmedia, "local"),
        (scrape_ghanaweb, "local"),
        (scrape_vanguard, "local"),
        (scrape_premiumtimes, "local"),
        (scrape_thisday, "local"),
    ]

    for scraper, news_type in scraper_functions:
        headings, bodies = scraper()  # each scraper returns (all_headings, message_map)

        for heading_text in headings:
            body_data = bodies.get(heading_text, "")

            # Extract body and image if structured as dict
            if isinstance(body_data, dict):
                body_text = body_data.get("body", "")
                image_url = body_data.get("image")
            else:
                body_text = body_data
                image_url = None

            # --- Database logic using update_or_create to avoid duplicates ---
            news_obj, created = News.objects.update_or_create(
                heading=heading_text,
                defaults={
                    "description": body_text,
                    "author": "news_hub_author",
                    "news_type": news_type,
                }
            )

            # Download and save image from scraping if available and not already saved
            if image_url and not news_obj.file:
                try:
                    resp = requests.get(image_url, timeout=20)
                    resp.raise_for_status()
                    filename = f"{heading_text[:50].replace(' ', '_')}.jpg"
                    news_obj.file.save(filename, ContentFile(resp.content), save=True)
                    print(f"✅ Image downloaded for '{heading_text}'")
                except Exception as e:
                    print(f"⚠️ Failed to download image for '{heading_text}': {e}")
                    # If download fails, fall back to AI generation
                    if generate_images:
                        from .ai_image_generator import AI_image_generation
                        AI_image_generation(news_obj)

            # AI image generation if no file exists
            elif generate_images and not news_obj.file:
                from .ai_image_generator import AI_image_generation
                AI_image_generation(news_obj)

            # Keep track for return
            if heading_text not in message_map:
                all_headings.append(heading_text)
                message_map[heading_text] = body_text
            else:
                if not message_map[heading_text] and body_text:
                    message_map[heading_text] = body_text

    return all_headings, message_map
