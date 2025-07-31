from dataclasses import dataclass
from typing import Optional

from .player import Player


PLAYER1 = "player1"
PLAYER2 = "player2"
DRAW = "draw"


@dataclass
class Match:
    """
    Represents a single match between two players in a round. Supports both Player objects and minimal dicts.

    Attributes:
        player1 (Player): The first player.
        player2 (Player): The second player.
        winner (Optional[str]): "player1", "player2", "draw", or None.
        completed (bool): True if match has been completed.
    """

    player1: Player | dict
    player2: Player | dict
    winner: Optional[str] = None
    completed: bool = False

    def _get_name(self, player: Player | dict) -> str:
        """
        Retrieves the name for a tournament registrant.

        Supports both full Player objects and minimal tournament player dictionaries.

        Args:
            player (Player or dict): The registrant to extract the registrant name from.

        Returns:
            str: The registrant's name.
        """
        return player.name if hasattr(player, "name") else player["name"]

    def _get_chess_id(self, player: Player | dict) -> str:
        """
        Retrieves the chess ID for a tournament registrant.

        Supports both full Player objects and minimal tournament player dictionaries.

        Args:
            player (Player or dict): The registrant to extract the chess ID from.

        Returns:
            str: The registrant's chess ID.
        """
        return player.chess_id if hasattr(player, "chess_id") else player["chess_id"]

    def _get_club(self, player: Player | dict) -> str:
        """
        Retrieves the club name for a tournament registrant.

        Supports both full Player objects and minimal tournament player dictionaries.

        Args:
            player (Player or dict): The registrant to extract the club name from.

        Returns:
            str: The registrant's club name.
        """
        return player.club_name if hasattr(player, "club_name") else player["club_name"]

    def is_draw(self) -> bool:
        """
        Check if match is a draw.
        Returns:
            bool: True if a match is completed with no winners; False otherwise.
        """
        return self.completed and self.winner == DRAW

    def get_points(self, player: Player | dict) -> float:
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
        if self.winner == PLAYER1 and self._get_chess_id(player) == self._get_chess_id(
            self.player1
        ):
            return 1.0
        if self.winner == PLAYER2 and self._get_chess_id(player) == self._get_chess_id(
            self.player2
        ):
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
            winner_id = self._get_chess_id(self.player1)
        elif self.winner == PLAYER2:
            winner_id = self._get_chess_id(self.player2)
        else:
            winner_id = None

        return {
            "players": [
                self._get_chess_id(self.player1),
                self._get_chess_id(self.player2),
            ],
            "winner": winner_id,
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
