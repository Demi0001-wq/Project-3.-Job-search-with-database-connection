# Job Search Database Project

This project automates the process of collecting job vacancy data from HH.ru, storing it in a PostgreSQL database, and providing analytical tools to query the data.

## Features

- API Integration: Fetches real-time data for 10 prominent tech companies via HH.ru Public API.
- Database Automation: Automatically creates the database schema and populates tables.
- Analytical Manager: `DBManager` class provides easy methods for:
    - Company vacancy counts.
    - Comprehensive vacancy listings.
    - Average salary calculations.
    - Filtering high-salary roles.
    - Keyword-based search.
- User Interface: Interactive console menu for easy data exploration.

## Prerequisites

- Python 3.x
- PostgreSQL
- HH.ru API (Public access, no key required for these endpoints)

## Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure your database in `database.ini`:
   ```ini
   [postgresql]
   host=localhost
   user=postgres
   password=your_password
   port=5432
   ```

## Usage

Run the main script:
```bash
python main.py
```

## Structure

- `main.py`: Entry point and UI.
- `src/api_client.py`: HH.ru API interaction.
- `src/db_creator.py`: Database schema and population.
- `src/db_manager.py`: Analytical queries.
- `src/config.py`: Configuration loader.
