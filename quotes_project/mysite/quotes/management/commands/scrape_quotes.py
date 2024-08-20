import scrapy
from scrapy.crawler import CrawlerProcess
from django.core.management.base import BaseCommand
from quotes.models import Author, Quote
from quotes_scraper.quotes_scraper.spiders.quotes_spider import QuotesSpider
import json
import os



class Command(BaseCommand):
    help = 'Scrapes quotes from quotes.toscrape.com and loads them into the database.'

    def handle(self, *args, **kwargs):
        process = CrawlerProcess({
            'FEEDS': {
                'quotes.json': {'format': 'json'},
            },
            'ROBOTSTXT_OBEY': True,
        })

        process.crawl(QuotesSpider)
        process.start()

        self.load_data_into_db()

        self.stdout.write(self.style.SUCCESS('Quotes scraped and loaded into the database successfully!'))

    def load_data_into_db(self):
        with open('quotes.json', 'r') as f:
            data = json.load(f)

        for author_data in data['authors']:
            author, created = Author.objects.get_or_create(
                name=author_data['name'],
                defaults={
                    'bio': author_data.get('bio', ''),
                    'birth_date': author_data.get('birth_date', '')
                }
            )

        for quote_data in data['quotes']:
            author = Author.objects.get(name=quote_data['author'])
            Quote.objects.create(
                text=quote_data['text'],
                author=author,
                tags=quote_data.get('tags', [])
            )



print("Current working directory:", os.getcwd())