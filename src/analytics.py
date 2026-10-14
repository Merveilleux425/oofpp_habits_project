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

def get_struggled_habits(habits: List[Habit]) -> List[Habit]:
    """
    Returns a list of habits the user struggled with.
    Definition of "struggled": The habit is currently broken 
    (i.e., missed the completion deadline in the current or previous period).
    Uses filter().
    
    Args:
        habits (List[Habit]): The list of habits to analyze.
        
    Returns:
        List[Habit]: A list of habits that are currently broken.
    """
    return list(filter(lambda habit: habit.is_broken(), habits))