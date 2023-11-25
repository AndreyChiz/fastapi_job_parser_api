from http.client import HTTPException
from typing import List

import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler  # Import the asyncio scheduler
from fastapi import FastAPI

from models import OrderData
from scrapper import Scraper

host = 'https://procapitalist.ru'
main_page = 'obyavleniya/ishchu-proizvoditelej-uslugi-po-poshivu-5'

app = FastAPI(
    debug=True,
    docs_url='/api/docs',
    title='Procapi API',
)

scrapper = Scraper(host, main_page)
scheduler = AsyncIOScheduler()


async def update_data_job():
    await scrapper.update_data()


scheduler.add_job(update_data_job, 'interval', minutes=5)
scheduler.start()

order_example = {"id": 12081,
                 "url": "https://procapitalist.ru/obyavleniya/ad/ishchu-proizvoditelej-uslugi-po-poshivu-5/ishchem-podryadchika-po-poshivu-chekhlov-dlya-avtokresel-i-kolyasok-12081",
                 "title": "Ищем подрядчика по пошиву чехлов для детских автомобильных кресел",
                 "post_date": "13.09.2021 16:21", "price": None,
                 "location": "Рязань",
                 "seller": "Елена",
                 "description": "В связи с увеличением потребности в швейном ресурсе ищем подрядчика по пошиву. ....в вотсап по номеру 8-910-901-45-28",
                 "views": 422, "expiration_date": "09.12.2023 17:44",
                 "categories": "Ищу производителей - Услуги по пошиву",
                 "images": ["https://procapitalist.ru/images/classifieds/12/12081_kolibri_thb.jpg",
                            "https://procapitalist.ru/images/classifieds/12/12081_gals_plyus_thb.jpg"]}


@app.get("/orders", description="Возвращает список данных всех заказов.", response_model=List[OrderData])
async def get_orders():
    data = await scrapper.get_data()

    # Проверка, что данные не пусты, если нужно
    if not data:
        raise HTTPException(status_code=404, detail="No orders found")

    # Возвращаем данные в виде списка Pydantic-моделей
    return data


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
