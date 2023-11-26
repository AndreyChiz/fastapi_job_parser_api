from loguru import logger

logger.add("../log.log", level="DEBUG", format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}")

# logger.add(lambda msg: print(msg, end=''), level="TRACE")
