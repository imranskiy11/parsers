from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random


def parse_reviews(driver, logger, batch_size, processed_ids):
    """
    Collecting reviews by recording the last processed item 
    and processing only new reviews.
    """
    logger.info("Starting ... ")
    reviews_data = []
    review_block_xpath = "//*[@id='yDmH0d']/div[5]/div[2]/div/div/div/div/div[2]/div/div[2]/div"

    try:
        while len(reviews_data) < batch_size:
            logger.info("Waiting for the container with reviews to load...")
            container_xpath = "//*[@id='yDmH0d']/div[5]/div[2]/div/div/div/div/div[2]"
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, container_xpath))
            )
            logger.info("Container with reviews found.")

            # Прокрутка контейнера для загрузки новых отзывов
            logger.info("I start scrolling through the container with reviews...")
            review_container = driver.find_element(By.XPATH, container_xpath)
            for _ in range(3):
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", review_container)
                time.sleep(random.uniform(2, 3))
            logger.info("Container scrolling completed.")

            # Парсинг отзывов
            logger.info("Parsing...")
            review_blocks = driver.find_elements(By.XPATH, review_block_xpath)
            logger.info(f"Reviews founded: {len(review_blocks)}")

            new_reviews = []

            for review in review_blocks:
                try:
                    # review unique id (author + review_date)
                    try:
                        author = review.find_element(By.XPATH, "./header/div[1]").text
                    except Exception:
                        author = "Не указан"

                    try:
                        review_date = review.find_element(By.XPATH, ".//span[@class='bp9Aid']").text
                    except Exception:
                        review_date = "Не указана"

                    review_id = f"{author}-{review_date}"

                    if review_id in processed_ids:
                        continue

                    # Оценка (текст)
                    try:
                        rating_element = review.find_element(By.XPATH, "./header/div[2]/div")
                        rating = rating_element.get_attribute("aria-label")
                    except Exception:
                        rating = "Не указано"

                    # Текст отзыва
                    try:
                        review_text = review.find_element(By.XPATH, "./div[1]").text
                    except Exception:
                        review_text = "Не указан"

                    # Полезность отзыва
                    try:
                        helpful_count = review.find_element(By.XPATH, "./div[2]").text
                    except Exception:
                        helpful_count = "0"

                    # Ответ от разработчиков
                    try:
                        dev_reply = review.find_element(By.XPATH, "./div[3]/div[2]").text
                    except Exception:
                        dev_reply = "Нет ответа"

                    new_reviews.append({
                        "author": author,
                        "rating": rating,
                        "review_text": review_text,
                        "helpful_count": helpful_count,
                        "review_date": review_date,
                        "dev_reply": dev_reply,
                    })

                    # add to processed ID
                    processed_ids.add(review_id)

                except Exception as e:
                    logger.error(f"Parsing error: {e}")

            if not new_reviews:
                logger.info("New reviews not founed. Closing collecting")
                break

            # Добавляем новые отзывы
            reviews_data.extend(new_reviews)
            logger.info(f"Collected {len(new_reviews)} new reviews.")

            # Прекращаем сбор, если достигнут batch_size
            if len(reviews_data) >= batch_size:
                break

    except Exception as e:
        logger.error(f"Error: {e}")

    return reviews_data