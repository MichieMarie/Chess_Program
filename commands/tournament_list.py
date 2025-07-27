from datetime import date
from typing import List, Optional

from models import TournamentManager, Tournament

from .base import BaseCommand
from .context import Context


class TournamentListCmd(BaseCommand):
    """Command to list all tournaments by descending start date and allow selection"""

    def get_all_tournaments_sorted(self) -> List[Tournament]:
        """Get all tournaments sorted by descending start date"""
        tm = TournamentManager()
        return sorted(tm.get_all(), key=lambda t: t.start_date, reverse=True)

    def select_tournament_by_index(
        self, index: int, tournaments: List[Tournament]
    ) -> Optional[Tournament]:
        """Select a tournament from the list by its index"""
        if 1 <= index <= len(tournaments):
            return tournaments[index - 1]
        return None

    def get_status_label(self, tournament: Tournament) -> str:
        """
        Returns a label describing the tournament's status.
        - [Upcoming]: Starts in the future
        - [Active]: Today is between start and end date
        - [Completed]: Tournament is over
        """
        today = date.today()
        if tournament.start_date > today:
            return "[Upcoming]"
        elif tournament.end_date < today:
            return "[Completed]"
        return "[Active]"

    def print_tournament_list(self, tournaments: List[Tournament]) -> None:
        """Displays a numbered list of tournaments with their name, dates, and status"""
        print("\nAvailable Tournaments:\n")
        for i, t in enumerate(tournaments, 1):
            status = self.get_status_label(t)
            print(f"{i}. {t.name} ({t.start_date} to {t.end_date}) {status}")

    def execute(self) -> Context:
        """Displays tournaments and lets the user select one"""
        tournaments = self.get_all_tournaments_sorted()

        if not tournaments:
            print("No tournaments available.")
            return Context("main")

        self.print_tournament_list(tournaments)

        try:
            choice = int(input("\nSelect a tournament by number: "))
            selected = self.select_tournament_by_index(choice, tournaments)
            if selected:
                return Context("tournament-view", tournament=selected)
        except ValueError:
            pass

        print("Invalid selection. Returning to main menu.")
        return Context("main")
