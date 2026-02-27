import psycopg2
from typing import Any, Dict, List


def create_database(db_name: str, params: dict):
    """
    Creates a new database.
    """
    # Connect to the default database (postgres) to create a new one
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()

    # Check if database exists
    cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
    exists = cur.fetchone()
    if not exists:
        cur.execute(f"CREATE DATABASE {db_name}")
        print(f"Database {db_name} created.")
    else:
        print(f"Database {db_name} already exists.")

    cur.close()
    conn.close()


def create_tables(db_name: str, params: dict):
    """
    Creates employers and vacancies tables.
    """
    conn = psycopg2.connect(dbname=db_name, **params)
    with conn.cursor() as cur:
        # Create employers table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employers (
                employer_id INT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                url TEXT,
                open_vacancies INT
            )
        """)

        # Create vacancies table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                vacancy_id INT PRIMARY KEY,
                employer_id INT REFERENCES employers(employer_id),
                name VARCHAR(255) NOT NULL,
                salary_from INT,
                salary_to INT,
                currency VARCHAR(10),
                url TEXT
            )
        """)
    conn.commit()
    conn.close()
    print("Tables created.")


def save_data_to_db(db_name: str, params: dict, employers: List[Dict[str, Any]], vacancies: List[Dict[str, Any]]):
    """
    Saves fetched data into the database.
    """
    conn = psycopg2.connect(dbname=db_name, **params)
    with conn.cursor() as cur:
        # Insert employers
        for emp in employers:
            cur.execute(
                "INSERT INTO employers (employer_id, name, url, open_vacancies) "
                "VALUES (%s, %s, %s, %s) ON CONFLICT (employer_id) DO UPDATE SET "
                "name = EXCLUDED.name, url = EXCLUDED.url, open_vacancies = EXCLUDED.open_vacancies",
                (emp["id"], emp["name"], emp["url"], emp["open_vacancies"])
            )

        # Insert vacancies
        for vac in vacancies:
            cur.execute(
                "INSERT INTO vacancies (vacancy_id, employer_id, name, salary_from, salary_to, currency, url) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (vacancy_id) DO UPDATE SET "
                "name = EXCLUDED.name, salary_from = EXCLUDED.salary_from, "
                "salary_to = EXCLUDED.salary_to, currency = EXCLUDED.currency, url = EXCLUDED.url",
                (vac["id"], vac["employer_id"], vac["name"], vac["salary_from"], vac["salary_to"], vac["currency"], vac["url"])
            )
    conn.commit()
    conn.close()
    print("Data saved to database.")
