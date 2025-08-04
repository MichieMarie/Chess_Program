from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional
import json

from .match import Match
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

    @property
    def is_overdue(self) -> bool:
        """
        Indicates whether the tournament has passed its end date but is not complete.

        Returns:
            bool: True if today is after end date and not complete.
        """
        return datetime.today().date() > self.end_date.date() and not self.is_complete

    @property
    def status_label(self) -> str:
        """
        Returns a string label describing the current status of the tournament.

        Returns:
            str: One of [Upcoming], [Active], [Completed], or [Overdue]
        """
        today = datetime.today().date()

        if self.is_complete:
            return "[Completed]"
        elif today < self.start_date.date():
            return "[Upcoming]"
        elif self.is_overdue:
            return "[Overdue]"
        return "[Active]"

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
        players = data.get("players", [])
        players_by_id = {p["chess_id"]: p for p in players}

        # Deserialize rounds and rebuild matches as Match objects
        rounds = []
        for round_data in data.get("rounds", []):
            match_objs = [
                Match.from_dict(m, players_by_id) for m in round_data.get("matches", [])
            ]
            round_obj = Round(
                round_number=round_data.get("round_number", 1),
                matches=match_objs,
                is_complete=round_data.get("is_complete", False),
            )
            rounds.append(round_obj)

        return cls(
            name=data["name"],
            start_date=datetime.fromisoformat(data["start_date"]),
            end_date=datetime.fromisoformat(data["end_date"]),
            venue=data["venue"],
            players=players,
            rounds=rounds,
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
