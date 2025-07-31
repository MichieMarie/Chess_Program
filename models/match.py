from dataclasses import dataclass
from typing import Optional

from .player import Player


PLAYER1 = "player1"
PLAYER2 = "player2"
DRAW = "draw"


@dataclass
class Match:
    """
    Represents a single match between two players in a round.

    Attributes:
        player1 (Player): The first player.
        player2 (Player): The second player.
        winner (Optional[str]): "player1", "player2", "draw", or None.
        completed (bool): True if match has been completed.
    """

    player1: Player
    player2: Player
    winner: str | None = None
    completed: bool = False

    def is_draw(self) -> bool:
        """
        Check if match is a draw.
        Returns:
            bool: True if a match is completed with no winners; False otherwise.
        """
        return self.completed and self.winner == DRAW

    def get_points(self, player: Player) -> float:
        """
        Calculates how many points the given player earned in this match.

        Args:
            player (Player): The player to evaluate.

        Returns:
            float: 1.0 for a win, 0.5 for a draw, 0.0 for a loss or if incomplete.
        """
        if not self.completed:
            return 0.0
        if self.winner == DRAW:
            return 0.5
        if self.winner == PLAYER1 and player == self.player1:
            return 1.0
        if self.winner == PLAYER2 and player == self.player2:
            return 1.0
        return 0.0

    def update_result(self, winner: str) -> None:
        """
         Sets the result of the match.

        Args:
            winner (str): One of "player1", "player2", or "draw".

        Raises:
            ValueError: If the winner argument is not one of the accepted values.
        """
        if winner not in {PLAYER1, PLAYER2, DRAW}:
            raise ValueError("Winner must be 'player1', 'player2', or 'draw'")
        self.winner = winner
        self.completed = True

    def serialize(self) -> dict:
        """
        Serializes the match data to a dictionary for JSON output.

        Returns:
            dict: A dictionary with player IDs, winner, and completion status.
        """
        if self.winner == DRAW:
            winner_id = None
        elif self.winner == PLAYER1:
            winner_id = self.player1.chess_id
        elif self.winner == PLAYER2:
            winner_id = self.player2.chess_id
        else:
            winner_id = None

        return {
            "players": [self.player1.chess_id, self.player2.chess_id],
            "winner": self.winner,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data: dict, players_by_id: dict) -> "Match":
        """
        Reconstructs a Match object from a dictionary.

        Args:
            data (dict): Dictionary with keys 'players', 'winner', and 'completed'.
            players_by_id (dict): Dictionary mapping chess_id to Player objects.

        Returns:
            Match: The reconstructed Match object.
        """
        player1_id, player2_id = data["players"]
        return cls(
            player1=players_by_id[player1_id],
            player2=players_by_id[player2_id],
            winner=data.get("winner"),
            completed=data.get("completed", False),
        )
