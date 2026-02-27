import requests
from typing import Any, Dict, List


class HHApi:
    """
    Class for interacting with the HH.ru API.
    """

    BASE_URL = "https://api.hh.ru/"

    def __init__(self, employer_ids: List[str]):
        """
        Initialize with a list of employer IDs.
        :param employer_ids: List of strings containing employer IDs.
        """
        self.employer_ids = employer_ids

    def get_employers(self) -> List[Dict[str, Any]]:
        """
        Fetch details for the specified employers.
        :return: List of dictionaries with employer data.
        """
        employers_data = []
        for employer_id in self.employer_ids:
            response = requests.get(f"{self.BASE_URL}employers/{employer_id}")
            if response.status_code == 200:
                data = response.json()
                employers_data.append({
                    "id": data["id"],
                    "name": data["name"],
                    "url": data["alternate_url"],
                    "open_vacancies": data["open_vacancies"]
                })
            else:
                print(f"Error fetching employer {employer_id}: {response.status_code}")
        return employers_data

    def get_vacancies(self, employer_id: str) -> List[Dict[str, Any]]:
        """
        Fetch all vacancies for a specific employer.
        :param employer_id: Employer ID string.
        :return: List of dictionaries with vacancy data.
        """
        vacancies = []
        params = {
            "employer_id": employer_id,
            "per_page": 100,
            "page": 0
        }
        
        while True:
            response = requests.get(f"{self.BASE_URL}vacancies", params=params)
            if response.status_code == 200:
                data = response.json()
                items = data.get("items", [])
                for item in items:
                    # Filter for vacancies with salaries if needed, but the task says "receive a list of all vacancies"
                    # We will store what we can get.
                    salary = item.get("salary")
                    salary_from = salary.get("from") if salary else None
                    salary_to = salary.get("to") if salary else None
                    currency = salary.get("currency") if salary else None

                    vacancies.append({
                        "id": item["id"],
                        "name": item["name"],
                        "employer_id": employer_id,
                        "salary_from": salary_from,
                        "salary_to": salary_to,
                        "currency": currency,
                        "url": item["alternate_url"]
                    })
                
                # Check if there are more pages
                if data.get("pages", 0) > params["page"] + 1:
                    params["page"] += 1
                else:
                    break
            else:
                print(f"Error fetching vacancies for employer {employer_id}: {response.status_code}")
                break
                
        return vacancies

    def get_all_vacancies(self) -> List[Dict[str, Any]]:
        """
        Fetch all vacancies for all employers initialized in the class.
        :return: A flat list of dictionaries with vacancy data.
        """
        all_vacancies = []
        for emp_id in self.employer_ids:
            all_vacancies.extend(self.get_vacancies(emp_id))
        return all_vacancies


if __name__ == "__main__":
    # Test with a few IDs
    test_ids = ["1740", "3529"]
    api = HHApi(test_ids)
    emps = api.get_employers()
    print(f"Fetched {len(emps)} employers.")
    vacs = api.get_all_vacancies()
    print(f"Fetched {len(vacs)} vacancies total.")
