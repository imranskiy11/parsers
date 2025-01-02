import psycopg2
from psycopg2.extras import execute_values
from config import DB_SETTINGS


def connect_to_db():
    return psycopg2.connect(**DB_SETTINGS)


def save_to_db(data, table_name: str = 'todolist'):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        query = f"""
        INSERT INTO {table_name} 
        (author, rating, review_text, helpful_count, review_date, dev_reply)
        VALUES %s
        """

        formatted_data = [
            (
                item["author"],
                item["rating"],
                item["review_text"],
                item["helpful_count"],
                item["review_date"],
                item["dev_reply"],
            )
            for item in data
        ]

        execute_values(cursor, query, formatted_data)
        conn.commit()
        print(f"Saved {len(formatted_data)} reviews to DB.")

    except Exception as e:
        print(f"Saving Error: {e}")
    finally:
        conn.close()
