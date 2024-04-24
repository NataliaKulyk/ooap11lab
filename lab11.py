import asyncio
from bs4 import BeautifulSoup
from selenium import webdriver

# Клас, що представляє товар
class Product:
    def __init__(self, name, price, product_code):
        self.name = name
        self.price = price
        self.product_code = product_code

# Клас для парсингу інформації про товар з HTML
class ProductParser:
    def parse(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        # Знаходимо назву товару
        name_element = soup.find('h1', {'class': 'product__title-left'})
        if name_element is None:
            print(f"Error: Could not find product name")
            return None
        name = name_element.text.strip()

        # Знаходимо ціну товару
        price_element = soup.find('p', {'class': 'product-price__big'})
        if price_element is None:
            print(f"Error: Could not find product price")
            return None
        price = float(price_element.text.strip().replace('₴', '').replace(',', '').replace('\xa0', ''))

        # Знаходимо код товару
        product_code_element = soup.find('span', {'class': 'product__code-accent'})
        if product_code_element is None:
            print(f"Error: Could not find product code")
            return None
        product_code = product_code_element.text.strip().split()[-1]

        return Product(name, price, product_code)

# Асинхронна функція для завантаження сторінки товару та парсингу інформації
async def fetch_product(url):
    driver = webdriver.Chrome()  # Assuming you have Chrome WebDriver installed
    driver.get(url)
    html = driver.page_source
    driver.quit()

    parser = ProductParser()
    product = parser.parse(html)
    if product is not None:
        print(f'Product name: {product.name}')
        print(f'Product price: ₴{product.price:.2f}')
        print(f'Product code: {product.product_code}\n')

# Основна асинхронна функція
async def main():
    urls = [
        'https://hard.rozetka.com.ua/ua/logitech-910-006559/p393618522/',
        'https://hard.rozetka.com.ua/ua/apple-mmfk3ua-a/p364899384/'
    ]

    # Створюємо завдання для кожної URL-адреси товару та виконуємо їх паралельно
    tasks = [fetch_product(url) for url in urls]
    await asyncio.gather(*tasks)

# Виконання основної функції
if __name__ == '__main__':
    asyncio.run(main())
