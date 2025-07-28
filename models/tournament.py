from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date, datetime
from pathlib import Path
import json

from .player import Player
from .round import Round


@dataclass
class Tournament:
    """
    Represents a local chess tournament.

    Attributes:
        name (str): Name of the tournament.
        start_date (date): Tournament start date.
        end_date (date): Tournament end date.
        venue (Optional[str]): Venue where the tournament is held.
        players (List[Player]): Registered players.
        rounds (List[Round]): Rounds of the tournament.
        current_round_index (Optional[int]): Index of the current round (0-based).
        filepath (Optional[Path]): Filepath for saving to disk.
    """

    name: str
    start_date: date
    end_date: date
    venue: Optional[str] = None

    players: List[Player] = field(default_factory=list)
    rounds: List[Round] = field(default_factory=list)
    current_round_index: Optional[int] = None

    filepath: Optional[Path] = None

    def is_active(self) -> bool:
        """
        Determines if the tournament is currently active based on the date.

        Returns:
            bool: True if today is between the start and end dates, inclusive.
        """
        today: date = date.today()
        return self.start_date <= today <= self.end_date

    def is_complete(self) -> bool:
        """
        Checks whether the tournament has ended.

        Returns:
            bool: True if today's date is after the end date.
        """
        return date.today() > self.end_date

    def save(self) -> None:
        """
        Saves the tournament data to the file specified in `filepath`.

        Raises:
            ValueError: If no filepath is specified.
        """
        if not self.filepath:
            raise ValueError("No filepath provided for saving.")
        with open(self.filepath, "w") as f:
            json.dump(self.to_dict(), f, default=str, indent=2)

    def to_dict(self) -> dict:
        """
        Converts the tournament to a dictionary suitable for JSON serialization.

        Returns:
            dict: Serialized tournament data.
        """
        return {
            "name": self.name,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "venue": self.venue,
            "players": [p.serialize() for p in self.players],
            "rounds": [rnd.serialize() for rnd in self.rounds],
            "current_round_index": self.current_round_index,
        }

    @classmethod
    def from_dict(cls, data: dict, filepath: Optional[Path] = None) -> "Tournament":
        """
        Reconstructs a Tournament from dictionary data and an optional file path.

        Args:
            data (dict): Dictionary containing tournament data.
            filepath (Optional[Path]): Path to the tournament JSON file, if any.

        Returns:
            Tournament: A reconstructed Tournament instance.
        """
        player_objs = [Player(**p) for p in data.get("players", [])]
        players_by_id = {p.chess_id: p for p in player_objs}

        rounds = [
            Round.from_list(rnd_data, players_by_id, round_number=i + 1)
            for i, rnd_data in enumerate(data.get("rounds", []))
        ]

        return cls(
            name=data["name"],
            start_date=datetime.fromisoformat(data["start_date"]).date(),
            end_date=datetime.fromisoformat(data["end_date"]).date(),
            venue=data.get("venue"),
            players=player_objs,
            rounds=rounds,
            current_round_index=data.get("current_round_index"),
            filepath=filepath,
        )

    @property
    def player_scores(self) -> dict[Player, float]:
        """
        Calculates total points earned by each player in the tournament.

        Returns:
            dict[Player, float]: Dictionary mapping Player objects to total points earned.
        """
        scores = {p: 0.0 for p in self.players}

        for rnd in self.rounds:
            for match in rnd.matches:
                for player in (match.player1, match.player2):
                    scores[player] += match.get_points(player)

        return scores
