# tests/test_analytics.py
import pytest
from src.analytics import (
    get_all_habits,
    get_habits_by_periodicity,
    get_longest_streak_for_habit,
    get_longest_streak_overall,
    get_struggled_habits
)
from src.predefined import get_predefined_habits_for_testing

@pytest.fixture
def predefined_habits():
    return get_predefined_habits_for_testing()

def test_get_all_habits(predefined_habits):
    """Test returning all habits."""
    all_habits = get_all_habits(predefined_habits)
    assert len(all_habits) == 5

def test_get_habits_by_periodicity(predefined_habits):
    """Test filtering by periodicity."""
    daily_habits = get_habits_by_periodicity(predefined_habits, "daily")
    weekly_habits = get_habits_by_periodicity(predefined_habits, "weekly")
    
    assert len(daily_habits) == 3
    assert len(weekly_habits) == 2

def test_get_longest_streak_for_habit(predefined_habits):
    """Test getting longest streak for a specific habit."""
    workout = predefined_habits[3]
    assert get_longest_streak_for_habit(workout) == 4 # 4 weeks completed

def test_get_longest_streak_overall(predefined_habits):
    """Test getting the longest streak among all habits."""
    # Brush teeth has a 28-day streak, which is the highest
    assert get_longest_streak_overall(predefined_habits) == 28

def test_get_struggled_habits(predefined_habits):
    """Test identifying struggled (broken) habits over the last month."""
    struggled = get_struggled_habits(predefined_habits)
    
    # Water (missed 1 day), Read (missed weekends), Call Parents (missed 2 weeks)
    assert len(struggled) == 3
    names = [h.name for h in struggled]
    assert "Drink 2L Water" in names
    assert "Read 30 mins" in names
    assert "Call Parents" in names