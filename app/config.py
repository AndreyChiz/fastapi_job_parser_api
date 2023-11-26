import os


class DatabaseConfig:
    """
    Класс с настройками базы данных.
    """
    HOST = os.getenv('DB_HOST', 'mysql')
    USER = os.getenv('DB_USER', 'procapi')
    PASSWORD = os.getenv('DB_PASSWORD', 'procapi')
    DATABASE = os.getenv('DATABASE', 'procapi')


class SchedulerConfig:
    UPDATE_FREQUENCY = os.getenv('SCHEDULER_UPDATE_FREQUENCY_MINUTES', 5)
