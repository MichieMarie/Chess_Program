from models import TournamentManager, Tournament

from .context import Context
from .base import BaseCommand


class CreateTournamentCmd(BaseCommand):
    """Command to create a new tournament"""

    def __init__(self, name: str) -> None:
        self.name: str = name

    def execute(self) -> Context:
        """Uses a TournamentManager instance to create a new tournament"""
        tm: TournamentManager = TournamentManager()
        tournament: Tournament = tm.create(name=self.name)
        return Context("tournament-view", tournament=tournament)
