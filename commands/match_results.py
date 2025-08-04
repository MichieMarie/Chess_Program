from models import Tournament
from models.match import PLAYER1, PLAYER2, DRAW

from .context import Context
from .base import BaseCommand


class MatchResultsCmd(BaseCommand):
    """
    Command to enter results for selected matches in the current round of a tournament.

    Attributes:
        tournament (Tournament): The tournament being updated.
    """

    def __init__(self, tournament: Tournament, results: dict[int, str]) -> None:
        """
        Initialize the command.

        Args:
            tournament (Tournament): The tournament being updated.
            results (dict[int, str]): Match index mapped to result ("1", "2", or "d").
        """
        self.tournament = tournament
        self.results = results

    def execute(self) -> Context:
        """
        Applies results to selected matches in the current round.

        Returns:
            Context: Updated context returning to the tournament view.
        """
        current_index = self.tournament.current_round_index

        if current_index < 0 or current_index >= len(self.tournament.rounds):
            return Context(
                "tournament-view",
                tournament=self.tournament,
                message="No active round to enter results for. Use 'Advance Round' first.",
            )

        current_round = self.tournament.rounds[current_index]

        for index, result in self.results.items():
            if 0 <= index < len(current_round.matches):
                match = current_round.matches[index]
                if result == "1":
                    match.update_result(PLAYER1)
                elif result == "2":
                    match.update_result(PLAYER2)
                elif result == "d":
                    match.update_result(DRAW)

        self.tournament.save()
        return Context("tournament-view", tournament=self.tournament)
