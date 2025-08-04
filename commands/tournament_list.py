from models import TournamentManager

from .base import BaseCommand
from .context import Context


class TournamentListCmd(BaseCommand):
    """
    Command to list all tournaments by descending start date and allow user selection.
    """

    def execute(self) -> Context:
        """
        Execute the command to list tournaments sorted by start date (newest first).

        Returns:
            Context: A context object for the tournament list view, with all tournaments loaded.
        """
        tm = TournamentManager()
        tournaments = sorted(tm.get_all(), key=lambda t: t.start_date, reverse=True)
        return Context("tournament-list", tournaments=tournaments)
