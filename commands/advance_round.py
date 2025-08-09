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

    def _current_round(self) -> Round | None:
        idx = self.tournament.current_round_index
        if 0 <= idx < len(self.tournament.rounds):
            return self.tournament.rounds[idx]
        return None

    def generate_match_pairings(self) -> List[Match]:
        """
        Generate match pairings for the new round, sorted by descending score.
        Players are paired in order (1st vs 2nd, 3rd vs 4th, etc.).

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
        Advance to the next round if available.
        - Creates the next round with pairings.

        Returns:
            Context: Updated tournament view.
        """
        last_index = self.tournament.num_rounds - 1

        if self.tournament.current_round_index == last_index:
            current_round = self._current_round()
            if current_round and current_round.is_complete:
                self.tournament.is_complete = True
                self.tournament.save()
                return Context(
                    "tournament-view",
                    tournament=self.tournament,
                    message="Tournament is now complete.",
                )
            return Context(
                "tournament-view",
                tournament=self.tournament,
                message="Final round is in progress. Enter match results to complete the tournament.",
            )

        next_index = (
            0
            if self.tournament.current_round_index == -1
            else self.tournament.current_round_index + 1
        )

        matches = self.generate_match_pairings()

        new_round = Round(round_number=next_index + 1, matches=matches)
        self.tournament.rounds.append(new_round)
        self.tournament.current_round_index = next_index

        self.tournament.save()

        return Context("tournament-view", tournament=self.tournament)
