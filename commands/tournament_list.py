from datetime import date
from typing import List, Optional

from models import TournamentManager, Tournament

from .base import BaseCommand
from .context import Context


class TournamentListCmd(BaseCommand):
    """
    Command to list all tournaments by descending start date and allow user selection.
    """

    def get_all_tournaments_sorted(self) -> List[Tournament]:
        """
        Get all tournaments sorted by descending start date.

        Returns:
            List[Tournament]: List of tournaments sorted by descending start date.
        """
        tm = TournamentManager()
        return sorted(tm.get_all(), key=lambda t: t.start_date, reverse=True)

    def print_tournament_list(self, tournaments: List[Tournament]) -> None:
        """
        Displays a numbered list of tournaments with name, venue, dates, and status.

        Args:
            tournaments (List[Tournament]): The tournaments to display.
        """
        print("\nAvailable Tournaments:\n")
        for i, t in enumerate(tournaments, 1):
            status = self.get_status_label(t)
            print(f"{i}. {t.name} {t.venue} ({t.start_date} to {t.end_date}) {status}")

    def get_status_label(self, tournament: Tournament) -> str:
        """
        Returns a label describing the tournament's status.

        - [Upcoming]: Starts in the future
        - [Active]: Today is between start and end date
        - [Completed]: Tournament is over

        Args:
            tournament (Tournament): The tournament to evaluate.

        Returns:
            str: A label indicating the tournament status.
        """
        today = date.today()
        if tournament.start_date > today:
            return "[Upcoming]"
        elif tournament.end_date < today:
            return "[Completed]"
        return "[Active]"

    def select_tournament_by_index(
        self, index: int, tournaments: List[Tournament]
    ) -> Optional[Tournament]:
        """
        Select a tournament from the list by its index.

        Args:
            index (int): Index of the tournament to select.
            tournaments (List[Tournament]): List of available tournaments.

        Returns:
            Optional[Tournament]: The selected tournament, or None if invalid.
        """
        if 1 <= index <= len(tournaments):
            return tournaments[index - 1]
        return None

    def execute(self) -> Context:
        """
        Executes the command to list tournaments and return the selected tournament view.

        Returns:
            Context: The context for the selected tournament, or home if no valid selection.
        """
        tournaments = self.get_all_tournaments_sorted()

        if not tournaments:
            print("No tournaments found.")
            return Context("home")

        self.print_tournament_list(tournaments)

        try:
            index = int(
                input("\nEnter the number of the tournament to manage: ").strip()
            )
        except ValueError:
            print("Invalid input.")
            return Context("home")

        tournament = self.select_tournament_by_index(index, tournaments)
        if tournament:
            return Context("tournament-view", tournament=tournament)

        print("Invalid selection.")
        return Context("main-menu")
