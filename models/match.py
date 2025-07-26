from dataclasses import dataclass
from typing import Optional

from .player import Player


@dataclass
class Match:
    """
    Represents a single match between two players in a round.
    """

    player1: Player
    player2: Player
    winner: Optional[str] = None  # "player1", "player2", "draw", or None
    completed: bool = False

    def is_draw(self) -> bool:
        """Returns True if the match ended in a draw."""
        return self.completed and self.winner == "draw"

    def get_points(self, player: Player) -> float:
        """
        Returns how many points the given player earned in this match.
        - 1.0 for a win
        - 0.5 for a draw
        - 0.0 for a loss or incomplete match
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
        Acceptable values for `winner`: "player1", "player2", "draw"
        """
        if winner not in {"player1", "player2", "draw"}:
            raise ValueError("Winner must be 'player1', 'player2', or 'draw'")
        self.winner = winner
        self.completed = True

    def serialize(self) -> dict:
        """Converts the match to a JSON-serializable dictionary."""
        return {
            "players": [self.player1.chess_id, self.player2.chess_id],
            "winner": self.winner,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data: dict, players_by_id: dict) -> "Match":
        """
        Reconstructs a Match from a dictionary and a lookup of players by chess_id.
        The key 'players' should be a list of 2 chess IDs.
        """
        player1_id, player2_id = data["players"]
        return cls(
            player1=players_by_id[player1_id],
            player2=players_by_id[player2_id],
            winner=data.get("winner"),
            completed=data.get("completed", False),
        )
