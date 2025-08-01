from random import shuffle
from typing import List

from models import Tournament, Round, Match

from .base import BaseCommand
from .context import Context


class StartTournamentCmd(BaseCommand):
    """
    Command to start a tournament by creating the first round with randomized pairings.

    Attributes:
        tournament (Tournament): The tournament to operate on.
    """

    def __init__(self, tournament: Tournament) -> None:
        """
        Initialize the command with the given tournament.

        Args:
            tournament (Tournament): The tournament to start.
        """
        self.tournament = tournament

    def tournament_already_started(self) -> bool:
        """
        Check if the tournament has already started.

        Returns:
            bool: True if a round already exists; False otherwise.
        """
        return self.tournament.current_round_index >= 0

    def random_match_assignment(self) -> List[Match]:
        """
        Randomly shuffle players and create match pairings.

        Returns:
            List[Match]: A list of randomized matchups.

        Raises:
            ValueError: If the number of players is not even.
        """
        players = self.tournament.players[:]

        if len(players) % 2 != 0:
            raise ValueError("Tournament must have an even number of players.")

        shuffle(players)

        matches = [
            Match(player1=players[i], player2=players[i + 1])
            for i in range(0, len(players), 2)
        ]
        return matches

    def execute(self) -> Context:
        """
        Starts the tournament by creating and saving the first round.

        Returns:
            Context: The updated tournament view.
        """
        if self.tournament_already_started():
            print("Tournament has already started.")
            return Context("tournament-view", tournament=self.tournament)

        try:
            matches = self.random_match_assignment()
        except ValueError as e:
            print(f"Error: {e}")
            return Context("tournament-view", tournament=self.tournament)

        first_round = Round(round_number=1, matches=matches)
        self.tournament.rounds.append(first_round)
        self.tournament.current_round_index = 0
        self.tournament.save()

        print("Tournament started. Round 1 created.")
        return Context("tournament-view", tournament=self.tournament)
