import json
import pymysql.cursors
from dataclasses import asdict
from typing import List
from config import DatabaseConfig
from logger import logger
import traceback
from models import OrderData


class Database:
    def __init__(self, config=None):
        """
        Инициализирует Database с параметрами подключения к базе данных.

        :param config: Объект с настройками базы данных (по умолчанию используется DatabaseConfig из config.py).
        """
        if config is None:
            config = DatabaseConfig()

        self.connection_params = {
            'host': config.HOST,
            'user': config.USER,
            'password': config.PASSWORD,
            'db': config.DATABASE,
            'port': 3307,  # Изменен порт на 3307
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }

    def save_orders_to_database(self, orders: List[OrderData]) -> None:
        """
        Сохраняет список объектов OrderData в базу данных.

        :param orders: Список объектов OrderData для сохранения.
        """
        connection = pymysql.connect(**self.connection_params)

        try:
            with connection.cursor() as cursor:
                # Проверяем существование таблицы
                cursor.execute("SHOW TABLES LIKE 'procapi_orders'")
                table_exists = cursor.fetchone()

                if not table_exists:
                    # Если таблицы не существует, создаем её
                    cursor.execute("""
                        CREATE TABLE procapi_orders (
                            id INT PRIMARY KEY,
                            url VARCHAR(255),
                            title VARCHAR(255),
                            post_date VARCHAR(255),
                            price INT,
                            location VARCHAR(255),
                            seller VARCHAR(255),
                            description TEXT,
                            views INT,
                            expiration_date VARCHAR(255),
                            categories VARCHAR(255),
                            images TEXT
                        )
                    """)

                for order in orders:
                    try:
                        # Заменяем существующую запись, если она есть
                        cursor.execute(
                            "REPLACE INTO procapi_orders VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (order.id, order.url, order.title, order.post_date, order.price, order.location,
                             order.seller, order.description, order.views, order.expiration_date, order.categories,
                             json.dumps(order.images))
                        )

                    except pymysql.Error as e:
                        logger.error(f'Ошибка при записи заказа {order.id} в базу данных: {e}')

                connection.commit()
        except pymysql.Error as e:
            logger.error(f'Ошибка при взаимодействии с базой данных: {e}')
        finally:
            connection.close()

    def get_all_orders_as_json(self):
        """
        Получает все объекты OrderData из базы данных и возвращает их в формате JSON.

        :return: JSON-строка с данными всех заказов.
        """
        connection = pymysql.connect(**self.connection_params)

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM procapi_orders")
                result = cursor.fetchall()

                orders = []
                for row in result:
                    order_data = dict(zip(cursor.column_names, row))
                    order_data['images'] = json.loads(order_data['images'])
                    orders.append(OrderData(**order_data))

        finally:
            connection.close()

        return json.dumps([asdict(order) for order in orders], ensure_ascii=False)

    def check_connection(self):
        """
        Проверяет соединение с базой данных и записывает результат в лог.

        """
        try:
            connection = pymysql.connect(**self.connection_params)
            connection.ping(reconnect=True)
            connection.close()
            logger.debug('Успешное соединение с базой данных.')
        except pymysql.MySQLError as e:
            logger.error(f'Ошибка соединения с базой данных: {e}')
            logger.error(traceback.format_exc())


if __name__ == '__main__':

    db = Database()
    db.check_connection()