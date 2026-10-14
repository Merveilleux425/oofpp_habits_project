# tests/test_habit.py
import pytest
from datetime import datetime, timedelta
from src.habit import Habit
from src.predefined import get_predefined_habits_for_testing

@pytest.fixture
def predefined_habits():
    """Fixture to load 5 predefined habits with 4 weeks of data."""
    return get_predefined_habits_for_testing()

def test_habit_creation(predefined_habits):
    """Test if habits are initialized correctly."""
    assert len(predefined_habits) == 5
    assert predefined_habits[0].name == "Brush teeth"
    assert predefined_habits[3].periodicity == "weekly"

def test_longest_streak_perfect(predefined_habits):
    """Test longest streak for a habit completed every day."""
    brush_teeth = predefined_habits[0]
    assert brush_teeth.get_longest_streak() == 28

def test_longest_streak_broken(predefined_habits):
    """Test longest streak for a habit with a break."""
    water = predefined_habits[1]
    # 14 days, missed 1, 13 days -> longest is 14
    assert water.get_longest_streak() == 14

def test_is_broken_true():
    """Test if a habit with missed periods is marked as broken."""
    # Create a habit that hasn't been completed in 5 days
    old_date = datetime.now() - timedelta(days=5)
    habit = Habit(99, "Old Habit", "Test", "daily", old_date)
    habit.complete_task(old_date)
    
    assert habit.is_broken() == True

def test_is_broken_false(predefined_habits):
    """Test if a perfectly maintained habit is not broken."""
    brush_teeth = predefined_habits[0]
    assert brush_teeth.is_broken() == False