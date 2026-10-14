# src/storage.py
import sqlite3
import os
from datetime import datetime
from typing import List
from src.habit import Habit

class StorageManager:
    """
    Manages the persistence of habits and completions using a SQLite database.
    Abstraction layer for database operations.
    """
    
    def __init__(self, db_path: str = "data/habits.db"):
        """
        Initializes the storage manager and ensures the database schema exists.
        Uses ':memory:' for unit testing, otherwise creates a file.
        """
        self.db_path = db_path
        
        # Ensure the data directory exists if we are using a file-based DB
        if db_path != ":memory:":
            db_dir = os.path.dirname(db_path)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir)
                
        self.initialize_db()

    def _get_connection(self) -> sqlite3.Connection:
        """
        Creates and returns a new database connection.
        Sets row_factory to sqlite3.Row for dictionary-like access to rows.
        """
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")  # Enforce foreign key constraints
        conn.row_factory = sqlite3.Row
        return conn

    def initialize_db(self) -> None:
        """Creates the habits and completions tables if they don't already exist."""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS habits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    specification TEXT,
                    periodicity TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS completions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_id INTEGER NOT NULL,
                    completed_at TEXT NOT NULL,
                    FOREIGN KEY (habit_id) REFERENCES habits (id) ON DELETE CASCADE
                )
            """)

    def save_habit(self, habit: Habit) -> int:
        """
        Inserts a new habit into the database.
        
        Args:
            habit (Habit): The Habit object to save.
            
        Returns:
            int: The database ID assigned to the newly created habit.
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO habits (name, specification, periodicity, created_at) VALUES (?, ?, ?, ?)",
                (habit.name, habit.specification, habit.periodicity, habit.created_at.isoformat())
            )
            return cursor.lastrowid

    def load_habits(self) -> List[Habit]:
        """
        Loads all habits and their corresponding completions from the database.
        Reconstructs them into Habit objects.
        
        Returns:
            List[Habit]: A list of all stored Habit objects.
        """
        habits = []
        with self._get_connection() as conn:
            # Fetch all habits
            habit_rows = conn.execute("SELECT * FROM habits").fetchall()
            
            for row in habit_rows:
                habit_id = row["id"]
                
                # Fetch completions for this specific habit
                completion_rows = conn.execute(
                    "SELECT completed_at FROM completions WHERE habit_id = ? ORDER BY completed_at ASC",
                    (habit_id,)
                ).fetchall()
                
                # Convert string timestamps back to datetime objects
                completions = [datetime.fromisoformat(c["completed_at"]) for c in completion_rows]
                
                # Reconstruct the Habit object
                habit = Habit(
                    id=habit_id,
                    name=row["name"],
                    specification=row["specification"],
                    periodicity=row["periodicity"],
                    created_at=datetime.fromisoformat(row["created_at"]),
                    completions=completions
                )
                habits.append(habit)
                
        return habits

    def save_completion(self, habit_id: int, timestamp: datetime) -> None:
        """
        Saves a single task completion to the database.
        
        Args:
            habit_id (int): The ID of the habit that was completed.
            timestamp (datetime): The time of completion.
        """
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO completions (habit_id, completed_at) VALUES (?, ?)",
                (habit_id, timestamp.isoformat())
            )

    def delete_habit(self, habit_id: int) -> None:
        """
        Deletes a habit and all its associated completions from the database.
        Relies on ON DELETE CASCADE set in the schema.
        
        Args:
            habit_id (int): The ID of the habit to delete.
        """
        with self._get_connection() as conn:
            conn.execute("DELETE FROM habits WHERE id = ?", (habit_id,))