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
                
        # Maintain a persistent connection to avoid losing :memory: databases
        # and to improve performance.
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA foreign_keys = ON")  # Enforce foreign key constraints
        self.conn.row_factory = sqlite3.Row
        
        self.initialize_db()

    def initialize_db(self) -> None:
        """Creates the habits and completions tables if they don't already exist."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                specification TEXT,
                periodicity TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                completed_at TEXT NOT NULL,
                FOREIGN KEY (habit_id) REFERENCES habits (id) ON DELETE CASCADE
            )
        """)
        self.conn.commit()

    def save_habit(self, habit: Habit) -> int:
        """
        Inserts a new habit into the database.
        """
        cursor = self.conn.execute(
            "INSERT INTO habits (name, specification, periodicity, created_at) VALUES (?, ?, ?, ?)",
            (habit.name, habit.specification, habit.periodicity, habit.created_at.isoformat())
        )
        self.conn.commit()
        return cursor.lastrowid

    def load_habits(self) -> List[Habit]:
        """
        Loads all habits and their corresponding completions from the database.
        """
        habits = []
        habit_rows = self.conn.execute("SELECT * FROM habits").fetchall()
        
        for row in habit_rows:
            habit_id = row["id"]
            
            completion_rows = self.conn.execute(
                "SELECT completed_at FROM completions WHERE habit_id = ? ORDER BY completed_at ASC",
                (habit_id,)
            ).fetchall()
            
            completions = [datetime.fromisoformat(c["completed_at"]) for c in completion_rows]
            
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
        """
        self.conn.execute(
            "INSERT INTO completions (habit_id, completed_at) VALUES (?, ?)",
            (habit_id, timestamp.isoformat())
        )
        self.conn.commit()

    def delete_habit(self, habit_id: int) -> None:
        """
        Deletes a habit and all its associated completions from the database.
        """
        self.conn.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
        self.conn.commit()