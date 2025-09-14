from django.core.management.base import BaseCommand
from newsApp.scrape_news import scrape_method

class Command(BaseCommand):
    help = "Scrape news automatically and refresh the database"

    def handle(self, *args, **options):
        all_headings, _ = scrape_method(generate_images=False)
        self.stdout.write(self.style.SUCCESS(f"✅ Scraped {len(all_headings)} news items."))
