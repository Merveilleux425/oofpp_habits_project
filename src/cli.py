# src/cli.py
import click
from datetime import datetime
from src.tracker import HabitTracker
from src.analytics import (
    get_all_habits,
    get_habits_by_periodicity,
    get_longest_streak_overall,
    get_longest_streak_for_habit,
    get_struggled_habits
)
from src.predefined import populate_predefined_habits

@click.group()
@click.pass_context
def cli(ctx):
    """Habit Tracker App - Manage and analyze your daily and weekly habits."""
    # Initialize tracker and attach to context so commands can access it
    ctx.obj = HabitTracker()

@cli.command()
@click.option('--name', prompt='Habit Name', help='Short name of the habit.')
@click.option('--spec', prompt='Specification', help='Detailed description of the task.')
@click.option('--periodicity', prompt='Periodicity (daily/weekly)', type=click.Choice(['daily', 'weekly']), help='Frequency of the habit.')
def create(name, spec, periodicity):
    """Create a new habit."""
    tracker = HabitTracker()
    habit = tracker.add_habit(name, spec, periodicity)
    click.echo(f"Success! Habit '{habit.name}' created with ID {habit.id}.")

@cli.command()
@click.argument('habit_id', type=int)
def complete(habit_id):
    """Mark a habit as complete for the current period."""
    tracker = HabitTracker()
    if tracker.complete_task(habit_id):
        click.echo(f"Success! Habit {habit_id} marked as complete.")
    else:
        click.echo(f"Error: Habit with ID {habit_id} not found.")

@cli.command()
@click.argument('habit_id', type=int)
def delete(habit_id):
    """Delete a habit and its history."""
    tracker = HabitTracker()
    if tracker.delete_habit(habit_id):
        click.echo(f"Success! Habit {habit_id} deleted.")
    else:
        click.echo(f"Error: Habit with ID {habit_id} not found.")

@cli.command()
def list_habits():
    """List all currently tracked habits."""
    tracker = HabitTracker()
    habits = get_all_habits(tracker.get_all_habits())
    if not habits:
        click.echo("No habits found. Try creating one or loading predefined data!")
        return
        
    click.echo("\n--- Your Habits ---")
    for h in habits:
        click.echo(h)

@cli.command()
@click.argument('periodicity', type=click.Choice(['daily', 'weekly']))
def analyze_periodicity(periodicity):
    """List habits filtered by periodicity."""
    tracker = HabitTracker()
    habits = get_habits_by_periodicity(tracker.get_all_habits(), periodicity)
    
    click.echo(f"\n--- {periodicity.capitalize()} Habits ---")
    for h in habits:
        click.echo(h)

@cli.command()
def analyze_streaks():
    """Show the longest streak overall and individual streaks."""
    tracker = HabitTracker()
    habits = tracker.get_all_habits()
    
    longest = get_longest_streak_overall(habits)
    click.echo(f"\nLongest streak across all habits: {longest} periods")
    
    click.echo("\n--- Individual Longest Streaks ---")
    for h in habits:
        streak = get_longest_streak_for_habit(h)
        click.echo(f"{h.name}: {streak} periods")

@cli.command()
def analyze_struggles():
    """Show habits you struggled with in the last 30 days."""
    tracker = HabitTracker()
    struggled = get_struggled_habits(tracker.get_all_habits())
    
    if not struggled:
        click.echo("Great job! No struggled habits in the last 30 days.")
        return
        
    click.echo("\n--- Struggled Habits (Last 30 Days) ---")
    for h in struggled:
        click.echo(f"{h.name} (Current streak: {h.get_current_streak()})")

@cli.command()
def load_fixtures():
    """Loads the 5 predefined habits and 4 weeks of example data."""
    tracker = HabitTracker()
    if len(tracker.get_all_habits()) > 0:
        click.echo("Database already has habits. Clear the database first to load fixtures.")
        return
        
    populate_predefined_habits(tracker)
    click.echo("Success! 5 predefined habits and 4 weeks of data loaded.")

if __name__ == '__main__':
    cli()