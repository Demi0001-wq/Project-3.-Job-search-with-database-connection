from src.api_client import HHApi
from src.db_creator import create_database, create_tables, save_data_to_db
from src.db_manager import DBManager
from src.config import config


def user_interaction():
    """
    Console interface for interacting with the database.
    """
    db_name = "hh_jobs"
    params = config()
    db_manager = DBManager(db_name, params)

    print("\n--- Job Search Database Management ---")
    
    while True:
        print("\nChoose an action:")
        print("1. List all companies and their vacancy count")
        print("2. List all vacancies")
        print("3. Show average salary")
        print("4. List vacancies with salary higher than average")
        print("5. Search vacancies by keyword")
        print("0. Exit")
        
        choice = input("\nEnter choice: ")
        
        if choice == "1":
            results = db_manager.get_companies_and_vacancies_count()
            print("\nCompanies and vacancy counts:")
            for company, count in results:
                print(f"{company}: {count} vacancies")
                
        elif choice == "2":
            results = db_manager.get_all_vacancies()
            print("\nAll vacancies:")
            for company, title, sal_from, sal_to, curr, url in results:
                salary = f"{sal_from if sal_from else 0}-{sal_to if sal_to else '...'}"
                print(f"[{company}] {title} | Salary: {salary} {curr if curr else ''} | Link: {url}")
                
        elif choice == "3":
            avg_salary = db_manager.get_avg_salary()
            print(f"\nAverage salary: {avg_salary:.2f}")
            
        elif choice == "4":
            results = db_manager.get_vacancies_with_higher_salary()
            print("\nVacancies with higher than average salary:")
            for company, title, sal_from, sal_to, curr, url in results:
                salary = f"{sal_from if sal_from else 0}-{sal_to if sal_to else '...'}"
                print(f"[{company}] {title} | Salary: {salary} {curr if curr else ''} | Link: {url}")
                
        elif choice == "5":
            keyword = input("Enter keyword to search: ")
            results = db_manager.get_vacancies_with_keyword(keyword)
            print(f"\nVacancies matching '{keyword}':")
            for company, title, sal_from, sal_to, curr, url in results:
                salary = f"{sal_from if sal_from else 0}-{sal_to if sal_to else '...'}"
                print(f"[{company}] {title} | Salary: {salary} {curr if curr else ''} | Link: {url}")
                
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


def main():
    # 10 Selected Company IDs
    employer_ids = [
        "1740",    # Yandex
        "3529",    # Sber
        "15478",   # VK
        "7863",    # Tinkoff
        "1057",    # Kaspersky
        "2180",    # Alfa-Bank
        "3776",    # MTS
        "1122401", # Skyeng
        "7172",    # Ozon
        "84552"    # Avito
    ]
    
    db_name = "hh_jobs"
    params = config()
    
    print("Fetching data from HH.ru...")
    api = HHApi(employer_ids)
    employers = api.get_employers()
    vacancies = api.get_all_vacancies()
    print(f"Fetched {len(employers)} employers and {len(vacancies)} vacancies.")
    
    print("Initializing database...")
    create_database(db_name, params)
    create_tables(db_name, params)
    
    print("Saving data to database...")
    save_data_to_db(db_name, params, employers, vacancies)
    
    user_interaction()


if __name__ == "__main__":
    main()
