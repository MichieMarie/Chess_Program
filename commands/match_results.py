from .context import Context
from .base import BaseCommand

from models import Tournament, Match


class MatchResultsCmd(BaseCommand):
    """
    Command to enter results for all matches in the current round of a tournament.

    Attributes:
        tournament (Tournament): The tournament being updated.
    """

    def __init__(self, tournament: Tournament) -> None:
        """
        Initialize the command with the given tournament.

        Args:
            tournament (Tournament): The tournament to update.
        """
        self.tournament: Tournament = tournament

    def execute(self) -> Context:
        """
        Prompts the user to enter the results for each match in the current round.

        Returns:
            Context: Updated context returning to the tournament view.
        """
        current_index: int = self.tournament.current_round_index

        if current_index < 0 or current_index >= len(self.tournament.rounds):
            print(
                "No round in progress. Use 'Advance Round' to start one before entering results."
            )
            return Context("tournament-view", tournament=self.tournament)

        current_round = self.tournament.rounds[current_index]

        for idx, match in enumerate(current_round.matches, 1):
            match: Match
            print(f"\nMatch {idx}: {match.player1.name} vs {match.player2.name}")
            while True:
                result: str = input("Who won? (1/2/d for draw): ").strip().lower()
                if result == "1":
                    match.update_result("player1")
                    break
                elif result == "2":
                    match.update_result("player2")
                    break
                elif result == "d":
                    match.update_result("draw")
                    break
                else:
                    print("Invalid input. Type 1, 2, or d.")

        self.tournament.save()
        return Context("tournament-view", tournament=self.tournament)
