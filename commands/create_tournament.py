from datetime import datetime
from models import TournamentManager, Tournament
from .context import Context
from .base import BaseCommand


class CreateTournamentCmd(BaseCommand):
    """
    Command to create a new tournament.

    Expects data for tournament name, venue, dates, and number of rounds
    to be provided during initialization (typically from a screen).
    """

    def __init__(
        self,
        name: str,
        start_date: datetime,
        end_date: datetime,
        venue: str | None,
        num_rounds: int,
    ) -> None:
        """
        Initialize the tournament creation command with user-provided data.

        Args:
            name (str): Name of the tournament.
            start_date (date): Start date.
            end_date (date): End date.
            venue (str | None): Venue name or None if blank.
            num_rounds (int): Total number of rounds.
        """
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.venue = venue
        self.num_rounds = num_rounds

    def execute(self) -> Context:
        """
        Executes the tournament creation using pre-gathered data.

        Returns:
            Context: Context showing the newly created tournament.
        """
        tm: TournamentManager = TournamentManager()
        tournament: Tournament = tm.create(
            name=self.name,
            start_date=self.start_date,
            end_date=self.end_date,
            venue=self.venue,
            num_rounds=self.num_rounds,
        )
        return Context("tournament-view", tournament=tournament)
