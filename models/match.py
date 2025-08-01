from dataclasses import dataclass
from typing import Optional

from .player import Player


PLAYER1 = "player1"
PLAYER2 = "player2"
DRAW = "draw"


@dataclass
class Match:
    """
    Represents a single match between two tournament registrants in a round.

    Supports both full Player objects and minimal tournament registrant dictionaries
    (with 'name', 'chess_id', and 'club_name').

    Attributes:
        player1 (Player | dict): The first registrant.
        player2 (Player | dict): The second registrant.
        winner (Optional[str]): "player1", "player2", "draw", or None.
        completed (bool): True if the match has been completed.
    """

    player1: Player | dict
    player2: Player | dict
    winner: Optional[str] = None
    completed: bool = False

    def _get_name(self, player: Player | dict) -> str:
        """
        Retrieves the name for a tournament registrant.

        Args:
            player (Player | dict): The registrant.

        Returns:
            str: The registrant's name.
        """
        return player.name if hasattr(player, "name") else player["name"]

    def _get_chess_id(self, player: Player | dict) -> str:
        """
        Retrieves the chess ID for a tournament registrant.

        Args:
            player (Player | dict): The registrant.

        Returns:
            str: The registrant's chess ID.
        """
        return player.chess_id if hasattr(player, "chess_id") else player["chess_id"]

    def _get_club(self, player: Player | dict) -> str:
        """
        Retrieves the club name for a tournament registrant.

        Args:
            player (Player | dict): The registrant.

        Returns:
            str: The registrant's club name.
        """
        return player.club_name if hasattr(player, "club_name") else player["club_name"]

    def is_draw(self) -> bool:
        """
        Check if the match ended in a draw.

        Returns:
            bool: True if completed and no winner declared.
        """
        return self.completed and self.winner == DRAW

    def get_points(self, player: Player | dict) -> float:
        """
        Calculates how many points the given registrant earned in this match.

        Args:
            player (Player | dict): The registrant to evaluate.

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
            ValueError: If the winner argument is not valid.
        """
        if winner not in {PLAYER1, PLAYER2, DRAW}:
            raise ValueError("Winner must be 'player1', 'player2', or 'draw'")
        self.winner = winner
        self.completed = True

    def serialize(self) -> dict:
        """
        Serializes the match data for JSON output.

        Returns:
            dict: Contains chess IDs of both players, winner ID, and completion status.
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
    def from_dict(cls, data: dict, players_by_id: dict[str, Player | dict]) -> "Match":
        """
        Reconstructs a Match from serialized data and registrants-by-ID lookup.

        Args:
            data (dict): Contains 'players', 'winner', and 'completed' keys.
            players_by_id (dict): Maps chess_id to registrants (either Player or dict).

        Returns:
            Match: Reconstructed match instance.
        """
        player1_id, player2_id = data["players"]
        return cls(
            player1=players_by_id[player1_id],
            player2=players_by_id[player2_id],
            winner=data.get("winner"),
            completed=data.get("completed", False),
        )
