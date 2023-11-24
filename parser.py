from urllib.parse import urlparse, parse_qs, urljoin, ParseResult

from bs4 import BeautifulSoup
from dateparser import parse as dateparse

from ctypes import OrderData


class Parser:
    """Реализует логику парсинга"""

    async def parse_pagination(self, page_html: str) -> list[int]:
        """
        Парсит в список url страниц из пагинации
        :param page_html: HTML
        :return: список url из пагинации
        """
        if page_html:
            soup: BeautifulSoup = BeautifulSoup(page_html, 'lxml')
            count_items: str = soup.find('div', 'pagination').find('a', {'aria-label': 'Перейти В конец'}).get('href')
            numb_item_last_page_tarts: int = int(parse_qs(urlparse(count_items).query)['start'][0])
            numbs_item_very_page_starts: list[int] = list(range(0, numb_item_last_page_tarts + 1, 25))
            return numbs_item_very_page_starts

    async def parse_items_list(self, page_html: str) -> list[str]:
        """
        Парсит в список url карточек заказов
        :param page_html: HTML
        :return: список url карточек заказов
        """
        if page_html:
            soup: BeautifulSoup = BeautifulSoup(page_html, 'lxml')
            items_list = [element['href'] for element in soup.find_all('a', class_='blog_det_link')]
            return items_list

    async def parse_item_data(self, page_html: str) -> OrderData:
        """
        Парсит данные с карточки заказа в пользовательский объект OrderData
        :param page_html: html карточки заказа
        :return: OrderData
        """
        if page_html:
            soup = BeautifulSoup(page_html, 'lxml')

            url: str = soup.find('head').find('link').get('href')

            host: ParseResult = urlparse(url)
            host: str = f"{host.scheme}://{host.netloc}"

            item_id: str = url.split('-')[-1]

            item_data_container: BeautifulSoup | None = soup.find('div', id='dj-classifieds')

            title: BeautifulSoup | None = item_data_container.find('div', 'title_top')
            title: str = title.text.strip() if title else None

            post_date: BeautifulSoup | None = item_data_container.find('span', 'row_value')
            post_date: str | None = post_date.text.strip() if post_date else None

            price: BeautifulSoup | None = item_data_container.find('span', 'price_val')
            price: str | None = price.text.strip() if price else None
            try:
                price: int | None = int(price)
            except (TypeError, ValueError):
                price = None

            location: BeautifulSoup | None = item_data_container.find('div', 'contact_row row_city')
            location: BeautifulSoup | None = location.find('span', 'row_value') if location else None
            location: str | None = location.text.strip() if location else None
            seller: str = item_data_container.find('div', 'row_value user_name_row').find('a', 'profile_name')
            seller: str = seller.text.strip() if seller else None

            description: BeautifulSoup | None = item_data_container.find('div', 'desc_content')
            description: str = description.text.strip(
            ).replace('\n', '').replace('\r', '').replace('\xa0', '').strip(
            ) if description else None

            images_list: BeautifulSoup | None = item_data_container.find('div', 'djc_thumbnails djc_thumbs_gal3')
            images_list: list = [urljoin(host, image.get('href')) for image in
                                 images_list.findAll('a')] if images_list else None

            additional: BeautifulSoup | None = item_data_container.find('div', 'additional')
            additional: list = additional.findAll('span', 'row_value') if additional else None

            views: str | None = None
            expiration_date: str | None = None
            categories: str | None = None

            if additional:
                aditional_items = [item.text.strip() for item in additional]
                add_id, views, expiration_date, categories = aditional_items

            order_data = OrderData(

                id=int(item_id) if item_id.isdigit() else None,
                url=url,
                title=title,
                post_date=dateparse(post_date, languages=['ru']).strftime('%d.%m.%Y %H:%M') if post_date else None,
                price=price,
                location=location,
                seller=seller,
                description=description,
                views=int(views) if views.isdigit() else None,
                expiration_date=dateparse(expiration_date, languages=['ru']).strftime(
                    '%d.%m.%Y %H:%M') if post_date else None,
                categories=categories,
                images=images_list
            )

            return order_data
