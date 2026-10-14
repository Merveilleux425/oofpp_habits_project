# tests/test_tracker.py
import pytest
from datetime import datetime
from src.tracker import HabitTracker

@pytest.fixture
def tracker():
    """Fixture for an empty in-memory database tracker."""
    return HabitTracker(db_path=":memory:")

def test_add_habit(tracker):
    """Test creating a habit."""
    habit = tracker.add_habit("Test", "Test spec", "daily")
    assert habit.id is not None
    assert len(tracker.get_all_habits()) == 1
    assert habit.name == "Test"

def test_complete_task(tracker):
    """Test completing a task and verifying it saves."""
    habit = tracker.add_habit("Test", "Test spec", "daily")
    success = tracker.complete_task(habit.id)
    
    assert success == True
    assert len(habit.completions) == 1
    
    # Verify it persists in the DB by reloading the tracker
    tracker2 = HabitTracker(db_path=":memory:") # Wait, in-memory is lost. 
    # Let's just check the in-memory state for this test, DB integration is tested below.
    
def test_delete_habit(tracker):
    """Test deleting a habit."""
    habit = tracker.add_habit("Test", "Test spec", "daily")
    assert len(tracker.get_all_habits()) == 1
    
    success = tracker.delete_habit(habit.id)
    assert success == True
    assert len(tracker.get_all_habits()) == 0

def test_persistence(tmp_path):
    """Test that data survives between sessions using a temporary file."""
    db_file = tmp_path / "test_habits.db"
    
    # Session 1: Create and complete
    tracker1 = HabitTracker(db_path=str(db_file))
    habit = tracker1.add_habit("Persist", "Save to disk", "daily")
    tracker1.complete_task(habit.id)
    
    # Session 2: Load and verify
    tracker2 = HabitTracker(db_path=str(db_file))
    assert len(tracker2.get_all_habits()) == 1
    
    loaded_habit = tracker2.get_all_habits()[0]
    assert loaded_habit.name == "Persist"
    assert len(loaded_habit.completions) == 1