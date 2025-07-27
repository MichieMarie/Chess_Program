from random import shuffle
from typing import List

from models import Round, Match, Tournament

from .base import BaseCommand
from .context import Context


class AdvanceRoundCmd(BaseCommand):
    """Command to advance the tournament to the next round, handling match generation."""

    def __init__(self, tournament: Tournament) -> None:
        """Initialize with the tournament to operate on."""
        self.tournament: Tournament = tournament

    def confirm_round_advance(self) -> bool:
        """Prompt the user to confirm advancing to the next round."""
        answer = input("Advance to next round? (y/n): ").strip().lower()
        return answer == "y"

    def random_match_assignment(self) -> List[Match]:
        """Generate random match pairings for the first round."""
        players = self.tournament.players[:]
        shuffle(players)

        matches = []
        for i in range(0, len(players), 2):
            player1 = players[i]
            player2 = players[i + 1]
            matches.append(Match(player1=player1, player2=player2))

        return matches

    def calc_match_assignment(self) -> List[Match]:
        """Generate match pairings based on cumulative tournament scores."""
        scores = self.tournament.get_player_scores()
        sorted_players = [
            p for p, _ in sorted(scores.items(), key=lambda x: x[1], reverse=True)
        ]

        matches = []
        for i in range(0, len(sorted_players), 2):
            player1 = sorted_players[i]
            player2 = sorted_players[i + 1]
            matches.append(Match(player1=player1, player2=player2))

        return matches

    def match_list(self) -> List[Match]:
        """Return the appropriate match list based on whether it's the first round."""
        if self.tournament.current_round_index == -1:
            return self.random_match_assignment()
        return self.calc_match_assignment()

    def save_tournament(self) -> None:
        """Save the tournament state to disk."""
        self.tournament.save()

    def execute(self) -> Context:
        """Advance the tournament to the next round and return the next screen context."""
        if not self.confirm_round_advance():
            return Context(screen="tournament-view", tournament=self.tournament)

        matches = self.match_list()
        new_round = Round(
            matches=matches,
            round_number=self.tournament.current_round_index + 1,
        )
        self.tournament.rounds.append(new_round)
        self.tournament.current_round_index += 1
        self.save_tournament()

        return Context(screen="tournament-view", tournament=self.tournament)
