# 🎬 IMDb Popular Movies Scraper

Um web scraper automatizado desenvolvido em Python para extrair dados dos **100 filmes mais populares** do IMDb. O projeto utiliza **Selenium** para lidar com o carregamento dinâmico e **Multithreading** para extrair detalhes dos filmes em alta velocidade.

## 🚀 Funcionalidades

* **Contorno de Anti-Bot:** Configurado com headers e flags para evitar detecção e bloqueio.
* **Infinite Scroll:** Utiliza Selenium para carregar a lista completa de filmes que exige interação do usuário.
* **Performance:** Uso de `ThreadPoolExecutor` para processar as páginas individuais dos filmes simultaneamente.
* **Exportação:** Salva os dados automaticamente em um arquivo `filmes_populares.csv`.

## 🛠️ Tecnologias Utilizadas

* [Python](https://www.python.org/)
* [Selenium](https://www.selenium.dev/)
* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
* [WebDriver Manager](https://pypi.org/project/webdriver-manager/)
* [Requests](https://requests.readthedocs.io/)

## 📋 Pré-requisitos

Antes de começar, você precisará ter o Python instalado e o navegador Google Chrome.

1. Instale as dependências:

```bash
pip install selenium webdriver-manager beautifulsoup4 requests

```

## 📂 Como usar

1. Clone este repositório:

```bash
git clone https://github.com/Lunes0/IMDb_Popular_Movies.git

```

2. Navegue até a pasta:

```bash
cd IMDb_Popular_Movies

```

3. Execute o script:

```bash
python PopularMoviesExtractor.py

```

## 📊 Saída de Dados

O script gera um arquivo `.csv` contendo:

* **Título** do filme
* **Nota**
* **Sinopse**
* **URL** do filme

---
