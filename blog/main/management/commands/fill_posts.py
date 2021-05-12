from django.core.management import BaseCommand
from main.models import Post


class Command(BaseCommand):
    def handle(self, *args, **options):
        from bs4 import BeautifulSoup
        import requests

        url = "https://doroshenkoaa.ru/med/"

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        links_list = []

        for link in soup.find_all("h2", "title", "a"):
            for tmp in link.find_all("a"):
                links_list.append(tmp.get("href"))

        for link in links_list:
            response = requests.get(link)
            soup = BeautifulSoup(response.text, "html.parser")

            article_title = soup.find("h1", {"itemprop": "headline"}).text.strip()
            article_content = ""
            for p in soup.find_all("div", {"itemprop": "articleBody"}, "p"):
                article_content += p.text

            Post(title=article_title, content=article_content).save()
