from datetime import datetime
from models import TournamentManager, Tournament

from .context import Context
from .base import BaseCommand


class CreateTournamentCmd(BaseCommand):
    """Command to create a new tournament"""

    def __init__(self, name: str) -> None:
        self.name: str = name

    def execute(self) -> Context:
        """Prompts for tournament dates and creates the tournament"""
        tm: TournamentManager = TournamentManager()

        def prompt_date(prompt: str) -> datetime.date:
            while True:
                user_input = input(prompt + " (YYYY-MM-DD): ")
                try:
                    return datetime.strptime(user_input, "%Y-%m-%d").date()
                except ValueError:
                    print("Invalid format. Please use YYYY-MM-DD.")

        start_date = prompt_date("Enter tournament start date")
        end_date = prompt_date("Enter tournament end date")

        if end_date < start_date:
            print("End date cannot be before start date.")
            return Context("main")

        tournament: Tournament = tm.create(
            name=self.name, start_date=start_date, end_date=end_date
        )

        return Context("tournament-view", tournament=tournament)
