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
        self.tournament = tournament

    def generate_match_pairings(self) -> List[Match]:
        """
        Generate match pairings for the new round based on
        cumulative player scores (descending).

        Returns:
            List[Match]: A list of new match pairings.
        """
        scores = self.tournament.player_scores()
        registrants_by_id = {p["chess_id"]: p for p in self.tournament.players}
        sorted_players = [
            registrants_by_id[cid]
            for cid in sorted(scores, key=scores.get, reverse=True)
        ]

        matches = [
            Match(player1=sorted_players[i], player2=sorted_players[i + 1])
            for i in range(0, len(sorted_players), 2)
        ]
        return matches

    def execute(self) -> Context:
        """
        Executes the round advancement.

        Returns:
            Context: Updated tournament view.
        """
        if self.tournament.current_round_index == -1:
            return Context(
                "tournament-view",
                tournament=self.tournament,
                message="Cannot advance: Tournament has not been started.",
            )

        matches = self.generate_match_pairings()
        next_round_number = self.tournament.current_round_index + 1

        new_round = Round(round_number=next_round_number, matches=matches)
        self.tournament.rounds.append(new_round)
        self.tournament.current_round_index = next_round_number

        self.tournament.save()
        return Context("tournament-view", tournament=self.tournament)
