import psycopg2
from typing import Any, Dict, List


class DBManager:
    """
    Class for managing and querying data in the PostgreSQL database.
    """

    def __init__(self, db_name: str, params: dict):
        """
        Initialize the DBManager with database name and connection parameters.
        :param db_name: Name of the database to connect to.
        :param params: Dictionary of connection parameters.
        """
        self.db_name = db_name
        self.params = params

    def _execute_query(self, query: str, params: tuple = None) -> List[tuple]:
        """
        Internal method to execute a query and return results.
        """
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(query, params)
            results = cur.fetchall()
        conn.close()
        return results

    def get_companies_and_vacancies_count(self) -> List[tuple]:
        """
        Receives a list of all companies and the number of vacancies at each company.
        :return: List of tuples (company_name, vacancies_count).
        """
        query = """
            SELECT e.name, COUNT(v.vacancy_id)
            FROM employers e
            LEFT JOIN vacancies v ON e.employer_id = v.employer_id
            GROUP BY e.name
        """
        return self._execute_query(query)

    def get_all_vacancies(self) -> List[tuple]:
        """
        Receives a list of all vacancies with company name, job title, salary, and link.
        :return: List of tuples (company_name, job_title, salary_from, salary_to, currency, url).
        """
        query = """
            SELECT e.name, v.name, v.salary_from, v.salary_to, v.currency, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
        """
        return self._execute_query(query)

    def get_avg_salary(self) -> float:
        """
        Receives the average salary for vacancies.
        :return: Average salary as a float.
        """
        query = """
            SELECT AVG((COALESCE(salary_from, salary_to) + COALESCE(salary_to, salary_from)) / 2)
            FROM vacancies
            WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL
        """
        result = self._execute_query(query)
        return float(result[0][0]) if result and result[0][0] else 0.0

    def get_vacancies_with_higher_salary(self) -> List[tuple]:
        """
        Receives a list of all vacancies with salaries higher than the average.
        :return: List of tuples (company_name, job_title, salary_from, salary_to, currency, url).
        """
        avg_salary = self.get_avg_salary()
        query = """
            SELECT e.name, v.name, v.salary_from, v.salary_to, v.currency, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
            WHERE (COALESCE(v.salary_from, v.salary_to) + COALESCE(v.salary_to, v.salary_from)) / 2 > %s
        """
        return self._execute_query(query, (avg_salary,))

    def get_vacancies_with_keyword(self, keyword: str) -> List[tuple]:
        """
        Gets a list of all vacancies whose titles contain the keyword.
        :param keyword: Word to search for in vacancy titles.
        :return: List of tuples (company_name, job_title, salary_from, salary_to, currency, url).
        """
        query = """
            SELECT e.name, v.name, v.salary_from, v.salary_to, v.currency, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
            WHERE v.name ILIKE %s
        """
        return self._execute_query(query, (f"%{keyword}%",))
