# src/predefined.py
from datetime import datetime, timedelta
from src.habit import Habit
from src.tracker import HabitTracker

def populate_predefined_habits(tracker: HabitTracker) -> None:
    """
    Populates the tracker with 5 predefined habits and 4 weeks of example tracking data.
    This serves as the test fixture and default data for the application.
    """
    # Start date is exactly 28 days ago at 10:00 AM to avoid timezone/midnight edge cases
    start_date = datetime.now() - timedelta(days=28)
    start_date = start_date.replace(hour=10, minute=0, second=0, microsecond=0)
    
    # 1. Create the 5 predefined habits
    habit1 = tracker.add_habit("Brush teeth", "Brush teeth every morning and night", "daily", start_date)
    habit2 = tracker.add_habit("Drink 2L Water", "Drink 2 liters of water throughout the day", "daily", start_date)
    habit3 = tracker.add_habit("Read 30 mins", "Read a book for at least 30 minutes before bed", "daily", start_date)
    habit4 = tracker.add_habit("Workout", "Go to the gym or do a home workout", "weekly", start_date)
    habit5 = tracker.add_habit("Call Parents", "Call parents to check in", "weekly", start_date)
    
    # 2. Generate 4 weeks (28 days) of completion data
    
    # Habit 1: Brush teeth (Completed every single day - 28 day streak)
    for i in range(28):
        completion_time = start_date + timedelta(days=i)
        tracker.complete_task(habit1.id, completion_time)
        
    # Habit 2: Drink 2L Water (14 day streak, missed 1 day, then 13 day streak)
    for i in range(14):
        completion_time = start_date + timedelta(days=i)
        tracker.complete_task(habit2.id, completion_time)
    # Day 15 (index 14) is missed!
    for i in range(15, 28):
        completion_time = start_date + timedelta(days=i)
        tracker.complete_task(habit2.id, completion_time)
        
    # Habit 3: Read 30 mins (Struggled: only completed Mon-Fri, missed weekends)
    for i in range(28):
        completion_time = start_date + timedelta(days=i)
        if completion_time.weekday() < 5:  # 0=Mon, 4=Fri
            tracker.complete_task(habit3.id, completion_time)
            
    # Habit 4: Workout (Completed every Monday for 4 weeks - 4 week streak)
    for i in range(28):
        completion_time = start_date + timedelta(days=i)
        if completion_time.weekday() == 0:  # 0=Monday
            tracker.complete_task(habit4.id, completion_time)
            
    # Habit 5: Call Parents (Struggled: missed weeks 2 and 4)
    week_1 = start_date + timedelta(days=2) # Wednesday of week 1
    week_3 = start_date + timedelta(days=16) # Wednesday of week 3
    tracker.complete_task(habit5.id, week_1)
    tracker.complete_task(habit5.id, week_3)

def get_predefined_habits_for_testing() -> list[Habit]:
    """
    Returns a list of predefined Habit objects with 4 weeks of completion data
    directly in memory. Used for unit testing without needing a database.
    """
    start_date = datetime.now() - timedelta(days=28)
    start_date = start_date.replace(hour=10, minute=0, second=0, microsecond=0)
    
    habits = [
        Habit(1, "Brush teeth", "Brush teeth every morning and night", "daily", start_date),
        Habit(2, "Drink 2L Water", "Drink 2 liters of water throughout the day", "daily", start_date),
        Habit(3, "Read 30 mins", "Read a book for at least 30 minutes before bed", "daily", start_date),
        Habit(4, "Workout", "Go to the gym or do a home workout", "weekly", start_date),
        Habit(5, "Call Parents", "Call parents to check in", "weekly", start_date)
    ]
    
    # Habit 1: 28 day streak
    for i in range(28):
        habits[0].complete_task(start_date + timedelta(days=i))
        
    # Habit 2: 14 day streak, missed 1, 13 day streak
    for i in range(14):
        habits[1].complete_task(start_date + timedelta(days=i))
    for i in range(15, 28):
        habits[1].complete_task(start_date + timedelta(days=i))
        
    # Habit 3: Weekdays only
    for i in range(28):
        if (start_date + timedelta(days=i)).weekday() < 5:
            habits[2].complete_task(start_date + timedelta(days=i))
            
    # Habit 4: Every Monday (4 week streak)
    for i in range(28):
        if (start_date + timedelta(days=i)).weekday() == 0:
            habits[3].complete_task(start_date + timedelta(days=i))
            
    # Habit 5: Week 1 and Week 3 only
    habits[4].complete_task(start_date + timedelta(days=2))
    habits[4].complete_task(start_date + timedelta(days=16))
    
    return habits