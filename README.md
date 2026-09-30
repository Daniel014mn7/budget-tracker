# Budget Tracker

A command-line budget tracking application built with Python.

The application allows users to record income and expenses, manage transactions, calculate their current balance, and view monthly financial summaries. Data is stored locally using SQLite, with CSV support for backup and export.

## Features

- Add income and expense transactions
- Edit existing transactions
- Delete transactions
- Calculate the current balance
- View monthly income and expense summaries
- Validate dates and transaction amounts
- Store data locally using SQLite
- Save transaction data to CSV

## Technologies Used

- Python
- SQLite
- CSV
- Object-Oriented Programming (OOP)
- Python Dataclasses
- Type Hints

## Project Structure

```text
budget_tracker/
├── app.py
├── tracker.py
├── storage.py
├── models.py
├── utils.py
├── README.md
└── .gitignore
```

- **app.py** — Entry point and command-line interface.
- **tracker.py** — Contains the main budget tracking logic.
- **storage.py** — Handles SQLite and CSV data storage.
- **models.py** — Defines the transaction data model.
- **utils.py** — Contains validation and helper functions.

## How to Run

Clone the repository:

```bash
git clone <repository-url>
```

Navigate to the project directory:

```bash
cd budget-tracker
```

Run the application:

```bash
python3 app.py
```

No external Python packages are required.

## Data Privacy

Financial data is stored locally in `budget_data.db` and `budget_data.csv`.

These files are excluded from Git through `.gitignore`, so personal transaction data is not uploaded to the repository.

## What I Learned

While building this project, I practiced:

- Organizing Python code into multiple modules
- Object-Oriented Programming
- Working with SQLite databases
- Reading and writing CSV files
- Input validation and error handling
- Python type hints and dataclasses
- Separating application logic from data storage
- Using Git and GitHub for version control