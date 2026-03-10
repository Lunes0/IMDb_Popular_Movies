import requests
import time
import csv
import random
import concurrent.futures

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.5",
}

MAX_THREADS = 10


def get_100_movie_links():
    print("Iniciando navegador...")
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )

    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    url = "https://www.imdb.com/chart/moviemeter/"
    driver.get(url)

    time.sleep(5)

    for _ in range(5):
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(1)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    items = soup.find_all("li", class_="ipc-metadata-list-summary-item")

    links = []
    for item in items:
        a_tag = item.find("a", href=True)
        if a_tag and "/title/tt" in a_tag["href"]:
            link = "https://imdb.com" + a_tag["href"].split("?")[0]
            if link not in links:
                links.append(link)

    print(f"Sucesso! Encontrados {len(links)} links.")
    driver.quit()
    return links[:100]


def extract_movie_details(movie_link):
    try:
        time.sleep(random.uniform(0.3, 0.8))
        response = requests.get(movie_link, headers=headers, timeout=10)
        movie_soup = BeautifulSoup(response.content, "html.parser")

        title = movie_soup.find("span", attrs={"data-testid": "hero__primary-text"})
        title = title.get_text() if title else "N/A"

        rating_tag = movie_soup.find(
            "div", attrs={"data-testid": "hero-rating-bar__aggregate-rating__score"}
        )
        rating = rating_tag.find("span").get_text() if rating_tag else "N/A"

        plot_tag = movie_soup.find("span", attrs={"data-testid": "plot-xl"})
        plot_text = plot_tag.get_text().strip() if plot_tag else "N/A"

        print(f"Extraído: {title}")
        return [title, rating, plot_text, movie_link]
    except Exception as e:
        return None


def main():
    start_time = time.time()
    movie_links = get_100_movie_links()

    if not movie_links:
        print("Nenhum link encontrado.")
        return

    print(f"\nIniciando extração de detalhes de {len(movie_links)} filmes...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        results = list(executor.map(extract_movie_details, movie_links))

    with open("popular_movies.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Título", "Rating", "Sinopse", "Link"])
        for row in results:
            if row:
                writer.writerow(row)

    end_time = time.time()
    print(f"\n--- Sucesso! ---")
    print(f"Total de filmes salvos: {len([r for r in results if r])}")
    print(f"Tempo total: {end_time - start_time:.2f} segundos")


if __name__ == "__main__":
    main()
