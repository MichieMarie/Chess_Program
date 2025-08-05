from models import Tournament

from .base import BaseCommand
from .context import Context


class RegisterPlayerCmd(BaseCommand):
    """
    Command to navigate to the player search screen for registering participants into a tournament.

    Attributes:
        tournament (Tournament): The tournament players are registering into.
    """

    def __init__(self, tournament: Tournament) -> None:
        """
        Initialize the command with the given tournament.

        Args:
            tournament (Tournament): The tournament being updated.
        """
        self.tournament = tournament

    def execute(self) -> Context:
        """
        Executes the search command by sending the user to the player search screen.

        Returns:
            Context: The player search context for the given tournament.
        """
        return Context("player-search", tournament=self.tournament)
