import asyncio
import time
from urllib.parse import urljoin

from ctypes import Page, OrderData
from downloader import Downloader
from parser import Parser
from config import logger


class Scraper:

    def __init__(self, host: str, main_page_path: str):
        self._host: str = host
        self.main_page = Page(urljoin(self._host, main_page_path), params={'start': 0})
        self._url: str = urljoin(self._host, main_page_path)
        self._downloader = Downloader()
        self._parser = Parser()

    async def _get_pages_from_pagination(self) -> list[Page]:
        """Получает данные  из пагинации"""
        page_html = await self._downloader.download_html_from_url(self.main_page)
        pages_wrap_list = await self._parser.parse_pagination(page_html)
        pages_list = [Page(self.main_page.url, params={'start': item}) for item in pages_wrap_list] if pages_wrap_list else None
        return pages_list

    async def _get_orders_pages(self, page: Page) -> list[Page]:
        """Получает список адресов карточек заказов"""
        page_html = await self._downloader.download_html_from_url(page)
        orders_pages_wrap_list = await self._parser.parse_items_list(page_html)
        orders_pages_list = [Page(urljoin(self._host, path)) for path in orders_pages_wrap_list]
        return orders_pages_list

    async def _get_orders_data(self, pages: list[Page]):
        """Получает данные заказов с одной страницы"""
        orders = list()
        pages_html_list = await self._downloader.download_html_from_url_list(pages)
        for page_html in pages_html_list:
            orders.append(await self._parser.parse_item_data(page_html))
        return orders

    async def get_data(self) -> list[OrderData]:
        """Получает данные заказов в список пользовательских объектов OrderData"""
        orders_data_list = list()
        pages_urls_list_from_pagination = await self._get_pages_from_pagination()
        if pages_urls_list_from_pagination:
            for pare_url in pages_urls_list_from_pagination:
                orders_html_list = await self._get_orders_pages(pare_url)
                orders_data_list.extend(await self._get_orders_data(orders_html_list))
        return orders_data_list




async def main():
    start_time = time.time()  # Замеряем время перед выполнением кода
    host = 'https://procapitalist.ru'
    main_page = 'obyavleniya/ishchu-proizvoditelej-uslugi-po-poshivu-5'

    scraper = Scraper(host, main_page)
    orders_data_list = await scraper.get_data()

    print(*orders_data_list, sep='\n')
    logger.debug(len(orders_data_list))

    end_time = time.time()  # Замеряем время после выполнения кода
    elapsed_time = end_time - start_time
    print(f"Время выполнения кода: {elapsed_time} секунд")

if __name__ == '__main__':
    asyncio.run(main())
