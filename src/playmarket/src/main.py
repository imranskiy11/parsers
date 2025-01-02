from config import URL, BATCH_SIZE
from logger import setup_logger
from parser import parse_reviews
from db_handler import save_to_db
from utils import get_driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def main():
    logger = setup_logger()
    driver = get_driver()

    # Инициализация
    processed_ids = set()
    total_reviews_collected = 0

    try:
        logger.info(f"Open: {URL}")
        driver.get(URL)

        logger.info(
            "Waiting for the 'Ratings and Reviews' button to appear...")
        reviews_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (
                    By.XPATH, 
                    "//button[@aria-label='Подробнее об игре \"Оценки и отзывы\"']"))
        )
        logger.info("Founded \ Click...")
        reviews_button.click()

        # Главный цикл парсинга
        while True:
            data = parse_reviews(driver, logger, BATCH_SIZE, processed_ids)
            logger.info(f"Collected {len(data)} new reviews.")

            if not data:
                logger.info("New rebiews not founded. Finish collecting .. .")
                break

            save_to_db(data=data, table_name='twimby')
            logger.info(f"Saved {len(data)} unique review to DB.")

            total_reviews_collected += len(data)
            logger.info(
                f"Total of reviews collected: {total_reviews_collected}")

    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        logger.info("Closing browser..")
        driver.quit()


def debug():
    """
    test func.
    """
    TEST_BATCH_SIZE = 50
    logger = setup_logger()
    driver = get_driver()

    try:
        logger.info(f"OPen: {URL}")
        driver.get(URL)

        logger.info(
            "Waiting for the 'Ratings and Reviews' button to appear...")
        reviews_button = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located(
                (By.XPATH, 
                 "//button[@aria-label='Подробнее об игре \"Оценки и отзывы\"']"))
        )
        logger.info("Founded...")
        reviews_button.click()

        logger.info(f"Start collecting first {TEST_BATCH_SIZE} reviews...")
        data = parse_reviews(driver, logger, TEST_BATCH_SIZE)
        save_to_db(data=data, table_name='todolist')

    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        logger.info("Closing...")
        driver.quit()


if __name__ == "__main__":
    main()
