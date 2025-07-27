from typing import TYPE_CHECKING

from .context import Context
from .base import BaseCommand

if TYPE_CHECKING:
    from models import Tournament, Match


class MatchResultsCmd(BaseCommand):
    def __init__(self, tournament: "Tournament") -> None:
        self.tournament: "Tournament" = tournament

    def execute(self) -> Context:
        current_index: int = self.tournament.current_round_index
        current_round = self.tournament.rounds[current_index]

        for idx, match in enumerate(current_round.matches, 1):
            match: "Match"  # inline type hint
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
