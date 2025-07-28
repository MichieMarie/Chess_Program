from dataclasses import dataclass
from typing import Optional

from .player import Player


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
    winner: Optional[str] = None  # "player1", "player2", "draw", or None
    completed: bool = False

    def is_draw(self) -> bool:
        """
        Check if match is a draw.
        Returns:
            bool: True if a match is completed with no winners; False otherwise.
        """
        return self.completed and self.winner == "draw"

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
        if self.winner == "draw":
            return 0.5
        if self.winner == "player1" and player == self.player1:
            return 1.0
        if self.winner == "player2" and player == self.player2:
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
        if winner not in {"player1", "player2", "draw"}:
            raise ValueError("Winner must be 'player1', 'player2', or 'draw'")
        self.winner = winner
        self.completed = True

    def serialize(self) -> dict:
        """Converts the match into a dictionary suitable for JSON serialization.

        Returns:
            dict: A dictionary with player IDs, winner, and completion status."""
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
