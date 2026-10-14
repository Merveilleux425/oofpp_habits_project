# src/habit.py
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

class Habit:
    """
    Represents a habit to be tracked periodically.
    
    Attributes:
        id (int): Unique identifier for the habit.
        name (str): Short name of the habit (e.g., "Brush teeth").
        specification (str): Detailed description of the task.
        periodicity (str): Frequency of the habit ("daily" or "weekly").
        created_at (datetime): When the habit was created.
        completions (List[datetime]): List of timestamps when the task was completed.
    """
    
    def __init__(self, id: int, name: str, specification: str, periodicity: str, created_at: datetime, completions: Optional[List[datetime]] = None):
        self.id = id
        self.name = name
        self.specification = specification
        self.periodicity = periodicity.lower()
        self.created_at = created_at
        self.completions = completions if completions is not None else []
        
        # Sort completions to ensure chronological order for streak calculations
        self.completions.sort()

    def complete_task(self, timestamp: Optional[datetime] = None) -> None:
        """
        Marks the habit as complete by adding a timestamp to the completions list.
        
        Args:
            timestamp (datetime, optional): The time of completion. Defaults to now.
        """
        if timestamp is None:
            timestamp = datetime.now()
        self.completions.append(timestamp)
        self.completions.sort()

    def _get_period_key(self, dt: datetime) -> Tuple[int, int]:
        """
        Generates a unique key for the period of a given datetime.
        Used to group completions by day or week.
        
        Args:
            dt (datetime): The datetime to generate a key for.
            
        Returns:
            Tuple[int, int]: A tuple representing (year, day_of_year) or (year, week_of_year).
        """
        if self.periodicity == "daily":
            return (dt.year, dt.timetuple().tm_yday)
        elif self.periodicity == "weekly":
            iso = dt.isocalendar()
            return (iso[0], iso[1]) # (ISO year, ISO week number)
        else:
            raise ValueError(f"Unsupported periodicity: {self.periodicity}")

    def get_longest_streak(self) -> int:
        """
        Calculates the longest streak of consecutive periods where the habit was completed.
        
        Returns:
            int: The longest streak in periods (days or weeks).
        """
        if not self.completions:
            return 0
            
        # Extract unique periods that have at least one completion
        periods = sorted(list(set(self._get_period_key(c) for c in self.completions)))
        
        longest = 1
        current_streak = 1
        
        for i in range(1, len(periods)):
            # Check if the current period is exactly 1 step after the previous period
            prev_period = periods[i-1]
            curr_period = periods[i]
            
            if self.periodicity == "daily":
                prev_dt = datetime(prev_period[0], 1, 1) + timedelta(days=prev_period[1] - 1)
                curr_dt = datetime(curr_period[0], 1, 1) + timedelta(days=curr_period[1] - 1)
                if (curr_dt - prev_dt).days == 1:
                    current_streak += 1
                else:
                    longest = max(longest, current_streak)
                    current_streak = 1
            elif self.periodicity == "weekly":
                # For weeks, we can calculate the difference in ISO weeks
                # Note: This requires handling year boundaries carefully.
                # A simpler way is to convert back to datetime and check if difference is 7 days.
                prev_dt = datetime.fromisocalendar(prev_period[0], prev_period[1], 1)
                curr_dt = datetime.fromisocalendar(curr_period[0], curr_period[1], 1)
                if (curr_dt - prev_dt).days == 7:
                    current_streak += 1
                else:
                    longest = max(longest, current_streak)
                    current_streak = 1
                    
        return max(longest, current_streak)

    def get_current_streak(self) -> int:
        """
        Calculates the current ongoing streak. 
        Counts backwards from the current period.
        
        Returns:
            int: The current streak in periods.
        """
        if not self.completions:
            return 0
            
        now = datetime.now()
        current_period = self._get_period_key(now)
        
        # Get unique periods sorted descending
        periods = sorted(list(set(self._get_period_key(c) for c in self.completions)), reverse=True)
        
        # If the most recent completion isn't in the current period or the previous period, streak is 0
        if periods[0] != current_period:
            # Check if it was completed in the previous period (grace period logic)
            if self.periodicity == "daily":
                prev_period = self._get_period_key(now - timedelta(days=1))
            elif self.periodicity == "weekly":
                prev_period = self._get_period_key(now - timedelta(weeks=1))
            else:
                return 0
                
            if periods[0] != prev_period:
                return 0
        
        # Count consecutive periods
        streak = 1
        for i in range(len(periods) - 1):
            curr = periods[i]
            nxt = periods[i+1]
            
            if self.periodicity == "daily":
                curr_dt = datetime(curr[0], 1, 1) + timedelta(days=curr[1] - 1)
                nxt_dt = datetime(nxt[0], 1, 1) + timedelta(days=nxt[1] - 1)
                if (curr_dt - nxt_dt).days == 1:
                    streak += 1
                else:
                    break
            elif self.periodicity == "weekly":
                curr_dt = datetime.fromisocalendar(curr[0], curr[1], 1)
                nxt_dt = datetime.fromisocalendar(nxt[0], nxt[1], 1)
                if (curr_dt - nxt_dt).days == 7:
                    streak += 1
                else:
                    break
                    
        return streak

    def is_broken(self) -> bool:
        """
        Determines if the habit has been broken.
        A habit is broken if the user missed completing it in the current period 
        AND the previous period. (If they missed the previous period, they broke it).
        
        Returns:
            bool: True if the habit is currently broken.
        """
        if not self.completions:
            return True
            
        now = datetime.now()
        current_period = self._get_period_key(now)
        
        if self.periodicity == "daily":
            prev_period = self._get_period_key(now - timedelta(days=1))
        elif self.periodicity == "weekly":
            prev_period = self._get_period_key(now - timedelta(weeks=1))
        else:
            return True
            
        last_completion_period = self._get_period_key(self.completions[-1])
        
        # If the last completion was before the previous period, the habit is broken.
        return last_completion_period < prev_period

    def __str__(self) -> str:
        """String representation of the habit."""
        return f"[{self.id}] {self.name} ({self.periodicity}) - Created: {self.created_at.strftime('%Y-%m-%d')} - Completions: {len(self.completions)}"