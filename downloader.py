import asyncio
from typing import List

import aiohttp

from config import logger
from ctypes import Page


class Downloader:
    """Управление загрузкой"""

    def __init__(self):
        self.session: aiohttp.ClientSession | None = None

    async def _start_session(self) -> None:
        """Открывает сессию"""
        try:
            self.session = aiohttp.ClientSession()
        except (aiohttp.ClientConnectorError, aiohttp.ClientResponseError) as e:
            logger.error(f"Ошибка при подключении: {e}")

    async def _stop_session(self) -> None:
        """Закрывает сессию >:-)"""
        if self.session:
            await self.session.close()

    async def _fetch_html(self, url: str, params: str | None = None, retry: int = 5) -> str:
        """
        Выполняет GET запрос, возвращает текст ответа
        :param url:
        :param params:
        :param retry: количество попыток при неудачном соединении
        :return: html страницы
        """
        while retry > 0:
            try:
                async with self.session.get(url, params=params) as response:
                    logger.debug(f'{url} {response.status}')
                    if response.status != 200:
                        raise aiohttp.ClientResponseError(
                            request_info=response.request_info,
                            history=response.history,
                            status=response.status,
                            message=f"Недопустимый статус запроса на {url} {response.status}",
                        )
                    return await response.text()
            except Exception as e:
                logger.warning(f'Ошибка при запросе {url}: {e}. Осталось попыток: {retry}')
                await asyncio.sleep(3)
                retry -= 1
            else:
                continue

    async def download_html_from_url_list(self, pages: List[Page]) -> tuple:
        """Загружает HTML страниц из списка пользовательских объектов Pages"""
        await self._start_session()
        try:
            page_html_list = await asyncio.gather(
                *[self._fetch_html(page.url, params=page.params) for page in pages])
            return page_html_list
        except Exception:
            return list()
        finally:
            await self._stop_session()

    async def download_html_from_url(self, page: Page):
        """Загружает HTML по url и headers из пользовательского объекта Page"""
        await self._start_session()
        try:
            page_html = await self._fetch_html(page.url, params=page.params)
            return page_html
        finally:
            await self._stop_session()


async def main():
    downloader = Downloader()
    page = Page(url="https://procapit234alist.ru/obyavleniya/ishchu-proizvoditelej-uslugi-po-poshivu-5")
    page_html = await downloader.download_html_from_url(page)
    print(page_html)


if __name__ == "__main__":
    asyncio.run(main())
