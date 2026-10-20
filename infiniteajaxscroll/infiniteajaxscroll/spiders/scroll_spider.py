
import scrapy
import time

from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By


class ScrapingClubSpider(scrapy.Spider):
    name = "scroll"

    async def start(self):
        url = "https://infiniteajaxscroll.com/examples/articles/"
        yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        # Pobieramy obiekt przeglądarki Selenium
        driver = response.meta["driver"]

        znalezione = set()
        bez_zmian = 0

        for i in range(20):
            # Odczytaj tytuły aktualnie załadowanych artykułów
            articles = driver.find_elements(By.CSS_SELECTOR, ".article")

            for article in articles:
                headings = article.find_elements(
                    By.CSS_SELECTOR, "h1, h2, h3"
                )

                if headings:
                    title = headings[0].text.strip()

                    if title and title not in znalezione:
                        znalezione.add(title)
                        print(title)

            # Przewiń stronę na sam dół
            poprzednia_liczba = len(articles)
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )

            # Poczekaj, aż JavaScript doładuje kolejne artykuły
            time.sleep(2)

            nowa_liczba = len(
                driver.find_elements(By.CSS_SELECTOR, ".article")
            )

            if nowa_liczba > poprzednia_liczba:
                bez_zmian = 0
            else:
                bez_zmian += 1

            # Zakończ, jeśli przez kilka prób nie ma nowych artykułów
            if bez_zmian >= 3:
                break

        print(f"\nŁącznie znalezionych tytułów: {len(znalezione)}")
