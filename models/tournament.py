from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional
import json

from .round import Round
from .player import Player


@dataclass
class Tournament:
    """
    Represents a chess tournament.

    Attributes:
        name (str): The name of the tournament.
        start_date (datetime): When the tournament begins.
        end_date (datetime): When the tournament ends.
        venue (str): The location of the tournament.
        players (List[dict[str, str]]): List of tournament registrants,
            each with 'name', 'chess_id', and 'club_name'.
        rounds (List[Round]): List of rounds in the tournament.
        current_round_index (int): Index of the active round (-1 if none started).
        num_rounds (int): Total number of rounds planned.
        filepath (Optional[Path]): Path to the tournament's JSON file.
        is_complete (bool): True if the tournament has concluded.
    """

    name: str
    start_date: datetime
    end_date: datetime
    venue: str
    players: List[dict[str, str]] = field(default_factory=list)
    rounds: List[Round] = field(default_factory=list)
    current_round_index: int = -1
    num_rounds: int = 4
    filepath: Optional[Path] = None
    is_complete: bool = False

    @staticmethod
    def tournament_registrant(player: Player) -> dict[str, str]:
        """
        Extracts minimal tournament registration info from a full Player object.

        Args:
            player (Player): A Player instance.

        Returns:
            dict[str, str]: Dictionary with name, club_name, and chess_id.
        """
        return {
            "name": player.name,
            "chess_id": player.chess_id,
            "club_name": player.club_name,
        }

    @staticmethod
    def tournament_players(players: List[Player]) -> List[dict[str, str]]:
        """
        Converts a list of Player objects into tournament registration format.

        Args:
            players (List[Player]): List of Player instances.

        Returns:
            List[dict[str, str]]: Simplified player info for tournament storage.
        """
        return [Tournament.tournament_registrant(p) for p in players]

    def player_scores(self) -> dict[str, float]:
        scores: dict[str, float] = {p["chess_id"]: 0.0 for p in self.players}
        for rnd in self.rounds:
            for match in rnd.matches:
                for player in [match.player1, match.player2]:
                    cid = match._get_chess_id(player)
                    scores[cid] += match.get_points(player)
        return scores

    def to_dict(self) -> dict:
        """
        Converts the tournament to a dictionary suitable for JSON serialization.
        """
        return {
            "name": self.name,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "venue": self.venue,
            "players": self.players,
            "rounds": [rnd.serialize() for rnd in self.rounds],
            "current_round_index": self.current_round_index,
            "num_rounds": self.num_rounds,
            "is_complete": self.is_complete,
        }

    @classmethod
    def from_dict(cls, data: dict, filepath: Optional[Path] = None) -> Tournament:
        """
        Create a Tournament instance from a dictionary (e.g., loaded from JSON).
        Handles both modern and legacy round formats.

        Args:
            data (dict): The dictionary of tournament data.
            filepath (Optional[Path]): Filepath to the tournament file.

        Returns:
            Tournament: The reconstructed Tournament instance.
        """
        return cls(
            name=data["name"],
            start_date=datetime.fromisoformat(data["start_date"]),
            end_date=datetime.fromisoformat(data["end_date"]),
            venue=data["venue"],
            players=data.get("players", []),
            rounds=[Round.deserialize(r) for r in data.get("rounds", [])],
            current_round_index=data.get("current_round_index", -1),
            num_rounds=data.get("num_rounds", 4),
            filepath=filepath,
            is_complete=data.get("is_complete", False),
        )

    def save(self) -> None:
        """
        Save the current tournament state to its JSON file.
        """
        if not self.filepath:
            raise ValueError("No filepath provided for saving.")
        with open(self.filepath, "w") as f:
            json.dump(self.to_dict(), f, default=str, indent=2)

        print(f"[DEBUG] Saving tournament to: {self.filepath}")
