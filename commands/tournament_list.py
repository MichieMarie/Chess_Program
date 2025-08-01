from models import TournamentManager

from .base import BaseCommand
from .context import Context


class TournamentListCmd(BaseCommand):
    """
    Command to list all tournaments by descending start date and allow user selection.
    """

    def execute(self) -> Context:
        """
        Executes the command to list tournaments and return the selected tournament view.

        Returns:
            Context: The context for the selected tournament list screen.
        """
        tm = TournamentManager()
        tournaments = sorted(tm.get_all(), key=lambda t: t.start_date, reverse=True)
        return Context("tournament-list", tournaments=tournaments)
