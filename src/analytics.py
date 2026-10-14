# src/analytics.py
from typing import List
from src.habit import Habit

def get_all_habits(habits: List[Habit]) -> List[Habit]:
    """
    Returns a list of all currently tracked habits.
    (Functional approach: returns a new list reference, leaving original untouched)
    
    Args:
        habits (List[Habit]): The list of habits to analyze.
        
    Returns:
        List[Habit]: All tracked habits.
    """
    return list(habits)

def get_habits_by_periodicity(habits: List[Habit], periodicity: str) -> List[Habit]:
    """
    Filters the list of habits and returns only those matching the given periodicity.
    Uses the built-in filter() function.
    
    Args:
        habits (List[Habit]): The list of habits to filter.
        periodicity (str): The periodicity to filter by ("daily" or "weekly").
        
    Returns:
        List[Habit]: A list of habits with the specified periodicity.
    """
    return list(filter(lambda habit: habit.periodicity == periodicity.lower(), habits))

def get_longest_streak_for_habit(habit: Habit) -> int:
    """
    Returns the longest run streak for a given habit.
    (Wrapped in a function to maintain a functional API style).
    
    Args:
        habit (Habit): The habit to analyze.
        
    Returns:
        int: The longest streak achieved for this habit.
    """
    return habit.get_longest_streak()

def get_longest_streak_overall(habits: List[Habit]) -> int:
    """
    Returns the longest run streak among all defined habits.
    Uses map() to extract streaks and max() to find the highest value.
    
    Args:
        habits (List[Habit]): The list of habits to analyze.
        
    Returns:
        int: The longest streak across all habits. Returns 0 if no habits exist.
    """
    if not habits:
        return 0
        
    # Map each habit to its longest streak, then find the maximum value
    streaks = map(lambda habit: habit.get_longest_streak(), habits)
    return max(streaks)

from datetime import datetime, timedelta # Add this to the top of analytics.py if not there

def get_struggled_habits(habits: List[Habit]) -> List[Habit]:
    """
    Returns a list of habits the user struggled with in the last 30 days.
    Definition of "struggled": The habit was completed less than 90% of the expected periods.
    Uses filter().
    
    Args:
        habits (List[Habit]): The list of habits to analyze.
        
    Returns:
        List[Habit]: A list of habits that were struggled with.
    """
    thirty_days_ago = datetime.now() - timedelta(days=30)
    
    def is_struggled(habit: Habit) -> bool:
        # Get completions within the last 30 days
        recent_completions = list(filter(lambda c: c >= thirty_days_ago, habit.completions))
        count = len(recent_completions)
        
        if habit.periodicity == "daily":
            return count < 28  # Missed 2 or more days
        elif habit.periodicity == "weekly":
            return count < 4   # Missed 1 or more weeks
        return False
        
    return list(filter(is_struggled, habits))