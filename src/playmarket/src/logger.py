import logging


def setup_logger():
    logger = logging.getLogger("playmarket_review")
    logger.setLevel(logging.DEBUG)

    # console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # file handle
    file_handler = logging.FileHandler("reviews.log")
    file_handler.setLevel(logging.DEBUG)

    # log formatter
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
