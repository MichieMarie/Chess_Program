from typing import List
from models import Round, Match, Tournament

from .base import BaseCommand
from .context import Context


class AdvanceRoundCmd(BaseCommand):
    """
    Command to advance the tournament to the next round.

    Generates match pairings based on tournament scores,
    updates round index, and saves the tournament state.

    Attributes:
        tournament (Tournament): The tournament to operate on.
    """

    def __init__(self, tournament: Tournament) -> None:
        """
        Initialize the command with the given tournament.

        Args:
            tournament (Tournament): The tournament being updated.
        """
        self.tournament: Tournament = tournament

    def confirm_round_advance(self) -> bool:
        """
        Prompt the user to confirm advancing to the next round.

        Returns:
            bool: True if user confirms; False otherwise.
        """
        answer = input("Advance to next round? (y/n): ").strip().lower()
        return answer == "y"

    def generate_match_pairings(self) -> List[Match]:
        """
        Generate match pairings based on cumulative tournament scores.

        Returns:
            List[Match]: Match pairings sorted by player scores.
        """
        scores = self.tournament.player_scores
        sorted_players = [
            p for p, _ in sorted(scores.items(), key=lambda x: x[1], reverse=True)
        ]

        matches = []
        for i in range(0, len(sorted_players), 2):
            matches.append(
                Match(player1=sorted_players[i], player2=sorted_players[i + 1])
            )

        return matches

    def save_tournament(self) -> None:
        """
        Save the current tournament state to disk.
        """
        self.tournament.save()

    def execute(self) -> Context:
        """
        Advance the tournament to the next round and return the updated context.

        Returns:
            Context: The next screen context for the updated tournament view.
        """
        if self.tournament.current_round_index == -1:
            print("Cannot advance: Tournament has not been started.")
            return Context(screen="tournament-view", tournament=self.tournament)

        if not self.confirm_round_advance():
            return Context(screen="tournament-view", tournament=self.tournament)

        matches = self.generate_match_pairings()
        next_round_number = self.tournament.current_round_index + 1

        new_round = Round(
            matches=matches,
            round_number=next_round_number,
        )
        self.tournament.rounds.append(new_round)
        self.tournament.current_round_index = next_round_number
        self.save_tournament()

        return Context(screen="tournament-view", tournament=self.tournament)
