from typing import List

from models import Round, Match, Tournament

from .base import BaseCommand
from .context import Context


class AdvanceRoundCmd(BaseCommand):
    """
    Command to advance the tournament to the next round.

    Generates match pairings based on tournament scores,
    updates round index, saves the tournament state, and
    prevents advancement past the total number of rounds.
    """

    def __init__(self, tournament: Tournament) -> None:
        """
        Initialize the AdvanceRoundCmd.

        Args:
            tournament (Tournament): The tournament to update.
        """
        self.tournament: Tournament = tournament

    def confirm_round_advance(self) -> bool:
        """
        Prompt the user to confirm advancing to the next round.

        Returns:
            bool: True if user confirms; False otherwise.
        """
        answer: str = input("Advance to next round? (y/n): ").strip().lower()
        return answer == "y"

    def generate_match_pairings(self) -> List[Match]:
        """
        Generate match pairings for the new round based on
        cumulative player scores (descending).

        Returns:
            List[Match]: A list of new match pairings.
        """
        scores: dict = self.tournament.player_scores()
        sorted_players: List = [
            p for p, _ in sorted(scores.items(), key=lambda x: x[1], reverse=True)
        ]

        matches: List[Match] = []
        for i in range(0, len(sorted_players), 2):
            matches.append(
                Match(player1=sorted_players[i], player2=sorted_players[i + 1])
            )

        return matches

    def save_tournament(self) -> None:
        """
        Save the updated tournament state to disk.
        """
        self.tournament.save()

    def execute(self) -> Context:
        """
        Execute the round advancement process.

        Checks if the tournament has started and if more rounds are allowed.
        If confirmed, generates pairings and appends a new round.

        Returns:
            Context: Updated context for the tournament view screen.
        """
        if self.tournament.current_round_index == -1:
            print("Cannot advance: Tournament has not been started.")
            return Context(screen="tournament-view", tournament=self.tournament)

        if self.tournament.current_round_index + 1 >= self.tournament.num_rounds:
            print("All rounds have been played. The tournament is complete.")
            self.tournament.is_complete = True
            self.save_tournament()
            return Context(screen="tournament-view", tournament=self.tournament)

        if not self.confirm_round_advance():
            return Context(screen="tournament-view", tournament=self.tournament)

        matches: List[Match] = self.generate_match_pairings()
        next_round_number: int = self.tournament.current_round_index + 1

        new_round: Round = Round(
            matches=matches,
            round_number=next_round_number,
        )
        self.tournament.rounds.append(new_round)
        self.tournament.current_round_index = next_round_number

        if next_round_number + 1 >= self.tournament.num_rounds:
            self.tournament.is_complete = True

        self.save_tournament()
        return Context(screen="tournament-view", tournament=self.tournament)
