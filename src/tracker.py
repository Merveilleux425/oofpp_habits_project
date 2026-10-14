# src/tracker.py
from datetime import datetime
from typing import List, Optional
from src.habit import Habit
from src.storage import StorageManager

class HabitTracker:
    """
    Manages the collection of habits and coordinates interactions with the storage layer.
    Acts as the core orchestrator for the application.
    """
    
    def __init__(self, db_path: str = "data/habits.db"):
        """
        Initializes the tracker, connects to the database, and loads existing habits into memory.
        """
        self.storage = StorageManager(db_path)
        self.habits: List[Habit] = self.storage.load_habits()

    def add_habit(self, name: str, specification: str, periodicity: str, created_at: Optional[datetime] = None) -> Habit:
        """
        Creates a new habit, saves it to the database, and adds it to the in-memory list.
        
        Args:
            name (str): Short name of the habit.
            specification (str): Detailed description.
            periodicity (str): "daily" or "weekly".
            created_at (datetime, optional): The creation date. Defaults to now.
            
        Returns:
            Habit: The newly created Habit object.
        """
        periodicity = periodicity.lower()
        if periodicity not in ["daily", "weekly"]:
            raise ValueError("Periodicity must be 'daily' or 'weekly'.")
            
        if created_at is None:
            created_at = datetime.now()
            
        # Create a temporary Habit object without an ID first
        new_habit = Habit(
            id=0,  # Temporary ID, will be replaced by DB
            name=name,
            specification=specification,
            periodicity=periodicity,
            created_at=created_at
        )
        
        # Save to DB and get the actual generated ID
        new_id = self.storage.save_habit(new_habit)
        new_habit.id = new_id
        
        # Add to memory
        self.habits.append(new_habit)
        return new_habit

    def delete_habit(self, habit_id: int) -> bool:
        """
        Deletes a habit and its completion history from the database and memory.
        
        Args:
            habit_id (int): The ID of the habit to delete.
            
        Returns:
            bool: True if deletion was successful, False if habit was not found.
        """
        habit = self.get_habit_by_id(habit_id)
        if habit:
            self.storage.delete_habit(habit_id)
            self.habits.remove(habit)
            return True
        return False

    def complete_task(self, habit_id: int, timestamp: Optional[datetime] = None) -> bool:
        """
        Marks a habit as complete for the given timestamp.
        
        Args:
            habit_id (int): The ID of the habit to complete.
            timestamp (datetime, optional): The time of completion. Defaults to now.
            
        Returns:
            bool: True if successful, False if habit was not found.
        """
        habit = self.get_habit_by_id(habit_id)
        if habit:
            if timestamp is None:
                timestamp = datetime.now()
                
            # Update memory
            habit.complete_task(timestamp)
            
            # Update database
            self.storage.save_completion(habit_id, timestamp)
            return True
        return False

    def get_habit_by_id(self, habit_id: int) -> Optional[Habit]:
        """
        Retrieves a single habit from memory by its ID.
        
        Args:
            habit_id (int): The ID of the habit.
            
        Returns:
            Optional[Habit]: The Habit object if found, else None.
        """
        for habit in self.habits:
            if habit.id == habit_id:
                return habit
        return None

    def get_all_habits(self) -> List[Habit]:
        """
        Returns all currently tracked habits.
        """
        return self.habits