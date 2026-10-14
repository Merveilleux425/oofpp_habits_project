Habit Tracking App (DLBDSOOFPP01 Portfolio)
    A Python backend for a habit tracking application. This application allows users to define daily and weekly habits, track task completions, and analyze their progress over time. It is built using Object-Oriented Programming (OOP) for state management and Functional Programming for data analytics.

Features
    Object-Oriented Design: Encapsulated Habit and HabitTracker classes.
    Functional Analytics: Pure functions (map, filter, max) to calculate streaks and identify struggles.
    Persistent Storage: Uses SQLite3 to reliably store habits and completion history between sessions.
    Command Line Interface (CLI): Clean, easy-to-use API built with click.
    Predefined Test Fixtures: Includes 5 default habits with 4 weeks of realistic example tracking data.
    Unit Tested: Comprehensive pytest suite covering critical paths and edge cases.

Prerequisites
    Python 3.7 or later
    pip (Python package installer)

Installation
1. Clone the repository to your local machine:
    git clone https://github.com/Merveilleux425/oofpp_habits_project.git
2. Navigate into the project directory:
    cd oofpp_habits_project
3. Install the required dependencies:
    pip install -r requirements.txt
(Note: This installs click for the CLI and pytest for testing).

Usage
    The application is operated entirely via the Command Line Interface. To see a list of available commands, run:
        python main.py --help

Loading Example Data
    To get started immediately with 5 predefined habits and 4 weeks of test data, run:
        python main.py load_fixtures

Creating a New Habit
    You can create a new habit by providing a name, specification, and periodicity (daily or weekly).
        python main.py create --name "Meditate" --spec "Meditate for 10 mins" --periodicity daily
    Alternatively, you can run python main.py create and the CLI will interactively prompt you for the details.

Completing a Task
    To check off a habit for the current period, use the complete command followed by the habit's ID.
        python main.py complete 1

Listing Habits
    To view all currently tracked habits:
        python main.py list_habits

Deleting a Habit
    To delete a habit and all of its associated completion history:
        python main.py delete 1

Analytics
    The analytics module allows you to analyze your tracking data.
    List all habits of a specific periodicity:
        python main.py analyze-periodicity daily
    View longest streaks: Shows the longest streak across all habits, as well as individual longest streaks.
        python main.py analyze-streaks
    Identify struggled habits: Shows habits that were missed frequently in the last 30 days.
        python main.py analyze-struggles

Testing
    The critical parts of the solution (habit validity, streak calculation, analytics, and DB persistence) are covered by a unit test suite using pytest.
    To run the tests, ensure you are in the project root directory and execute:
        python -m pytest
    The test suite uses an in-memory SQLite database and pure in-memory object fixtures to ensure tests run quickly and do not pollute your local database files.

Project Structure
    oofpp_habits_project/
    ├── data/                   # Automatically created to store the SQLite DB file
    ├── src/
    │   ├── habit.py            # Habit class (OOP core)
    │   ├── tracker.py          # HabitTracker orchestrator
    │   ├── storage.py          # SQLite3 database abstraction layer
    │   ├── analytics.py        # Functional programming analytics module
    │   ├── predefined.py       # Fixture data generator (5 habits, 4 weeks)
    │   └── cli.py              # Click-based Command Line Interface
    ├── tests/
    │   ├── test_habit.py       # Unit tests for OOP logic
    │   ├── test_tracker.py     # Unit tests for DB persistence
    │   └── test_analytics.py   # Unit tests for functional analytics
    ├── main.py                 # Entry point for the CLI application
    ├── requirements.txt        # Python dependencies
    └── README.md               # This file
